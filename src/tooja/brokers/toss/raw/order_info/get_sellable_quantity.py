"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.toss.raw.base import TossApiExecutor
from tooja.brokers.toss.raw.models import SellableQuantityResponse


class GetSellableQuantityExecutor(TossApiExecutor[SellableQuantityResponse]):
    """판매 가능 수량 조회"""

    PATH = "/api/v1/sellable-quantity"
    METHOD = "GET"
    RESPONSE_TYPE = SellableQuantityResponse
    QUERY_PARAMS = ("symbol",)
    HEADER_PARAMS = ("X-Tossinvest-Account",)
    BODY_CONTENT = "none"
