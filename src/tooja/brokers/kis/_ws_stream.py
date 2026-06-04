"""Unified KIS WebSocket subscription stream.

One WS connection per stream instance. Each symbol subscribed adds a per-tr_id
subscribe frame. Incoming pipe-delimited frames are split into records and
handed to a per-tr_id mapper to produce Quote / Trade / Orderbook / OrderUpdate.

Reconnect on close (when auto_reconnect=True) by reissuing all currently-known
subscribes; the consumer sees a StreamControlEvent(kind="reconnected").
"""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING, AsyncIterator, Callable, Generic, TypeVar

import websockets
from websockets.exceptions import ConnectionClosed

from tooja.brokers.kis.raw.ws_base import (
    REAL_WS_URL, TR_TYPE_SUBSCRIBE, TR_TYPE_UNSUBSCRIBE, VIRTUAL_WS_URL,
)
from tooja.core.errors import BrokerError
from tooja.core.models import StreamControlEvent, Symbol

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker

logger = logging.getLogger(__name__)

T = TypeVar("T")

Mapper = Callable[[dict[str, str]], object | None]


async def _safe_send(ws, payload: str) -> None:
    """Send a payload that we don't care about the outcome of (e.g. PINGPONG
    echo). Swallow ConnectionClosed and similar — the reader loop will see the
    same condition and handle reconnection."""
    try:
        await ws.send(payload)
    except Exception as e:  # noqa: BLE001 — best-effort fire-and-forget
        logger.debug("KIS WS background send failed: %s", e)


class _SubscriptionTopic:
    """A (tr_id, COLUMNS, mapper) bundle used by the stream."""

    def __init__(self, tr_id: str, columns: tuple[str, ...], mapper: Mapper):
        self.tr_id = tr_id
        self.columns = columns
        self.mapper = mapper


class KisWsStream(Generic[T]):
    """Base implementation of `_SymbolStream`-shaped interface for KIS WS.

    Subclasses pick a `_SubscriptionTopic` and message type T.
    """

    def __init__(
        self,
        broker: "KisBroker",
        topic: _SubscriptionTopic,
        symbols: list[Symbol | str],
        *,
        include_control: bool,
        auto_reconnect: bool,
        buffer_size: int,
    ):
        self._broker = broker
        self._topic = topic
        self._include_control = include_control
        self._auto_reconnect = auto_reconnect
        self._buffer_size = buffer_size
        self._symbols: set[Symbol] = {self._as_symbol(s) for s in symbols}
        self._ws: websockets.WebSocketClientProtocol | None = None
        self._queue: asyncio.Queue[T] = asyncio.Queue(maxsize=buffer_size)
        self._reader_task: asyncio.Task | None = None
        self._url: str = VIRTUAL_WS_URL if broker.is_virtual else REAL_WS_URL
        self._closed = False

    @staticmethod
    def _as_symbol(s: Symbol | str) -> Symbol:
        return s if isinstance(s, Symbol) else Symbol.parse(s)

    @property
    def symbols(self) -> frozenset[Symbol]:
        return frozenset(self._symbols)

    @property
    def auto_reconnect(self) -> bool:
        return self._auto_reconnect

    async def subscribe(self, symbol: Symbol | str) -> None:
        sym = self._as_symbol(symbol)
        if sym in self._symbols and self._ws is not None:
            return
        self._symbols.add(sym)
        if self._ws is not None:
            await self._send_subscribe(sym, TR_TYPE_SUBSCRIBE)
            if self._include_control:
                await self._queue.put(self._control("subscribed", [sym]))  # type: ignore[arg-type]

    async def unsubscribe(self, symbol: Symbol | str) -> None:
        sym = self._as_symbol(symbol)
        if sym not in self._symbols:
            return
        self._symbols.discard(sym)
        if self._ws is not None:
            await self._send_subscribe(sym, TR_TYPE_UNSUBSCRIBE)
            if self._include_control:
                await self._queue.put(self._control("unsubscribed", [sym]))  # type: ignore[arg-type]

    async def __aenter__(self) -> "KisWsStream[T]":
        await self._connect_and_subscribe()
        self._reader_task = asyncio.create_task(self._reader_loop())
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self._closed = True
        if self._reader_task is not None:
            self._reader_task.cancel()
            try:
                await self._reader_task
            except (asyncio.CancelledError, Exception):
                pass
        if self._ws is not None:
            await self._ws.close()
            self._ws = None

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def __anext__(self) -> T:
        if self._closed and self._queue.empty():
            raise StopAsyncIteration
        return await self._queue.get()

    async def _connect_and_subscribe(self) -> None:
        approval = await self._broker.get_approval_key()
        self._approval = approval
        self._ws = await websockets.connect(self._url)
        try:
            for sym in list(self._symbols):
                await self._send_subscribe(sym, TR_TYPE_SUBSCRIBE)
        except Exception:
            # Don't leak the freshly-opened socket if subscribe fails midway.
            try:
                await self._ws.close()
            finally:
                self._ws = None
            raise

    async def _send_subscribe(self, sym: Symbol, tr_type: str) -> None:
        if self._ws is None:
            raise BrokerError("KIS WS not connected", broker="kis")
        msg = json.dumps({
            "header": {
                "approval_key": self._approval,
                "custtype": "P",
                "tr_type": tr_type,
                "content-type": "utf-8",
            },
            "body": {"input": {"tr_id": self._topic.tr_id, "tr_key": sym.ticker}},
        })
        await self._ws.send(msg)

    async def _reader_loop(self) -> None:
        while not self._closed:
            try:
                if self._ws is None:
                    await self._connect_and_subscribe()
                assert self._ws is not None
                async for raw in self._ws:
                    for item in self._parse(raw):
                        await self._queue.put(item)
            except ConnectionClosed:
                if not self._auto_reconnect or self._closed:
                    break
                logger.warning("KIS WS closed — reconnecting")
                self._ws = None
                if self._include_control:
                    await self._queue.put(self._control("disconnected", []))  # type: ignore[arg-type]
                await asyncio.sleep(1.0)
                continue
            except Exception as e:
                logger.exception("KIS WS reader loop error: %s", e)
                if not self._auto_reconnect or self._closed:
                    break
                self._ws = None
                await asyncio.sleep(1.0)
                continue

    def _parse(self, raw: str | bytes) -> list:
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="replace")
        if raw.startswith("{"):
            return self._handle_control(raw)
        try:
            flag, tr_id, count_str, body = raw.split("|", 3)
        except ValueError:
            return []
        if tr_id != self._topic.tr_id:
            return []
        try:
            count = int(count_str)
        except ValueError:
            count = 1
        per = len(self._topic.columns)
        tokens = body.split("^")
        out: list = []
        for i in range(count):
            chunk = tokens[i * per:(i + 1) * per]
            if len(chunk) != per:
                break
            record = dict(zip(self._topic.columns, chunk))
            mapped = self._topic.mapper(record)
            if mapped is not None:
                out.append(mapped)
        return out

    def _handle_control(self, raw: str) -> list:
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError:
            return []
        header = msg.get("header", {})
        if header.get("tr_id") == "PINGPONG":
            # KIS server-initiated keepalive. Reply with the same frame.
            if self._ws is not None:
                asyncio.create_task(_safe_send(self._ws, raw))
            return []
        rt_cd = msg.get("body", {}).get("rt_cd")
        if rt_cd not in (None, "0"):
            logger.error("KIS WS control error: %s", msg)
        return []

    def _control(self, kind: str, syms: list[Symbol]) -> StreamControlEvent:
        return StreamControlEvent(
            kind=kind,  # type: ignore[arg-type]
            time=datetime.now(timezone.utc),
            symbols_affected=syms,
        )


class KisOrderUpdateStream:
    """Account-scoped my-order WS (no per-symbol subscribe).

    KIS H0STCNI0 subscribes by HTS_ID (tr_key). The single connection delivers
    every order event for that account.
    """

    def __init__(
        self,
        broker: "KisBroker",
        *,
        tr_id: str,
        columns: tuple[str, ...],
        mapper: Mapper,
        include_control: bool,
        auto_reconnect: bool,
        buffer_size: int,
    ):
        self._broker = broker
        self._tr_id = tr_id
        self._columns = columns
        self._mapper = mapper
        self._include_control = include_control
        self._auto_reconnect = auto_reconnect
        self._queue: asyncio.Queue = asyncio.Queue(maxsize=buffer_size)
        self._ws: websockets.WebSocketClientProtocol | None = None
        self._reader_task: asyncio.Task | None = None
        self._url = VIRTUAL_WS_URL if broker.is_virtual else REAL_WS_URL
        self._closed = False

    @property
    def auto_reconnect(self) -> bool:
        return self._auto_reconnect

    async def __aenter__(self) -> "KisOrderUpdateStream":
        await self._connect()
        self._reader_task = asyncio.create_task(self._reader_loop())
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self._closed = True
        if self._reader_task is not None:
            self._reader_task.cancel()
            try:
                await self._reader_task
            except (asyncio.CancelledError, Exception):
                pass
        if self._ws is not None:
            await self._ws.close()
            self._ws = None

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._closed and self._queue.empty():
            raise StopAsyncIteration
        return await self._queue.get()

    async def _connect(self) -> None:
        approval = await self._broker.get_approval_key()
        self._approval = approval
        self._ws = await websockets.connect(self._url)
        try:
            await self._send_subscribe(TR_TYPE_SUBSCRIBE)
        except Exception:
            try:
                await self._ws.close()
            finally:
                self._ws = None
            raise

    async def _send_subscribe(self, tr_type: str) -> None:
        assert self._ws is not None
        hts_id = self._broker.credentials.hts_id
        msg = json.dumps({
            "header": {
                "approval_key": self._approval,
                "custtype": "P",
                "tr_type": tr_type,
                "content-type": "utf-8",
            },
            "body": {"input": {"tr_id": self._tr_id, "tr_key": hts_id}},
        })
        await self._ws.send(msg)

    async def _reader_loop(self) -> None:
        while not self._closed:
            try:
                if self._ws is None:
                    await self._connect()
                assert self._ws is not None
                async for raw in self._ws:
                    for item in self._parse(raw):
                        await self._queue.put(item)
            except ConnectionClosed:
                if not self._auto_reconnect or self._closed:
                    break
                logger.warning("KIS order WS closed — reconnecting")
                self._ws = None
                if self._include_control:
                    await self._queue.put(StreamControlEvent(
                        kind="disconnected", time=datetime.now(timezone.utc),
                    ))
                await asyncio.sleep(1.0)
                continue
            except Exception as e:
                logger.exception("KIS order WS error: %s", e)
                if not self._auto_reconnect or self._closed:
                    break
                self._ws = None
                await asyncio.sleep(1.0)
                continue

    def _parse(self, raw: str | bytes) -> list:
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="replace")
        if raw.startswith("{"):
            # Handle KIS PINGPONG keepalive — server expects an echo.
            try:
                msg = json.loads(raw)
                if msg.get("header", {}).get("tr_id") == "PINGPONG" and self._ws is not None:
                    asyncio.create_task(_safe_send(self._ws, raw))
            except json.JSONDecodeError:
                pass
            return []
        try:
            flag, tr_id, count_str, body = raw.split("|", 3)
        except ValueError:
            return []
        if tr_id != self._tr_id:
            return []
        try:
            count = int(count_str)
        except ValueError:
            count = 1
        per = len(self._columns)
        tokens = body.split("^")
        out: list = []
        for i in range(count):
            chunk = tokens[i * per:(i + 1) * per]
            if len(chunk) != per:
                break
            record = dict(zip(self._columns, chunk))
            mapped = self._mapper(record)
            if mapped is not None:
                out.append(mapped)
        return out
