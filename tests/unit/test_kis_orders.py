"""Unit tests for orders.create/cancel/replace — verify TR_ID routing,
payload construction, and response mapping. Network calls are stubbed.
"""

from __future__ import annotations

from decimal import Decimal
from types import SimpleNamespace

import pytest

from tooja.brokers.kis.broker import KisBroker
from tooja.brokers.kis.orders import (
    _TR_BUY_DEMO, _TR_BUY_REAL, _TR_SELL_DEMO, _TR_SELL_REAL,
    KisOrdersClient, _order_tr_id,
)
from tooja.core.enums import Currency, OrderSide, OrderStatus
from tooja.core.models import LimitOrder, MarketOrder, Symbol
from tooja.core.money import Money


def _broker(env="real"):
    return KisBroker(
        app_key="K", app_secret="S", cano="12345678", hts_id="H", env=env,
    )


def test_tr_id_routing_real_buy():
    assert _order_tr_id(OrderSide.BUY, is_virtual=False) == _TR_BUY_REAL


def test_tr_id_routing_real_sell():
    assert _order_tr_id(OrderSide.SELL, is_virtual=False) == _TR_SELL_REAL


def test_tr_id_routing_demo_buy():
    assert _order_tr_id(OrderSide.BUY, is_virtual=True) == _TR_BUY_DEMO


def test_tr_id_routing_demo_sell():
    assert _order_tr_id(OrderSide.SELL, is_virtual=True) == _TR_SELL_DEMO


@pytest.mark.asyncio
async def test_create_passes_buy_tr_id_and_builds_payload(monkeypatch):
    from tooja.brokers.kis import orders as orders_mod

    received: dict = {}

    async def fake_call(broker, executor_cls, request, *, tr_id=None, extra_headers=None):
        received["tr_id"] = tr_id
        received["request"] = request
        return SimpleNamespace(output=[SimpleNamespace(
            ODNO="0000000123", KRX_FWDG_ORD_ORGNO="01577", ORD_TMD="143000",
        )])

    monkeypatch.setattr(orders_mod, "call", fake_call)

    broker = _broker(env="real")
    await broker.open()
    try:
        client = KisOrdersClient(broker)
        req = LimitOrder(
            symbol=Symbol(ticker="005930"),
            side=OrderSide.BUY,
            qty=Decimal("10"),
            price=Money(amount=Decimal("70000"), currency=Currency.KRW),
        )
        order = await client.create(req)
    finally:
        await broker.close()

    assert received["tr_id"] == _TR_BUY_REAL
    raw = received["request"]
    assert raw.PDNO == "005930"
    assert raw.ORD_DVSN == "00"  # limit
    assert raw.ORD_QTY == "10"
    assert raw.ORD_UNPR == "70000"
    assert order.order_id == "0000000123"
    assert order.status is OrderStatus.OPEN
    assert order.raw["krx_fwdg_ord_orgno"] == "01577"


@pytest.mark.asyncio
async def test_create_market_order_uses_dvsn_01(monkeypatch):
    from tooja.brokers.kis import orders as orders_mod

    captured = {}

    async def fake_call(broker, executor_cls, request, *, tr_id=None, extra_headers=None):
        captured["request"] = request
        return SimpleNamespace(output=[SimpleNamespace(
            ODNO="0000000456", KRX_FWDG_ORD_ORGNO=None, ORD_TMD=None,
        )])

    monkeypatch.setattr(orders_mod, "call", fake_call)

    broker = _broker(env="demo")
    await broker.open()
    try:
        client = KisOrdersClient(broker)
        req = MarketOrder(
            symbol=Symbol(ticker="005930"),
            side=OrderSide.SELL,
            qty=Decimal("5"),
        )
        await client.create(req)
    finally:
        await broker.close()

    assert captured["request"].ORD_DVSN == "01"
    assert captured["request"].ORD_UNPR == "0"


@pytest.mark.asyncio
async def test_create_rejected_when_response_has_no_odno(monkeypatch):
    from tooja.brokers.kis import orders as orders_mod
    from tooja.core.errors import OrderRejected

    async def fake_call(broker, executor_cls, request, *, tr_id=None, extra_headers=None):
        return SimpleNamespace(output=[])

    monkeypatch.setattr(orders_mod, "call", fake_call)

    broker = _broker(env="real")
    await broker.open()
    try:
        client = KisOrdersClient(broker)
        req = MarketOrder(
            symbol=Symbol(ticker="005930"),
            side=OrderSide.BUY,
            qty=Decimal("1"),
        )
        with pytest.raises(OrderRejected):
            await client.create(req)
    finally:
        await broker.close()
