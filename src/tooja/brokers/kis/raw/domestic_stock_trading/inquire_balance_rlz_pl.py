"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireBalanceRlzPlRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    AFHR_FLPR_YN: str  # 시간외단일가여부 — 'N : 기본값 Y : 시간외단일가'
    OFL_YN: str  # 오프라인여부 — 공란
    INQR_DVSN: str  # 조회구분 — 00 : 전체
    UNPR_DVSN: str  # 단가구분 — 01 : 기본값
    FUND_STTL_ICLD_YN: str  # 펀드결제포함여부 — N : 포함하지 않음 Y : 포함
    FNCG_AMT_AUTO_RDPT_YN: str  # 융자금액자동상환여부 — N : 기본값
    PRCS_DVSN: str  # PRCS_DVSN — 00 : 전일매매포함 01 : 전일매매미포함
    COST_ICLD_YN: str  # 비용포함여부
    CTX_AREA_FK100: str  # 연속조회검색조건100 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)
    CTX_AREA_NK100: str  # 연속조회키100 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)

class InquireBalanceRlzPlResponse_Output1Item(KisBaseModel):
    """nested item."""

    pdno: str | None = None  # 상품번호 — 종목번호(뒷 6자리)
    prdt_name: str | None = None  # 상품명 — 종목명
    trad_dvsn_name: str | None = None  # 매매구분명 — 매수매도구분
    bfdy_buy_qty: str | None = None  # 전일매수수량
    bfdy_sll_qty: str | None = None  # 전일매도수량
    thdt_buyqty: str | None = None  # 금일매수수량
    thdt_sll_qty: str | None = None  # 금일매도수량
    hldg_qty: str | None = None  # 보유수량
    ord_psbl_qty: str | None = None  # 주문가능수량
    pchs_avg_pric: str | None = None  # 매입평균가격 — 매입금액 / 보유수량
    pchs_amt: str | None = None  # 매입금액
    prpr: str | None = None  # 현재가
    evlu_amt: str | None = None  # 평가금액
    evlu_pfls_amt: str | None = None  # 평가손익금액 — 평가금액 - 매입금액
    evlu_pfls_rt: str | None = None  # 평가손익율
    evlu_erng_rt: str | None = None  # 평가수익율
    loan_dt: str | None = None  # 대출일자
    loan_amt: str | None = None  # 대출금액
    stln_slng_chgs: str | None = None  # 대주매각대금 — 신용 거래에서, 고객이 증권 회사로부터 대부받은 주식의 매각 대금
    expd_dt: str | None = None  # 만기일자
    stck_loan_unpr: str | None = None  # 주식대출단가
    bfdy_cprs_icdc: str | None = None  # 전일대비증감
    fltt_rt: str | None = None  # 등락율

class InquireBalanceRlzPlResponse_Output2Item(KisBaseModel):
    """nested item."""

    dnca_tot_amt: str | None = None  # 예수금총금액
    nxdy_excc_amt: str | None = None  # 익일정산금액
    prvs_rcdl_excc_amt: str | None = None  # 가수도정산금액
    cma_evlu_amt: str | None = None  # CMA평가금액
    bfdy_buy_amt: str | None = None  # 전일매수금액
    thdt_buy_amt: str | None = None  # 금일매수금액
    nxdy_auto_rdpt_amt: str | None = None  # 익일자동상환금액
    bfdy_sll_amt: str | None = None  # 전일매도금액
    thdt_sll_amt: str | None = None  # 금일매도금액
    d2_auto_rdpt_amt: str | None = None  # D+2자동상환금액
    bfdy_tlex_amt: str | None = None  # 전일제비용금액
    thdt_tlex_amt: str | None = None  # 금일제비용금액
    tot_loan_amt: str | None = None  # 총대출금액
    scts_evlu_amt: str | None = None  # 유가평가금액
    tot_evlu_amt: str | None = None  # 총평가금액
    nass_amt: str | None = None  # 순자산금액
    fncg_gld_auto_rdpt_yn: str | None = None  # 융자금자동상환여부
    pchs_amt_smtl_amt: str | None = None  # 매입금액합계금액
    evlu_amt_smtl_amt: str | None = None  # 평가금액합계금액
    evlu_pfls_smtl_amt: str | None = None  # 평가손익합계금액
    tot_stln_slng_chgs: str | None = None  # 총대주매각대금
    bfdy_tot_asst_evlu_amt: str | None = None  # 전일총자산평가금액
    asst_icdc_amt: str | None = None  # 자산증감액
    asst_icdc_erng_rt: str | None = None  # 자산증감수익율
    rlzt_pfls: str | None = None  # 실현손익
    rlzt_erng_rt: str | None = None  # 실현수익율
    real_evlu_pfls: str | None = None  # 실평가손익
    real_evlu_pfls_erng_rt: str | None = None  # 실평가손익수익율

class InquireBalanceRlzPlResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[InquireBalanceRlzPlResponse_Output1Item] = []  # 응답상세 — Array
    output2: list[InquireBalanceRlzPlResponse_Output2Item] = []  # 응답상세2 — Array

class InquireBalanceRlzPlExecutor(ApiExecutor[InquireBalanceRlzPlRequest, InquireBalanceRlzPlResponse]):
    """주식잔고조회_실현손익[v1_국내주식-041]."""

    # 주식잔고조회_실현손익 API입니다. 한국투자 HTS(eFriend Plus) [0800] 국내 체결기준잔고 화면을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. (참고: 포럼 - 공지사항 - 신규 API 추가 안내(주식잔고조회_실현손익 외 1건))

    PATH = "/uapi/domestic-stock/v1/trading/inquire-balance-rlz-pl"
    METHOD = "GET"
    RESPONSE_TYPE = InquireBalanceRlzPlResponse
    TR_ID = "TTTC8494R"
