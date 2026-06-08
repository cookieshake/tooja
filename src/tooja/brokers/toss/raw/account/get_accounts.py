"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.toss.raw.base import TossApiExecutor, TossBaseModel
from tooja.brokers.toss.raw.models import Account


class GetAccountsResult(TossBaseModel):
    """Wrapper for the array ``result`` payload of getAccounts."""

    root: list[Account] = []


class GetAccountsExecutor(TossApiExecutor[GetAccountsResult]):
    """계좌 목록 조회"""

    PATH = "/api/v1/accounts"
    METHOD = "GET"
    RESPONSE_TYPE = GetAccountsResult
    BODY_CONTENT = "none"
