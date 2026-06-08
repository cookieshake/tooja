"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.toss.raw.base import TossApiExecutor
from tooja.brokers.toss.raw.models import OAuth2TokenResponse


class IssueOAuth2TokenExecutor(TossApiExecutor[OAuth2TokenResponse]):
    """OAuth2 액세스 토큰 발급"""

    PATH = "/oauth2/token"
    METHOD = "POST"
    RESPONSE_TYPE = OAuth2TokenResponse
    BODY_CONTENT = "form"
    ENVELOPED = False
