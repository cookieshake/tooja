"""Unit tests for Toss raw→domain mappers."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

import pytest

from tooja.core.enums import AssetClass, Currency, Exchange, OrderSide, OrderStatus
from tooja.core.money import Money
from tooja.brokers.toss import _mappers as m
from tooja.brokers.toss.raw.models import (
    Candle,
    HoldingsOverview,
    Order as TossOrder,
    OrderbookResponse,
    PriceLimitResponse,
    PriceResponse,
    StockInfo as TossStockInfo,
    StockWarning,
)


# ─── primitives ──────────────────────────────────────────


def test_to_currency():
    assert m.to_currency("KRW") is Currency.KRW
    assert m.to_currency("usd") is Currency.USD
    assert m.to_currency(Currency.KRW) is Currency.KRW


def test_money_none_safe():
    assert m._money(None, "KRW") is None
    money = m._money(Decimal("1000"), "KRW")
    assert money == Money(amount=Decimal("1000"), currency=Currency.KRW)


def test_parse_dt_with_offset():
    dt = m._parse_dt("2026-06-08T10:30:00+09:00")
    assert isinstance(dt, datetime)
    assert dt.utcoffset().total_seconds() == 9 * 3600
    assert m._parse_dt(None) is None


def test_parse_date():
    assert m._parse_date("2020-01-15").isoformat() == "2020-01-15"
    assert m._parse_date(None) is None


# ─── symbol ──────────────────────────────────────────────


def test_to_symbol_digit_only_krx():
    s = m.to_symbol("005930")
    assert s.ticker == "005930"
    assert s.exchange is Exchange.KRX
    assert s.asset is AssetClass.STOCK


def test_to_symbol_alpha_nasd():
    s = m.to_symbol("AAPL")
    assert s.exchange is Exchange.NASD


def test_to_symbol_market_hints():
    assert m.to_symbol("X", market="KOSPI").exchange is Exchange.KRX
    assert m.to_symbol("X", market="KOSDAQ").exchange is Exchange.KRX
    assert m.to_symbol("X", market="KR_ETC").exchange is Exchange.KRX
    assert m.to_symbol("X", market="NYSE").exchange is Exchange.NYSE
    assert m.to_symbol("X", market="NASDAQ").exchange is Exchange.NASD
    assert m.to_symbol("X", market="AMEX").exchange is Exchange.AMEX
    assert m.to_symbol("005930", market="US_ETC").exchange is Exchange.NASD


def test_to_symbol_country_hints():
    assert m.to_symbol("AAPL", market_country="KR").exchange is Exchange.KRX
    assert m.to_symbol("005930", market_country="US").exchange is Exchange.NASD


# ─── market data ─────────────────────────────────────────


def test_quote_from_price():
    p = PriceResponse.model_validate(
        {
            "symbol": "005930",
            "timestamp": "2026-06-08T10:30:00+09:00",
            "lastPrice": "72000",
            "currency": "KRW",
        }
    )
    q = m.quote_from_price(p)
    assert q.symbol == m.to_symbol("005930")
    assert q.price == Money(amount=Decimal("72000"), currency=Currency.KRW)
    assert q.price.currency is Currency.KRW
    assert q.time.utcoffset().total_seconds() == 9 * 3600


def test_quote_from_price_no_timestamp_uses_now():
    p = PriceResponse.model_validate(
        {"symbol": "AAPL", "lastPrice": "190.5", "currency": "USD"}
    )
    q = m.quote_from_price(p)
    assert q.symbol.exchange is Exchange.NASD
    assert q.price.currency is Currency.USD
    assert isinstance(q.time, datetime)


def test_orderbook_from_response_trims_to_depth():
    r = OrderbookResponse.model_validate(
        {
            "timestamp": "2026-06-08T10:30:00+09:00",
            "currency": "KRW",
            "asks": [
                {"price": "72100", "volume": "10"},
                {"price": "72200", "volume": "20"},
                {"price": "72300", "volume": "30"},
            ],
            "bids": [
                {"price": "72000", "volume": "5"},
                {"price": "71900", "volume": "15"},
            ],
        }
    )
    sym = m.to_symbol("005930")
    ob = m.orderbook_from_response(sym, r, depth=2)
    assert len(ob.asks) == 2
    assert len(ob.bids) == 2
    assert ob.asks[0].price == Money(amount=Decimal("72100"), currency=Currency.KRW)
    assert ob.asks[0].qty == Decimal("10")


def test_ohlcv_from_candle():
    c = Candle.model_validate(
        {
            "timestamp": "2026-06-08T00:00:00+09:00",
            "openPrice": "71000",
            "highPrice": "72500",
            "lowPrice": "70800",
            "closePrice": "72000",
            "volume": "1234567",
            "currency": "KRW",
        }
    )
    sym = m.to_symbol("005930")
    o = m.ohlcv_from_candle(sym, c)
    assert o.open == Money(amount=Decimal("71000"), currency=Currency.KRW)
    assert o.high == Money(amount=Decimal("72500"), currency=Currency.KRW)
    assert o.low == Money(amount=Decimal("70800"), currency=Currency.KRW)
    assert o.close == Money(amount=Decimal("72000"), currency=Currency.KRW)
    assert o.volume == Decimal("1234567")


def test_price_limit_kr_has_bounds():
    r = PriceLimitResponse.model_validate(
        {
            "timestamp": "2026-06-08T10:30:00+09:00",
            "upperLimitPrice": "93600",
            "lowerLimitPrice": "50400",
            "currency": "KRW",
        }
    )
    pl = m.price_limit_from_response(m.to_symbol("005930"), r)
    assert pl.upper_limit == Money(amount=Decimal("93600"), currency=Currency.KRW)
    assert pl.lower_limit == Money(amount=Decimal("50400"), currency=Currency.KRW)
    assert pl.as_of is not None


def test_price_limit_us_none():
    r = PriceLimitResponse.model_validate(
        {
            "timestamp": "2026-06-08T10:30:00+09:00",
            "upperLimitPrice": None,
            "lowerLimitPrice": None,
            "currency": "USD",
        }
    )
    pl = m.price_limit_from_response(m.to_symbol("AAPL"), r)
    assert pl.upper_limit is None
    assert pl.lower_limit is None


# ─── account ─────────────────────────────────────────────


def _holdings_payload() -> dict:
    return {
        "totalPurchaseAmount": {"krw": "1000000", "usd": None},
        "marketValue": {
            "amount": {"krw": "1100000", "usd": None},
            "amountAfterCost": {"krw": "1098000", "usd": None},
        },
        "profitLoss": {
            "amount": {"krw": "100000", "usd": None},
            "amountAfterCost": {"krw": "98000", "usd": None},
            "rate": "0.1",
            "rateAfterCost": "0.098",
        },
        "dailyProfitLoss": {
            "amount": {"krw": "5000", "usd": None},
            "amountAfterCost": {"krw": "4900", "usd": None},
            "rate": "0.005",
            "rateAfterCost": "0.0049",
        },
        "items": [
            {
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
                    "amountAfterCost": "719000",
                },
                "profitLoss": {
                    "amount": "20000",
                    "amountAfterCost": "19000",
                    "rate": "0.0285",
                    "rateAfterCost": "0.027",
                },
                "dailyProfitLoss": {
                    "amount": "1000",
                    "amountAfterCost": "950",
                    "rate": "0.0014",
                    "rateAfterCost": "0.0013",
                },
                "cost": {"commission": "100", "tax": "0"},
            }
        ],
    }


def test_position_from_holding():
    o = HoldingsOverview.model_validate(_holdings_payload())
    pos = m.position_from_holding(o.items[0])
    assert pos.symbol == m.to_symbol("005930", market_country="KR")
    assert pos.symbol.exchange is Exchange.KRX
    assert pos.qty == Decimal("10")
    assert pos.avg_price == Money(amount=Decimal("70000"), currency=Currency.KRW)
    assert pos.current_price == Money(amount=Decimal("72000"), currency=Currency.KRW)
    assert pos.market_value == Money(amount=Decimal("720000"), currency=Currency.KRW)
    assert pos.pnl == Money(amount=Decimal("20000"), currency=Currency.KRW)
    assert pos.pnl_rate == Decimal("0.0285")


def test_balance_from_holdings_total_asset_krw_and_empty_cash():
    o = HoldingsOverview.model_validate(_holdings_payload())
    bal = m.balance_from_holdings(o)
    assert bal.total_asset == Money(amount=Decimal("1100000"), currency=Currency.KRW)
    assert bal.cash == []
    assert len(bal.positions) == 1


def test_balance_total_asset_none_when_krw_missing():
    payload = _holdings_payload()
    payload["marketValue"]["amount"]["krw"] = None
    o = HoldingsOverview.model_validate(payload)
    bal = m.balance_from_holdings(o)
    assert bal.total_asset is None


# ─── orders ──────────────────────────────────────────────


def _order_payload(status: str, *, order_type: str = "LIMIT", side: str = "BUY") -> dict:
    return {
        "orderId": "ord-1",
        "symbol": "005930",
        "side": side,
        "orderType": order_type,
        "timeInForce": "DAY",
        "status": status,
        "price": "72000",
        "quantity": "10",
        "orderAmount": "720000",
        "currency": "KRW",
        "orderedAt": "2026-06-08T10:30:00+09:00",
        "canceledAt": None,
        "execution": {
            "filledQuantity": "4",
            "averageFilledPrice": "71900",
            "filledAmount": "287600",
            "commission": "10",
            "tax": "0",
            "filledAt": "2026-06-08T10:31:00+09:00",
            "settlementDate": "2026-06-10",
        },
    }


@pytest.mark.parametrize(
    "toss_status, expected",
    [
        ("PENDING", OrderStatus.PENDING),
        ("PENDING_CANCEL", OrderStatus.OPEN),
        ("PENDING_REPLACE", OrderStatus.OPEN),
        ("PARTIAL_FILLED", OrderStatus.PARTIALLY_FILLED),
        ("FILLED", OrderStatus.FILLED),
        ("CANCELED", OrderStatus.CANCELLED),
        ("REJECTED", OrderStatus.REJECTED),
        ("CANCEL_REJECTED", OrderStatus.REJECTED),
        ("REPLACE_REJECTED", OrderStatus.REJECTED),
        ("REPLACED", OrderStatus.OPEN),
        ("SOME_FUTURE_STATUS", OrderStatus.PENDING),  # unknown → PENDING
    ],
)
def test_order_status_mapping(toss_status, expected):
    o = TossOrder.model_validate(_order_payload(toss_status))
    assert m.order_from_toss(o).status is expected


def test_order_side_and_type_and_fields():
    o = TossOrder.model_validate(_order_payload("PARTIAL_FILLED", order_type="LIMIT", side="SELL"))
    core = m.order_from_toss(o)
    assert core.order_id == "ord-1"
    assert core.symbol == m.to_symbol("005930")
    assert core.side is OrderSide.SELL
    assert core.type == "limit"
    assert core.qty == Decimal("10")
    assert core.filled_qty == Decimal("4")
    assert core.avg_fill_price == Money(amount=Decimal("71900"), currency=Currency.KRW)
    assert core.price == Money(amount=Decimal("72000"), currency=Currency.KRW)
    assert core.submitted_at is not None
    assert core.updated_at is None


def test_order_market_type_and_buy():
    o = TossOrder.model_validate(_order_payload("FILLED", order_type="MARKET", side="BUY"))
    core = m.order_from_toss(o)
    assert core.type == "market"
    assert core.side is OrderSide.BUY


# ─── info ────────────────────────────────────────────────


def test_stock_info_from_toss():
    s = TossStockInfo.model_validate(
        {
            "symbol": "005930",
            "name": "삼성전자",
            "englishName": "Samsung Electronics",
            "isinCode": "KR7005930003",
            "market": "KOSPI",
            "securityType": "COMMON",
            "isCommonShare": True,
            "status": "LISTED",
            "currency": "KRW",
            "listDate": "1975-06-11",
            "delistDate": None,
            "sharesOutstanding": "5969782550",
            "leverageFactor": None,
            "koreanMarketDetail": None,
        }
    )
    info = m.stock_info_from_toss(s)
    assert info.symbol == m.to_symbol("005930", market="KOSPI")
    assert info.symbol.exchange is Exchange.KRX
    assert info.name == "삼성전자"
    assert info.listed_at.isoformat() == "1975-06-11"
    assert info.listed_shares == Decimal("5969782550")
    assert info.sector is None
    assert info.market_cap is None


# ─── warnings ────────────────────────────────────────────


def _warning(warning_type: str) -> StockWarning:
    return StockWarning.model_validate(
        {
            "warningType": warning_type,
            "exchange": "KRX",
            "startDate": "2026-06-01",
            "endDate": None,
        }
    )


def test_stock_warnings_flag_mapping():
    sym = m.to_symbol("005930")
    w = m.stock_warnings_from_toss(
        sym, [_warning("INVESTMENT_RISK"), _warning("VI_STATIC")]
    )
    assert w.is_risk is True
    assert w.vi_triggered is True
    # Flags with no matching warning stay None.
    assert w.is_liquidation is None
    assert w.is_overheated is None
    assert w.is_warning is None
    assert w.is_caution is None
    assert w.is_trading_halt is None


def test_stock_warnings_liquidation_and_overheated_and_rights():
    sym = m.to_symbol("005930")
    w = m.stock_warnings_from_toss(
        sym,
        [
            _warning("liquidation_trading"),  # case-insensitive
            _warning("OVERHEATED"),
            _warning("STOCK_WARRANTS"),
        ],
    )
    assert w.is_liquidation is True
    assert w.is_overheated is True
    assert w.is_rights_offering is True


def test_stock_warnings_unknown_type_ignored():
    sym = m.to_symbol("005930")
    w = m.stock_warnings_from_toss(sym, [_warning("SOME_NEW_CODE")])
    # No flag set; no crash.
    assert w.is_risk is None
    assert w.vi_triggered is None
    assert w.symbol == sym
