"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.toss.raw.base import TossApiExecutor
from tooja.brokers.toss.raw.models import KrMarketCalendarResponse


class GetKrMarketCalendarExecutor(TossApiExecutor[KrMarketCalendarResponse]):
    """국내 장 운영 정보 조회"""

    PATH = "/api/v1/market-calendar/KR"
    METHOD = "GET"
    RESPONSE_TYPE = KrMarketCalendarResponse
    QUERY_PARAMS = ("date",)
    BODY_CONTENT = "none"
