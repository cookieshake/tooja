"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePsblOrderTttc0503rRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드 — 29
    PDNO: str  # 상품번호
    ACCA_DVSN_CD: str  # 적립금구분코드 — 00
    CMA_EVLU_AMT_ICLD_YN: str  # CMA평가금액포함여부
    ORD_DVSN: str  # 주문구분 — 00 : 지정가 / 01 : 시장가
    ORD_UNPR: str  # 주문단가

class InquirePsblOrderTttc0503rResponse_OutputItem(KisBaseModel):
    """nested item."""

    ord_psbl_cash: str | None = None  # 주문가능현금
    ruse_psbl_amt: str | None = None  # 재사용가능금액
    psbl_qty_calc_unpr: str | None = None  # 가능수량계산단가
    max_buy_amt: str | None = None  # 최대매수금액
    max_buy_qty: str | None = None  # 최대매수수량

class InquirePsblOrderTttc0503rResponse(KisCommonResponse):
    """응답 본문."""

    output: InquirePsblOrderTttc0503rResponse_OutputItem | None = None  # 응답상세1

class InquirePsblOrderTttc0503rExecutor(ApiExecutor[InquirePsblOrderTttc0503rRequest, InquirePsblOrderTttc0503rResponse]):
    """퇴직연금 매수가능조회[v1_국내주식-034]."""

    # ​※ 55번 계좌(DC가입자계좌)의 경우 해당 API 이용이 불가합니다. KIS Developers API의 경우 HTS ID에 반드시 연결되어있어야만 API 신청 및 앱정보 발급이 가능한 서비스로 개발되어서 실물계좌가 아닌 55번 계좌는 API 이용이 불가능한 점 양해 부탁드립니다.

    PATH = "/uapi/domestic-stock/v1/trading/pension/inquire-psbl-order"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePsblOrderTttc0503rResponse
    TR_ID = "TTTC0503R"
