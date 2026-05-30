"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireBalanceValuationPlRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    MGNA_DVSN: str  # 증거금구분 — 01 : 개시, 02 : 유지
    EXCC_STAT_CD: str  # 정산상태코드 — 1 : 정산 (정산가격으로 잔고 조회) 2 : 본정산 (매입가격으로 잔고 조회)
    CTX_AREA_FK200: str  # 연속조회검색조건200
    CTX_AREA_NK200: str  # 연속조회키200

class InquireBalanceValuationPlResponse_Output2Item(KisBaseModel):
    """nested item."""

    dnca_cash: str | None = None  # 예수금현금
    frcr_dncl_amt: str | None = None  # 외화예수금액
    dnca_sbst: str | None = None  # 예수금대용
    tot_dncl_amt: str | None = None  # 총예수금액
    tot_ccld_amt: str | None = None  # 총체결금액
    cash_mgna: str | None = None  # 현금증거금
    sbst_mgna: str | None = None  # 대용증거금
    mgna_tota: str | None = None  # 증거금총액
    opt_dfpa: str | None = None  # 옵션차금
    thdt_dfpa: str | None = None  # 당일차금
    rnwl_dfpa: str | None = None  # 갱신차금
    fee: str | None = None  # 수수료
    nxdy_dnca: str | None = None  # 익일예수금
    nxdy_dncl_amt: str | None = None  # 익일예수금액
    prsm_dpast: str | None = None  # 추정예탁자산
    prsm_dpast_amt: str | None = None  # 추정예탁자산금액
    pprt_ord_psbl_cash: str | None = None  # 적정주문가능현금
    add_mgna_cash: str | None = None  # 추가증거금현금
    add_mgna_tota: str | None = None  # 추가증거금총액
    futr_trad_pfls_amt: str | None = None  # 선물매매손익금액
    opt_trad_pfls_amt: str | None = None  # 옵션매매손익금액
    futr_evlu_pfls_amt: str | None = None  # 선물평가손익금액
    opt_evlu_pfls_amt: str | None = None  # 옵션평가손익금액
    trad_pfls_amt_smtl: str | None = None  # 매매손익금액합계
    evlu_pfls_amt_smtl: str | None = None  # 평가손익금액합계
    wdrw_psbl_tot_amt: str | None = None  # 인출가능총금액
    ord_psbl_cash: str | None = None  # 주문가능현금
    ord_psbl_sbst: str | None = None  # 주문가능대용
    ord_psbl_tota: str | None = None  # 주문가능총액

class InquireBalanceValuationPlResponse_Output1Item(KisBaseModel):
    """nested item."""

    cano: str | None = None  # 종합계좌번호
    acnt_prdt_cd: str | None = None  # 계좌상품코드
    pdno: str | None = None  # 상품번호
    prdt_type_cd: str | None = None  # 상품유형코드
    shtn_pdno: str | None = None  # 단축상품번호
    prdt_name: str | None = None  # 상품명
    sll_buy_dvsn_name: str | None = None  # 매도매수구분명
    cblc_qty1: str | None = None  # 잔고수량1
    excc_unpr: str | None = None  # 정산단가
    ccld_avg_unpr1: str | None = None  # 체결평균단가1
    idx_clpr: str | None = None  # 지수종가
    pchs_amt: str | None = None  # 매입금액
    evlu_amt: str | None = None  # 평가금액
    evlu_pfls_amt: str | None = None  # 평가손익금액
    trad_pfls_amt: str | None = None  # 매매손익금액
    lqd_psbl_qty: str | None = None  # 청산가능수량

class InquireBalanceValuationPlResponse(KisCommonResponse):
    """응답 본문."""

    output2: InquireBalanceValuationPlResponse_Output2Item | None = None  # 응답상세
    output1: list[str] = []  # 응답상세2 — array

class InquireBalanceValuationPlExecutor(ApiExecutor[InquireBalanceValuationPlRequest, InquireBalanceValuationPlResponse]):
    """선물옵션 잔고평가손익내역[v1_국내선물-015]."""

    # 선물옵션 잔고평가손익내역 API입니다.

    PATH = "/uapi/domestic-futureoption/v1/trading/inquire-balance-valuation-pl"
    METHOD = "GET"
    RESPONSE_TYPE = InquireBalanceValuationPlResponse
    TR_ID = "CTFO6159R"
