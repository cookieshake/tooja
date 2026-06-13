"""Target-weight rebalancer.

Computes a diff between current portfolio and a target weight set, then
generates broker-neutral PlannedTrade intents to bring the portfolio closer
to the targets. execute() converts each trade to a concrete order at submit
time: domestic (KRX) trades become market orders; overseas trades become
marketable limit orders at quote × (1 ± limit_offset), since KIS overseas
regular-session trading is limit-only.

Drift = sum of |actual_weight - target_weight| across symbols.

Constraints:
- Single-currency: all Money inputs (balance, positions, quotes) must share one
  currency — KRW and USD accounts both work, mixing does not. The plan currency
  is derived from the exchange of the target symbols (via currency_of); the
  balance is then sliced to that currency. Note min_order_value's default
  (10000) is KRW-oriented; pass an appropriate value for USD accounts.
- A symbol is skipped when its full gap |target - actual| is below
  `min_order_value`. The gap — not the step-scaled order notional — is what is
  gated: with step_rate < 1 a smaller order may still be emitted, otherwise
  gradual runs whose per-step amount falls under the minimum could never
  converge.
- `cash_buffer_rate` of the sleeve total (cash + current position value in the
  sleeve currency) is held aside (not invested).
- execute() is phased: SELLs are submitted and confirmed first, then real cash
  is re-read from the broker and BUYs are re-sized against it (long-only).
  compute_plan() remains pure and uses estimated cash.
"""

from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Iterable

from tooja.core.broker import Broker
from tooja.core.enums import Currency, Exchange, OrderSide, OrderStatus, RebalanceDirection
from tooja.core.markets import currency_of
from tooja.core.models import (
    LimitOrder,
    MarketOrder,
    Order,
    OrderRequest,
    Position,
    Symbol,
)
from tooja.core.money import Money
from tooja.portfolio.rebalance.models import (
    ExpectedHolding,
    PlannedTrade,
    RebalancePlan,
    TargetWeight,
    _WEIGHT_TOLERANCE,
)


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
        limit_offset: Decimal = Decimal("0.01"),
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
        self.limit_offset = _require_decimal("limit_offset", limit_offset)
        if not (Decimal("0") <= self.limit_offset < Decimal("1.0")):
            raise ValueError("limit_offset must be in [0, 1.0)")
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
        """Diff current vs target weights and produce the trade list.

        Held positions whose price cannot be resolved (broker omitted
        current_price and market.get_quote also fails) are flagged as
        unpriced. Any target symbol whose corresponding position is
        unpriced is skipped — otherwise treating its actual value as 0
        would generate a runaway BUY for the entire target weight.
        """
        ctx = await self._load_account()
        await self._resolve_prices(ctx)
        self._compute_totals(ctx)
        sell_trades, buy_candidates = await self._diff_targets(ctx)

        fixed_trades: list[PlannedTrade] = list(sell_trades)
        self._exit_off_targets(ctx, fixed_trades)  # off-target 청산을 예산 전에 합류

        trades = self._apply_cash_budget(ctx, fixed_trades, buy_candidates)
        self._apply_cash_sink(ctx, trades)
        trades.sort(key=lambda t: 0 if t.side is OrderSide.SELL else 1)

        holdings, cash, drift = self._summarize(ctx, trades)
        return RebalancePlan(
            trades=trades,
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
        positions = []
        for p in balance.positions:
            try:
                in_sleeve = currency_of(p.symbol.exchange) == currency
            except KeyError:
                # A holding on an exchange with no currency mapping can't belong
                # to this (or any) currency sleeve, so it's filtered out — an
                # unrelated holding must not crash the rebalance of another
                # sleeve. (currency_of is total over the Exchange enum today,
                # guarded by a totality test; this is robustness against future
                # broker adapters / enum growth, not a silent data drop — the
                # ingestion mappers still raise on unmapped wire codes.)
                continue
            if in_sleeve:
                positions.append(p)
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
    ) -> tuple[list[PlannedTrade], list[tuple[PlannedTrade, Decimal]]]:
        sell_trades: list[PlannedTrade] = []
        buy_candidates: list[tuple[PlannedTrade, Decimal]] = []  # (trade, |diff_value| 우선순위)
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
                    (PlannedTrade(symbol=t.symbol, side=OrderSide.BUY, qty=qty), abs(diff_value))
                )
            else:
                held_qty = held_qties.get(t.symbol, Decimal(0))
                sell_qty = min(qty, held_qty)
                if sell_qty > 0:
                    sell_trades.append(
                        PlannedTrade(symbol=t.symbol, side=OrderSide.SELL, qty=sell_qty)
                    )
        return sell_trades, buy_candidates

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

    def _exit_off_targets(self, ctx: _PlanContext, orders: list[PlannedTrade]) -> None:
        # Symbols currently held but not in targets -> exit toward zero. Long
        # positions SELL their qty; short positions BUY back abs(qty). The exit
        # honors step_rate like every other trade: full mode (>= 1.0) clears the
        # whole position at once, gradual mode (< 1.0) liquidates a stochastic
        # fraction each run so a single dropped symbol doesn't dump in one go.
        # min_order_value / drift_band are intentionally not gated here — a
        # zero-target symbol is always out of band and dust should still clear.
        target_syms = {t.symbol for t in self.targets}
        for pos in ctx.positions:
            if pos.symbol in target_syms or pos.qty == 0:
                continue
            side = OrderSide.SELL if pos.qty > 0 else OrderSide.BUY
            if side is OrderSide.SELL and self.direction is RebalanceDirection.BUY_ONLY:
                continue
            if side is OrderSide.BUY and self.direction is RebalanceDirection.SELL_ONLY:
                continue
            full = abs(pos.qty)
            # Scale in shares, not value/price: off-target positions may be
            # unpriced, and full mode must preserve fractional qty exactly
            # (price=1 turns _size's unit math into a pass-through of the share
            # count, but only call it in gradual mode to avoid flooring full).
            if self.step_rate >= Decimal("1.0"):
                qty = full
            else:
                # Cap at the held qty: stochastic rounding can push a fractional
                # position's scaled count above `full` (0.5 × 0.5 = 0.25 -> 1),
                # which would oversell a long or flip a short to long. Mirrors
                # _diff_targets' min(qty, held_qty) guard.
                qty = min(self._size(full * self.step_rate, Decimal(1)), full)
            if qty <= 0:
                continue
            orders.append(PlannedTrade(symbol=pos.symbol, side=side, qty=qty))

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
        fixed_orders: list[PlannedTrade],
        buy_candidates: list[tuple[PlannedTrade, Decimal]],
    ) -> list[PlannedTrade]:
        orders: list[PlannedTrade] = list(fixed_orders)
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
                    orders.append(PlannedTrade(symbol=order.symbol, side=OrderSide.BUY, qty=affordable))
                    available -= affordable * px
        return orders

    def _apply_cash_sink(self, ctx: _PlanContext, orders: list[PlannedTrade]) -> None:
        """Invest surplus cash above buffer into the sink symbol."""
        if self.cash_sink is None:
            return
        if self.direction is RebalanceDirection.SELL_ONLY:
            return  # the sink only ever adds BUY exposure — honor sell-only runs

        price = ctx.current_price.get(self.cash_sink)
        if price is None or price <= 0:
            return  # price unknown -> cannot invest

        # 주문 반영 후 예상 현금
        projected_cash = ctx.starting_cash
        sink_order: PlannedTrade | None = None
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
            orders.append(PlannedTrade(symbol=self.cash_sink, side=OrderSide.BUY, qty=add_qty))
        elif sink_order.side is OrderSide.BUY:
            idx = orders.index(sink_order)
            orders[idx] = PlannedTrade(symbol=self.cash_sink, side=OrderSide.BUY, qty=sink_order.qty + add_qty)
        else:  # 기존 SELL을 축소/플립
            # projected_cash already counted this SELL's proceeds, inflating add_qty by
            # sink_order.qty. The reduce step below absorbs exactly that amount, so the
            # net flipped BUY qty stays correct.
            offset_qty = min(sink_order.qty, add_qty)
            remaining = sink_order.qty - offset_qty
            idx = orders.index(sink_order)
            if remaining > 0:
                orders[idx] = PlannedTrade(symbol=self.cash_sink, side=OrderSide.SELL, qty=remaining)
            else:
                orders.pop(idx)
                flip = add_qty - offset_qty
                if flip > 0:
                    orders.append(PlannedTrade(symbol=self.cash_sink, side=OrderSide.BUY, qty=flip))

    def _summarize(
        self, ctx: _PlanContext, orders: list[PlannedTrade]
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
        the broker's real reported cash after sells settle. Long-only (see the
        rebalance module docstring / design spec).
        """
        sells = [t for t in plan.trades if t.side is OrderSide.SELL]
        buys = [t for t in plan.trades if t.side is OrderSide.BUY]

        out: list[Order] = []
        sell_orders = await self._submit_orders(sells, out)
        await self._await_fills(sell_orders)
        recapped = await self._recap_buys(plan, buys)
        await self._submit_orders(recapped, out)
        return out

    async def _to_order_request(self, trade: PlannedTrade) -> OrderRequest | None:
        """Choose the concrete order type for a trade at submit time.

        KRX accepts market orders; every other venue we route through KIS is
        limit-only in the regular session, so emit a marketable limit at
        quote × (1 ± limit_offset) — Money quantizes it to the currency's
        tick. Returns None when no usable quote exists; the caller skips the
        trade, same as a failed submit.
        """
        if trade.symbol.exchange is Exchange.KRX:
            return MarketOrder(symbol=trade.symbol, side=trade.side, qty=trade.qty)
        px = await self._lookup_price(trade.symbol, self.currency)
        if px is None or px <= 0:
            return None
        factor = (
            Decimal(1) + self.limit_offset
            if trade.side is OrderSide.BUY
            else Decimal(1) - self.limit_offset
        )
        amount = px * factor
        if amount <= 0:
            return None
        return LimitOrder(
            symbol=trade.symbol,
            side=trade.side,
            qty=trade.qty,
            price=Money(amount=amount, currency=self.currency),
        )

    async def _submit_orders(
        self, trades: list[PlannedTrade], out: list[Order]
    ) -> list[Order]:
        """Convert and submit each trade; skip (don't abort) on individual failures.

        A failed conversion (no usable quote) or submit is dropped from the
        results — the subsequent cash re-read reflects whatever actually
        executed, so the buy phase stays safe. Appends to the shared
        cross-phase ``out`` list; returns only this call's orders (used for
        fill-tracking).
        """
        submitted: list[Order] = []
        for trade in trades:
            try:
                req = await self._to_order_request(trade)
                if req is None:
                    continue
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
        self, plan: RebalancePlan, buys: list[PlannedTrade]
    ) -> list[PlannedTrade]:
        """Re-size buys against the broker's real cash, largest-notional first."""
        if not buys:
            return []
        balance = await self.broker.account.get_balance()
        # Budget strictly in the sleeve currency (derived from the targets at
        # construction). balance.total_asset is the whole-account FX rollup —
        # taking the budget currency from it would spend e.g. a KRW cash figure
        # against USD-priced buys on a multi-currency account.
        currency = self.currency
        available = next(
            (m.amount for m in balance.cash if m.currency == currency), Decimal(0)
        )
        # Buffer is denominated in the sleeve currency; expected_total is the
        # sleeve total computed at plan time (cash + positions in this currency).
        # Note: recap deliberately reserves the buffer against the real post-sell
        # cash here, rather than re-deriving investable — it only re-caps the buy
        # budget, and the reserve stays in the same currency, so it is not a
        # double application of the buffer.
        if plan.expected_total is not None and plan.expected_total.currency == currency:
            available -= plan.expected_total.amount * self.cash_buffer_rate

        fallback = {h.symbol: h.price for h in plan.expected_holdings}
        # Re-quote concurrently — sequential round-trips would add latency and
        # widen the price-drift window the phasing is meant to close.
        quotes = await asyncio.gather(
            *(self._lookup_price(o.symbol, currency) for o in buys)
        )
        priced: list[tuple[PlannedTrade, Decimal]] = []
        for o, px in zip(buys, quotes):
            if px is None or px <= 0:
                px = fallback.get(o.symbol, Decimal(0))
            if px <= 0:
                continue
            # Budget at the price the broker will actually reserve: overseas
            # buys are submitted as marketable limits at quote × (1 + offset),
            # and brokers check buying power against the limit price — sizing
            # at the raw quote would overshoot and get the order rejected.
            if o.symbol.exchange is not Exchange.KRX:
                px = px * (Decimal(1) + self.limit_offset)
            priced.append((o, px))
        priced.sort(key=lambda x: x[0].qty * x[1], reverse=True)

        out: list[PlannedTrade] = []
        for o, px in priced:
            cost = o.qty * px
            if cost <= available:
                out.append(o)
                available -= cost
            elif available >= px:
                affordable = (available / px).quantize(Decimal("1"), rounding="ROUND_DOWN")
                if affordable > 0 and affordable * px >= self.min_order_value:
                    out.append(PlannedTrade(symbol=o.symbol, side=OrderSide.BUY, qty=affordable))
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
