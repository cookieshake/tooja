"""Rebalancer domain models."""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel

from tooja.core.models import OrderRequest, Symbol
from tooja.core.money import Money

_WEIGHT_TOLERANCE = Decimal("0.001")


class TargetWeight(BaseModel):
    symbol: Symbol
    weight: Decimal


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
