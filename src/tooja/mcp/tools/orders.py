# src/tooja/mcp/tools/orders.py
"""Order read tools + write tools (trading opt-in, two-phase confirm, value cap)."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from tooja.core.enums import Currency, OrderSide, TimeInForce
from tooja.core.errors import BrokerError
from tooja.core.models import LimitOrder, MarketOrder, OrderRequest, Symbol
from tooja.core.money import Money
from tooja.mcp._serialize import to_json
from tooja.mcp.errors import format_broker_error, preview, rejection

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP

    from tooja.mcp.confirm import ConfirmGate
    from tooja.mcp.registry import Account, Registry


# ── read ────────────────────────────────────────────
def _opt_date(s: str | None) -> date | None:
    return date.fromisoformat(s) if s else None


async def list_orders(
    reg: "Registry", account: str | None, status: str = "all",
    symbol: str | None = None, since: str | None = None, until: str | None = None,
) -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(
            await broker.orders.list_orders(
                status=status, symbol=symbol,  # type: ignore[arg-type]
                since=_opt_date(since), until=_opt_date(until),
            )
        )
    except BrokerError as exc:
        return format_broker_error(exc)


async def get_order(reg: "Registry", account: str | None, order_id: str) -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(await broker.orders.get(order_id))
    except BrokerError as exc:
        return format_broker_error(exc)


async def list_fills(
    reg: "Registry", account: str | None, symbol: str | None = None,
    since: str | None = None, until: str | None = None,
) -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(
            await broker.orders.list_fills(
                symbol=symbol, since=_opt_date(since), until=_opt_date(until)
            )
        )
    except BrokerError as exc:
        return format_broker_error(exc)


# ── write helpers ───────────────────────────────────
async def _estimate_value(acc: "Account", symbol: str, qty: Decimal, price: Money | None) -> Money:
    if price is not None:
        return price * qty
    quote = await acc.broker.market.get_quote(symbol)
    return quote.price * qty


def _cap_rejection(acc: "Account", estimate: Money) -> dict[str, Any] | None:
    if acc.max_order_value is not None and estimate.amount > acc.max_order_value:
        return rejection(
            "max_order_value_exceeded",
            account=acc.name,
            limit=str(acc.max_order_value),
            estimated=str(estimate.amount),
        )
    return None


# ── create ──────────────────────────────────────────
async def create(
    reg: "Registry", gate: "ConfirmGate", account: str | None, *,
    symbol: str, side: str, qty: str, type: str = "market",
    price: str | None = None, currency: str = "KRW", tif: str = "DAY",
    confirm_token: str | None = None,
) -> Any:
    acc = reg.resolve(account)
    if not acc.trading:
        return rejection("trading_disabled", account=acc.name)

    qty_d = Decimal(qty)
    price_money = (
        Money(amount=Decimal(price), currency=Currency(currency))
        if (type == "limit" and price is not None)
        else None
    )
    payload = {
        "tool": "orders_create", "symbol": symbol, "side": side, "qty": qty,
        "type": type, "price": price, "currency": currency, "tif": tif,
    }
    try:
        estimate = await _estimate_value(acc, symbol, qty_d, price_money)
    except BrokerError as exc:
        return format_broker_error(exc)

    capped = _cap_rejection(acc, estimate)
    if capped is not None:
        return capped

    details = {
        "symbol": symbol, "side": side, "qty": qty, "type": type,
        "price": to_json(price_money), "estimated_value": to_json(estimate),
    }
    if confirm_token is None or not gate.verify(acc.name, payload, confirm_token):
        return preview(acc.name, "orders_create", details, gate.issue(acc.name, payload))

    sym = Symbol.parse(symbol)
    order_side = OrderSide(side)
    req: OrderRequest
    if type == "limit":
        assert price_money is not None
        req = LimitOrder(symbol=sym, side=order_side, qty=qty_d,
                         price=price_money, time_in_force=TimeInForce(tif))
    else:
        req = MarketOrder(symbol=sym, side=order_side, qty=qty_d)
    try:
        order = await acc.broker.orders.create(req)
        return {"status": "executed", "order": to_json(order)}
    except BrokerError as exc:
        return format_broker_error(exc)


# ── cancel ──────────────────────────────────────────
async def cancel(
    reg: "Registry", gate: "ConfirmGate", account: str | None, *,
    order_id: str, confirm_token: str | None = None,
) -> Any:
    acc = reg.resolve(account)
    if not acc.trading:
        return rejection("trading_disabled", account=acc.name)
    payload = {"tool": "orders_cancel", "order_id": order_id}
    details = {"order_id": order_id}
    if confirm_token is None or not gate.verify(acc.name, payload, confirm_token):
        return preview(acc.name, "orders_cancel", details, gate.issue(acc.name, payload))
    try:
        order = await acc.broker.orders.cancel(order_id)
        return {"status": "executed", "order": to_json(order)}
    except BrokerError as exc:
        return format_broker_error(exc)


# ── replace ─────────────────────────────────────────
async def replace(
    reg: "Registry", gate: "ConfirmGate", account: str | None, *,
    order_id: str, qty: str | None = None, price: str | None = None,
    confirm_token: str | None = None,
) -> Any:
    acc = reg.resolve(account)
    if not acc.trading:
        return rejection("trading_disabled", account=acc.name)
    payload = {"tool": "orders_replace", "order_id": order_id, "qty": qty, "price": price}
    details = {"order_id": order_id, "new_qty": qty, "new_price": price}
    if confirm_token is None or not gate.verify(acc.name, payload, confirm_token):
        return preview(acc.name, "orders_replace", details, gate.issue(acc.name, payload))
    try:
        order = await acc.broker.orders.replace(
            order_id,
            qty=Decimal(qty) if qty is not None else None,
            price=Decimal(price) if price is not None else None,
        )
        return {"status": "executed", "order": to_json(order)}
    except BrokerError as exc:
        return format_broker_error(exc)


# ── registration ────────────────────────────────────
def register_read_only(mcp: "FastMCP", registry: "Registry") -> None:
    @mcp.tool()
    async def orders_list(
        status: str = "all", symbol: str | None = None, since: str | None = None,
        until: str | None = None, account: str | None = None,
    ) -> Any:
        """List orders. status one of all/open/closed."""
        return await list_orders(registry, account, status, symbol, since, until)

    @mcp.tool()
    async def orders_get(order_id: str, account: str | None = None) -> Any:
        """Fetch a single order by id."""
        return await get_order(registry, account, order_id)

    @mcp.tool()
    async def orders_list_fills(
        symbol: str | None = None, since: str | None = None,
        until: str | None = None, account: str | None = None,
    ) -> Any:
        """List fills (executions)."""
        return await list_fills(registry, account, symbol, since, until)


def register(mcp: "FastMCP", registry: "Registry", gate: "ConfirmGate") -> None:
    register_read_only(mcp, registry)

    @mcp.tool()
    async def orders_create(
        symbol: str, side: str, qty: str, type: str = "market",
        price: str | None = None, currency: str = "KRW", tif: str = "DAY",
        confirm_token: str | None = None, account: str | None = None,
    ) -> Any:
        """Place an order. Two-phase: first call previews + returns confirm_token;
        call again with confirm_token to execute. side buy/sell; type market/limit."""
        return await create(
            registry, gate, account, symbol=symbol, side=side, qty=qty, type=type,
            price=price, currency=currency, tif=tif, confirm_token=confirm_token,
        )

    @mcp.tool()
    async def orders_cancel(
        order_id: str, confirm_token: str | None = None, account: str | None = None
    ) -> Any:
        """Cancel an order. Two-phase confirm (see orders_create)."""
        return await cancel(
            registry, gate, account, order_id=order_id, confirm_token=confirm_token
        )

    @mcp.tool()
    async def orders_replace(
        order_id: str, qty: str | None = None, price: str | None = None,
        confirm_token: str | None = None, account: str | None = None,
    ) -> Any:
        """Replace an order's qty/price. Two-phase confirm (see orders_create)."""
        return await replace(
            registry, gate, account, order_id=order_id, qty=qty, price=price,
            confirm_token=confirm_token,
        )
