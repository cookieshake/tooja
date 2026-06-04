"""Broker ABC — entry point of the multi-broker abstraction."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar, Self

from tooja.core.clients import (
    AccountClient,
    AnalyticsClient,
    InfoClient,
    MarketClient,
    OrdersClient,
    RankingsClient,
    StreamClient,
)


_DOMAIN_TO_BASE: dict[str, type] = {
    "market": MarketClient,
    "account": AccountClient,
    "orders": OrdersClient,
    "info": InfoClient,
    "analytics": AnalyticsClient,
    "rankings": RankingsClient,
    "stream": StreamClient,
}


class Broker(ABC):
    """Common interface every broker adapter implements."""

    broker_name: ClassVar[str]

    market: MarketClient
    account: AccountClient
    orders: OrdersClient
    info: InfoClient
    analytics: AnalyticsClient
    rankings: RankingsClient
    stream: StreamClient

    @abstractmethod
    async def open(self) -> None:
        """Prepare session / auth / cache. Idempotent."""

    @abstractmethod
    async def close(self) -> None:
        """Cleanup session / streams. Idempotent."""

    async def __aenter__(self) -> Self:
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    def supports(self, method: str) -> bool:
        """`'<domain>.<method>'` -> True if the adapter overrides that method.

        Returns False when the adapter uses the default defined on the ABC client
        base (MarketClient, etc.); True when the adapter or one of its intermediate
        bases overrides it.

        `name` must be a domain method defined on the ABC base — dunder / internal
        attributes return False.
        """
        domain, _, name = method.partition(".")
        abc_base = _DOMAIN_TO_BASE.get(domain)
        if abc_base is None or not name or name not in abc_base.__dict__:
            return False
        sub = getattr(self, domain)
        for cls in type(sub).__mro__:
            if name in cls.__dict__:
                return cls is not abc_base
        return False
