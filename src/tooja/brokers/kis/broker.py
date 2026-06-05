"""KisBroker — Broker ABC implementation. Interface skeleton; method bodies live in a separate plan."""

from __future__ import annotations

from typing import ClassVar, Literal

import httpx

from tooja.brokers.kis.account import KisAccountClient
from tooja.brokers.kis.analytics import KisAnalyticsClient
from tooja.brokers.kis._rate_limit import DEFAULT_DEMO, DEFAULT_REAL
from tooja.brokers.kis.auth import TokenManager
from tooja.core.rate_limit import RateLimitConfig, TokenBucket
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
        rate_limit: RateLimitConfig | None = None,
    ):
        self.env = env
        self.is_virtual = env == "demo"
        self.base_url = _VIRTUAL_BASE_URL if self.is_virtual else _REAL_BASE_URL
        self.rate_limit: RateLimitConfig = rate_limit or (
            DEFAULT_DEMO if self.is_virtual else DEFAULT_REAL
        )
        self.rate_limit_per_sec = self.rate_limit.per_sec

        self.credentials: KisCredentials = KisCredentials(
            app_key=app_key,
            app_secret=app_secret,
            cano=cano,
            acnt_prdt_cd=acnt_prdt_cd,
            hts_id=hts_id,
        )

        self._http: httpx.AsyncClient | None = None
        self._tokens: TokenManager | None = None
        self._rate_limiter = TokenBucket(capacity=self.rate_limit.per_sec)
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
        """Prepare HTTP session and prime the token manager.

        Token issuance is lazy — the first authenticated call triggers it via
        TokenManager.get_token(). approval_key likewise issues on first WS use.
        """
        if self._open:
            return
        if self._http is None:
            self._http = httpx.AsyncClient(base_url=self.base_url, timeout=_HTTP_TIMEOUT_SEC)
        self._tokens = TokenManager(
            self.credentials,
            base_url=self.base_url,
            is_virtual=self.is_virtual,
            http=self._http,
        )
        self._open = True

    async def close(self) -> None:
        """Cleanup session / streams. Always discards the HTTP session regardless of _open."""
        try:
            if self._http is not None:
                await self._http.aclose()
                self._http = None
            self._tokens = None
        finally:
            self._open = False

    async def get_access_token(self) -> str:
        self._require_open()
        assert self._tokens is not None
        return await self._tokens.get_token()

    async def get_approval_key(self) -> str:
        self._require_open()
        assert self._tokens is not None
        return await self._tokens.get_approval_key()

    def invalidate_token(self) -> None:
        if self._tokens is not None:
            self._tokens.invalidate_token()

    def build_auth_headers(self, access_token: str, tr_id: str) -> dict[str, str]:
        """Standard header set for an authenticated KIS REST call."""
        return {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {access_token}",
            "appkey": self.credentials.app_key,
            "appsecret": self.credentials.app_secret,
            "tr_id": tr_id,
            "custtype": "P",
        }
