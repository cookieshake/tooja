"""Market data read tools."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from tooja.core.errors import BrokerError
from tooja.mcp._serialize import to_json
from tooja.mcp.errors import format_broker_error

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP

    from tooja.mcp.registry import Registry

_Interval = Literal["1m", "5m", "15m", "30m", "1h", "1d", "1w", "1M"]


async def get_quote(reg: "Registry", account: str | None, symbol: str) -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(await broker.market.get_quote(symbol))
    except BrokerError as exc:
        return format_broker_error(exc)
    except (ValueError, ArithmeticError, KeyError) as exc:
        return {"error": type(exc).__name__, "message": str(exc)}


async def get_quotes(reg: "Registry", account: str | None, symbols: list[str]) -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(await broker.market.get_quotes(list(symbols)))
    except BrokerError as exc:
        return format_broker_error(exc)
    except (ValueError, ArithmeticError, KeyError) as exc:
        return {"error": type(exc).__name__, "message": str(exc)}


async def get_ohlcv(
    reg: "Registry",
    account: str | None,
    symbol: str,
    interval: _Interval,
    start: str | None = None,
    end: str | None = None,
    limit: int | None = None,
) -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(
            await broker.market.get_ohlcv(
                symbol, interval=interval, start=start, end=end, limit=limit
            )
        )
    except BrokerError as exc:
        return format_broker_error(exc)
    except (ValueError, ArithmeticError, KeyError) as exc:
        return {"error": type(exc).__name__, "message": str(exc)}


async def get_orderbook(
    reg: "Registry", account: str | None, symbol: str, depth: int = 10
) -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(await broker.market.get_orderbook(symbol, depth=depth))
    except BrokerError as exc:
        return format_broker_error(exc)
    except (ValueError, ArithmeticError, KeyError) as exc:
        return {"error": type(exc).__name__, "message": str(exc)}


def register(mcp: "FastMCP", registry: "Registry") -> None:
    @mcp.tool()
    async def market_get_quote(symbol: str, account: str | None = None) -> Any:
        """Current quote for a symbol (e.g. "005930" or "NASD:AAPL")."""
        return await get_quote(registry, account, symbol)

    @mcp.tool()
    async def market_get_quotes(symbols: list[str], account: str | None = None) -> Any:
        """Current quotes for multiple symbols."""
        return await get_quotes(registry, account, symbols)

    @mcp.tool()
    async def market_get_ohlcv(
        symbol: str,
        interval: _Interval,
        start: str | None = None,
        end: str | None = None,
        limit: int | None = None,
        account: str | None = None,
    ) -> Any:
        """OHLCV candles. interval e.g. "1d", "1h", "5m"."""
        return await get_ohlcv(registry, account, symbol, interval, start, end, limit)

    @mcp.tool()
    async def market_get_orderbook(
        symbol: str, depth: int = 10, account: str | None = None
    ) -> Any:
        """Order book (bid/ask levels) for a symbol."""
        return await get_orderbook(registry, account, symbol, depth)
