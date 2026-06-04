"""KIS Stream subclient — interface skeleton."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tooja.core.clients import StreamClient

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker


class KisStreamClient(StreamClient):
    _broker_name = "kis"

    def __init__(self, broker: "KisBroker"):
        self._broker = broker
