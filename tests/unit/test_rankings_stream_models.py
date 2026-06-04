from datetime import datetime, timezone
from decimal import Decimal

from tooja.core.enums import Currency, OrderStatus
from tooja.core.money import Money
from tooja.core.models import (
    OrderUpdate,
    RankingEntry,
    StreamControlEvent,
    Symbol,
)


_NOW = datetime(2026, 6, 1, 9, 0, tzinfo=timezone.utc)


def test_ranking_entry_value_decimal_price_money():
    e = RankingEntry(
        rank=1,
        symbol=Symbol(ticker="005930"),
        name="Samsung Electronics",
        value=Decimal("500000000000000"),
        price=Money(amount=Decimal("70000"), currency=Currency.KRW),
    )
    assert e.price == Money(amount=Decimal("70000"), currency=Currency.KRW)
    assert e.value == Decimal("500000000000000")


def test_ranking_entry_price_optional():
    e = RankingEntry(
        rank=1,
        symbol=Symbol(ticker="005930"),
        name="Samsung Electronics",
        value=Decimal("500000000000000"),
    )
    assert e.price is None
    assert e.raw == {}


def test_order_update():
    u = OrderUpdate(
        order_id="0000123456",
        symbol=Symbol(ticker="005930"),
        status=OrderStatus.FILLED,
        filled_qty=Decimal("10"),
        avg_fill_price=Money(amount=Decimal("70000"), currency=Currency.KRW),
        time=_NOW,
    )
    assert u.status == OrderStatus.FILLED
    assert u.avg_fill_price.currency is Currency.KRW


def test_stream_control_event_kinds():
    ev = StreamControlEvent(kind="reconnected", time=_NOW)
    assert ev.kind == "reconnected"
    assert ev.symbols_affected == []
