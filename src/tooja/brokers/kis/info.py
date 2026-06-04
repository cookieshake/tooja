"""KIS Info subclient — instrument lookup / dividends.

Methods that need scope (search by name, halts list, holiday calendar) raise
UnsupportedOperation rather than guessing endpoints — adapters add them as needed.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING

from tooja.brokers.kis._call import call
from tooja.brokers.kis._mappers import dividend_from_row, stock_info_from_search
from tooja.brokers.kis.raw.domestic_stock_info.dividend import (
    DividendExecutor,
    DividendRequest,
)
from tooja.brokers.kis.raw.domestic_stock_info.search_stock_info import (
    SearchStockInfoExecutor,
    SearchStockInfoRequest,
)
from tooja.core.clients import InfoClient
from tooja.core.errors import SymbolNotFound
from tooja.core.models import Dividend, StockInfo, Symbol

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker


def _as_symbol(s: Symbol | str) -> Symbol:
    return s if isinstance(s, Symbol) else Symbol.parse(s)


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
        self,
        symbol: Symbol | str,
        *,
        since: date | None = None,
    ) -> list[Dividend]:
        sym = _as_symbol(symbol)
        today = date.today()
        start = since or (today - timedelta(days=365))
        req = DividendRequest(
            CTS=" ",
            GB1="0",
            F_DT=_yyyymmdd(start),
            T_DT=_yyyymmdd(today),
            SHT_CD=sym.ticker,
            HIGH_GB=" ",
        )
        resp = await call(self._broker, DividendExecutor, req)
        out: list[Dividend] = []
        for row in getattr(resp, "output1", []) or []:
            d = dividend_from_row(sym, row, row.model_dump())
            if d is not None:
                out.append(d)
        return out
