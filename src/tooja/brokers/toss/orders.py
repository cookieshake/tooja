"""Toss Orders subclient — create / get / cancel / replace / list.

Toss has no stop orders and no fills endpoint, and does not support listing
closed orders (the API returns ``400 closed-not-supported``). Those map to
``UnsupportedOperation``; ``list_fills`` / ``iter_fills`` stay as the ABC
defaults.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, AsyncIterator, Literal

from tooja.brokers.toss._call import call
from tooja.brokers.toss._mappers import order_from_toss
from tooja.brokers.toss.raw.order.cancel_order import CancelOrderExecutor
from tooja.brokers.toss.raw.order.create_order import CreateOrderExecutor
from tooja.brokers.toss.raw.order.modify_order import ModifyOrderExecutor
from tooja.brokers.toss.raw.order_history.get_order import GetOrderExecutor
from tooja.brokers.toss.raw.order_history.get_orders import GetOrdersExecutor
from tooja.core.clients import OrdersClient
from tooja.core.enums import OrderStatus
from tooja.core.errors import UnsupportedOperation
from tooja.core.models import Order, OrderRequest, Symbol

if TYPE_CHECKING:
    from tooja.brokers.toss.broker import TossBroker

# Guard against a runaway pagination loop (Toss caps page size at 100; OPEN
# always returns a single page with hasNext=false, but be defensive).
_MAX_PAGES = 50

# getOrders `status` query enum is {"OPEN", "CLOSED"}; our ABC "open" → "OPEN".
_OPEN_STATUS = "OPEN"


def _as_symbol(symbol: Symbol | str) -> Symbol:
    return Symbol.parse(symbol) if isinstance(symbol, str) else symbol


def _iso(value: date | datetime) -> str:
    return value.isoformat()


class TossOrdersClient(OrdersClient):
    _broker_name = "toss"

    def __init__(self, broker: "TossBroker") -> None:
        self._broker = broker

    # ------------------------------------------------------------------
    # create
    # ------------------------------------------------------------------

    async def create(self, req: OrderRequest) -> Order:
        if req.type == "stop_limit":
            raise UnsupportedOperation("toss has no stop orders", broker="toss")

        body: dict = {
            "symbol": req.symbol.ticker,
            "side": req.side.value.upper(),
            "orderType": "MARKET" if req.type == "market" else "LIMIT",
            "quantity": str(req.qty),
        }
        if req.type == "limit":
            body["price"] = str(req.price.amount)

        resp = await call(self._broker, CreateOrderExecutor, body=body)

        # Toss create returns only the (client) order id. The returned Order
        # reflects the *accepted* request as PENDING; call get() for live state.
        return Order(
            order_id=resp.order_id,
            symbol=req.symbol,
            side=req.side,
            qty=req.qty,
            type=req.type,
            price=getattr(req, "price", None),
            status=OrderStatus.PENDING,
            submitted_at=datetime.now(timezone.utc),
            client_order_id=resp.client_order_id,
            raw=resp.model_dump(by_alias=True),
        )

    # ------------------------------------------------------------------
    # get
    # ------------------------------------------------------------------

    async def get(self, order_id: str) -> Order:
        resp = await call(
            self._broker, GetOrderExecutor, path_params={"orderId": order_id}
        )
        return order_from_toss(resp)

    # ------------------------------------------------------------------
    # cancel
    # ------------------------------------------------------------------

    async def cancel(self, order_id: str) -> Order:
        # Cancel issues a NEW order id; fetch it to reflect real post-cancel state.
        resp = await call(
            self._broker,
            CancelOrderExecutor,
            path_params={"orderId": order_id},
            body={},
        )
        return await self.get(resp.order_id)

    # ------------------------------------------------------------------
    # replace
    # ------------------------------------------------------------------

    async def replace(
        self,
        order_id: str,
        *,
        qty: Decimal | None = None,
        price: Decimal | None = None,
    ) -> Order:
        """Modify an existing order's quantity and/or price.

        Note: assumes the order is a LIMIT order (only price/quantity-modifiable
        orders are limit orders on Toss); ``orderType=LIMIT`` is sent on modify.
        """
        # OrderModifyRequest requires `orderType`; quantity/price are optional.
        # A price implies a LIMIT modify; otherwise default to LIMIT (Toss
        # rejects MARKET modify with a price and KR market orders aren't modified
        # by price). We keep the existing order type's most common case (LIMIT).
        body: dict = {"orderType": "LIMIT"}
        if qty is not None:
            body["quantity"] = str(qty)
        if price is not None:
            body["price"] = str(price)

        resp = await call(
            self._broker,
            ModifyOrderExecutor,
            path_params={"orderId": order_id},
            body=body,
        )
        return await self.get(resp.order_id)

    # ------------------------------------------------------------------
    # list_orders
    # ------------------------------------------------------------------

    async def list_orders(
        self,
        *,
        status: Literal["all", "open", "closed"] = "all",
        symbol: Symbol | str | None = None,
        since: date | datetime | None = None,
        until: date | datetime | None = None,
    ) -> list[Order]:
        if status == "closed":
            raise UnsupportedOperation(
                "toss does not support closed order listing", broker="toss"
            )

        base_query: dict = {}
        if status == "open":
            base_query["status"] = _OPEN_STATUS
        if symbol is not None:
            base_query["symbol"] = _as_symbol(symbol).ticker
        if since is not None:
            base_query["from"] = _iso(since)
        if until is not None:
            base_query["to"] = _iso(until)

        collected: list = []
        cursor: str | None = None
        for _ in range(_MAX_PAGES):
            query = dict(base_query)
            if cursor is not None:
                query["cursor"] = cursor
            resp = await call(self._broker, GetOrdersExecutor, query=query)
            collected.extend(resp.orders)
            if not resp.has_next or not resp.next_cursor:
                break
            cursor = resp.next_cursor

        return [order_from_toss(o) for o in collected]

    # ------------------------------------------------------------------
    # iter_orders
    # ------------------------------------------------------------------

    async def iter_orders(self, **kwargs) -> AsyncIterator[Order]:
        for order in await self.list_orders(**kwargs):
            yield order
