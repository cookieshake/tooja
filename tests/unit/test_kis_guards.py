"""Subclient guards added in the second Gemini review round:
- info / analytics reject overseas symbols up front
- kst_today / kst_today_yyyymmdd anchor to KST regardless of host TZ
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

import pytest

from tooja.brokers.kis._mappers import kst_today, kst_today_yyyymmdd
from tooja.brokers.kis.analytics import _as_symbol as analytics_as_symbol
from tooja.brokers.kis.info import _as_symbol as info_as_symbol
from tooja.core.enums import Exchange
from tooja.core.errors import UnsupportedOperation
from tooja.core.models import Symbol


def test_kst_today_matches_kst_calendar_date():
    """kst_today should equal (now + 9h).date() regardless of host TZ."""
    expected = (datetime.now(timezone.utc) + timedelta(hours=9)).date()
    assert kst_today() == expected


def test_kst_today_yyyymmdd_matches_kst_today():
    assert kst_today_yyyymmdd() == kst_today().strftime("%Y%m%d")


def test_kst_today_returns_date_instance():
    assert isinstance(kst_today(), date)


def test_info_rejects_overseas_symbol():
    with pytest.raises(UnsupportedOperation, match="domestic"):
        info_as_symbol(Symbol(ticker="AAPL", exchange=Exchange.NASD))


def test_info_accepts_krx_symbol():
    sym = info_as_symbol(Symbol(ticker="005930"))
    assert sym.exchange is Exchange.KRX


def test_info_accepts_nxt_symbol():
    sym = info_as_symbol(Symbol(ticker="005930", exchange=Exchange.NXT))
    assert sym.exchange is Exchange.NXT


def test_analytics_rejects_overseas_symbol():
    with pytest.raises(UnsupportedOperation, match="domestic"):
        analytics_as_symbol(Symbol(ticker="AAPL", exchange=Exchange.NASD))


def test_analytics_rejects_exchange_object():
    with pytest.raises(UnsupportedOperation, match="Exchange"):
        analytics_as_symbol(Exchange.KRX)


def test_analytics_accepts_krx_symbol():
    sym = analytics_as_symbol(Symbol(ticker="005930"))
    assert sym.exchange is Exchange.KRX
