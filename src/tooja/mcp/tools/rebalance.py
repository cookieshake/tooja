"""Portfolio rebalance tools: plan (read) and execute (write, two-phase confirm)."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any

from tooja.core.errors import BrokerError
from tooja.core.models import Symbol
from tooja.mcp._serialize import to_json
from tooja.mcp.errors import format_broker_error, preview, rejection
from tooja.portfolio.rebalance.models import TargetWeight
from tooja.portfolio.rebalance.rebalancer import Rebalancer

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP

    from tooja.mcp.confirm import ConfirmGate
    from tooja.mcp.registry import Registry


def _targets(raw: list[dict[str, str]]) -> list[TargetWeight]:
    return [
        TargetWeight(symbol=Symbol.parse(t["symbol"]), weight=Decimal(t["weight"]))
        for t in raw
    ]


def _trades_payload(computed: Any) -> list[dict[str, str]]:
    return [
        {"symbol": str(t.symbol), "side": t.side.value, "qty": str(t.qty)}
        for t in computed.trades
    ]


async def plan(reg: "Registry", account: str | None, targets: list[dict[str, str]]) -> Any:
    broker = reg.resolve(account).broker
    try:
        rb = Rebalancer(broker, _targets(targets))
        return to_json(await rb.compute_plan())
    except BrokerError as exc:
        return format_broker_error(exc)
    except (ValueError, TypeError, ArithmeticError, KeyError) as exc:
        return {"error": type(exc).__name__, "message": str(exc)}


async def execute(
    reg: "Registry",
    gate: "ConfirmGate",
    account: str | None,
    targets: list[dict[str, str]],
    confirm_token: str | None = None,
) -> Any:
    acc = reg.resolve(account)
    if not acc.trading:
        return rejection("trading_disabled", account=acc.name)
    try:
        rb = Rebalancer(acc.broker, _targets(targets))
        computed = await rb.compute_plan()
    except BrokerError as exc:
        return format_broker_error(exc)
    except (ValueError, TypeError, ArithmeticError, KeyError) as exc:
        return {"error": type(exc).__name__, "message": str(exc)}

    payload = {"tool": "rebalance_execute", "trades": _trades_payload(computed)}
    details = {"plan": to_json(computed)}
    if confirm_token is None or not gate.verify(acc.name, payload, confirm_token):
        return preview(acc.name, "rebalance_execute", details, gate.issue(acc.name, payload))
    try:
        orders = await rb.execute(computed)
        return {"status": "executed", "orders": to_json(orders)}
    except BrokerError as exc:
        return format_broker_error(exc)


def register_read_only(mcp: "FastMCP", registry: "Registry") -> None:
    @mcp.tool()
    async def rebalance_plan(
        targets: list[dict[str, str]], account: str | None = None
    ) -> Any:
        """Compute a rebalance plan (no execution). targets: [{symbol, weight}]."""
        return await plan(registry, account, targets)


def register(mcp: "FastMCP", registry: "Registry", gate: "ConfirmGate") -> None:
    register_read_only(mcp, registry)

    @mcp.tool()
    async def rebalance_execute(
        targets: list[dict[str, str]],
        confirm_token: str | None = None,
        account: str | None = None,
    ) -> Any:
        """Execute a rebalance. Two-phase: first call previews the plan + returns
        confirm_token; call again with it to submit. A drifted plan invalidates the token."""
        return await execute(registry, gate, account, targets, confirm_token)
