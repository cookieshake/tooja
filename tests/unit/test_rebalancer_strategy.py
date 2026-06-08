import pytest
from datetime import datetime, timezone
from decimal import Decimal

from tooja.core.enums import Currency, RebalanceDirection
from tooja.core.models import Balance, Quote, Symbol
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
