"""Smoke test that the 7 KIS subclient classes import + instantiate."""

from tooja.core.clients import (
    AccountClient,
    AnalyticsClient,
    InfoClient,
    MarketClient,
    OrdersClient,
    RankingsClient,
    StreamClient,
)


def _all_subclients():
    from tooja.brokers.kis.account import KisAccountClient
    from tooja.brokers.kis.analytics import KisAnalyticsClient
    from tooja.brokers.kis.info import KisInfoClient
    from tooja.brokers.kis.market import KisMarketClient
    from tooja.brokers.kis.orders import KisOrdersClient
    from tooja.brokers.kis.rankings import KisRankingsClient
    from tooja.brokers.kis.stream import KisStreamClient
    return [
        (KisMarketClient, MarketClient),
        (KisAccountClient, AccountClient),
        (KisOrdersClient, OrdersClient),
        (KisInfoClient, InfoClient),
        (KisAnalyticsClient, AnalyticsClient),
        (KisRankingsClient, RankingsClient),
        (KisStreamClient, StreamClient),
    ]


def test_each_subclient_inherits_abc():
    for kis_cls, abc_cls in _all_subclients():
        assert issubclass(kis_cls, abc_cls), f"{kis_cls.__name__} must inherit from {abc_cls.__name__}"


def test_each_subclient_has_kis_broker_name():
    for kis_cls, _ in _all_subclients():
        assert kis_cls._broker_name == "kis"
