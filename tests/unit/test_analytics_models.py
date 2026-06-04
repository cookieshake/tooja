from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError

from tooja.core.enums import Currency
from tooja.core.money import Money
from tooja.core.models import (
    InvestorFlow,
    MarginBalance,
    ProgramTrading,
    SecuritiesLending,
    ShortSellingDaily,
    Symbol,
)


def _krw(amount: int | str) -> Money:
    return Money(amount=Decimal(amount), currency=Currency.KRW)


def _usd(amount: int | str) -> Money:
    return Money(amount=Decimal(amount), currency=Currency.USD)


def test_investor_flow_breakdown():
    f = InvestorFlow(
        symbol=Symbol(ticker="005930"),
        date=date(2026, 5, 30),
        individual_net=_krw(100_000),
        foreign_net=_krw(-50_000),
        institutional_net=_krw(-30_000),
        institutional_breakdown={"securities_firm": _krw(-10_000), "investment_trust": _krw(-20_000)},
    )
    assert f.institutional_breakdown["investment_trust"] == _krw(-20_000)


def test_investor_flow_rejects_mixed_currency_in_breakdown():
    with pytest.raises(ValidationError, match="inconsistent currencies"):
        InvestorFlow(
            symbol=Symbol(ticker="005930"),
            date=date(2026, 5, 30),
            individual_net=_krw(0),
            foreign_net=_krw(0),
            institutional_net=_krw(0),
            institutional_breakdown={"securities_firm": _usd("100.00")},
        )


def test_program_trading():
    p = ProgramTrading(
        symbol=Symbol(ticker="005930"),
        date=date(2026, 5, 30),
        arbitrage_net=_krw(0),
        non_arbitrage_net=_krw(-200_000),
    )
    assert p.arbitrage_net == _krw(0)


def test_short_selling_value_is_money_volume_decimal():
    s = ShortSellingDaily(
        symbol=Symbol(ticker="005930"),
        date=date(2026, 5, 30),
        short_volume=Decimal("12345"),
        short_value=_krw(864_150_000),
    )
    assert s.short_ratio is None
    assert s.short_value.currency is Currency.KRW
    assert s.short_volume == Decimal("12345")


def test_margin_balance_optional_stock_loan():
    m = MarginBalance(
        symbol=Symbol(ticker="005930"),
        date=date(2026, 5, 30),
        margin_loan=_krw(1_000_000_000),
    )
    assert m.stock_loan is None


def test_securities_lending():
    sl = SecuritiesLending(
        symbol=Symbol(ticker="005930"),
        date=date(2026, 5, 30),
        balance=_krw(5_000_000_000),
    )
    assert sl.new_loan is None
