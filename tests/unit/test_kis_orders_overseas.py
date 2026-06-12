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


# ─── cancel / replace routing ────────────────────────

from datetime import datetime, timezone

from tooja.core.models import Order


def _ovrs_order(qty="5", filled="2", price="145.00"):
    return Order(
        order_id="0030089601",
        symbol=Symbol.parse("NASD:AAPL"),
        side=OrderSide.BUY,
        qty=Decimal(qty), filled_qty=Decimal(filled),
        type="limit",
        price=Money(amount=Decimal(price), currency=Currency.USD),
        status=OrderStatus.PARTIALLY_FILLED,
        submitted_at=datetime(2026, 6, 12, 1, 0, tzinfo=timezone.utc),
        raw={},
    )


def _patch_get(monkeypatch, order):
    async def fake_get(self, order_id):
        assert order_id == order.order_id
        return order

    monkeypatch.setattr(orders_mod.KisOrdersClient, "get", fake_get)


@pytest.mark.asyncio
async def test_cancel_overseas_sends_remaining_qty(monkeypatch):
    order = _ovrs_order(qty="5", filled="2")
    _patch_get(monkeypatch, order)
    calls = _capture_call(monkeypatch, _ovrs_create_head())
    client = orders_mod.KisOrdersClient(_broker())

    result = await client.cancel(order.order_id)

    (c,) = calls
    assert c.executor.PATH == "/uapi/overseas-stock/v1/trading/order-rvsecncl"
    assert c.tr_id == "TTTT1004U"
    assert c.request.OVRS_EXCG_CD == "NASD"
    assert c.request.PDNO == "AAPL"
    assert c.request.ORGN_ODNO == order.order_id
    assert c.request.RVSE_CNCL_DVSN_CD == "02"
    assert c.request.ORD_QTY == "3"            # 5 ordered - 2 filled
    assert c.request.OVRS_ORD_UNPR == "0"      # cancel sends "0"
    assert result.status is OrderStatus.CANCELLED


@pytest.mark.asyncio
async def test_replace_overseas_sends_new_price(monkeypatch):
    order = _ovrs_order()
    _patch_get(monkeypatch, order)
    calls = _capture_call(monkeypatch, _ovrs_create_head())
    client = orders_mod.KisOrdersClient(_broker())

    result = await client.replace(order.order_id, price=Decimal("150.50"))

    (c,) = calls
    assert c.request.RVSE_CNCL_DVSN_CD == "01"
    assert c.request.ORD_QTY == "5"
    assert c.request.OVRS_ORD_UNPR == "150.50"
    assert result.price.amount == Decimal("150.50")
    assert result.status is OrderStatus.OPEN


# ─── get / list_orders / list_fills fan-out ──────────

from tooja.core.errors import PermissionDenied


def _ovrs_ccnl_row(**over):
    base = dict(
        ord_dt="20260611", odno="OVRS1", orgn_odno=None,
        sll_buy_dvsn_cd="02", rvse_cncl_dvsn=None,
        pdno="AAPL", ft_ord_qty="5", ft_ord_unpr3="145.00",
        ft_ccld_qty="2", ft_ccld_unpr3="144.90", nccs_qty="3",
        prcs_stat_name="완료", rjct_rson="", ord_tmd="221500",
        ovrs_excg_cd="NASD", tr_crcy_cd="USD",
        dmst_ord_dt="20260612", thco_ord_tmd="071500",
    )
    base.update(over)
    ns = SimpleNamespace(**base)
    ns.model_dump = lambda: dict(base)
    return ns


def _patch_iter(monkeypatch, *, domestic_rows=(), ovrs_rows=(),
                ovrs_exc=None):
    async def fake_dom(self, **kw):
        return list(domestic_rows)

    async def fake_ovrs(self, **kw):
        if ovrs_exc is not None:
            raise ovrs_exc
        return list(ovrs_rows)

    monkeypatch.setattr(orders_mod.KisOrdersClient, "_iter_ccld", fake_dom)
    monkeypatch.setattr(
        orders_mod.KisOrdersClient, "_iter_ovrs_ccnl", fake_ovrs,
    )


@pytest.mark.asyncio
async def test_list_orders_merges_domestic_and_overseas(monkeypatch):
    _patch_iter(monkeypatch, domestic_rows=[], ovrs_rows=[_ovrs_ccnl_row()])
    client = orders_mod.KisOrdersClient(_broker())
    orders = await client.list_orders()
    assert [o.order_id for o in orders] == ["OVRS1"]
    assert orders[0].symbol.exchange is Exchange.NASD


@pytest.mark.asyncio
async def test_list_orders_degrades_when_overseas_not_enrolled(monkeypatch):
    _patch_iter(
        monkeypatch, domestic_rows=[],
        ovrs_exc=PermissionDenied("not enrolled", broker="kis"),
    )
    client = orders_mod.KisOrdersClient(_broker())
    assert await client.list_orders() == []


@pytest.mark.asyncio
async def test_list_orders_explicit_overseas_symbol_propagates_denied(monkeypatch):
    _patch_iter(
        monkeypatch, ovrs_exc=PermissionDenied("not enrolled", broker="kis"),
    )
    client = orders_mod.KisOrdersClient(_broker())
    with pytest.raises(PermissionDenied):
        await client.list_orders(symbol="NASD:AAPL")


@pytest.mark.asyncio
async def test_list_orders_overseas_symbol_filters_client_side(monkeypatch):
    _patch_iter(monkeypatch, ovrs_rows=[
        _ovrs_ccnl_row(), _ovrs_ccnl_row(odno="OVRS2", pdno="TSLA"),
    ])
    client = orders_mod.KisOrdersClient(_broker())
    orders = await client.list_orders(symbol="NASD:AAPL")
    assert [o.order_id for o in orders] == ["OVRS1"]


@pytest.mark.asyncio
async def test_list_fills_includes_overseas(monkeypatch):
    _patch_iter(monkeypatch, ovrs_rows=[_ovrs_ccnl_row()])
    client = orders_mod.KisOrdersClient(_broker())
    fills = await client.list_fills()
    assert len(fills) == 1
    assert fills[0].price.currency is Currency.USD


@pytest.mark.asyncio
async def test_get_finds_overseas_order(monkeypatch):
    _patch_iter(monkeypatch, ovrs_rows=[_ovrs_ccnl_row()])
    client = orders_mod.KisOrdersClient(_broker())
    order = await client.get("OVRS1")
    assert order.order_id == "OVRS1"


@pytest.mark.asyncio
async def test_iter_ovrs_ccnl_demo_sends_wildcards(monkeypatch):
    captured = []

    async def fake_call(broker, executor_cls, request, *, tr_id=None,
                        extra_headers=None):
        captured.append(request)
        return SimpleNamespace(
            output=[], headers=SimpleNamespace(tr_cont=""),
            ctx_area_fk200="", ctx_area_nk200="",
        )

    monkeypatch.setattr(orders_mod, "call", fake_call)
    client = orders_mod.KisOrdersClient(_broker(env="demo"))
    await client._iter_ovrs_ccnl(
        symbol=Symbol.parse("NASD:AAPL"), since=None, until=None,
        status="open", only_filled=False,
    )
    (req,) = captured
    assert req.PDNO == ""             # demo: server-side filters not allowed
    assert req.OVRS_EXCG_CD == "%"
    assert req.CCLD_NCCS_DVSN == "00"
    assert req.SLL_BUY_DVSN == "00"


@pytest.mark.asyncio
async def test_iter_ovrs_ccnl_real_sends_filters(monkeypatch):
    captured = []

    async def fake_call(broker, executor_cls, request, *, tr_id=None,
                        extra_headers=None):
        captured.append(request)
        return SimpleNamespace(
            output=[], headers=SimpleNamespace(tr_cont=""),
            ctx_area_fk200="", ctx_area_nk200="",
        )

    monkeypatch.setattr(orders_mod, "call", fake_call)
    client = orders_mod.KisOrdersClient(_broker())
    await client._iter_ovrs_ccnl(
        symbol=Symbol.parse("NASD:AAPL"), since=None, until=None,
        status="open", only_filled=False,
    )
    (req,) = captured
    assert req.PDNO == "AAPL"
    assert req.OVRS_EXCG_CD == "NASD"
    assert req.CCLD_NCCS_DVSN == "02"  # open == 미체결
    assert req.SORT_SQN == "DS"
    assert req.ODNO == ""              # spec: must stay empty
