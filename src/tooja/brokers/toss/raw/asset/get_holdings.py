"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.toss.raw.base import TossApiExecutor
from tooja.brokers.toss.raw.models import HoldingsOverview


class GetHoldingsExecutor(TossApiExecutor[HoldingsOverview]):
    """보유 주식 조회"""

    PATH = "/api/v1/holdings"
    METHOD = "GET"
    RESPONSE_TYPE = HoldingsOverview
    QUERY_PARAMS = ("symbol",)
    HEADER_PARAMS = ("X-Tossinvest-Account",)
    BODY_CONTENT = "none"
