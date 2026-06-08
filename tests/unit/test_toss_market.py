"""Unit tests for TossMarketClient — monkeypatches `call` so no network needed."""

from __future__ import annotations

from decimal import Decimal

import pytest

from tooja.brokers.toss import market as market_mod
from tooja.brokers.toss.market import TossMarketClient
from tooja.brokers.toss.raw.market_data.get_prices import GetPricesExecutor, GetPricesResult
from tooja.brokers.toss.raw.market_data.get_orderbook import GetOrderbookExecutor
from tooja.brokers.toss.raw.market_data.get_candles import GetCandlesExecutor
from tooja.brokers.toss.raw.market_data.get_price_limit import GetPriceLimitExecutor
from tooja.brokers.toss.raw.models import (
    CandlePageResponse,
    OrderbookResponse,
    PriceLimitResponse,
)
from tooja.core.enums import Currency, Exchange
from tooja.core.errors import SymbolNotFound, UnsupportedOperation
from tooja.core.models import Symbol
from tooja.core.money import Money


# ── fixture helpers ───────────────────────────────────────────────────────────


def _broker():
    """Lightweight dummy broker — call is monkeypatched so nothing real happens."""
    return object()


def _client(broker=None):
    return TossMarketClient(broker or _broker())


# ── get_quote ─────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_quote_maps_price_and_symbol(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["executor_cls"] = executor_cls
        captured["query"] = query
        return GetPricesResult.model_validate({
            "root": [
                {"symbol": "005930", "lastPrice": "72000", "currency": "KRW",
                 "timestamp": "2026-06-08T10:30:00+09:00"}
            ]
        })

    monkeypatch.setattr(market_mod, "call", fake_call)

    quote = await _client().get_quote("005930")

    assert captured["executor_cls"] is GetPricesExecutor
    assert captured["query"] == {"symbols": "005930"}
    assert quote.price == Money(amount=Decimal("72000"), currency=Currency.KRW)
    assert quote.symbol.ticker == "005930"
    assert quote.symbol.exchange is Exchange.KRX


@pytest.mark.asyncio
async def test_get_quote_raises_symbol_not_found_when_empty(monkeypatch):
    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        return GetPricesResult.model_validate({"root": []})

    monkeypatch.setattr(market_mod, "call", fake_call)

    with pytest.raises(SymbolNotFound):
        await _client().get_quote("NONEXISTENT")


@pytest.mark.asyncio
async def test_get_quote_accepts_symbol_object(monkeypatch):
    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        return GetPricesResult.model_validate({
            "root": [{"symbol": "005930", "lastPrice": "72000", "currency": "KRW"}]
        })

    monkeypatch.setattr(market_mod, "call", fake_call)

    sym = Symbol(ticker="005930", exchange=Exchange.KRX)
    quote = await _client().get_quote(sym)
    assert quote.price.amount == Decimal("72000")


# ── get_quotes ────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_quotes_joins_tickers(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["query"] = query
        return GetPricesResult.model_validate({
            "root": [
                {"symbol": "005930", "lastPrice": "72000", "currency": "KRW"},
                {"symbol": "000660", "lastPrice": "130000", "currency": "KRW"},
            ]
        })

    monkeypatch.setattr(market_mod, "call", fake_call)

    quotes = await _client().get_quotes(["005930", "000660"])

    assert captured["query"] == {"symbols": "005930,000660"}
    assert len(quotes) == 2
    assert quotes[0].price.amount == Decimal("72000")
    assert quotes[1].price.amount == Decimal("130000")


@pytest.mark.asyncio
async def test_get_quotes_batches_at_200(monkeypatch):
    """Symbols > 200 must be split into two calls."""
    call_count = 0

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        nonlocal call_count
        call_count += 1
        # return one entry per call so we can count
        return GetPricesResult.model_validate({
            "root": [{"symbol": "005930", "lastPrice": "72000", "currency": "KRW"}]
        })

    monkeypatch.setattr(market_mod, "call", fake_call)

    symbols = [f"{i:06d}" for i in range(201)]
    await _client().get_quotes(symbols)

    assert call_count == 2  # 200 + 1


# ── get_orderbook ─────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_orderbook_maps_bids_and_asks(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["executor_cls"] = executor_cls
        captured["query"] = query
        return OrderbookResponse.model_validate({
            "timestamp": "2026-06-08T10:30:00+09:00",
            "currency": "KRW",
            "asks": [
                {"price": "72100", "volume": "10"},
                {"price": "72200", "volume": "20"},
            ],
            "bids": [
                {"price": "72000", "volume": "5"},
                {"price": "71900", "volume": "15"},
            ],
        })

    monkeypatch.setattr(market_mod, "call", fake_call)

    ob = await _client().get_orderbook("005930", depth=2)

    assert captured["executor_cls"] is GetOrderbookExecutor
    assert captured["query"] == {"symbol": "005930"}
    assert len(ob.asks) == 2
    assert len(ob.bids) == 2
    assert ob.asks[0].price == Money(amount=Decimal("72100"), currency=Currency.KRW)
    assert ob.asks[0].qty == Decimal("10")
    assert ob.bids[0].price == Money(amount=Decimal("72000"), currency=Currency.KRW)


@pytest.mark.asyncio
async def test_get_orderbook_respects_depth(monkeypatch):
    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        return OrderbookResponse.model_validate({
            "currency": "KRW",
            "asks": [{"price": str(72000 + i * 100), "volume": "10"} for i in range(10)],
            "bids": [{"price": str(72000 - i * 100), "volume": "10"} for i in range(10)],
        })

    monkeypatch.setattr(market_mod, "call", fake_call)

    ob = await _client().get_orderbook("005930", depth=3)
    assert len(ob.asks) == 3
    assert len(ob.bids) == 3


# ── get_ohlcv ─────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_ohlcv_unsupported_interval_raises(monkeypatch):
    monkeypatch.setattr(market_mod, "call", None)  # should never be called

    with pytest.raises(UnsupportedOperation):
        await _client().get_ohlcv("005930", interval="5m")


@pytest.mark.asyncio
async def test_get_ohlcv_1m_maps_candles(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["executor_cls"] = executor_cls
        captured["query"] = query
        return CandlePageResponse.model_validate({
            "candles": [
                {
                    "timestamp": "2026-06-08T10:00:00+09:00",
                    "openPrice": "71000",
                    "highPrice": "72500",
                    "lowPrice": "70800",
                    "closePrice": "72000",
                    "volume": "1234567",
                    "currency": "KRW",
                },
            ]
        })

    monkeypatch.setattr(market_mod, "call", fake_call)

    bars = await _client().get_ohlcv("005930", interval="1m", limit=5)

    assert captured["executor_cls"] is GetCandlesExecutor
    assert captured["query"]["interval"] == "1m"
    assert captured["query"]["symbol"] == "005930"
    assert captured["query"]["count"] == 5
    assert len(bars) == 1
    bar = bars[0]
    assert bar.open == Money(amount=Decimal("71000"), currency=Currency.KRW)
    assert bar.high == Money(amount=Decimal("72500"), currency=Currency.KRW)
    assert bar.low == Money(amount=Decimal("70800"), currency=Currency.KRW)
    assert bar.close == Money(amount=Decimal("72000"), currency=Currency.KRW)
    assert bar.volume == Decimal("1234567")


@pytest.mark.asyncio
async def test_get_ohlcv_1d_maps_candles(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["query"] = query
        return CandlePageResponse.model_validate({
            "candles": [
                {
                    "timestamp": "2026-06-07T00:00:00+09:00",
                    "openPrice": "71000",
                    "highPrice": "73000",
                    "lowPrice": "70000",
                    "closePrice": "72000",
                    "volume": "9876543",
                    "currency": "KRW",
                }
            ]
        })

    monkeypatch.setattr(market_mod, "call", fake_call)

    bars = await _client().get_ohlcv("005930", interval="1d")

    assert captured["query"]["interval"] == "1d"
    assert captured["query"]["count"] == 100  # default when limit=None
    assert len(bars) == 1


@pytest.mark.asyncio
async def test_get_ohlcv_end_adds_before_param(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["query"] = query
        return CandlePageResponse.model_validate({"candles": []})

    monkeypatch.setattr(market_mod, "call", fake_call)

    from datetime import datetime, timezone
    end_dt = datetime(2026, 6, 8, 10, 0, 0, tzinfo=timezone.utc)
    await _client().get_ohlcv("005930", interval="1m", end=end_dt)

    assert "before" in captured["query"]
    assert "2026-06-08" in captured["query"]["before"]


@pytest.mark.asyncio
async def test_get_ohlcv_count_capped_at_200(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["query"] = query
        return CandlePageResponse.model_validate({"candles": []})

    monkeypatch.setattr(market_mod, "call", fake_call)

    await _client().get_ohlcv("005930", interval="1d", limit=9999)
    assert captured["query"]["count"] == 200


# ── get_price_limits ──────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_price_limits_maps_upper_lower(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["executor_cls"] = executor_cls
        captured["query"] = query
        return PriceLimitResponse.model_validate({
            "timestamp": "2026-06-08T10:30:00+09:00",
            "upperLimitPrice": "93600",
            "lowerLimitPrice": "50400",
            "currency": "KRW",
        })

    monkeypatch.setattr(market_mod, "call", fake_call)

    pl = await _client().get_price_limits("005930")

    assert captured["executor_cls"] is GetPriceLimitExecutor
    assert captured["query"] == {"symbol": "005930"}
    assert pl.upper_limit == Money(amount=Decimal("93600"), currency=Currency.KRW)
    assert pl.lower_limit == Money(amount=Decimal("50400"), currency=Currency.KRW)
    assert pl.as_of is not None


@pytest.mark.asyncio
async def test_get_price_limits_none_for_us_stock(monkeypatch):
    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        return PriceLimitResponse.model_validate({
            "timestamp": "2026-06-08T10:30:00+09:00",
            "upperLimitPrice": None,
            "lowerLimitPrice": None,
            "currency": "USD",
        })

    monkeypatch.setattr(market_mod, "call", fake_call)

    pl = await _client().get_price_limits("NASD:AAPL")

    assert pl.upper_limit is None
    assert pl.lower_limit is None
