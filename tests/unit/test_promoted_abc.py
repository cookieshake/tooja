"""Promoted cross-broker methods: ABC defaults raise, models construct, supports() flips."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

import pytest

from tooja.core.clients import AccountClient, InfoClient, MarketClient
from tooja.core.enums import Currency, Exchange
from tooja.core.errors import UnsupportedOperation
from tooja.core.models import PriceLimit, StockWarnings, Symbol
from tooja.core.money import Money


def test_price_limit_model_constructs():
    pl = PriceLimit(
        symbol=Symbol(ticker="005930", exchange=Exchange.KRX),
        upper_limit=Money(amount=Decimal("91000"), currency=Currency.KRW),
        lower_limit=Money(amount=Decimal("49000"), currency=Currency.KRW),
        as_of=datetime(2026, 6, 8, tzinfo=timezone.utc),
    )
    assert pl.upper_limit.amount == Decimal("91000")
    assert pl.lower_limit.currency == Currency.KRW


def test_price_limit_allows_none_for_unlimited_market():
    pl = PriceLimit(symbol=Symbol(ticker="AAPL", exchange=Exchange.NASD))
    assert pl.upper_limit is None and pl.lower_limit is None


def test_price_limit_rejects_mixed_currency():
    with pytest.raises(ValueError):
        PriceLimit(
            symbol=Symbol(ticker="005930"),
            upper_limit=Money(amount=Decimal("1"), currency=Currency.KRW),
            lower_limit=Money(amount=Decimal("1"), currency=Currency.USD),
        )


def test_stock_warnings_model_defaults_none():
    w = StockWarnings(symbol=Symbol(ticker="005930"))
    assert w.is_trading_halt is None
    assert w.is_administrative is None
    assert w.is_liquidation is None


def test_market_get_price_limits_default_raises():
    c = MarketClient()
    c._broker_name = "x"
    with pytest.raises(UnsupportedOperation):
        import asyncio
        asyncio.run(c.get_price_limits("005930"))


def test_account_buying_power_and_sellable_default_raise():
    c = AccountClient()
    c._broker_name = "x"
    import asyncio
    with pytest.raises(UnsupportedOperation):
        asyncio.run(c.get_buying_power())
    with pytest.raises(UnsupportedOperation):
        asyncio.run(c.get_sellable_quantity("005930"))


def test_info_get_warnings_default_raises():
    c = InfoClient()
    c._broker_name = "x"
    with pytest.raises(UnsupportedOperation):
        import asyncio
        asyncio.run(c.get_warnings("005930"))
