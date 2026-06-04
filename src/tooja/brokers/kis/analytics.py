"""KIS Analytics subclient — interface skeleton."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tooja.core.clients import AnalyticsClient

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker


class KisAnalyticsClient(AnalyticsClient):
    _broker_name = "kis"

    def __init__(self, broker: "KisBroker"):
        self._broker = broker
