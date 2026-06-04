"""KIS Market subclient — interface skeleton.

Out of scope for this plan: actual raw endpoint calls + model mapping live in a separate plan.
All methods use the ABC default and therefore raise UnsupportedOperation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from tooja.core.clients import MarketClient

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker


class KisMarketClient(MarketClient):
    _broker_name = "kis"

    def __init__(self, broker: "KisBroker"):
        self._broker = broker
