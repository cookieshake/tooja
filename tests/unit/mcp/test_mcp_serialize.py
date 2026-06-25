from datetime import datetime
from decimal import Decimal

from tooja.core.enums import Currency, OrderSide, OrderStatus
from tooja.core.models import Order, Symbol
from tooja.core.money import Money
from tooja.mcp._serialize import to_json


def _order() -> Order:
    return Order(
        order_id="A1", symbol=Symbol(ticker="005930"), side=OrderSide.BUY,
        qty=Decimal("10"), type="limit",
        price=Money(amount=Decimal("70000"), currency=Currency.KRW),
        status=OrderStatus.OPEN, submitted_at=datetime(2026, 1, 2, 9, 0, 0),
    )


def test_to_json_none():
    assert to_json(None) is None


def test_to_json_money_is_string_amount():
    d = to_json(_order())
    assert d["price"] == {"amount": "70000", "currency": "KRW"}
    assert d["qty"] == "10"
    assert d["symbol"]["ticker"] == "005930"


def test_to_json_list():
    out = to_json([_order(), _order()])
    assert isinstance(out, list) and len(out) == 2
