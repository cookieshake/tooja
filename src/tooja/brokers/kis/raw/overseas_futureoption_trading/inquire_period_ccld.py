"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePeriodCcldRequest(KisBaseModel):
    """요청."""

    INQR_TERM_FROM_DT: str  # 조회기간FROM일자
    INQR_TERM_TO_DT: str  # 조회기간TO일자
    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    CRCY_CD: str  # 통화코드 — '%%% : 전체 TUS: TOT_USD / TKR: TOT_KRW KRW: 한국 / USD: 미국 EUR: EUR / HKD: 홍콩 CNY: 중국 / JPY: 일본'
    WHOL_TRSL_YN: str  # 전체환산여부 — N
    FUOP_DVSN: str  # 선물옵션구분 — 00:전체 / 01:선물 / 02:옵션
    CTX_AREA_FK200: str  # 연속조회검색조건200
    CTX_AREA_NK200: str  # 연속조회키200

class InquirePeriodCcldResponse_Output1Item(KisBaseModel):
    """nested item."""

    cano: str | None = None  # 종합계좌번호
    acnt_prdt_cd: str | None = None  # 계좌상품코드
    crcy_cd: str | None = None  # 통화코드
    fm_buy_qty: str | None = None  # FM매수수량
    fm_sll_qty: str | None = None  # FM매도수량
    fm_lqd_pfls_amt: str | None = None  # FM청산손익금액
    fm_fee: str | None = None  # FM수수료
    fm_net_pfls_amt: str | None = None  # FM순손익금액
    fm_ustl_buy_qty: str | None = None  # FM미결제매수수량
    fm_ustl_sll_qty: str | None = None  # FM미결제매도수량
    fm_ustl_evlu_pfls_amt: str | None = None  # FM미결제평가손익금액
    fm_ustl_evlu_pfls_amt2: str | None = None  # FM미결제평가손익금액2
    fm_ustl_evlu_pfls_icdc_amt: str | None = None  # FM미결제평가손익증감금액
    fm_ustl_agrm_amt: str | None = None  # FM미결제약정금액
    fm_opt_lqd_amt: str | None = None  # FM옵션청산금액

class InquirePeriodCcldResponse_Output2Item(KisBaseModel):
    """nested item."""

    cano: str | None = None  # 종합계좌번호
    acnt_prdt_cd: str | None = None  # 계좌상품코드
    ovrs_futr_fx_pdno: str | None = None  # 해외선물FX상품번호
    crcy_cd: str | None = None  # 통화코드
    fm_buy_qty: str | None = None  # FM매수수량
    fm_sll_qty: str | None = None  # FM매도수량
    fm_lqd_pfls_amt: str | None = None  # FM청산손익금액
    fm_fee: str | None = None  # FM수수료
    fm_net_pfls_amt: str | None = None  # FM순손익금액
    fm_ustl_buy_qty: str | None = None  # FM미결제매수수량
    fm_ustl_sll_qty: str | None = None  # FM미결제매도수량
    fm_ustl_evlu_pfls_amt: str | None = None  # FM미결제평가손익금액
    fm_ustl_evlu_pfls_amt2: str | None = None  # FM미결제평가손익금액2
    fm_ustl_evlu_pfls_icdc_amt: str | None = None  # FM미결제평가손익증감금액
    fm_ccld_avg_pric: str | None = None  # FM체결평균가격
    fm_ustl_agrm_amt: str | None = None  # FM미결제약정금액
    fm_opt_lqd_amt: str | None = None  # FM옵션청산금액

class InquirePeriodCcldResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[InquirePeriodCcldResponse_Output1Item] = []  # 응답상세1 — Array
    output2: list[InquirePeriodCcldResponse_Output2Item] = []  # 응답상세2 — Array

class InquirePeriodCcldExecutor(ApiExecutor[InquirePeriodCcldRequest, InquirePeriodCcldResponse]):
    """해외선물옵션 기간계좌손익 일별[해외선물-010]."""

    # 해외선물옵션 기간계좌손익 일별 API입니다.

    PATH = "/uapi/overseas-futureoption/v1/trading/inquire-period-ccld"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePeriodCcldResponse
    TR_ID = "OTFM3118R"
