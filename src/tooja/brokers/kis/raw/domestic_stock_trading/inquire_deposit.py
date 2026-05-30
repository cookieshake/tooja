"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireDepositRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드 — 29
    ACCA_DVSN_CD: str  # 적립금구분코드 — 00

class InquireDepositResponse_OutputItem(KisBaseModel):
    """nested item."""

    dnca_tota: str | None = None  # 예수금총액
    nxdy_excc_amt: str | None = None  # 익일정산액
    nxdy_sttl_amt: str | None = None  # 익일결제금액
    nx2_day_sttl_amt: str | None = None  # 2익일결제금액

class InquireDepositResponse(KisCommonResponse):
    """응답 본문."""

    output: InquireDepositResponse_OutputItem | None = None  # 응답상세1

class InquireDepositExecutor(ApiExecutor[InquireDepositRequest, InquireDepositResponse]):
    """퇴직연금 예수금조회[v1_국내주식-035]."""

    # ​※ 55번 계좌(DC가입자계좌)의 경우 해당 API 이용이 불가합니다. KIS Developers API의 경우 HTS ID에 반드시 연결되어있어야만 API 신청 및 앱정보 발급이 가능한 서비스로 개발되어서 실물계좌가 아닌 55번 계좌는 API 이용이 불가능한 점 양해 부탁드립니다.

    PATH = "/uapi/domestic-stock/v1/trading/pension/inquire-deposit"
    METHOD = "GET"
    RESPONSE_TYPE = InquireDepositResponse
    TR_ID = "TTTC0506R"
