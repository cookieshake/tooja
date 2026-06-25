from datetime import date, datetime, timezone
from decimal import Decimal


from tooja.core.enums import Currency, FinancialPeriod
from tooja.core.money import Money
from tooja.core.models import (
    Dividend,
    FinancialSummary,
    StockInfo,
    Symbol,
    TradingHalt,
)


def _krw(amount: int | str) -> Money:
    return Money(amount=Decimal(amount), currency=Currency.KRW)


def _usd(amount: int | str) -> Money:
    return Money(amount=Decimal(amount), currency=Currency.USD)


def test_stock_info_minimum():
    s = StockInfo(symbol=Symbol(ticker="005930"), name="Samsung Electronics")
    assert s.market_cap is None
    assert s.raw == {}


def test_stock_info_with_market_cap():
    s = StockInfo(
        symbol=Symbol(ticker="005930"),
        name="Samsung Electronics",
        par_value=_krw(100),
        market_cap=_krw(500_000_000_000_000),
    )
    assert s.market_cap.currency is Currency.KRW


def test_financial_summary_quarterly():
    f = FinancialSummary(
        symbol=Symbol(ticker="005930"),
        period=FinancialPeriod.QUARTERLY,
        fiscal_date=date(2026, 3, 31),
        revenue=_krw(75_000_000_000_000),
    )
    assert f.period == FinancialPeriod.QUARTERLY
    assert f.revenue.currency is Currency.KRW


def test_financial_summary_ratios_stay_decimal():
    """per/pbr/roe are ratios — keep them as Decimal, not Money."""
    f = FinancialSummary(
        symbol=Symbol(ticker="005930"),
        period=FinancialPeriod.ANNUAL,
        fiscal_date=date(2025, 12, 31),
        eps=_krw(7500),
        per=Decimal("9.3"),
        pbr=Decimal("1.2"),
        roe=Decimal("0.13"),
    )
    assert f.per == Decimal("9.3")


def test_dividend_default_cash():
    d = Dividend(
        symbol=Symbol(ticker="005930"),
        ex_date=date(2026, 12, 28),
        amount_per_share=_krw(361),
    )
    assert d.dividend_type == "cash"
    assert d.amount_per_share == _krw(361)


def test_trading_halt():
    h = TradingHalt(
        symbol=Symbol(ticker="005930"),
        start=datetime(2026, 5, 1, 9, 0, tzinfo=timezone.utc),
        reason="inquiry suspended",
    )
    assert h.end is None
