"""ABC subclient default behavior — same pattern for all 7 subclients, unified via parametrize."""

from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal

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
from tooja.core.enums import Currency, OrderSide, RankingType
from tooja.core.errors import UnsupportedOperation
from tooja.core.money import Money
from tooja.core.models import MarketOrder, Quote, Symbol


def _stub(cls):
    """Stub for the given ABC client subclass — overrides no methods."""
    sub = type("_Stub", (cls,), {"__init__": lambda self: setattr(self, "_broker_name", "stub")})
    return sub()


# ─── default raise: identical pattern across every subclient -> parametrize ──
@pytest.mark.asyncio
@pytest.mark.parametrize("cls,invoke", [
    (MarketClient, lambda c: c.get_quote("005930")),
    (MarketClient, lambda c: c.get_ohlcv("005930", interval="1d")),
    (AccountClient, lambda c: c.get_balance()),
    (OrdersClient, lambda c: c.create(
        MarketOrder(symbol=Symbol(ticker="005930"), side=OrderSide.BUY, qty=Decimal("10"))
    )),
    (InfoClient, lambda c: c.get_financials("005930")),
    (InfoClient, lambda c: c.list_halts(on_date=date(2026, 1, 1))),
    (AnalyticsClient, lambda c: c.investor_flows(
        "005930", since=date(2026, 1, 1), until=date(2026, 6, 1)
    )),
    (RankingsClient, lambda c: c.get(RankingType.VOLUME)),
])
async def test_async_method_default_raises_with_broker_name(cls, invoke):
    """ABC method defaults raise UnsupportedOperation while preserving the broker name."""
    inst = _stub(cls)
    with pytest.raises(UnsupportedOperation) as ei:
        await invoke(inst)
    assert ei.value.broker == "stub"


def test_stream_sync_method_default_raises():
    """Stream entry points (quotes / trades / orderbook ...) are synchronous and
    return an async iterator, but the default raises immediately on call."""
    with pytest.raises(UnsupportedOperation):
        _stub(StreamClient).quotes(["005930"])


# ─── async generator: call-time vs iteration-time raise ──
@pytest.mark.asyncio
async def test_iter_method_is_async_generator_raises_on_iteration():
    """iter_orders/iter_fills are async generators — call returns the generator;
    the first __anext__ raises."""
    orders = _stub(OrdersClient)
    gen = orders.iter_orders()  # Calling does not raise.
    with pytest.raises(UnsupportedOperation):
        async for _ in gen:
            pass


# ─── overriding bypasses the default ──
@pytest.mark.asyncio
async def test_overriding_bypasses_default():
    class _M(MarketClient):
        def __init__(self): self._broker_name = "stub"
        async def get_quote(self, symbol):
            return Quote(
                symbol=Symbol(ticker="005930"),
                price=Money(amount=Decimal("70000"), currency=Currency.KRW),
                time=datetime(2026, 6, 1, tzinfo=timezone.utc),
            )

    q = await _M().get_quote("005930")
    assert q.price.currency is Currency.KRW
