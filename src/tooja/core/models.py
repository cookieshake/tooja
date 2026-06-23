"""Shared domain models. Every response keeps a raw: dict for the broker payload."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Any, ClassVar, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from tooja.core.enums import (
    AssetClass,
    Exchange,
    FinancialPeriod,
    OrderSide,
    OrderStatus,
    TimeInForce,
)
from tooja.core.money import Money


class Symbol(BaseModel):
    """Instrument identifier.

    Accepted string forms:
      "005930"               -> KRX:STOCK
      "KRX:005930"           -> KRX:STOCK
      "NASD:AAPL"            -> NASD:STOCK
      "KRX:FUTOP:101W12000"  -> KRX:FUTURES_OPTIONS

    Parsing normalizes exchange to upper-case and asset to lower-case before enum lookup.
    """

    model_config = ConfigDict(frozen=True)

    ticker: str = Field(min_length=1)
    exchange: Exchange = Exchange.KRX
    asset: AssetClass = AssetClass.STOCK

    def __str__(self) -> str:
        return f"{self.exchange.value}:{self.ticker}"

    def __hash__(self) -> int:
        # frozen=True already makes Symbol hashable at runtime; declaring it
        # explicitly keeps it usable as a set/dict key under static type checkers
        # (which don't model pydantic's generated __hash__).
        return hash((self.ticker, self.exchange, self.asset))

    @classmethod
    def parse(cls, s: str) -> "Symbol":
        parts = [p.strip() for p in s.split(":")]
        if len(parts) == 1:
            return cls(ticker=parts[0])
        if len(parts) == 2:
            ex, tkr = parts
            return cls(ticker=tkr, exchange=cls._parse_exchange(ex))
        if len(parts) == 3:
            ex, ac, tkr = parts
            return cls(
                ticker=tkr,
                exchange=cls._parse_exchange(ex),
                asset=cls._parse_asset(ac),
            )
        raise ValueError(f"too many colons: {s!r}")

    @staticmethod
    def _parse_exchange(s: str) -> Exchange:
        try:
            return Exchange(s.upper())
        except ValueError as e:
            raise ValueError(f"unknown exchange: {s!r}") from e

    @staticmethod
    def _parse_asset(s: str) -> AssetClass:
        try:
            return AssetClass(s.lower())
        except ValueError as e:
            raise ValueError(f"unknown asset: {s!r}") from e


def _require_single_currency(values: Sequence[Money | None], context: str) -> None:
    currencies = {m.currency for m in values if m is not None}
    if len(currencies) > 1:
        raise ValueError(f"{context} has inconsistent currencies: {currencies}")


class _MoneyConsistent(BaseModel):
    """Subclasses declare `_money_fields: ClassVar[tuple[str, ...]]`; this mixin then
    verifies all listed fields share the same currency. Models with nested Money
    (list/dict of Money) keep an explicit validator."""

    _money_fields: ClassVar[tuple[str, ...]] = ()

    @model_validator(mode="after")
    def _check_money_currencies(self) -> Self:
        if self._money_fields:
            values = [getattr(self, name) for name in self._money_fields]
            _require_single_currency(values, type(self).__name__)
        return self


class Quote(_MoneyConsistent):
    _money_fields = ("price", "change", "open", "high", "low", "prev_close")
    symbol: Symbol
    price: Money
    time: datetime
    change: Money | None = None
    change_rate: Decimal | None = None
    open: Money | None = None
    high: Money | None = None
    low: Money | None = None
    prev_close: Money | None = None
    volume: Decimal | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class OHLCV(_MoneyConsistent):
    _money_fields = ("open", "high", "low", "close")
    symbol: Symbol
    time: datetime
    open: Money
    high: Money
    low: Money
    close: Money
    volume: Decimal


class OrderbookLevel(BaseModel):
    price: Money
    qty: Decimal


class Orderbook(BaseModel):
    symbol: Symbol
    time: datetime
    bids: list[OrderbookLevel]
    asks: list[OrderbookLevel]
    raw: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _check_currency(self) -> "Orderbook":
        levels = [lvl.price for lvl in (*self.bids, *self.asks)]
        _require_single_currency(levels, "Orderbook")
        return self


class Trade(BaseModel):
    symbol: Symbol
    time: datetime
    price: Money
    qty: Decimal
    side: OrderSide | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


# ─── Account ─────────────────────────────────────────
class Position(_MoneyConsistent):
    _money_fields = ("avg_price", "current_price", "market_value", "pnl")
    symbol: Symbol
    qty: Decimal
    avg_price: Money
    current_price: Money | None = None
    market_value: Money | None = None
    pnl: Money | None = None
    pnl_rate: Decimal | None = None


class Balance(BaseModel):
    total_asset: Money | None = None
    cash: list[Money] = Field(default_factory=list)
    positions: list[Position] = Field(default_factory=list)
    raw: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _check_cash_unique_currencies(self) -> "Balance":
        currencies = [m.currency for m in self.cash]
        if len(currencies) != len(set(currencies)):
            raise ValueError(f"Balance.cash has duplicate currencies: {currencies}")
        return self


# ─── Order state ─────────────────────────────────────
class Order(_MoneyConsistent):
    _money_fields = ("avg_fill_price", "price", "stop_price")
    order_id: str
    symbol: Symbol
    side: OrderSide
    qty: Decimal
    filled_qty: Decimal = Decimal(0)
    avg_fill_price: Money | None = None
    type: Literal["market", "limit", "stop_limit"]
    price: Money | None = None
    stop_price: Money | None = None
    status: OrderStatus
    time_in_force: TimeInForce = TimeInForce.DAY
    client_order_id: str | None = None
    submitted_at: datetime
    updated_at: datetime | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class Fill(_MoneyConsistent):
    _money_fields = ("price", "fee")
    order_id: str
    symbol: Symbol
    side: OrderSide
    qty: Decimal
    price: Money
    time: datetime
    fee: Money | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


# ─── Order requests (discriminated union) ────────────
class _OrderRequestBase(BaseModel):
    symbol: Symbol
    side: OrderSide
    qty: Decimal
    client_order_id: str | None = None


class MarketOrder(_OrderRequestBase):
    type: Literal["market"] = "market"


class LimitOrder(_OrderRequestBase):
    type: Literal["limit"] = "limit"
    price: Money
    time_in_force: TimeInForce = TimeInForce.DAY


class StopLimitOrder(_OrderRequestBase, _MoneyConsistent):
    _money_fields: ClassVar[tuple[str, ...]] = ("price", "stop_price")
    type: Literal["stop_limit"] = "stop_limit"
    price: Money
    stop_price: Money
    time_in_force: TimeInForce = TimeInForce.DAY


OrderRequest = Annotated[
    MarketOrder | LimitOrder | StopLimitOrder,
    Field(discriminator="type"),
]


# ─── Info models ─────────────────────────────────────
class StockInfo(_MoneyConsistent):
    _money_fields = ("par_value", "market_cap")
    symbol: Symbol
    name: str
    sector: str | None = None
    industry: str | None = None
    listed_at: date | None = None
    listed_shares: Decimal | None = None
    par_value: Money | None = None
    market_cap: Money | None = None
    foreign_ownership_rate: Decimal | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class FinancialSummary(_MoneyConsistent):
    _money_fields = ("revenue", "operating_profit", "net_profit", "eps", "bps")
    symbol: Symbol
    period: FinancialPeriod
    fiscal_date: date
    revenue: Money | None = None
    operating_profit: Money | None = None
    net_profit: Money | None = None
    eps: Money | None = None
    bps: Money | None = None
    per: Decimal | None = None
    pbr: Decimal | None = None
    roe: Decimal | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class Dividend(BaseModel):
    symbol: Symbol
    ex_date: date
    pay_date: date | None = None
    amount_per_share: Money
    dividend_type: Literal["cash", "stock"] = "cash"
    raw: dict[str, Any] = Field(default_factory=dict)


class TradingHalt(BaseModel):
    symbol: Symbol
    start: datetime
    end: datetime | None = None
    reason: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class PriceLimit(_MoneyConsistent):
    """Daily price band. upper/lower are None for markets without limits (e.g. US)."""

    _money_fields = ("upper_limit", "lower_limit", "base_price")
    symbol: Symbol
    upper_limit: Money | None = None
    lower_limit: Money | None = None
    base_price: Money | None = None
    as_of: datetime | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class StockWarnings(BaseModel):
    """Per-symbol trading caution flags. A flag is None when the broker does not
    report it (each adapter fills only the flags it actually exposes)."""

    symbol: Symbol
    is_trading_halt: bool | None = None     # 거래정지
    is_administrative: bool | None = None   # 관리종목
    is_liquidation: bool | None = None      # 정리매매
    is_overheated: bool | None = None       # 단기과열
    is_caution: bool | None = None          # 투자주의
    is_warning: bool | None = None          # 투자경고
    is_risk: bool | None = None             # 투자위험
    is_rights_offering: bool | None = None  # 신주인수권 등 권리 관련
    vi_triggered: bool | None = None        # VI 발동
    raw: dict[str, Any] = Field(default_factory=dict)


# ─── Analytics models ────────────────────────────────
class InvestorFlow(BaseModel):
    symbol: Symbol
    date: date
    individual_net: Money
    foreign_net: Money
    institutional_net: Money
    institutional_breakdown: dict[str, Money] = Field(default_factory=dict)
    raw: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _check_currency(self) -> "InvestorFlow":
        _require_single_currency(
            [
                self.individual_net,
                self.foreign_net,
                self.institutional_net,
                *self.institutional_breakdown.values(),
            ],
            "InvestorFlow",
        )
        return self


class ProgramTrading(_MoneyConsistent):
    _money_fields = ("arbitrage_net", "non_arbitrage_net")
    symbol: Symbol
    date: date
    arbitrage_net: Money
    non_arbitrage_net: Money
    raw: dict[str, Any] = Field(default_factory=dict)


class ShortSellingDaily(BaseModel):
    symbol: Symbol
    date: date
    short_volume: Decimal
    short_value: Money
    short_ratio: Decimal | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class MarginBalance(_MoneyConsistent):
    _money_fields = ("margin_loan", "stock_loan")
    symbol: Symbol
    date: date
    margin_loan: Money
    stock_loan: Money | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class SecuritiesLending(_MoneyConsistent):
    _money_fields = ("balance", "new_loan")
    symbol: Symbol
    date: date
    balance: Money
    new_loan: Money | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


# ─── Rankings / stream events ────────────────────────
class RankingEntry(BaseModel):
    """A single ranking row. `value` carries different meanings depending on
    RankingType (volume / turnover / change rate / ...), so it stays Decimal.
    `price` is always a price, so it is Money."""

    rank: int
    symbol: Symbol
    name: str
    value: Decimal
    price: Money | None = None
    change_rate: Decimal | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class OrderUpdate(BaseModel):
    order_id: str
    symbol: Symbol
    status: OrderStatus
    filled_qty: Decimal
    avg_fill_price: Money | None = None
    time: datetime
    raw: dict[str, Any] = Field(default_factory=dict)


class StreamControlEvent(BaseModel):
    kind: Literal["reconnected", "disconnected", "subscribed", "unsubscribed"]
    time: datetime
    detail: str | None = None
    symbols_affected: list[Symbol] = Field(default_factory=list)
