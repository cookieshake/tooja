"""Toss Rankings subclient — unsupported.

Toss publishes no rankings endpoint. This client inherits the ``RankingsClient``
ABC defaults, which raise ``UnsupportedOperation``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from tooja.core.clients import RankingsClient

if TYPE_CHECKING:
    from tooja.brokers.toss.broker import TossBroker


class TossRankingsClient(RankingsClient):
    _broker_name = "toss"

    def __init__(self, broker: "TossBroker"):
        self._broker = broker
