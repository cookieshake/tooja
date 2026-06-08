"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.toss.raw.base import TossApiExecutor
from tooja.brokers.toss.raw.models import OrderResponse


class CreateOrderExecutor(TossApiExecutor[OrderResponse]):
    """주문 생성"""

    PATH = "/api/v1/orders"
    METHOD = "POST"
    RESPONSE_TYPE = OrderResponse
    HEADER_PARAMS = ("X-Tossinvest-Account",)
    BODY_CONTENT = "json"
