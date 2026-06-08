"""tooja.core — shared interfaces, models, and errors."""

from tooja.core.broker import Broker
from tooja.core.clients import (
    AccountClient,
    AnalyticsClient,
    InfoClient,
    MarketClient,
    OrdersClient,
    RankingsClient,
    StreamClient,
)
from tooja.core.enums import (
    AssetClass,
    Currency,
    Exchange,
    FinancialPeriod,
    OrderSide,
    OrderStatus,
    RankingType,
    TimeInForce,
)
from tooja.core.errors import (
    AuthError,
    BrokerAPIError,
    BrokerError,
    ConfigError,
    InsufficientFunds,
    MarketClosed,
    NetworkError,
    OrderError,
    OrderNotFound,
    OrderRejected,
    PermissionDenied,
    RateLimitError,
    SubscriptionLimitExceeded,
    SymbolNotFound,
    TimeoutError,
    UnsupportedOperation,
)
from tooja.core.money import CurrencyMismatchError, Money
from tooja.core.rate_limit import RateLimitConfig, TokenBucket
from tooja.core.models import (
    OHLCV,
    Balance,
    Dividend,
    Fill,
    FinancialSummary,
    InvestorFlow,
    LimitOrder,
    MarginBalance,
    MarketOrder,
    Order,
    OrderRequest,
    OrderUpdate,
    Orderbook,
    OrderbookLevel,
    Position,
    PriceLimit,
    ProgramTrading,
    Quote,
    RankingEntry,
    SecuritiesLending,
    ShortSellingDaily,
    StockInfo,
    StockWarnings,
    StopLimitOrder,
    StreamControlEvent,
    Symbol,
    Trade,
    TradingHalt,
)
from tooja.core.stream import (
    OrderUpdateStream,
    OrderbookStream,
    QuoteStream,
    TradeStream,
)

__all__ = [
    # enums
    "AssetClass", "Currency", "Exchange", "FinancialPeriod",
    "OrderSide", "OrderStatus", "RankingType", "TimeInForce",
    # money
    "Money", "CurrencyMismatchError",
    # rate limit
    "RateLimitConfig", "TokenBucket",
    # models
    "Symbol", "Quote", "OHLCV", "Orderbook", "OrderbookLevel", "Trade",
    "Position", "Balance", "Order", "Fill",
    "MarketOrder", "LimitOrder", "StopLimitOrder", "OrderRequest",
    "StockInfo", "FinancialSummary", "Dividend", "TradingHalt",
    "PriceLimit", "StockWarnings",
    "InvestorFlow", "ProgramTrading", "ShortSellingDaily",
    "MarginBalance", "SecuritiesLending",
    "RankingEntry", "OrderUpdate", "StreamControlEvent",
    # ABCs
    "Broker",
    "MarketClient", "AccountClient", "OrdersClient", "InfoClient",
    "AnalyticsClient", "RankingsClient", "StreamClient",
    "QuoteStream", "TradeStream", "OrderbookStream", "OrderUpdateStream",
    # errors
    "BrokerError", "AuthError", "PermissionDenied",
    "RateLimitError", "UnsupportedOperation",
    "MarketClosed", "SymbolNotFound",
    "OrderError", "OrderRejected", "InsufficientFunds", "OrderNotFound",
    "NetworkError", "SubscriptionLimitExceeded",
    "TimeoutError",
    "ConfigError", "BrokerAPIError",
]
