"""Money value object — tests for currency-safe arithmetic + quantization."""

from __future__ import annotations

from decimal import Decimal

import pytest
from pydantic import ValidationError

from tooja.core.enums import Currency
from tooja.core.money import CurrencyMismatchError, Money, quantum_for


# ─── Construction: Decimal only ──────────────────────
def test_create_with_decimal():
    m = Money(amount=Decimal("10.50"), currency=Currency.USD)
    assert m.amount == Decimal("10.50")
    assert m.currency is Currency.USD


@pytest.mark.parametrize("bad", [1000, "10.50", 10.5])
def test_non_decimal_types_rejected(bad):
    """Python input must be Decimal — int / str / float all rejected."""
    with pytest.raises((TypeError, ValidationError)):
        Money(amount=bad, currency=Currency.KRW)  # type: ignore[arg-type]


@pytest.mark.parametrize("bad", [True, False])
def test_bool_rejected_despite_int_subclass(bad):
    """bool is a subclass of int — must be explicitly rejected (Decimal('1')/('0') gotcha)."""
    with pytest.raises((TypeError, ValidationError)):
        Money(amount=bad, currency=Currency.KRW)  # type: ignore[arg-type]


# ─── quantize per currency ───────────────────────────
def test_quantize_krw_rounds_to_integer():
    m = Money(amount=Decimal("1000.789"), currency=Currency.KRW)
    assert m.amount == Decimal("1001")


def test_quantize_usd_two_digits_half_up():
    m = Money(amount=Decimal("10.555"), currency=Currency.USD)
    assert m.amount == Decimal("10.56")


def test_quantize_jpy_integer():
    m = Money(amount=Decimal("100.5"), currency=Currency.JPY)
    assert m.amount == Decimal("101")


def test_quantum_for_lookup():
    assert quantum_for(Currency.KRW) == Decimal("1")
    assert quantum_for(Currency.USD) == Decimal("0.01")
    assert quantum_for(Currency.JPY) == Decimal("1")
    assert quantum_for(Currency.HKD) == Decimal("0.01")
    assert quantum_for(Currency.CNY) == Decimal("0.01")
    assert quantum_for(Currency.VND) == Decimal("1")


# ─── frozen + hashable ───────────────────────────────
def test_frozen():
    m = Money(amount=Decimal("100"), currency=Currency.KRW)
    with pytest.raises(ValidationError):
        m.amount = Decimal("200")  # type: ignore[misc]


def test_equality_and_hash():
    m1 = Money(amount=Decimal("100"), currency=Currency.KRW)
    m2 = Money(amount=Decimal("100"), currency=Currency.KRW)
    m3 = Money(amount=Decimal("100"), currency=Currency.USD)
    assert m1 == m2
    assert hash(m1) == hash(m2)
    assert m1 != m3


# ─── Arithmetic ──────────────────────────────────────
def test_add_same_currency():
    a = Money(amount=Decimal("100"), currency=Currency.KRW)
    b = Money(amount=Decimal("200"), currency=Currency.KRW)
    result = a + b
    assert result.amount == Decimal("300")
    assert result.currency is Currency.KRW


def test_add_currency_mismatch_raises():
    a = Money(amount=Decimal("100"), currency=Currency.KRW)
    b = Money(amount=Decimal("100"), currency=Currency.USD)
    with pytest.raises(CurrencyMismatchError):
        a + b


def test_sub_same_currency():
    a = Money(amount=Decimal("300"), currency=Currency.KRW)
    b = Money(amount=Decimal("100"), currency=Currency.KRW)
    assert (a - b).amount == Decimal("200")


def test_sub_currency_mismatch_raises():
    a = Money(amount=Decimal("100"), currency=Currency.KRW)
    b = Money(amount=Decimal("100"), currency=Currency.USD)
    with pytest.raises(CurrencyMismatchError):
        a - b


def test_mul_by_int():
    a = Money(amount=Decimal("100"), currency=Currency.KRW)
    assert (a * 3).amount == Decimal("300")
    assert (3 * a).amount == Decimal("300")


def test_mul_by_decimal_quantizes():
    a = Money(amount=Decimal("10"), currency=Currency.USD)
    result = a * Decimal("1.5")
    assert result.amount == Decimal("15.00")


def test_truediv_by_int():
    a = Money(amount=Decimal("100"), currency=Currency.KRW)
    assert (a / 4).amount == Decimal("25")


def test_neg():
    a = Money(amount=Decimal("100"), currency=Currency.KRW)
    assert (-a).amount == Decimal("-100")


# ─── Comparison ──────────────────────────────────────
def test_compare_same_currency():
    a = Money(amount=Decimal("100"), currency=Currency.KRW)
    b = Money(amount=Decimal("200"), currency=Currency.KRW)
    assert a < b
    assert b > a
    assert a <= b
    assert b >= a
    assert a <= Money(amount=Decimal("100"), currency=Currency.KRW)


def test_compare_currency_mismatch_raises():
    a = Money(amount=Decimal("100"), currency=Currency.KRW)
    b = Money(amount=Decimal("100"), currency=Currency.USD)
    with pytest.raises(CurrencyMismatchError):
        _ = a < b


# ─── Representation / JSON ───────────────────────────
def test_str_contains_amount_and_currency():
    m = Money(amount=Decimal("1000"), currency=Currency.KRW)
    s = str(m)
    assert "1000" in s
    assert "KRW" in s


def test_json_round_trip():
    m = Money(amount=Decimal("10.50"), currency=Currency.USD)
    payload = m.model_dump_json()
    restored = Money.model_validate_json(payload)
    assert restored == m
    assert restored.amount == Decimal("10.50")
    assert restored.currency is Currency.USD
