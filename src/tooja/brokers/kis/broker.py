"""KisBroker — Broker ABC implementation. Interface skeleton; method bodies live in a separate plan."""

from __future__ import annotations

from typing import ClassVar, Literal

import httpx

from tooja.brokers.kis.account import KisAccountClient
from tooja.brokers.kis.analytics import KisAnalyticsClient
from tooja.brokers.kis.credentials import KisCredentials
from tooja.brokers.kis.info import KisInfoClient
from tooja.brokers.kis.market import KisMarketClient
from tooja.brokers.kis.orders import KisOrdersClient
from tooja.brokers.kis.rankings import KisRankingsClient
from tooja.brokers.kis.raw_namespace import KisRawNamespace
from tooja.brokers.kis.stream import KisStreamClient
from tooja.core.broker import Broker
from tooja.core.errors import BrokerError


_REAL_BASE_URL = "https://openapi.koreainvestment.com:9443"
_VIRTUAL_BASE_URL = "https://openapivts.koreainvestment.com:29443"
_HTTP_TIMEOUT_SEC = 30.0
_RATE_LIMIT_REAL = 20
_RATE_LIMIT_DEMO = 2


class KisBroker(Broker):
    """Korea Investment & Securities adapter."""

    broker_name: ClassVar[str] = "kis"

    def __init__(
        self,
        *,
        app_key: str,
        app_secret: str,
        cano: str,
        hts_id: str,
        acnt_prdt_cd: str = "01",
        env: Literal["real", "demo"] = "real",
    ):
        self.env = env
        self.is_virtual = env == "demo"
        self.base_url = _VIRTUAL_BASE_URL if self.is_virtual else _REAL_BASE_URL
        self.rate_limit_per_sec = _RATE_LIMIT_DEMO if self.is_virtual else _RATE_LIMIT_REAL

        self.credentials: KisCredentials = KisCredentials(
            app_key=app_key,
            app_secret=app_secret,
            cano=cano,
            acnt_prdt_cd=acnt_prdt_cd,
            hts_id=hts_id,
        )

        self._http: httpx.AsyncClient | None = None
        self._open = False

        # Attach subclients
        self.market = KisMarketClient(self)
        self.account = KisAccountClient(self)
        self.orders = KisOrdersClient(self)
        self.info = KisInfoClient(self)
        self.analytics = KisAnalyticsClient(self)
        self.rankings = KisRankingsClient(self)
        self.stream = KisStreamClient(self)
        self.raw = KisRawNamespace(self)

    @property
    def is_open(self) -> bool:
        return self._open

    @property
    def http(self) -> httpx.AsyncClient:
        """HTTP session entry point. Accessing before open() raises BrokerError."""
        self._require_open()
        assert self._http is not None  # Always set once _require_open passes.
        return self._http

    def _require_open(self) -> None:
        if not self._open:
            raise BrokerError(
                "KisBroker is not opened — call await broker.open() or use "
                "`async with KisBroker(...) as broker:` before invoking API methods",
                broker=self.broker_name,
            )

    async def open(self) -> None:
        """Prepare session / auth. This plan only flips the lifecycle flag — token /
        approval_key issuance is a separate plan."""
        if self._open:
            return
        if self._http is None:
            self._http = httpx.AsyncClient(base_url=self.base_url, timeout=_HTTP_TIMEOUT_SEC)
        # TODO(separate plan): issue token / load cache / fetch approval_key.
        self._open = True

    async def close(self) -> None:
        """Cleanup session / streams. Always discards the HTTP session regardless of _open.

        Prevents a leak when open() raised mid-way leaving self._open=False but self._http set.
        """
        try:
            if self._http is not None:
                await self._http.aclose()
                self._http = None
        finally:
            self._open = False
