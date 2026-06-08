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

import asyncio
import random
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Iterable

from tooja.core.broker import Broker
from tooja.core.enums import Currency, OrderSide, RebalanceDirection
from tooja.core.models import (
    MarketOrder,
    Order,
    OrderRequest,
    Position,
    Symbol,
)
from tooja.core.money import Money
from tooja.portfolio.rebalance.models import ExpectedHolding, RebalancePlan, TargetWeight, _WEIGHT_TOLERANCE


def _require_decimal(name: str, value: Decimal) -> Decimal:
    if not isinstance(value, Decimal):
        raise TypeError(
            f"{name} must be Decimal (got {type(value).__name__}); use Decimal('...') explicitly"
        )
    return value


@dataclass
class _PlanContext:
    total: Decimal
    currency: Currency
    investable: Decimal
    positions: list[Position]
    # Cash before any planned orders, taken straight from the broker's reported
    # balance. We do NOT derive it as ``total - invested`` because unpriced
    # positions are missing from ``invested`` and would inflate the figure.
    starting_cash: Decimal = Decimal(0)
    current_value: dict[Symbol, Decimal] = field(default_factory=dict)
    current_price: dict[Symbol, Decimal] = field(default_factory=dict)
    unpriced: set[Symbol] = field(default_factory=set)


class Rebalancer:
    """Depends only on the `Broker` ABC — works against any adapter."""

    def __init__(
        self,
        broker: Broker,
        targets: Iterable[TargetWeight],
        *,
        cash_buffer_rate: Decimal = Decimal("0.02"),
        min_order_value: Decimal = Decimal("10000"),
        drift_band: Decimal = Decimal("0"),
        step_rate: Decimal = Decimal("1.0"),
        rng: random.Random | None = None,
        direction: RebalanceDirection = RebalanceDirection.BOTH,
        cash_sink: Symbol | None = None,
    ):
        self.broker = broker
        self.targets = list(targets)
        self.cash_buffer_rate = _require_decimal("cash_buffer_rate", cash_buffer_rate)
        if not (Decimal("0") <= self.cash_buffer_rate < Decimal("1.0")):
            raise ValueError("cash_buffer_rate must be in [0, 1.0)")
        self.min_order_value = _require_decimal("min_order_value", min_order_value)
        if self.min_order_value < Decimal("0"):
            raise ValueError("min_order_value must be non-negative")
        self.drift_band = _require_decimal("drift_band", drift_band)
        if self.drift_band < Decimal("0"):
            raise ValueError("drift_band must be non-negative")
        self.step_rate = _require_decimal("step_rate", step_rate)
        if not (Decimal("0") <= self.step_rate <= Decimal("1.0")):
            raise ValueError("step_rate must be in [0, 1.0]")
        self.direction = direction
        self.cash_sink = cash_sink
        self._rng = rng if rng is not None else random.Random()
        self._validate_weights()

    def _validate_weights(self) -> None:
        symbols = [t.symbol for t in self.targets]
        if len(symbols) != len(set(symbols)):
            raise ValueError("targets contain duplicate symbols")
        if any(t.weight < 0 for t in self.targets):
            raise ValueError("target weights must be non-negative")
        total = sum((t.weight for t in self.targets), Decimal(0))
        if abs(total - Decimal("1.0")) > _WEIGHT_TOLERANCE:
            raise ValueError(
                f"weights must sum to 1.0 (got {total}, tolerance {_WEIGHT_TOLERANCE})"
            )

    async def compute_plan(self) -> RebalancePlan:
        """Diff current vs target weights and produce the order list.

        Held positions whose price cannot be resolved (broker omitted
        current_price and market.get_quote also fails) are flagged as
        unpriced. Any target symbol whose corresponding position is
        unpriced is skipped — otherwise treating its actual value as 0
        would generate a runaway BUY for the entire target weight.
        """
        ctx = await self._load_account()
        await self._resolve_prices(ctx)
        sell_orders, buy_candidates = await self._diff_targets(ctx)

        fixed_orders: list[OrderRequest] = list(sell_orders)
        self._exit_off_targets(ctx, fixed_orders)  # off-target 청산을 예산 전에 합류

        orders = self._apply_cash_budget(ctx, fixed_orders, buy_candidates)
        self._apply_cash_sink(ctx, orders)
        orders.sort(key=lambda o: 0 if o.side is OrderSide.SELL else 1)

        holdings, cash, drift = self._summarize(ctx, orders)
        return RebalancePlan(
            orders=orders,
            expected_drift=drift,
            expected_holdings=holdings,
            expected_cash=cash,
        )

    async def _load_account(self) -> _PlanContext:
        balance = await self.broker.account.get_balance()
        if balance.total_asset is None or balance.total_asset.amount <= 0:
            raise ValueError(
                "broker returned no or non-positive total_asset — cannot compute plan"
            )
        total = balance.total_asset.amount
        currency = balance.total_asset.currency
        investable = (total * (Decimal("1.0") - self.cash_buffer_rate)).quantize(Decimal("1"))
        starting_cash = next(
            (m.amount for m in balance.cash if m.currency == currency), Decimal(0)
        )
        return _PlanContext(
            total=total, currency=currency, investable=investable,
            positions=balance.positions, starting_cash=starting_cash,
        )

    async def _resolve_prices(self, ctx: _PlanContext) -> None:
        # Position prices: prefer position.current_price (matching currency), else needs a quote.
        need_quote: set[Symbol] = set()
        for pos in ctx.positions:
            if pos.qty == 0:
                continue  # worth 0, never exited — no quote needed
            if pos.current_price is not None and pos.current_price.currency == ctx.currency:
                ctx.current_price[pos.symbol] = pos.current_price.amount
            else:
                need_quote.add(pos.symbol)
        # Target symbols and cash_sink that don't yet have a price also need a quote.
        for t in self.targets:
            if t.symbol not in ctx.current_price:
                need_quote.add(t.symbol)
        if self.cash_sink is not None and self.cash_sink not in ctx.current_price:
            need_quote.add(self.cash_sink)
        # Fetch all missing quotes concurrently.
        symbols = list(need_quote)
        if symbols:
            results = await asyncio.gather(
                *(self._lookup_price(s, ctx.currency) for s in symbols)
            )
            for sym, price in zip(symbols, results):
                if price is not None and price > 0:
                    ctx.current_price[sym] = price
        # Compute current position values; flag unpriced holdings (incl. shorts qty<0).
        for pos in ctx.positions:
            price = ctx.current_price.get(pos.symbol)
            if price is not None and price > 0:
                ctx.current_value[pos.symbol] = pos.qty * price
            elif pos.qty != 0:
                ctx.unpriced.add(pos.symbol)

    async def _diff_targets(
        self, ctx: _PlanContext
    ) -> tuple[list[OrderRequest], list[tuple[OrderRequest, Decimal]]]:
        sell_orders: list[OrderRequest] = []
        buy_candidates: list[tuple[OrderRequest, Decimal]] = []  # (order, |diff_value| 우선순위)
        held_qties = {p.symbol: p.qty for p in ctx.positions}
        for t in self.targets:
            if t.symbol in ctx.unpriced:
                continue

            target_value = ctx.investable * t.weight
            actual = ctx.current_value.get(t.symbol, Decimal(0))
            diff_value = target_value - actual
            if target_value > 0 and (abs(diff_value) / target_value) < self.drift_band:
                continue
            if abs(diff_value) < self.min_order_value:
                continue
            price = ctx.current_price.get(t.symbol)
            if price is None or price <= 0:
                continue

            # No-trade band: ignore gaps smaller than one share. Prevents stochastic
            # rounding from churning ±1 share around a non-integer-share target.
            if abs(diff_value) < price:
                continue

            adjusted_diff = diff_value * self.step_rate
            if self.direction is RebalanceDirection.BUY_ONLY and adjusted_diff < 0:
                continue
            if self.direction is RebalanceDirection.SELL_ONLY and adjusted_diff > 0:
                continue
            qty = self._size(adjusted_diff, price)
            if qty <= 0:
                continue

            if adjusted_diff > 0:
                buy_candidates.append(
                    (MarketOrder(symbol=t.symbol, side=OrderSide.BUY, qty=qty), abs(diff_value))
                )
            else:
                held_qty = held_qties.get(t.symbol, Decimal(0))
                sell_qty = min(qty, held_qty)
                if sell_qty > 0:
                    sell_orders.append(
                        MarketOrder(symbol=t.symbol, side=OrderSide.SELL, qty=sell_qty)
                    )
        return sell_orders, buy_candidates

    def _size(self, adjusted_diff: Decimal, price: Decimal) -> Decimal:
        """Compute integer share count from an already-scaled difference value.

        When ``step_rate == 1.0`` (full rebalance), the result is deterministic:
        ``floor(|adjusted_diff| / price)``.

        When ``step_rate < 1`` (incremental mode), stochastic rounding is used:
        the fractional part ``frac`` of the raw unit count becomes the probability
        of rounding up to ``floor + 1``.  This keeps the expected value equal to
        the exact unit count (unbiased), so repeated partial steps converge to the
        target without systematic under-shooting.
        """
        units = abs(adjusted_diff) / price
        floor = units.quantize(Decimal("1"), rounding="ROUND_DOWN")
        if self.step_rate >= Decimal("1.0"):
            return floor
        frac = units - floor
        if self._rng.random() < float(frac):
            return floor + Decimal("1")
        return floor

    def _exit_off_targets(self, ctx: _PlanContext, orders: list[OrderRequest]) -> None:
        # Symbols currently held but not in targets -> fully exit. Long
        # positions SELL their qty; short positions BUY back abs(qty).
        target_syms = {t.symbol for t in self.targets}
        for pos in ctx.positions:
            if pos.symbol in target_syms or pos.qty == 0:
                continue
            side = OrderSide.SELL if pos.qty > 0 else OrderSide.BUY
            if side is OrderSide.SELL and self.direction is RebalanceDirection.BUY_ONLY:
                continue
            if side is OrderSide.BUY and self.direction is RebalanceDirection.SELL_ONLY:
                continue
            orders.append(MarketOrder(symbol=pos.symbol, side=side, qty=abs(pos.qty)))

    def _apply_cash_budget(
        self,
        ctx: _PlanContext,
        fixed_orders: list[OrderRequest],
        buy_candidates: list[tuple[OrderRequest, Decimal]],
    ) -> list[OrderRequest]:
        orders: list[OrderRequest] = list(fixed_orders)
        available = ctx.starting_cash
        for o in fixed_orders:  # SELL은 현금↑, 숏청산 BUY는 현금↓
            px = ctx.current_price.get(o.symbol)
            if px is None or px <= 0:
                # Unpriced order (e.g. exiting an unpriced position): fall back to
                # avg_price so a short cover BUY still debits cash and can't overdraw.
                pos = next((p for p in ctx.positions if p.symbol == o.symbol), None)
                px = pos.avg_price.amount if pos else Decimal(0)
            available += o.qty * px if o.side is OrderSide.SELL else -(o.qty * px)

        buy_candidates.sort(key=lambda x: x[1], reverse=True)  # 괴리 큰 순
        for order, _prio in buy_candidates:
            px = ctx.current_price.get(order.symbol, Decimal(0))
            if px <= 0:
                continue
            cost = order.qty * px
            if cost <= available:
                orders.append(order)
                available -= cost
            elif available >= px:
                affordable = (available / px).quantize(Decimal("1"), rounding="ROUND_DOWN")
                if affordable > 0 and affordable * px >= self.min_order_value:
                    orders.append(MarketOrder(symbol=order.symbol, side=OrderSide.BUY, qty=affordable))
                    available -= affordable * px
        return orders

    def _apply_cash_sink(self, ctx: _PlanContext, orders: list[OrderRequest]) -> None:
        """Invest surplus cash above buffer into the sink symbol."""
        if self.cash_sink is None:
            return

        price = ctx.current_price.get(self.cash_sink)
        if price is None or price <= 0:
            return  # price unknown -> cannot invest

        # 주문 반영 후 예상 현금
        projected_cash = ctx.starting_cash
        sink_order: OrderRequest | None = None
        for o in orders:
            px = ctx.current_price.get(o.symbol, Decimal(0))
            cost = o.qty * px
            projected_cash += cost if o.side is OrderSide.SELL else -cost
            if o.symbol == self.cash_sink:
                sink_order = o

        reserve = ctx.total * self.cash_buffer_rate  # buffer로 남길 현금
        # step_rate scales the lump-sum surplus for gradual investment (single-symbol sink,
        # so applied once as a scalar rather than per-order as in the main pass).
        investable_cash = (projected_cash - reserve) * self.step_rate
        if investable_cash <= 0:
            return
        # Cap by the full surplus above buffer so stochastic rounding never dips into the buffer.
        max_qty = ((projected_cash - reserve) / price).quantize(Decimal("1"), rounding="ROUND_DOWN")
        add_qty = min(self._size(investable_cash, price), max_qty)
        if add_qty <= 0:
            return

        if sink_order is None:
            orders.append(MarketOrder(symbol=self.cash_sink, side=OrderSide.BUY, qty=add_qty))
        elif sink_order.side is OrderSide.BUY:
            idx = orders.index(sink_order)
            orders[idx] = MarketOrder(symbol=self.cash_sink, side=OrderSide.BUY, qty=sink_order.qty + add_qty)
        else:  # 기존 SELL을 축소/플립
            # projected_cash already counted this SELL's proceeds, inflating add_qty by
            # sink_order.qty. The reduce step below absorbs exactly that amount, so the
            # net flipped BUY qty stays correct.
            offset_qty = min(sink_order.qty, add_qty)
            remaining = sink_order.qty - offset_qty
            idx = orders.index(sink_order)
            if remaining > 0:
                orders[idx] = MarketOrder(symbol=self.cash_sink, side=OrderSide.SELL, qty=remaining)
            else:
                orders.pop(idx)
                flip = add_qty - offset_qty
                if flip > 0:
                    orders.append(MarketOrder(symbol=self.cash_sink, side=OrderSide.BUY, qty=flip))

    def _summarize(
        self, ctx: _PlanContext, orders: list[OrderRequest]
    ) -> tuple[list[ExpectedHolding], Money, Decimal]:
        qty: dict[Symbol, Decimal] = {p.symbol: p.qty for p in ctx.positions}
        price: dict[Symbol, Decimal] = dict(ctx.current_price)
        cash = ctx.starting_cash

        for o in orders:
            px = price.get(o.symbol, Decimal(0))
            cost = o.qty * px
            if o.side is OrderSide.BUY:
                qty[o.symbol] = qty.get(o.symbol, Decimal(0)) + o.qty
                cash -= cost
            else:
                qty[o.symbol] = qty.get(o.symbol, Decimal(0)) - o.qty
                cash += cost

        holdings = [
            ExpectedHolding(
                symbol=s, qty=q, price=price.get(s, Decimal(0)),
                value=q * price.get(s, Decimal(0)),
            )
            for s, q in qty.items()
            if q != 0
        ]
        target_map = {t.symbol: t.weight for t in self.targets}
        weighted = {h.symbol: (h.value / ctx.total) for h in holdings}
        syms = set(target_map) | set(weighted)
        drift = sum(
            (abs(weighted.get(s, Decimal(0)) - target_map.get(s, Decimal(0))) for s in syms),
            Decimal(0),
        )
        return holdings, Money(amount=cash, currency=ctx.currency), drift

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
            if quote is None or quote.price is None:
                return None
            if quote.price.currency != currency:
                return None
            return quote.price.amount
        except Exception:  # noqa: BLE001 — price unavailable -> skip this symbol
            return None
