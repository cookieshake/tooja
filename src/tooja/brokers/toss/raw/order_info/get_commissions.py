"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.toss.raw.base import TossApiExecutor, TossBaseModel
from tooja.brokers.toss.raw.models import Commission


class GetCommissionsResult(TossBaseModel):
    """Wrapper for the array ``result`` payload of getCommissions."""

    root: list[Commission] = []


class GetCommissionsExecutor(TossApiExecutor[GetCommissionsResult]):
    """매매 수수료 조회"""

    PATH = "/api/v1/commissions"
    METHOD = "GET"
    RESPONSE_TYPE = GetCommissionsResult
    HEADER_PARAMS = ("X-Tossinvest-Account",)
    BODY_CONTENT = "none"
