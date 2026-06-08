"""Toss Analytics subclient — unsupported.

Toss publishes no analytics endpoints (investor flows / program trading /
short selling / margin balance / securities lending). This client inherits the
``AnalyticsClient`` ABC defaults, which all raise ``UnsupportedOperation``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from tooja.core.clients import AnalyticsClient

if TYPE_CHECKING:
    from tooja.brokers.toss.broker import TossBroker


class TossAnalyticsClient(AnalyticsClient):
    _broker_name = "toss"

    def __init__(self, broker: "TossBroker"):
        self._broker = broker
