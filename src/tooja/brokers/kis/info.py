"""KIS Info subclient.

Mapped:
- get_stock / get_dividends / get_financials / is_holiday / list_halts

Not mapped (KIS has no equivalent endpoint):
- search (no name-based search endpoint)
- list_by_industry (industry endpoints return prices, not instrument lists)
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING

from tooja.brokers.kis._call import call
from tooja.brokers.kis._mappers import (
    dividend_from_row,
    financial_summary_from_ratio_row,
    kst_today,
    stock_info_from_search,
    trading_halt_from_vi_row,
)
from tooja.brokers.kis.raw.domestic_stock_industry.chk_holiday import (
    ChkHolidayExecutor,
    ChkHolidayRequest,
)
from tooja.brokers.kis.raw.domestic_stock_industry.inquire_vi_status import (
    InquireViStatusExecutor,
    InquireViStatusRequest,
)
from tooja.brokers.kis.raw.domestic_stock_info.dividend import (
    DividendExecutor,
    DividendRequest,
)
from tooja.brokers.kis.raw.domestic_stock_info.financial_ratio import (
    FinancialRatioExecutor,
    FinancialRatioRequest,
)
from tooja.brokers.kis.raw.domestic_stock_info.search_stock_info import (
    SearchStockInfoExecutor,
    SearchStockInfoRequest,
)
from tooja.core.clients import InfoClient
from tooja.core.enums import Exchange, FinancialPeriod
from tooja.core.errors import SymbolNotFound, UnsupportedOperation
from tooja.core.models import (
    Dividend,
    FinancialSummary,
    StockInfo,
    Symbol,
    TradingHalt,
)

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker


def _as_symbol(s: Symbol | str) -> Symbol:
    sym = s if isinstance(s, Symbol) else Symbol.parse(s)
    if sym.exchange not in (Exchange.KRX, Exchange.NXT):
        raise UnsupportedOperation(
            f"KIS info supports domestic KRX/NXT symbols only (got {sym.exchange})",
            broker="kis",
        )
    return sym


def _yyyymmdd(d: date) -> str:
    return d.strftime("%Y%m%d")


class KisInfoClient(InfoClient):
    _broker_name = "kis"

    def __init__(self, broker: "KisBroker"):
        self._broker = broker

    async def get_stock(self, symbol: Symbol | str) -> StockInfo:
        sym = _as_symbol(symbol)
        req = SearchStockInfoRequest(PRDT_TYPE_CD="300", PDNO=sym.ticker)
        resp = await call(self._broker, SearchStockInfoExecutor, req)
        out = getattr(resp, "output", None)
        if out is None:
            raise SymbolNotFound(
                f"KIS search-stock-info returned no result for {sym}",
                broker="kis",
            )
        return stock_info_from_search(sym, out, out.model_dump())

    async def get_dividends(
        self, symbol: Symbol | str, *, since: date | None = None,
    ) -> list[Dividend]:
        sym = _as_symbol(symbol)
        today = kst_today()
        start = since or (today - timedelta(days=365))
        req = DividendRequest(
            CTS=" ", GB1="0",
            F_DT=_yyyymmdd(start), T_DT=_yyyymmdd(today),
            SHT_CD=sym.ticker, HIGH_GB=" ",
        )
        resp = await call(self._broker, DividendExecutor, req)
        out: list[Dividend] = []
        for row in getattr(resp, "output1", []) or []:
            d = dividend_from_row(sym, row, row.model_dump())
            if d is not None:
                out.append(d)
        return out

    async def get_financials(
        self,
        symbol: Symbol | str,
        *,
        period: FinancialPeriod = FinancialPeriod.QUARTERLY,
        limit: int = 8,
    ) -> list[FinancialSummary]:
        sym = _as_symbol(symbol)
        req = FinancialRatioRequest(
            FID_DIV_CLS_CODE="1" if period is FinancialPeriod.QUARTERLY else "0",
            fid_cond_mrkt_div_code="J",
            fid_input_iscd=sym.ticker,
        )
        resp = await call(self._broker, FinancialRatioExecutor, req)
        out: list[FinancialSummary] = []
        for row in getattr(resp, "output", []) or []:
            s = financial_summary_from_ratio_row(sym, row, row.model_dump(), period=period)
            if s is not None:
                out.append(s)
        out.sort(key=lambda x: x.fiscal_date, reverse=True)
        return out[:limit]

    async def is_holiday(self, d: date) -> bool:
        req = ChkHolidayRequest(BASS_DT=_yyyymmdd(d), CTX_AREA_NK=" ", CTX_AREA_FK=" ")
        resp = await call(self._broker, ChkHolidayExecutor, req)
        # output1[?].opnd_yn == 'N' on target day means market closed.
        rows = getattr(resp, "output", None) or getattr(resp, "output1", []) or []
        for row in rows:
            if getattr(row, "bass_dt", None) == _yyyymmdd(d):
                return getattr(row, "opnd_yn", "Y") == "N"
        return False

    async def list_halts(self, *, on_date: date | None = None) -> list[TradingHalt]:
        """Halts via inquire-vi-status (volatility-interruption events).

        KIS does not expose a "trading-halt list" endpoint; VI events are the
        closest analogue. Permanent halts are reflected in inquire-price's
        trht_yn per-symbol — not surfaced here.
        """
        d = on_date or kst_today()
        req = InquireViStatusRequest(
            FID_DIV_CLS_CODE="0",
            FID_COND_SCR_DIV_CODE="20139",
            FID_MRKT_CLS_CODE="0",
            FID_INPUT_ISCD="0000",
            FID_RANK_SORT_CLS_CODE="0",
            FID_INPUT_DATE_1=_yyyymmdd(d),
            FID_TRGT_CLS_CODE="",
            FID_TRGT_EXLS_CLS_CODE="",
        )
        resp = await call(self._broker, InquireViStatusExecutor, req)
        out: list[TradingHalt] = []
        for row in getattr(resp, "output", []) or getattr(resp, "output1", []) or []:
            h = trading_halt_from_vi_row(row, row.model_dump())
            if h is not None:
                out.append(h)
        return out
