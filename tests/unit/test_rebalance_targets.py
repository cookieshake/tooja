import logging
from decimal import Decimal

import pytest
from pydantic import ValidationError

from tooja.core.models import Symbol
from tooja.portfolio.rebalance import TargetSpec, TargetWeight, flatten_targets, validate_targets


# ---------------------------------------------------------------------------
# 1. Simple two-leaf normalisation via TargetSpec instances
# ---------------------------------------------------------------------------

def test_flatten_targets_simple():
    specs = [
        TargetSpec(weight=1, symbol=Symbol.parse("005930")),
        TargetSpec(weight=3, symbol=Symbol.parse("035720")),
    ]
    targets = flatten_targets(specs)
    by_sym = {t.symbol: t.weight for t in targets}
    assert by_sym[Symbol.parse("005930")] == Decimal("0.25")
    assert by_sym[Symbol.parse("035720")] == Decimal("0.75")


# ---------------------------------------------------------------------------
# 2. Nested TargetSpec: [1 leaf, 3 group[1 leaf, 2 leaf]] -> 0.25 / 0.25 / 0.5
# ---------------------------------------------------------------------------

def test_flatten_targets_nested():
    specs = [
        TargetSpec(weight=1, symbol=Symbol.parse("005930")),
        TargetSpec(
            weight=3,
            children=[
                TargetSpec(weight=1, symbol=Symbol.parse("035720")),
                TargetSpec(weight=2, symbol=Symbol.parse("NASD:AAPL")),
            ],
        ),
    ]
    targets = flatten_targets(specs)
    by_sym = {t.symbol: t.weight for t in targets}
    assert by_sym[Symbol.parse("005930")] == Decimal("0.25")
    assert by_sym[Symbol.parse("035720")] == Decimal("0.25")
    assert by_sym[Symbol.parse("NASD:AAPL")] == Decimal("0.5")


# ---------------------------------------------------------------------------
# 3. Dict input (settings-file style) — coercion & Symbol.parse applied
# ---------------------------------------------------------------------------

def test_flatten_targets_dict_input():
    raw = [
        {"weight": 1, "symbol": "005930"},
        {
            "weight": 3,
            "children": [
                {"weight": 1, "symbol": "035720"},
                {"weight": 2, "symbol": "NASD:AAPL"},
            ],
        },
    ]
    targets = flatten_targets(raw)
    by_sym = {t.symbol: t.weight for t in targets}
    assert by_sym[Symbol.parse("005930")] == Decimal("0.25")
    assert by_sym[Symbol.parse("035720")] == Decimal("0.25")
    # Exchange is parsed correctly from the string
    aapl = Symbol.parse("NASD:AAPL")
    assert by_sym[aapl] == Decimal("0.5")
    assert aapl.exchange.value == "NASD"


# ---------------------------------------------------------------------------
# 4. Invalid: both symbol and children -> ValidationError
# ---------------------------------------------------------------------------

def test_target_spec_both_symbol_and_children_raises():
    with pytest.raises(ValidationError):
        TargetSpec(
            weight=1,
            symbol=Symbol.parse("005930"),
            children=[TargetSpec(weight=1, symbol=Symbol.parse("035720"))],
        )


def test_flatten_targets_dict_both_raises():
    with pytest.raises(ValidationError):
        flatten_targets([
            {"weight": 1, "symbol": "005930", "children": [{"weight": 1, "symbol": "035720"}]}
        ])


# ---------------------------------------------------------------------------
# 5. Invalid: neither symbol nor children -> ValidationError
# ---------------------------------------------------------------------------

def test_target_spec_neither_symbol_nor_children_raises():
    with pytest.raises(ValidationError):
        TargetSpec(weight=1)


def test_flatten_targets_dict_neither_raises():
    with pytest.raises(ValidationError):
        flatten_targets([{"weight": 1}])


# ---------------------------------------------------------------------------
# 6. Invalid: weight <= 0 -> ValidationError
# ---------------------------------------------------------------------------

def test_target_spec_zero_weight_raises():
    with pytest.raises(ValidationError):
        TargetSpec(weight=0, symbol=Symbol.parse("005930"))


def test_target_spec_negative_weight_raises():
    with pytest.raises(ValidationError):
        TargetSpec(weight=-1, symbol=Symbol.parse("005930"))


def test_target_spec_zero_weight_dict_raises():
    with pytest.raises(ValidationError):
        flatten_targets([{"weight": 0, "symbol": "005930"}])


# ---------------------------------------------------------------------------
# 7. validate_targets warns when sum != 1.0
# ---------------------------------------------------------------------------

def test_validate_targets_warns_when_not_one(caplog):
    sym = Symbol.parse("005930")
    with caplog.at_level(logging.WARNING):
        validate_targets([TargetWeight(symbol=sym, weight=Decimal("0.5"))])
    assert any("0.5" in r.message or "50" in r.message for r in caplog.records)


# ---------------------------------------------------------------------------
# 8. Previously-diluting malformed input now RAISES instead of silently dropping
# ---------------------------------------------------------------------------

def test_old_positional_list_format_raises():
    """The old [weight, ticker] format is no longer accepted; it raises ValidationError."""
    with pytest.raises(ValidationError):
        flatten_targets([[1, "005930"], [3, "035720"]])
