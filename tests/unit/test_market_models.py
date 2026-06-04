from datetime import datetime, timezone
from decimal import Decimal

import pytest

from tooja.core.enums import Currency
from tooja.core.money import Money
from tooja.core.models import (
    OHLCV,
    Orderbook,
    OrderbookLevel,
    Quote,
    Symbol,
    Trade,
)


_KST_NOW = datetime(2026, 6, 1, 15, 30, tzinfo=timezone.utc)


def _krw(amount: int | str) -> Money:
    return Money(amount=Decimal(amount), currency=Currency.KRW)


def test_quote_minimum_fields():
    q = Quote(
        symbol=Symbol(ticker="005930"),
        price=_krw(70000),
        time=_KST_NOW,
    )
    assert q.price == _krw(70000)
    assert q.price.currency is Currency.KRW
    assert q.raw == {}
    assert q.change is None


def test_quote_preserves_raw():
    q = Quote(
        symbol=Symbol(ticker="005930"),
        price=_krw(70000),
        time=_KST_NOW,
        raw={"stck_prpr": "70000", "prdy_vrss": "100"},
    )
    assert q.raw["stck_prpr"] == "70000"


def test_ohlcv_required_fields():
    bar = OHLCV(
        symbol=Symbol(ticker="005930"),
        time=_KST_NOW,
        open=_krw(69800),
        high=_krw(70200),
        low=_krw(69500),
        close=_krw(70000),
        volume=Decimal("123456"),
    )
    assert bar.close == _krw(70000)
    assert bar.volume == Decimal("123456")


def test_orderbook_levels():
    ob = Orderbook(
        symbol=Symbol(ticker="005930"),
        time=_KST_NOW,
        bids=[OrderbookLevel(price=_krw(69900), qty=Decimal("100"))],
        asks=[OrderbookLevel(price=_krw(70000), qty=Decimal("200"))],
    )
    assert ob.bids[0].price == _krw(69900)
    assert ob.asks[0].qty == Decimal("200")


def test_orderbook_rejects_mixed_currencies():
    with pytest.raises(ValueError, match="inconsistent currencies"):
        Orderbook(
            symbol=Symbol(ticker="005930"),
            time=_KST_NOW,
            bids=[OrderbookLevel(price=_krw(69900), qty=Decimal("100"))],
            asks=[
                OrderbookLevel(
                    price=Money(amount=Decimal("70.00"), currency=Currency.USD),
                    qty=Decimal("200"),
                )
            ],
        )


def test_trade_minimum():
    t = Trade(
        symbol=Symbol(ticker="005930"),
        time=_KST_NOW,
        price=_krw(70000),
        qty=Decimal("10"),
    )
    assert t.side is None
    assert t.price.currency is Currency.KRW


def test_quote_raw_default_is_independent_dict():
    q1 = Quote(symbol=Symbol(ticker="005930"), price=_krw(70000), time=_KST_NOW)
    q2 = Quote(symbol=Symbol(ticker="035720"), price=_krw(50000), time=_KST_NOW)
    q1.raw["foo"] = "bar"
    assert q2.raw == {}


