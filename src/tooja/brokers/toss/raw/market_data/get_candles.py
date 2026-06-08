"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.toss.raw.base import TossApiExecutor
from tooja.brokers.toss.raw.models import CandlePageResponse


class GetCandlesExecutor(TossApiExecutor[CandlePageResponse]):
    """캔들 차트 조회"""

    PATH = "/api/v1/candles"
    METHOD = "GET"
    RESPONSE_TYPE = CandlePageResponse
    QUERY_PARAMS = ("symbol", "interval", "count", "before", "adjusted")
    BODY_CONTENT = "none"
