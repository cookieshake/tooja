"""Unit tests for the analytics / overseas / order-update mappers added in
the gap-fill round."""

from __future__ import annotations

from decimal import Decimal
from types import SimpleNamespace

from tooja.brokers.kis._mappers import (
    financial_summary_from_ratio_row,
    margin_balance_from_row,
    ohlcv_from_overseas_daily_item,
    order_update_from_ws_record,
    program_trading_from_row,
    quote_from_overseas_price,
    ranking_entry_from_credit_balance_row,
    ranking_entry_from_short_row,
    securities_lending_from_row,
    short_selling_from_row,
    trading_halt_from_vi_row,
)
from tooja.core.enums import Currency, Exchange, FinancialPeriod, OrderStatus
from tooja.core.models import Symbol


_KRX = Symbol(ticker="005930", exchange=Exchange.KRX)
_NASD = Symbol(ticker="AAPL", exchange=Exchange.NASD)


def _ns(**kw):
    return SimpleNamespace(**kw)


# ─── analytics ───────────────────────────────────────


def test_program_trading_zero_arbitrage_total_as_non_arb():
    row = _ns(stck_bsop_date="20260601", whol_smtn_ntby_tr_pbmn="123456789")
    p = program_trading_from_row(_KRX, row, raw_row={})
    assert p is not None
    assert p.arbitrage_net.amount == Decimal(0)
    assert p.non_arbitrage_net.amount == Decimal("123456789")


def test_short_selling_returns_volume_only_no_value():
    row = _ns(stck_bsop_date="20260601", ssts_cntg_qty="500000", ssts_vol_rlim="3.5")
    s = short_selling_from_row(_KRX, row, raw_row={})
    assert s is not None
    assert s.short_volume == Decimal("500000")
    assert s.short_ratio == Decimal("3.5")
    assert s.short_value.amount == Decimal(0)  # placeholder


def test_margin_balance_converts_manwon_to_krw():
    row = _ns(deal_date="20260601", whol_loan_rmnd_amt="5000")  # 5,000 만원
    m = margin_balance_from_row(_KRX, row, raw_row={})
    assert m is not None
    assert m.margin_loan.amount == Decimal("50000000")  # 50M KRW


def test_securities_lending_uses_rmnd_amt():
    row = _ns(bsop_date="20260601", rmnd_amt="123456")
    s = securities_lending_from_row(_KRX, row, raw_row={})
    assert s is not None
    assert s.balance.amount == Decimal("123456")


# ─── info ────────────────────────────────────────────


def test_financial_summary_uses_eps_bps_roe():
    row = _ns(stac_yymm="202503", eps="5400", bps="48000", roe_val="11.2")
    s = financial_summary_from_ratio_row(_KRX, row, raw_row={}, period=FinancialPeriod.QUARTERLY)
    assert s is not None
    assert s.eps.amount == Decimal("5400")
    assert s.bps.amount == Decimal("48000")
    assert s.roe == Decimal("11.2")
    assert s.fiscal_date.year == 2025
    assert s.fiscal_date.month == 3


def test_trading_halt_only_emits_when_vi_active():
    inactive = _ns(mksc_shrn_iscd="005930", vi_cls_code="N",
                   bsop_date="20260601", cntg_vi_hour="143000", vi_cncl_hour="143200")
    assert trading_halt_from_vi_row(inactive, raw_row={}) is None

    active = _ns(mksc_shrn_iscd="005930", vi_cls_code="Y",
                 bsop_date="20260601", cntg_vi_hour="143000", vi_cncl_hour="000000")
    h = trading_halt_from_vi_row(active, raw_row={})
    assert h is not None
    assert h.end is None
    assert h.reason == "VI"


# ─── overseas ────────────────────────────────────────


def test_overseas_quote_uses_usd_for_nasd():
    out = _ns(last="190.50", diff="2.25", sign="2", rate="1.19",
              base="188.25", tvol="123456")
    q = quote_from_overseas_price(_NASD, out, raw={})
    assert q.price.currency is Currency.USD
    assert q.price.amount == Decimal("190.50")
    assert q.change.amount == Decimal("2.25")


def test_overseas_quote_negative_change_on_sign_5():
    out = _ns(last="188.00", diff="2.25", sign="5", rate="-1.18",
              base="190.25", tvol=None)
    q = quote_from_overseas_price(_NASD, out, raw={})
    assert q.change.amount == Decimal("-2.25")


def test_overseas_ohlcv_uses_usd_quantum():
    item = _ns(xymd="20260601", open="100.10", high="101.20", low="99.30",
               clos="100.50", tvol="500000")
    bar = ohlcv_from_overseas_daily_item(_NASD, item)
    assert bar is not None
    assert bar.close.currency is Currency.USD
    assert bar.volume == Decimal("500000")


# ─── rankings ────────────────────────────────────────


def test_ranking_short_uses_ssts_cntg_qty():
    row = _ns(mksc_shrn_iscd="005930", hts_kor_isnm="삼성전자",
              data_rank="3", ssts_cntg_qty="123000", stck_prpr="70000",
              prdy_ctrt="0.5")
    e = ranking_entry_from_short_row(row, raw_row={})
    assert e is not None
    assert e.value == Decimal("123000")
    assert e.rank == 3


def test_ranking_credit_balance_falls_back_through_fields():
    row = _ns(mksc_shrn_iscd="005930", hts_kor_isnm="삼성전자",
              data_rank="1", whol_loan_rmnd="999", stck_prpr="70000",
              prdy_ctrt=None)
    e = ranking_entry_from_credit_balance_row(row, raw_row={})
    assert e is not None
    assert e.value == Decimal("999")


# ─── order WS ────────────────────────────────────────


def test_order_update_rejected_when_rfus_yn_is_1():
    rec = {
        "ODER_NO": "0000000001", "STCK_SHRN_ISCD": "005930",
        "RFUS_YN": "1", "CNTG_YN": "1",
        "CNTG_QTY": "0", "CNTG_UNPR": "0",
        "STCK_CNTG_HOUR": "143000", "ODER_QTY": "10",
    }
    u = order_update_from_ws_record(rec)
    assert u is not None
    assert u.status is OrderStatus.REJECTED


def test_order_update_filled_when_cntg_yn_is_2_and_qty_matches():
    rec = {
        "ODER_NO": "0000000002", "STCK_SHRN_ISCD": "005930",
        "RFUS_YN": "0", "CNTG_YN": "2",
        "CNTG_QTY": "10", "CNTG_UNPR": "70000",
        "STCK_CNTG_HOUR": "143000", "ODER_QTY": "10",
    }
    u = order_update_from_ws_record(rec)
    assert u is not None
    assert u.status is OrderStatus.FILLED
    assert u.filled_qty == Decimal("10")
    assert u.avg_fill_price.amount == Decimal("70000")


def test_order_update_open_when_cntg_yn_is_1():
    rec = {
        "ODER_NO": "0000000003", "STCK_SHRN_ISCD": "005930",
        "RFUS_YN": "0", "CNTG_YN": "1",
        "CNTG_QTY": "0", "CNTG_UNPR": "0",
        "STCK_CNTG_HOUR": "143000", "ODER_QTY": "10",
    }
    u = order_update_from_ws_record(rec)
    assert u is not None
    assert u.status is OrderStatus.OPEN
