"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel,
)


class RevokepRequest(KisBaseModel):
    """요청."""

    appkey: str  # 고객 앱Key — 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.)
    appsecret: str  # 고객 앱Secret — 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.)
    token: str  # 접근토큰 — OAuth 토큰이 필요한 API 경우 발급한 Access token 일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용) 법인(Access token 유효기간 3개월

class RevokepResponse(KisBaseModel):
    """응답 본문."""

    code: str | None = None  # 응답코드 — HTTP 응답코드
    message: str | None = None  # 응답메세지

class RevokepExecutor(ApiExecutor[RevokepRequest, RevokepResponse]):
    """접근토큰폐기(P)[인증-002]."""

    # 부여받은 접큰토큰을 더 이상 활용하지 않을 때 사용합니다.

    PATH = "/oauth2/revokeP"
    METHOD = "POST"
    RESPONSE_TYPE = RevokepResponse
