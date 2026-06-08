"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.toss.raw.base import TossApiExecutor
from tooja.brokers.toss.raw.models import OrderbookResponse


class GetOrderbookExecutor(TossApiExecutor[OrderbookResponse]):
    """호가 조회"""

    PATH = "/api/v1/orderbook"
    METHOD = "GET"
    RESPONSE_TYPE = OrderbookResponse
    QUERY_PARAMS = ("symbol",)
    BODY_CONTENT = "none"
