"""TossBroker — Broker ABC implementation over the generated Toss raw layer."""

from __future__ import annotations

from typing import ClassVar

import httpx

from tooja.brokers.toss.account import TossAccountClient
from tooja.brokers.toss.analytics import TossAnalyticsClient
from tooja.brokers.toss.auth import TossTokenManager
from tooja.brokers.toss.credentials import TossCredentials
from tooja.brokers.toss.info import TossInfoClient
from tooja.brokers.toss.market import TossMarketClient
from tooja.brokers.toss.orders import TossOrdersClient
from tooja.brokers.toss.rankings import TossRankingsClient
from tooja.brokers.toss.raw.base import BASE_URL
from tooja.brokers.toss.raw_namespace import TossRawNamespace
from tooja.brokers.toss.stream import TossStreamClient
from tooja.brokers.toss._rate_limit import DEFAULT
from tooja.core.broker import Broker
from tooja.core.errors import BrokerError
from tooja.core.rate_limit import RateLimitConfig, TokenBucket
from tooja.core.token_cache import CacheMode

_HTTP_TIMEOUT_SEC = 30.0


class TossBroker(Broker):
    """Toss Securities adapter."""

    broker_name: ClassVar[str] = "toss"

    def __init__(
        self,
        *,
        client_id: str,
        client_secret: str,
        account_seq: int | None = None,
        token_cache: CacheMode = "disk",
        rate_limit: RateLimitConfig | None = None,
    ):
        self.credentials: TossCredentials = TossCredentials(
            client_id=client_id,
            client_secret=client_secret,
        )
        self.account_seq = account_seq
        self.token_cache: CacheMode = token_cache
        self.base_url = BASE_URL
        self.rate_limit: RateLimitConfig = rate_limit or DEFAULT
        self._rate_limiter = TokenBucket(capacity=self.rate_limit.per_sec)

        self._http: httpx.AsyncClient | None = None
        self._tokens: TossTokenManager | None = None
        self._open = False

        # Attach subclients
        self.market = TossMarketClient(self)
        self.account = TossAccountClient(self)
        self.orders = TossOrdersClient(self)
        self.info = TossInfoClient(self)
        self.analytics = TossAnalyticsClient(self)
        self.rankings = TossRankingsClient(self)
        self.stream = TossStreamClient(self)
        self.raw = TossRawNamespace(self)

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
                "TossBroker is not opened — call await broker.open() or use "
                "`async with TossBroker(...) as broker:` before invoking API methods",
                broker=self.broker_name,
            )

    async def open(self) -> None:
        """Prepare the HTTP session and prime the token manager. Idempotent.

        Token issuance is lazy — the first authenticated call triggers it via
        ``TossTokenManager.get_token()``.
        """
        if self._open:
            return
        if self._http is None:
            self._http = httpx.AsyncClient(
                base_url=self.base_url, timeout=_HTTP_TIMEOUT_SEC
            )
        self._tokens = TossTokenManager(
            self.credentials,
            http=self._http,
            base_url=self.base_url,
            token_cache=self.token_cache,
        )
        self._open = True

    async def close(self) -> None:
        """Cleanup session. Always discards the HTTP session regardless of _open."""
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

    def invalidate_token(self) -> None:
        if self._tokens is not None:
            self._tokens.invalidate()
