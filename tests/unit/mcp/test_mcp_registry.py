"""Tests for MCP account registry."""

from __future__ import annotations

import pytest

from tooja.core.errors import ConfigError
from tooja.mcp.config import McpConfig
from tooja.mcp.registry import Account, Registry, build_registry
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


def test_has_kis_true_when_kis_account_present():
    kis_acc = Account("kis_main", FakeBroker("kis"), False, None)
    reg_kis = Registry({"a": kis_acc})
    assert reg_kis.has_kis is True

    non_kis_acc = Account("toss_main", FakeBroker("toss"), False, None)
    reg_non_kis = Registry({"a": non_kis_acc})
    assert reg_non_kis.has_kis is False


def test_all_returns_every_account():
    a = _acc("a")
    b = _acc("b")
    reg = Registry({"a": a, "b": b})
    all_accs = reg.all()
    assert len(all_accs) == 2
    names = {acc.name for acc in all_accs}
    assert names == {"a", "b"}


def test_build_registry_uses_injected_factory():
    config = McpConfig.model_validate(
        {
            "accounts": {
                "main": {
                    "broker": "kis",
                    "app_key": "k",
                    "app_secret": "s",
                    "cano": "1",
                    "hts_id": "h",
                }
            }
        }
    )
    fake_broker = FakeBroker("kis")
    reg = build_registry(config, broker_factory=lambda cfg: fake_broker)
    acc = reg.resolve("main")
    assert acc.broker is fake_broker


@pytest.mark.asyncio
async def test_aclose_closes_all_even_if_one_raises():
    a = _acc("a")
    b = _acc("b")
    reg = Registry({"a": a, "b": b})

    # Monkeypatch first broker to raise
    async def raising_close() -> None:
        raise RuntimeError("broker a failed")

    a.broker.close = raising_close  # type: ignore[assignment]

    with pytest.raises(RuntimeError, match="broker a failed"):
        await reg.aclose()

    # Second broker should still be closed
    assert b.broker.closed is True  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_aclose_groups_multiple_close_errors():
    a = _acc("a")
    b = _acc("b")
    reg = Registry({"a": a, "b": b})

    async def raising_close_a() -> None:
        raise RuntimeError("broker a failed")

    async def raising_close_b() -> None:
        raise ValueError("broker b failed")

    a.broker.close = raising_close_a  # type: ignore[assignment]
    b.broker.close = raising_close_b  # type: ignore[assignment]

    with pytest.raises(ExceptionGroup) as exc_info:
        await reg.aclose()

    assert len(exc_info.value.exceptions) == 2
