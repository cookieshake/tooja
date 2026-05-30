"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireDailyCcldRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    STRT_DT: str  # 시작일자 — 시작일자(YYYYMMDD)
    END_DT: str  # 종료일자 — 종료일자(YYYYMMDD)
    FUOP_DVSN_CD: str  # 선물옵션구분코드 — 00:전체 / 01:선물 / 02:옵션
    FM_PDGR_CD: str  # FM상품군코드 — 공란(Default)
    CRCY_CD: str  # 통화코드 — %%% : 전체 TUS: TOT_USD / TKR: TOT_KRW KRW: 한국 / USD: 미국 EUR: EUR / HKD: 홍콩 CNY: 중국 / JPY: 일본 VND: 베트남
    FM_ITEM_FTNG_YN: str  # FM종목합산여부 — "N"(Default)
    SLL_BUY_DVSN_CD: str  # 매도매수구분코드 — %%: 전체 / 01 : 매도 / 02 : 매수
    CTX_AREA_FK200: str  # 연속조회검색조건200
    CTX_AREA_NK200: str  # 연속조회키200

class InquireDailyCcldResponse_Output2Item(KisBaseModel):
    """nested item."""

    fm_tot_ccld_qty: str | None = None  # FM총체결수량
    fm_tot_futr_agrm_amt: str | None = None  # FM총선물약정금액
    fm_tot_opt_agrm_amt: str | None = None  # FM총옵션약정금액
    fm_fee_smtl: str | None = None  # FM수수료합계

class InquireDailyCcldResponse_Output1Item(KisBaseModel):
    """nested item."""

    dt: str | None = None  # 일자
    ccno: str | None = None  # 체결번호
    ovrs_futr_fx_pdno: str | None = None  # 해외선물FX상품번호
    sll_buy_dvsn_cd: str | None = None  # 매도매수구분코드
    fm_ccld_qty: str | None = None  # FM체결수량
    fm_ccld_amt: str | None = None  # FM체결금액
    fm_futr_ccld_amt: str | None = None  # FM선물체결금액
    fm_opt_ccld_amt: str | None = None  # FM옵션체결금액
    crcy_cd: str | None = None  # 통화코드
    fm_fee: str | None = None  # FM수수료
    fm_futr_pure_agrm_amt: str | None = None  # FM선물순약정금액
    fm_opt_pure_agrm_amt: str | None = None  # FM옵션순약정금액
    ccld_dtl_dtime: str | None = None  # 체결상세일시
    ord_dt: str | None = None  # 주문일자
    odno: str | None = None  # 주문번호 — 접수한 주문의 일련번호(ex. 00360686)
    ord_mdia_dvsn_name: str | None = None  # 주문매체구분명

class InquireDailyCcldResponse(KisCommonResponse):
    """응답 본문."""

    output2: InquireDailyCcldResponse_Output2Item | None = None  # 응답상세2
    output1: list[InquireDailyCcldResponse_Output1Item] = []  # 응답상세1 — Array

class InquireDailyCcldExecutor(ApiExecutor[InquireDailyCcldRequest, InquireDailyCcldResponse]):
    """해외선물옵션 일별 체결내역[해외선물-011]."""

    # 해외선물옵션 일별 체결내역 API입니다. 거래소 체결 내역에 따라 , output1에 동일한 주문번호의 데이터들이 수신될 수 있습니다.

    PATH = "/uapi/overseas-futureoption/v1/trading/inquire-daily-ccld"
    METHOD = "GET"
    RESPONSE_TYPE = InquireDailyCcldResponse
    TR_ID = "OTFM3122R"
