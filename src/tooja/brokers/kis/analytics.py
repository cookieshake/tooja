"""KIS Analytics subclient — investor flows / program trading / short selling /
margin balance / securities lending.

All endpoints scope by symbol + date window. KIS daily endpoints return up to
~100 rows per call; we filter to the [since, until] window client-side.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from tooja.brokers.kis._call import call
from tooja.brokers.kis._mappers import (
    investor_flow_from_row,
    margin_balance_from_row,
    program_trading_from_row,
    securities_lending_from_row,
    short_selling_from_row,
)
from tooja.brokers.kis.raw.domestic_stock_quotations.inquire_investor import (
    InquireInvestorExecutor,
    InquireInvestorRequest,
)
from tooja.brokers.kis.raw.domestic_stock_quote_analysis.daily_credit_balance import (
    DailyCreditBalanceExecutor,
    DailyCreditBalanceRequest,
)
from tooja.brokers.kis.raw.domestic_stock_quote_analysis.daily_loan_trans import (
    DailyLoanTransExecutor,
    DailyLoanTransRequest,
)
from tooja.brokers.kis.raw.domestic_stock_quote_analysis.daily_short_sale import (
    DailyShortSaleExecutor,
    DailyShortSaleRequest,
)
from tooja.brokers.kis.raw.domestic_stock_quote_analysis.program_trade_by_stock_daily import (
    ProgramTradeByStockDailyExecutor,
    ProgramTradeByStockDailyRequest,
)
from tooja.core.clients import AnalyticsClient
from tooja.core.enums import Exchange
from tooja.core.errors import UnsupportedOperation
from tooja.core.models import (
    InvestorFlow,
    MarginBalance,
    ProgramTrading,
    SecuritiesLending,
    ShortSellingDaily,
    Symbol,
)

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker


def _as_symbol(s: Symbol | str | Exchange) -> Symbol:
    if isinstance(s, Symbol):
        return s
    if isinstance(s, Exchange):
        raise UnsupportedOperation(
            "KIS analytics requires a Symbol, not an Exchange (market-level not supported)",
            broker="kis",
        )
    return Symbol.parse(s)


def _yyyymmdd(d: date) -> str:
    return d.strftime("%Y%m%d")


class KisAnalyticsClient(AnalyticsClient):
    _broker_name = "kis"

    def __init__(self, broker: "KisBroker"):
        self._broker = broker

    async def investor_flows(
        self, symbol: Symbol | str, *, since: date, until: date,
    ) -> list[InvestorFlow]:
        sym = _as_symbol(symbol)
        req = InquireInvestorRequest(FID_COND_MRKT_DIV_CODE="J", FID_INPUT_ISCD=sym.ticker)
        resp = await call(self._broker, InquireInvestorExecutor, req)
        out: list[InvestorFlow] = []
        for row in getattr(resp, "output", []) or []:
            f = investor_flow_from_row(sym, row, row.model_dump())
            if f is not None and since <= f.date <= until:
                out.append(f)
        out.sort(key=lambda x: x.date)
        return out

    async def program_trading(
        self,
        symbol_or_market: Symbol | str | Exchange,
        *,
        since: date,
        until: date,
    ) -> list[ProgramTrading]:
        sym = _as_symbol(symbol_or_market)
        req = ProgramTradeByStockDailyRequest(
            FID_COND_MRKT_DIV_CODE="J",
            FID_INPUT_ISCD=sym.ticker,
            FID_INPUT_DATE_1=_yyyymmdd(until),
        )
        resp = await call(self._broker, ProgramTradeByStockDailyExecutor, req)
        out: list[ProgramTrading] = []
        for row in getattr(resp, "output", []) or []:
            p = program_trading_from_row(sym, row, row.model_dump())
            if p is not None and since <= p.date <= until:
                out.append(p)
        out.sort(key=lambda x: x.date)
        return out

    async def short_selling(
        self, symbol: Symbol | str, *, since: date, until: date,
    ) -> list[ShortSellingDaily]:
        sym = _as_symbol(symbol)
        req = DailyShortSaleRequest(
            FID_INPUT_DATE_2=_yyyymmdd(until),
            FID_COND_MRKT_DIV_CODE="J",
            FID_INPUT_ISCD=sym.ticker,
            FID_INPUT_DATE_1=_yyyymmdd(since),
        )
        resp = await call(self._broker, DailyShortSaleExecutor, req)
        out: list[ShortSellingDaily] = []
        for row in getattr(resp, "output", []) or getattr(resp, "output1", []) or []:
            s = short_selling_from_row(sym, row, row.model_dump())
            if s is not None and since <= s.date <= until:
                out.append(s)
        out.sort(key=lambda x: x.date)
        return out

    async def margin_balance(
        self, symbol: Symbol | str, *, since: date, until: date,
    ) -> list[MarginBalance]:
        sym = _as_symbol(symbol)
        # Endpoint returns latest backwards from FID_INPUT_DATE_1.
        req = DailyCreditBalanceRequest(
            fid_cond_mrkt_div_code="J",
            fid_cond_scr_div_code="20476",
            fid_input_iscd=sym.ticker,
            fid_input_date_1=_yyyymmdd(until),
        )
        resp = await call(self._broker, DailyCreditBalanceExecutor, req)
        out: list[MarginBalance] = []
        for row in getattr(resp, "output", []) or getattr(resp, "output1", []) or []:
            m = margin_balance_from_row(sym, row, row.model_dump())
            if m is not None and since <= m.date <= until:
                out.append(m)
        out.sort(key=lambda x: x.date)
        return out

    async def securities_lending(
        self, symbol: Symbol | str, *, since: date, until: date,
    ) -> list[SecuritiesLending]:
        sym = _as_symbol(symbol)
        req = DailyLoanTransRequest(
            MRKT_DIV_CLS_CODE="3",
            MKSC_SHRN_ISCD=sym.ticker,
            START_DATE=_yyyymmdd(since),
            END_DATE=_yyyymmdd(until),
            CTS=" ",
        )
        resp = await call(self._broker, DailyLoanTransExecutor, req)
        out: list[SecuritiesLending] = []
        for row in getattr(resp, "output1", []) or []:
            s = securities_lending_from_row(sym, row, row.model_dump())
            if s is not None and since <= s.date <= until:
                out.append(s)
        out.sort(key=lambda x: x.date)
        return out
