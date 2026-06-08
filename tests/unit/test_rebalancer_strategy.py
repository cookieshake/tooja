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
