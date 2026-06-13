"""Rebalancer domain models."""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel

from tooja.core.enums import OrderSide
from tooja.core.models import Symbol
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


class PlannedTrade(BaseModel):
    """Broker-neutral trade intent: *what* to trade, not *how* to submit.

    Order type and price selection happen at execute() time, where venue
    constraints are known (e.g. KIS overseas is limit-only in the regular
    session).
    """

    symbol: Symbol
    side: OrderSide
    qty: Decimal


class RebalancePlan(BaseModel):
    trades: list[PlannedTrade]
    expected_drift: Decimal
    expected_holdings: list[ExpectedHolding] = []
    expected_cash: Money | None = None
    expected_total: Money | None = None
