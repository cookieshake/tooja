"""Unit tests for TossInfoClient.

All calls are intercepted via ``monkeypatch.setattr(info_mod, "call", fake_call)``.
Response objects are built with ``Model.model_validate({...wire json...})`` to
mirror the exact shapes that the raw layer produces at runtime.
"""

from __future__ import annotations

from datetime import date

import pytest

import tooja.brokers.toss.info as info_mod
from tooja.brokers.toss.info import TossInfoClient
from tooja.brokers.toss.raw.market_info.get_kr_market_calendar import (
    GetKrMarketCalendarExecutor,
)
from tooja.brokers.toss.raw.models import KrMarketCalendarResponse
from tooja.brokers.toss.raw.stock_info.get_stock_warnings import (
    GetStockWarningsExecutor,
    GetStockWarningsResult,
)
from tooja.brokers.toss.raw.stock_info.get_stocks import (
    GetStocksExecutor,
    GetStocksResult,
)
from tooja.core.enums import Exchange
from tooja.core.errors import SymbolNotFound
from tooja.core.models import Symbol

# ── fixture helpers ───────────────────────────────────────────────────────────

# A minimal valid StockInfo wire payload (all required fields).
_STOCK_WIRE = {
    "symbol": "005930",
    "name": "삼성전자",
    "englishName": "Samsung Electronics",
    "isinCode": "KR7005930003",
    "market": "KOSPI",
    "securityType": "STOCK",
    "isCommonShare": True,
    "status": "ACTIVE",
    "currency": "KRW",
    "sharesOutstanding": "5969782550",
}


def _dummy_broker() -> object:
    """Return a minimal broker object (call is monkeypatched, so only identity matters)."""
    return object()


def _client() -> TossInfoClient:
    return TossInfoClient(_dummy_broker())


# ── get_stock ─────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_stock_returns_mapped_stock_info(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["executor_cls"] = executor_cls
        captured["query"] = query
        return GetStocksResult.model_validate({"root": [_STOCK_WIRE]})

    monkeypatch.setattr(info_mod, "call", fake_call)

    info = await _client().get_stock("005930")

    assert captured["executor_cls"] is GetStocksExecutor
    assert captured["query"] == {"symbols": "005930"}
    assert info.symbol.ticker == "005930"
    assert info.symbol.exchange is Exchange.KRX
    assert info.name == "삼성전자"


@pytest.mark.asyncio
async def test_get_stock_accepts_symbol_object(monkeypatch):
    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        return GetStocksResult.model_validate({"root": [_STOCK_WIRE]})

    monkeypatch.setattr(info_mod, "call", fake_call)

    sym = Symbol(ticker="005930", exchange=Exchange.KRX)
    info = await _client().get_stock(sym)
    assert info.symbol.ticker == "005930"


@pytest.mark.asyncio
async def test_get_stock_raises_symbol_not_found_when_empty(monkeypatch):
    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        return GetStocksResult.model_validate({"root": []})

    monkeypatch.setattr(info_mod, "call", fake_call)

    with pytest.raises(SymbolNotFound):
        await _client().get_stock("NONEXISTENT")


# ── get_warnings ──────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_warnings_maps_overheated_flag(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["executor_cls"] = executor_cls
        captured["path_params"] = path_params
        return GetStockWarningsResult.model_validate({
            "root": [{"warningType": "OVERHEATED", "startDate": "2026-06-01", "endDate": "2026-06-30"}]
        })

    monkeypatch.setattr(info_mod, "call", fake_call)

    warnings = await _client().get_warnings("005930")

    assert captured["executor_cls"] is GetStockWarningsExecutor
    assert captured["path_params"] == {"symbol": "005930"}
    assert warnings.is_overheated is True


@pytest.mark.asyncio
async def test_get_warnings_empty_list_returns_no_flags(monkeypatch):
    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        return GetStockWarningsResult.model_validate({"root": []})

    monkeypatch.setattr(info_mod, "call", fake_call)

    warnings = await _client().get_warnings("005930")

    assert warnings.is_overheated is None
    assert warnings.is_warning is None
    assert warnings.is_liquidation is None


@pytest.mark.asyncio
async def test_get_warnings_accepts_symbol_object(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["path_params"] = path_params
        return GetStockWarningsResult.model_validate({"root": []})

    monkeypatch.setattr(info_mod, "call", fake_call)

    sym = Symbol(ticker="005930", exchange=Exchange.KRX)
    await _client().get_warnings(sym)

    assert captured["path_params"] == {"symbol": "005930"}


# ── is_holiday ────────────────────────────────────────────────────────────────

# Wire helper: build a KrMarketCalendarResponse with a given today.date and
# an optional integrated hours block (None means closed/holiday).

def _make_calendar_resp(today_date: str, *, integrated: dict | None) -> KrMarketCalendarResponse:
    """Minimal KrMarketCalendarResponse for testing is_holiday."""
    # previous_business_day and next_business_day are required fields; use the
    # same date as placeholders — the impl only reads .today.
    day = {"date": today_date, "integrated": integrated}
    return KrMarketCalendarResponse.model_validate({
        "today": day,
        "previousBusinessDay": {"date": "2026-01-01"},
        "nextBusinessDay": {"date": "2026-01-02"},
    })


# A minimal integrated hours payload: regular market session only.
_INTEGRATED_OPEN = {
    "preMarket": None,
    "regularMarket": {"startTime": "09:00", "endTime": "15:30"},
    "afterMarket": None,
}


@pytest.mark.asyncio
async def test_is_holiday_returns_false_on_business_day(monkeypatch):
    """Today matches the requested date and integrated hours exist → business day."""
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["executor_cls"] = executor_cls
        captured["query"] = query
        return _make_calendar_resp("2026-06-09", integrated=_INTEGRATED_OPEN)

    monkeypatch.setattr(info_mod, "call", fake_call)

    result = await _client().is_holiday(date(2026, 6, 9))

    assert captured["executor_cls"] is GetKrMarketCalendarExecutor
    assert captured["query"] == {"date": "2026-06-09"}
    assert result is False


@pytest.mark.asyncio
async def test_is_holiday_returns_true_when_integrated_is_none(monkeypatch):
    """Date matches but integrated is None → both exchanges closed → holiday."""
    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        return _make_calendar_resp("2026-06-07", integrated=None)

    monkeypatch.setattr(info_mod, "call", fake_call)

    result = await _client().is_holiday(date(2026, 6, 7))

    assert result is True


@pytest.mark.asyncio
async def test_is_holiday_returns_true_when_date_snapped(monkeypatch):
    """API returned a different date (snapped to nearest business day) → holiday."""
    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        # Requested 2026-06-06 (Sunday) but API returned Monday 2026-06-08
        return _make_calendar_resp("2026-06-08", integrated=_INTEGRATED_OPEN)

    monkeypatch.setattr(info_mod, "call", fake_call)

    result = await _client().is_holiday(date(2026, 6, 6))

    assert result is True
