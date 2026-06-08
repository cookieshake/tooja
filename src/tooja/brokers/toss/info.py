"""Toss info subclient — implements the InfoClient ABC.

All remote calls go through ``call(broker, ExecutorCls, ...)``.
No I/O or state beyond ``self._broker``.

Supported methods:
- get_stock      — fetches basic instrument metadata for one symbol
- get_warnings   — fetches per-symbol caution flags
- is_holiday     — checks whether a date is a KR market holiday

Not implemented (no suitable Toss endpoint):
- search / list_by_industry / get_financials / get_dividends / list_halts
  — these raise UnsupportedOperation via the ABC default.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from tooja.brokers.toss._call import call
from tooja.brokers.toss._mappers import stock_info_from_toss, stock_warnings_from_toss
from tooja.brokers.toss.raw.market_info.get_kr_market_calendar import (
    GetKrMarketCalendarExecutor,
)
from tooja.brokers.toss.raw.stock_info.get_stock_warnings import (
    GetStockWarningsExecutor,
)
from tooja.brokers.toss.raw.stock_info.get_stocks import GetStocksExecutor
from tooja.core.clients import InfoClient
from tooja.core.errors import SymbolNotFound
from tooja.core.models import StockInfo, StockWarnings, Symbol

if TYPE_CHECKING:
    from tooja.brokers.toss.broker import TossBroker

# ── helpers ───────────────────────────────────────────────────────────────────


def _as_symbol(symbol: Symbol | str) -> Symbol:
    return Symbol.parse(symbol) if isinstance(symbol, str) else symbol


def _ticker(symbol: Symbol | str) -> str:
    return _as_symbol(symbol).ticker


# ── subclient ─────────────────────────────────────────────────────────────────


class TossInfoClient(InfoClient):
    _broker_name = "toss"

    def __init__(self, broker: "TossBroker") -> None:
        self._broker = broker

    # ------------------------------------------------------------------
    # get_stock
    # ------------------------------------------------------------------

    async def get_stock(self, symbol: Symbol | str) -> StockInfo:
        ticker = _ticker(symbol)
        result = await call(
            self._broker,
            GetStocksExecutor,
            query={"symbols": ticker},
        )
        if not result.root:
            raise SymbolNotFound(
                f"Toss: no stock data returned for {ticker!r}",
                broker="toss",
            )
        return stock_info_from_toss(result.root[0])

    # ------------------------------------------------------------------
    # get_warnings
    # ------------------------------------------------------------------

    async def get_warnings(self, symbol: Symbol | str) -> StockWarnings:
        sym = _as_symbol(symbol)
        result = await call(
            self._broker,
            GetStockWarningsExecutor,
            path_params={"symbol": sym.ticker},
        )
        return stock_warnings_from_toss(sym, result.root)

    # ------------------------------------------------------------------
    # is_holiday
    # ------------------------------------------------------------------

    async def is_holiday(self, d: date) -> bool:
        """Return True if *d* is a KR market holiday, False if it is a business day.

        Holiday heuristic: Toss's KR market calendar API returns a
        ``KrMarketCalendarResponse`` whose ``today`` field describes the *closest*
        business day, not necessarily *d* itself.  We therefore treat *d* as a
        holiday in either of two cases:

        1. ``resp.today.date != d.isoformat()`` — the API snapped to a different
           date, meaning *d* itself has no business-day record (weekend or holiday).
        2. ``resp.today.integrated is None`` — the date matches but both KRX and NXT
           are closed (integrated trading hours absent), so no market session runs.
        """
        resp = await call(
            self._broker,
            GetKrMarketCalendarExecutor,
            query={"date": d.isoformat()},
        )
        if resp.today.date != d.isoformat():
            return True
        if resp.today.integrated is None:
            return True
        return False
