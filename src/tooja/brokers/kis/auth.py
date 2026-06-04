"""KIS OAuth token + WS approval_key lifecycle.

Tokens are valid 24h; KIS reissues the same token within a 6h window.
We cache to disk so adjacent processes / restarts don't burn the rate limit.

Cache layout (.kis-spec/):
    token.json         -> {access_token, expires_at}
    approval_key.json  -> {approval_key, issued_at}

Storage path is `.kis-spec/` per user policy (already in .gitignore).
"""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import TYPE_CHECKING

import httpx

from tooja.brokers.kis.raw.base import KisApiError
from tooja.brokers.kis.raw.oauth.approval import ApprovalExecutor, ApprovalRequest
from tooja.brokers.kis.raw.oauth.tokenp import TokenpExecutor, TokenpRequest
from tooja.core.errors import AuthError

if TYPE_CHECKING:
    from tooja.brokers.kis.credentials import KisCredentials

logger = logging.getLogger(__name__)

_CACHE_DIR = Path(".kis-spec")
_TOKEN_FILE = _CACHE_DIR / "token.json"
_APPROVAL_FILE = _CACHE_DIR / "approval_key.json"
_TOKEN_REFRESH_MARGIN = timedelta(minutes=10)
_APPROVAL_TTL = timedelta(hours=23)


@dataclass(frozen=True)
class TokenCache:
    access_token: str
    expires_at: datetime

    def expired(self, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return now >= self.expires_at - _TOKEN_REFRESH_MARGIN


@dataclass(frozen=True)
class ApprovalCache:
    approval_key: str
    issued_at: datetime

    def expired(self, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return now >= self.issued_at + _APPROVAL_TTL


def _read_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("Failed to read cache %s: %s", path, e)
        return None


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _load_token() -> TokenCache | None:
    raw = _read_json(_TOKEN_FILE)
    if raw is None:
        return None
    try:
        return TokenCache(
            access_token=raw["access_token"],
            expires_at=datetime.fromisoformat(raw["expires_at"]),
        )
    except (KeyError, ValueError) as e:
        logger.warning("Token cache malformed: %s", e)
        return None


def _save_token(token: TokenCache) -> None:
    _write_json(_TOKEN_FILE, {
        "access_token": token.access_token,
        "expires_at": token.expires_at.isoformat(),
    })


def _load_approval() -> ApprovalCache | None:
    raw = _read_json(_APPROVAL_FILE)
    if raw is None:
        return None
    try:
        return ApprovalCache(
            approval_key=raw["approval_key"],
            issued_at=datetime.fromisoformat(raw["issued_at"]),
        )
    except (KeyError, ValueError) as e:
        logger.warning("Approval cache malformed: %s", e)
        return None


def _save_approval(approval: ApprovalCache) -> None:
    _write_json(_APPROVAL_FILE, {
        "approval_key": approval.approval_key,
        "issued_at": approval.issued_at.isoformat(),
    })


class TokenManager:
    """Per-broker token lifecycle.

    Methods:
        get_token() -> str — returns cached or freshly-issued access_token
        get_approval_key() -> str — returns cached or freshly-issued WS approval_key
        invalidate_token() — drops in-memory + disk cache (call on EGW00123)
    """

    def __init__(
        self,
        credentials: "KisCredentials",
        *,
        base_url: str,
        is_virtual: bool,
        http: httpx.AsyncClient,
    ):
        self._creds = credentials
        self._base_url = base_url
        self._is_virtual = is_virtual
        self._http = http
        self._token: TokenCache | None = _load_token()
        self._approval: ApprovalCache | None = _load_approval()
        self._token_lock = asyncio.Lock()
        self._approval_lock = asyncio.Lock()

    async def get_token(self) -> str:
        if self._token and not self._token.expired():
            return self._token.access_token
        async with self._token_lock:
            if self._token and not self._token.expired():
                return self._token.access_token
            self._token = await self._issue_token()
            _save_token(self._token)
            return self._token.access_token

    async def get_approval_key(self) -> str:
        if self._approval and not self._approval.expired():
            return self._approval.approval_key
        async with self._approval_lock:
            if self._approval and not self._approval.expired():
                return self._approval.approval_key
            self._approval = await self._issue_approval()
            _save_approval(self._approval)
            return self._approval.approval_key

    def invalidate_token(self) -> None:
        self._token = None
        try:
            _TOKEN_FILE.unlink(missing_ok=True)
        except OSError as e:
            logger.warning("Failed to delete %s: %s", _TOKEN_FILE, e)

    async def _issue_token(self) -> TokenCache:
        req = TokenpRequest(
            grant_type="client_credentials",
            appkey=self._creds.app_key,
            appsecret=self._creds.app_secret,
        )
        try:
            resp = await TokenpExecutor(
                req,
                base_url=self._base_url,
                is_virtual=self._is_virtual,
                client=self._http,
            ).execute()
        except KisApiError as e:
            raise AuthError(
                f"KIS token issue failed: {e.message}",
                broker="kis",
                raw_code=e.code,
                raw_message=e.message,
                endpoint="/oauth2/tokenP",
            ) from e

        if not resp.access_token or resp.expires_in is None:
            raise AuthError(
                "KIS token response missing access_token/expires_in",
                broker="kis",
                endpoint="/oauth2/tokenP",
            )

        now = datetime.now(timezone.utc)
        return TokenCache(
            access_token=resp.access_token,
            expires_at=now + timedelta(seconds=int(resp.expires_in)),
        )

    async def _issue_approval(self) -> ApprovalCache:
        req = ApprovalRequest(
            grant_type="client_credentials",
            appkey=self._creds.app_key,
            secretkey=self._creds.app_secret,
        )
        try:
            resp = await ApprovalExecutor(
                req,
                base_url=self._base_url,
                is_virtual=self._is_virtual,
                client=self._http,
            ).execute()
        except KisApiError as e:
            raise AuthError(
                f"KIS approval_key issue failed: {e.message}",
                broker="kis",
                raw_code=e.code,
                raw_message=e.message,
                endpoint="/oauth2/Approval",
            ) from e

        if not resp.approval_key:
            raise AuthError(
                "KIS approval response missing approval_key",
                broker="kis",
                endpoint="/oauth2/Approval",
            )

        return ApprovalCache(
            approval_key=resp.approval_key,
            issued_at=datetime.now(timezone.utc),
        )
