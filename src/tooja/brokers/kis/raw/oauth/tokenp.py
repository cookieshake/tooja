"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse, SDecimal,
)


class TokenpRequest(KisBaseModel):
    """요청."""

    grant_type: str  # 권한부여 Type — client_credentials
    appkey: str  # 앱키 — 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.)
    appsecret: str  # 앱시크릿키 — 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.)

class TokenpResponse(KisBaseModel):
    """응답 본문."""

    access_token: str | None = None  # 접근토큰 — OAuth 토큰이 필요한 API 경우 발급한 Access token ex) "eyJ0eXUxMiJ9.eyJz…..................................." - 일반개인고객/일반법인고객 . Access token 유효기간
    token_type: str | None = None  # 접근토큰유형 — 접근토큰유형 : "Bearer" ※ API 호출 시, 접근토큰유형 "Bearer" 입력. ex) "Bearer eyJ...."
    expires_in: SDecimal = None  # 접근토큰 유효기간 — 유효기간(초) ex) 7776000
    access_token_token_expired: str | None = None  # 접근토큰 유효기간(일시표시) — 유효기간(년:월:일 시:분:초) ex) "2022-08-30 08:10:10"

class TokenpExecutor(ApiExecutor[TokenpRequest, TokenpResponse]):
    """접근토큰발급(P)[인증-001]."""

    # 본인 계좌에 필요한 인증 절차로, 인증을 통해 접근 토큰을 부여받아 오픈API 활용이 가능합니다. 1. 접근토큰(access_token)의 유효기간은 24시간 이며(1일 1회발급 원칙) 갱신발급주기는 6시간 입니다.(6시간 이내는 기존 발급키로 응답) 2. 접근토큰발급(/oauth2/tokenP) 시 접근토큰값(access_token)과 함께 수신되는 접근토큰 유효기간(acess_token_token_expired)을 이용해 

    PATH = "/oauth2/tokenP"
    METHOD = "POST"
    RESPONSE_TYPE = TokenpResponse
