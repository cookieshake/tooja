"""Toss market-data subclient — implements the MarketClient ABC.

All remote calls go through ``call(broker, ExecutorCls, query={...})``.
No I/O or state beyond ``self._broker``.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from tooja.brokers.toss._call import call
from tooja.brokers.toss._mappers import (
    ohlcv_from_candle,
    orderbook_from_response,
    price_limit_from_response,
    quote_from_price,
)
from tooja.brokers.toss.raw.market_data.get_candles import GetCandlesExecutor
from tooja.brokers.toss.raw.market_data.get_orderbook import GetOrderbookExecutor
from tooja.brokers.toss.raw.market_data.get_price_limit import GetPriceLimitExecutor
from tooja.brokers.toss.raw.market_data.get_prices import GetPricesExecutor
from tooja.core.clients import MarketClient
from tooja.core.errors import SymbolNotFound, UnsupportedOperation
from tooja.core.models import OHLCV, Orderbook, PriceLimit, Quote, Symbol

if TYPE_CHECKING:
    from tooja.brokers.toss.broker import TossBroker

# ── interval mapping ──────────────────────────────────────────────────────────

_INTERVAL_MAP: dict[str, str] = {
    "1m": "1m",
    "1d": "1d",
}

# ── helpers ───────────────────────────────────────────────────────────────────


logger = logging.getLogger(__name__)


def _as_symbol(symbol: Symbol | str) -> Symbol:
    return Symbol.parse(symbol) if isinstance(symbol, str) else symbol


def _ticker(symbol: Symbol | str) -> str:
    return _as_symbol(symbol).ticker


# ── subclient ─────────────────────────────────────────────────────────────────


class TossMarketClient(MarketClient):
    _broker_name = "toss"

    def __init__(self, broker: "TossBroker") -> None:
        self._broker = broker

    # ------------------------------------------------------------------
    # get_quote
    # ------------------------------------------------------------------

    async def get_quote(self, symbol: Symbol | str) -> Quote:
        ticker = _ticker(symbol)
        result = await call(
            self._broker,
            GetPricesExecutor,
            query={"symbols": ticker},
        )
        if not result.root:
            raise SymbolNotFound(
                f"Toss: no price data returned for {ticker!r}",
                broker="toss",
            )
        return quote_from_price(result.root[0])

    # ------------------------------------------------------------------
    # get_quotes
    # ------------------------------------------------------------------

    async def get_quotes(self, symbols: list[Symbol | str]) -> list[Quote]:
        tickers = [_ticker(s) for s in symbols]
        quotes: list[Quote] = []
        # Batch in groups of 200 (Toss API limit per call)
        for i in range(0, max(len(tickers), 1), 200):
            batch = tickers[i : i + 200]
            if not batch:
                break
            result = await call(
                self._broker,
                GetPricesExecutor,
                query={"symbols": ",".join(batch)},
            )
            quotes.extend(quote_from_price(p) for p in result.root)
        return quotes

    # ------------------------------------------------------------------
    # get_orderbook
    # ------------------------------------------------------------------

    async def get_orderbook(self, symbol: Symbol | str, *, depth: int = 10) -> Orderbook:
        sym = _as_symbol(symbol)
        resp = await call(
            self._broker,
            GetOrderbookExecutor,
            query={"symbol": sym.ticker},
        )
        return orderbook_from_response(sym, resp, depth=depth)

    # ------------------------------------------------------------------
    # get_ohlcv
    # ------------------------------------------------------------------

    async def get_ohlcv(
        self,
        symbol: Symbol | str,
        *,
        interval: str,
        start: object = None,
        end: object = None,
        limit: int | None = None,
    ) -> list[OHLCV]:
        """Return OHLCV candles for *symbol* at the given *interval*.

        Note: Toss candles support only ``before``/``count`` pagination —
        ``start`` is not supported by the API and is ignored
        (use ``end`` → ``before``).
        """
        if start is not None:
            logger.debug(
                "toss get_ohlcv ignores start=%s (unsupported by candles API)", start
            )
        iv = _INTERVAL_MAP.get(interval)
        if iv is None:
            raise UnsupportedOperation(
                "toss supports only 1m/1d candles",
                broker="toss",
            )
        sym = _as_symbol(symbol)
        query: dict = {
            "symbol": sym.ticker,
            "interval": iv,
            "count": min(limit or 100, 200),
        }
        if end is not None:
            # end may be datetime or str; convert to ISO string if needed
            if hasattr(end, "isoformat"):
                query["before"] = end.isoformat()
            else:
                query["before"] = str(end)

        resp = await call(self._broker, GetCandlesExecutor, query=query)
        return [ohlcv_from_candle(sym, c) for c in resp.candles]

    # ------------------------------------------------------------------
    # get_price_limits
    # ------------------------------------------------------------------

    async def get_price_limits(self, symbol: Symbol | str) -> PriceLimit:
        sym = _as_symbol(symbol)
        resp = await call(
            self._broker,
            GetPriceLimitExecutor,
            query={"symbol": sym.ticker},
        )
        return price_limit_from_response(sym, resp)
