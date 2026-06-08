"""TossBroker assembly: construction, token_cache wiring, supports(), raw namespace."""

from __future__ import annotations

import asyncio

import pytest

from tooja.brokers.toss import TossBroker
from tooja.brokers.toss.account import TossAccountClient
from tooja.brokers.toss.analytics import TossAnalyticsClient
from tooja.brokers.toss.broker import TossBroker as TossBrokerDirect
from tooja.brokers.toss.info import TossInfoClient
from tooja.brokers.toss.market import TossMarketClient
from tooja.brokers.toss.orders import TossOrdersClient
from tooja.brokers.toss.rankings import TossRankingsClient
from tooja.brokers.toss.raw_namespace import TossRawNamespace
from tooja.brokers.toss.stream import TossStreamClient
from tooja.core.broker import Broker
from tooja.core.errors import BrokerError


def _kwargs(**override):
    base = dict(client_id="cid", client_secret="sec")
    base.update(override)
    return base


def test_subclass_of_broker_abc():
    assert issubclass(TossBroker, Broker)
    assert TossBroker is TossBrokerDirect


def test_broker_name_is_toss():
    assert TossBroker.broker_name == "toss"


def test_construct_without_account_seq():
    b = TossBroker(**_kwargs())
    assert b.credentials.client_id == "cid"
    assert b.account_seq is None


def test_construct_with_account_seq():
    b = TossBroker(**_kwargs(account_seq=42))
    assert b.account_seq == 42


def test_subclients_attached_with_correct_types():
    b = TossBroker(**_kwargs())
    assert isinstance(b.market, TossMarketClient)
    assert isinstance(b.account, TossAccountClient)
    assert isinstance(b.orders, TossOrdersClient)
    assert isinstance(b.info, TossInfoClient)
    assert isinstance(b.analytics, TossAnalyticsClient)
    assert isinstance(b.rankings, TossRankingsClient)
    assert isinstance(b.stream, TossStreamClient)
    assert isinstance(b.raw, TossRawNamespace)


def test_token_cache_forwarded_to_token_manager(tmp_path, monkeypatch):
    import tooja.core.token_cache as tc

    monkeypatch.setattr(tc.platformdirs, "user_cache_dir", lambda *a, **k: str(tmp_path))

    b = TossBroker(**_kwargs(token_cache="memory"))
    asyncio.run(b.open())
    try:
        assert b._tokens is not None
        assert b._tokens._store.mode == "memory"
    finally:
        asyncio.run(b.close())


@pytest.mark.parametrize(
    "method",
    [
        "market.get_quote",
        "market.get_ohlcv",
        "market.get_price_limits",
        "account.get_balance",
        "account.get_buying_power",
        "account.get_sellable_quantity",
        "orders.create",
        "info.get_stock",
        "info.get_warnings",
        "info.is_holiday",
    ],
)
def test_supports_true(method):
    b = TossBroker(**_kwargs())
    assert b.supports(method) is True


@pytest.mark.parametrize(
    "method",
    [
        "analytics.investor_flows",
        "rankings.get",
        "stream.quotes",
        "orders.list_fills",
        "info.list_halts",
    ],
)
def test_supports_false(method):
    b = TossBroker(**_kwargs())
    assert b.supports(method) is False


def test_raw_market_data_exposes_executor():
    b = TossBroker(**_kwargs())
    assert getattr(b.raw.market_data, "GetPricesExecutor") is not None


def test_http_before_open_raises():
    b = TossBroker(**_kwargs())
    with pytest.raises(BrokerError):
        _ = b.http
