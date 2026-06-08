"""Unit tests for the Toss orders subclient.

The subclient module's ``call`` is monkeypatched with a ``fake_call`` returning
the generated RESPONSE_TYPE instance. No network / broker internals exercised.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

import tooja.brokers.toss.orders as orders_mod
from tooja.brokers.toss.orders import TossOrdersClient
from tooja.brokers.toss.raw.order.cancel_order import CancelOrderExecutor
from tooja.brokers.toss.raw.order.create_order import CreateOrderExecutor
from tooja.brokers.toss.raw.order.modify_order import ModifyOrderExecutor
from tooja.brokers.toss.raw.order_history.get_order import GetOrderExecutor
from tooja.brokers.toss.raw.order_history.get_orders import GetOrdersExecutor
from tooja.brokers.toss.raw.models import (
    Order as TossOrder,
    OrderOperationResponse,
    OrderResponse,
    PaginatedOrderResponse,
)
from tooja.core.enums import Currency, Exchange, OrderSide, OrderStatus
from tooja.core.errors import UnsupportedOperation
from tooja.core.models import LimitOrder, MarketOrder, StopLimitOrder, Symbol
from tooja.core.money import Money


def _client() -> TossOrdersClient:
    return TossOrdersClient(broker=object())


def _toss_order_json(order_id: str = "ord-1", status: str = "FILLED") -> dict:
    return {
        "orderId": order_id,
        "symbol": "005930",
        "side": "BUY",
        "orderType": "LIMIT",
        "timeInForce": "DAY",
        "status": status,
        "price": "70000",
        "quantity": "10",
        "orderAmount": None,
        "currency": "KRW",
        "orderedAt": "2026-06-08T10:30:00+09:00",
        "canceledAt": None,
        "execution": {
            "filledQuantity": "10",
            "averageFilledPrice": "70000",
            "filledAmount": "700000",
        },
    }


# ── create ──────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_create_limit_body_shape_and_returns_pending_order(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["executor_cls"] = executor_cls
        captured["body"] = body
        return OrderResponse.model_validate({"orderId": "ord-99", "clientOrderId": "cli-7"})

    monkeypatch.setattr(orders_mod, "call", fake_call)

    req = LimitOrder(
        symbol=Symbol(ticker="005930", exchange=Exchange.KRX),
        side=OrderSide.BUY,
        qty=Decimal(10),
        price=Money(amount=Decimal(70000), currency=Currency.KRW),
    )
    order = await _client().create(req)

    assert captured["executor_cls"] is CreateOrderExecutor
    assert captured["body"] == {
        "symbol": "005930",
        "side": "BUY",
        "orderType": "LIMIT",
        "quantity": "10",
        "price": "70000",
    }
    assert order.order_id == "ord-99"
    assert order.status is OrderStatus.PENDING
    assert order.side is OrderSide.BUY
    assert order.qty == Decimal(10)
    assert order.type == "limit"
    assert order.price == Money(amount=Decimal(70000), currency=Currency.KRW)
    assert order.client_order_id == "cli-7"
    assert order.submitted_at is not None


@pytest.mark.asyncio
async def test_create_market_omits_price(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["body"] = body
        return OrderResponse.model_validate({"orderId": "ord-m"})

    monkeypatch.setattr(orders_mod, "call", fake_call)

    req = MarketOrder(
        symbol=Symbol(ticker="005930", exchange=Exchange.KRX),
        side=OrderSide.SELL,
        qty=Decimal(3),
    )
    order = await _client().create(req)

    assert captured["body"] == {
        "symbol": "005930",
        "side": "SELL",
        "orderType": "MARKET",
        "quantity": "3",
    }
    assert "price" not in captured["body"]
    assert order.order_id == "ord-m"
    assert order.type == "market"
    assert order.price is None
    assert order.status is OrderStatus.PENDING


@pytest.mark.asyncio
async def test_create_stop_limit_raises_unsupported(monkeypatch):
    monkeypatch.setattr(orders_mod, "call", None)  # must not be called

    req = StopLimitOrder(
        symbol=Symbol(ticker="005930", exchange=Exchange.KRX),
        side=OrderSide.BUY,
        qty=Decimal(1),
        price=Money(amount=Decimal(70000), currency=Currency.KRW),
        stop_price=Money(amount=Decimal(69000), currency=Currency.KRW),
    )
    with pytest.raises(UnsupportedOperation):
        await _client().create(req)


# ── get ─────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_maps_via_order_from_toss(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["executor_cls"] = executor_cls
        captured["path_params"] = path_params
        return TossOrder.model_validate(_toss_order_json("ord-1", status="FILLED"))

    monkeypatch.setattr(orders_mod, "call", fake_call)

    order = await _client().get("ord-1")

    assert captured["executor_cls"] is GetOrderExecutor
    assert captured["path_params"] == {"orderId": "ord-1"}
    assert order.order_id == "ord-1"
    assert order.status is OrderStatus.FILLED
    assert order.symbol.ticker == "005930"
    assert order.filled_qty == Decimal(10)
    assert order.avg_fill_price == Money(amount=Decimal(70000), currency=Currency.KRW)


# ── cancel ──────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_cancel_calls_cancel_then_get_new_id(monkeypatch):
    calls: list = []

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        calls.append((executor_cls, path_params, body))
        if executor_cls is CancelOrderExecutor:
            return OrderOperationResponse.model_validate({"orderId": "ord-new"})
        if executor_cls is GetOrderExecutor:
            return TossOrder.model_validate(_toss_order_json("ord-new", status="CANCELED"))
        raise AssertionError(f"unexpected executor {executor_cls}")

    monkeypatch.setattr(orders_mod, "call", fake_call)

    order = await _client().cancel("ord-old")

    assert calls[0][0] is CancelOrderExecutor
    assert calls[0][1] == {"orderId": "ord-old"}
    assert calls[0][2] == {}
    assert calls[1][0] is GetOrderExecutor
    assert calls[1][1] == {"orderId": "ord-new"}
    assert order.order_id == "ord-new"
    assert order.status is OrderStatus.CANCELLED


# ── replace ─────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_replace_builds_modify_body_then_gets_new_id(monkeypatch):
    calls: list = []

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        calls.append((executor_cls, path_params, body))
        if executor_cls is ModifyOrderExecutor:
            return OrderOperationResponse.model_validate({"orderId": "ord-rep"})
        if executor_cls is GetOrderExecutor:
            return TossOrder.model_validate(_toss_order_json("ord-rep", status="REPLACED"))
        raise AssertionError(f"unexpected executor {executor_cls}")

    monkeypatch.setattr(orders_mod, "call", fake_call)

    order = await _client().replace("ord-x", qty=Decimal(5), price=Decimal(71000))

    modify = calls[0]
    assert modify[0] is ModifyOrderExecutor
    assert modify[1] == {"orderId": "ord-x"}
    # orderType is required by the spec's OrderModifyRequest
    assert modify[2]["orderType"] == "LIMIT"
    assert modify[2]["quantity"] == "5"
    assert modify[2]["price"] == "71000"
    assert calls[1][0] is GetOrderExecutor
    assert calls[1][1] == {"orderId": "ord-rep"}
    assert order.order_id == "ord-rep"


# ── list_orders ─────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_list_orders_closed_raises_unsupported(monkeypatch):
    monkeypatch.setattr(orders_mod, "call", None)  # must not be called

    with pytest.raises(UnsupportedOperation):
        await _client().list_orders(status="closed")


@pytest.mark.asyncio
async def test_list_orders_open_maps_status_enum(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["executor_cls"] = executor_cls
        captured["query"] = query
        return PaginatedOrderResponse.model_validate({
            "orders": [_toss_order_json("ord-1")],
            "nextCursor": None,
            "hasNext": False,
        })

    monkeypatch.setattr(orders_mod, "call", fake_call)

    orders = await _client().list_orders(status="open")

    assert captured["executor_cls"] is GetOrdersExecutor
    assert captured["query"]["status"] == "OPEN"
    assert len(orders) == 1
    assert orders[0].order_id == "ord-1"


@pytest.mark.asyncio
async def test_list_orders_all_omits_status(monkeypatch):
    captured: dict = {}

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        captured["query"] = query
        return PaginatedOrderResponse.model_validate({
            "orders": [], "nextCursor": None, "hasNext": False,
        })

    monkeypatch.setattr(orders_mod, "call", fake_call)

    await _client().list_orders(status="all", symbol="005930")

    assert "status" not in captured["query"]
    assert captured["query"]["symbol"] == "005930"


@pytest.mark.asyncio
async def test_list_orders_paginates_across_pages(monkeypatch):
    cursors_seen: list = []

    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        cursors_seen.append(query.get("cursor"))
        if query.get("cursor") is None:
            return PaginatedOrderResponse.model_validate({
                "orders": [_toss_order_json("ord-1")],
                "nextCursor": "cur-2",
                "hasNext": True,
            })
        return PaginatedOrderResponse.model_validate({
            "orders": [_toss_order_json("ord-2")],
            "nextCursor": None,
            "hasNext": False,
        })

    monkeypatch.setattr(orders_mod, "call", fake_call)

    orders = await _client().list_orders(status="open")

    assert cursors_seen == [None, "cur-2"]
    assert [o.order_id for o in orders] == ["ord-1", "ord-2"]


@pytest.mark.asyncio
async def test_iter_orders_yields_orders(monkeypatch):
    async def fake_call(broker, executor_cls, *, path_params=None, query=None,
                        body=None, extra_headers=None):
        return PaginatedOrderResponse.model_validate({
            "orders": [_toss_order_json("ord-1"), _toss_order_json("ord-2")],
            "nextCursor": None,
            "hasNext": False,
        })

    monkeypatch.setattr(orders_mod, "call", fake_call)

    ids = [o.order_id async for o in _client().iter_orders(status="open")]
    assert ids == ["ord-1", "ord-2"]
