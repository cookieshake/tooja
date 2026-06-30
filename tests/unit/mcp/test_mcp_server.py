"""Tests for MCP server assembly."""

from __future__ import annotations

import pytest

from tooja.mcp.config import McpConfig
from tooja.mcp.server import build_server
from tests.unit.mcp.conftest import FakeBroker


def _kis_cfg(trading: bool) -> McpConfig:
    return McpConfig.model_validate(
        {"accounts": {"default": {
            "broker": "kis", "app_key": "k", "app_secret": "s",
            "cano": "1", "hts_id": "h", "trading": trading,
        }}}
    )


@pytest.mark.asyncio
async def test_build_server_registers_read_tools_only_when_no_trading():
    mcp, _ = build_server(_kis_cfg(trading=False), broker_factory=lambda c: FakeBroker("kis"))
    names = {t.name for t in await mcp.list_tools()}
    assert "market_get_quote" in names
    assert "orders_list" in names
    assert "orders_create" not in names  # trading disabled


@pytest.mark.asyncio
async def test_build_server_registers_write_tools_when_trading():
    mcp, _ = build_server(_kis_cfg(trading=True), broker_factory=lambda c: FakeBroker("kis"))
    names = {t.name for t in await mcp.list_tools()}
    assert "orders_create" in names
    assert "rebalance_execute" in names
    assert "analytics_investor_flows" in names  # kis present
