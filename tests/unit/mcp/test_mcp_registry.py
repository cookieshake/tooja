"""Tests for MCP account registry."""

from __future__ import annotations

import pytest

from tooja.core.errors import ConfigError
from tooja.mcp.registry import Account, Registry
from tests.unit.mcp.conftest import FakeBroker


def _acc(name: str, *, trading: bool = False) -> Account:
    return Account(name=name, broker=FakeBroker(name), trading=trading, max_order_value=None)


def test_resolve_single_defaults_to_only_account():
    reg = Registry({"default": _acc("default")})
    assert reg.resolve(None).name == "default"


def test_resolve_multiple_requires_name():
    reg = Registry({"a": _acc("a"), "b": _acc("b")})
    with pytest.raises(ConfigError):
        reg.resolve(None)
    assert reg.resolve("b").name == "b"


def test_resolve_unknown_raises():
    reg = Registry({"a": _acc("a")})
    with pytest.raises(ConfigError):
        reg.resolve("zzz")


def test_has_trading_flag():
    assert Registry({"a": _acc("a", trading=True)}).has_trading is True
    assert Registry({"a": _acc("a")}).has_trading is False


@pytest.mark.asyncio
async def test_aclose_closes_all():
    a = _acc("a")
    await Registry({"a": a}).aclose()
    assert a.broker.closed is True  # type: ignore[attr-defined]
