"""Pure raw→domain converters for the Toss adapter.

No I/O. Each function takes a generated Toss raw model (or primitive) and
returns a core domain model. Money amounts are always ``Decimal`` (the
generated ``TDecimal`` fields are already ``Decimal | None``).
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal

from tooja.core.enums import AssetClass, Currency, Exchange, OrderSide, OrderStatus
from tooja.core.models import (
    Balance,
    OHLCV,
    Order,
    Orderbook,
    OrderbookLevel,
    Position,
    PriceLimit,
    Quote,
    StockInfo,
    StockWarnings,
    Symbol,
)
from tooja.core.money import Money

from tooja.brokers.toss.raw.models import (
    Candle,
    HoldingsItem,
    HoldingsOverview,
    Order as TossOrder,
    OrderbookResponse,
    PriceLimitResponse,
    PriceResponse,
    StockInfo as TossStockInfo,
    StockWarning,
)


# ─── primitives ──────────────────────────────────────────


def to_currency(s: str | Currency) -> Currency:
    """Map a Toss currency string ("KRW"/"USD") to ``Currency``."""
    if isinstance(s, Currency):
        return s
    return Currency(s.upper())


def _money(amount: Decimal | None, currency: str | Currency) -> Money | None:
    """None-safe Money builder. ``amount is None`` → ``None``."""
    if amount is None:
        return None
    return Money(amount=amount, currency=to_currency(currency))


def _parse_dt(s: str | None) -> datetime | None:
    """Parse an ISO 8601 timestamp (incl. offset like ``+09:00``)."""
    if not s:
        return None
    return datetime.fromisoformat(s)


def _parse_date(s: str | None) -> date | None:
    """Parse a ``YYYY-MM-DD`` date string."""
    if not s:
        return None
    return date.fromisoformat(s)


# ─── symbol ──────────────────────────────────────────────

# Toss `market` segment → core Exchange.
_MARKET_EXCHANGE: dict[str, Exchange] = {
    "KOSPI": Exchange.KRX,
    "KOSDAQ": Exchange.KRX,
    "KR_ETC": Exchange.KRX,
    "NYSE": Exchange.NYSE,
    "NASDAQ": Exchange.NASD,
    "AMEX": Exchange.AMEX,
    "US_ETC": Exchange.NASD,
}

# Toss `marketCountry` → core Exchange.
_COUNTRY_EXCHANGE: dict[str, Exchange] = {
    "KR": Exchange.KRX,
    "US": Exchange.NASD,
}


def to_symbol(
    toss_symbol: str,
    *,
    market: str | None = None,
    market_country: str | None = None,
) -> Symbol:
    """Build a core ``Symbol`` with market-aware exchange inference.

    Priority: explicit ``market`` segment → ``market_country`` → ticker shape
    (digit-only → KRX, otherwise → NASD). Always ``asset=STOCK``.
    """
    exchange: Exchange | None = None
    if market is not None:
        exchange = _MARKET_EXCHANGE.get(market.upper())
    if exchange is None and market_country is not None:
        exchange = _COUNTRY_EXCHANGE.get(market_country.upper())
    if exchange is None:
        exchange = Exchange.KRX if toss_symbol.isdigit() else Exchange.NASD
    return Symbol(ticker=toss_symbol, exchange=exchange, asset=AssetClass.STOCK)


# ─── market data ─────────────────────────────────────────


def quote_from_price(p: PriceResponse) -> Quote:
    price = _money(p.last_price, p.currency)
    if price is None:
        raise ValueError("PriceResponse has no lastPrice")
    return Quote(
        symbol=to_symbol(p.symbol),
        price=price,
        time=_parse_dt(p.timestamp) or datetime.now(timezone.utc),
        raw=p.model_dump(by_alias=True),
    )


def orderbook_from_response(
    symbol: Symbol, r: OrderbookResponse, *, depth: int
) -> Orderbook:
    def _levels(entries: list) -> list[OrderbookLevel]:
        out: list[OrderbookLevel] = []
        for entry in entries[:depth]:
            price = _money(entry.price, r.currency)
            if price is None or entry.volume is None:
                continue
            out.append(OrderbookLevel(price=price, qty=entry.volume))
        return out

    return Orderbook(
        symbol=symbol,
        time=_parse_dt(r.timestamp) or datetime.now(timezone.utc),
        bids=_levels(r.bids),
        asks=_levels(r.asks),
        raw=r.model_dump(by_alias=True),
    )


def ohlcv_from_candle(symbol: Symbol, c: Candle) -> OHLCV:
    cur = c.currency
    o = _money(c.open_price, cur)
    h = _money(c.high_price, cur)
    low = _money(c.low_price, cur)
    close = _money(c.close_price, cur)
    if o is None or h is None or low is None or close is None:
        raise ValueError("Candle is missing OHLC prices")
    return OHLCV(
        symbol=symbol,
        time=_parse_dt(c.timestamp) or datetime.now(timezone.utc),
        open=o,
        high=h,
        low=low,
        close=close,
        volume=c.volume if c.volume is not None else Decimal(0),
    )


def price_limit_from_response(symbol: Symbol, r: PriceLimitResponse) -> PriceLimit:
    return PriceLimit(
        symbol=symbol,
        upper_limit=_money(r.upper_limit_price, r.currency),
        lower_limit=_money(r.lower_limit_price, r.currency),
        as_of=_parse_dt(r.timestamp),
        raw=r.model_dump(by_alias=True),
    )


# ─── account ─────────────────────────────────────────────


def position_from_holding(item: HoldingsItem) -> Position:
    cur = item.currency
    avg = _money(item.average_purchase_price, cur)
    if avg is None:
        raise ValueError(f"HoldingsItem {item.symbol} has no averagePurchasePrice")
    return Position(
        symbol=to_symbol(item.symbol, market_country=item.market_country),
        qty=item.quantity if item.quantity is not None else Decimal(0),
        avg_price=avg,
        current_price=_money(item.last_price, cur),
        market_value=_money(item.market_value.amount, cur),
        pnl=_money(item.profit_loss.amount, cur),
        pnl_rate=item.profit_loss.rate,
    )


def balance_from_holdings(o: HoldingsOverview, cash: list[Money] | None = None) -> Balance:
    # total_asset is the KRW-denominated holdings market value. Cash is the
    # per-currency spendable amount (Toss buying-power endpoint), passed in by
    # the account client; positions keep their own per-currency Money.
    total_asset: Money | None = None
    krw = o.market_value.amount.krw
    if krw is not None:
        total_asset = Money(amount=krw, currency=Currency.KRW)
    return Balance(
        total_asset=total_asset,
        cash=cash or [],
        positions=[position_from_holding(item) for item in o.items],
        raw=o.model_dump(by_alias=True),
    )


# ─── orders ──────────────────────────────────────────────

_ORDER_STATUS: dict[str, OrderStatus] = {
    "PENDING": OrderStatus.PENDING,
    "PENDING_CANCEL": OrderStatus.OPEN,
    "PENDING_REPLACE": OrderStatus.OPEN,
    "PARTIAL_FILLED": OrderStatus.PARTIALLY_FILLED,
    "FILLED": OrderStatus.FILLED,
    "CANCELED": OrderStatus.CANCELLED,
    "REJECTED": OrderStatus.REJECTED,
    "CANCEL_REJECTED": OrderStatus.REJECTED,
    "REPLACE_REJECTED": OrderStatus.REJECTED,
    "REPLACED": OrderStatus.OPEN,
}

_ORDER_TYPE: dict[str, str] = {
    "LIMIT": "limit",
    "MARKET": "market",
}


def order_from_toss(o: TossOrder) -> Order:
    cur = o.currency
    side = OrderSide.BUY if o.side.upper() == "BUY" else OrderSide.SELL
    order_type = _ORDER_TYPE.get(o.order_type.upper(), "limit")
    status = _ORDER_STATUS.get(o.status.upper(), OrderStatus.PENDING)
    ex = o.execution
    return Order(
        order_id=o.order_id,
        symbol=to_symbol(o.symbol),
        side=side,
        qty=o.quantity if o.quantity is not None else Decimal(0),
        filled_qty=ex.filled_quantity if ex.filled_quantity is not None else Decimal(0),
        avg_fill_price=_money(ex.average_filled_price, cur),
        type=order_type,
        price=_money(o.price, cur),
        status=status,
        submitted_at=_parse_dt(o.ordered_at) or datetime.now(timezone.utc),
        updated_at=_parse_dt(o.canceled_at),
        raw=o.model_dump(by_alias=True),
    )


# ─── info ────────────────────────────────────────────────


def stock_info_from_toss(s: TossStockInfo) -> StockInfo:
    # Toss does not provide sector/industry/par_value/market_cap.
    return StockInfo(
        symbol=to_symbol(s.symbol, market=s.market),
        name=s.name,
        listed_at=_parse_date(s.list_date),
        listed_shares=s.shares_outstanding,
        raw=s.model_dump(by_alias=True),
    )


# Toss StockWarning.warningType enum → which StockWarnings flag it sets.
# Codes with no semantic match in our flag set (e.g. a plain CAUTION /
# trading-halt / administrative designation) are intentionally absent so
# unknown/forward-compat codes are ignored rather than crashing.
_WARNING_FLAGS: dict[str, str] = {
    "LIQUIDATION_TRADING": "is_liquidation",
    "OVERHEATED": "is_overheated",
    "INVESTMENT_WARNING": "is_warning",
    "INVESTMENT_RISK": "is_risk",
    "VI_STATIC_AND_DYNAMIC": "vi_triggered",
    "VI_STATIC": "vi_triggered",
    "VI_DYNAMIC": "vi_triggered",
    "STOCK_WARRANTS": "is_rights_offering",
}


def stock_warnings_from_toss(
    symbol: Symbol, warnings: list[StockWarning]
) -> StockWarnings:
    """Set per-symbol caution flags from Toss warnings.

    A flag becomes True if any matching warning is present; flags with no
    matching warning stay None. Matching is case-insensitive; unmapped warning
    types are ignored (forward-compat).
    """
    flags: dict[str, bool] = {}
    for w in warnings:
        if not w.warning_type:
            continue
        attr = _WARNING_FLAGS.get(w.warning_type.upper())
        if attr is not None:
            flags[attr] = True
    return StockWarnings(
        symbol=symbol,
        raw={"warnings": [w.model_dump(by_alias=True) for w in warnings]},
        **flags,
    )
