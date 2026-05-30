"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireCcldRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    CCLD_NCCS_DVSN: str  # 체결미체결구분 — 01:전체 / 02:체결 / 03:미체결
    SLL_BUY_DVSN_CD: str  # 매도매수구분코드 — %%:전체 / 01:매도 / 02:매수
    FUOP_DVSN: str  # 선물옵션구분 — 00:전체 / 01:선물 / 02:옵션
    CTX_AREA_FK200: str  # 연속조회검색조건200
    CTX_AREA_NK200: str  # 연속조회키200

class InquireCcldResponse_OutputItem(KisBaseModel):
    """nested item."""

    cano: str | None = None  # 종합계좌번호
    acnt_prdt_cd: str | None = None  # 계좌상품코드
    ord_dt: str | None = None  # 주문일자
    odno: str | None = None  # 주문번호 — 접수한 주문의 일련번호(ex. 00360686) * 정정/취소시 문자열처럼 "0"을 포함해서 전송 (ex. ORGN_ODNO : 00360686)
    orgn_ord_dt: str | None = None  # 원주문일자
    orgn_odno: str | None = None  # 원주문번호 — 원주문번호(ex. 00360685)
    ovrs_futr_fx_pdno: str | None = None  # 해외선물FX상품번호
    rcit_dvsn_cd: str | None = None  # 접수구분코드 — 05 온라인
    sll_buy_dvsn_cd: str | None = None  # 매도매수구분코드 — 01:매도, 02:매수
    trad_stgy_dvsn_cd: str | None = None  # 매매전략구분코드
    bass_pric_type_cd: str | None = None  # 기준가격유형코드 — 01 시가평가 02 액면가 03 기준가격 04 대용가
    ord_stat_cd: str | None = None  # 주문상태코드
    fm_ord_qty: str | None = None  # FM주문수량
    fm_ord_pric: str | None = None  # FM주문가격
    fm_stop_ord_pric: str | None = None  # FMSTOP주문가격
    rsvn_dvsn: str | None = None  # 예약구분
    fm_ccld_qty: str | None = None  # FM체결수량
    fm_ccld_pric: str | None = None  # FM체결가격
    fm_ord_rmn_qty: str | None = None  # FM주문잔여수량
    ord_grp_name: str | None = None  # 주문그룹명
    erlm_dtl_dtime: str | None = None  # 등록상세일시
    ccld_dtl_dtime: str | None = None  # 체결상세일시
    ord_stfno: str | None = None  # 주문직원번호
    rmks1: str | None = None  # 비고1
    new_lqd_dvsn_cd: str | None = None  # 신규청산구분코드 — 01 신규 02 청산
    fm_lqd_lmt_ord_pric: str | None = None  # FM청산LIMIT주문가격
    fm_lqd_stop_pric: str | None = None  # FM청산STOP가격
    ccld_cndt_cd: str | None = None  # 체결조건코드
    noti_vald_dt: str | None = None  # 게시유효일자
    acnt_type_cd: str | None = None  # 계좌유형코드
    fuop_dvsn: str | None = None  # 선물옵션구분 — 01:선물, 02: 옵션

class InquireCcldResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InquireCcldResponse_OutputItem] = []  # 응답상세1 — Array

class InquireCcldExecutor(ApiExecutor[InquireCcldRequest, InquireCcldResponse]):
    """해외선물옵션 당일주문내역조회 [v1_해외선물-004]."""

    # 해외선물옵션 당일주문내역조회 API입니다.

    PATH = "/uapi/overseas-futureoption/v1/trading/inquire-ccld"
    METHOD = "GET"
    RESPONSE_TYPE = InquireCcldResponse
    TR_ID = "OTFM3116R"
