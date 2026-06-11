"""Target-weight rebalancer.

Computes a diff between current portfolio and a target weight set, then
generates MarketOrder requests to bring the portfolio closer to the targets.

Drift = sum of |actual_weight - target_weight| across symbols.

Constraints:
- Single-currency: all Money inputs (balance, positions, quotes) must share one
  currency — KRW and USD accounts both work, mixing does not. The plan currency
  is derived from the exchange of the target symbols (via currency_of); the
  balance is then sliced to that currency. Note min_order_value's default
  (10000) is KRW-oriented; pass an appropriate value for USD accounts.
- An order is dropped if its notional is below `min_order_value`.
- `cash_buffer_rate` of the sleeve total (cash + current position value in the
  sleeve currency) is held aside (not invested).
- execute() is phased: SELLs are submitted and confirmed first, then real cash
  is re-read from the broker and BUYs are re-sized against it (long-only,
  market orders only). compute_plan() remains pure and uses estimated cash.
"""

from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Iterable

from tooja.core.broker import Broker
from tooja.core.enums import Currency, OrderSide, OrderStatus, RebalanceDirection
from tooja.core.markets import currency_of
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
    currency: Currency
    positions: list[Position]
    # Cash before any planned orders, taken straight from the broker's reported
    # balance for THIS sleeve's currency.
    starting_cash: Decimal = Decimal(0)
    # total/investable are computed AFTER prices resolve (sleeve total = cash +
    # Σ position value), so they start at 0 and are filled by _compute_totals.
    total: Decimal = Decimal(0)
    investable: Decimal = Decimal(0)
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
        fill_poll_interval: float = 0.5,
        fill_timeout: float = 30.0,
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
        if fill_poll_interval <= 0:
            raise ValueError("fill_poll_interval must be positive")
        if fill_timeout <= 0:
            raise ValueError("fill_timeout must be positive")
        self.fill_poll_interval = fill_poll_interval
        self.fill_timeout = fill_timeout
        self._rng = rng if rng is not None else random.Random()
        self._validate_weights()
        self.currency = self._derive_currency()

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

    def _derive_currency(self) -> Currency:
        """Sleeve currency = the one currency shared by all targets (+ cash_sink).

        The rebalancer manages exactly one currency. Deriving it from the
        targets (rather than a constructor argument) keeps Currency out of the
        public signature and makes a target/currency mismatch impossible.
        """
        exchanges = {t.symbol.exchange for t in self.targets}
        if self.cash_sink is not None:
            exchanges.add(self.cash_sink.exchange)
        currencies = {currency_of(ex) for ex in exchanges}
        if len(currencies) != 1:
            raise ValueError(
                f"targets span multiple currencies {sorted(c.value for c in currencies)} "
                "— use one Rebalancer per currency"
            )
        return next(iter(currencies))

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
        self._compute_totals(ctx)
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
            expected_total=Money(amount=ctx.total, currency=ctx.currency),
        )

    async def _load_account(self) -> _PlanContext:
        """Read the broker balance and keep only this sleeve's currency slice.

        The sleeve total is NOT taken from balance.total_asset (that is the whole
        account FX-converted into one base currency). It is computed later, after
        prices resolve, from this currency's cash + positions (_compute_totals).
        """
        balance = await self.broker.account.get_balance()
        currency = self.currency
        starting_cash = next(
            (m.amount for m in balance.cash if m.currency == currency), Decimal(0)
        )
        positions = [
            p for p in balance.positions
            if currency_of(p.symbol.exchange) == currency
        ]
        return _PlanContext(
            currency=currency, positions=positions, starting_cash=starting_cash,
        )

    def _compute_totals(self, ctx: _PlanContext) -> None:
        """Sleeve total = sleeve cash + Σ(qty × effective_price) over sleeve positions.

        effective_price is the resolved market price, or avg_price when the quote
        was unavailable (consistent with _summarize/_get_effective_price). This
        replaces the old reliance on balance.total_asset, which conflates
        currencies in a multi-currency account.
        """
        total = ctx.starting_cash
        for pos in ctx.positions:
            price = ctx.current_price.get(pos.symbol)
            if price is None or price <= 0:
                price = pos.avg_price.amount
            total += pos.qty * price
        if total <= 0:
            raise ValueError(
                "sleeve has no positive total (no cash or positions in "
                f"{ctx.currency.value}) — cannot compute plan"
            )
        ctx.total = total
        ctx.investable = (
            total * (Decimal("1.0") - self.cash_buffer_rate)
        ).quantize(Decimal("1"))

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

    def _get_effective_price(self, symbol: Symbol, ctx: _PlanContext) -> Decimal:
        """Resolved market price, or the position's avg_price when unpriced.

        Falling back to avg_price keeps cash math honest for unpriced orders
        (e.g. covering an unpriced short) instead of treating them as free.
        """
        px = ctx.current_price.get(symbol)
        if px is not None and px > 0:
            return px
        pos = next((p for p in ctx.positions if p.symbol == symbol), None)
        return pos.avg_price.amount if pos else Decimal(0)

    def _apply_cash_budget(
        self,
        ctx: _PlanContext,
        fixed_orders: list[OrderRequest],
        buy_candidates: list[tuple[OrderRequest, Decimal]],
    ) -> list[OrderRequest]:
        orders: list[OrderRequest] = list(fixed_orders)
        available = ctx.starting_cash
        for o in fixed_orders:  # SELL은 현금↑, 숏청산 BUY는 현금↓
            px = self._get_effective_price(o.symbol, ctx)
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
            px = self._get_effective_price(o.symbol, ctx)
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
        cash = ctx.starting_cash

        for o in orders:
            px = self._get_effective_price(o.symbol, ctx)
            cost = o.qty * px
            if o.side is OrderSide.BUY:
                qty[o.symbol] = qty.get(o.symbol, Decimal(0)) + o.qty
                cash -= cost
            else:
                qty[o.symbol] = qty.get(o.symbol, Decimal(0)) - o.qty
                cash += cost

        holdings = []
        for s, q in qty.items():
            if q == 0:
                continue
            px = self._get_effective_price(s, ctx)
            holdings.append(ExpectedHolding(symbol=s, qty=q, price=px, value=q * px))
        target_map = {t.symbol: t.weight for t in self.targets}
        weighted = {h.symbol: (h.value / ctx.total) for h in holdings}
        syms = set(target_map) | set(weighted)
        drift = sum(
            (abs(weighted.get(s, Decimal(0)) - target_map.get(s, Decimal(0))) for s in syms),
            Decimal(0),
        )
        return holdings, Money(amount=cash, currency=ctx.currency), drift

    async def execute(self, plan: RebalancePlan) -> list[Order]:
        """Phased execution: sell, confirm fills, re-read real cash, then buy.

        Buy quantities in ``plan`` were sized against *estimated* cash. Prices
        move between planning and execution, so we re-derive the buy budget from
        the broker's real reported cash after sells settle. Long-only, market
        orders only (see the rebalance module docstring / design spec).
        """
        sells = [o for o in plan.orders if o.side is OrderSide.SELL]
        buys = [o for o in plan.orders if o.side is OrderSide.BUY]

        out: list[Order] = []
        sell_orders = await self._submit_orders(sells, out)
        await self._await_fills(sell_orders)
        recapped = await self._recap_buys(plan, buys)
        await self._submit_orders(recapped, out)
        return out

    async def _submit_orders(
        self, reqs: list[OrderRequest], out: list[Order]
    ) -> list[Order]:
        """Submit each request; skip (don't abort) on individual failures.

        A failed submit is dropped from the results — the subsequent cash
        re-read reflects whatever actually executed, so the buy phase stays safe.
        Appends to the shared cross-phase ``out`` list; returns only this
        call's orders (used for fill-tracking).
        """
        submitted: list[Order] = []
        for req in reqs:
            try:
                order = await self.broker.orders.create(req)
            except Exception:  # noqa: BLE001 — one bad order must not abort the rest
                continue
            out.append(order)
            submitted.append(order)
        return submitted

    async def _await_fills(self, orders: list[Order]) -> None:
        """Poll each order until terminal status or fill_timeout elapses.

        On timeout we simply return: the cash re-read in _recap_buys reflects
        whatever filled, so under-filled sells just shrink the buy budget.
        """
        if not orders:
            return
        terminal = {OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.REJECTED}
        pending = {o.order_id for o in orders}
        loop = asyncio.get_running_loop()
        start = loop.time()
        while pending and (loop.time() - start) < self.fill_timeout:
            oids = list(pending)
            results = await asyncio.gather(
                *(self.broker.orders.get(oid) for oid in oids),
                return_exceptions=True,
            )
            for oid, res in zip(oids, results):
                if isinstance(res, Exception):
                    continue  # treat unknown as still pending
                if res.status in terminal:
                    pending.discard(oid)
            if not pending:
                break
            await asyncio.sleep(self.fill_poll_interval)

    async def _recap_buys(
        self, plan: RebalancePlan, buys: list[OrderRequest]
    ) -> list[OrderRequest]:
        """Re-size buys against the broker's real cash, largest-notional first."""
        if not buys:
            return []
        balance = await self.broker.account.get_balance()
        if plan.expected_cash is not None:
            currency = plan.expected_cash.currency
        elif balance.total_asset is not None:
            currency = balance.total_asset.currency  # mirror _load_account
        else:
            currency = Currency.KRW
        available = next(
            (m.amount for m in balance.cash if m.currency == currency), Decimal(0)
        )
        # Buffer is denominated in the sleeve currency; expected_total is the
        # sleeve total computed at plan time (cash + positions in this currency).
        if plan.expected_total is not None and plan.expected_total.currency == currency:
            available -= plan.expected_total.amount * self.cash_buffer_rate

        fallback = {h.symbol: h.price for h in plan.expected_holdings}
        # Re-quote concurrently — sequential round-trips would add latency and
        # widen the price-drift window the phasing is meant to close.
        quotes = await asyncio.gather(
            *(self._lookup_price(o.symbol, currency) for o in buys)
        )
        priced: list[tuple[OrderRequest, Decimal]] = []
        for o, px in zip(buys, quotes):
            if px is None or px <= 0:
                px = fallback.get(o.symbol, Decimal(0))
            if px > 0:
                priced.append((o, px))
        priced.sort(key=lambda x: x[0].qty * x[1], reverse=True)

        out: list[OrderRequest] = []
        for o, px in priced:
            cost = o.qty * px
            if cost <= available:
                out.append(o)
                available -= cost
            elif available >= px:
                affordable = (available / px).quantize(Decimal("1"), rounding="ROUND_DOWN")
                if affordable > 0 and affordable * px >= self.min_order_value:
                    out.append(MarketOrder(symbol=o.symbol, side=OrderSide.BUY, qty=affordable))
                    available -= affordable * px
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
