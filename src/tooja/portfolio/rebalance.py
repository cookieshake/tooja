"""Target-weight rebalancer.

Computes a diff between current portfolio and a target weight set, then
generates MarketOrder requests to bring the portfolio closer to the targets.

Drift = sum of |actual_weight - target_weight| across symbols.

Constraints:
- All Money inputs are KRW-only (Money currency must match across balance/positions).
- An order is dropped if its notional is below `min_order_value`.
- `cash_buffer_rate` of total assets is held aside (not invested).
"""

from __future__ import annotations

from decimal import Decimal
from typing import Iterable

from pydantic import BaseModel

from tooja.core.broker import Broker
from tooja.core.enums import Currency, OrderSide
from tooja.core.models import (
    MarketOrder,
    Order,
    OrderRequest,
    Symbol,
)


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

        Held positions whose price cannot be resolved (broker omitted
        current_price and market.get_quote also fails) are flagged as
        `unpriced`. Any target symbol whose corresponding position is
        unpriced is skipped — otherwise treating its actual value as 0
        would generate a runaway BUY for the entire target weight.
        """
        balance = await self.broker.account.get_balance()
        if balance.total_asset is None or balance.total_asset.amount <= 0:
            raise ValueError(
                "broker returned no or non-positive total_asset — cannot compute plan"
            )
        total = balance.total_asset.amount
        currency = balance.total_asset.currency

        investable = (total * (Decimal("1.0") - self.cash_buffer_rate)).quantize(Decimal("1"))

        current_value: dict[Symbol, Decimal] = {}
        current_price: dict[Symbol, Decimal] = {}
        unpriced: set[Symbol] = set()
        for pos in balance.positions:
            if pos.current_price is not None and pos.current_price.currency == currency:
                price = pos.current_price.amount
            else:
                price = await self._lookup_price(pos.symbol, currency) or Decimal(0)
            if price > 0:
                current_price[pos.symbol] = price
                current_value[pos.symbol] = pos.qty * price
            elif pos.qty != 0:
                # Catches shorts (qty<0) too — silently dropping them would
                # leak into the BUY pass with actual=0.
                unpriced.add(pos.symbol)

        orders: list[OrderRequest] = []
        drift = Decimal(0)

        for t in self.targets:
            if t.symbol in unpriced:
                # Cannot rebalance this target without a valid price for the
                # existing holding — issuing a BUY based on actual=0 would be
                # catastrophic. Pre-rebalance weight stays as drift.
                actual_now = current_value.get(t.symbol, Decimal(0))
                drift += abs((actual_now / total) - t.weight)
                continue

            target_value = investable * t.weight
            actual = current_value.get(t.symbol, Decimal(0))
            actual_weight = actual / total

            diff_value = target_value - actual
            if abs(diff_value) < self.min_order_value:
                # No trade — residual drift = current drift.
                drift += abs(actual_weight - t.weight)
                continue

            price = current_price.get(t.symbol)
            if price is None or price <= 0:
                price = await self._lookup_price(t.symbol, currency)
            if price is None or price <= 0:
                drift += abs(actual_weight - t.weight)
                continue

            qty_raw = (diff_value / price)
            qty = qty_raw.quantize(Decimal("1"), rounding="ROUND_DOWN") if qty_raw > 0 else \
                (-qty_raw).quantize(Decimal("1"), rounding="ROUND_DOWN")
            if qty <= 0:
                drift += abs(actual_weight - t.weight)
                continue

            side = OrderSide.BUY if diff_value > 0 else OrderSide.SELL
            orders.append(MarketOrder(symbol=t.symbol, side=side, qty=qty))

            trade_val = qty * price
            actual_after = actual + trade_val if side is OrderSide.BUY else actual - trade_val
            drift += abs((actual_after / total) - t.weight)

        # Symbols currently held but not in targets -> fully exit (residual = 0
        # for priced positions; unpriced positions still get a SELL but their
        # post-trade weight is unknown so we don't contribute to drift).
        target_syms = {t.symbol for t in self.targets}
        for pos in balance.positions:
            if pos.symbol in target_syms or pos.qty <= 0:
                continue
            orders.append(MarketOrder(symbol=pos.symbol, side=OrderSide.SELL, qty=pos.qty))

        # Execute SELLs before BUYs so cash is freed up first — otherwise a
        # large BUY at the head of the queue can be rejected for insufficient
        # funds.
        orders.sort(key=lambda o: 0 if o.side is OrderSide.SELL else 1)

        return RebalancePlan(orders=orders, expected_drift=drift)

    async def execute(self, plan: RebalancePlan) -> list[Order]:
        """Run the plan against the broker — calls broker.orders.create per order."""
        out: list[Order] = []
        for req in plan.orders:
            order = await self.broker.orders.create(req)
            out.append(order)
        return out

    async def _lookup_price(self, sym: Symbol, currency: Currency) -> Decimal | None:
        try:
            quote = await self.broker.market.get_quote(sym)
        except Exception:  # noqa: BLE001 — price unavailable -> skip this symbol
            return None
        if quote.price.currency is not currency:
            return None
        return quote.price.amount
