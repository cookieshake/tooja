"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireUnpdRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    FUOP_DVSN: str  # 선물옵션구분 — 00: 전체 / 01:선물 / 02: 옵션
    CTX_AREA_FK100: str  # 연속조회검색조건100
    CTX_AREA_NK100: str  # 연속조회키100

class InquireUnpdResponse_OutputItem(KisBaseModel):
    """nested item."""

    cano: str | None = None  # 종합계좌번호
    acnt_prdt_cd: str | None = None  # 계좌상품코드
    ovrs_futr_fx_pdno: str | None = None  # 해외선물FX상품번호
    prdt_type_cd: str | None = None  # 상품유형코드
    crcy_cd: str | None = None  # 통화코드
    sll_buy_dvsn_cd: str | None = None  # 매도매수구분코드
    fm_ustl_qty: str | None = None  # FM미결제수량
    fm_ccld_avg_pric: str | None = None  # FM체결평균가격
    fm_now_pric: str | None = None  # FM현재가격
    fm_evlu_pfls_amt: str | None = None  # FM평가손익금액
    fm_opt_evlu_amt: str | None = None  # FM옵션평가금액
    fm_otp_evlu_pfls_amt: str | None = None  # FM옵션평가손익금액
    fuop_dvsn: str | None = None  # 선물옵션구분
    ecis_rsvn_ord_yn: str | None = None  # 행사예약주문여부
    fm_lqd_psbl_qty: str | None = None  # FM청산가능수량

class InquireUnpdResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InquireUnpdResponse_OutputItem] = []  # 응답상세1 — Array

class InquireUnpdExecutor(ApiExecutor[InquireUnpdRequest, InquireUnpdResponse]):
    """해외선물옵션 미결제내역조회(잔고) [v1_해외선물-005]."""

    # 해외선물옵션 미결제내역조회(잔고) API입니다.

    PATH = "/uapi/overseas-futureoption/v1/trading/inquire-unpd"
    METHOD = "GET"
    RESPONSE_TYPE = InquireUnpdResponse
    TR_ID = "OTFM1412R"
