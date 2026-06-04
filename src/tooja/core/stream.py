"""Stream ABCs — adapters subclass and implement."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import AsyncIterator, Generic, TypeVar

from tooja.core.models import (
    Orderbook,
    OrderUpdate,
    Quote,
    StreamControlEvent,
    Symbol,
    Trade,
)

T = TypeVar("T")


class _SymbolStream(ABC, Generic[T]):
    """Symbol-keyed stream base shared by quotes / trades / orderbook."""

    @property
    @abstractmethod
    def symbols(self) -> frozenset[Symbol]: ...

    @property
    @abstractmethod
    def auto_reconnect(self) -> bool: ...

    @abstractmethod
    async def subscribe(self, symbol: Symbol | str) -> None: ...

    @abstractmethod
    async def unsubscribe(self, symbol: Symbol | str) -> None: ...

    @abstractmethod
    async def __aenter__(self) -> "_SymbolStream[T]": ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb) -> None: ...

    @abstractmethod
    def __aiter__(self) -> AsyncIterator[T]: ...

    @abstractmethod
    async def __anext__(self) -> T: ...


class QuoteStream(_SymbolStream[Quote | StreamControlEvent]):
    """With `include_control=True` the stream yields Quote + StreamControlEvent; otherwise Quote only."""


class TradeStream(_SymbolStream[Trade | StreamControlEvent]):
    pass


class OrderbookStream(_SymbolStream[Orderbook | StreamControlEvent]):
    pass


class OrderUpdateStream(ABC):
    """My-order notifications — no symbol subscription concept (account-scoped)."""

    @property
    @abstractmethod
    def auto_reconnect(self) -> bool: ...

    @abstractmethod
    async def __aenter__(self) -> "OrderUpdateStream": ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb) -> None: ...

    @abstractmethod
    def __aiter__(self) -> AsyncIterator[OrderUpdate | StreamControlEvent]: ...

    @abstractmethod
    async def __anext__(self) -> OrderUpdate | StreamControlEvent: ...
