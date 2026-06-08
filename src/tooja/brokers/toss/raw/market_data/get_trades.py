"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.toss.raw.base import TossApiExecutor, TossBaseModel
from tooja.brokers.toss.raw.models import Trade


class GetTradesResult(TossBaseModel):
    """Wrapper for the array ``result`` payload of getTrades."""

    root: list[Trade] = []


class GetTradesExecutor(TossApiExecutor[GetTradesResult]):
    """최근 체결 내역 조회"""

    PATH = "/api/v1/trades"
    METHOD = "GET"
    RESPONSE_TYPE = GetTradesResult
    QUERY_PARAMS = ("symbol", "count")
    BODY_CONTENT = "none"
