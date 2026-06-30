"""Instrument info read tools."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Any

from tooja.core.enums import FinancialPeriod
from tooja.core.errors import BrokerError
from tooja.mcp._serialize import to_json
from tooja.mcp.errors import format_broker_error

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP

    from tooja.mcp.registry import Registry


async def get_stock(reg: "Registry", account: str | None, symbol: str) -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(await broker.info.get_stock(symbol))
    except BrokerError as exc:
        return format_broker_error(exc)
    except (ValueError, TypeError, ArithmeticError, KeyError) as exc:
        return {"error": type(exc).__name__, "message": str(exc)}


async def search(reg: "Registry", account: str | None, query: str) -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(await broker.info.search(query))
    except BrokerError as exc:
        return format_broker_error(exc)
    except (ValueError, TypeError, ArithmeticError, KeyError) as exc:
        return {"error": type(exc).__name__, "message": str(exc)}


async def get_financials(
    reg: "Registry", account: str | None, symbol: str, period: str = "Q", limit: int = 8
) -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(
            await broker.info.get_financials(
                symbol, period=FinancialPeriod(period), limit=limit
            )
        )
    except BrokerError as exc:
        return format_broker_error(exc)
    except (ValueError, TypeError, ArithmeticError, KeyError) as exc:
        return {"error": type(exc).__name__, "message": str(exc)}


async def get_dividends(
    reg: "Registry", account: str | None, symbol: str, since: str | None = None
) -> Any:
    broker = reg.resolve(account).broker
    try:
        since_d = date.fromisoformat(since) if since else None
        return to_json(await broker.info.get_dividends(symbol, since=since_d))
    except BrokerError as exc:
        return format_broker_error(exc)
    except (ValueError, TypeError, ArithmeticError, KeyError) as exc:
        return {"error": type(exc).__name__, "message": str(exc)}


async def get_warnings(reg: "Registry", account: str | None, symbol: str) -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(await broker.info.get_warnings(symbol))
    except BrokerError as exc:
        return format_broker_error(exc)
    except (ValueError, TypeError, ArithmeticError, KeyError) as exc:
        return {"error": type(exc).__name__, "message": str(exc)}


async def is_holiday(reg: "Registry", account: str | None, day: str) -> Any:
    broker = reg.resolve(account).broker
    try:
        result = await broker.info.is_holiday(date.fromisoformat(day))
        return {"date": day, "is_holiday": result}
    except BrokerError as exc:
        return format_broker_error(exc)
    except (ValueError, TypeError, ArithmeticError, KeyError) as exc:
        return {"error": type(exc).__name__, "message": str(exc)}


def register(mcp: "FastMCP", registry: "Registry") -> None:
    @mcp.tool()
    async def info_get_stock(symbol: str, account: str | None = None) -> Any:
        """Stock master info (name, sector, market cap, ...)."""
        return await get_stock(registry, account, symbol)

    @mcp.tool()
    async def info_search(query: str, account: str | None = None) -> Any:
        """Search instruments by name/ticker."""
        return await search(registry, account, query)

    @mcp.tool()
    async def info_get_financials(
        symbol: str, period: str = "Q", limit: int = 8, account: str | None = None
    ) -> Any:
        """Financial summaries. period "Q" (quarterly) or "Y" (annual)."""
        return await get_financials(registry, account, symbol, period, limit)

    @mcp.tool()
    async def info_get_dividends(
        symbol: str, since: str | None = None, account: str | None = None
    ) -> Any:
        """Dividend history. since is an ISO date (YYYY-MM-DD)."""
        return await get_dividends(registry, account, symbol, since)

    @mcp.tool()
    async def info_get_warnings(symbol: str, account: str | None = None) -> Any:
        """Trading caution flags for a symbol."""
        return await get_warnings(registry, account, symbol)

    @mcp.tool()
    async def info_is_holiday(day: str, account: str | None = None) -> Any:
        """Whether an ISO date (YYYY-MM-DD) is a market holiday."""
        return await is_holiday(registry, account, day)
