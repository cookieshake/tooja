"""TokenStore — secure, broker-agnostic token persistence."""

from __future__ import annotations

import os

import pytest

from tooja.core.token_cache import TokenStore, scope_tag


@pytest.fixture
def store_dir(tmp_path, monkeypatch):
    """Redirect platformdirs to a temp dir so tests never touch the real cache."""
    import tooja.core.token_cache as tc

    monkeypatch.setattr(tc.platformdirs, "user_cache_dir", lambda *a, **k: str(tmp_path))
    return tmp_path


def test_disk_save_then_load_roundtrip(store_dir):
    store = TokenStore(namespace="kis", mode="disk")
    store.save("token_abcd1234", {"access_token": "X", "expires_at": "2026-06-01T09:00:00+00:00"})
    loaded = store.load("token_abcd1234")
    assert loaded == {"access_token": "X", "expires_at": "2026-06-01T09:00:00+00:00"}


def test_disk_load_missing_returns_none(store_dir):
    store = TokenStore(namespace="kis", mode="disk")
    assert store.load("token_missing") is None


def test_disk_delete_removes_entry(store_dir):
    store = TokenStore(namespace="kis", mode="disk")
    store.save("token_x", {"access_token": "Y"})
    store.delete("token_x")
    assert store.load("token_x") is None


def test_scope_tag_distinct_per_secret():
    assert scope_tag("appkey-A") != scope_tag("appkey-B")
    assert scope_tag("appkey-A") == scope_tag("appkey-A")
    assert len(scope_tag("appkey-A")) == 8


def test_memory_mode_roundtrip_without_disk(store_dir):
    store = TokenStore(namespace="kis", mode="memory")
    store.save("token_x", {"access_token": "Z"})
    assert store.load("token_x") == {"access_token": "Z"}
    # Nothing was written under the (redirected) cache dir.
    assert not (store_dir / "tokens").exists()


def test_memory_mode_delete(store_dir):
    store = TokenStore(namespace="kis", mode="memory")
    store.save("token_x", {"access_token": "Z"})
    store.delete("token_x")
    assert store.load("token_x") is None


def test_memory_instances_are_isolated(store_dir):
    a = TokenStore(namespace="kis", mode="memory")
    b = TokenStore(namespace="kis", mode="memory")
    a.save("token_x", {"access_token": "A"})
    assert b.load("token_x") is None


@pytest.mark.skipif(os.name == "nt", reason="POSIX file mode not enforced on Windows")
def test_disk_file_permissions_are_0600(store_dir):
    store = TokenStore(namespace="kis", mode="disk")
    store.save("token_perm", {"access_token": "X"})
    path = store_dir / "tokens" / "kis" / "token_perm.json"
    assert path.exists()
    assert (path.stat().st_mode & 0o777) == 0o600


def test_disk_load_returns_none_on_malformed_json(store_dir):
    store = TokenStore(namespace="kis", mode="disk")
    store.save("token_bad", {"access_token": "X"})  # creates the dir
    (store_dir / "tokens" / "kis" / "token_bad.json").write_text("{not json")
    assert store.load("token_bad") is None


def test_disk_overwrite_replaces_value(store_dir):
    store = TokenStore(namespace="kis", mode="disk")
    store.save("token_x", {"access_token": "OLD"})
    store.save("token_x", {"access_token": "NEW"})
    assert store.load("token_x") == {"access_token": "NEW"}
    # No leftover temp file.
    assert not (store_dir / "tokens" / "kis" / "token_x.tmp").exists()
