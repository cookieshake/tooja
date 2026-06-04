"""KIS raw response -> shared domain model converters.

These are deliberately small pure functions so subclients stay focused on
sequencing API calls rather than field-by-field translation. KIS uses string
numerics with comma separators in many places, so all numeric parsing flows
through `_dec` / `_int`.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any

from tooja.core.enums import Currency, Exchange, OrderSide, OrderStatus
from tooja.core.models import (
    Balance,
    OHLCV,
    Orderbook,
    OrderbookLevel,
    Position,
    Quote,
    Symbol,
)
from tooja.core.money import Money

KST_OFFSET_HOURS = 9


def _dec(v: Any) -> Decimal | None:
    if v is None:
        return None
    if isinstance(v, Decimal):
        return v
    if isinstance(v, str):
        v = v.strip().replace(",", "")
        if not v:
            return None
    try:
        return Decimal(v)
    except (InvalidOperation, ValueError, TypeError):
        return None


def _int(v: Any) -> int | None:
    d = _dec(v)
    return int(d) if d is not None else None


def _money_krw(v: Any) -> Money | None:
    d = _dec(v)
    if d is None:
        return None
    return Money(amount=d, currency=Currency.KRW)


def _kst_now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_kst_date(s: str) -> date | None:
    """KIS daily price uses YYYYMMDD."""
    if not s or len(s) != 8:
        return None
    try:
        return date(int(s[:4]), int(s[4:6]), int(s[6:8]))
    except ValueError:
        return None


def _parse_kst_datetime(d: str, t: str | None = None) -> datetime | None:
    """KIS uses YYYYMMDD + HHMMSS, KST. Return tz-aware UTC."""
    if not d or len(d) < 8:
        return None
    try:
        year, month, day = int(d[:4]), int(d[4:6]), int(d[6:8])
        if t and len(t) >= 6:
            hour, minute, sec = int(t[:2]), int(t[2:4]), int(t[4:6])
        else:
            hour = minute = sec = 0
        from datetime import timedelta
        kst = datetime(year, month, day, hour, minute, sec)
        return (kst - timedelta(hours=KST_OFFSET_HOURS)).replace(tzinfo=timezone.utc)
    except ValueError:
        return None


# ─── Market ──────────────────────────────────────────


def quote_from_inquire_price(
    symbol: Symbol, output: Any, raw: dict[str, Any]
) -> Quote:
    """Convert InquirePriceResponse.output to Quote."""
    price = _money_krw(getattr(output, "stck_prpr", None))
    if price is None:
        raise ValueError("KIS inquire-price returned no price")

    change = _money_krw(getattr(output, "prdy_vrss", None))
    sign = getattr(output, "prdy_vrss_sign", None)
    # KIS sign: 1/2 = up, 4/5 = down. Apply sign to change magnitude.
    if change is not None and sign in ("4", "5") and change.amount > 0:
        change = -change

    return Quote(
        symbol=symbol,
        price=price,
        time=_kst_now(),
        change=change,
        change_rate=_dec(getattr(output, "prdy_ctrt", None)),
        open=_money_krw(getattr(output, "stck_oprc", None)),
        high=_money_krw(getattr(output, "stck_hgpr", None)),
        low=_money_krw(getattr(output, "stck_lwpr", None)),
        prev_close=_money_krw(getattr(output, "stck_sdpr", None)),
        volume=_dec(getattr(output, "acml_vol", None)),
        raw=raw,
    )


def orderbook_from_inquire_asking(
    symbol: Symbol, output1: Any, raw: dict[str, Any], *, depth: int = 10
) -> Orderbook:
    """Build Orderbook from InquireAskingPriceExpCcn output1.

    KIS returns 10 levels each side with fields askp1..askp10 / askp_rsqn1..10.
    """
    depth = min(max(depth, 1), 10)
    bids: list[OrderbookLevel] = []
    asks: list[OrderbookLevel] = []

    for i in range(1, depth + 1):
        ask_p = _money_krw(getattr(output1, f"askp{i}", None))
        ask_q = _dec(getattr(output1, f"askp_rsqn{i}", None))
        if ask_p is not None and ask_q is not None and ask_q > 0 and ask_p.amount > 0:
            asks.append(OrderbookLevel(price=ask_p, qty=ask_q))

        bid_p = _money_krw(getattr(output1, f"bidp{i}", None))
        bid_q = _dec(getattr(output1, f"bidp_rsqn{i}", None))
        if bid_p is not None and bid_q is not None and bid_q > 0 and bid_p.amount > 0:
            bids.append(OrderbookLevel(price=bid_p, qty=bid_q))

    accept_t = getattr(output1, "aspr_acpt_hour", None)
    today = _kst_now().date().strftime("%Y%m%d")
    time = _parse_kst_datetime(today, accept_t) or _kst_now()

    return Orderbook(symbol=symbol, time=time, bids=bids, asks=asks, raw=raw)


def ohlcv_from_chartprice_item(symbol: Symbol, item: Any) -> OHLCV | None:
    """Convert one InquireDailyItemchartpriceResponse output2 row to OHLCV."""
    d = getattr(item, "stck_bsop_date", None)
    bday = _parse_kst_date(d) if d else None
    if bday is None:
        return None
    o = _money_krw(getattr(item, "stck_oprc", None))
    h = _money_krw(getattr(item, "stck_hgpr", None))
    l = _money_krw(getattr(item, "stck_lwpr", None))
    c = _money_krw(getattr(item, "stck_clpr", None))
    if not (o and h and l and c):
        return None
    vol = _dec(getattr(item, "acml_vol", None)) or Decimal(0)
    return OHLCV(
        symbol=symbol,
        time=datetime(bday.year, bday.month, bday.day, tzinfo=timezone.utc),
        open=o, high=h, low=l, close=c, volume=vol,
    )


def ohlcv_from_intraday_item(symbol: Symbol, item: Any) -> OHLCV | None:
    """Convert one InquireTimeItemchartpriceResponse output2 row to OHLCV.

    Intraday rows use stck_prpr (current) as the close of the minute bar and
    stck_cntg_hour (HHMMSS) for the minute timestamp.
    """
    d = getattr(item, "stck_bsop_date", None)
    t = getattr(item, "stck_cntg_hour", None)
    dt = _parse_kst_datetime(d, t) if d else None
    if dt is None:
        return None
    o = _money_krw(getattr(item, "stck_oprc", None))
    h = _money_krw(getattr(item, "stck_hgpr", None))
    l = _money_krw(getattr(item, "stck_lwpr", None))
    c = _money_krw(getattr(item, "stck_prpr", None))
    if not (o and h and l and c):
        return None
    vol = _dec(getattr(item, "cntg_vol", None)) or Decimal(0)
    return OHLCV(symbol=symbol, time=dt, open=o, high=h, low=l, close=c, volume=vol)


# ─── Account ─────────────────────────────────────────


def position_from_balance_row(item: Any) -> Position | None:
    """One row of inquire-balance output1 -> Position. Returns None for zero qty."""
    qty = _dec(getattr(item, "hldg_qty", None))
    if qty is None or qty == 0:
        return None
    ticker = getattr(item, "pdno", None)
    if not ticker:
        return None
    avg = _money_krw(getattr(item, "pchs_avg_pric", None))
    if avg is None:
        return None
    cur = _money_krw(getattr(item, "prpr", None))
    mv = _money_krw(getattr(item, "evlu_amt", None))
    pnl = _money_krw(getattr(item, "evlu_pfls_amt", None))
    pnl_rate = _dec(getattr(item, "evlu_pfls_rt", None))
    return Position(
        symbol=Symbol(ticker=ticker, exchange=Exchange.KRX),
        qty=qty, avg_price=avg, current_price=cur,
        market_value=mv, pnl=pnl, pnl_rate=pnl_rate,
    )


def balance_from_inquire(output1: list[Any], output2: list[Any], raw: dict[str, Any]) -> Balance:
    """Build Balance from inquire-balance output1 (positions) + output2 (summary)."""
    positions = [p for p in (position_from_balance_row(i) for i in output1) if p is not None]
    cash: list[Money] = []
    total: Money | None = None
    if output2:
        head = output2[0]
        deposit = _money_krw(getattr(head, "dnca_tot_amt", None))
        if deposit is not None:
            cash.append(deposit)
        total = _money_krw(getattr(head, "tot_evlu_amt", None))
    return Balance(total_asset=total, cash=cash, positions=positions, raw=raw)


# ─── Orders ──────────────────────────────────────────


_KIS_ORDER_STATUS: dict[str, OrderStatus] = {
    "01": OrderStatus.OPEN,
    "02": OrderStatus.PARTIALLY_FILLED,
    "03": OrderStatus.FILLED,
    "04": OrderStatus.CANCELLED,
}


def map_order_status(code: str | None, qty: Decimal, filled_qty: Decimal) -> OrderStatus:
    if code and code in _KIS_ORDER_STATUS:
        return _KIS_ORDER_STATUS[code]
    if filled_qty == 0:
        return OrderStatus.OPEN
    if filled_qty < qty:
        return OrderStatus.PARTIALLY_FILLED
    return OrderStatus.FILLED


def order_side_to_kis(side: OrderSide) -> str:
    """KIS uses ord_dvsn separately; side comes from the tr_id (buy vs sell)."""
    return "buy" if side is OrderSide.BUY else "sell"


_KIS_ORD_DVSN_BY_TYPE: dict[str, str] = {
    "limit": "00",       # 지정가
    "market": "01",      # 시장가
    "stop_limit": "00",  # stop-limit handled at order layer; KIS lacks native stop
}


def kis_ord_dvsn(order_type: str) -> str:
    return _KIS_ORD_DVSN_BY_TYPE[order_type]


def order_from_daily_ccld_row(item: Any, raw_row: dict[str, Any]) -> "Order | None":
    """Convert inquire-daily-ccld row to Order."""
    from datetime import time as _t

    from tooja.core.models import Order

    odno = getattr(item, "odno", None)
    ticker = getattr(item, "pdno", None)
    if not odno or not ticker:
        return None
    qty = _dec(getattr(item, "tot_ord_qty", None)) or Decimal(0)
    filled = _dec(getattr(item, "tot_ccld_qty", None)) or Decimal(0)
    side_code = getattr(item, "sll_buy_dvsn_cd", None)
    side = OrderSide.BUY if side_code == "02" else OrderSide.SELL
    avg = _money_krw(getattr(item, "avg_prvs", None))
    price = _money_krw(getattr(item, "ord_unpr", None))
    ord_dvsn = getattr(item, "ord_dvsn_cd", None) or getattr(item, "ord_dvsn", None)
    order_type = "market" if ord_dvsn == "01" else "limit"
    ord_dt = getattr(item, "ord_dt", None)
    ord_tmd = getattr(item, "ord_tmd", None)
    submitted = _parse_kst_datetime(ord_dt, ord_tmd) or _kst_now()
    ccld_status = getattr(item, "rmn_qty", None)
    status = map_order_status(None, qty, filled)
    return Order(
        order_id=odno,
        symbol=Symbol(ticker=ticker, exchange=Exchange.KRX),
        side=side, qty=qty, filled_qty=filled, avg_fill_price=avg,
        type=order_type, price=price,
        status=status, submitted_at=submitted, raw=raw_row,
    )


def stock_info_from_search(symbol: Symbol, output: Any, raw: dict[str, Any]) -> "StockInfo":
    from datetime import date as _d

    from tooja.core.models import StockInfo

    name = getattr(output, "prdt_abrv_name", None) or getattr(output, "prdt_name", None) or symbol.ticker
    cap_amt = _money_krw(getattr(output, "lstg_cptl_amt", None))
    par = _money_krw(getattr(output, "papr", None))
    shares = _dec(getattr(output, "lstg_stqt", None))

    listed_at: _d | None = None
    listing = getattr(output, "scts_mket_lstg_dt", None) or getattr(output, "kosdaq_mket_lstg_dt", None)
    if listing:
        listed_at = _parse_kst_date(listing)

    return StockInfo(
        symbol=symbol, name=name,
        listed_at=listed_at, listed_shares=shares,
        par_value=par, market_cap=cap_amt, raw=raw,
    )


def dividend_from_row(symbol: Symbol, item: Any, raw_row: dict[str, Any]) -> "Dividend | None":
    from datetime import date as _d

    from tooja.core.enums import Currency
    from tooja.core.models import Dividend
    from tooja.core.money import Money

    record_date = getattr(item, "record_date", None)
    ex: _d | None = _parse_kst_date(record_date) if record_date else None
    if ex is None:
        return None
    pay_s = getattr(item, "divi_pay_dt", None)
    pay = _parse_kst_date(pay_s) if pay_s else None
    amt = _dec(getattr(item, "per_sto_divi_amt", None))
    if amt is None:
        return None
    return Dividend(
        symbol=symbol, ex_date=ex, pay_date=pay,
        amount_per_share=Money(amount=amt, currency=Currency.KRW),
        raw=raw_row,
    )


def ranking_entry_from_volume_row(item: Any, raw_row: dict[str, Any]) -> "RankingEntry | None":
    from tooja.core.models import RankingEntry

    rank = _int(getattr(item, "data_rank", None))
    ticker = getattr(item, "mksc_shrn_iscd", None)
    if rank is None or not ticker:
        return None
    name = getattr(item, "hts_kor_isnm", None) or ticker
    value = _dec(getattr(item, "acml_vol", None)) or Decimal(0)
    price = _money_krw(getattr(item, "stck_prpr", None))
    change_rate = _dec(getattr(item, "prdy_ctrt", None))
    return RankingEntry(
        rank=rank,
        symbol=Symbol(ticker=ticker, exchange=Exchange.KRX),
        name=name, value=value, price=price, change_rate=change_rate,
        raw=raw_row,
    )


def ranking_entry_from_market_cap_row(item: Any, raw_row: dict[str, Any]) -> "RankingEntry | None":
    from tooja.core.models import RankingEntry

    rank = _int(getattr(item, "data_rank", None))
    ticker = getattr(item, "mksc_shrn_iscd", None)
    if rank is None or not ticker:
        return None
    name = getattr(item, "hts_kor_isnm", None) or ticker
    cap = _dec(getattr(item, "stck_avls", None)) or _dec(getattr(item, "hts_avls", None)) or Decimal(0)
    price = _money_krw(getattr(item, "stck_prpr", None))
    change_rate = _dec(getattr(item, "prdy_ctrt", None))
    return RankingEntry(
        rank=rank,
        symbol=Symbol(ticker=ticker, exchange=Exchange.KRX),
        name=name, value=cap, price=price, change_rate=change_rate,
        raw=raw_row,
    )


def investor_flow_from_row(symbol: Symbol, item: Any, raw_row: dict[str, Any]) -> "InvestorFlow | None":
    from tooja.core.enums import Currency
    from tooja.core.models import InvestorFlow
    from tooja.core.money import Money

    d_s = getattr(item, "stck_bsop_date", None)
    d = _parse_kst_date(d_s) if d_s else None
    if d is None:
        return None
    indiv = _dec(getattr(item, "prsn_ntby_tr_pbmn", None))
    foreign = _dec(getattr(item, "frgn_ntby_tr_pbmn", None))
    inst = _dec(getattr(item, "orgn_ntby_tr_pbmn", None))
    if indiv is None or foreign is None or inst is None:
        return None
    return InvestorFlow(
        symbol=symbol, date=d,
        individual_net=Money(amount=indiv, currency=Currency.KRW),
        foreign_net=Money(amount=foreign, currency=Currency.KRW),
        institutional_net=Money(amount=inst, currency=Currency.KRW),
        raw=raw_row,
    )


_WS_QUOTE_COLUMNS = (
    "MKSC_SHRN_ISCD", "STCK_CNTG_HOUR", "STCK_PRPR", "PRDY_VRSS_SIGN",
    "PRDY_VRSS", "PRDY_CTRT", "WGHN_AVRG_STCK_PRC", "STCK_OPRC",
    "STCK_HGPR", "STCK_LWPR", "ASKP1", "BIDP1", "CNTG_VOL", "ACML_VOL",
    "ACML_TR_PBMN",
)


def quote_from_ws_record(record: dict[str, str]) -> "Quote | None":
    """Build a Quote from an H0STCNT0 record (pipe-decoded raw fields)."""
    from tooja.core.models import Quote

    ticker = record.get("MKSC_SHRN_ISCD")
    if not ticker:
        return None
    price = _money_krw(record.get("STCK_PRPR"))
    if price is None:
        return None
    change = _money_krw(record.get("PRDY_VRSS"))
    sign = record.get("PRDY_VRSS_SIGN")
    if change is not None and sign in ("4", "5") and change.amount > 0:
        change = -change
    today = _kst_now().date().strftime("%Y%m%d")
    when = _parse_kst_datetime(today, record.get("STCK_CNTG_HOUR")) or _kst_now()
    return Quote(
        symbol=Symbol(ticker=ticker, exchange=Exchange.KRX),
        price=price, time=when, change=change,
        change_rate=_dec(record.get("PRDY_CTRT")),
        open=_money_krw(record.get("STCK_OPRC")),
        high=_money_krw(record.get("STCK_HGPR")),
        low=_money_krw(record.get("STCK_LWPR")),
        volume=_dec(record.get("ACML_VOL")),
        raw=record,
    )


def trade_from_ws_record(record: dict[str, str]) -> "Trade | None":
    from tooja.core.models import Trade

    ticker = record.get("MKSC_SHRN_ISCD")
    price = _money_krw(record.get("STCK_PRPR"))
    qty = _dec(record.get("CNTG_VOL"))
    if not ticker or price is None or qty is None:
        return None
    today = _kst_now().date().strftime("%Y%m%d")
    when = _parse_kst_datetime(today, record.get("STCK_CNTG_HOUR")) or _kst_now()
    side_code = record.get("CCLD_DVSN")
    side: OrderSide | None = (
        OrderSide.BUY if side_code == "1" else OrderSide.SELL if side_code == "5" else None
    )
    return Trade(
        symbol=Symbol(ticker=ticker, exchange=Exchange.KRX),
        time=when, price=price, qty=qty, side=side, raw=record,
    )


def orderbook_from_ws_record(record: dict[str, str], *, depth: int = 10) -> "Orderbook | None":
    """Map H0STASP0 record to Orderbook."""
    from tooja.core.models import Orderbook

    ticker = record.get("MKSC_SHRN_ISCD")
    if not ticker:
        return None
    bids: list[OrderbookLevel] = []
    asks: list[OrderbookLevel] = []
    for i in range(1, depth + 1):
        ap = _money_krw(record.get(f"ASKP{i}"))
        aq = _dec(record.get(f"ASKP_RSQN{i}"))
        if ap is not None and aq is not None and aq > 0 and ap.amount > 0:
            asks.append(OrderbookLevel(price=ap, qty=aq))
        bp = _money_krw(record.get(f"BIDP{i}"))
        bq = _dec(record.get(f"BIDP_RSQN{i}"))
        if bp is not None and bq is not None and bq > 0 and bp.amount > 0:
            bids.append(OrderbookLevel(price=bp, qty=bq))
    today = _kst_now().date().strftime("%Y%m%d")
    when = _parse_kst_datetime(today, record.get("BSOP_HOUR")) or _kst_now()
    return Orderbook(
        symbol=Symbol(ticker=ticker, exchange=Exchange.KRX),
        time=when, bids=bids, asks=asks, raw=record,
    )


def fill_from_daily_ccld_row(item: Any, raw_row: dict[str, Any]) -> "Fill | None":
    from tooja.core.models import Fill

    odno = getattr(item, "odno", None)
    ticker = getattr(item, "pdno", None)
    qty = _dec(getattr(item, "tot_ccld_qty", None))
    avg = _money_krw(getattr(item, "avg_prvs", None))
    if not odno or not ticker or qty is None or qty == 0 or avg is None:
        return None
    side_code = getattr(item, "sll_buy_dvsn_cd", None)
    side = OrderSide.BUY if side_code == "02" else OrderSide.SELL
    ord_dt = getattr(item, "ord_dt", None)
    ord_tmd = getattr(item, "ord_tmd", None)
    when = _parse_kst_datetime(ord_dt, ord_tmd) or _kst_now()
    return Fill(
        order_id=odno,
        symbol=Symbol(ticker=ticker, exchange=Exchange.KRX),
        side=side, qty=qty, price=avg, time=when, raw=raw_row,
    )
