"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.toss.raw.base import TossApiExecutor
from tooja.brokers.toss.raw.models import PriceLimitResponse


class GetPriceLimitExecutor(TossApiExecutor[PriceLimitResponse]):
    """상/하한가 조회"""

    PATH = "/api/v1/price-limits"
    METHOD = "GET"
    RESPONSE_TYPE = PriceLimitResponse
    QUERY_PARAMS = ("symbol",)
    BODY_CONTENT = "none"
