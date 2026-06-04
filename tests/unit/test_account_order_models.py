from datetime import datetime, timezone
from decimal import Decimal

import pytest
from pydantic import TypeAdapter, ValidationError

from tooja.core.enums import Currency, OrderSide, OrderStatus, TimeInForce
from tooja.core.money import Money
from tooja.core.models import (
    Balance,
    Fill,
    LimitOrder,
    MarketOrder,
    Order,
    OrderRequest,
    Position,
    StopLimitOrder,
    Symbol,
)


_NOW = datetime(2026, 6, 1, 15, 30, tzinfo=timezone.utc)


def _krw(amount: int | str) -> Money:
    return Money(amount=Decimal(amount), currency=Currency.KRW)


def _usd(amount: int | str) -> Money:
    return Money(amount=Decimal(amount), currency=Currency.USD)


# ─── Position ─────────────────────────────────────────
def test_position_basic():
    p = Position(
        symbol=Symbol(ticker="005930"),
        qty=Decimal("10"),
        avg_price=_krw(69500),
    )
    assert p.market_value is None
    assert p.avg_price.currency is Currency.KRW


# ─── Balance ──────────────────────────────────────────
def test_balance_with_positions_and_cash_list():
    b = Balance(
        total_asset=_krw(1_000_000),
        cash=[_krw(500_000)],
        positions=[
            Position(
                symbol=Symbol(ticker="005930"),
                qty=Decimal("10"),
                avg_price=_krw(69500),
            ),
        ],
    )
    assert b.cash[0] == _krw(500_000)
    assert len(b.positions) == 1


def test_balance_multi_currency_cash():
    b = Balance(cash=[_krw(500_000), _usd("1000.00")])
    assert {m.currency for m in b.cash} == {Currency.KRW, Currency.USD}


def test_balance_rejects_duplicate_cash_currency():
    with pytest.raises(ValidationError, match="duplicate currencies"):
        Balance(cash=[_krw(100), _krw(200)])


def test_balance_defaults_are_independent():
    b1 = Balance()
    b2 = Balance()
    b1.cash.append(_usd("100.00"))
    b1.positions.append(
        Position(
            symbol=Symbol(ticker="005930"),
            qty=Decimal("1"),
            avg_price=_krw(70000),
        )
    )
    assert b2.cash == []
    assert b2.positions == []


# ─── Order request union ──────────────────────────────
def test_market_order_discriminator():
    mo = MarketOrder(
        symbol=Symbol(ticker="005930"),
        side=OrderSide.BUY,
        qty=Decimal("10"),
    )
    assert mo.type == "market"


def test_limit_order_default_tif_day():
    lo = LimitOrder(
        symbol=Symbol(ticker="005930"),
        side=OrderSide.SELL,
        qty=Decimal("5"),
        price=_krw(72000),
    )
    assert lo.time_in_force == TimeInForce.DAY


def test_order_request_discriminated_union_parses():
    adapter = TypeAdapter(OrderRequest)

    mo = adapter.validate_python({
        "type": "market",
        "symbol": {"ticker": "005930"},
        "side": "buy",
        "qty": "10",
    })
    assert isinstance(mo, MarketOrder)

    lo = adapter.validate_python({
        "type": "limit",
        "symbol": {"ticker": "005930"},
        "side": "sell",
        "qty": "10",
        "price": {"amount": Decimal("70000"), "currency": "KRW"},
    })
    assert isinstance(lo, LimitOrder)
    assert lo.price == _krw(70000)

    so = adapter.validate_python({
        "type": "stop_limit",
        "symbol": {"ticker": "005930"},
        "side": "buy",
        "qty": "5",
        "price": {"amount": Decimal("70000"), "currency": "KRW"},
        "stop_price": {"amount": Decimal("69500"), "currency": "KRW"},
    })
    assert isinstance(so, StopLimitOrder)


def test_stop_limit_order_currency_mismatch_rejected():
    """The _MoneyConsistent mixin detects price/stop_price currency mismatch on StopLimitOrder."""
    with pytest.raises(ValidationError, match="inconsistent currencies"):
        StopLimitOrder(
            symbol=Symbol(ticker="005930"),
            side=OrderSide.BUY,
            qty=Decimal("5"),
            price=_krw(70000),
            stop_price=_usd(50),
        )


def test_order_request_unknown_type_rejected():
    adapter = TypeAdapter(OrderRequest)
    with pytest.raises(ValidationError):
        adapter.validate_python({
            "type": "iceberg",
            "symbol": {"ticker": "005930"},
            "side": "buy",
            "qty": "10",
        })


# ─── Order state ──────────────────────────────────────
def test_order_state():
    o = Order(
        order_id="0000123456",
        symbol=Symbol(ticker="005930"),
        side=OrderSide.BUY,
        qty=Decimal("10"),
        type="limit",
        price=_krw(70000),
        status=OrderStatus.OPEN,
        submitted_at=_NOW,
    )
    assert o.filled_qty == Decimal(0)
    assert o.price == _krw(70000)


# ─── Fill ─────────────────────────────────────────────
def test_fill_minimum():
    f = Fill(
        order_id="0000123456",
        symbol=Symbol(ticker="005930"),
        side=OrderSide.BUY,
        qty=Decimal("10"),
        price=_krw(70000),
        time=_NOW,
    )
    assert f.fee is None
    assert f.raw == {}


def test_fill_with_fee():
    f = Fill(
        order_id="0000123456",
        symbol=Symbol(ticker="005930"),
        side=OrderSide.SELL,
        qty=Decimal("10"),
        price=_krw(70000),
        time=_NOW,
        fee=_krw(150),
    )
    assert f.fee == _krw(150)


def test_fill_preserves_raw():
    f = Fill(
        order_id="0000123456",
        symbol=Symbol(ticker="005930"),
        side=OrderSide.BUY,
        qty=Decimal("10"),
        price=_krw(70000),
        time=_NOW,
        raw={"cntg_qty": "10", "cntg_unpr": "70000"},
    )
    assert f.raw["cntg_qty"] == "10"
