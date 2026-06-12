"""KIS overseas order routing: TR matrix, create/cancel/replace, queries."""

from __future__ import annotations

import pytest

from tooja.brokers.kis import orders as orders_mod
from tooja.core.enums import Exchange, OrderSide

US = (Exchange.NASD, Exchange.NYSE, Exchange.AMEX)


@pytest.mark.parametrize("exchange", US)
def test_us_order_tr_ids(exchange):
    assert orders_mod._ovrs_order_tr_id(exchange, OrderSide.BUY, False) == "TTTT1002U"
    assert orders_mod._ovrs_order_tr_id(exchange, OrderSide.SELL, False) == "TTTT1006U"
    assert orders_mod._ovrs_order_tr_id(exchange, OrderSide.BUY, True) == "VTTT1002U"
    # KIS asymmetry: US demo sell is VTTT1001U, NOT VTTT1006U.
    assert orders_mod._ovrs_order_tr_id(exchange, OrderSide.SELL, True) == "VTTT1001U"


@pytest.mark.parametrize(
    ("exchange", "buy_real", "sell_real"),
    [
        (Exchange.TKSE, "TTTS0308U", "TTTS0307U"),
        (Exchange.SHAA, "TTTS0202U", "TTTS1005U"),
        (Exchange.SEHK, "TTTS1002U", "TTTS1001U"),
        (Exchange.SZAA, "TTTS0305U", "TTTS0304U"),
        (Exchange.HASE, "TTTS0311U", "TTTS0310U"),
        (Exchange.VNSE, "TTTS0311U", "TTTS0310U"),
    ],
)
def test_asia_order_tr_ids(exchange, buy_real, sell_real):
    assert orders_mod._ovrs_order_tr_id(exchange, OrderSide.BUY, False) == buy_real
    assert orders_mod._ovrs_order_tr_id(exchange, OrderSide.SELL, False) == sell_real
    assert orders_mod._ovrs_order_tr_id(exchange, OrderSide.BUY, True) == "V" + buy_real[1:]
    assert orders_mod._ovrs_order_tr_id(exchange, OrderSide.SELL, True) == "V" + sell_real[1:]


@pytest.mark.parametrize(
    ("exchange", "real"),
    [
        (Exchange.NASD, "TTTT1004U"), (Exchange.NYSE, "TTTT1004U"),
        (Exchange.AMEX, "TTTT1004U"), (Exchange.SEHK, "TTTS1003U"),
        (Exchange.TKSE, "TTTS0309U"), (Exchange.SHAA, "TTTS0302U"),
        (Exchange.SZAA, "TTTS0306U"), (Exchange.HASE, "TTTS0312U"),
        (Exchange.VNSE, "TTTS0312U"),
    ],
)
def test_rvsecncl_tr_ids(exchange, real):
    assert orders_mod._ovrs_rvsecncl_tr_id(exchange, False) == real
    assert orders_mod._ovrs_rvsecncl_tr_id(exchange, True) == "V" + real[1:]


def test_is_overseas_predicate():
    assert not orders_mod._is_overseas(Exchange.KRX)
    assert not orders_mod._is_overseas(Exchange.NXT)
    for ex in (Exchange.NASD, Exchange.NYSE, Exchange.AMEX, Exchange.SEHK,
               Exchange.SHAA, Exchange.SZAA, Exchange.TKSE, Exchange.HASE,
               Exchange.VNSE):
        assert orders_mod._is_overseas(ex)


# ─── create() routing ────────────────────────────────

from decimal import Decimal
from types import SimpleNamespace

from tooja.brokers.kis.broker import KisBroker
from tooja.core.enums import Currency, OrderStatus
from tooja.core.errors import UnsupportedOperation
from tooja.core.models import LimitOrder, MarketOrder, Symbol
from tooja.core.money import Money


def _broker(env="real"):
    return KisBroker(app_key="K", app_secret="S", cano="12345678",
                     hts_id="H", env=env)


def _capture_call(monkeypatch, output):
    calls = []

    async def fake_call(broker, executor_cls, request, *, tr_id=None,
                        extra_headers=None):
        calls.append(SimpleNamespace(executor=executor_cls, request=request,
                                     tr_id=tr_id))
        return SimpleNamespace(output=output)

    monkeypatch.setattr(orders_mod, "call", fake_call)
    return calls


def _ovrs_create_head():
    # Overseas order response: output is a single object, not a list.
    return SimpleNamespace(KRX_FWDG_ORD_ORGNO="02711", ODNO="0030089601",
                           ORD_TMD="213000")


@pytest.mark.asyncio
async def test_create_overseas_buy_routes_to_overseas_endpoint(monkeypatch):
    calls = _capture_call(monkeypatch, _ovrs_create_head())
    client = orders_mod.KisOrdersClient(_broker())
    order = await client.create(LimitOrder(
        symbol=Symbol.parse("NASD:AAPL"), side=OrderSide.BUY,
        qty=Decimal(2), price=Money(amount=Decimal("145.00"),
                                    currency=Currency.USD),
    ))
    (c,) = calls
    assert c.executor.PATH == "/uapi/overseas-stock/v1/trading/order"
    assert c.tr_id == "TTTT1002U"
    assert c.request.OVRS_EXCG_CD == "NASD"
    assert c.request.PDNO == "AAPL"
    assert c.request.ORD_QTY == "2"
    assert c.request.OVRS_ORD_UNPR == "145.00"
    assert c.request.ORD_DVSN == "00"
    assert c.request.SLL_TYPE is None          # buy: omitted
    assert c.request.ORD_SVR_DVSN_CD == "0"
    assert order.order_id == "0030089601"
    assert order.status is OrderStatus.OPEN
    assert order.symbol == Symbol.parse("NASD:AAPL")


@pytest.mark.asyncio
async def test_create_overseas_sell_sets_sll_type_and_demo_tr(monkeypatch):
    calls = _capture_call(monkeypatch, _ovrs_create_head())
    client = orders_mod.KisOrdersClient(_broker(env="demo"))
    await client.create(LimitOrder(
        symbol=Symbol.parse("NASD:AAPL"), side=OrderSide.SELL,
        qty=Decimal(1), price=Money(amount=Decimal("150.10"),
                                    currency=Currency.USD),
    ))
    (c,) = calls
    assert c.tr_id == "VTTT1001U"   # US demo sell asymmetry
    assert c.request.SLL_TYPE == "00"


@pytest.mark.asyncio
async def test_create_overseas_market_order_unsupported(monkeypatch):
    _capture_call(monkeypatch, _ovrs_create_head())
    client = orders_mod.KisOrdersClient(_broker())
    with pytest.raises(UnsupportedOperation):
        await client.create(MarketOrder(
            symbol=Symbol.parse("NASD:AAPL"), side=OrderSide.BUY,
            qty=Decimal(1),
        ))


@pytest.mark.asyncio
async def test_create_overseas_rejects_currency_mismatch(monkeypatch):
    _capture_call(monkeypatch, _ovrs_create_head())
    client = orders_mod.KisOrdersClient(_broker())
    with pytest.raises(ValueError, match="currency"):
        await client.create(LimitOrder(
            symbol=Symbol.parse("NASD:AAPL"), side=OrderSide.BUY,
            qty=Decimal(1), price=Money(amount=Decimal(70000),
                                        currency=Currency.KRW),
        ))


@pytest.mark.asyncio
async def test_create_domestic_still_routes_to_order_cash(monkeypatch):
    head = SimpleNamespace(KRX_FWDG_ORD_ORGNO="06010", ODNO="0000117057",
                           ORD_TMD="093000")
    calls = _capture_call(monkeypatch, [head])   # domestic output is a list
    client = orders_mod.KisOrdersClient(_broker())
    await client.create(LimitOrder(
        symbol=Symbol.parse("005930"), side=OrderSide.BUY,
        qty=Decimal(1), price=Money(amount=Decimal(70000),
                                    currency=Currency.KRW),
    ))
    (c,) = calls
    assert c.executor.PATH.endswith("/order-cash")
    assert c.tr_id == "TTTC0012U"
