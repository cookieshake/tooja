"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.toss.raw.base import TossApiExecutor, TossBaseModel
from tooja.brokers.toss.raw.models import PriceResponse


class GetPricesResult(TossBaseModel):
    """Wrapper for the array ``result`` payload of getPrices."""

    root: list[PriceResponse] = []


class GetPricesExecutor(TossApiExecutor[GetPricesResult]):
    """현재가 조회"""

    PATH = "/api/v1/prices"
    METHOD = "GET"
    RESPONSE_TYPE = GetPricesResult
    QUERY_PARAMS = ("symbols",)
    BODY_CONTENT = "none"
