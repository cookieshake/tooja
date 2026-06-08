"""Toss OAuth2 client_credentials token lifecycle, persisted via the shared TokenStore."""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

import httpx

from tooja.brokers.toss.raw.base import BASE_URL, TossApiError
from tooja.brokers.toss.raw.auth.issue_o_auth2_token import IssueOAuth2TokenExecutor
from tooja.core.errors import AuthError
from tooja.core.token_cache import CacheMode, TokenStore, scope_tag

if TYPE_CHECKING:
    from tooja.brokers.toss.credentials import TossCredentials

logger = logging.getLogger(__name__)

_TOKEN_REFRESH_MARGIN = timedelta(minutes=5)


@dataclass(frozen=True)
class TossTokenCache:
    access_token: str
    expires_at: datetime

    def expired(self, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return now >= self.expires_at - _TOKEN_REFRESH_MARGIN


class TossTokenManager:
    def __init__(self, credentials: "TossCredentials", *, http: httpx.AsyncClient,
                 base_url: str = BASE_URL, token_cache: CacheMode = "disk"):
        self._creds = credentials
        self._http = http
        self._base_url = base_url
        self._scope = scope_tag(credentials.client_id)
        self._store = TokenStore(namespace="toss", mode=token_cache)
        self._token: TossTokenCache | None = self._load()
        self._lock = asyncio.Lock()

    def _key(self) -> str:
        return f"token_{self._scope}"

    def _load(self) -> TossTokenCache | None:
        raw = self._store.load(self._key())
        if raw is None:
            return None
        try:
            return TossTokenCache(access_token=raw["access_token"],
                                  expires_at=datetime.fromisoformat(raw["expires_at"]))
        except (KeyError, ValueError) as e:
            logger.warning("toss token cache malformed: %s", e)
            return None

    def _cache(self, t: TossTokenCache) -> None:
        self._token = t
        self._store.save(self._key(), {"access_token": t.access_token, "expires_at": t.expires_at.isoformat()})

    def invalidate(self) -> None:
        self._token = None
        self._store.delete(self._key())

    async def get_token(self) -> str:
        if self._token and not self._token.expired():
            return self._token.access_token
        async with self._lock:
            if self._token and not self._token.expired():
                return self._token.access_token
            t = await self._issue()
            self._cache(t)
            return t.access_token

    async def _issue(self) -> TossTokenCache:
        body = {"grant_type": "client_credentials",
                "client_id": self._creds.client_id, "client_secret": self._creds.client_secret}
        try:
            resp = await IssueOAuth2TokenExecutor(body=body, client=self._http, base_url=self._base_url).execute()
        except TossApiError as e:
            raise AuthError(f"Toss token issue failed: {e.message}", broker="toss",
                            raw_code=e.code, raw_message=e.message, endpoint="/oauth2/token") from e
        if not resp.access_token or resp.expires_in is None:
            raise AuthError("Toss token response missing access_token/expires_in", broker="toss", endpoint="/oauth2/token")
        return TossTokenCache(access_token=resp.access_token,
                              expires_at=datetime.now(timezone.utc) + timedelta(seconds=int(resp.expires_in)))
