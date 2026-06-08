"""The seven subclient ABCs.

Adapters override only the methods they support.
Non-overridden methods raise the default `UnsupportedOperation(...)`.
"""

from __future__ import annotations

from abc import ABC
from datetime import date, datetime
from decimal import Decimal
from typing import AsyncIterator, Literal

from tooja.core.enums import Currency, Exchange, FinancialPeriod, RankingType
from tooja.core.errors import UnsupportedOperation
from tooja.core.models import (
    Balance,
    Dividend,
    FinancialSummary,
    Fill,
    InvestorFlow,
    MarginBalance,
    Money,
    OHLCV,
    Order,
    OrderRequest,
    Orderbook,
    Position,
    PriceLimit,
    ProgramTrading,
    Quote,
    RankingEntry,
    SecuritiesLending,
    ShortSellingDaily,
    StockInfo,
    StockWarnings,
    Symbol,
    TradingHalt,
)
from tooja.core.stream import (
    OrderUpdateStream,
    OrderbookStream,
    QuoteStream,
    TradeStream,
)


def _raise(method: str, broker_name: str) -> "UnsupportedOperation":
    return UnsupportedOperation(
        f"{broker_name} does not support {method}",
        broker=broker_name,
    )


class _Sub(ABC):
    """Subclient base — carries the adapter's broker_name."""

    _broker_name: str


class MarketClient(_Sub):
    async def get_quote(self, symbol: Symbol | str) -> Quote:
        raise _raise("market.get_quote", self._broker_name)

    async def get_quotes(self, symbols: list[Symbol | str]) -> list[Quote]:
        raise _raise("market.get_quotes", self._broker_name)

    async def get_ohlcv(
        self,
        symbol: Symbol | str,
        *,
        interval: Literal["1m", "5m", "15m", "30m", "1h", "1d", "1w", "1M"],
        start: date | datetime | str | None = None,
        end: date | datetime | str | None = None,
        limit: int | None = None,
    ) -> list[OHLCV]:
        raise _raise("market.get_ohlcv", self._broker_name)

    async def get_orderbook(self, symbol: Symbol | str, *, depth: int = 10) -> Orderbook:
        raise _raise("market.get_orderbook", self._broker_name)

    async def get_price_limits(self, symbol: Symbol | str) -> PriceLimit:
        raise _raise("market.get_price_limits", self._broker_name)


class AccountClient(_Sub):
    async def get_balance(self) -> Balance:
        raise _raise("account.get_balance", self._broker_name)

    async def get_positions(self) -> list[Position]:
        raise _raise("account.get_positions", self._broker_name)

    async def get_position(self, symbol: Symbol | str) -> Position | None:
        raise _raise("account.get_position", self._broker_name)

    async def get_buying_power(self, *, currency: Currency = Currency.KRW) -> Money:
        raise _raise("account.get_buying_power", self._broker_name)

    async def get_sellable_quantity(self, symbol: Symbol | str) -> Decimal:
        raise _raise("account.get_sellable_quantity", self._broker_name)


class OrdersClient(_Sub):
    async def create(self, req: OrderRequest) -> Order:
        raise _raise("orders.create", self._broker_name)

    async def cancel(self, order_id: str) -> Order:
        raise _raise("orders.cancel", self._broker_name)

    async def replace(
        self,
        order_id: str,
        *,
        qty: Decimal | None = None,
        price: Decimal | None = None,
    ) -> Order:
        raise _raise("orders.replace", self._broker_name)

    async def get(self, order_id: str) -> Order:
        raise _raise("orders.get", self._broker_name)

    async def list_orders(
        self,
        *,
        status: Literal["all", "open", "closed"] = "all",
        symbol: Symbol | str | None = None,
        since: date | datetime | None = None,
        until: date | datetime | None = None,
    ) -> list[Order]:
        raise _raise("orders.list_orders", self._broker_name)

    async def iter_orders(self, **kwargs) -> AsyncIterator[Order]:
        raise _raise("orders.iter_orders", self._broker_name)
        yield  # makes this an async generator (unreachable)

    async def list_fills(
        self,
        *,
        symbol: Symbol | str | None = None,
        since: date | datetime | None = None,
        until: date | datetime | None = None,
    ) -> list[Fill]:
        raise _raise("orders.list_fills", self._broker_name)

    async def iter_fills(self, **kwargs) -> AsyncIterator[Fill]:
        raise _raise("orders.iter_fills", self._broker_name)
        yield  # makes this an async generator (unreachable)


class InfoClient(_Sub):
    async def get_stock(self, symbol: Symbol | str) -> StockInfo:
        raise _raise("info.get_stock", self._broker_name)

    async def search(self, query: str) -> list[StockInfo]:
        raise _raise("info.search", self._broker_name)

    async def list_by_industry(self, industry: str) -> list[StockInfo]:
        raise _raise("info.list_by_industry", self._broker_name)

    async def get_financials(
        self,
        symbol: Symbol | str,
        *,
        period: FinancialPeriod = FinancialPeriod.QUARTERLY,
        limit: int = 8,
    ) -> list[FinancialSummary]:
        raise _raise("info.get_financials", self._broker_name)

    async def get_dividends(
        self,
        symbol: Symbol | str,
        *,
        since: date | None = None,
    ) -> list[Dividend]:
        raise _raise("info.get_dividends", self._broker_name)

    async def list_halts(self, *, on_date: date | None = None) -> list[TradingHalt]:
        raise _raise("info.list_halts", self._broker_name)

    async def is_holiday(self, d: date) -> bool:
        raise _raise("info.is_holiday", self._broker_name)

    async def get_warnings(self, symbol: Symbol | str) -> StockWarnings:
        raise _raise("info.get_warnings", self._broker_name)


class AnalyticsClient(_Sub):
    async def investor_flows(
        self,
        symbol: Symbol | str,
        *,
        since: date,
        until: date,
    ) -> list[InvestorFlow]:
        raise _raise("analytics.investor_flows", self._broker_name)

    async def program_trading(
        self,
        symbol_or_market: Symbol | str | Exchange,
        *,
        since: date,
        until: date,
    ) -> list[ProgramTrading]:
        raise _raise("analytics.program_trading", self._broker_name)

    async def short_selling(
        self,
        symbol: Symbol | str,
        *,
        since: date,
        until: date,
    ) -> list[ShortSellingDaily]:
        raise _raise("analytics.short_selling", self._broker_name)

    async def margin_balance(
        self,
        symbol: Symbol | str,
        *,
        since: date,
        until: date,
    ) -> list[MarginBalance]:
        raise _raise("analytics.margin_balance", self._broker_name)

    async def securities_lending(
        self,
        symbol: Symbol | str,
        *,
        since: date,
        until: date,
    ) -> list[SecuritiesLending]:
        raise _raise("analytics.securities_lending", self._broker_name)


class RankingsClient(_Sub):
    async def get(
        self,
        type: RankingType,
        *,
        market: Exchange = Exchange.KRX,
        limit: int = 30,
    ) -> list[RankingEntry]:
        raise _raise("rankings.get", self._broker_name)


class StreamClient(_Sub):
    def quotes(
        self,
        symbols: list[Symbol | str],
        *,
        include_control: bool = False,
        auto_reconnect: bool = True,
        buffer_size: int = 1024,
    ) -> QuoteStream:
        raise _raise("stream.quotes", self._broker_name)

    def trades(
        self,
        symbols: list[Symbol | str],
        *,
        include_control: bool = False,
        auto_reconnect: bool = True,
        buffer_size: int = 1024,
    ) -> TradeStream:
        raise _raise("stream.trades", self._broker_name)

    def orderbook(
        self,
        symbols: list[Symbol | str],
        *,
        include_control: bool = False,
        auto_reconnect: bool = True,
        buffer_size: int = 1024,
    ) -> OrderbookStream:
        raise _raise("stream.orderbook", self._broker_name)

    def orders(
        self,
        *,
        include_control: bool = False,
        auto_reconnect: bool = True,
        buffer_size: int = 1024,
    ) -> OrderUpdateStream:
        raise _raise("stream.orders", self._broker_name)
