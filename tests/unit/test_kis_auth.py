"""TokenCache / ApprovalCache expiry logic and TokenManager persistence wiring.

Pure unit tests — no HTTP. Disk persistence itself is covered by
tests/unit/test_token_cache.py; here we verify the dataclass expiry checks and
that TokenManager round-trips through a TokenStore with app_key scoping.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from tooja.brokers.kis.auth import ApprovalCache, TokenCache, TokenManager
from tooja.brokers.kis.credentials import KisCredentials
from tooja.core.token_cache import scope_tag

_NOW = datetime(2026, 6, 1, 9, 0, tzinfo=timezone.utc)


def _creds(app_key: str = "APPKEY") -> KisCredentials:
    return KisCredentials(
        app_key=app_key,
        app_secret="SECRET",
        cano="50000000",
        acnt_prdt_cd="01",
        hts_id="hts",
    )


def test_token_cache_not_expired_when_within_ttl():
    tc = TokenCache(access_token="X", expires_at=_NOW + timedelta(hours=12))
    assert tc.expired(now=_NOW) is False


def test_token_cache_expired_within_refresh_margin():
    tc = TokenCache(access_token="X", expires_at=_NOW + timedelta(minutes=5))
    assert tc.expired(now=_NOW) is True


def test_token_cache_expired_in_past():
    tc = TokenCache(access_token="X", expires_at=_NOW - timedelta(hours=1))
    assert tc.expired(now=_NOW) is True


def test_approval_cache_not_expired_under_23h():
    ac = ApprovalCache(approval_key="K", issued_at=_NOW)
    assert ac.expired(now=_NOW + timedelta(hours=22)) is False


def test_approval_cache_expired_after_23h():
    ac = ApprovalCache(approval_key="K", issued_at=_NOW)
    assert ac.expired(now=_NOW + timedelta(hours=23, minutes=1)) is True


@pytest.fixture
def cache_dir(tmp_path, monkeypatch):
    import tooja.core.token_cache as tc

    monkeypatch.setattr(tc.platformdirs, "user_cache_dir", lambda *a, **k: str(tmp_path))
    return tmp_path


def test_manager_persists_and_reloads_token(cache_dir):
    """A token saved by one manager is visible to a fresh manager (disk mode)."""
    import httpx

    http = httpx.AsyncClient()
    mgr = TokenManager(_creds(), base_url="https://x", is_virtual=False, http=http)
    tc = TokenCache(access_token="abc", expires_at=_NOW + timedelta(hours=12))
    mgr._cache_token(tc)

    mgr2 = TokenManager(_creds(), base_url="https://x", is_virtual=False, http=http)
    assert mgr2._token is not None
    assert mgr2._token.access_token == "abc"


def test_manager_token_scoped_by_app_key(cache_dir):
    import httpx

    http = httpx.AsyncClient()
    mgr_a = TokenManager(_creds("KEY_A"), base_url="https://x", is_virtual=False, http=http)
    mgr_a._cache_token(TokenCache(access_token="tok_a", expires_at=_NOW + timedelta(hours=12)))

    mgr_b = TokenManager(_creds("KEY_B"), base_url="https://x", is_virtual=False, http=http)
    assert mgr_b._token is None
    assert scope_tag("KEY_A") != scope_tag("KEY_B")


def test_manager_memory_mode_writes_nothing(cache_dir):
    import httpx

    http = httpx.AsyncClient()
    mgr = TokenManager(
        _creds(), base_url="https://x", is_virtual=False, http=http, token_cache="memory"
    )
    mgr._cache_token(TokenCache(access_token="abc", expires_at=_NOW + timedelta(hours=12)))
    assert not (cache_dir / "tokens").exists()


def test_manager_invalidate_drops_cached_token(cache_dir):
    import httpx

    http = httpx.AsyncClient()
    mgr = TokenManager(_creds(), base_url="https://x", is_virtual=False, http=http)
    mgr._cache_token(TokenCache(access_token="abc", expires_at=_NOW + timedelta(hours=12)))
    mgr.invalidate_token()
    assert mgr._token is None
    mgr2 = TokenManager(_creds(), base_url="https://x", is_virtual=False, http=http)
    assert mgr2._token is None


def test_manager_persists_and_reloads_approval_key(cache_dir):
    """An approval_key saved by one manager is visible to a fresh manager."""
    import httpx

    http = httpx.AsyncClient()
    mgr = TokenManager(_creds(), base_url="https://x", is_virtual=False, http=http)
    ac = ApprovalCache(approval_key="ws-key-xyz", issued_at=_NOW)
    mgr._cache_approval(ac)

    mgr2 = TokenManager(_creds(), base_url="https://x", is_virtual=False, http=http)
    assert mgr2._approval is not None
    assert mgr2._approval.approval_key == "ws-key-xyz"
