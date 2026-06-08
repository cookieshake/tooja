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
