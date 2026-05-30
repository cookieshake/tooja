"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireBalanceRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    AFHR_FLPR_YN: str  # 시간외단일가, 거래소여부 — N : 기본값, Y : 시간외단일가, X : NXT 정규장 (프리마켓, 메인, 애프터마켓) ※ NXT 선택 시 : NXT 거래종목만 시세 등 정보가 NXT 기준으로 변동됩니다. KRX 종목들은 그대로 유지
    OFL_YN: str | None = None  # 오프라인여부 — 공란(Default)
    INQR_DVSN: str  # 조회구분 — 01 : 대출일별
    UNPR_DVSN: str  # 단가구분 — 01 : 기본값
    FUND_STTL_ICLD_YN: str  # 펀드결제분포함여부 — N : 포함하지 않음 Y : 포함
    FNCG_AMT_AUTO_RDPT_YN: str  # 융자금액자동상환여부 — N : 기본값
    PRCS_DVSN: str  # 처리구분 — 00 : 전일매매포함 01 : 전일매매미포함
    CTX_AREA_FK100: str | None = None  # 연속조회검색조건100 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)
    CTX_AREA_NK100: str | None = None  # 연속조회키100 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)

class InquireBalanceResponse_Output1Item(KisBaseModel):
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
    evlu_erng_rt: str | None = None  # 평가수익율 — 미사용항목(0으로 출력)
    loan_dt: str | None = None  # 대출일자 — INQR_DVSN(조회구분)을 01(대출일별)로 설정해야 값이 나옴
    loan_amt: str | None = None  # 대출금액
    stln_slng_chgs: str | None = None  # 대주매각대금
    expd_dt: str | None = None  # 만기일자
    fltt_rt: str | None = None  # 등락율
    bfdy_cprs_icdc: str | None = None  # 전일대비증감
    item_mgna_rt_name: str | None = None  # 종목증거금율명
    grta_rt_name: str | None = None  # 보증금율명
    sbst_pric: str | None = None  # 대용가격 — 증권매매의 위탁보증금으로서 현금 대신에 사용되는 유가증권 가격
    stck_loan_unpr: str | None = None  # 주식대출단가

class InquireBalanceResponse_Output2Item(KisBaseModel):
    """nested item."""

    dnca_tot_amt: str | None = None  # 예수금총금액 — 예수금
    nxdy_excc_amt: str | None = None  # 익일정산금액 — D+1 예수금
    prvs_rcdl_excc_amt: str | None = None  # 가수도정산금액 — D+2 예수금
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
    tot_evlu_amt: str | None = None  # 총평가금액 — 유가증권 평가금액 합계금액 + D+2 예수금
    nass_amt: str | None = None  # 순자산금액
    fncg_gld_auto_rdpt_yn: str | None = None  # 융자금자동상환여부 — 보유현금에 대한 융자금만 차감여부 신용융자 매수체결 시점에서는 융자비율을 매매대금 100%로 계산 하였다가 수도결제일에 보증금에 해당하는 금액을 고객의 현금으로 충당하여 융자금을 감소시키는 업무
    pchs_amt_smtl_amt: str | None = None  # 매입금액합계금액
    evlu_amt_smtl_amt: str | None = None  # 평가금액합계금액 — 유가증권 평가금액 합계금액
    evlu_pfls_smtl_amt: str | None = None  # 평가손익합계금액
    tot_stln_slng_chgs: str | None = None  # 총대주매각대금
    bfdy_tot_asst_evlu_amt: str | None = None  # 전일총자산평가금액
    asst_icdc_amt: str | None = None  # 자산증감액
    asst_icdc_erng_rt: str | None = None  # 자산증감수익율 — 데이터 미제공

class InquireBalanceResponse(KisCommonResponse):
    """응답 본문."""

    ctx_area_fk100: str | None = None  # 연속조회검색조건100
    ctx_area_nk100: str | None = None  # 연속조회키100
    output1: list[InquireBalanceResponse_Output1Item] = []  # 응답상세1 — Array
    output2: list[InquireBalanceResponse_Output2Item] = []  # 응답상세2 — Array

class InquireBalanceExecutor(ApiExecutor[InquireBalanceRequest, InquireBalanceResponse]):
    """주식잔고조회[v1_국내주식-006]."""

    # 주식 잔고조회 API입니다. 실전계좌의 경우, 한 번의 호출에 최대 50건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다. 모의계좌의 경우, 한 번의 호출에 최대 20건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다. * 당일 전량매도한 잔고도 보유수량 0으로 보여질 수 있으나, 해당 보유수량 0인 잔고는 최종 D-2일 이후에는 잔고에서 사라집니다. ※ 중요 : 해당 API는 제공

    PATH = "/uapi/domestic-stock/v1/trading/inquire-balance"
    METHOD = "GET"
    RESPONSE_TYPE = InquireBalanceResponse
    TR_ID = "TTTC8434R"
    TR_ID_VIRTUAL = "VTTC8434R"
