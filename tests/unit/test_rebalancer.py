from decimal import Decimal

import pytest

from tooja.core import (
    AccountClient, AnalyticsClient, Broker, InfoClient,
    MarketClient, OrdersClient, RankingsClient, StreamClient, Symbol,
)
from tooja.portfolio import Rebalancer, RebalancePlan, TargetWeight


class _StubBroker(Broker):
    broker_name = "stub"

    def __init__(self):
        for name, cls in {
            "market": MarketClient, "account": AccountClient,
            "orders": OrdersClient, "info": InfoClient,
            "analytics": AnalyticsClient, "rankings": RankingsClient,
            "stream": StreamClient,
        }.items():
            inst = cls.__new__(cls)
            inst._broker_name = "stub"
            setattr(self, name, inst)

    async def open(self): pass
    async def close(self): pass


def test_target_weight_construction():
    tw = TargetWeight(symbol=Symbol(ticker="005930"), weight=Decimal("0.3"))
    assert tw.weight == Decimal("0.3")


def test_rebalancer_accepts_broker_and_targets_list():
    rb = Rebalancer(
        broker=_StubBroker(),
        targets=[
            TargetWeight(symbol=Symbol(ticker="005930"), weight=Decimal("0.5")),
            TargetWeight(symbol=Symbol(ticker="035720"), weight=Decimal("0.5")),
        ],
    )
    assert len(rb.targets) == 2


def test_rebalancer_weight_sum_must_be_close_to_one():
    with pytest.raises(ValueError, match="weights must sum"):
        Rebalancer(
            broker=_StubBroker(),
            targets=[TargetWeight(symbol=Symbol(ticker="005930"), weight=Decimal("0.5"))],
        )


def test_rebalancer_rejects_duplicate_symbols():
    """Duplicate Symbol entries are rejected — avoids accidental duplicate orders."""
    with pytest.raises(ValueError, match="duplicate symbols"):
        Rebalancer(
            broker=_StubBroker(),
            targets=[
                TargetWeight(symbol=Symbol(ticker="005930"), weight=Decimal("0.5")),
                TargetWeight(symbol=Symbol(ticker="005930"), weight=Decimal("0.5")),
            ],
        )


def test_rebalance_plan_dataclass():
    plan = RebalancePlan(orders=[], expected_drift=Decimal("0.02"))
    assert plan.expected_drift == Decimal("0.02")


@pytest.mark.asyncio
async def test_compute_plan_returns_empty_when_no_positions_and_no_quotes():
    """A stub broker exposes no balance — compute_plan should raise UnsupportedOperation."""
    from tooja.core.errors import UnsupportedOperation

    rb = Rebalancer(
        broker=_StubBroker(),
        targets=[TargetWeight(symbol=Symbol(ticker="005930"), weight=Decimal("1.0"))],
    )
    with pytest.raises(UnsupportedOperation):
        await rb.compute_plan()


class _ScriptedAccount:
    _broker_name = "stub"
    def __init__(self, balance):
        self._balance = balance
    async def get_balance(self):
        return self._balance


class _ScriptedMarket:
    _broker_name = "stub"
    def __init__(self, quote_map):
        self._quotes = quote_map
    async def get_quote(self, symbol):
        return self._quotes[symbol]


class _ScriptedOrders:
    _broker_name = "stub"
    def __init__(self):
        self.received = []
    async def create(self, req):
        from datetime import datetime, timezone

        from tooja.core.enums import OrderStatus
        from tooja.core.models import Order
        self.received.append(req)
        return Order(
            order_id=f"DRY-{len(self.received)}",
            symbol=req.symbol, side=req.side, qty=req.qty, type=req.type,
            status=OrderStatus.PENDING,
            submitted_at=datetime.now(timezone.utc),
        )


class _ScriptedBroker(_StubBroker):
    def __init__(self, balance, quotes):
        super().__init__()
        self.account = _ScriptedAccount(balance)
        self.market = _ScriptedMarket(quotes)
        self.orders = _ScriptedOrders()


@pytest.mark.asyncio
async def test_compute_plan_buys_to_reach_target():
    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance, Quote
    from tooja.core.money import Money
    from datetime import datetime, timezone

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
    assert len(plan.orders) == 1
    assert plan.orders[0].side == OrderSide.BUY
    # 1,000,000 / 70,000 = 14.28 → 14 shares
    assert plan.orders[0].qty == Decimal("14")


@pytest.mark.asyncio
async def test_compute_plan_skips_below_min_order_value():
    from tooja.core.enums import Currency
    from tooja.core.models import Balance, Position, Quote
    from tooja.core.money import Money
    from datetime import datetime, timezone

    sym = Symbol(ticker="005930")
    other = Symbol(ticker="035720")
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("500000"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=sym, qty=Decimal("7"),
                avg_price=Money(amount=Decimal("70000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("70000"), currency=Currency.KRW),
            ),
        ],
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),
        targets=[
            TargetWeight(symbol=sym, weight=Decimal("0.49")),
            TargetWeight(symbol=other, weight=Decimal("0.51")),
        ],
        cash_buffer_rate=Decimal("0"),
        min_order_value=Decimal("10000"),
    )
    quotes = {other: Quote(
        symbol=other,
        price=Money(amount=Decimal("50000"), currency=Currency.KRW),
        time=datetime.now(timezone.utc),
    )}
    rb.broker.market._quotes.update(quotes)
    plan = await rb.compute_plan()
    # Existing position diff (~490,000 target vs 490,000 actual) → < min → no order
    # New symbol diff (510,000 target vs 0 actual) → 10 shares buy
    assert any(o.symbol == other for o in plan.orders)


@pytest.mark.asyncio
async def test_execute_calls_orders_create():
    from tooja.core.enums import Currency
    from tooja.core.models import Balance, MarketOrder
    from tooja.core.enums import OrderSide
    from tooja.core.money import Money

    sym = Symbol(ticker="005930")
    plan = RebalancePlan(
        orders=[MarketOrder(symbol=sym, side=OrderSide.BUY, qty=Decimal("10"))],
        expected_drift=Decimal("0.1"),
    )
    balance = Balance(
        total_asset=Money(amount=Decimal("0"), currency=Currency.KRW),
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
    )
    out = await rb.execute(plan)
    assert len(out) == 1
    assert rb.broker.orders.received[0].symbol == sym
