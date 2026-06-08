# tests/unit/test_imports.py
def test_core_top_level_exports():
    import tooja.core as c
    expected = {
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
    }
    actual = set(c.__all__)
    missing = expected - actual
    extra = actual - expected
    assert not missing, f"missing exports: {missing}"
    assert not extra, f"unexpected exports in __all__: {extra}"
    # also detect duplicates in __all__
    assert len(c.__all__) == len(actual), f"duplicate entries in __all__: {c.__all__}"


def test_all_exports_actually_resolve():
    """Every name in __all__ must actually be importable from tooja.core."""
    import tooja.core as c
    for name in c.__all__:
        assert hasattr(c, name), f"{name} listed in __all__ but not accessible"


def test_kis_top_level_exports():
    import tooja.brokers.kis as k
    assert "KisBroker" in k.__all__
    from tooja.brokers.kis import KisBroker
    assert KisBroker.broker_name == "kis"


def test_existing_raw_layer_still_importable():
    """Verify the raw layer still imports cleanly — this plan does not touch raw/."""
    from tooja.brokers.kis.raw.oauth.tokenp import TokenpExecutor, TokenpRequest
    from tooja.brokers.kis.raw.domestic_stock_quotations.inquire_price import (
        InquirePriceExecutor,
        InquirePriceRequest,
    )
    assert TokenpExecutor.PATH == "/oauth2/tokenP"
    assert InquirePriceRequest.__name__ == "InquirePriceRequest"


def test_no_circular_imports():
    """Import every major module in one shot."""
    import tooja.core
    import tooja.core.broker
    import tooja.core.clients
    import tooja.core.enums
    import tooja.core.errors
    import tooja.core.models
    import tooja.core.stream
    import tooja.brokers.kis
    import tooja.brokers.kis.broker
    import tooja.brokers.kis.credentials
    import tooja.brokers.kis.mapping
    import tooja.brokers.kis.raw_namespace
    import tooja.portfolio
    import tooja.portfolio.rebalance


