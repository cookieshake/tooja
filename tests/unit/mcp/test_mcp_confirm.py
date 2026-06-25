from tooja.mcp.confirm import ConfirmGate


def test_issue_then_verify_roundtrip():
    g = ConfirmGate(secret=b"x" * 32)
    payload = {"symbol": "005930", "side": "buy", "qty": "10"}
    tok = g.issue("main", payload)
    assert g.verify("main", payload, tok) is True


def test_tampered_payload_rejected():
    g = ConfirmGate(secret=b"x" * 32)
    tok = g.issue("main", {"qty": "10"})
    assert g.verify("main", {"qty": "11"}, tok) is False


def test_swapped_account_rejected():
    g = ConfirmGate(secret=b"x" * 32)
    tok = g.issue("main", {"qty": "10"})
    assert g.verify("pension", {"qty": "10"}, tok) is False


def test_expired_token_rejected():
    clock = {"t": 1000.0}
    g = ConfirmGate(secret=b"x" * 32, ttl=60.0, now=lambda: clock["t"])
    tok = g.issue("main", {"qty": "10"})
    clock["t"] = 1100.0
    assert g.verify("main", {"qty": "10"}, tok) is False


def test_malformed_token_rejected():
    g = ConfirmGate(secret=b"x" * 32)
    assert g.verify("main", {"qty": "10"}, "garbage") is False
