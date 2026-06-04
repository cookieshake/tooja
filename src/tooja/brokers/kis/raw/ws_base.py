"""KIS WebSocket subscriber base.

KIS realtime data flow:
1. POST /oauth2/Approval (REST) returns ``approval_key``.
2. Connect to ws://ops.koreainvestment.com:21000 (real) / :31000 (virtual).
3. Send JSON subscribe message:
   ``{"header": {"approval_key": ..., "custtype": "P", "tr_type": "1",
                  "content-type": "utf-8"},
      "body": {"input": {"tr_id": "<TR_ID>", "tr_key": "<KEY>"}}}``
4. Server pushes pipe-delimited frames: ``<encrypted>|<tr_id>|<count>|<body>``
   where ``body`` contains ``count`` records, each with fields joined by ``^``.
"""

from __future__ import annotations

import json
import logging
from typing import AsyncGenerator, ClassVar, Generic, TypeVar

import websockets
from pydantic import BaseModel

logger = logging.getLogger(__name__)

REAL_WS_URL = "ws://ops.koreainvestment.com:21000"
VIRTUAL_WS_URL = "ws://ops.koreainvestment.com:31000"

TR_TYPE_SUBSCRIBE = "1"
TR_TYPE_UNSUBSCRIBE = "2"

TResponse = TypeVar("TResponse", bound=BaseModel)


class WsSubscriber(Generic[TResponse]):
    """Subscriber for a single KIS realtime TR.

    Subclass sets ``TR_ID``, ``RESPONSE_TYPE``, ``COLUMNS`` (response field order).
    """

    TR_ID: ClassVar[str]
    RESPONSE_TYPE: ClassVar[type]
    COLUMNS: ClassVar[tuple[str, ...]]
    CUST_TYPE: ClassVar[str] = "P"

    def __init__(
        self,
        approval_key: str,
        tr_key: str,
        is_virtual: bool = False,
        url: str | None = None,
    ):
        self.approval_key = approval_key
        self.tr_key = tr_key
        self.is_virtual = is_virtual
        self.url = url or (VIRTUAL_WS_URL if is_virtual else REAL_WS_URL)

    def _subscribe_message(self, tr_type: str) -> str:
        return json.dumps({
            "header": {
                "approval_key": self.approval_key,
                "custtype": self.CUST_TYPE,
                "tr_type": tr_type,
                "content-type": "utf-8",
            },
            "body": {"input": {"tr_id": self.TR_ID, "tr_key": self.tr_key}},
        })

    async def subscribe(self) -> AsyncGenerator[TResponse, None]:
        """Connect, subscribe, yield messages. Auto-unsubscribes when ``async for`` exits."""
        async with websockets.connect(self.url) as ws:
            await ws.send(self._subscribe_message(TR_TYPE_SUBSCRIBE))
            try:
                async for raw in ws:
                    parsed = self._parse_frame(raw)
                    for record in parsed:
                        yield record
            finally:
                try:
                    await ws.send(self._subscribe_message(TR_TYPE_UNSUBSCRIBE))
                except Exception as e:
                    logger.warning("Unsubscribe send failed: %s", e)

    def _parse_frame(self, raw: str | bytes) -> list[TResponse]:
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="replace")

        # Control frames (PINGPONG / SUBSCRIBE ACK / ...) arrive as JSON.
        if raw.startswith("{"):
            return self._handle_control(raw)

        # Data frame: <flag>|<tr_id>|<count>|<body>
        try:
            flag, tr_id, count_str, body = raw.split("|", 3)
        except ValueError:
            logger.warning("Unexpected ws frame: %s", raw[:200])
            return []

        if tr_id != self.TR_ID:
            return []

        try:
            count = int(count_str)
        except ValueError:
            count = 1

        fields_per_record = len(self.COLUMNS)
        tokens = body.split("^")
        records: list[TResponse] = []
        for i in range(count):
            chunk = tokens[i * fields_per_record : (i + 1) * fields_per_record]
            if len(chunk) != fields_per_record:
                break
            data = dict(zip(self.COLUMNS, chunk))
            records.append(self.RESPONSE_TYPE(**data))
        return records

    def _handle_control(self, raw: str) -> list[TResponse]:
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError:
            return []
        rt_cd = msg.get("body", {}).get("rt_cd")
        msg_cd = msg.get("body", {}).get("msg_cd")
        msg1 = msg.get("body", {}).get("msg1")
        if rt_cd not in (None, "0"):
            logger.error("WS subscribe error: rt_cd=%s msg_cd=%s msg1=%s", rt_cd, msg_cd, msg1)
        else:
            logger.debug("WS control: %s", msg)
        return []
