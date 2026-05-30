"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePsamountRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    OVRS_FUTR_FX_PDNO: str  # 해외선물FX상품번호
    SLL_BUY_DVSN_CD: str  # 매도매수구분코드 — 01 : 매도 / 02 : 매수
    FM_ORD_PRIC: str  # FM주문가격
    ECIS_RSVN_ORD_YN: str  # 행사예약주문여부 — N

class InquirePsamountResponse_OutputItem(KisBaseModel):
    """nested item."""

    cano: str | None = None  # 종합계좌번호
    acnt_prdt_cd: str | None = None  # 계좌상품코드
    ovrs_futr_fx_pdno: str | None = None  # 해외선물FX상품번호
    crcy_cd: str | None = None  # 통화코드
    sll_buy_dvsn_cd: str | None = None  # 매도매수구분코드
    fm_ustl_qty: str | None = None  # FM미결제수량
    fm_lqd_psbl_qty: str | None = None  # FM청산가능수량
    fm_new_ord_psbl_qty: str | None = None  # FM신규주문가능수량
    fm_tot_ord_psbl_qty: str | None = None  # FM총주문가능수량
    fm_mkpr_tot_ord_psbl_qty: str | None = None  # FM시장가총주문가능수량

class InquirePsamountResponse(KisCommonResponse):
    """응답 본문."""

    output: InquirePsamountResponse_OutputItem | None = None  # 응답상세1

class InquirePsamountExecutor(ApiExecutor[InquirePsamountRequest, InquirePsamountResponse]):
    """해외선물옵션 주문가능조회 [v1_해외선물-006]."""

    # 해외선물옵션 주문가능조회 API입니다.

    PATH = "/uapi/overseas-futureoption/v1/trading/inquire-psamount"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePsamountResponse
    TR_ID = "OTFM3304R"
