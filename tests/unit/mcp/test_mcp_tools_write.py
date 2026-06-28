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


# ── cancel two-phase ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_cancel_rejected_when_trading_disabled():
    out = await orders_tools.cancel(
        _reg(FakeBroker(), trading=False), _gate(), None, order_id="X"
    )
    assert out["status"] == "rejected" and out["reason"] == "trading_disabled"


@pytest.mark.asyncio
async def test_cancel_first_call_previews_no_execution():
    fb = FakeBroker()

    async def cancel_must_not_run(order_id: str):
        raise AssertionError("must not execute")

    fb.orders.cancel = cancel_must_not_run  # type: ignore[method-assign]
    out = await orders_tools.cancel(
        _reg(fb, trading=True), _gate(), None, order_id="X"
    )
    assert out["status"] == "needs_confirmation"
    assert out["confirm_token"]


@pytest.mark.asyncio
async def test_cancel_executes_with_valid_token():
    fb = FakeBroker()
    called = {"n": 0}

    async def cancel_stub(order_id: str):
        called["n"] += 1
        return Order(
            order_id="COID", symbol=Symbol(ticker="005930"),
            side=OrderSide.BUY, qty=Decimal("1"), type="market",
            status=OrderStatus.CANCELLED, submitted_at=datetime(2026, 1, 2),
        )

    fb.orders.cancel = cancel_stub  # type: ignore[method-assign]
    gate = _gate()
    reg = _reg(fb, trading=True)
    prev = await orders_tools.cancel(reg, gate, None, order_id="COID")
    out = await orders_tools.cancel(
        reg, gate, None, order_id="COID", confirm_token=prev["confirm_token"]
    )
    assert out["status"] == "executed" and out["order"]["order_id"] == "COID"
    assert called["n"] == 1


# ── replace two-phase ───────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_replace_first_call_previews_no_execution():
    fb = FakeBroker()

    async def replace_must_not_run(order_id: str, *, qty=None, price=None):
        raise AssertionError("must not execute")

    fb.orders.replace = replace_must_not_run  # type: ignore[method-assign]
    out = await orders_tools.replace(
        _reg(fb, trading=True), _gate(), None, order_id="X", qty="5", price="100"
    )
    assert out["status"] == "needs_confirmation"
    assert out["confirm_token"]


@pytest.mark.asyncio
async def test_replace_token_invalidated_by_changed_price():
    fb = FakeBroker()

    async def replace_must_not_run(order_id: str, *, qty=None, price=None):
        raise AssertionError("must not execute")

    fb.orders.replace = replace_must_not_run  # type: ignore[method-assign]
    gate = _gate()
    reg = _reg(fb, trading=True)
    prev = await orders_tools.replace(reg, gate, None, order_id="X", qty="5", price="100")
    out = await orders_tools.replace(
        reg, gate, None, order_id="X", qty="5", price="999",
        confirm_token=prev["confirm_token"],
    )
    assert out["status"] == "needs_confirmation"  # old token must not authorise changed price


@pytest.mark.asyncio
async def test_replace_executes_with_valid_token():
    fb = FakeBroker()
    called = {"n": 0}

    async def replace_stub(order_id: str, *, qty=None, price=None):
        called["n"] += 1
        return Order(
            order_id="ROID", symbol=Symbol(ticker="005930"),
            side=OrderSide.BUY, qty=Decimal("5"), type="limit",
            price=Money(amount=Decimal("100"), currency=Currency.KRW),
            status=OrderStatus.OPEN, submitted_at=datetime(2026, 1, 2),
        )

    fb.orders.replace = replace_stub  # type: ignore[method-assign]
    gate = _gate()
    reg = _reg(fb, trading=True)
    prev = await orders_tools.replace(reg, gate, None, order_id="X", qty="5", price="100")
    out = await orders_tools.replace(
        reg, gate, None, order_id="X", qty="5", price="100",
        confirm_token=prev["confirm_token"],
    )
    assert out["status"] == "executed" and out["order"]["order_id"] == "ROID"
    assert called["n"] == 1
