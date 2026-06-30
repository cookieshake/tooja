from tooja.core.errors import InsufficientFunds
from tooja.mcp.errors import format_broker_error, preview, rejection


def test_format_broker_error():
    exc = InsufficientFunds("nope", broker="kis", raw_code="40310000", endpoint="/x")
    d = format_broker_error(exc)
    assert d["error"] == "InsufficientFunds"
    assert d["broker"] == "kis" and d["raw_code"] == "40310000"
    assert "nope" in d["message"]


def test_rejection():
    d = rejection("trading_disabled", account="pension")
    assert d["status"] == "rejected" and d["reason"] == "trading_disabled"
    assert d["account"] == "pension"


def test_preview_carries_token_and_instructions():
    d = preview("main", "orders_create", {"qty": "10"}, "tok123")
    assert d["status"] == "needs_confirmation"
    assert d["confirm_token"] == "tok123"
    assert "confirm_token" in d["instructions"]
