"""Rebalancer domain models."""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, field_validator, model_validator

from tooja.core.models import OrderRequest, Symbol
from tooja.core.money import Money

_WEIGHT_TOLERANCE = Decimal("0.001")


class TargetWeight(BaseModel):
    symbol: Symbol
    weight: Decimal


class TargetSpec(BaseModel):
    """A node in a target allocation tree: a leaf (symbol) or a group (children).

    weight is relative within its sibling group (normalized on flatten).
    Accepts ticker strings (parsed via Symbol.parse) and numeric weights
    (int/float/str -> Decimal) for ergonomic config / dict input.
    """

    weight: Decimal
    symbol: Symbol | None = None
    children: list["TargetSpec"] | None = None

    @field_validator("weight", mode="before")
    @classmethod
    def _coerce_weight(cls, v: object) -> Decimal:
        if isinstance(v, Decimal):
            return v
        return Decimal(str(v))  # exact: avoids float-repr error

    @field_validator("symbol", mode="before")
    @classmethod
    def _parse_symbol(cls, v: object) -> object:
        if isinstance(v, str):
            return Symbol.parse(v)
        return v

    @model_validator(mode="after")
    def _exactly_one(self) -> "TargetSpec":
        if (self.symbol is None) == (self.children is None):
            raise ValueError("TargetSpec needs exactly one of symbol / children")
        if self.weight <= 0:
            raise ValueError("weight must be positive")
        return self


TargetSpec.model_rebuild()


class ExpectedHolding(BaseModel):
    """Post-trade expected position, for plan inspection.

    price/value are bare Decimal (not Money): the rebalancer is single-currency
    and RebalancePlan.expected_cash carries the currency for the whole plan.
    """
    symbol: Symbol
    qty: Decimal
    price: Decimal
    value: Decimal


class RebalancePlan(BaseModel):
    orders: list[OrderRequest]
    expected_drift: Decimal
    expected_holdings: list[ExpectedHolding] = []
    expected_cash: Money | None = None
