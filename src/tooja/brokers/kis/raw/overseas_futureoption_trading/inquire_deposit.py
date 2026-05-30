"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireDepositRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    CRCY_CD: str  # 통화코드 — TUS: TOT_USD / TKR: TOT_KRW KRW: 한국 / USD: 미국 EUR: EUR / HKD: 홍콩 CNY: 중국 / JPY: 일본 VND: 베트남
    INQR_DT: str  # 조회일자

class InquireDepositResponse_OutputItem(KisBaseModel):
    """nested item."""

    fm_nxdy_dncl_amt: str | None = None  # FM익일예수금액
    fm_tot_asst_evlu_amt: str | None = None  # FM총자산평가금액
    cano: str | None = None  # 종합계좌번호
    acnt_prdt_cd: str | None = None  # 계좌상품코드
    crcy_cd: str | None = None  # 통화코드
    resp_dt: str | None = None  # 응답일자
    fm_dnca_rmnd: str | None = None  # FM예수금잔액
    fm_lqd_pfls_amt: str | None = None  # FM청산손익금액
    fm_fee: str | None = None  # FM수수료
    fm_fuop_evlu_pfls_amt: str | None = None  # FM선물옵션평가손익금액
    fm_rcvb_amt: str | None = None  # FM미수금액
    fm_brkg_mgn_amt: str | None = None  # FM위탁증거금액
    fm_mntn_mgn_amt: str | None = None  # FM유지증거금액
    fm_add_mgn_amt: str | None = None  # FM추가증거금액
    fm_risk_rt: str | None = None  # FM위험율
    fm_ord_psbl_amt: str | None = None  # FM주문가능금액
    fm_drwg_psbl_amt: str | None = None  # FM출금가능금액
    fm_echm_rqrm_amt: str | None = None  # FM환전요청금액
    fm_drwg_prar_amt: str | None = None  # FM출금예정금액
    fm_opt_tr_chgs: str | None = None  # FM옵션거래대금
    fm_opt_icld_asst_evlu_amt: str | None = None  # FM옵션포함자산평가금액
    fm_opt_evlu_amt: str | None = None  # FM옵션평가금액
    fm_crcy_sbst_amt: str | None = None  # FM통화대용금액
    fm_crcy_sbst_use_amt: str | None = None  # FM통화대용사용금액
    fm_crcy_sbst_stup_amt: str | None = None  # FM통화대용설정금액

class InquireDepositResponse(KisCommonResponse):
    """응답 본문."""

    output: InquireDepositResponse_OutputItem | None = None  # 응답상세1

class InquireDepositExecutor(ApiExecutor[InquireDepositRequest, InquireDepositResponse]):
    """해외선물옵션 예수금현황[해외선물-012]."""

    # 해외선물옵션 예수금현황 API입니다.

    PATH = "/uapi/overseas-futureoption/v1/trading/inquire-deposit"
    METHOD = "GET"
    RESPONSE_TYPE = InquireDepositResponse
    TR_ID = "OTFM1411R"
