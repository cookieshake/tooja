"""Unit tests for KIS raw -> domain mappers."""

from __future__ import annotations

from decimal import Decimal
from types import SimpleNamespace

from tooja.brokers.kis._mappers import (
    balance_from_inquire,
    map_order_status,
    ohlcv_from_chartprice_item,
    orderbook_from_inquire_asking,
    position_from_balance_row,
    quote_from_inquire_price,
    quote_from_ws_record,
    ranking_entry_from_volume_row,
    stock_info_from_search,
)
from tooja.core.enums import Currency, OrderStatus
from tooja.core.models import Symbol


_SYM = Symbol(ticker="005930")


def _ns(**kw) -> SimpleNamespace:
    return SimpleNamespace(**kw)


def test_parse_kst_datetime_returns_none_when_time_missing():
    """Regression: returning midnight when t is missing made every
    `_parse_kst_datetime(d, t) or _utc_now()` fallback dead code."""
    from tooja.brokers.kis._mappers import _parse_kst_datetime
    assert _parse_kst_datetime("20260601", None) is None
    assert _parse_kst_datetime("20260601", "") is None
    # Sanity: with a real time, still returns a datetime.
    assert _parse_kst_datetime("20260601", "143000") is not None


def test_dec_float_routes_through_str_to_avoid_binary_artifacts():
    """Regression: Decimal(0.1) yields 0.1000000000000000055511151231257827021181583404541015625;
    we must convert floats via str() first to get a clean 0.1."""
    from tooja.brokers.kis._mappers import _dec

    assert _dec(0.1) == Decimal("0.1")
    assert _dec(70000.50) == Decimal("70000.5")


def test_quote_basic_fields():
    output = _ns(
        stck_prpr="70000", prdy_vrss="500", prdy_vrss_sign="2",
        prdy_ctrt="0.71", stck_oprc="69500", stck_hgpr="70500",
        stck_lwpr="69000", stck_sdpr="69500", acml_vol="12345678",
    )
    q = quote_from_inquire_price(_SYM, output, raw={"x": 1})
    assert q.price.amount == Decimal("70000")
    assert q.price.currency is Currency.KRW
    assert q.change.amount == Decimal("500")
    assert q.volume == Decimal("12345678")


def test_quote_negative_change_when_sign_is_down():
    output = _ns(
        stck_prpr="69000", prdy_vrss="500", prdy_vrss_sign="5",
        prdy_ctrt=None, stck_oprc=None, stck_hgpr=None,
        stck_lwpr=None, stck_sdpr=None, acml_vol=None,
    )
    q = quote_from_inquire_price(_SYM, output, raw={})
    assert q.change.amount == Decimal("-500")


def test_orderbook_skips_zero_levels():
    output = _ns(**{
        "aspr_acpt_hour": "143000",
        "askp1": "70000", "askp_rsqn1": "100",
        "askp2": "0", "askp_rsqn2": "0",
        "bidp1": "69900", "bidp_rsqn1": "200",
    })
    for i in range(2, 11):
        setattr(output, f"askp{i}", "0")
        setattr(output, f"askp_rsqn{i}", "0")
    for i in range(2, 11):
        setattr(output, f"bidp{i}", "0")
        setattr(output, f"bidp_rsqn{i}", "0")

    ob = orderbook_from_inquire_asking(_SYM, output, raw={})
    assert len(ob.asks) == 1
    assert len(ob.bids) == 1
    assert ob.asks[0].price.amount == Decimal("70000")


def test_ohlcv_returns_none_when_fields_missing():
    item = _ns(stck_bsop_date="20260601", stck_clpr=None, stck_oprc=None,
               stck_hgpr=None, stck_lwpr=None, acml_vol=None)
    assert ohlcv_from_chartprice_item(_SYM, item) is None


def test_ohlcv_happy_path():
    item = _ns(
        stck_bsop_date="20260601",
        stck_clpr="70000", stck_oprc="69500",
        stck_hgpr="70500", stck_lwpr="69000",
        acml_vol="123456",
    )
    bar = ohlcv_from_chartprice_item(_SYM, item)
    assert bar is not None
    assert bar.close.amount == Decimal("70000")
    assert bar.volume == Decimal("123456")


def test_position_skips_zero_qty():
    row = _ns(hldg_qty="0", pdno="005930", pchs_avg_pric="70000", prpr="70500",
              evlu_amt=None, evlu_pfls_amt=None, evlu_pfls_rt=None)
    assert position_from_balance_row(row) is None


def test_balance_from_inquire():
    row = _ns(hldg_qty="10", pdno="005930", pchs_avg_pric="70000", prpr="70500",
              evlu_amt="705000", evlu_pfls_amt="5000", evlu_pfls_rt="0.71")
    summary = _ns(dnca_tot_amt="1000000", tot_evlu_amt="1705000")
    b = balance_from_inquire([row], [summary], raw={})
    assert b.total_asset is not None
    assert b.total_asset.amount == Decimal("1705000")
    assert len(b.positions) == 1
    assert len(b.cash) == 1


def test_map_order_status_codes():
    assert map_order_status("01", Decimal(10), Decimal(0)) == OrderStatus.OPEN
    assert map_order_status("02", Decimal(10), Decimal(3)) == OrderStatus.PARTIALLY_FILLED
    assert map_order_status("03", Decimal(10), Decimal(10)) == OrderStatus.FILLED


def test_map_order_status_inferred_from_quantities():
    assert map_order_status(None, Decimal(10), Decimal(0)) == OrderStatus.OPEN
    assert map_order_status(None, Decimal(10), Decimal(5)) == OrderStatus.PARTIALLY_FILLED
    assert map_order_status(None, Decimal(10), Decimal(10)) == OrderStatus.FILLED


def test_stock_info_from_search():
    out = _ns(
        prdt_abrv_name="삼성전자", prdt_name="삼성전자보통주",
        lstg_cptl_amt="500000000000000", papr="100", lstg_stqt="5969782550",
        scts_mket_lstg_dt="19750611", kosdaq_mket_lstg_dt=None,
    )
    info = stock_info_from_search(_SYM, out, raw={})
    assert info.name == "삼성전자"
    assert info.par_value.amount == Decimal("100")
    assert info.listed_at is not None


def test_ranking_entry_from_volume_row():
    row = _ns(
        data_rank="1", mksc_shrn_iscd="005930", hts_kor_isnm="삼성전자",
        acml_vol="12345678", stck_prpr="70000", prdy_ctrt="0.71",
    )
    e = ranking_entry_from_volume_row(row, raw_row={})
    assert e is not None
    assert e.rank == 1
    assert e.symbol.ticker == "005930"
    assert e.value == Decimal("12345678")


def test_quote_from_ws_record():
    record = {
        "MKSC_SHRN_ISCD": "005930", "STCK_CNTG_HOUR": "143000",
        "STCK_PRPR": "70000", "PRDY_VRSS_SIGN": "2",
        "PRDY_VRSS": "500", "PRDY_CTRT": "0.71",
        "WGHN_AVRG_STCK_PRC": "69800", "STCK_OPRC": "69500",
        "STCK_HGPR": "70500", "STCK_LWPR": "69000",
        "ASKP1": "70100", "BIDP1": "69900",
        "CNTG_VOL": "100", "ACML_VOL": "12345678", "ACML_TR_PBMN": "8e11",
    }
    q = quote_from_ws_record(record)
    assert q is not None
    assert q.price.amount == Decimal("70000")
    assert q.symbol.ticker == "005930"
