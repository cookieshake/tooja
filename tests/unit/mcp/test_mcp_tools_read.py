"""Unit tests for read tool modules: market, account, info, rankings."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

import pytest

from tooja.core.enums import Currency
from tooja.core.errors import SymbolNotFound
from tooja.core.models import Balance, InvestorFlow, Quote, Symbol
from tooja.core.money import Money
from tooja.mcp.registry import Account, Registry
from tooja.mcp.tools import account as account_tools
from tooja.mcp.tools import analytics as analytics_tools
from tooja.mcp.tools import market as market_tools
from tests.unit.mcp.conftest import FakeBroker


def _reg(broker: FakeBroker) -> Registry:
    return Registry({"default": Account("default", broker, False)})


@pytest.mark.asyncio
async def test_market_get_quote_serializes():
    fb = FakeBroker()

    async def fake_quote(symbol):
        return Quote(
            symbol=Symbol(ticker="005930"),
            price=Money(amount=Decimal("70000"), currency=Currency.KRW),
            time=datetime(2026, 1, 2),
        )

    fb.market.get_quote = fake_quote  # type: ignore[method-assign]
    out = await market_tools.get_quote(_reg(fb), None, "005930")
    assert out["price"] == {"amount": "70000", "currency": "KRW"}


@pytest.mark.asyncio
async def test_market_get_quote_maps_broker_error():
    fb = FakeBroker()

    async def boom(symbol):
        raise SymbolNotFound("no", broker="fake", raw_code="404")

    fb.market.get_quote = boom  # type: ignore[method-assign]
    out = await market_tools.get_quote(_reg(fb), None, "ZZZ")
    assert out["error"] == "SymbolNotFound"


@pytest.mark.asyncio
async def test_account_get_balance_serializes():
    fb = FakeBroker()

    async def bal():
        return Balance(cash=[Money(amount=Decimal("1000"), currency=Currency.KRW)])

    fb.account.get_balance = bal  # type: ignore[method-assign]
    out = await account_tools.get_balance(_reg(fb), None)
    assert out["cash"][0] == {"amount": "1000", "currency": "KRW"}


@pytest.mark.asyncio
async def test_analytics_investor_flows_serializes():
    fb = FakeBroker()

    async def flows(symbol, *, since, until):
        assert (since, until) == (date(2026, 1, 1), date(2026, 1, 31))
        return [InvestorFlow(
            symbol=Symbol(ticker="005930"), date=date(2026, 1, 2),
            individual_net=Money(amount=Decimal("1"), currency=Currency.KRW),
            foreign_net=Money(amount=Decimal("2"), currency=Currency.KRW),
            institutional_net=Money(amount=Decimal("3"), currency=Currency.KRW),
        )]
    fb.analytics.investor_flows = flows  # type: ignore[method-assign]
    out = await analytics_tools.investor_flows(
        _reg(fb), None, "005930", "2026-01-01", "2026-01-31"
    )
    assert out[0]["foreign_net"] == {"amount": "2", "currency": "KRW"}
