"""Wire-level regression tests for the Toss adapter.

Mirrors ``tests/unit/test_kis_wire_regression.py``: instead of monkeypatching
``call``, we inject an ``httpx.MockTransport`` into a real ``TossBroker`` so the
entire raw layer runs end-to-end — ``TossApiExecutor.execute() → _parse``
(envelope unwrap ``{"result": ...}``) → generated model parse → subclient
mapper → core domain model.

The fixtures under ``tests/fixtures/toss/`` are the BARE inner payloads taken
verbatim from Toss's own published 200-response examples in
``specs/toss/openapi.json`` (each example there is wrapped in ``{"result": ...}``
— we store the inner value and the MockTransport handler re-wraps it for the
enveloped endpoints; ``/oauth2/token`` is served bare). This catches
field-name / shape / envelope mismatches between our generated models/mappers
and the official spec.

Token issuance is stubbed by pre-attaching a fake token manager whose
``get_token()`` returns a dummy token, so no OAuth round-trip is needed.
"""

from __future__ import annotations

import json
from datetime import date
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest

from tooja.brokers.toss.broker import TossBroker
from tooja.core.enums import Currency, OrderSide, OrderStatus

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures" / "toss"

# Map of request path → fixture file. The handler wraps each in {"result": ...}
# (the executor's ENVELOPED unwrap then reverses it), reproducing the wire shape.
_ROUTES: dict[str, str] = {
    "/api/v1/prices": "get_prices.json",
    "/api/v1/orderbook": "get_orderbook.json",
    "/api/v1/candles": "get_candles.json",
    "/api/v1/price-limits": "price_limits.json",
    "/api/v1/stocks": "get_stocks.json",
    "/api/v1/holdings": "holdings.json",
    "/api/v1/buying-power": "buying_power.json",
    "/api/v1/sellable-quantity": "sellable_quantity.json",
    "/api/v1/orders": "get_orders.json",
    "/api/v1/market-calendar/KR": "kr_market_calendar.json",
}


def _load(name: str):
    return json.loads((FIXTURES / name).read_text())


async def _fake_get_token() -> str:
    return "tok"


def _handler(request: httpx.Request) -> httpx.Response:
    """Route by URL path to the matching official-example fixture.

    Enveloped endpoints return ``{"result": <fixture>}``; ``/oauth2/token``
    returns the bare token fixture. Parameterised paths
    (``/api/v1/stocks/{symbol}/warnings``, ``/api/v1/orders/{orderId}``) are
    matched by prefix/suffix.
    """
    path = request.url.path

    if path == "/oauth2/token":
        return httpx.Response(200, json=_load("oauth_token.json"))

    if path.startswith("/api/v1/stocks/") and path.endswith("/warnings"):
        return httpx.Response(200, json={"result": _load("get_stock_warnings.json")})

    # /api/v1/orders/{orderId} — but NOT the bare /api/v1/orders list endpoint.
    if path.startswith("/api/v1/orders/"):
        return httpx.Response(200, json={"result": _load("get_order.json")})

    fixture = _ROUTES.get(path)
    if fixture is not None:
        return httpx.Response(200, json={"result": _load(fixture)})

    return httpx.Response(404, json={"error": {"code": "not-found", "message": path}})


def _broker() -> TossBroker:
    broker = TossBroker(
        client_id="cid", client_secret="csec", account_seq=12345678,
        token_cache="memory",
    )
    transport = httpx.MockTransport(_handler)
    broker._http = httpx.AsyncClient(base_url=broker.base_url, transport=transport)
    broker._tokens = SimpleNamespace(
        get_token=_fake_get_token,
        invalidate=lambda: None,
    )
    broker._open = True
    return broker


# ────────────────────────────────────────────────────────────────────────────
# market
# ────────────────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_get_quote_maps_official_prices_example():
    broker = _broker()
    try:
        quote = await broker.market.get_quote("005930")
    finally:
        await broker.close()
    assert quote.symbol.ticker == "005930"
    assert quote.price.amount == Decimal("72000")
    assert quote.price.currency is Currency.KRW


@pytest.mark.asyncio
async def test_get_orderbook_maps_official_orderbook_example():
    broker = _broker()
    try:
        ob = await broker.market.get_orderbook("005930")
    finally:
        await broker.close()
    assert ob.symbol.ticker == "005930"
    assert ob.asks and ob.bids
    # Best ask 72300 / best bid 72000 from the official KR example.
    assert ob.asks[0].price.amount == Decimal("72300")
    assert ob.asks[0].qty == Decimal("1200")
    assert ob.bids[0].price.amount == Decimal("72000")
    assert ob.bids[0].price.currency is Currency.KRW


@pytest.mark.asyncio
async def test_get_ohlcv_maps_official_candles_example():
    broker = _broker()
    try:
        candles = await broker.market.get_ohlcv("005930", interval="1d")
    finally:
        await broker.close()
    assert len(candles) == 2
    first = candles[0]
    assert first.open.amount == Decimal("71600")
    assert first.high.amount == Decimal("72300")
    assert first.low.amount == Decimal("71500")
    assert first.close.amount == Decimal("72000")
    assert first.volume == Decimal("3521000")
    assert first.close.currency is Currency.KRW


@pytest.mark.asyncio
async def test_get_price_limits_maps_official_example():
    broker = _broker()
    try:
        pl = await broker.market.get_price_limits("005930")
    finally:
        await broker.close()
    assert pl.symbol.ticker == "005930"
    assert pl.upper_limit is not None and pl.upper_limit.amount == Decimal("93000")
    assert pl.lower_limit is not None and pl.lower_limit.amount == Decimal("50400")
    assert pl.upper_limit.currency is Currency.KRW


# ────────────────────────────────────────────────────────────────────────────
# info
# ────────────────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_get_stock_maps_official_stocks_example():
    broker = _broker()
    try:
        info = await broker.info.get_stock("005930")
    finally:
        await broker.close()
    assert info.symbol.ticker == "005930"
    assert info.name == "삼성전자"
    assert info.listed_at == date(1975, 6, 11)
    assert info.listed_shares == Decimal("5919637922")


@pytest.mark.asyncio
async def test_get_warnings_maps_official_warnings_example():
    broker = _broker()
    try:
        w = await broker.info.get_warnings("005930")
    finally:
        await broker.close()
    assert w.symbol.ticker == "005930"
    # OVERHEATED → is_overheated; VI_STATIC → vi_triggered (per official example).
    assert w.is_overheated is True
    assert w.vi_triggered is True


@pytest.mark.asyncio
async def test_is_holiday_business_day_official_calendar_example():
    broker = _broker()
    try:
        # Calendar fixture's today.date is 2026-03-25 with integrated hours present
        # → business day → not a holiday.
        result = await broker.info.is_holiday(date(2026, 3, 25))
    finally:
        await broker.close()
    assert result is False


# ────────────────────────────────────────────────────────────────────────────
# account
# ────────────────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_get_balance_maps_deeply_nested_official_holdings_example():
    """Highest-value case: the deeply nested holdings overview must parse and map.

    Exercises nested Money buckets (krw/usd), per-position currency, and the
    profitLoss/marketValue sub-objects from Toss's own withHoldings example.
    """
    broker = _broker()
    try:
        bal = await broker.account.get_balance()
    finally:
        await broker.close()
    # total_asset is the KRW market value (marketValue.amount.krw).
    assert bal.total_asset is not None
    assert bal.total_asset.amount == Decimal("7200000")
    assert bal.total_asset.currency is Currency.KRW
    assert len(bal.positions) == 2
    kr, us = bal.positions[0], bal.positions[1]
    assert kr.symbol.ticker == "005930"
    assert kr.qty == Decimal("100")
    assert kr.avg_price.amount == Decimal("65000")
    assert kr.avg_price.currency is Currency.KRW
    assert us.symbol.ticker == "AAPL"
    assert us.qty == Decimal("10")
    assert us.avg_price.currency is Currency.USD


@pytest.mark.asyncio
async def test_get_buying_power_maps_official_example():
    broker = _broker()
    try:
        bp = await broker.account.get_buying_power(currency=Currency.KRW)
    finally:
        await broker.close()
    assert bp.amount == Decimal("5000000")
    assert bp.currency is Currency.KRW


@pytest.mark.asyncio
async def test_get_sellable_quantity_maps_official_example():
    broker = _broker()
    try:
        qty = await broker.account.get_sellable_quantity("005930")
    finally:
        await broker.close()
    assert qty == Decimal("100")


# ────────────────────────────────────────────────────────────────────────────
# orders
# ────────────────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_orders_get_maps_official_order_example():
    broker = _broker()
    try:
        order = await broker.orders.get("0d5QIHjmtksbsmM")
    finally:
        await broker.close()
    assert order.symbol.ticker == "005930"
    assert order.side is OrderSide.BUY
    assert order.type == "limit"
    assert order.status is OrderStatus.FILLED
    assert order.qty == Decimal("10")
    assert order.filled_qty == Decimal("10")
    assert order.price is not None and order.price.amount == Decimal("70000")
    assert order.avg_fill_price is not None
    assert order.avg_fill_price.amount == Decimal("70000")


@pytest.mark.asyncio
async def test_orders_list_maps_official_orders_example():
    broker = _broker()
    try:
        orders = await broker.orders.list_orders()
    finally:
        await broker.close()
    assert len(orders) == 2
    buy, sell = orders[0], orders[1]
    assert buy.symbol.ticker == "005930"
    assert buy.side is OrderSide.BUY
    assert buy.status is OrderStatus.PENDING
    assert sell.symbol.ticker == "AAPL"
    assert sell.side is OrderSide.SELL
    assert sell.status is OrderStatus.PARTIALLY_FILLED
    assert sell.filled_qty == Decimal("2")
    assert sell.price is not None and sell.price.currency is Currency.USD
