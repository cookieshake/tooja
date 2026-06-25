# tests/unit/mcp/test_mcp_tools_write.py
from datetime import datetime
from decimal import Decimal

import pytest

from tooja.core.enums import Currency, OrderSide, OrderStatus
from tooja.core.models import Order, Symbol
from tooja.core.money import Money
from tooja.mcp.confirm import ConfirmGate
from tooja.mcp.registry import Account, Registry
from tooja.mcp.tools import orders as orders_tools
from tests.unit.mcp.conftest import FakeBroker


def _reg(broker: FakeBroker, *, trading: bool, cap: Decimal | None = None) -> Registry:
    return Registry({"default": Account("default", broker, trading, cap)})


def _gate() -> ConfirmGate:
    return ConfirmGate(secret=b"x" * 32)


@pytest.mark.asyncio
async def test_create_rejected_when_trading_disabled():
    out = await orders_tools.create(
        _reg(FakeBroker(), trading=False), _gate(), None,
        symbol="005930", side="buy", qty="10", type="limit", price="70000",
    )
    assert out["status"] == "rejected" and out["reason"] == "trading_disabled"


@pytest.mark.asyncio
async def test_create_first_call_returns_preview_no_execution():
    fb = FakeBroker()
    called = {"n": 0}

    async def create(req):
        called["n"] += 1
        raise AssertionError("must not execute on preview")
    fb.orders.create = create  # type: ignore[method-assign]
    out = await orders_tools.create(
        _reg(fb, trading=True), _gate(), None,
        symbol="005930", side="buy", qty="10", type="limit", price="70000",
    )
    assert out["status"] == "needs_confirmation"
    assert out["confirm_token"]
    assert called["n"] == 0


@pytest.mark.asyncio
async def test_create_executes_with_valid_token():
    fb = FakeBroker()

    async def create(req):
        return Order(order_id="OID", symbol=Symbol(ticker="005930"),
                     side=OrderSide.BUY, qty=Decimal("10"), type="limit",
                     price=Money(amount=Decimal("70000"), currency=Currency.KRW),
                     status=OrderStatus.OPEN, submitted_at=datetime(2026, 1, 2))
    fb.orders.create = create  # type: ignore[method-assign]
    gate = _gate()
    reg = _reg(fb, trading=True)
    prev = await orders_tools.create(
        reg, gate, None, symbol="005930", side="buy", qty="10",
        type="limit", price="70000",
    )
    out = await orders_tools.create(
        reg, gate, None, symbol="005930", side="buy", qty="10",
        type="limit", price="70000", confirm_token=prev["confirm_token"],
    )
    assert out["status"] == "executed" and out["order"]["order_id"] == "OID"


@pytest.mark.asyncio
async def test_create_value_cap_blocks_preview():
    fb = FakeBroker()
    out = await orders_tools.create(
        _reg(fb, trading=True, cap=Decimal("100000")), _gate(), None,
        symbol="005930", side="buy", qty="10", type="limit", price="70000",
    )
    assert out["status"] == "rejected" and out["reason"] == "max_order_value_exceeded"


@pytest.mark.asyncio
async def test_create_token_does_not_carry_to_changed_qty():
    fb = FakeBroker()

    async def create(req):
        raise AssertionError("must not execute")
    fb.orders.create = create  # type: ignore[method-assign]
    gate = _gate()
    reg = _reg(fb, trading=True)
    prev = await orders_tools.create(
        reg, gate, None, symbol="005930", side="buy", qty="10",
        type="limit", price="70000",
    )
    out = await orders_tools.create(
        reg, gate, None, symbol="005930", side="buy", qty="999",
        type="limit", price="70000", confirm_token=prev["confirm_token"],
    )
    assert out["status"] == "needs_confirmation"  # token invalid for new qty
