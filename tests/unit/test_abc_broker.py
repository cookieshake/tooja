import pytest
from typing import ClassVar

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


class _OpenCloseRecord:
    opened = closed = False


def _stub(cls):
    class _S(cls):
        def __init__(self): self._broker_name = "stub"
    return _S


_StubMarket = _stub(MarketClient)
_StubAccount = _stub(AccountClient)
_StubOrders = _stub(OrdersClient)
_StubInfo = _stub(InfoClient)
_StubAnalytics = _stub(AnalyticsClient)
_StubRankings = _stub(RankingsClient)
_StubStream = _stub(StreamClient)


class _StubBroker(Broker):
    broker_name: ClassVar[str] = "stub"

    def __init__(self):
        self._rec = _OpenCloseRecord()
        self.market = _StubMarket()
        self.account = _StubAccount()
        self.orders = _StubOrders()
        self.info = _StubInfo()
        self.analytics = _StubAnalytics()
        self.rankings = _StubRankings()
        self.stream = _StubStream()

    async def open(self):
        self._rec.opened = True

    async def close(self):
        self._rec.closed = True


def test_broker_is_abc_open_close_required():
    """Instantiation must fail when open/close are unimplemented."""
    class _Bad(Broker):
        broker_name: ClassVar[str] = "bad"
    with pytest.raises(TypeError):
        _Bad()  # abstract methods open/close unimplemented


@pytest.mark.asyncio
async def test_async_with_calls_open_close():
    b = _StubBroker()
    async with b as ctx:
        assert ctx is b
        assert b._rec.opened
    assert b._rec.closed


@pytest.mark.asyncio
async def test_open_close_manual():
    b = _StubBroker()
    await b.open()
    assert b._rec.opened
    await b.close()
    assert b._rec.closed


def test_supports_method_not_overridden():
    b = _StubBroker()
    # _StubMarket does not override get_quote -> default still in place.
    assert b.supports("market.get_quote") is False


def test_supports_method_overridden():
    class _M(MarketClient):
        def __init__(self): self._broker_name = "stub"
        async def get_quote(self, symbol):
            return None

    class _B(_StubBroker):
        def __init__(self):
            super().__init__()
            self.market = _M()

    assert _B().supports("market.get_quote") is True


def test_supports_invalid_method_returns_false():
    b = _StubBroker()
    assert b.supports("garbage.method") is False
    assert b.supports("market.no_such_method") is False
    assert b.supports("no_dot_format") is False


def test_supports_rejects_non_client_attribute():
    """Domains that are not subclient ABCs (e.g. broker_name str methods) return False."""
    b = _StubBroker()
    # broker_name is a str; str.upper exists on its dict but must not match supports().
    assert b.supports("broker_name.upper") is False
    assert b.supports("broker_name.startswith") is False


def test_supports_rejects_dunder_and_internal():
    """Dunder / internal attributes not defined on the ABC base return False (domain methods only)."""
    b = _StubBroker()
    # __init__ / __doc__ / __class__ are dunders, not ABC-base domain methods.
    assert b.supports("market.__init__") is False
    assert b.supports("market.__class__") is False
    # _broker_name is an instance attribute, not in the ABC dict.
    assert b.supports("market._broker_name") is False
    # A real domain method that has NOT been overridden — the name is valid, so False means "not overridden".
    assert b.supports("market.get_quote") is False


def test_supports_inherited_override():
    """Subclass that inherits an override from its parent → still supports() == True."""
    class _M1(MarketClient):
        def __init__(self): self._broker_name = "stub"
        async def get_quote(self, symbol):
            return None

    class _M2(_M1):
        # Inherits get_quote; should still be reported as supported.
        pass

    class _B(_StubBroker):
        def __init__(self):
            super().__init__()
            self.market = _M2()

    assert _B().supports("market.get_quote") is True


@pytest.mark.asyncio
async def test_open_close_idempotent_on_repeated_calls():
    """open()/close() docstring promises idempotency — repeated calls must not error."""
    b = _StubBroker()
    await b.open()
    await b.open()  # second call — should not error
    assert b._rec.opened
    await b.close()
    await b.close()  # second call — should not error
    assert b._rec.closed
