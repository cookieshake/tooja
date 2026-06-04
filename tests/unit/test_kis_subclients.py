"""Smoke test that the 7 KIS subclient skeleton classes import + instantiate."""
import pytest

from tooja.core.clients import (
    AccountClient,
    AnalyticsClient,
    InfoClient,
    MarketClient,
    OrdersClient,
    RankingsClient,
    StreamClient,
)
from tooja.core.errors import UnsupportedOperation


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


@pytest.mark.asyncio
async def test_default_methods_still_raise_unsupported():
    """Skeleton — no method overrides — calling get_quote should still raise."""
    from tooja.brokers.kis.market import KisMarketClient

    # Pass a dummy broker (skeleton doesn't dereference it)
    m = KisMarketClient(broker=None)
    with pytest.raises(UnsupportedOperation) as ei:
        await m.get_quote("005930")
    assert ei.value.broker == "kis"
