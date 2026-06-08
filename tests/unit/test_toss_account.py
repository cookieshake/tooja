"""Unit tests for TossAccountClient — call is monkeypatched throughout."""

from __future__ import annotations

from decimal import Decimal

import pytest

import tooja.brokers.toss.account as account_mod
from tooja.brokers.toss.account import TossAccountClient
from tooja.brokers.toss.raw.asset.get_holdings import GetHoldingsExecutor
from tooja.brokers.toss.raw.models import (
    BuyingPowerResponse,
    HoldingsOverview,
    SellableQuantityResponse,
)
from tooja.brokers.toss.raw.order_info.get_buying_power import GetBuyingPowerExecutor
from tooja.brokers.toss.raw.order_info.get_sellable_quantity import GetSellableQuantityExecutor
from tooja.core.enums import Currency
from tooja.core.money import Money

# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------

_HOLDING_ITEM_WIRE = {
    "symbol": "005930",
    "name": "삼성전자",
    "marketCountry": "KR",
    "currency": "KRW",
    "quantity": "10",
    "lastPrice": "72000",
    "averagePurchasePrice": "70000",
    "marketValue": {
        "purchaseAmount": "700000",
        "amount": "720000",
    },
    "profitLoss": {
        "amount": "20000",
        "rate": "0.0286",
    },
    "dailyProfitLoss": {
        "amount": "5000",
        "rate": "0.007",
    },
    "cost": {
        "tax": "0",
        "commission": "0",
        "totalCost": "0",
    },
}

_HOLDINGS_OVERVIEW_WIRE = {
    "totalPurchaseAmount": {"krw": "700000", "usd": None},
    "marketValue": {
        "amount": {"krw": "720000", "usd": None},
        "amountAfterCost": {"krw": "720000", "usd": None},
    },
    "profitLoss": {
        "amount": {"krw": "20000", "usd": None},
        "amountAfterCost": {"krw": "20000", "usd": None},
        "rate": "0.0286",
        "rateAfterCost": "0.0286",
    },
    "dailyProfitLoss": {
        "amount": {"krw": "5000", "usd": None},
        "rate": "0.007",
    },
    "items": [_HOLDING_ITEM_WIRE],
}


def _broker():
    """Lightweight dummy broker — call is monkeypatched, nothing real executes."""
    return object()


def _client(broker=None):
    return TossAccountClient(broker or _broker())


# ---------------------------------------------------------------------------
# get_balance
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_balance_total_asset_is_krw_money(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["executor_cls"] = executor_cls
        captured["query"] = query
        return HoldingsOverview.model_validate(_HOLDINGS_OVERVIEW_WIRE)

    monkeypatch.setattr(account_mod, "call", fake_call)

    balance = await _client().get_balance()

    assert captured["executor_cls"] is GetHoldingsExecutor
    assert captured["query"] is None
    assert balance.total_asset == Money(amount=Decimal("720000"), currency=Currency.KRW)
    assert balance.cash == []
    assert len(balance.positions) == 1


@pytest.mark.asyncio
async def test_get_balance_position_symbol_and_qty(monkeypatch):
    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        return HoldingsOverview.model_validate(_HOLDINGS_OVERVIEW_WIRE)

    monkeypatch.setattr(account_mod, "call", fake_call)

    balance = await _client().get_balance()
    pos = balance.positions[0]

    assert pos.symbol.ticker == "005930"
    assert pos.qty == Decimal("10")
    assert pos.avg_price == Money(amount=Decimal("70000"), currency=Currency.KRW)


@pytest.mark.asyncio
async def test_get_balance_no_items_empty_positions(monkeypatch):
    wire = dict(_HOLDINGS_OVERVIEW_WIRE, items=[])

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        return HoldingsOverview.model_validate(wire)

    monkeypatch.setattr(account_mod, "call", fake_call)

    balance = await _client().get_balance()

    assert balance.positions == []
    assert balance.cash == []


# ---------------------------------------------------------------------------
# get_positions
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_positions_returns_list_of_positions(monkeypatch):
    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        return HoldingsOverview.model_validate(_HOLDINGS_OVERVIEW_WIRE)

    monkeypatch.setattr(account_mod, "call", fake_call)

    positions = await _client().get_positions()

    assert len(positions) == 1
    assert positions[0].symbol.ticker == "005930"
    assert positions[0].qty == Decimal("10")


@pytest.mark.asyncio
async def test_get_positions_empty_when_no_holdings(monkeypatch):
    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        return HoldingsOverview.model_validate(dict(_HOLDINGS_OVERVIEW_WIRE, items=[]))

    monkeypatch.setattr(account_mod, "call", fake_call)

    assert await _client().get_positions() == []


# ---------------------------------------------------------------------------
# get_position
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_position_returns_first_item(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["executor_cls"] = executor_cls
        captured["query"] = query
        return HoldingsOverview.model_validate(_HOLDINGS_OVERVIEW_WIRE)

    monkeypatch.setattr(account_mod, "call", fake_call)

    pos = await _client().get_position("005930")

    assert captured["executor_cls"] is GetHoldingsExecutor
    assert captured["query"] == {"symbol": "005930"}
    assert pos is not None
    assert pos.symbol.ticker == "005930"


@pytest.mark.asyncio
async def test_get_position_returns_none_when_empty(monkeypatch):
    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        return HoldingsOverview.model_validate(dict(_HOLDINGS_OVERVIEW_WIRE, items=[]))

    monkeypatch.setattr(account_mod, "call", fake_call)

    result = await _client().get_position("005930")

    assert result is None


# ---------------------------------------------------------------------------
# get_buying_power
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_buying_power_krw_maps_money(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["executor_cls"] = executor_cls
        captured["query"] = query
        return BuyingPowerResponse.model_validate({
            "currency": "KRW",
            "cashBuyingPower": "5000000",
        })

    monkeypatch.setattr(account_mod, "call", fake_call)

    power = await _client().get_buying_power(currency=Currency.KRW)

    assert captured["executor_cls"] is GetBuyingPowerExecutor
    assert captured["query"] == {"currency": "KRW"}
    assert power == Money(amount=Decimal("5000000"), currency=Currency.KRW)


@pytest.mark.asyncio
async def test_get_buying_power_usd_maps_money(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["query"] = query
        return BuyingPowerResponse.model_validate({
            "currency": "USD",
            "cashBuyingPower": "1234.56",
        })

    monkeypatch.setattr(account_mod, "call", fake_call)

    power = await _client().get_buying_power(currency=Currency.USD)

    assert captured["query"] == {"currency": "USD"}
    assert power == Money(amount=Decimal("1234.56"), currency=Currency.USD)


@pytest.mark.asyncio
async def test_get_buying_power_none_cash_returns_zero(monkeypatch):
    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        return BuyingPowerResponse.model_validate({
            "currency": "KRW",
            "cashBuyingPower": None,
        })

    monkeypatch.setattr(account_mod, "call", fake_call)

    power = await _client().get_buying_power()

    assert power == Money(amount=Decimal(0), currency=Currency.KRW)


@pytest.mark.asyncio
async def test_get_buying_power_default_currency_is_krw(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["query"] = query
        return BuyingPowerResponse.model_validate({
            "currency": "KRW",
            "cashBuyingPower": "1000000",
        })

    monkeypatch.setattr(account_mod, "call", fake_call)

    power = await _client().get_buying_power()

    assert captured["query"] == {"currency": "KRW"}
    assert power.currency == Currency.KRW


# ---------------------------------------------------------------------------
# get_sellable_quantity
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_sellable_quantity_maps_value(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["executor_cls"] = executor_cls
        captured["query"] = query
        return SellableQuantityResponse.model_validate({
            "sellableQuantity": "8",
        })

    monkeypatch.setattr(account_mod, "call", fake_call)

    qty = await _client().get_sellable_quantity("005930")

    assert captured["executor_cls"] is GetSellableQuantityExecutor
    assert captured["query"] == {"symbol": "005930"}
    assert qty == Decimal("8")


@pytest.mark.asyncio
async def test_get_sellable_quantity_none_returns_zero(monkeypatch):
    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        return SellableQuantityResponse.model_validate({
            "sellableQuantity": None,
        })

    monkeypatch.setattr(account_mod, "call", fake_call)

    qty = await _client().get_sellable_quantity("005930")

    assert qty == Decimal(0)


@pytest.mark.asyncio
async def test_get_sellable_quantity_accepts_symbol_object(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["query"] = query
        return SellableQuantityResponse.model_validate({"sellableQuantity": "5"})

    monkeypatch.setattr(account_mod, "call", fake_call)

    from tooja.core.models import Symbol
    from tooja.core.enums import Exchange

    sym = Symbol(ticker="005930", exchange=Exchange.KRX)
    qty = await _client().get_sellable_quantity(sym)

    assert captured["query"] == {"symbol": "005930"}
    assert qty == Decimal("5")
