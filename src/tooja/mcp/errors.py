"""Structured MCP tool results for broker errors, rejections, and confirm previews."""

from __future__ import annotations

from typing import Any

from tooja.core.errors import BrokerError


def format_broker_error(exc: BrokerError) -> dict[str, Any]:
    return {
        "error": type(exc).__name__,
        "message": str(exc),
        "broker": exc.broker,
        "raw_code": exc.raw_code,
        "endpoint": exc.endpoint,
    }


def rejection(reason: str, **extra: Any) -> dict[str, Any]:
    return {"status": "rejected", "reason": reason, **extra}


def preview(account: str, action: str, details: dict[str, Any], token: str) -> dict[str, Any]:
    return {
        "status": "needs_confirmation",
        "account": account,
        "action": action,
        "details": details,
        "confirm_token": token,
        "instructions": (
            "This is a preview — no order was placed. To execute exactly this "
            f"order, call {action} again with confirm_token set to the value above. "
            "Any change to the parameters invalidates the token."
        ),
    }
