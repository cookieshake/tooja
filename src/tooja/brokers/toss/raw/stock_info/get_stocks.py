"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.toss.raw.base import TossApiExecutor, TossBaseModel
from tooja.brokers.toss.raw.models import StockInfo


class GetStocksResult(TossBaseModel):
    """Wrapper for the array ``result`` payload of getStocks."""

    root: list[StockInfo] = []


class GetStocksExecutor(TossApiExecutor[GetStocksResult]):
    """종목 기본 정보 조회"""

    PATH = "/api/v1/stocks"
    METHOD = "GET"
    RESPONSE_TYPE = GetStocksResult
    QUERY_PARAMS = ("symbols",)
    BODY_CONTENT = "none"
