"""Account read tools."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from tooja.core.enums import Currency
from tooja.core.errors import BrokerError
from tooja.mcp._serialize import to_json
from tooja.mcp.errors import format_broker_error

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP

    from tooja.mcp.registry import Registry


async def get_balance(reg: "Registry", account: str | None) -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(await broker.account.get_balance())
    except BrokerError as exc:
        return format_broker_error(exc)


async def get_positions(reg: "Registry", account: str | None) -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(await broker.account.get_positions())
    except BrokerError as exc:
        return format_broker_error(exc)


async def get_buying_power(reg: "Registry", account: str | None, currency: str = "KRW") -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(await broker.account.get_buying_power(currency=Currency(currency)))
    except BrokerError as exc:
        return format_broker_error(exc)


async def get_sellable_quantity(reg: "Registry", account: str | None, symbol: str) -> Any:
    broker = reg.resolve(account).broker
    try:
        qty = await broker.account.get_sellable_quantity(symbol)
        return {"symbol": symbol, "quantity": str(qty)}
    except BrokerError as exc:
        return format_broker_error(exc)


def register(mcp: "FastMCP", registry: "Registry") -> None:
    @mcp.tool()
    async def account_get_balance(account: str | None = None) -> Any:
        """Account balance: cash (gross + orderable) and positions."""
        return await get_balance(registry, account)

    @mcp.tool()
    async def account_get_positions(account: str | None = None) -> Any:
        """Held positions for the account."""
        return await get_positions(registry, account)

    @mcp.tool()
    async def account_get_buying_power(
        currency: str = "KRW", account: str | None = None
    ) -> Any:
        """Buying power in the given currency (KRW/USD/HKD/CNY/JPY/VND)."""
        return await get_buying_power(registry, account, currency)

    @mcp.tool()
    async def account_get_sellable_quantity(
        symbol: str, account: str | None = None
    ) -> Any:
        """Sellable quantity for a held symbol."""
        return await get_sellable_quantity(registry, account, symbol)
