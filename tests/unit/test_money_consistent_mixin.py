"""Validate the _MoneyConsistent mixin once, instead of repeating it across 13 models."""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

import pytest
from pydantic import ValidationError

from tooja.core.enums import Currency
from tooja.core.money import Money
from tooja.core.models import _MoneyConsistent


def _krw(amount: int | str) -> Money:
    return Money(amount=Decimal(amount), currency=Currency.KRW)


def _usd(amount: int | str) -> Money:
    return Money(amount=Decimal(amount), currency=Currency.USD)


class _Sample(_MoneyConsistent):
    """Single-currency check target — two flat monetary fields."""

    _money_fields: ClassVar[tuple[str, ...]] = ("a", "b")
    a: Money
    b: Money | None = None


def test_mixin_accepts_single_currency():
    s = _Sample(a=_krw(100), b=_krw(200))
    assert s.a == _krw(100)


def test_mixin_accepts_none_optional():
    s = _Sample(a=_krw(100))
    assert s.b is None


def test_mixin_rejects_mixed_currencies():
    with pytest.raises(ValidationError, match="inconsistent currencies"):
        _Sample(a=_krw(100), b=_usd("50.00"))


def test_mixin_empty_money_fields_no_check():
    """Models without _money_fields perform no check — default behavior."""

    class _Empty(_MoneyConsistent):
        x: int = 0

    assert _Empty(x=5).x == 5


def test_mixin_message_contains_model_name():
    with pytest.raises(ValidationError, match="_Sample"):
        _Sample(a=_krw(100), b=_usd("50.00"))
