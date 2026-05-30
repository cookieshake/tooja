"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireAccountBalanceRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    INQR_DVSN_1: str  # 조회구분1 — 공백입력
    BSPR_BF_DT_APLY_YN: str  # 기준가이전일자적용여부 — 공백입력

class InquireAccountBalanceResponse_Output1Item(KisBaseModel):
    """nested item."""

    pchs_amt: str | None = None  # 매입금액
    evlu_amt: str | None = None  # 평가금액
    evlu_pfls_amt: str | None = None  # 평가손익금액
    crdt_lnd_amt: str | None = None  # 신용대출금액
    real_nass_amt: str | None = None  # 실제순자산금액
    whol_weit_rt: str | None = None  # 전체비중율

class InquireAccountBalanceResponse_Output2Item(KisBaseModel):
    """nested item."""

    pchs_amt_smtl: str | None = None  # 매입금액합계 — 유가매입금액
    nass_tot_amt: str | None = None  # 순자산총금액
    loan_amt_smtl: str | None = None  # 대출금액합계
    evlu_pfls_amt_smtl: str | None = None  # 평가손익금액합계 — 평가손익금액
    evlu_amt_smtl: str | None = None  # 평가금액합계 — 유가평가금액
    tot_asst_amt: str | None = None  # 총자산금액 — 총 자산금액
    tot_lnda_tot_ulst_lnda: str | None = None  # 총대출금액총융자대출금액
    cma_auto_loan_amt: str | None = None  # CMA자동대출금액
    tot_mgln_amt: str | None = None  # 총담보대출금액
    stln_evlu_amt: str | None = None  # 대주평가금액
    crdt_fncg_amt: str | None = None  # 신용융자금액
    ocl_apl_loan_amt: str | None = None  # OCL_APL대출금액
    pldg_stup_amt: str | None = None  # 질권설정금액
    frcr_evlu_tota: str | None = None  # 외화평가총액
    tot_dncl_amt: str | None = None  # 총예수금액
    cma_evlu_amt: str | None = None  # CMA평가금액
    dncl_amt: str | None = None  # 예수금액
    tot_sbst_amt: str | None = None  # 총대용금액
    thdt_rcvb_amt: str | None = None  # 당일미수금액
    ovrs_stck_evlu_amt1: str | None = None  # 해외주식평가금액1
    ovrs_bond_evlu_amt: str | None = None  # 해외채권평가금액
    mmf_cma_mgge_loan_amt: str | None = None  # MMFCMA담보대출금액
    sbsc_dncl_amt: str | None = None  # 청약예수금액
    pbst_sbsc_fnds_loan_use_amt: str | None = None  # 공모주청약자금대출사용금액
    etpr_crdt_grnt_loan_amt: str | None = None  # 기업신용공여대출금액

class InquireAccountBalanceResponse(KisCommonResponse):
    """응답 본문."""

    Output1: list[InquireAccountBalanceResponse_Output1Item] = []  # 응답상세 — Array [아래 순서대로 출력 : 20항목] 1: 주식 2: 펀드/MMW 3: IMA 4: 채권 5: ELS/DLS 6: WRAP 7: 신탁 8: RP/발행어음 9: 해외주식 10: 해외채권 11: 금현물 12: CD/CP 13: 전자단
    Output2: InquireAccountBalanceResponse_Output2Item | None = None  # 응답상세2

class InquireAccountBalanceExecutor(ApiExecutor[InquireAccountBalanceRequest, InquireAccountBalanceResponse]):
    """투자계좌자산현황조회[v1_국내주식-048]."""

    # 투자계좌자산현황조회 API입니다. output1은 한국투자 HTS(eFriend Plus) &gt; [0891] 계좌 자산비중(결제기준) 화면 아래 테이블의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/trading/inquire-account-balance"
    METHOD = "GET"
    RESPONSE_TYPE = InquireAccountBalanceResponse
    TR_ID = "CTRP6548R"
