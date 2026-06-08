"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.toss.raw.base import TossApiExecutor
from tooja.brokers.toss.raw.models import Order


class GetOrderExecutor(TossApiExecutor[Order]):
    """주문 상세 조회"""

    PATH = "/api/v1/orders/{orderId}"
    METHOD = "GET"
    RESPONSE_TYPE = Order
    PATH_PARAMS = ("orderId",)
    HEADER_PARAMS = ("X-Tossinvest-Account",)
    BODY_CONTENT = "none"
