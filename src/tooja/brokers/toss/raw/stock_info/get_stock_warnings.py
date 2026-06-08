"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.toss.raw.base import TossApiExecutor, TossBaseModel
from tooja.brokers.toss.raw.models import StockWarning


class GetStockWarningsResult(TossBaseModel):
    """Wrapper for the array ``result`` payload of getStockWarnings."""

    root: list[StockWarning] = []


class GetStockWarningsExecutor(TossApiExecutor[GetStockWarningsResult]):
    """매수 유의사항 조회"""

    PATH = "/api/v1/stocks/{symbol}/warnings"
    METHOD = "GET"
    RESPONSE_TYPE = GetStockWarningsResult
    PATH_PARAMS = ("symbol",)
    BODY_CONTENT = "none"
