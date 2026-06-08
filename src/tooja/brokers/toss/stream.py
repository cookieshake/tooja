"""Toss Stream subclient — unsupported.

Toss publishes no streaming/websocket endpoint in this adapter. This client
inherits the ``StreamClient`` ABC defaults, which raise ``UnsupportedOperation``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from tooja.core.clients import StreamClient

if TYPE_CHECKING:
    from tooja.brokers.toss.broker import TossBroker


class TossStreamClient(StreamClient):
    _broker_name = "toss"

    def __init__(self, broker: "TossBroker"):
        self._broker = broker
