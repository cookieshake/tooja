"""Market ranking read tool."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from tooja.core.enums import Exchange, RankingType
from tooja.core.errors import BrokerError
from tooja.mcp._serialize import to_json
from tooja.mcp.errors import format_broker_error

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP

    from tooja.mcp.registry import Registry


async def get(
    reg: "Registry", account: str | None, type: str, market: str = "KRX", limit: int = 30
) -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(
            await broker.rankings.get(
                RankingType(type), market=Exchange(market), limit=limit
            )
        )
    except BrokerError as exc:
        return format_broker_error(exc)
    except (ValueError, TypeError, ArithmeticError, KeyError) as exc:
        return {"error": exc.__class__.__name__, "message": str(exc)}


def register(mcp: "FastMCP", registry: "Registry") -> None:
    @mcp.tool()
    async def rankings_get(
        type: str, market: str = "KRX", limit: int = 30, account: str | None = None
    ) -> Any:
        """Ranking rows. type e.g. volume/turnover/up/down/market_cap/foreign_buy."""
        return await get(registry, account, type, market, limit)
