"""Toss OAuth2 token manager: issue, cache (disk/memory), expiry, reissue."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import httpx
import pytest

from tooja.brokers.toss.auth import TossTokenManager, TossTokenCache
from tooja.brokers.toss.credentials import TossCredentials

_NOW = datetime(2026, 6, 1, 9, 0, tzinfo=timezone.utc)


def _creds(cid="cid"):
    return TossCredentials(client_id=cid, client_secret="sec")


@pytest.fixture
def cache_dir(tmp_path, monkeypatch):
    import tooja.core.token_cache as tc
    monkeypatch.setattr(tc.platformdirs, "user_cache_dir", lambda *a, **k: str(tmp_path))
    return tmp_path


def test_token_cache_expiry():
    tcache = TossTokenCache(access_token="X", expires_at=_NOW + timedelta(hours=12))
    assert tcache.expired(now=_NOW) is False
    assert TossTokenCache(access_token="X", expires_at=_NOW + timedelta(minutes=2)).expired(now=_NOW) is True


@pytest.mark.asyncio
async def test_issue_and_cache_token(cache_dir):
    calls = {"n": 0}

    async def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        assert request.url.path == "/oauth2/token"
        # form body carries client_credentials
        body = request.content.decode()
        assert "grant_type=client_credentials" in body
        assert "client_id=cid" in body
        return httpx.Response(200, json={"access_token": "tok-abc", "token_type": "Bearer", "expires_in": 86400})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        mgr = TossTokenManager(_creds(), http=client)
        t1 = await mgr.get_token()
        t2 = await mgr.get_token()  # cached, no 2nd issue
    assert t1 == "tok-abc" and t2 == "tok-abc"
    assert calls["n"] == 1

    # a fresh manager (disk mode default) reloads from cache without issuing
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        mgr2 = TossTokenManager(_creds(), http=client)
        assert mgr2._token is not None and mgr2._token.access_token == "tok-abc"


@pytest.mark.asyncio
async def test_memory_mode_writes_nothing(cache_dir):
    async def handler(request):
        return httpx.Response(200, json={"access_token": "t", "token_type": "Bearer", "expires_in": 86400})
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        mgr = TossTokenManager(_creds(), http=client, token_cache="memory")
        await mgr.get_token()
    assert not (cache_dir / "tokens").exists()
