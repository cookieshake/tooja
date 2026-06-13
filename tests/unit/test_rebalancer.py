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
    plan = RebalancePlan(trades=[], expected_drift=Decimal("0.02"))
    assert plan.expected_drift == Decimal("0.02")


def test_planned_trade_model():
    from tooja.core.enums import OrderSide
    from tooja.portfolio.rebalance.models import PlannedTrade

    t = PlannedTrade(symbol=Symbol(ticker="005930"), side=OrderSide.BUY, qty=Decimal("3"))
    assert t.symbol.ticker == "005930"
    assert t.side is OrderSide.BUY
    assert t.qty == Decimal("3")


def test_rebalance_plan_carries_trades():
    from tooja.core.enums import OrderSide
    from tooja.portfolio.rebalance.models import PlannedTrade

    t = PlannedTrade(symbol=Symbol(ticker="005930"), side=OrderSide.SELL, qty=Decimal("1"))
    plan = RebalancePlan(trades=[t], expected_drift=Decimal("0"))
    assert plan.trades == [t]


def test_rebalance_plan_carries_expected_total():
    from tooja.core.enums import Currency
    from tooja.core.money import Money
    plan = RebalancePlan(
        trades=[],
        expected_drift=Decimal("0"),
        expected_total=Money(amount=Decimal("5900"), currency=Currency.USD),
    )
    assert plan.expected_total == Money(amount=Decimal("5900"), currency=Currency.USD)


def test_rebalance_plan_expected_total_defaults_none():
    plan = RebalancePlan(trades=[], expected_drift=Decimal("0"))
    assert plan.expected_total is None


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


class _FillTrackingOrders(_ScriptedOrders):
    """Tracks created orders so execute()'s fill polling can resolve them."""
    def __init__(self, fill_status=None):
        super().__init__()
        from tooja.core.enums import OrderStatus
        self._fill_status = fill_status or OrderStatus.FILLED
        self._by_id = {}

    async def create(self, req):
        order = await super().create(req)
        self._by_id[order.order_id] = order
        return order

    async def get(self, order_id):
        return self._by_id[order_id].model_copy(update={"status": self._fill_status})




def _usd_quote_map(sym, price):
    """Quote map for execute()-time overseas limit pricing in USD tests."""
    from datetime import datetime, timezone

    from tooja.core.enums import Currency
    from tooja.core.models import Quote
    from tooja.core.money import Money
    return {sym: Quote(
        symbol=sym,
        price=Money(amount=Decimal(price), currency=Currency.USD),
        time=datetime.now(timezone.utc),
    )}

def test_rebalancer_accepts_fill_poll_params():
    rb = Rebalancer(
        broker=_StubBroker(),
        targets=[
            TargetWeight(symbol=Symbol(ticker="005930"), weight=Decimal("0.5")),
            TargetWeight(symbol=Symbol(ticker="035720"), weight=Decimal("0.5")),
        ],
        fill_poll_interval=0.2,
        fill_timeout=10.0,
    )
    assert rb.fill_poll_interval == 0.2
    assert rb.fill_timeout == 10.0


def test_rebalancer_rejects_non_positive_fill_timeout():
    with pytest.raises(ValueError, match="fill_timeout"):
        Rebalancer(
            broker=_StubBroker(),
            targets=[TargetWeight(symbol=Symbol(ticker="005930"), weight=Decimal("1.0"))],
            fill_timeout=0.0,
        )


def test_rebalancer_rejects_non_positive_fill_poll_interval():
    with pytest.raises(ValueError, match="fill_poll_interval"):
        Rebalancer(
            broker=_StubBroker(),
            targets=[TargetWeight(symbol=Symbol(ticker="005930"), weight=Decimal("1.0"))],
            fill_poll_interval=0.0,
        )


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
    assert len(plan.trades) == 1
    assert plan.trades[0].side == OrderSide.BUY
    # 1,000,000 / 70,000 = 14.28 → 14 shares
    assert plan.trades[0].qty == Decimal("14")


@pytest.mark.asyncio
async def test_load_account_skips_position_on_unmapped_exchange(monkeypatch):
    """A holding on an exchange with no currency mapping is filtered out, not crashed on."""
    from tooja.core.enums import Currency, Exchange, OrderSide
    from tooja.core.models import Balance, Position, Quote
    from tooja.core.money import Money
    from tooja.core import markets
    from datetime import datetime, timezone

    # Simulate an exchange present in the enum but missing its currency mapping
    # (e.g. a market added to the enum before its currency is registered).
    monkeypatch.delitem(markets._EXCHANGE_CURRENCY, Exchange.SEHK)

    sym = Symbol(ticker="005930")  # KRX → KRW sleeve
    unmapped = Symbol(ticker="0700", exchange=Exchange.SEHK)
    balance = Balance(
        cash=[Money(amount=Decimal("1000000"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=unmapped, qty=Decimal("5"),
                avg_price=Money(amount=Decimal("300"), currency=Currency.HKD),
                current_price=Money(amount=Decimal("320"), currency=Currency.HKD),
            ),
        ],
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
    plan = await rb.compute_plan()  # must not raise KeyError on the SEHK holding
    # The unmapped SEHK holding is excluded from the KRW sleeve; only the KRW
    # target is planned (1,000,000 / 70,000 = 14 shares).
    assert [o.symbol for o in plan.trades] == [sym]
    assert plan.trades[0].side == OrderSide.BUY
    assert plan.trades[0].qty == Decimal("14")


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
    assert any(o.symbol == other for o in plan.trades)


@pytest.mark.asyncio
async def test_expected_drift_is_post_rebalance_not_current():
    """Regression: expected_drift means residual drift after the planned
    trades execute, not the current (pre-rebalance) drift."""
    from datetime import datetime, timezone
    from tooja.core.enums import Currency
    from tooja.core.models import Balance, Position, Quote
    from tooja.core.money import Money

    sym = Symbol(ticker="005930")
    # Start with 0 in target sym, 1,000,000 cash, target=100%.
    # Plan should buy ~14 shares (14*70k=980k <= 1M investable).
    # Residual = abs((980k / 1M) - 1.0) = 0.02 — small, not 1.0.
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
    assert len(plan.trades) == 1
    # 14 * 70,000 = 980,000 → residual = 20,000 / 1,000,000 = 0.02.
    assert plan.expected_drift == Decimal("0.02")


@pytest.mark.asyncio
async def test_expected_drift_zero_when_already_balanced():
    """No trades emitted → residual drift = 0 (already at target)."""
    from tooja.core.enums import Currency
    from tooja.core.models import Balance, Position
    from tooja.core.money import Money

    sym = Symbol(ticker="005930")
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
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
    )
    plan = await rb.compute_plan()
    assert plan.trades == []
    assert plan.expected_drift == Decimal("0")


@pytest.mark.asyncio
async def test_compute_plan_skips_target_with_unpriced_holding():
    """Critical regression: if an existing target position has no resolvable
    price, compute_plan must NOT generate a BUY based on actual=0. Doing so
    would attempt to invest the full target_value, doubling the position."""
    from tooja.core.enums import Currency
    from tooja.core.models import Balance, Position
    from tooja.core.money import Money

    sym = Symbol(ticker="005930")
    balance = Balance(
        total_asset=Money(amount=Decimal("100000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("0"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=sym, qty=Decimal("100"),
                avg_price=Money(amount=Decimal("70000"), currency=Currency.KRW),
                current_price=None,  # KIS sometimes omits — halted, etc.
            ),
        ],
    )

    # Broker whose market.get_quote also fails (unpriced everywhere).
    class _FailingMarket:
        _broker_name = "stub"
        async def get_quote(self, symbol):
            raise RuntimeError("price unavailable")

    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
    )
    rb.broker.market = _FailingMarket()
    plan = await rb.compute_plan()
    # No order should be emitted — the target is skipped because price is unknown.
    assert plan.trades == []


@pytest.mark.asyncio
async def test_compute_plan_rejects_zero_sleeve_total():
    # Migrated: total is now computed from sleeve cash + positions, not total_asset.
    # A balance with no KRW cash and no KRW positions → sleeve total = 0 → raises.
    from tooja.core.enums import Currency
    from tooja.core.models import Balance
    from tooja.core.money import Money

    sym = Symbol(ticker="005930")
    balance = Balance(
        total_asset=Money(amount=Decimal("0"), currency=Currency.KRW),
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
    )
    with pytest.raises(ValueError, match="no positive total"):
        await rb.compute_plan()


@pytest.mark.asyncio
async def test_compute_plan_exits_position_without_current_price():
    """Regression: positions whose current_price is None must still be exited."""
    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance, Position
    from tooja.core.money import Money

    sym = Symbol(ticker="005930")
    other = Symbol(ticker="035720")
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("0"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=other, qty=Decimal("5"),
                avg_price=Money(amount=Decimal("50000"), currency=Currency.KRW),
                current_price=None,  # KIS sometimes omits current price for halted/illiquid names.
            ),
        ],
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
    )
    rb.broker.market._quotes[sym] = type("_Q", (), {
        "price": Money(amount=Decimal("70000"), currency=Currency.KRW),
    })()
    plan = await rb.compute_plan()
    # Off-target position with qty=5 must be in the SELL orders.
    exits = [o for o in plan.trades if o.symbol == other and o.side is OrderSide.SELL]
    assert len(exits) == 1
    assert exits[0].qty == Decimal("5")


@pytest.mark.asyncio
async def test_off_target_short_position_closed_by_buy():
    """Regression: off-target short position must be closed with a BUY for
    abs(qty), not silently left open by a `qty <= 0` skip."""
    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance, Position
    from tooja.core.money import Money

    keep = Symbol(ticker="005930")  # target
    short = Symbol(ticker="035720")  # off-target short
    # Migrated: sleeve total = cash + positions. Short position has qty<0 → negative
    # contribution. Add cash=1,000,000 so sleeve_total > 0 (1,000,000 - 250,000 = 750,000).
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("1000000"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=short, qty=Decimal("-5"),
                avg_price=Money(amount=Decimal("50000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("50000"), currency=Currency.KRW),
            ),
        ],
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),
        targets=[TargetWeight(symbol=keep, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
    )
    plan = await rb.compute_plan()
    exits = [o for o in plan.trades if o.symbol == short]
    assert len(exits) == 1
    assert exits[0].side is OrderSide.BUY
    assert exits[0].qty == Decimal("5")


@pytest.mark.asyncio
async def test_unpriced_short_position_marked_unpriced_not_dropped():
    """Regression: a short position (qty<0) with unresolvable price must be
    flagged unpriced, not silently dropped. Otherwise the matching target
    would treat actual=0 and emit a runaway BUY."""
    from tooja.core.enums import Currency
    from tooja.core.models import Balance, Position
    from tooja.core.money import Money

    sym = Symbol(ticker="005930")
    # Migrated: sleeve total = cash + positions. Short (qty=-10) × avg_price(70,000) = -700,000.
    # Add cash=1,000,000 so sleeve_total = 300,000 > 0. Test intent: unpriced short is flagged,
    # so target is skipped and no BUY is emitted.
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("1000000"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=sym, qty=Decimal("-10"),  # short
                avg_price=Money(amount=Decimal("70000"), currency=Currency.KRW),
                current_price=None,
            ),
        ],
    )

    class _FailingMarket:
        _broker_name = "stub"
        async def get_quote(self, symbol):
            raise RuntimeError("price unavailable")

    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
    )
    rb.broker.market = _FailingMarket()
    plan = await rb.compute_plan()
    # Unpriced short → target skipped, no BUY emitted.
    assert plan.trades == []


@pytest.mark.asyncio
async def test_plan_sells_before_buys():
    """Cash from SELLs must be freed before BUYs hit, otherwise the broker
    rejects them for insufficient funds."""
    from datetime import datetime, timezone

    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance, Position, Quote
    from tooja.core.money import Money

    keep = Symbol(ticker="005930")    # target=100%, currently 0
    drop = Symbol(ticker="035720")    # off-target, currently fully invested
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("0"), currency=Currency.KRW)],
        positions=[
            Position(
                symbol=drop, qty=Decimal("20"),
                avg_price=Money(amount=Decimal("50000"), currency=Currency.KRW),
                current_price=Money(amount=Decimal("50000"), currency=Currency.KRW),
            ),
        ],
    )
    quote = Quote(
        symbol=keep,
        price=Money(amount=Decimal("70000"), currency=Currency.KRW),
        time=datetime.now(timezone.utc),
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {keep: quote}),
        targets=[TargetWeight(symbol=keep, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
    )
    plan = await rb.compute_plan()
    sides = [o.side for o in plan.trades]
    # All SELLs precede the first BUY.
    first_buy_idx = next((i for i, s in enumerate(sides) if s is OrderSide.BUY), len(sides))
    assert all(s is OrderSide.SELL for s in sides[:first_buy_idx])


@pytest.mark.asyncio
async def test_execute_recaps_buys_to_real_cash():
    """Plan assumed ~980k cash; real cash is only 500k → buy shrinks to what fits."""
    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance
    from tooja.portfolio.rebalance.models import PlannedTrade
    from tooja.core.money import Money
    from tooja.portfolio import ExpectedHolding

    sym = Symbol(ticker="005930")
    plan = RebalancePlan(
        trades=[PlannedTrade(symbol=sym, side=OrderSide.BUY, qty=Decimal("14"))],
        expected_drift=Decimal("0.02"),
        expected_holdings=[
            ExpectedHolding(symbol=sym, qty=Decimal("14"),
                            price=Decimal("70000"), value=Decimal("980000")),
        ],
        expected_cash=Money(amount=Decimal("20000"), currency=Currency.KRW),
    )
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("500000"), currency=Currency.KRW)],  # real cash < plan
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
    )
    rb.broker.orders = _FillTrackingOrders()
    out = await rb.execute(plan)
    # floor(500000 / 70000) = 7 shares
    assert len(out) == 1
    submitted = rb.broker.orders.received
    assert submitted[0].side is OrderSide.BUY
    assert submitted[0].qty == Decimal("7")


@pytest.mark.asyncio
async def test_execute_buy_only_plan_skips_sell_phase():
    """No SELLs → go straight to cash re-read + buys; full buy fits."""
    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance
    from tooja.portfolio.rebalance.models import PlannedTrade
    from tooja.core.money import Money
    from tooja.portfolio import ExpectedHolding

    sym = Symbol(ticker="005930")
    plan = RebalancePlan(
        trades=[PlannedTrade(symbol=sym, side=OrderSide.BUY, qty=Decimal("10"))],
        expected_drift=Decimal("0.0"),
        expected_holdings=[
            ExpectedHolding(symbol=sym, qty=Decimal("10"),
                            price=Decimal("70000"), value=Decimal("700000")),
        ],
        expected_cash=Money(amount=Decimal("300000"), currency=Currency.KRW),
    )
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("1000000"), currency=Currency.KRW)],
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
    )
    rb.broker.orders = _FillTrackingOrders()
    out = await rb.execute(plan)
    assert len(out) == 1
    assert rb.broker.orders.received[0].qty == Decimal("10")


@pytest.mark.asyncio
async def test_execute_recaps_buys_with_fresh_quote():
    """Buy price rose since planning (70k → 100k) → fewer shares fit real cash."""
    from datetime import datetime, timezone
    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance, Quote
    from tooja.portfolio.rebalance.models import PlannedTrade
    from tooja.core.money import Money
    from tooja.portfolio import ExpectedHolding

    sym = Symbol(ticker="005930")
    plan = RebalancePlan(
        trades=[PlannedTrade(symbol=sym, side=OrderSide.BUY, qty=Decimal("14"))],
        expected_drift=Decimal("0.0"),
        expected_holdings=[
            ExpectedHolding(symbol=sym, qty=Decimal("14"),
                            price=Decimal("70000"), value=Decimal("980000")),
        ],
        expected_cash=Money(amount=Decimal("0"), currency=Currency.KRW),
    )
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("1000000"), currency=Currency.KRW)],
    )
    fresh = Quote(
        symbol=sym,
        price=Money(amount=Decimal("100000"), currency=Currency.KRW),  # risen
        time=datetime.now(timezone.utc),
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {sym: fresh}),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
    )
    rb.broker.orders = _FillTrackingOrders()
    await rb.execute(plan)
    # floor(1,000,000 / 100,000) = 10 shares, not the planned 14.
    assert rb.broker.orders.received[0].qty == Decimal("10")


@pytest.mark.asyncio
async def test_execute_calls_orders_create():
    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance
    from tooja.portfolio.rebalance.models import PlannedTrade
    from tooja.core.money import Money
    from tooja.portfolio import ExpectedHolding

    sym = Symbol(ticker="005930")
    plan = RebalancePlan(
        trades=[PlannedTrade(symbol=sym, side=OrderSide.BUY, qty=Decimal("10"))],
        expected_drift=Decimal("0.1"),
        expected_holdings=[
            ExpectedHolding(symbol=sym, qty=Decimal("10"),
                            price=Decimal("70000"), value=Decimal("700000")),
        ],
        expected_cash=Money(amount=Decimal("300000"), currency=Currency.KRW),
    )
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("1000000"), currency=Currency.KRW)],
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
    )
    rb.broker.orders = _FillTrackingOrders()
    out = await rb.execute(plan)
    assert len(out) == 1
    assert rb.broker.orders.received[0].symbol == sym
    assert rb.broker.orders.received[0].qty == Decimal("10")


@pytest.mark.asyncio
async def test_execute_proceeds_on_fill_timeout():
    """Sells never reach terminal status → execute waits fill_timeout then buys."""
    from tooja.core.enums import Currency, OrderSide, OrderStatus
    from tooja.core.models import Balance
    from tooja.portfolio.rebalance.models import PlannedTrade
    from tooja.core.money import Money
    from tooja.portfolio import ExpectedHolding

    sell_sym = Symbol(ticker="035720")
    buy_sym = Symbol(ticker="005930")
    plan = RebalancePlan(
        trades=[
            PlannedTrade(symbol=sell_sym, side=OrderSide.SELL, qty=Decimal("5")),
            PlannedTrade(symbol=buy_sym, side=OrderSide.BUY, qty=Decimal("3")),
        ],
        expected_drift=Decimal("0.0"),
        expected_holdings=[
            ExpectedHolding(symbol=buy_sym, qty=Decimal("3"),
                            price=Decimal("70000"), value=Decimal("210000")),
        ],
        expected_cash=Money(amount=Decimal("0"), currency=Currency.KRW),
    )
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("500000"), currency=Currency.KRW)],
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),
        targets=[TargetWeight(symbol=buy_sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
        fill_poll_interval=0.01,
        fill_timeout=0.05,  # never fills → times out fast
    )
    rb.broker.orders = _FillTrackingOrders(fill_status=OrderStatus.OPEN)  # stays non-terminal
    out = await rb.execute(plan)
    sides = [o.side for o in rb.broker.orders.received]
    assert OrderSide.SELL in sides and OrderSide.BUY in sides
    # SELL submitted before BUY.
    assert sides.index(OrderSide.SELL) < sides.index(OrderSide.BUY)


@pytest.mark.asyncio
async def test_execute_continues_when_a_sell_submit_fails():
    """One SELL raises on create → it's skipped; the BUY still executes."""
    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance
    from tooja.portfolio.rebalance.models import PlannedTrade
    from tooja.core.money import Money
    from tooja.portfolio import ExpectedHolding

    bad_sell = Symbol(ticker="035720")
    buy_sym = Symbol(ticker="005930")
    plan = RebalancePlan(
        trades=[
            PlannedTrade(symbol=bad_sell, side=OrderSide.SELL, qty=Decimal("5")),
            PlannedTrade(symbol=buy_sym, side=OrderSide.BUY, qty=Decimal("3")),
        ],
        expected_drift=Decimal("0.0"),
        expected_holdings=[
            ExpectedHolding(symbol=buy_sym, qty=Decimal("3"),
                            price=Decimal("70000"), value=Decimal("210000")),
        ],
        expected_cash=Money(amount=Decimal("0"), currency=Currency.KRW),
    )
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("500000"), currency=Currency.KRW)],
    )

    class _FlakyOrders(_FillTrackingOrders):
        async def create(self, req):
            if req.side is OrderSide.SELL:
                raise RuntimeError("broker rejected sell")
            return await super().create(req)

    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),
        targets=[TargetWeight(symbol=buy_sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
    )
    rb.broker.orders = _FlakyOrders()
    out = await rb.execute(plan)
    # The failed SELL is absent; the BUY went through.
    assert all(o.side is OrderSide.BUY for o in out)
    assert len(out) == 1
    assert out[0].side is OrderSide.BUY


@pytest.mark.asyncio
async def test_execute_recaps_buys_in_usd():
    """USD-denominated plan/balance: recap math must work in USD, not assume KRW."""
    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance
    from tooja.portfolio.rebalance.models import PlannedTrade
    from tooja.core.money import Money
    from tooja.portfolio import ExpectedHolding

    sym = Symbol.parse("NASD:AAPL")
    plan = RebalancePlan(
        trades=[PlannedTrade(symbol=sym, side=OrderSide.BUY, qty=Decimal("10"))],
        expected_drift=Decimal("0.0"),
        expected_holdings=[
            ExpectedHolding(symbol=sym, qty=Decimal("10"),
                            price=Decimal("200"), value=Decimal("2000")),
        ],
        expected_cash=Money(amount=Decimal("0"), currency=Currency.USD),
    )
    balance = Balance(
        total_asset=Money(amount=Decimal("2000"), currency=Currency.USD),
        cash=[Money(amount=Decimal("1500"), currency=Currency.USD)],  # real cash < plan
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, _usd_quote_map(sym, "200")),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
        min_order_value=Decimal("100"),
    )
    rb.broker.orders = _FillTrackingOrders()
    out = await rb.execute(plan)
    # floor(1500 / 200) = 7 shares
    assert len(out) == 1
    assert rb.broker.orders.received[0].qty == Decimal("7")


@pytest.mark.asyncio
async def test_recap_uses_sleeve_currency_when_no_expected_cash():
    """expected_cash=None must not silently assume KRW — the budget currency is
    the sleeve currency derived from the targets, NOT balance.total_asset
    (which is the whole-account FX rollup, here adversarially KRW)."""
    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance
    from tooja.portfolio.rebalance.models import PlannedTrade
    from tooja.core.money import Money
    from tooja.portfolio import ExpectedHolding

    sym = Symbol.parse("NASD:AAPL")
    plan = RebalancePlan(
        trades=[PlannedTrade(symbol=sym, side=OrderSide.BUY, qty=Decimal("5"))],
        expected_drift=Decimal("0.0"),
        expected_holdings=[
            ExpectedHolding(symbol=sym, qty=Decimal("5"),
                            price=Decimal("200"), value=Decimal("1000")),
        ],
        expected_cash=None,
    )
    balance = Balance(
        total_asset=Money(amount=Decimal("2600000"), currency=Currency.KRW),  # FX rollup
        cash=[Money(amount=Decimal("2000"), currency=Currency.USD)],
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, _usd_quote_map(sym, "200")),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
        min_order_value=Decimal("100"),
    )
    rb.broker.orders = _FillTrackingOrders()
    await rb.execute(plan)
    # With a KRW fallback the USD cash entry is never found → budget 0 → buy dropped.
    assert len(rb.broker.orders.received) == 1
    assert rb.broker.orders.received[0].qty == Decimal("5")


@pytest.mark.asyncio
async def test_recap_never_budgets_other_currency_cash():
    """Regression: a USD sleeve with only KRW cash has budget 0. The old code
    derived the budget currency from balance.total_asset (KRW rollup) and spent
    the KRW *amount* against USD-priced buys — submitting a $2,000 buy with $0."""
    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance
    from tooja.portfolio.rebalance.models import PlannedTrade
    from tooja.core.money import Money
    from tooja.portfolio import ExpectedHolding

    sym = Symbol.parse("NASD:AAPL")
    plan = RebalancePlan(
        trades=[PlannedTrade(symbol=sym, side=OrderSide.BUY, qty=Decimal("10"))],
        expected_drift=Decimal("0.0"),
        expected_holdings=[
            ExpectedHolding(symbol=sym, qty=Decimal("10"),
                            price=Decimal("200"), value=Decimal("2000")),
        ],
        expected_cash=None,
    )
    balance = Balance(
        total_asset=Money(amount=Decimal("500000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("500000"), currency=Currency.KRW)],  # zero USD
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, _usd_quote_map(sym, "200")),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0"),
        min_order_value=Decimal("100"),
    )
    rb.broker.orders = _FillTrackingOrders()
    await rb.execute(plan)
    assert rb.broker.orders.received == []


@pytest.mark.asyncio
async def test_recap_skips_buffer_when_expected_total_is_none():
    """With no expected_total on the plan, _recap_buys has no buffer base, so it
    applies none and spends the full real cash."""
    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance
    from tooja.portfolio.rebalance.models import PlannedTrade
    from tooja.core.money import Money
    from tooja.portfolio import ExpectedHolding

    sym = Symbol.parse("NASD:AAPL")
    plan = RebalancePlan(
        trades=[PlannedTrade(symbol=sym, side=OrderSide.BUY, qty=Decimal("10"))],
        expected_drift=Decimal("0.0"),
        expected_holdings=[
            ExpectedHolding(symbol=sym, qty=Decimal("10"),
                            price=Decimal("200"), value=Decimal("2000")),
        ],
        expected_cash=Money(amount=Decimal("0"), currency=Currency.USD),
        # expected_total intentionally omitted (None)
    )
    balance = Balance(
        total_asset=Money(amount=Decimal("2600000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("2000"), currency=Currency.USD)],
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, _usd_quote_map(sym, "200")),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0.02"),
        min_order_value=Decimal("100"),
    )
    rb.broker.orders = _FillTrackingOrders()
    await rb.execute(plan)
    # No expected_total -> no buffer -> full 10-share buy fits (10*200 == 2000).
    assert len(rb.broker.orders.received) == 1
    assert rb.broker.orders.received[0].qty == Decimal("10")


@pytest.mark.asyncio
async def test_recap_skips_buffer_when_expected_total_currency_differs():
    """A buffer base reported in a different currency than the sleeve must not be
    subtracted verbatim — the currency guard skips it."""
    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance
    from tooja.portfolio.rebalance.models import PlannedTrade
    from tooja.core.money import Money
    from tooja.portfolio import ExpectedHolding

    sym = Symbol.parse("NASD:AAPL")
    plan = RebalancePlan(
        trades=[PlannedTrade(symbol=sym, side=OrderSide.BUY, qty=Decimal("10"))],
        expected_drift=Decimal("0.0"),
        expected_holdings=[
            ExpectedHolding(symbol=sym, qty=Decimal("10"),
                            price=Decimal("200"), value=Decimal("2000")),
        ],
        expected_cash=Money(amount=Decimal("0"), currency=Currency.USD),
        # expected_total reported in KRW while the sleeve is USD -> guard skips it.
        expected_total=Money(amount=Decimal("2600000"), currency=Currency.KRW),
    )
    balance = Balance(
        total_asset=Money(amount=Decimal("2600000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("2000"), currency=Currency.USD)],
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, _usd_quote_map(sym, "200")),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        cash_buffer_rate=Decimal("0.02"),
        min_order_value=Decimal("100"),
    )
    rb.broker.orders = _FillTrackingOrders()
    await rb.execute(plan)
    # Buffer base currency (KRW) != sleeve currency (USD) -> buffer skipped ->
    # full 10-share buy (subtracting 2,600,000*0.02 KRW from 2,000 USD is invalid).
    assert len(rb.broker.orders.received) == 1
    assert rb.broker.orders.received[0].qty == Decimal("10")


def test_rebalancer_derives_usd_currency_from_targets():
    from tooja.core.enums import Currency
    rb = Rebalancer(
        broker=_StubBroker(),
        targets=[
            TargetWeight(symbol=Symbol.parse("NASD:AAPL"), weight=Decimal("0.5")),
            TargetWeight(symbol=Symbol.parse("NYSE:IBM"), weight=Decimal("0.5")),
        ],
    )
    assert rb.currency == Currency.USD


def test_rebalancer_derives_krw_currency_from_targets():
    from tooja.core.enums import Currency
    rb = Rebalancer(
        broker=_StubBroker(),
        targets=[TargetWeight(symbol=Symbol(ticker="005930"), weight=Decimal("1.0"))],
    )
    assert rb.currency == Currency.KRW


def test_rebalancer_rejects_mixed_currency_targets():
    with pytest.raises(ValueError, match="multiple currencies"):
        Rebalancer(
            broker=_StubBroker(),
            targets=[
                TargetWeight(symbol=Symbol.parse("NASD:AAPL"), weight=Decimal("0.5")),
                TargetWeight(symbol=Symbol(ticker="005930"), weight=Decimal("0.5")),
            ],
        )


def test_rebalancer_cash_sink_currency_must_match_targets():
    with pytest.raises(ValueError, match="multiple currencies"):
        Rebalancer(
            broker=_StubBroker(),
            targets=[TargetWeight(symbol=Symbol.parse("NASD:AAPL"), weight=Decimal("1.0"))],
            cash_sink=Symbol(ticker="005930"),  # KRW sink, USD targets
        )


def _usd_balance():
    """KRW + USD multi-currency balance: USD $2000 cash, AAPL 10 @ avg 150, TSLA 5 @ avg 380."""
    from tooja.core.enums import Currency
    from tooja.core.models import Balance, Position
    from tooja.core.money import Money
    aapl = Symbol.parse("NASD:AAPL")
    tsla = Symbol.parse("NASD:TSLA")
    return Balance(
        total_asset=Money(amount=Decimal("9999999"), currency=Currency.KRW),  # FX-rolled-up; must be ignored
        cash=[
            Money(amount=Decimal("500000"), currency=Currency.KRW),
            Money(amount=Decimal("2000"), currency=Currency.USD),
        ],
        positions=[
            Position(symbol=aapl, qty=Decimal("10"),
                     avg_price=Money(amount=Decimal("150"), currency=Currency.USD)),
            Position(symbol=tsla, qty=Decimal("5"),
                     avg_price=Money(amount=Decimal("380"), currency=Currency.USD)),
        ],
    )


def _usd_quotes(aapl_px="200", tsla_px="400"):
    from datetime import datetime, timezone
    from tooja.core.enums import Currency
    from tooja.core.models import Quote
    from tooja.core.money import Money
    aapl = Symbol.parse("NASD:AAPL")
    tsla = Symbol.parse("NASD:TSLA")
    def q(sym, px):
        return Quote(symbol=sym, price=Money(amount=Decimal(px), currency=Currency.USD),
                     time=datetime.now(timezone.utc))
    return {aapl: q(aapl, aapl_px), tsla: q(tsla, tsla_px)}


@pytest.mark.asyncio
async def test_sleeve_total_uses_cash_plus_positions_not_total_asset():
    from tooja.core.enums import Currency
    from tooja.core.money import Money
    aapl = Symbol.parse("NASD:AAPL")
    tsla = Symbol.parse("NASD:TSLA")
    broker = _ScriptedBroker(_usd_balance(), _usd_quotes())
    rb = Rebalancer(
        broker=broker,
        targets=[
            TargetWeight(symbol=aapl, weight=Decimal("0.5")),
            TargetWeight(symbol=tsla, weight=Decimal("0.5")),
        ],
    )
    plan = await rb.compute_plan()
    # sleeve_total = 2000 + 10*200 + 5*400 = 6000 USD (NOT the 9,999,999 KRW total_asset)
    assert plan.expected_total == Money(amount=Decimal("6000"), currency=Currency.USD)


@pytest.mark.asyncio
async def test_sleeve_ignores_other_currency_cash_and_positions():
    aapl = Symbol.parse("NASD:AAPL")
    tsla = Symbol.parse("NASD:TSLA")
    broker = _ScriptedBroker(_usd_balance(), _usd_quotes())
    rb = Rebalancer(
        broker=broker,
        targets=[
            TargetWeight(symbol=aapl, weight=Decimal("0.5")),
            TargetWeight(symbol=tsla, weight=Decimal("0.5")),
        ],
    )
    plan = await rb.compute_plan()
    assert plan.expected_cash.currency.value == "USD"
    assert plan.expected_total.amount == Decimal("6000")


@pytest.mark.asyncio
async def test_sleeve_total_uses_avg_price_for_unpriced_position():
    aapl = Symbol.parse("NASD:AAPL")
    tsla = Symbol.parse("NASD:TSLA")
    quotes = _usd_quotes()
    del quotes[tsla]  # _ScriptedMarket raises KeyError -> _lookup_price returns None
    broker = _ScriptedBroker(_usd_balance(), quotes)
    rb = Rebalancer(
        broker=broker,
        targets=[
            TargetWeight(symbol=aapl, weight=Decimal("0.5")),
            TargetWeight(symbol=tsla, weight=Decimal("0.5")),
        ],
    )
    plan = await rb.compute_plan()
    # TSLA valued at avg 380: total = 2000 + 10*200 + 5*380 = 5900
    assert plan.expected_total.amount == Decimal("5900")


@pytest.mark.asyncio
async def test_sleeve_total_zero_raises():
    from tooja.core.enums import Currency
    from tooja.core.models import Balance
    from tooja.core.money import Money
    aapl = Symbol.parse("NASD:AAPL")
    balance = Balance(
        total_asset=Money(amount=Decimal("500000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("500000"), currency=Currency.KRW)],
        positions=[],
    )
    broker = _ScriptedBroker(balance, _usd_quotes())
    rb = Rebalancer(broker=broker, targets=[TargetWeight(symbol=aapl, weight=Decimal("1.0"))])
    with pytest.raises(ValueError, match="no positive total"):
        await rb.compute_plan()


@pytest.mark.asyncio
async def test_recap_applies_buffer_from_expected_total_in_sleeve_currency():
    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance
    from tooja.portfolio.rebalance.models import PlannedTrade
    from tooja.core.money import Money
    aapl = Symbol.parse("NASD:AAPL")
    # Real cash after sells: USD $1000. expected_total = $5000 -> buffer 2% = $100.
    # Spendable = 1000 - 100 = 900. AAPL @ $200 -> floor(900/200)=4 shares.
    balance = Balance(
        total_asset=Money(amount=Decimal("9999999"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("1000"), currency=Currency.USD)],
        positions=[],
    )
    broker = _ScriptedBroker(balance, _usd_quotes())
    rb = Rebalancer(
        broker=broker,
        targets=[TargetWeight(symbol=aapl, weight=Decimal("1.0"))],
        min_order_value=Decimal("100"),  # USD account; default 10000 is KRW-oriented
    )
    plan = RebalancePlan(
        trades=[PlannedTrade(symbol=aapl, side=OrderSide.BUY, qty=Decimal("100"))],
        expected_drift=Decimal("0"),
        expected_cash=Money(amount=Decimal("0"), currency=Currency.USD),
        expected_total=Money(amount=Decimal("5000"), currency=Currency.USD),
        expected_holdings=[],
    )
    recapped = await rb._recap_buys(plan, plan.trades)
    assert len(recapped) == 1
    assert recapped[0].qty == Decimal("4")


@pytest.mark.asyncio
async def test_execute_overseas_buy_uses_marketable_limit():
    """Overseas trades become limit orders at quote × (1 + limit_offset),
    since KIS overseas regular-session trading is limit-only."""
    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance
    from tooja.core.money import Money
    from tooja.portfolio.rebalance.models import PlannedTrade

    sym = Symbol.parse("NASD:AAPL")
    balance = Balance(
        total_asset=Money(amount=Decimal("10000"), currency=Currency.USD),
        cash=[Money(amount=Decimal("10000"), currency=Currency.USD)],
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, _usd_quote_map(sym, "100.00")),
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        min_order_value=Decimal("100"),
    )
    plan = RebalancePlan(
        trades=[PlannedTrade(symbol=sym, side=OrderSide.BUY, qty=Decimal("5"))],
        expected_drift=Decimal("0"),
    )
    out = await rb.execute(plan)
    assert len(out) == 1
    [req] = rb.broker.orders.received
    assert req.type == "limit"
    assert req.price.amount == Decimal("101.00")  # 100 × 1.01, USD-quantized
    assert req.price.currency is Currency.USD
    assert req.qty == Decimal("5")


@pytest.mark.asyncio
async def test_execute_overseas_sell_limits_below_quote():
    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance
    from tooja.core.money import Money
    from tooja.portfolio.rebalance.models import PlannedTrade

    sym = Symbol.parse("NASD:AAPL")
    balance = Balance(
        total_asset=Money(amount=Decimal("0"), currency=Currency.USD),
        cash=[Money(amount=Decimal("0"), currency=Currency.USD)],
    )
    broker = _ScriptedBroker(balance, _usd_quote_map(sym, "100.00"))
    broker.orders = _FillTrackingOrders()
    rb = Rebalancer(
        broker=broker,
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        min_order_value=Decimal("100"),
    )
    plan = RebalancePlan(
        trades=[PlannedTrade(symbol=sym, side=OrderSide.SELL, qty=Decimal("5"))],
        expected_drift=Decimal("0"),
    )
    out = await rb.execute(plan)
    assert len(out) == 1
    [req] = broker.orders.received
    assert req.type == "limit"
    assert req.price.amount == Decimal("99.00")  # 100 × 0.99
    assert req.side is OrderSide.SELL


@pytest.mark.asyncio
async def test_execute_overseas_skips_trade_when_quote_unavailable():
    """No usable quote -> no limit price -> the trade is skipped, like a
    failed submit (next rebalance run will retry)."""
    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance
    from tooja.core.money import Money
    from tooja.portfolio.rebalance.models import PlannedTrade

    sym = Symbol.parse("NASD:AAPL")
    balance = Balance(
        total_asset=Money(amount=Decimal("10000"), currency=Currency.USD),
        cash=[Money(amount=Decimal("10000"), currency=Currency.USD)],
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),  # empty quote map
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
        min_order_value=Decimal("100"),
    )
    plan = RebalancePlan(
        trades=[PlannedTrade(symbol=sym, side=OrderSide.BUY, qty=Decimal("5"))],
        expected_drift=Decimal("0"),
        expected_holdings=[],
    )
    out = await rb.execute(plan)
    assert out == []
    assert rb.broker.orders.received == []


@pytest.mark.asyncio
async def test_execute_domestic_still_uses_market_order():
    from tooja.core.enums import Currency, OrderSide
    from tooja.core.models import Balance
    from tooja.core.money import Money
    from tooja.portfolio import ExpectedHolding
    from tooja.portfolio.rebalance.models import PlannedTrade

    sym = Symbol(ticker="005930")
    balance = Balance(
        total_asset=Money(amount=Decimal("1000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("1000000"), currency=Currency.KRW)],
    )
    rb = Rebalancer(
        broker=_ScriptedBroker(balance, {}),  # no quote needed for market orders
        targets=[TargetWeight(symbol=sym, weight=Decimal("1.0"))],
    )
    plan = RebalancePlan(
        trades=[PlannedTrade(symbol=sym, side=OrderSide.BUY, qty=Decimal("3"))],
        expected_drift=Decimal("0"),
        expected_holdings=[
            # recap fallback price so the buy survives without a quote
            ExpectedHolding(
                symbol=sym, qty=Decimal("3"), price=Decimal("70000"), value=Decimal("210000"),
            ),
        ],
    )
    out = await rb.execute(plan)
    assert len(out) == 1
    [req] = rb.broker.orders.received
    assert req.type == "market"


def test_rebalancer_rejects_bad_limit_offset():
    targets = [TargetWeight(symbol=Symbol.parse("NASD:AAPL"), weight=Decimal("1.0"))]
    with pytest.raises(ValueError, match="limit_offset"):
        Rebalancer(broker=_StubBroker(), targets=targets, limit_offset=Decimal("1.0"))
    with pytest.raises(ValueError, match="limit_offset"):
        Rebalancer(broker=_StubBroker(), targets=targets, limit_offset=Decimal("-0.01"))
    with pytest.raises(TypeError, match="limit_offset"):
        Rebalancer(broker=_StubBroker(), targets=targets, limit_offset=0.01)
