"""KIS Stream subclient — WS subscriptions for quotes / orderbook / trades.

`orders()` (private my-order WS) is not wired in — requires HTS user id / hash
key, treated separately.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from tooja.brokers.kis._mappers import (
    _WS_ORDER_COLUMNS,
    _WS_QUOTE_COLUMNS,
    orderbook_from_ws_record,
    order_update_from_ws_record,
    quote_from_ws_record,
    trade_from_ws_record,
)
from tooja.brokers.kis._ws_stream import KisOrderUpdateStream, KisWsStream, _SubscriptionTopic
from tooja.core.clients import StreamClient
from tooja.core.models import Symbol
from tooja.core.stream import (
    OrderbookStream,
    OrderUpdateStream,
    QuoteStream,
    TradeStream,
)

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker


_QUOTE_TOPIC = _SubscriptionTopic(
    tr_id="H0STCNT0",
    columns=_WS_QUOTE_COLUMNS,
    mapper=quote_from_ws_record,
)


_TRADE_TOPIC = _SubscriptionTopic(
    tr_id="H0STCNT0",
    columns=_WS_QUOTE_COLUMNS,  # CCLD_DVSN is at index 21 in the full 46-field set.
    mapper=trade_from_ws_record,
)


# Source from raw subscriber to avoid the same prefix-only bug as H0STCNT0.
from tooja.brokers.kis.raw.domestic_stock_ws.h0stasp0 import (
    H0stasp0Subscriber as _H0stasp0Subscriber,
)
_ORDERBOOK_COLUMNS = _H0stasp0Subscriber.COLUMNS

_ORDERBOOK_TOPIC = _SubscriptionTopic(
    tr_id="H0STASP0",
    columns=_ORDERBOOK_COLUMNS,
    mapper=orderbook_from_ws_record,
)


class KisStreamClient(StreamClient):
    _broker_name = "kis"

    def __init__(self, broker: "KisBroker"):
        self._broker = broker

    def quotes(
        self,
        symbols: list[Symbol | str],
        *,
        include_control: bool = False,
        auto_reconnect: bool = True,
        buffer_size: int = 1024,
    ) -> QuoteStream:
        return KisWsStream(  # type: ignore[return-value]
            self._broker, _QUOTE_TOPIC, symbols,
            include_control=include_control,
            auto_reconnect=auto_reconnect,
            buffer_size=buffer_size,
        )

    def trades(
        self,
        symbols: list[Symbol | str],
        *,
        include_control: bool = False,
        auto_reconnect: bool = True,
        buffer_size: int = 1024,
    ) -> TradeStream:
        return KisWsStream(  # type: ignore[return-value]
            self._broker, _TRADE_TOPIC, symbols,
            include_control=include_control,
            auto_reconnect=auto_reconnect,
            buffer_size=buffer_size,
        )

    def orderbook(
        self,
        symbols: list[Symbol | str],
        *,
        include_control: bool = False,
        auto_reconnect: bool = True,
        buffer_size: int = 1024,
    ) -> OrderbookStream:
        return KisWsStream(  # type: ignore[return-value]
            self._broker, _ORDERBOOK_TOPIC, symbols,
            include_control=include_control,
            auto_reconnect=auto_reconnect,
            buffer_size=buffer_size,
        )

    def orders(
        self,
        *,
        include_control: bool = False,
        auto_reconnect: bool = True,
        buffer_size: int = 1024,
    ) -> OrderUpdateStream:
        return KisOrderUpdateStream(  # type: ignore[return-value]
            self._broker,
            tr_id="H0STCNI0",
            columns=_WS_ORDER_COLUMNS,
            mapper=order_update_from_ws_record,
            include_control=include_control,
            auto_reconnect=auto_reconnect,
            buffer_size=buffer_size,
        )
