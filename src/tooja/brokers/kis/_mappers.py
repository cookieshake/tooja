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
    if isinstance(v, float):
        # Decimal(0.1) leaks binary float artifacts (0.1000000000…0555…).
        # Route floats through str so Decimal sees the rendered value.
        v = str(v)
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


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _kst_today() -> date:
    """Today's date in KST. Diverges from system-local date() across the
    UTC midnight ~ 09:00 KST window if the host is in UTC."""
    from datetime import timedelta
    return (datetime.now(timezone.utc) + timedelta(hours=KST_OFFSET_HOURS)).date()


def kst_today() -> date:
    """Public helper for adapters that need to anchor today to KST."""
    return _kst_today()


def kst_today_yyyymmdd() -> str:
    return _kst_today().strftime("%Y%m%d")


def _parse_kst_date(s: str) -> date | None:
    """KIS daily price uses YYYYMMDD."""
    if not s or len(s) != 8:
        return None
    try:
        return date(int(s[:4]), int(s[4:6]), int(s[6:8]))
    except ValueError:
        return None


def _parse_kst_datetime(d: str, t: str | None = None) -> datetime | None:
    """KIS uses YYYYMMDD + HHMMSS, KST. Return tz-aware UTC.

    Returns None when `t` is missing so callers' `... or _utc_now()` fallbacks
    take effect — defaulting to midnight KST would silently rewind timestamps
    by 9 hours.
    """
    if not d or len(d) < 8 or not t:
        return None
    try:
        year, month, day = int(d[:4]), int(d[4:6]), int(d[6:8])
        tp = t.zfill(6)
        hour, minute, sec = int(tp[:2]), int(tp[2:4]), int(tp[4:6])
        from datetime import timedelta
        kst = datetime(year, month, day, hour, minute, sec)
        return (kst - timedelta(hours=KST_OFFSET_HOURS)).replace(tzinfo=timezone.utc)
    except ValueError:
        return None


# ─── Market ──────────────────────────────────────────


_EXCD_BY_EXCHANGE = {
    Exchange.NASD: "NAS",
    Exchange.NYSE: "NYS",
    Exchange.AMEX: "AMS",
    Exchange.SEHK: "HKS",
    Exchange.TKSE: "TSE",
    Exchange.SHAA: "SHS",
    Exchange.SZAA: "SZS",
    Exchange.HASE: "HNX",
    Exchange.VNSE: "HSX",
}

_CURRENCY_BY_EXCHANGE = {
    Exchange.NASD: Currency.USD,
    Exchange.NYSE: Currency.USD,
    Exchange.AMEX: Currency.USD,
    Exchange.SEHK: Currency.HKD,
    Exchange.TKSE: Currency.JPY,
    Exchange.SHAA: Currency.CNY,
    Exchange.SZAA: Currency.CNY,
    Exchange.HASE: Currency.VND,
    Exchange.VNSE: Currency.VND,
}


def excd_for(exchange: Exchange) -> str | None:
    """Return KIS overseas EXCD code, or None for domestic."""
    return _EXCD_BY_EXCHANGE.get(exchange)


def _money_in(currency: Currency, v: Any) -> Money | None:
    d = _dec(v)
    if d is None:
        return None
    return Money(amount=d, currency=currency)


def quote_from_overseas_price(symbol: Symbol, output: Any, raw: dict[str, Any]) -> Quote:
    """Convert overseas price endpoint output to Quote."""
    currency = _CURRENCY_BY_EXCHANGE.get(symbol.exchange, Currency.USD)
    price = _money_in(currency, getattr(output, "last", None))
    if price is None:
        raise ValueError(f"KIS overseas price returned no last for {symbol}")
    diff = _money_in(currency, getattr(output, "diff", None))
    sign = getattr(output, "sign", None)
    if diff is not None and sign in ("4", "5") and diff.amount > 0:
        diff = -diff
    return Quote(
        symbol=symbol, price=price, time=_utc_now(),
        change=diff,
        change_rate=_dec(getattr(output, "rate", None)),
        prev_close=_money_in(currency, getattr(output, "base", None)),
        volume=_dec(getattr(output, "tvol", None)),
        raw=raw,
    )


def ohlcv_from_overseas_daily_item(symbol: Symbol, item: Any) -> "OHLCV | None":
    currency = _CURRENCY_BY_EXCHANGE.get(symbol.exchange, Currency.USD)
    d_s = getattr(item, "xymd", None)
    d = _parse_kst_date(d_s) if d_s else None
    if d is None:
        return None
    o = _money_in(currency, getattr(item, "open", None))
    h = _money_in(currency, getattr(item, "high", None))
    l = _money_in(currency, getattr(item, "low", None))
    c = _money_in(currency, getattr(item, "clos", None))
    if not (o and h and l and c):
        return None
    vol = _dec(getattr(item, "tvol", None)) or Decimal(0)
    return OHLCV(
        symbol=symbol,
        time=datetime(d.year, d.month, d.day, tzinfo=timezone.utc),
        open=o, high=h, low=l, close=c, volume=vol,
    )


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
        time=_utc_now(),
        change=change,
        change_rate=_dec(getattr(output, "prdy_ctrt", None)),
        open=_money_krw(getattr(output, "stck_oprc", None)),
        high=_money_krw(getattr(output, "stck_hgpr", None)),
        low=_money_krw(getattr(output, "stck_lwpr", None)),
        prev_close=_money_krw(getattr(output, "stck_sdpr", None)),
        volume=_dec(getattr(output, "acml_vol", None)),
        raw=raw,
    )


def price_limit_from_inquire_price(symbol: Symbol, output: Any, raw: dict[str, Any]) -> "PriceLimit":
    """InquirePrice output -> PriceLimit (KRW upper/lower band)."""
    from tooja.core.models import PriceLimit

    return PriceLimit(
        symbol=symbol,
        upper_limit=_money_krw(getattr(output, "stck_mxpr", None)),
        lower_limit=_money_krw(getattr(output, "stck_llam", None)),
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
    today = kst_today_yyyymmdd()
    time = _parse_kst_datetime(today, accept_t) or _utc_now()

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


def map_order_status(
    code: str | None,
    qty: Decimal,
    filled_qty: Decimal,
    remaining_qty: Decimal | None = None,
) -> OrderStatus:
    if code and code in _KIS_ORDER_STATUS:
        return _KIS_ORDER_STATUS[code]
    # KIS inquire-daily-ccld has no explicit status field — infer from the
    # filled/remaining split. When nothing remains but the order isn't fully
    # filled, the unfilled balance was cancelled (covers both a wholly
    # cancelled order, filled==0, and a partially-filled-then-cancelled one,
    # 0<filled<qty). Without remaining_qty we can't distinguish cancelled from
    # open, so fall back to the filled/qty inference.
    if remaining_qty is not None and remaining_qty == 0 and filled_qty < qty:
        return OrderStatus.CANCELLED
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
    submitted = _parse_kst_datetime(ord_dt, ord_tmd) or _utc_now()
    remaining = _dec(getattr(item, "rmn_qty", None))
    status = map_order_status(None, qty, filled, remaining)
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


def _ranking_common(item: Any, value_field: str) -> tuple[int, str, str, Decimal, Any, Any] | None:
    rank = _int(getattr(item, "data_rank", None))
    ticker = getattr(item, "mksc_shrn_iscd", None)
    if rank is None or not ticker:
        return None
    name = getattr(item, "hts_kor_isnm", None) or ticker
    value = _dec(getattr(item, value_field, None)) or Decimal(0)
    price = _money_krw(getattr(item, "stck_prpr", None))
    change_rate = _dec(getattr(item, "prdy_ctrt", None))
    return rank, ticker, name, value, price, change_rate


def _build_ranking(item: Any, raw_row: dict[str, Any], value_field: str) -> "RankingEntry | None":
    from tooja.core.models import RankingEntry

    parts = _ranking_common(item, value_field)
    if parts is None:
        return None
    rank, ticker, name, value, price, change_rate = parts
    return RankingEntry(
        rank=rank,
        symbol=Symbol(ticker=ticker, exchange=Exchange.KRX),
        name=name, value=value, price=price, change_rate=change_rate,
        raw=raw_row,
    )


def ranking_entry_from_volume_row(item: Any, raw_row: dict[str, Any]) -> "RankingEntry | None":
    return _build_ranking(item, raw_row, "acml_vol")


def ranking_entry_from_turnover_row(item: Any, raw_row: dict[str, Any]) -> "RankingEntry | None":
    return _build_ranking(item, raw_row, "acml_tr_pbmn")


def ranking_entry_from_short_row(item: Any, raw_row: dict[str, Any]) -> "RankingEntry | None":
    # short-sale endpoint uses ssts_cntg_qty (volume) and ssts_tr_pbmn (value).
    from tooja.core.models import RankingEntry

    ticker = getattr(item, "mksc_shrn_iscd", None)
    if not ticker:
        return None
    rank = _int(getattr(item, "data_rank", None)) or 0
    name = getattr(item, "hts_kor_isnm", None) or ticker
    qty = _dec(getattr(item, "ssts_cntg_qty", None)) or Decimal(0)
    price = _money_krw(getattr(item, "stck_prpr", None))
    change_rate = _dec(getattr(item, "prdy_ctrt", None))
    return RankingEntry(
        rank=rank,
        symbol=Symbol(ticker=ticker, exchange=Exchange.KRX),
        name=name, value=qty, price=price, change_rate=change_rate,
        raw=raw_row,
    )


def ranking_entry_from_quote_balance_row(item: Any, raw_row: dict[str, Any]) -> "RankingEntry | None":
    # quote-balance: total_askp_rsqn / total_bidp_rsqn.
    from tooja.core.models import RankingEntry

    ticker = getattr(item, "mksc_shrn_iscd", None)
    if not ticker:
        return None
    rank = _int(getattr(item, "data_rank", None)) or 0
    name = getattr(item, "hts_kor_isnm", None) or ticker
    bid_qty = _dec(getattr(item, "total_bidp_rsqn", None)) or Decimal(0)
    ask_qty = _dec(getattr(item, "total_askp_rsqn", None)) or Decimal(0)
    price = _money_krw(getattr(item, "stck_prpr", None))
    return RankingEntry(
        rank=rank,
        symbol=Symbol(ticker=ticker, exchange=Exchange.KRX),
        name=name, value=bid_qty,  # caller picks side via kwarg below
        price=price, change_rate=None,
        raw={**raw_row, "_bid_qty": str(bid_qty), "_ask_qty": str(ask_qty)},
    )


def ranking_entry_from_highlow_row(item: Any, raw_row: dict[str, Any]) -> "RankingEntry | None":
    # near-new-highlow: no acml_vol explicit; value is rank position; use prpr as proxy via change_rate.
    from tooja.core.models import RankingEntry

    ticker = getattr(item, "mksc_shrn_iscd", None)
    if not ticker:
        return None
    rank = _int(getattr(item, "data_rank", None)) or 0
    name = getattr(item, "hts_kor_isnm", None) or ticker
    price = _money_krw(getattr(item, "stck_prpr", None))
    change_rate = _dec(getattr(item, "prdy_ctrt", None))
    value = _dec(getattr(item, "stck_prpr", None)) or Decimal(0)
    return RankingEntry(
        rank=rank,
        symbol=Symbol(ticker=ticker, exchange=Exchange.KRX),
        name=name, value=value, price=price, change_rate=change_rate,
        raw=raw_row,
    )


def ranking_entry_from_credit_balance_row(item: Any, raw_row: dict[str, Any]) -> "RankingEntry | None":
    # credit-balance: margin balance ranking. Use 'crdt_loan_rmnd' if exists, else 'whol_loan_rmnd'.
    from tooja.core.models import RankingEntry

    ticker = getattr(item, "mksc_shrn_iscd", None)
    if not ticker:
        return None
    rank = _int(getattr(item, "data_rank", None)) or 0
    name = getattr(item, "hts_kor_isnm", None) or ticker
    value = _dec(getattr(item, "crdt_loan_rmnd", None)) or \
            _dec(getattr(item, "whol_loan_rmnd", None)) or \
            _dec(getattr(item, "acml_vol", None)) or Decimal(0)
    price = _money_krw(getattr(item, "stck_prpr", None))
    return RankingEntry(
        rank=rank,
        symbol=Symbol(ticker=ticker, exchange=Exchange.KRX),
        name=name, value=value, price=price,
        change_rate=_dec(getattr(item, "prdy_ctrt", None)),
        raw=raw_row,
    )


def ranking_entry_from_investor_total_row(item: Any, raw_row: dict[str, Any], *, value_field: str) -> "RankingEntry | None":
    """foreign-institution-total: net-buy ranking. value_field picks which actor."""
    from tooja.core.models import RankingEntry

    ticker = getattr(item, "mksc_shrn_iscd", None)
    if not ticker:
        return None
    rank = _int(getattr(item, "data_rank", None)) or 0
    name = getattr(item, "hts_kor_isnm", None) or ticker
    value = _dec(getattr(item, value_field, None)) or Decimal(0)
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


def financial_summary_from_ratio_row(
    symbol: Symbol, item: Any, raw_row: dict[str, Any], *, period: "FinancialPeriod",
) -> "FinancialSummary | None":
    from datetime import date as _d

    from tooja.core.enums import Currency
    from tooja.core.models import FinancialSummary
    from tooja.core.money import Money

    stac = getattr(item, "stac_yymm", None)
    if not stac or len(stac) < 6:
        return None
    try:
        fiscal = _d(int(stac[:4]), int(stac[4:6]), 1)
    except ValueError:
        return None
    eps = _dec(getattr(item, "eps", None))
    bps = _dec(getattr(item, "bps", None))
    roe = _dec(getattr(item, "roe_val", None))
    return FinancialSummary(
        symbol=symbol, period=period, fiscal_date=fiscal,
        eps=Money(amount=eps, currency=Currency.KRW) if eps is not None else None,
        bps=Money(amount=bps, currency=Currency.KRW) if bps is not None else None,
        roe=roe, raw=raw_row,
    )


def trading_halt_from_vi_row(item: Any, raw_row: dict[str, Any]) -> "TradingHalt | None":
    """VI (volatility-interruption) halts from inquire-vi-status."""
    from tooja.core.models import TradingHalt

    ticker = getattr(item, "mksc_shrn_iscd", None)
    if not ticker:
        return None
    if getattr(item, "vi_cls_code", None) != "Y":
        return None
    d_s = getattr(item, "bsop_date", None)
    t_s = getattr(item, "cntg_vi_hour", None)
    start = _parse_kst_datetime(d_s, t_s) if d_s else None
    if start is None:
        return None
    cancel_t = getattr(item, "vi_cncl_hour", None)
    end = _parse_kst_datetime(d_s, cancel_t) if (d_s and cancel_t and cancel_t != "000000") else None
    return TradingHalt(
        symbol=Symbol(ticker=ticker, exchange=Exchange.KRX),
        start=start, end=end, reason="VI", raw=raw_row,
    )


def program_trading_from_row(symbol: Symbol, item: Any, raw_row: dict[str, Any]) -> "ProgramTrading | None":
    from tooja.core.enums import Currency
    from tooja.core.models import ProgramTrading
    from tooja.core.money import Money

    d_s = getattr(item, "stck_bsop_date", None)
    d = _parse_kst_date(d_s) if d_s else None
    if d is None:
        return None
    # KIS exposes total program net only; arbitrage/non-arbitrage breakdown is
    # not in this endpoint — assign whole to non_arbitrage, zero arbitrage.
    total = _dec(getattr(item, "whol_smtn_ntby_tr_pbmn", None))
    if total is None:
        return None
    return ProgramTrading(
        symbol=symbol, date=d,
        arbitrage_net=Money(amount=Decimal(0), currency=Currency.KRW),
        non_arbitrage_net=Money(amount=total, currency=Currency.KRW),
        raw=raw_row,
    )


def short_selling_from_row(symbol: Symbol, item: Any, raw_row: dict[str, Any]) -> "ShortSellingDaily | None":
    from tooja.core.enums import Currency
    from tooja.core.models import ShortSellingDaily
    from tooja.core.money import Money

    d_s = getattr(item, "stck_bsop_date", None)
    d = _parse_kst_date(d_s) if d_s else None
    if d is None:
        return None
    vol = _dec(getattr(item, "ssts_cntg_qty", None)) or Decimal(0)
    ratio = _dec(getattr(item, "ssts_vol_rlim", None))
    # KIS daily-short-sale endpoint exposes qty + ratio but not value in KRW.
    # Use 0 KRW as placeholder; consumers needing the value should hit raw.
    value = Money(amount=Decimal(0), currency=Currency.KRW)
    return ShortSellingDaily(
        symbol=symbol, date=d,
        short_volume=vol, short_value=value, short_ratio=ratio,
        raw=raw_row,
    )


def margin_balance_from_row(symbol: Symbol, item: Any, raw_row: dict[str, Any]) -> "MarginBalance | None":
    from tooja.core.enums import Currency
    from tooja.core.models import MarginBalance
    from tooja.core.money import Money

    d_s = getattr(item, "deal_date", None) or getattr(item, "stlm_date", None)
    d = _parse_kst_date(d_s) if d_s else None
    if d is None:
        return None
    loan_amt = _dec(getattr(item, "whol_loan_rmnd_amt", None))  # 만원
    if loan_amt is None:
        return None
    # KIS unit is 만원 (10,000 KRW) — convert.
    loan_krw = loan_amt * Decimal(10000)
    stln_amt = _dec(getattr(item, "whol_stln_rmnd_amt", None))
    stock_loan = (
        Money(amount=stln_amt * Decimal(10000), currency=Currency.KRW)
        if stln_amt is not None else None
    )
    return MarginBalance(
        symbol=symbol, date=d,
        margin_loan=Money(amount=loan_krw, currency=Currency.KRW),
        stock_loan=stock_loan,
        raw=raw_row,
    )


def securities_lending_from_row(symbol: Symbol, item: Any, raw_row: dict[str, Any]) -> "SecuritiesLending | None":
    from tooja.core.enums import Currency
    from tooja.core.models import SecuritiesLending
    from tooja.core.money import Money

    d_s = getattr(item, "bsop_date", None)
    d = _parse_kst_date(d_s) if d_s else None
    if d is None:
        return None
    balance_amt = _dec(getattr(item, "rmnd_amt", None))
    if balance_amt is None:
        return None
    new_amt = _dec(getattr(item, "new_stcn", None))  # 주수 — not amount; placeholder
    return SecuritiesLending(
        symbol=symbol, date=d,
        balance=Money(amount=balance_amt, currency=Currency.KRW),
        new_loan=(
            Money(amount=new_amt, currency=Currency.KRW) if new_amt is not None else None
        ),
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


# Pulled from the raw subscriber's COLUMNS. KIS H0STCNT0 has 46 fields per
# record; defining only a prefix here silently misaligns CCLD_DVSN (trade
# side) and corrupts every record after the first in multi-record packets.
from tooja.brokers.kis.raw.domestic_stock_ws.h0stcnt0 import (
    H0stcnt0Subscriber as _H0stcnt0Subscriber,
)

_WS_QUOTE_COLUMNS = _H0stcnt0Subscriber.COLUMNS


# Sourced from the raw H0STCNI0 subscriber's COLUMNS — full field order matters
# because the WS frame splits records by index. Adding/removing fields silently
# shifts every later field by one position.
_WS_ORDER_COLUMNS = (
    "CUST_ID", "ACNT_NO", "ODER_NO", "OODER_NO", "SELN_BYOV_CLS",
    "RCTF_CLS", "ODER_KIND", "ODER_COND", "STCK_SHRN_ISCD",
    "CNTG_QTY", "CNTG_UNPR", "STCK_CNTG_HOUR", "RFUS_YN",
    "CNTG_YN", "ACPT_YN", "BRNC_NO", "ODER_QTY",
    "ACNT_NAME", "ORD_COND_PRC", "ORD_EXG_GB", "POPUP_YN",
    "FILLER", "CRDT_CLS", "CRDT_LOAN_DATE", "CNTG_ISNM40", "ODER_PRC",
)


def order_update_from_ws_record(record: dict[str, str]) -> "OrderUpdate | None":
    """Build OrderUpdate from an H0STCNI0 record."""
    from tooja.core.models import OrderUpdate

    odno = record.get("ODER_NO")
    ticker = record.get("STCK_SHRN_ISCD")
    if not odno or not ticker:
        return None
    qty_total = _dec(record.get("ODER_QTY")) or Decimal(0)
    filled = _dec(record.get("CNTG_QTY")) or Decimal(0)
    rfus = record.get("RFUS_YN")
    cntg_yn = record.get("CNTG_YN")
    if rfus == "1":
        status = OrderStatus.REJECTED
    elif cntg_yn == "2":
        status = map_order_status(None, qty_total, filled)
    else:
        status = OrderStatus.OPEN
    price = _money_krw(record.get("CNTG_UNPR"))
    today = kst_today_yyyymmdd()
    when = _parse_kst_datetime(today, record.get("STCK_CNTG_HOUR")) or _utc_now()
    return OrderUpdate(
        order_id=odno,
        symbol=Symbol(ticker=ticker, exchange=Exchange.KRX),
        status=status,
        filled_qty=filled,
        avg_fill_price=price,
        time=when,
        raw=record,
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
    today = kst_today_yyyymmdd()
    when = _parse_kst_datetime(today, record.get("STCK_CNTG_HOUR")) or _utc_now()
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
    today = kst_today_yyyymmdd()
    when = _parse_kst_datetime(today, record.get("STCK_CNTG_HOUR")) or _utc_now()
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
    today = kst_today_yyyymmdd()
    when = _parse_kst_datetime(today, record.get("BSOP_HOUR")) or _utc_now()
    return Orderbook(
        symbol=Symbol(ticker=ticker, exchange=Exchange.KRX),
        time=when, bids=bids, asks=asks, raw=record,
    )


def stock_warnings_from_search(symbol: Symbol, output: Any, raw: dict[str, Any]) -> "StockWarnings":
    """search-stock-info -> StockWarnings. KIS exposes only trading-halt and
    administrative-issue flags here; finer caution levels stay None."""
    from tooja.core.models import StockWarnings

    def _yn(v: Any) -> bool | None:
        if v is None:
            return None
        return str(v).strip().upper() == "Y"

    return StockWarnings(
        symbol=symbol,
        is_trading_halt=_yn(getattr(output, "tr_stop_yn", None)),
        is_administrative=_yn(getattr(output, "admn_item_yn", None)),
        raw=raw,
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
    when = _parse_kst_datetime(ord_dt, ord_tmd) or _utc_now()
    return Fill(
        order_id=odno,
        symbol=Symbol(ticker=ticker, exchange=Exchange.KRX),
        side=side, qty=qty, price=avg, time=when, raw=raw_row,
    )


# ─── Overseas present-balance ────────────────────────────────────────────────


def _money_ccy(amount: Any, currency_code: str | None) -> Money | None:
    """Foreign-currency Money from a KIS string amount + currency code."""
    amt = _dec(amount)
    if amt is None or not currency_code:
        return None
    try:
        ccy = Currency(currency_code)
    except ValueError:
        return None
    return Money(amount=amt, currency=ccy)


def position_from_present_balance_row(item: Any) -> Position | None:
    """One overseas present-balance output1 row -> Position (foreign currency)."""
    qty = _dec(getattr(item, "cblc_qty13", None))
    if qty is None or qty == 0:
        return None
    ticker = getattr(item, "pdno", None)
    excg = getattr(item, "ovrs_excg_cd", None)
    ccy = getattr(item, "buy_crcy_cd", None)
    if not ticker or not excg:
        return None
    try:
        exchange = Exchange(excg)
    except ValueError:
        return None  # unmapped exchange code -> skip this position
    avg = _money_ccy(getattr(item, "avg_unpr3", None), ccy)
    if avg is None:
        return None
    return Position(
        symbol=Symbol(ticker=ticker, exchange=exchange),
        qty=qty,
        avg_price=avg,
        current_price=_money_ccy(getattr(item, "ovrs_now_pric1", None), ccy),
        market_value=_money_ccy(getattr(item, "frcr_evlu_amt2", None), ccy),
        pnl=_money_ccy(getattr(item, "evlu_pfls_amt2", None), ccy),
        pnl_rate=_dec(getattr(item, "evlu_pfls_rt1", None)),
    )


def balance_from_present_balance(resp: Any) -> Balance:
    """Overseas inquire-present-balance -> Balance (foreign cash + positions).

    output2 -> per-currency cash (crcy_cd + frcr_dncl_amt_2).
    output1 -> positions (foreign currency, ovrs_excg_cd -> Exchange).
    output3.tot_asst_amt -> overseas total, KRW-converted.
    """
    cash: list[Money] = []
    for row in getattr(resp, "output2", None) or []:
        # A zero foreign deposit is a meaningful state (a held currency with no
        # spendable cash), so zero-amount rows are kept — unlike zero-qty
        # positions, which are dropped.
        m = _money_ccy(getattr(row, "frcr_dncl_amt_2", None), getattr(row, "crcy_cd", None))
        if m is not None:
            cash.append(m)
    positions = [
        p
        for p in (position_from_present_balance_row(r) for r in (getattr(resp, "output1", None) or []))
        if p is not None
    ]
    total: Money | None = None
    out3 = getattr(resp, "output3", None)
    if out3 is not None:
        total = _money_krw(getattr(out3, "tot_asst_amt", None))
    raw = resp.model_dump(by_alias=True) if hasattr(resp, "model_dump") else {}
    return Balance(
        total_asset=total, cash=cash, positions=positions, raw=raw,
    )


def merge_balances(domestic: Balance, overseas: Balance) -> Balance:
    """Merge two single-call Balances into one.

    Cash is summed per currency, positions are concatenated, and total_asset
    is summed (both are expected to be KRW-base).
    """
    by_ccy: dict = {}
    for m in list(domestic.cash) + list(overseas.cash):
        by_ccy[m.currency] = by_ccy.get(m.currency, Decimal(0)) + m.amount
    cash = [Money(amount=a, currency=c) for c, a in by_ccy.items()]
    totals = [b.total_asset for b in (domestic, overseas) if b.total_asset is not None]
    total: Money | None = None
    if totals:
        # KIS reports both domestic tot_evlu_amt and overseas tot_asst_amt in KRW,
        # so summing amounts and taking the first currency is sound. Guard loudly
        # if a non-KRW total ever slips in — summing across currencies would
        # silently produce a wrong number; it would need an FX step instead.
        currencies = {t.currency for t in totals}
        if len(currencies) > 1:
            raise ValueError(
                f"cannot merge total_asset across currencies "
                f"{sorted(c.value for c in currencies)} — both are expected in KRW base"
            )
        total = Money(
            amount=sum((t.amount for t in totals), Decimal(0)),
            currency=totals[0].currency,
        )
    return Balance(
        total_asset=total,
        cash=cash,
        positions=list(domestic.positions) + list(overseas.positions),
        raw={"domestic": domestic.raw, "overseas": overseas.raw},
    )
