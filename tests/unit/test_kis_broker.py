import httpx
import pytest

from tooja.brokers.kis.broker import KisBroker
from tooja.brokers.kis.account import KisAccountClient
from tooja.brokers.kis.analytics import KisAnalyticsClient
from tooja.brokers.kis.info import KisInfoClient
from tooja.brokers.kis.market import KisMarketClient
from tooja.brokers.kis.orders import KisOrdersClient
from tooja.brokers.kis.rankings import KisRankingsClient
from tooja.brokers.kis.raw_namespace import KisRawNamespace
from tooja.brokers.kis.stream import KisStreamClient
from tooja.core.broker import Broker
from tooja.core.errors import BrokerError


def _kwargs(**override):
    base = dict(
        app_key="K", app_secret="S", cano="12345678", hts_id="H",
    )
    base.update(override)
    return base


def test_subclass_of_broker_abc():
    assert issubclass(KisBroker, Broker)


def test_broker_name_is_kis():
    assert KisBroker.broker_name == "kis"


def test_construct_with_explicit_credentials():
    b = KisBroker(**_kwargs(env="real"))
    assert b.credentials.app_key == "K"
    assert b.is_virtual is False


def test_construct_demo_sets_is_virtual_true():
    b = KisBroker(**_kwargs(env="demo"))
    assert b.is_virtual is True


def test_missing_required_credentials_raises_type_error():
    """Missing required args (app_key, ...) raise Python TypeError (explicitness)."""
    with pytest.raises(TypeError):
        KisBroker(env="real")  # type: ignore[call-arg]


def test_acnt_prdt_cd_defaults_to_01():
    b = KisBroker(**_kwargs())
    assert b.credentials.acnt_prdt_cd == "01"


def test_subclients_attached_with_correct_types():
    b = KisBroker(**_kwargs())
    assert isinstance(b.market, KisMarketClient)
    assert isinstance(b.account, KisAccountClient)
    assert isinstance(b.orders, KisOrdersClient)
    assert isinstance(b.info, KisInfoClient)
    assert isinstance(b.analytics, KisAnalyticsClient)
    assert isinstance(b.rankings, KisRankingsClient)
    assert isinstance(b.stream, KisStreamClient)


def test_raw_namespace_attached():
    b = KisBroker(**_kwargs())
    assert isinstance(b.raw, KisRawNamespace)


def test_default_rate_limit_per_sec():
    assert KisBroker(**_kwargs(env="real")).rate_limit_per_sec == 20
    assert KisBroker(**_kwargs(env="demo")).rate_limit_per_sec == 2


@pytest.mark.asyncio
async def test_open_close_idempotent():
    b = KisBroker(**_kwargs(env="real"))
    await b.open()
    await b.open()  # no error
    assert b.is_open
    await b.close()
    await b.close()  # no error
    assert not b.is_open


@pytest.mark.asyncio
async def test_async_with_works():
    async with KisBroker(**_kwargs(env="real")) as client:
        assert client.is_open
    assert not client.is_open


def test_http_access_before_open_raises():
    b = KisBroker(**_kwargs(env="real"))
    with pytest.raises(BrokerError, match="not opened"):
        _ = b.http


def test_require_open_helper_raises_before_open():
    b = KisBroker(**_kwargs(env="real"))
    with pytest.raises(BrokerError, match="not opened"):
        b._require_open()


@pytest.mark.asyncio
async def test_http_access_after_open_returns_client():
    b = KisBroker(**_kwargs(env="real"))
    await b.open()
    try:
        assert isinstance(b.http, httpx.AsyncClient)
    finally:
        await b.close()


@pytest.mark.asyncio
async def test_open_close_open_cycle_recreates_internal_session():
    b = KisBroker(**_kwargs(env="real"))
    await b.open()
    first_http = b._http
    assert first_http is not None
    await b.close()
    assert b._http is None
    await b.open()
    second_http = b._http
    assert second_http is not None
    assert second_http is not first_http
    await b.close()


def test_http_access_after_close_raises():
    b = KisBroker(**_kwargs(env="real"))
    import asyncio
    asyncio.run(b.open())
    asyncio.run(b.close())
    with pytest.raises(BrokerError, match="not opened"):
        _ = b.http


@pytest.mark.asyncio
async def test_close_releases_http_even_when_open_failed_midway():
    """If open() raises mid-way leaving _open=False but _http set, close() still cleans up without leaking."""
    b = KisBroker(**_kwargs(env="real"))
    # Reproduce a scenario where open() failed during e.g. token issuance:
    #   - _http was created
    #   - _open stayed False
    b._http = httpx.AsyncClient(base_url=b.base_url)
    assert b._open is False
    assert b._http is not None

    await b.close()
    assert b._http is None  # internal http released
    assert b._open is False
