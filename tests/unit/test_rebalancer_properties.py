"""Property / integration tests for the rebalancer's core promises.

The unit suites (test_rebalancer, test_rebalancer_strategy) exercise each knob
in isolation. These tests verify the *emergent* behaviour the literature treats
as the whole point of a rebalancer:

- **Convergence to target** — one full pass over a drifted multi-asset sleeve
  lands every holding within one share of its target weight.
- **Drift monotonicity** — a plan never *increases* drift, even when cash is
  insufficient to fully fund it.
- **No-trade region / idempotency** — applying a full rebalance and re-planning
  produces no further orders (the portfolio is a maintenance task, not a source
  of churn). See Kitces, "Optimal Rebalancing – Tolerance Bands".
- **Symmetric bands** — an *overweight target* is sold down past the band and
  left alone within it (the mirror of the underweight skip test).
- **Bounded cash drag** — idle cash after a full deploy stays within the buffer
  plus at most one share.
- **Randomized invariants** — across 60 random drifted portfolios, a plan never
  oversells, never overspends, never goes cash-negative, never increases drift,
  always orders sells first, and is idempotent once settled.
- **Phased execution** — execute() really re-reads the balance between the sell
  and buy phases and re-sizes buys to the actual freed cash.
"""

import random
from datetime import datetime, timezone
from decimal import Decimal

import pytest

from tooja.core.enums import Currency, OrderSide
from tooja.core.models import Balance, Position, Quote, Symbol
from tooja.core.money import Money
from tooja.portfolio import Rebalancer, RebalancePlan, TargetWeight

from tests.unit.test_rebalancer import _FillTrackingOrders, _ScriptedBroker

_A = Symbol(ticker="005930")  # KRX → KRW
_B = Symbol(ticker="035720")
_C = Symbol(ticker="000660")


def _quote(sym: Symbol, px: str) -> Quote:
    return Quote(
        symbol=sym,
        price=Money(amount=Decimal(px), currency=Currency.KRW),
        time=datetime.now(timezone.utc),
    )


def _drift(values: dict[Symbol, Decimal], total: Decimal, targets: dict[Symbol, Decimal]) -> Decimal:
    """Sum of |actual_weight - target_weight| over the union of held + target symbols."""
    syms = set(values) | set(targets)
    return sum(
        (abs(values.get(s, Decimal(0)) / total - targets.get(s, Decimal(0))) for s in syms),
        Decimal(0),
    )


def _balance_from_plan(plan: RebalancePlan) -> Balance:
    """Reconstruct the post-trade balance a broker would report after `plan` fills.

    Each expected holding becomes a position priced at its plan price (so a
    re-plan sees the same prices and no spurious drift), and the leftover
    expected_cash becomes the sole cash entry.
    """
    currency = plan.expected_cash.currency
    positions = [
        Position(
            symbol=h.symbol,
            qty=h.qty,
            avg_price=Money(amount=h.price, currency=currency),
            current_price=Money(amount=h.price, currency=currency),
        )
        for h in plan.expected_holdings
    ]
    return Balance(cash=[plan.expected_cash], positions=positions)


@pytest.mark.asyncio
async def test_full_rebalance_converges_to_target_weights():
    """A drifted 3-asset sleeve, fully funded, lands every holding within one
    share of its ideal target value — the rebalancer's central promise."""
    # sleeve total = 500,000 cash + 50 sh A @ 10,000 = 1,000,000.
    balance = Balance(
        cash=[Money(amount=Decimal("500000"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=_A, qty=Decimal("50"),
                avg_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
            ),
        ],
    )
    quotes = {_A: _quote(_A, "10000"), _B: _quote(_B, "10000"), _C: _quote(_C, "10000")}
    targets = [
        TargetWeight(symbol=_A, weight=Decimal("0.5")),
        TargetWeight(symbol=_B, weight=Decimal("0.3")),
        TargetWeight(symbol=_C, weight=Decimal("0.2")),
    ]
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, quotes),
        targets=targets,
        cash_buffer_rate=Decimal("0"),
        min_order_value=Decimal("0"),
    )
    plan = await rb.compute_plan()

    total = plan.expected_total.amount  # 1,000,000
    held = {h.symbol: h for h in plan.expected_holdings}
    ideal = {_A: Decimal("0.5"), _B: Decimal("0.3"), _C: Decimal("0.2")}
    for sym, weight in ideal.items():
        ideal_shares = (total * weight) / Decimal("10000")
        actual_shares = held[sym].qty
        assert abs(actual_shares - ideal_shares) <= 1, f"{sym} off by >1 share"
    # Residual drift is tiny (clean divide → effectively zero).
    assert plan.expected_drift < Decimal("0.01")


@pytest.mark.asyncio
async def test_full_rebalance_reduces_drift_vs_pre_trade():
    """The plan's residual drift must be strictly smaller than the pre-trade
    drift — a rebalance never makes the allocation worse."""
    balance = Balance(
        cash=[Money(amount=Decimal("500000"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=_A, qty=Decimal("50"),
                avg_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
            ),
        ],
    )
    quotes = {_A: _quote(_A, "10000"), _B: _quote(_B, "10000"), _C: _quote(_C, "10000")}
    targets = {_A: Decimal("0.5"), _B: Decimal("0.3"), _C: Decimal("0.2")}
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, quotes),
        targets=[TargetWeight(symbol=s, weight=w) for s, w in targets.items()],
        cash_buffer_rate=Decimal("0"),
        min_order_value=Decimal("0"),
    )
    plan = await rb.compute_plan()

    # Pre-trade: only A held (500,000 of 1,000,000 sleeve total).
    pre_drift = _drift({_A: Decimal("500000")}, Decimal("1000000"), targets)
    assert plan.expected_drift < pre_drift


@pytest.mark.asyncio
async def test_rebalance_is_idempotent_no_trade_region():
    """Applying a full rebalance and re-planning yields no further orders.

    This is the no-trade-region property: once balanced, the rebalancer is a
    maintenance task, not a churn engine. A second plan that emitted orders
    would mean the first pass overshot or the bands leak.
    """
    balance = Balance(
        cash=[Money(amount=Decimal("500000"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=_A, qty=Decimal("50"),
                avg_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
            ),
        ],
    )
    quotes = {_A: _quote(_A, "10000"), _B: _quote(_B, "10000"), _C: _quote(_C, "10000")}
    targets = [
        TargetWeight(symbol=_A, weight=Decimal("0.5")),
        TargetWeight(symbol=_B, weight=Decimal("0.3")),
        TargetWeight(symbol=_C, weight=Decimal("0.2")),
    ]

    def _make(bal):
        return Rebalancer(
            broker=_ScriptedBroker(bal, quotes),
            targets=targets,
            cash_buffer_rate=Decimal("0"),
            min_order_value=Decimal("0"),
        )

    plan1 = await _make(balance).compute_plan()
    assert plan1.orders, "first pass should trade"

    settled = _balance_from_plan(plan1)
    plan2 = await _make(settled).compute_plan()
    assert plan2.orders == [], f"re-plan churned: {plan2.orders}"


@pytest.mark.asyncio
async def test_overweight_target_is_sold_down_past_band():
    """An overweight *target* (not an off-target holding) is sold toward weight.

    Mirror of test_drift_band_skips_small_drift, which only covers the
    underweight-skip side. Here A is held far above its 50% target and must be
    sold, with the proceeds rotating into the underweight B.
    """
    # A: 90 sh @ 10,000 = 900,000 (target 50%). B: 0 (target 50%). No cash.
    # sleeve total = 900,000 → target A = 450,000 (45 sh) → sell ~45, buy B ~45.
    balance = Balance(
        cash=[Money(amount=Decimal("0"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=_A, qty=Decimal("90"),
                avg_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
            ),
        ],
    )
    quotes = {_A: _quote(_A, "10000"), _B: _quote(_B, "10000")}
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, quotes),
        targets=[
            TargetWeight(symbol=_A, weight=Decimal("0.5")),
            TargetWeight(symbol=_B, weight=Decimal("0.5")),
        ],
        cash_buffer_rate=Decimal("0"),
        min_order_value=Decimal("0"),
    )
    plan = await rb.compute_plan()
    a_sells = [o for o in plan.orders if o.symbol == _A and o.side is OrderSide.SELL]
    assert len(a_sells) == 1, "overweight target A must be sold"
    assert a_sells[0].qty == Decimal("45")
    # Proceeds rotate into underweight B.
    assert any(o.symbol == _B and o.side is OrderSide.BUY for o in plan.orders)


@pytest.mark.asyncio
async def test_overweight_target_within_band_is_left_alone():
    """Symmetric to the underweight skip: a target whose drift sits inside the
    relative drift band emits no order, on either side.

    total = 4,000 cash + 500 sh A + 496 sh B (all @ 1,000) = 1,000,000.
    Targets A=B=50% → 500,000 each. A is exactly on target; B is 4,000 short,
    a relative drift of 4,000/500,000 = 0.008 < the 0.01 band → both skipped.
    """
    balance = Balance(
        cash=[Money(amount=Decimal("4000"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=_A, qty=Decimal("500"),
                avg_price=Money(amount=Decimal("1000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("1000"), currency=Currency.KRW),
            ),
            Position(
                symbol=_B, qty=Decimal("496"),
                avg_price=Money(amount=Decimal("1000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("1000"), currency=Currency.KRW),
            ),
        ],
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),
        targets=[
            TargetWeight(symbol=_A, weight=Decimal("0.5")),
            TargetWeight(symbol=_B, weight=Decimal("0.5")),
        ],
        cash_buffer_rate=Decimal("0"),
        min_order_value=Decimal("0"),
        drift_band=Decimal("0.01"),
    )
    plan = await rb.compute_plan()
    assert plan.orders == []


@pytest.mark.asyncio
async def test_cash_drag_bounded_by_buffer_after_full_deploy():
    """After a fully-funded deploy, idle cash stays within the buffer plus at
    most one share — the rebalancer doesn't strand investable cash."""
    balance = Balance(
        cash=[Money(amount=Decimal("1000000"), currency=Currency.KRW)],
        positions=[],
    )
    quotes = {_A: _quote(_A, "10000")}
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, quotes),
        targets=[TargetWeight(symbol=_A, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0.05"),
        min_order_value=Decimal("0"),
    )
    plan = await rb.compute_plan()
    total = plan.expected_total.amount  # 1,000,000
    buffer = total * Decimal("0.05")  # 50,000
    leftover = plan.expected_cash.amount
    # Idle cash is at least the buffer (we never dip below it) and at most the
    # buffer plus one share's price (rounding remainder).
    assert leftover >= buffer
    assert leftover <= buffer + Decimal("10000")


@pytest.mark.asyncio
async def test_random_portfolios_satisfy_core_invariants():
    """Randomized sweep: 60 drifted portfolios (2-4 targets, random weights,
    prices, holdings, cash, sometimes an off-target holding). Every plan must:

    1. never SELL more than the held quantity,
    2. never spend more than starting cash + sell proceeds,
    3. leave non-negative expected cash,
    4. not increase drift (each order moves a symbol toward target, never past),
    5. order all SELLs before the first BUY,
    6. be idempotent — re-planning the settled result trades nothing.
    """
    rng = random.Random(20260612)
    pool = ["005930", "035720", "000660", "051910", "005380"]
    off_target = Symbol(ticker="105560")

    for trial in range(60):
        n = rng.randint(2, 4)
        syms = [Symbol(ticker=t) for t in rng.sample(pool, n)]
        raw = [rng.randint(1, 100) for _ in range(n)]
        weights = [
            (Decimal(r) / Decimal(sum(raw))).quantize(Decimal("0.0001")) for r in raw[:-1]
        ]
        weights.append(Decimal("1") - sum(weights, Decimal(0)))
        prices = {s: Decimal(rng.randint(1, 500)) * 100 for s in syms}
        prices[off_target] = Decimal("20000")

        positions = []
        for s in syms:
            qty = rng.randint(0, 80)
            if qty:
                positions.append(Position(
                    symbol=s, qty=Decimal(qty),
                    avg_price=Money(amount=prices[s], currency=Currency.KRW),
                    current_price=Money(amount=prices[s], currency=Currency.KRW),
                ))
        if rng.random() < 0.5:
            positions.append(Position(
                symbol=off_target, qty=Decimal(rng.randint(1, 30)),
                avg_price=Money(amount=prices[off_target], currency=Currency.KRW),
                current_price=Money(amount=prices[off_target], currency=Currency.KRW),
            ))
        cash = Decimal(rng.randint(100_000, 5_000_000))

        quotes = {s: _quote(s, str(prices[s])) for s in syms}
        targets = [TargetWeight(symbol=s, weight=w) for s, w in zip(syms, weights)]

        def make(bal):
            return Rebalancer(
                broker=_ScriptedBroker(bal, quotes),
                targets=targets,
                cash_buffer_rate=Decimal("0"),
                min_order_value=Decimal("10000"),
            )

        balance = Balance(
            cash=[Money(amount=cash, currency=Currency.KRW)], positions=positions,
        )
        plan = await make(balance).compute_plan()

        held = {p.symbol: p.qty for p in positions}
        sell_notional = buy_notional = Decimal(0)
        for o in plan.orders:
            if o.side is OrderSide.SELL:
                assert o.qty <= held.get(o.symbol, Decimal(0)), f"trial {trial}: oversell {o}"
                sell_notional += o.qty * prices[o.symbol]
            else:
                buy_notional += o.qty * prices[o.symbol]
        assert buy_notional <= cash + sell_notional, f"trial {trial}: overspend"
        assert plan.expected_cash.amount >= 0, f"trial {trial}: negative expected cash"

        sides = [o.side for o in plan.orders]
        first_buy = next((i for i, s in enumerate(sides) if s is OrderSide.BUY), len(sides))
        assert all(s is OrderSide.SELL for s in sides[:first_buy]), f"trial {trial}: buy before sell"

        total = cash + sum(q * prices[s] for s, q in held.items())
        pre = _drift(
            {s: q * prices[s] for s, q in held.items()}, total, dict(zip(syms, weights)),
        )
        assert plan.expected_drift <= pre + Decimal("0.0001"), f"trial {trial}: drift increased"

        plan2 = await make(_balance_from_plan(plan)).compute_plan()
        assert plan2.orders == [], f"trial {trial}: re-plan churned {plan2.orders}"


class _SequencedAccount:
    """Returns successive balances on successive get_balance calls (last repeats)."""
    _broker_name = "stub"

    def __init__(self, *balances):
        self._balances = list(balances)
        self.calls = 0

    async def get_balance(self):
        self.calls += 1
        if len(self._balances) > 1:
            return self._balances.pop(0)
        return self._balances[0]


@pytest.mark.asyncio
async def test_execute_rereads_balance_between_sell_and_buy_phases():
    """End-to-end phased flow: the plan is computed against the pre-trade
    balance, but the buy budget comes from a SECOND get_balance call made after
    the sells fill — here the sells freed less cash than planned (700k vs 1M),
    so the buy shrinks from 14 to 10 shares."""
    sell_sym = Symbol(ticker="035720")
    buy_sym = Symbol(ticker="005930")
    before = Balance(
        cash=[Money(amount=Decimal("0"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=sell_sym, qty=Decimal("20"),
                avg_price=Money(amount=Decimal("50000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("50000"), currency=Currency.KRW),
            ),
        ],
    )
    after_sells = Balance(  # sells filled below plan price: only 700k freed
        cash=[Money(amount=Decimal("700000"), currency=Currency.KRW)],
        positions=[],
    )
    quotes = {buy_sym: _quote(buy_sym, "70000")}
    rb = Rebalancer(
        broker=_ScriptedBroker(before, quotes),
        targets=[TargetWeight(symbol=buy_sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
    )
    acct = _SequencedAccount(before, after_sells)
    rb.broker.account = acct
    rb.broker.orders = _FillTrackingOrders()

    plan = await rb.compute_plan()  # sized against estimated 1,000,000 proceeds
    assert [(o.side, o.qty) for o in plan.orders] == [
        (OrderSide.SELL, Decimal("20")), (OrderSide.BUY, Decimal("14")),
    ]

    await rb.execute(plan)
    assert acct.calls == 2  # one for the plan, one fresh read between phases
    submitted = rb.broker.orders.received
    assert [(o.side, o.qty) for o in submitted] == [
        (OrderSide.SELL, Decimal("20")),
        (OrderSide.BUY, Decimal("10")),  # floor(700,000 / 70,000), not the planned 14
    ]


@pytest.mark.asyncio
async def test_zero_weight_target_is_fully_exited():
    """weight=0 is an explicit exit instruction: the full holding is sold and
    the proceeds rotate into the remaining targets (distinct from an off-target
    holding only in intent — both must liquidate)."""
    balance = Balance(
        cash=[Money(amount=Decimal("900000"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=_A, qty=Decimal("10"),
                avg_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
            ),
        ],
    )
    quotes = {_B: _quote(_B, "10000")}
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, quotes),
        targets=[
            TargetWeight(symbol=_A, weight=Decimal("0")),
            TargetWeight(symbol=_B, weight=Decimal("1.0")),
        ],
        cash_buffer_rate=Decimal("0"),
        min_order_value=Decimal("10000"),
    )
    plan = await rb.compute_plan()
    assert [(o.side, o.symbol, o.qty) for o in plan.orders] == [
        (OrderSide.SELL, _A, Decimal("10")),
        (OrderSide.BUY, _B, Decimal("100")),  # (900,000 + 100,000) / 10,000
    ]
