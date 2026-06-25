"""KIS-only market analytics read tools (gated by Registry.has_kis at registration)."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Any

from tooja.core.enums import Exchange
from tooja.core.errors import BrokerError
from tooja.mcp._serialize import to_json
from tooja.mcp.errors import format_broker_error

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP

    from tooja.mcp.registry import Registry


def _d(s: str) -> date:
    return date.fromisoformat(s)


async def investor_flows(
    reg: "Registry", account: str | None, symbol: str, since: str, until: str
) -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(
            await broker.analytics.investor_flows(symbol, since=_d(since), until=_d(until))
        )
    except BrokerError as exc:
        return format_broker_error(exc)


async def program_trading(
    reg: "Registry", account: str | None, symbol_or_market: str, since: str, until: str
) -> Any:
    broker = reg.resolve(account).broker
    target: Any = symbol_or_market
    if symbol_or_market in Exchange.__members__ or symbol_or_market in {
        e.value for e in Exchange
    }:
        target = Exchange(symbol_or_market)
    try:
        return to_json(
            await broker.analytics.program_trading(target, since=_d(since), until=_d(until))
        )
    except BrokerError as exc:
        return format_broker_error(exc)


async def short_selling(
    reg: "Registry", account: str | None, symbol: str, since: str, until: str
) -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(
            await broker.analytics.short_selling(symbol, since=_d(since), until=_d(until))
        )
    except BrokerError as exc:
        return format_broker_error(exc)


async def margin_balance(
    reg: "Registry", account: str | None, symbol: str, since: str, until: str
) -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(
            await broker.analytics.margin_balance(symbol, since=_d(since), until=_d(until))
        )
    except BrokerError as exc:
        return format_broker_error(exc)


async def securities_lending(
    reg: "Registry", account: str | None, symbol: str, since: str, until: str
) -> Any:
    broker = reg.resolve(account).broker
    try:
        return to_json(
            await broker.analytics.securities_lending(symbol, since=_d(since), until=_d(until))
        )
    except BrokerError as exc:
        return format_broker_error(exc)


def register(mcp: "FastMCP", registry: "Registry") -> None:
    @mcp.tool()
    async def analytics_investor_flows(
        symbol: str, since: str, until: str, account: str | None = None
    ) -> Any:
        """Daily investor flows (individual/foreign/institutional net). KIS only."""
        return await investor_flows(registry, account, symbol, since, until)

    @mcp.tool()
    async def analytics_program_trading(
        symbol_or_market: str, since: str, until: str, account: str | None = None
    ) -> Any:
        """Program trading net (symbol or market like KRX). KIS only."""
        return await program_trading(registry, account, symbol_or_market, since, until)

    @mcp.tool()
    async def analytics_short_selling(
        symbol: str, since: str, until: str, account: str | None = None
    ) -> Any:
        """Daily short-selling volume/value. KIS only."""
        return await short_selling(registry, account, symbol, since, until)

    @mcp.tool()
    async def analytics_margin_balance(
        symbol: str, since: str, until: str, account: str | None = None
    ) -> Any:
        """Daily margin/stock-loan balance. KIS only."""
        return await margin_balance(registry, account, symbol, since, until)

    @mcp.tool()
    async def analytics_securities_lending(
        symbol: str, since: str, until: str, account: str | None = None
    ) -> Any:
        """Daily securities-lending balance/new loans. KIS only."""
        return await securities_lending(registry, account, symbol, since, until)
