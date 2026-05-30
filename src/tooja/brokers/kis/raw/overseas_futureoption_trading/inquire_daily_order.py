"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireDailyOrderRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    STRT_DT: str  # 시작일자
    END_DT: str  # 종료일자
    FM_PDGR_CD: str  # FM상품군코드
    CCLD_NCCS_DVSN: str  # 체결미체결구분 — 01:전체 / 02:체결 / 03:미체결
    SLL_BUY_DVSN_CD: str  # 매도매수구분코드 — %%전체 / 01 : 매도 / 02 : 매수
    FUOP_DVSN: str  # 선물옵션구분 — 00:전체 / 01:선물 / 02:옵션
    CTX_AREA_FK200: str  # 연속조회검색조건200
    CTX_AREA_NK200: str  # 연속조회키200

class InquireDailyOrderResponse_OutputItem(KisBaseModel):
    """nested item."""

    cano: str | None = None  # 종합계좌번호
    acnt_prdt_cd: str | None = None  # 계좌상품코드
    dt: str | None = None  # 일자
    ord_dt: str | None = None  # 주문일자
    odno: str | None = None  # 주문번호 — 접수한 주문의 일련번호(ex. 00360686) * 정정/취소시 문자열처럼 "0"을 포함해서 전송 (ex. ORGN_ODNO : 00360686) * 정정/취소시 문자열처럼 "0"을 포함해서 전송 (ex. ORGN_ODNO : 003606
    orgn_ord_dt: str | None = None  # 원주문일자
    orgn_odno: str | None = None  # 원주문번호 — 원주문번호(ex. 00360685)
    ovrs_futr_fx_pdno: str | None = None  # 해외선물FX상품번호
    rvse_cncl_dvsn_cd: str | None = None  # 정정취소구분코드 — 청산체결이 없는 신규 00 청산체결이 없는 정정 01 청산체결이 없는 취소 02 청산체결이 있는 취소 02 청산체결이 있는 신규 03 청산체결이 있는 정정 04 행사 05 배정 06 소멸 07 만기 08
    sll_buy_dvsn_cd: str | None = None  # 매도매수구분코드
    cplx_ord_dvsn_cd: str | None = None  # 복합주문구분코드
    pric_dvsn_cd: str | None = None  # 가격구분코드
    rcit_dvsn_cd: str | None = None  # 접수구분코드
    fm_ord_qty: str | None = None  # FM주문수량
    fm_ord_pric: str | None = None  # FM주문가격
    fm_stop_ord_pric: str | None = None  # FMSTOP주문가격
    ecis_rsvn_ord_yn: str | None = None  # 행사예약주문여부
    fm_ccld_qty: str | None = None  # FM체결수량
    fm_ccld_pric: str | None = None  # FM체결가격
    fm_ord_rmn_qty: str | None = None  # FM주문잔여수량
    ord_grp_name: str | None = None  # 주문그룹명
    rcit_dtl_dtime: str | None = None  # 접수상세일시
    ccld_dtl_dtime: str | None = None  # 체결상세일시
    ordr_emp_no: str | None = None  # 주문자사원번호
    rjct_rson_name: str | None = None  # 거부사유명
    ccld_cndt_cd: str | None = None  # 체결조건코드
    trad_end_dt: str | None = None  # 매매종료일자

class InquireDailyOrderResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InquireDailyOrderResponse_OutputItem] = []  # 응답상세1 — Array

class InquireDailyOrderExecutor(ApiExecutor[InquireDailyOrderRequest, InquireDailyOrderResponse]):
    """해외선물옵션 일별 주문내역[해외선물-013]."""

    # 해외선물옵션 일별 주문내역 API입니다.

    PATH = "/uapi/overseas-futureoption/v1/trading/inquire-daily-order"
    METHOD = "GET"
    RESPONSE_TYPE = InquireDailyOrderResponse
    TR_ID = "OTFM3120R"
