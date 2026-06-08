import random

import pytest
from datetime import datetime, timezone
from decimal import Decimal

from tooja.core.enums import Currency, RebalanceDirection
from tooja.core.models import Balance, Position, Quote, Symbol
from tooja.core.money import Money
from tooja.portfolio import Rebalancer, TargetWeight
from tooja.portfolio.rebalance import ExpectedHolding

# reuse _ScriptedBroker from the integration-style test module
from tests.unit.test_rebalancer import _ScriptedBroker


def test_rebalance_direction_values():
    assert RebalanceDirection.BOTH.value == "both"
    assert RebalanceDirection.BUY_ONLY.value == "buy_only"
    assert RebalanceDirection.SELL_ONLY.value == "sell_only"


@pytest.mark.asyncio
async def test_plan_reports_expected_holdings_and_cash():
    sym = Symbol(ticker="005930")
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("1000000"), currency=Currency.KRW)],
        positions=[],
    )
    quote = Quote(
        symbol=sym,
        price=Money(amount=Decimal("70000"), currency=Currency.KRW),
        time=datetime.now(timezone.utc),
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {sym: quote}),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
    )
    plan = await rb.compute_plan()
    # 14주 * 70,000 = 980,000 매수 → 현금 20,000 남음
    held = {h.symbol: h for h in plan.expected_holdings}
    assert held[sym].qty == Decimal("14")
    assert held[sym].value == Decimal("980000")
    assert plan.expected_cash == Money(amount=Decimal("20000"), currency=Currency.KRW)


@pytest.mark.asyncio
async def test_step_rate_partial_close():
    sym = Symbol(ticker="005930")
    # 보유 0, 현금 100만, target 100%, price 50,000.
    # step_rate 0.5 → 조정 gap 50만 → 50만/5만 = 10.0 (frac 0).
    # frac이 0이라 floor/stochastic 무관하게 항상 10주 → Task 7 도입 후에도 안정.
    # (step_rate 1.0이었다면 100만/5만 = 20주였을 것 → step_rate 효과 검증)
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("1000000"), currency=Currency.KRW)],
        positions=[],
    )
    quote = Quote(
        symbol=sym,
        price=Money(amount=Decimal("50000"), currency=Currency.KRW),
        time=datetime.now(timezone.utc),
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {sym: quote}),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
        step_rate=Decimal("0.5"),
    )
    plan = await rb.compute_plan()
    assert len(plan.orders) == 1
    assert plan.orders[0].qty == Decimal("10")


@pytest.mark.asyncio
async def test_drift_band_skips_small_drift():
    sym = Symbol(ticker="005930")
    # 보유 992주 × 1,000원 = 992,000 / total 1,000,000
    # target 100%, target_value = 1,000,000
    # diff = 8,000, 상대 drift = 8,000 / 1,000,000 = 0.008 < band 0.01 → skip
    # min_order_value=0 이라 밴드가 없으면 거래 발생
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("8000"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=sym, qty=Decimal("992"),
                avg_price=Money(amount=Decimal("1000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("1000"), currency=Currency.KRW),
            ),
        ],
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
        min_order_value=Decimal("0"),
        drift_band=Decimal("0.01"),
    )
    plan = await rb.compute_plan()
    assert plan.orders == []


@pytest.mark.asyncio
async def test_stochastic_rounding_is_seeded_and_unbiased():
    sym = Symbol(ticker="005930")

    def make_rb(seed: int):
        balance = Balance(
            total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
            cash=[Money(amount=Decimal("1000000"), currency=Currency.KRW)],
            positions=[],
        )
        quote = Quote(
            symbol=sym,
            price=Money(amount=Decimal("70000"), currency=Currency.KRW),
            time=datetime.now(timezone.utc),
        )
        return Rebalancer(
            broker=_ScriptedBroker(balance, {sym: quote}),
            targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
            cash_buffer_rate=Decimal("0"),
            step_rate=Decimal("0.5"),  # 조정 gap 50만 → 50만/7만 = 7.142..주
            rng=random.Random(seed),
        )

    # 동일 seed → 결정적 재현
    p1 = await make_rb(42).compute_plan()
    p2 = await make_rb(42).compute_plan()
    assert p1.orders[0].qty == p2.orders[0].qty
    # floor 7 또는 ceil 8 중 하나
    assert p1.orders[0].qty in (Decimal("7"), Decimal("8"))

    # 무편향: 다수 시도 평균이 7.14에 근접
    qtys = [int((await make_rb(s).compute_plan()).orders[0].qty) for s in range(400)]
    avg = sum(qtys) / len(qtys)
    assert 7.0 < avg < 7.3  # 기댓값 ≈ 7.142


@pytest.mark.asyncio
async def test_direction_buy_only_skips_sells():
    sym = Symbol(ticker="005930")
    sym2 = Symbol(ticker="000660")
    # sym: 보유 100만(100%), target 40% → SELL 필요. BUY_ONLY → 주문 없음.
    # sym2: 보유 없음, target 60% → BUY 필요. BUY_ONLY이므로 주문 발생해야 하지만
    #   현금이 0이라 구매불가 → 총 주문 없음. 핵심은 SELL이 skip됨을 확인.
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("0"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=sym, qty=Decimal("100"),
                avg_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
            ),
        ],
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),
        targets=[
            TargetWeight(symbol=sym, weight=Decimal("0.4")),
            TargetWeight(symbol=sym2, weight=Decimal("0.6")),
        ],
        cash_buffer_rate=Decimal("0"),
        direction=RebalanceDirection.BUY_ONLY,
    )
    plan = await rb.compute_plan()
    # sym: SELL이 BUY_ONLY로 skip. sym2: 가격 미조회 → skip.
    assert plan.orders == []


@pytest.mark.asyncio
async def test_direction_buy_only_allows_buy_suppresses_sell():
    from tooja.core.enums import OrderSide

    over = Symbol(ticker="005930")   # target 0.4, overweight → would SELL → suppressed
    under = Symbol(ticker="000660")  # target 0.6, underweight → would BUY → allowed
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("300000"), currency=Currency.KRW)],  # 1,000,000 - 700,000 held
        positions=[
            Position(
                symbol=over, qty=Decimal("700"),
                avg_price=Money(amount=Decimal("1000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("1000"), currency=Currency.KRW),
            ),
        ],
    )
    quote = Quote(
        symbol=under,
        price=Money(amount=Decimal("1000"), currency=Currency.KRW),
        time=datetime.now(timezone.utc),
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {under: quote}),
        targets=[
            TargetWeight(symbol=over, weight=Decimal("0.4")),
            TargetWeight(symbol=under, weight=Decimal("0.6")),
        ],
        cash_buffer_rate=Decimal("0"),
        direction=RebalanceDirection.BUY_ONLY,
    )
    plan = await rb.compute_plan()
    # over (SELL) suppressed; under (BUY) allowed. Don't assert qty (Task 9 may make it partial).
    assert all(o.side is OrderSide.BUY for o in plan.orders)
    assert any(o.symbol == under and o.side is OrderSide.BUY for o in plan.orders)
    assert not any(o.symbol == over for o in plan.orders)


@pytest.mark.asyncio
async def test_direction_sell_only_allows_sell_suppresses_buy():
    from tooja.core.enums import OrderSide

    over = Symbol(ticker="005930")   # target 0.4, overweight → SELL → allowed
    under = Symbol(ticker="000660")  # target 0.6, underweight → BUY → suppressed
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("300000"), currency=Currency.KRW)],  # 1,000,000 - 700,000 held
        positions=[
            Position(
                symbol=over, qty=Decimal("700"),
                avg_price=Money(amount=Decimal("1000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("1000"), currency=Currency.KRW),
            ),
        ],
    )
    quote = Quote(
        symbol=under,
        price=Money(amount=Decimal("1000"), currency=Currency.KRW),
        time=datetime.now(timezone.utc),
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {under: quote}),
        targets=[
            TargetWeight(symbol=over, weight=Decimal("0.4")),
            TargetWeight(symbol=under, weight=Decimal("0.6")),
        ],
        cash_buffer_rate=Decimal("0"),
        direction=RebalanceDirection.SELL_ONLY,
    )
    plan = await rb.compute_plan()
    # over (SELL) allowed; under (BUY) suppressed.
    assert all(o.side is OrderSide.SELL for o in plan.orders)
    assert any(o.symbol == over and o.side is OrderSide.SELL for o in plan.orders)
    assert not any(o.symbol == under for o in plan.orders)


@pytest.mark.asyncio
async def test_cash_budget_prioritizes_larger_underweight():
    big = Symbol(ticker="005930")    # target 0.7
    small = Symbol(ticker="035720")  # target 0.3
    balance = Balance(
        total_asset=Money(amount=Decimal("800000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("800000"), currency=Currency.KRW)],
        positions=[],
    )
    quotes = {
        big: Quote(symbol=big, price=Money(amount=Decimal("100000"), currency=Currency.KRW),
                   time=datetime.now(timezone.utc)),
        small: Quote(symbol=small, price=Money(amount=Decimal("100000"), currency=Currency.KRW),
                     time=datetime.now(timezone.utc)),
    }
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, quotes),
        targets=[
            TargetWeight(symbol=big, weight=Decimal("0.7")),
            TargetWeight(symbol=small, weight=Decimal("0.3")),
        ],
        cash_buffer_rate=Decimal("0"),
    )
    # investable 800,000: big target 560,000→5주(500,000), small 240,000→2주(200,000)
    # 합 700,000 ≤ 800,000 → 둘 다 가능
    plan = await rb.compute_plan()
    bought = {o.symbol: o.qty for o in plan.orders}
    assert bought[big] == Decimal("5")
    assert bought[small] == Decimal("2")
    total_buy = sum(o.qty * Decimal("100000") for o in plan.orders)
    assert total_buy <= Decimal("800000")


@pytest.mark.asyncio
async def test_cash_sink_respects_buffer():
    sink = Symbol(ticker="153130")
    # total 1,000,000, buffer 2% = 20,000 유지. target = sink 100%.
    # investable 980,000 → 98주(980,000) 매수. 잔여현금 20,000 = buffer.
    # sink 단계는 buffer 초과 현금이 없으므로 추가 매수 없음 → 98주.
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("1000000"), currency=Currency.KRW)],
        positions=[],
    )
    quote = Quote(
        symbol=sink, price=Money(amount=Decimal("10000"), currency=Currency.KRW),
        time=datetime.now(timezone.utc),
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {sink: quote}),
        targets=[TargetWeight(symbol=sink, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0.02"),
        cash_sink=sink,
    )
    plan = await rb.compute_plan()
    total_qty = sum(o.qty for o in plan.orders if o.symbol == sink)
    assert total_qty == Decimal("98")
    assert plan.expected_cash.amount >= Decimal("20000")  # buffer 유지


@pytest.mark.asyncio
async def test_cash_sink_invests_surplus_above_buffer():
    held = Symbol(ticker="005930")
    sink = Symbol(ticker="153130")
    # total=1,000,000, buffer 2%=20,000, investable=980,000
    # held: 50주×10,000=500,000; target held=0.5, sink=0.5
    # min_order_value=1,000,000 → 두 타깃 diff 모두 threshold 미달 → 일반 매수 없음
    # starting_cash = 500,000; reserve = 20,000
    # investable_cash = 480,000 → sink 48주 매수
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("500000"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=held, qty=Decimal("50"),
                avg_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
            ),
        ],
    )
    quote = Quote(
        symbol=sink, price=Money(amount=Decimal("10000"), currency=Currency.KRW),
        time=datetime.now(timezone.utc),
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {sink: quote}),
        targets=[TargetWeight(symbol=held, weight=Decimal("0.5")),
                 TargetWeight(symbol=sink, weight=Decimal("0.5"))],
        cash_buffer_rate=Decimal("0.02"),
        cash_sink=sink,
        min_order_value=Decimal("1000000"),  # 일반 pass에서 모든 diff skip
    )
    plan = await rb.compute_plan()
    sink_qty = sum(o.qty for o in plan.orders if o.symbol == sink)
    assert sink_qty == Decimal("48")  # 480,000 / 10,000 = 48
    assert plan.expected_cash.amount >= Decimal("20000")  # buffer 유지


@pytest.mark.asyncio
async def test_cash_sink_step_rate_throttles_surplus():
    sink = Symbol(ticker="153130")
    held = Symbol(ticker="005930")
    # Same setup as test_cash_sink_invests_surplus_above_buffer but step_rate=0.5.
    # held 50 * 10,000 = 500,000 is exactly its 50% target → no normal trade
    # (and min_order_value large enough to suppress normal pass like the sibling test).
    # surplus above buffer = 500,000 - 20,000 = 480,000; step_rate 0.5 → invest 240,000
    # → sink 24 shares at 10,000.
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("500000"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=held, qty=Decimal("50"),
                avg_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
            ),
        ],
    )
    quote = Quote(
        symbol=sink, price=Money(amount=Decimal("10000"), currency=Currency.KRW),
        time=datetime.now(timezone.utc),
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {sink: quote}),
        targets=[TargetWeight(symbol=held, weight=Decimal("0.5")),
                 TargetWeight(symbol=sink, weight=Decimal("0.5"))],
        cash_buffer_rate=Decimal("0.02"),
        cash_sink=sink,
        step_rate=Decimal("0.5"),
        min_order_value=Decimal("1000000"),  # suppress the normal rebalance pass
    )
    plan = await rb.compute_plan()
    sink_qty = sum(o.qty for o in plan.orders if o.symbol == sink)
    assert sink_qty == Decimal("24")  # 240,000 / 10,000, half of the 480,000 surplus


@pytest.mark.asyncio
async def test_cash_sink_flips_off_target_sell_to_buy():
    from tooja.core.enums import OrderSide

    sink = Symbol(ticker="153130")   # off-target holding → exit SELL 80, then cash_sink reinvests
    other = Symbol(ticker="005930")  # target 1.0 but unpriced → normal buy pass skips it
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("200000"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=sink, qty=Decimal("80"),
                avg_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
            ),
        ],
    )
    # other has no quote → unpriced → no normal buy.
    # _exit_off_targets emits SELL 80 for sink (off-target).
    # _apply_cash_sink: projected_cash = starting 200,000 + sink SELL 800,000 = 1,000,000.
    #   reserve = 1,000,000 * 0.02 = 20,000 → investable = 980,000 → add_qty = 98.
    #   existing SELL 80 → offset_qty = 80 (SELL removed) → flip BUY (98 - 80) = 18.
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),
        targets=[TargetWeight(symbol=other, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0.02"),
        cash_sink=sink,
    )
    plan = await rb.compute_plan()
    sink_orders = [o for o in plan.orders if o.symbol == sink]
    assert len(sink_orders) == 1
    assert sink_orders[0].side is OrderSide.BUY  # the off-target SELL was flipped to a BUY
    assert sink_orders[0].qty == Decimal("18")


@pytest.mark.asyncio
async def test_stochastic_convergence_over_many_rounds():
    """Repeatedly applying step_rate=0.5 + stochastic rounding converges to the integer-share optimum.

    Scenario: single asset, price 70,000 KRW, starting cash 1,000,000, 0 shares held.
    Target 100% weight, cash_buffer_rate=0, step_rate=0.5.
    Integer-share optimum: floor(1,000,000 / 70,000) = 14 shares (14 * 70,000 = 980,000;
    residual 20,000 < one share cost 70,000 → no further purchase possible).

    After converging, compute_plan must return no orders (the remaining gap of 20,000
    adjusted by step_rate 0.5 → 10,000 / 70,000 ≈ 0.14 shares → stochastic rounds to 0
    or 1, but 1 share costs 70,000 > 20,000 available cash → _apply_cash_budget floors to 0
    → empty order list).
    """
    import random as _random
    from tooja.core.enums import OrderSide

    sym = Symbol(ticker="005930")
    price = Decimal("70000")
    rng = _random.Random(12345)

    # mutable simulated account
    qty = Decimal("0")
    cash = Decimal("1000000")

    def make_broker(qty: Decimal, cash: Decimal):
        positions = []
        if qty != 0:
            positions.append(
                Position(
                    symbol=sym,
                    qty=qty,
                    avg_price=Money(amount=price, currency=Currency.KRW),
                    current_price=Money(amount=price, currency=Currency.KRW),
                )
            )
        total = cash + qty * price
        balance = Balance(
            total_asset=Money(amount=total, currency=Currency.KRW),
            cash=[Money(amount=cash, currency=Currency.KRW)],
            positions=positions,
        )
        quote = Quote(
            symbol=sym,
            price=Money(amount=price, currency=Currency.KRW),
            time=datetime.now(timezone.utc),
        )
        return _ScriptedBroker(balance, {sym: quote})

    final_plan = None
    for _ in range(60):
        rb = Rebalancer(
            broker=make_broker(qty, cash),
            targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
            cash_buffer_rate=Decimal("0"),
            step_rate=Decimal("0.5"),
            rng=rng,
        )
        plan = await rb.compute_plan()
        final_plan = plan
        if not plan.orders:
            break
        for o in plan.orders:
            if o.symbol == sym:
                if o.side is OrderSide.BUY:
                    qty += o.qty
                    cash -= o.qty * price
                else:
                    qty -= o.qty
                    cash += o.qty * price

    # Converged to the integer-share optimum: 14 shares, remaining cash too small for another share.
    assert qty == Decimal("14"), f"Expected 14 shares, got {qty}"
    assert cash == Decimal("20000"), f"Expected 20000 residual cash, got {cash}"
    # Rebalancer stops issuing orders once convergence is reached.
    assert final_plan is not None and final_plan.orders == []


@pytest.mark.asyncio
async def test_stochastic_convergence_with_tiny_step_rate():
    """Even with a very small step_rate (0.1), stochastic rounding still converges
    to the integer-share optimum. With plain floor this would stall forever (each
    round's adjusted gap < 1 share -> 0). Stochastic emits 1 share with small
    probability per round, so it converges over many rounds."""
    import random as _random
    from tooja.core.enums import OrderSide

    sym = Symbol(ticker="005930")
    price = Decimal("70000")
    rng = _random.Random(2024)

    qty = Decimal("0")
    cash = Decimal("1000000")

    def make_broker(qty: Decimal, cash: Decimal):
        positions = []
        if qty != 0:
            positions.append(Position(
                symbol=sym, qty=qty,
                avg_price=Money(amount=price, currency=Currency.KRW),
                current_price=Money(amount=price, currency=Currency.KRW),
            ))
        total = cash + qty * price
        balance = Balance(
            total_asset=Money(amount=total, currency=Currency.KRW),
            cash=[Money(amount=cash, currency=Currency.KRW)],
            positions=positions,
        )
        quote = Quote(symbol=sym, price=Money(amount=price, currency=Currency.KRW),
                      time=datetime.now(timezone.utc))
        return _ScriptedBroker(balance, {sym: quote})

    rounds_to_converge = None
    for r in range(2000):
        rb = Rebalancer(
            broker=make_broker(qty, cash),
            targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
            cash_buffer_rate=Decimal("0"),
            step_rate=Decimal("0.1"),
            rng=rng,
        )
        plan = await rb.compute_plan()
        for o in plan.orders:
            if o.symbol == sym:
                if o.side is OrderSide.BUY:
                    qty += o.qty
                    cash -= o.qty * price
                else:
                    qty -= o.qty
                    cash += o.qty * price
        if qty == Decimal("14"):
            rounds_to_converge = r
            break

    assert qty == Decimal("14"), f"did not converge; stuck at {qty} shares"
    assert rounds_to_converge is not None
    # Tiny step_rate means many more rounds than the ~6 rounds step=0.5 needs.
    assert rounds_to_converge > 6


@pytest.mark.asyncio
async def test_stochastic_convergence_with_extreme_tiny_step_rate():
    """step_rate=0.01: each round's adjusted gap is ~1% of the remaining gap, far
    below one share for most of the trajectory. Plain floor would never converge;
    stochastic rounding still reaches the 14-share integer optimum, just over many
    more rounds than step_rate 0.1 (~26) or 0.5 (~6)."""
    import random as _random
    from tooja.core.enums import OrderSide

    sym = Symbol(ticker="005930")
    price = Decimal("70000")
    rng = _random.Random(7)

    qty = Decimal("0")
    cash = Decimal("1000000")

    def make_broker(qty: Decimal, cash: Decimal):
        positions = []
        if qty != 0:
            positions.append(Position(
                symbol=sym, qty=qty,
                avg_price=Money(amount=price, currency=Currency.KRW),
                current_price=Money(amount=price, currency=Currency.KRW),
            ))
        total = cash + qty * price
        balance = Balance(
            total_asset=Money(amount=total, currency=Currency.KRW),
            cash=[Money(amount=cash, currency=Currency.KRW)],
            positions=positions,
        )
        quote = Quote(symbol=sym, price=Money(amount=price, currency=Currency.KRW),
                      time=datetime.now(timezone.utc))
        return _ScriptedBroker(balance, {sym: quote})

    rounds_to_converge = None
    for r in range(30000):
        rb = Rebalancer(
            broker=make_broker(qty, cash),
            targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
            cash_buffer_rate=Decimal("0"),
            step_rate=Decimal("0.01"),
            rng=rng,
        )
        plan = await rb.compute_plan()
        for o in plan.orders:
            if o.symbol == sym:
                if o.side is OrderSide.BUY:
                    qty += o.qty
                    cash -= o.qty * price
                else:
                    qty -= o.qty
                    cash += o.qty * price
        if qty == Decimal("14"):
            rounds_to_converge = r
            break

    assert qty == Decimal("14"), f"did not converge; stuck at {qty} shares after 30000 rounds"
    assert rounds_to_converge is not None


@pytest.mark.asyncio
async def test_cash_sink_does_not_stall_under_tiny_step_rate():
    import random as _random
    from tooja.core.enums import OrderSide
    sink = Symbol(ticker="153130")
    price = Decimal("70000")
    rng = _random.Random(123)
    qty = Decimal("0")
    cash = Decimal("1000000")  # all cash, no targets except sink → surplus goes to sink

    def make_broker(qty, cash):
        positions = []
        if qty != 0:
            positions.append(Position(symbol=sink, qty=qty,
                avg_price=Money(amount=price, currency=Currency.KRW),
                current_price=Money(amount=price, currency=Currency.KRW)))
        total = cash + qty * price
        balance = Balance(total_asset=Money(amount=total, currency=Currency.KRW),
            cash=[Money(amount=cash, currency=Currency.KRW)], positions=positions)
        quote = Quote(symbol=sink, price=Money(amount=price, currency=Currency.KRW),
            time=datetime.now(timezone.utc))
        return _ScriptedBroker(balance, {sink: quote})

    # sink is the only target at 100% AND the cash_sink. step_rate tiny.
    # Each round the step-scaled investable may be < 1 share, but stochastic rounding
    # means it still occasionally buys 1, converging over many rounds instead of stalling.
    for _ in range(3000):
        rb = Rebalancer(broker=make_broker(qty, cash),
            targets=[TargetWeight(symbol=sink, weight=Decimal("1.0"))],
            cash_buffer_rate=Decimal("0.02"), cash_sink=sink,
            step_rate=Decimal("0.05"), rng=rng)
        plan = await rb.compute_plan()
        if not plan.orders:
            break
        for o in plan.orders:
            if o.symbol == sink:
                if o.side is OrderSide.BUY:
                    qty += o.qty; cash -= o.qty * price
                else:
                    qty -= o.qty; cash += o.qty * price
    # buffer is 2% of total (~1,000,000) = ~20,000; max integer shares = floor(980,000/70,000) = 14
    # With old floor code this stalls at 4; stochastic rounding converges to 12 over 3000 rounds.
    assert qty >= Decimal("12")  # converged significantly, did NOT stall at low value


def test_rebalancer_rejects_negative_weight():
    sym1 = Symbol(ticker="005930")
    sym2 = Symbol(ticker="000660")
    broker = _ScriptedBroker(
        Balance(total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW)),
        {},
    )
    with pytest.raises(ValueError, match="non-negative"):
        Rebalancer(
            broker=broker,
            targets=[TargetWeight(symbol=sym1, weight=Decimal("-0.5")),
                     TargetWeight(symbol=sym2, weight=Decimal("1.5"))],
        )


def test_rebalancer_rejects_float_params():
    sym = Symbol(ticker="005930")
    targets = [TargetWeight(symbol=sym, weight=Decimal("1.0"))]
    broker = _ScriptedBroker(
        # minimal balance not needed; constructor must fail before any broker call
        Balance(
            total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        ),
        {},
    )
    for kw in ("cash_buffer_rate", "min_order_value", "drift_band", "step_rate"):
        with pytest.raises(TypeError, match="must be Decimal"):
            Rebalancer(broker=broker, targets=targets, **{kw: 0.5})


@pytest.mark.asyncio
async def test_cash_budget_partial_order_when_short_on_cash():
    a = Symbol(ticker="005930")  # 큰 괴리(우선)
    b = Symbol(ticker="035720")  # 작은 괴리
    balance = Balance(
        total_asset=Money(amount=Decimal("300000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("300000"), currency=Currency.KRW)],
        positions=[],
    )
    quotes = {
        a: Quote(symbol=a, price=Money(amount=Decimal("100000"), currency=Currency.KRW),
                 time=datetime.now(timezone.utc)),
        b: Quote(symbol=b, price=Money(amount=Decimal("100000"), currency=Currency.KRW),
                 time=datetime.now(timezone.utc)),
    }
    # target a 0.8(240,000→2주), b 0.2(60,000→0주: 60,000/100,000 floor 0 → skip)
    # a 우선 2주(200,000), 예산 300,000 내
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, quotes),
        targets=[
            TargetWeight(symbol=a, weight=Decimal("0.8")),
            TargetWeight(symbol=b, weight=Decimal("0.2")),
        ],
        cash_buffer_rate=Decimal("0"),
    )
    plan = await rb.compute_plan()
    buys = {o.symbol: o.qty for o in plan.orders}
    assert buys.get(a) == Decimal("2")
    total_buy = sum(o.qty * Decimal("100000") for o in plan.orders)
    assert total_buy <= Decimal("300000")


@pytest.mark.asyncio
async def test_no_trade_band_suppresses_subshare_churn():
    """No-trade band keeps orders empty when every gap is < one share's price.

    Setup:
      total=1,000,000, cash_buffer_rate=0 → investable=1,000,000
      price=70,000 per share
      sym1 weight 0.525 → target 525,000; held 7 shares = 490,000; gap +35,000
      sym2 weight 0.475 → target 475,000; held 7 shares = 490,000; gap -15,000

    Both gaps (35,000 and 15,000) are above the default min_order_value (10,000)
    but strictly below price (70,000 = one share). The no-trade band (abs(diff) < price
    → skip) must suppress all orders regardless of stochastic seed.

    Without the band: seed 99 produces ~18 trade rounds out of 50 (frac_sym1=0.25,
    frac_sym2~=0.107) — confirming this test fails against pre-band code.
    """
    import random as _random

    sym1 = Symbol(ticker="005930")
    sym2 = Symbol(ticker="000660")
    price = Decimal("70000")
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("20000"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=sym1,
                qty=Decimal("7"),
                avg_price=Money(amount=price, currency=Currency.KRW),
                current_price=Money(amount=price, currency=Currency.KRW),
            ),
            Position(
                symbol=sym2,
                qty=Decimal("7"),
                avg_price=Money(amount=price, currency=Currency.KRW),
                current_price=Money(amount=price, currency=Currency.KRW),
            ),
        ],
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),
        targets=[
            TargetWeight(symbol=sym1, weight=Decimal("0.525")),
            TargetWeight(symbol=sym2, weight=Decimal("0.475")),
        ],
        cash_buffer_rate=Decimal("0"),
        step_rate=Decimal("0.5"),
        rng=_random.Random(99),
    )
    # Run 50 plans against the same (fixed) broker state; the band must keep all empty.
    for _ in range(50):
        plan = await rb.compute_plan()
        assert plan.orders == [], f"no-trade band failed: {plan.orders}"


@pytest.mark.asyncio
async def test_lookup_price_handles_none_quote():
    sym = Symbol(ticker="005930")
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("1000000"), currency=Currency.KRW)],
        positions=[],
    )

    class _NoneMarket:
        _broker_name = "stub"
        async def get_quote(self, symbol):
            return None

    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
    )
    rb.broker.market = _NoneMarket()
    plan = await rb.compute_plan()   # must NOT raise
    assert plan.orders == []          # price unknown -> target skipped


@pytest.mark.asyncio
async def test_no_trade_band_allows_multishare_gap():
    """Gap clearly >= one share's price must still produce an order (band doesn't block real trades).

    0 shares held, 100% target, price 70,000, cash 1,000,000 → gap ~1,000,000 >> price.
    """
    sym = Symbol(ticker="005930")
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("1000000"), currency=Currency.KRW)],
        positions=[],
    )
    quote = Quote(
        symbol=sym,
        price=Money(amount=Decimal("70000"), currency=Currency.KRW),
        time=datetime.now(timezone.utc),
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {sym: quote}),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
    )
    plan = await rb.compute_plan()
    assert any(o.symbol == sym and o.qty > 0 for o in plan.orders)


def test_rebalancer_rejects_out_of_range_params():
    import pytest
    sym = Symbol(ticker="005930")
    targets = [TargetWeight(symbol=sym, weight=Decimal("1.0"))]
    broker = _ScriptedBroker(
        Balance(total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW)),
        {},
    )
    with pytest.raises(ValueError, match="cash_buffer_rate"):
        Rebalancer(broker=broker, targets=targets, cash_buffer_rate=Decimal("1.0"))
    with pytest.raises(ValueError, match="cash_buffer_rate"):
        Rebalancer(broker=broker, targets=targets, cash_buffer_rate=Decimal("-0.1"))
    with pytest.raises(ValueError, match="min_order_value"):
        Rebalancer(broker=broker, targets=targets, min_order_value=Decimal("-1"))
    with pytest.raises(ValueError, match="drift_band"):
        Rebalancer(broker=broker, targets=targets, drift_band=Decimal("-0.1"))
    with pytest.raises(ValueError, match="step_rate"):
        Rebalancer(broker=broker, targets=targets, step_rate=Decimal("1.5"))
    with pytest.raises(ValueError, match="step_rate"):
        Rebalancer(broker=broker, targets=targets, step_rate=Decimal("-0.1"))


@pytest.mark.asyncio
async def test_unpriced_position_does_not_inflate_starting_cash():
    # Regression: starting_cash must come from broker-reported cash, not
    # ``total - invested`` — an unpriced holding is absent from ``invested``
    # and would otherwise inflate the cash figure (here by B's 300,000).
    held = Symbol(ticker="005930")   # priced, 50 * 10,000 = 500,000
    dark = Symbol(ticker="000660")   # unpriced (no current_price, no quote)
    sink = Symbol(ticker="153130")   # cash sink, priced
    # total 1,000,000 = cash 200,000 + held 500,000 + dark 300,000
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("200000"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=held, qty=Decimal("50"),
                avg_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
            ),
            Position(
                symbol=dark, qty=Decimal("30"),
                avg_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
                current_price=None,  # broker gives no price and get_quote will fail
            ),
        ],
    )
    quote = Quote(
        symbol=sink, price=Money(amount=Decimal("10000"), currency=Currency.KRW),
        time=datetime.now(timezone.utc),
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {sink: quote}),  # no quote for `dark`
        targets=[TargetWeight(symbol=held, weight=Decimal("0.5")),
                 TargetWeight(symbol=dark, weight=Decimal("0.5"))],
        cash_buffer_rate=Decimal("0.02"),  # reserve = 20,000
        cash_sink=sink,
        min_order_value=Decimal("1000000"),  # suppress normal pass
    )
    plan = await rb.compute_plan()
    sink_qty = sum(o.qty for o in plan.orders if o.symbol == sink)
    # cash 200,000 - reserve 20,000 = 180,000 -> 18 shares.
    # Old (total - invested) would see 500,000 cash -> 48 shares.
    assert sink_qty == Decimal("18")


@pytest.mark.asyncio
async def test_unpriced_short_cover_reserves_cash_via_avg_price():
    from tooja.core.enums import OrderSide

    long_t = Symbol(ticker="005930")  # target, underweight -> BUY candidate
    short = Symbol(ticker="000660")   # off-target short, unpriced -> cover BUY
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("500000"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=long_t, qty=Decimal("50"),
                avg_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
            ),
            Position(  # unpriced short: cover BUY 10 must debit cash via avg_price
                symbol=short, qty=Decimal("-10"),
                avg_price=Money(amount=Decimal("10000"), currency=Currency.KRW),
                current_price=None,
            ),
        ],
    )
    quote = Quote(
        symbol=long_t, price=Money(amount=Decimal("10000"), currency=Currency.KRW),
        time=datetime.now(timezone.utc),
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),  # long_t priced from position; no quote needed
        targets=[TargetWeight(symbol=long_t, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
    )
    plan = await rb.compute_plan()
    # cover BUY 10 @ avg 10,000 = 100,000 reserved -> 400,000 left -> long_t buys 40.
    # Without the avg_price fallback the cover costs 0 -> long_t would buy 50.
    assert any(o.symbol == short and o.side is OrderSide.BUY and o.qty == Decimal("10")
               for o in plan.orders)
    long_buy = sum(o.qty for o in plan.orders
                   if o.symbol == long_t and o.side is OrderSide.BUY)
    assert long_buy == Decimal("40")
