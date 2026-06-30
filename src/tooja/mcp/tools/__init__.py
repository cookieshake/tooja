"""MCP tool registration. register_all wires every domain's tools onto the server."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP

    from tooja.mcp.confirm import ConfirmGate
    from tooja.mcp.registry import Registry


def register_all(mcp: "FastMCP", registry: "Registry", gate: "ConfirmGate") -> None:
    from tooja.mcp.tools import (
        account,
        analytics,
        info,
        market,
        orders,
        rankings,
        rebalance,
    )

    market.register(mcp, registry)
    account.register(mcp, registry)
    info.register(mcp, registry)
    rankings.register(mcp, registry)
    if registry.has_kis:
        analytics.register(mcp, registry)
    if registry.has_trading:
        orders.register(mcp, registry, gate)
        rebalance.register(mcp, registry, gate)
    else:
        orders.register_read_only(mcp, registry)
        rebalance.register_read_only(mcp, registry)
