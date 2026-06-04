"""KIS Info subclient — interface skeleton."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tooja.core.clients import InfoClient

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker


class KisInfoClient(InfoClient):
    _broker_name = "kis"

    def __init__(self, broker: "KisBroker"):
        self._broker = broker
