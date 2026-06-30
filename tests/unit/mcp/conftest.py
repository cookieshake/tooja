"""Fixtures for MCP unit tests."""

from __future__ import annotations

from typing import ClassVar

from tooja.core.broker import Broker
from tooja.core.clients import (
    AccountClient,
    AnalyticsClient,
    InfoClient,
    MarketClient,
    OrdersClient,
    RankingsClient,
    StreamClient,
)


class FakeBroker(Broker):
    broker_name: ClassVar[str] = "fake"

    def __init__(self, name: str = "fake") -> None:
        self.broker_name = name  # type: ignore[misc]
        self.opened = False
        self.closed = False
        self.market = MarketClient()
        self.account = AccountClient()
        self.orders = OrdersClient()
        self.info = InfoClient()
        self.analytics = AnalyticsClient()
        self.rankings = RankingsClient()
        self.stream = StreamClient()

    async def open(self) -> None:
        self.opened = True

    async def close(self) -> None:
        self.closed = True
