"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.toss.raw.base import TossApiExecutor
from tooja.brokers.toss.raw.models import OrderOperationResponse


class CancelOrderExecutor(TossApiExecutor[OrderOperationResponse]):
    """주문 취소"""

    PATH = "/api/v1/orders/{orderId}/cancel"
    METHOD = "POST"
    RESPONSE_TYPE = OrderOperationResponse
    PATH_PARAMS = ("orderId",)
    HEADER_PARAMS = ("X-Tossinvest-Account",)
    BODY_CONTENT = "json"
