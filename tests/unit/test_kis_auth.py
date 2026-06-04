"""TokenCache / ApprovalCache expiry logic.

These are pure unit tests — no HTTP. They exercise the cache file format and
the `expired()` checks.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest

from tooja.brokers.kis.auth import (
    ApprovalCache,
    TokenCache,
    _load_approval,
    _load_token,
    _save_approval,
    _save_token,
)


_NOW = datetime(2026, 6, 1, 9, 0, tzinfo=timezone.utc)


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


def test_token_roundtrip_via_disk(tmp_path, monkeypatch):
    import tooja.brokers.kis.auth as auth_mod

    token_file = tmp_path / "token.json"
    monkeypatch.setattr(auth_mod, "_TOKEN_FILE", token_file)

    tc = TokenCache(access_token="abc", expires_at=_NOW + timedelta(hours=12))
    _save_token(tc)
    loaded = _load_token()
    assert loaded is not None
    assert loaded.access_token == "abc"
    assert loaded.expires_at == tc.expires_at


def test_approval_roundtrip_via_disk(tmp_path, monkeypatch):
    import tooja.brokers.kis.auth as auth_mod

    file = tmp_path / "approval.json"
    monkeypatch.setattr(auth_mod, "_APPROVAL_FILE", file)

    ac = ApprovalCache(approval_key="key123", issued_at=_NOW)
    _save_approval(ac)
    loaded = _load_approval()
    assert loaded is not None
    assert loaded.approval_key == "key123"


def test_token_load_returns_none_on_missing_file(tmp_path, monkeypatch):
    import tooja.brokers.kis.auth as auth_mod

    monkeypatch.setattr(auth_mod, "_TOKEN_FILE", tmp_path / "nope.json")
    assert _load_token() is None


def test_token_load_returns_none_on_malformed_json(tmp_path, monkeypatch):
    import tooja.brokers.kis.auth as auth_mod

    f = tmp_path / "token.json"
    f.write_text("{not json")
    monkeypatch.setattr(auth_mod, "_TOKEN_FILE", f)
    assert _load_token() is None


def test_token_load_returns_none_when_missing_fields(tmp_path, monkeypatch):
    import tooja.brokers.kis.auth as auth_mod

    f = tmp_path / "token.json"
    f.write_text(json.dumps({"access_token": "x"}))  # expires_at missing
    monkeypatch.setattr(auth_mod, "_TOKEN_FILE", f)
    assert _load_token() is None
