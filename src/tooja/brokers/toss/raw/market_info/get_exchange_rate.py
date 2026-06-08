"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.toss.raw.base import TossApiExecutor
from tooja.brokers.toss.raw.models import ExchangeRateResponse


class GetExchangeRateExecutor(TossApiExecutor[ExchangeRateResponse]):
    """환율 조회"""

    PATH = "/api/v1/exchange-rate"
    METHOD = "GET"
    RESPONSE_TYPE = ExchangeRateResponse
    QUERY_PARAMS = ("dateTime", "baseCurrency", "quoteCurrency")
    BODY_CONTENT = "none"
