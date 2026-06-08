import logging
from decimal import Decimal

from tooja.core.models import Symbol
from tooja.portfolio.rebalance import flatten_targets, validate_targets


def test_flatten_targets_simple():
    targets = flatten_targets([[1, "005930"], [3, "035720"]])
    by_sym = {t.symbol: t.weight for t in targets}
    assert by_sym[Symbol.parse("005930")] == Decimal("0.25")
    assert by_sym[Symbol.parse("035720")] == Decimal("0.75")


def test_flatten_targets_nested_and_exchange():
    targets = flatten_targets([[1, "005930"], [3, [[1, "035720"], [2, "NASD:AAPL"]]]])
    by_sym = {t.symbol: t.weight for t in targets}
    assert by_sym[Symbol.parse("005930")] == Decimal("0.25")
    assert by_sym[Symbol.parse("035720")] == Decimal("0.25")
    assert by_sym[Symbol.parse("NASD:AAPL")] == Decimal("0.5")


def test_flatten_targets_accepts_float_parent_pct():
    # parent_pct as a float must not raise (lenient parser); weights scale correctly.
    targets = flatten_targets([[1, "005930"], [1, "000660"]], 0.5)
    by = {t.symbol: t.weight for t in targets}
    assert by[Symbol.parse("005930")] == Decimal("0.25")
    assert by[Symbol.parse("000660")] == Decimal("0.25")


def test_validate_targets_warns_when_not_one(caplog):
    sym = Symbol.parse("005930")
    from tooja.portfolio.rebalance import TargetWeight
    with caplog.at_level(logging.WARNING):
        validate_targets([TargetWeight(symbol=sym, weight=Decimal("0.5"))])
    assert any("0.5" in r.message or "50" in r.message for r in caplog.records)
