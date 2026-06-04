"""Money value object — currency-safe arithmetic with per-currency quantization."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator, model_validator

from tooja.core.enums import Currency

_CURRENCY_QUANTUM: dict[Currency, Decimal] = {
    Currency.KRW: Decimal("1"),
    Currency.USD: Decimal("0.01"),
    Currency.HKD: Decimal("0.01"),
    Currency.CNY: Decimal("0.01"),
    Currency.JPY: Decimal("1"),
    Currency.VND: Decimal("1"),
}


def quantum_for(currency: Currency) -> Decimal:
    return _CURRENCY_QUANTUM[currency]


class CurrencyMismatchError(ValueError):
    """Two Money values have different currencies — arithmetic/comparison disallowed."""


class Money(BaseModel):
    model_config = ConfigDict(frozen=True)

    amount: Decimal
    currency: Currency

    @field_validator("amount", mode="before")
    @classmethod
    def _validate_amount(cls, v: Any, info: ValidationInfo) -> Any:
        """Python input must be Decimal. JSON input may be a string -> Decimal (serialization standard)."""
        if info.mode == "json" and isinstance(v, str):
            return Decimal(v)
        if not isinstance(v, Decimal):
            raise TypeError(
                f"Money.amount must be Decimal (got {type(v).__name__}); "
                "use Decimal('1000') explicitly"
            )
        return v

    @model_validator(mode="after")
    def _quantize(self) -> "Money":
        q = _CURRENCY_QUANTUM[self.currency]
        quantized = self.amount.quantize(q, rounding=ROUND_HALF_UP)
        if quantized != self.amount:
            object.__setattr__(self, "amount", quantized)
        return self

    def __str__(self) -> str:
        return f"{self.amount} {self.currency.value}"

    def _require_same(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                f"currency mismatch: {self.currency.value} vs {other.currency.value}"
            )

    def __add__(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            return NotImplemented
        self._require_same(other)
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            return NotImplemented
        self._require_same(other)
        return Money(amount=self.amount - other.amount, currency=self.currency)

    def __mul__(self, factor: Decimal | int) -> "Money":
        if not isinstance(factor, (Decimal, int)):
            return NotImplemented
        return Money(amount=self.amount * Decimal(factor), currency=self.currency)

    __rmul__ = __mul__

    def __truediv__(self, divisor: Decimal | int) -> "Money":
        if not isinstance(divisor, (Decimal, int)):
            return NotImplemented
        return Money(amount=self.amount / Decimal(divisor), currency=self.currency)

    def __neg__(self) -> "Money":
        return Money(amount=-self.amount, currency=self.currency)

    def __lt__(self, other: "Money") -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        self._require_same(other)
        return self.amount < other.amount

    def __le__(self, other: "Money") -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        self._require_same(other)
        return self.amount <= other.amount

    def __gt__(self, other: "Money") -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        self._require_same(other)
        return self.amount > other.amount

    def __ge__(self, other: "Money") -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        self._require_same(other)
        return self.amount >= other.amount
