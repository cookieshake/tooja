"""Assemble the FastMCP server: registry + confirm gate + tool registration + lifespan."""

from __future__ import annotations

from collections.abc import Callable
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from tooja.mcp.config import AccountConfig, McpConfig
from tooja.mcp.confirm import ConfirmGate
from tooja.mcp.registry import Registry, build_registry
from tooja.mcp.tools import register_all

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP

    from tooja.core.broker import Broker


def build_server(
    config: McpConfig,
    *,
    broker_factory: "Callable[[AccountConfig], Broker] | None" = None,
) -> "tuple[FastMCP, Registry]":
    from mcp.server.fastmcp import FastMCP

    registry = (
        build_registry(config, broker_factory=broker_factory)
        if broker_factory is not None
        else build_registry(config)
    )
    gate = ConfirmGate()

    @asynccontextmanager
    async def lifespan(_server: "FastMCP"):  # type: ignore[misc]
        for acc in registry.all():
            await acc.broker.open()
        try:
            yield {}
        finally:
            await registry.aclose()

    mcp = FastMCP(name="tooja", lifespan=lifespan)
    register_all(mcp, registry, gate)
    return mcp, registry


def main() -> None:
    import os

    from tooja.mcp.config import load_config

    config = load_config(os.environ)
    mcp, _ = build_server(config)
    mcp.run()
