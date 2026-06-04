"""Target-weight rebalancer — outline only.

This plan covers types + constructor + weight-sum validation.
The compute_plan() / execute() algorithm bodies live in a separate plan.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Iterable

from pydantic import BaseModel

from tooja.core.broker import Broker
from tooja.core.models import Order, OrderRequest, Symbol  # noqa: F401


_WEIGHT_TOLERANCE = Decimal("0.001")


class TargetWeight(BaseModel):
    symbol: Symbol
    weight: Decimal


class RebalancePlan(BaseModel):
    orders: list[OrderRequest]
    expected_drift: Decimal


class Rebalancer:
    """Depends only on the `Broker` ABC — works against any adapter."""

    def __init__(
        self,
        broker: Broker,
        targets: Iterable[TargetWeight],
        *,
        cash_buffer_rate: Decimal = Decimal("0.02"),
        min_order_value: Decimal = Decimal("10000"),
    ):
        self.broker = broker
        self.targets = list(targets)
        self.cash_buffer_rate = cash_buffer_rate
        self.min_order_value = min_order_value
        self._validate_weights()

    def _validate_weights(self) -> None:
        symbols = [t.symbol for t in self.targets]
        if len(symbols) != len(set(symbols)):
            raise ValueError("targets contain duplicate symbols")
        total = sum((t.weight for t in self.targets), Decimal(0))
        if abs(total - Decimal("1.0")) > _WEIGHT_TOLERANCE:
            raise ValueError(
                f"weights must sum to 1.0 (got {total}, tolerance {_WEIGHT_TOLERANCE})"
            )

    async def compute_plan(self) -> RebalancePlan:
        """Diff current vs target weights and produce the order list.

        Implemented in a separate plan.
        """
        raise NotImplementedError("compute_plan: implemented in a separate plan")

    async def execute(self, plan: RebalancePlan, *, dry_run: bool = True) -> list[Order]:
        """Run the plan against the broker. dry_run=True simulates only.

        Implemented in a separate plan.
        """
        raise NotImplementedError("execute: implemented in a separate plan")
