"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.toss.raw.base import TossApiExecutor
from tooja.brokers.toss.raw.models import BuyingPowerResponse


class GetBuyingPowerExecutor(TossApiExecutor[BuyingPowerResponse]):
    """매수 가능 금액 조회"""

    PATH = "/api/v1/buying-power"
    METHOD = "GET"
    RESPONSE_TYPE = BuyingPowerResponse
    QUERY_PARAMS = ("currency",)
    HEADER_PARAMS = ("X-Tossinvest-Account",)
    BODY_CONTENT = "none"
