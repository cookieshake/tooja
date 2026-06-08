"""Rebalancer domain models."""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel

from tooja.core.models import OrderRequest, Symbol

_WEIGHT_TOLERANCE = Decimal("0.001")


class TargetWeight(BaseModel):
    symbol: Symbol
    weight: Decimal


class RebalancePlan(BaseModel):
    orders: list[OrderRequest]
    expected_drift: Decimal
