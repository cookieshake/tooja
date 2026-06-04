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
async def test_compute_plan_not_implemented_yet():
    """Outline only — implementation lives in a separate plan."""
    rb = Rebalancer(
        broker=_StubBroker(),
        targets=[TargetWeight(symbol=Symbol(ticker="005930"), weight=Decimal("1.0"))],
    )
    with pytest.raises(NotImplementedError, match="separate plan"):
        await rb.compute_plan()
