"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class MarginDetailRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드
    CRCY_CD: str  # 통화코드 — 'TKR(TOT_KRW), TUS(TOT_USD), USD(미국달러), HKD(홍콩달러), CNY(중국위안화), JPY )일본엔화), VND(베트남동)'
    INQR_DT: str  # 조회일자

class MarginDetailResponse_OutputItem(KisBaseModel):
    """nested item."""

    cano: str | None = None  # 종합계좌번호
    acnt_prdt_cd: str | None = None  # 계좌상품코드
    crcy_cd: str | None = None  # 통화코드
    resp_dt: str | None = None  # 응답일자
    acnt_net_risk_mgna_aply_yn: str | None = None  # 계좌순위험증거금적용여부
    fm_ord_psbl_amt: str | None = None  # FM주문가능금액
    fm_add_mgn_amt: str | None = None  # FM추가증거금액
    fm_brkg_mgn_amt: str | None = None  # FM위탁증거금액
    fm_excc_brkg_mgn_amt: str | None = None  # FM정산위탁증거금액
    fm_ustl_mgn_amt: str | None = None  # FM미결제증거금액
    fm_mntn_mgn_amt: str | None = None  # FM유지증거금액
    fm_ord_mgn_amt: str | None = None  # FM주문증거금액
    fm_futr_ord_mgn_amt: str | None = None  # FM선물주문증거금액
    fm_opt_buy_ord_amt: str | None = None  # FM옵션매수주문금액
    fm_opt_sll_ord_mgn_amt: str | None = None  # FM옵션매도주문증거금액
    fm_opt_buy_ord_mgn_amt: str | None = None  # FM옵션매수주문증거금액
    fm_ecis_rsvn_mgn_amt: str | None = None  # FM행사예약증거금액
    fm_span_brkg_mgn_amt: str | None = None  # FMSPAN위탁증거금액
    fm_span_pric_altr_mgn_amt: str | None = None  # FMSPAN가격변동증거금액
    fm_span_term_sprd_mgn_amt: str | None = None  # FMSPAN기간스프레드증거금액
    fm_span_buy_opt_min_mgn_amt: str | None = None  # FMSPAN옵션가격증거금액
    fm_span_opt_min_mgn_amt: str | None = None  # FMSPAN옵션최소증거금액
    fm_span_tot_risk_mgn_amt: str | None = None  # FMSPAN총위험증거금액
    fm_span_mntn_mgn_amt: str | None = None  # FMSPAN유지증거금액
    fm_span_mntn_pric_altr_mgn_amt: str | None = None  # FMSPAN유지가격변동증거금액
    fm_span_mntn_term_sprd_mgn_amt: str | None = None  # FMSPAN유지기간스프레드증거금액
    fm_span_mntn_opt_pric_mgn_amt: str | None = None  # FMSPAN유지옵션가격증거금액
    fm_span_mntn_opt_min_mgn_amt: str | None = None  # FMSPAN유지옵션최소증거금액
    fm_span_mntn_tot_risk_mgn_amt: str | None = None  # FMSPAN유지총위험증거금액
    fm_eurx_brkg_mgn_amt: str | None = None  # FMEUREX위탁증거금액
    fm_eurx_pric_altr_mgn_amt: str | None = None  # FMEUREX가격변동증거금액
    fm_eurx_term_sprd_mgn_amt: str | None = None  # FMEUREX기간스프레드증거금액
    fm_eurx_opt_pric_mgn_amt: str | None = None  # FMEUREX옵션가격증거금액
    fm_eurx_buy_opt_min_mgn_amt: str | None = None  # FMEUREX매수옵션최소증거금액
    fm_eurx_tot_risk_mgn_amt: str | None = None  # FMEUREX총위험증거금액
    fm_eurx_mntn_mgn_amt: str | None = None  # FMEUREX유지증거금액
    fm_eurx_mntn_pric_altr_mgn_amt: str | None = None  # FMEUREX유지가격변동증거금액
    fm_eurx_mntn_term_sprd_mgn_amt: str | None = None  # FMEUREX기간스프레드증거금액
    fm_eurx_mntn_opt_pric_mgn_amt: str | None = None  # FMEUREX유지옵션가격증거금액
    fm_eurx_mntn_tot_risk_mgn_amt: str | None = None  # FMEUREX유지총위험증거금액
    fm_gnrl_brkg_mgn_amt: str | None = None  # FM일반위탁증거금액
    fm_futr_ustl_mgn_amt: str | None = None  # FM선물미결제증거금액
    fm_sll_opt_ustl_mgn_amt: str | None = None  # FM매도옵션미결제증거금액
    fm_buy_opt_ustl_mgn_amt: str | None = None  # FM매수옵션미결제증거금액
    fm_sprd_ustl_mgn_amt: str | None = None  # FM스프레드미결제증거금액
    fm_avg_dsct_mgn_amt: str | None = None  # FMAVG할인증거금액
    fm_gnrl_mntn_mgn_amt: str | None = None  # FM일반유지증거금액
    fm_futr_mntn_mgn_amt: str | None = None  # FM선물유지증거금액
    fm_opt_mntn_mgn_amt: str | None = None  # FM옵션유지증거금액

class MarginDetailResponse(KisCommonResponse):
    """응답 본문."""

    output: MarginDetailResponse_OutputItem | None = None  # 응답상세

class MarginDetailExecutor(ApiExecutor[MarginDetailRequest, MarginDetailResponse]):
    """해외선물옵션 증거금상세 [해외선물-032]."""

    # 해외선물옵션 증거금상세 API입니다. 한국투자 HTS(eFriend Plus) &gt; [2711] 해외선물옵션 증거금상세 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. [증거금 상세설명] - SPAN, EUREX 증거금 1. 가격변동증거금 : 보유하고 있는 미결제를 Product Class 별로 구간[SPAN-16구간, EUREX-29구간)손익 합계액 산출하며 최대손실구간의 금액

    PATH = "/uapi/overseas-futureoption/v1/trading/margin-detail"
    METHOD = "GET"
    RESPONSE_TYPE = MarginDetailResponse
    TR_ID = "OTFM3115R"
