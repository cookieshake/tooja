"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel,
)


class ApprovalRequest(KisBaseModel):
    """요청."""

    grant_type: str  # 권한부여타입 — "client_credentials"
    appkey: str  # 앱키 — 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.)
    secretkey: str  # 시크릿키 — 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) * 주의 : appsecret와 secretkey는 동일하오니 착오없으시기 바랍니다. (용어가 다른점 양해 부탁드립니다.)

class ApprovalResponse(KisBaseModel):
    """응답 본문."""

    approval_key: str | None = None  # 웹소켓 접속키 — 웹소켓 이용 시 발급받은 웹소켓 접속키를 appkey와 appsecret 대신 헤더에 넣어 API 호출합니다.

class ApprovalExecutor(ApiExecutor[ApprovalRequest, ApprovalResponse]):
    """실시간 (웹소켓) 접속키 발급[실시간-000]."""

    # 실시간 (웹소켓) 접속키 발급받으실 수 있는 API 입니다. 웹소켓 이용 시 해당 키를 appkey와 appsecret 대신 헤더에 넣어 API를 호출합니다. 접속키의 유효기간은 24시간이지만, 접속키는 세션 연결 시 초기 1회만 사용하기 때문에 접속키 인증 후에는 세션종료되지 않는 이상 접속키 신규 발급받지 않으셔도 365일 내내 웹소켓 데이터 수신하실 수 있습니다.

    PATH = "/oauth2/Approval"
    METHOD = "POST"
    RESPONSE_TYPE = ApprovalResponse
