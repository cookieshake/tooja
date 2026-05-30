"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireDepositRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리

class InquireDepositResponse_OutputItem(KisBaseModel):
    """nested item."""

    dnca_tota: str | None = None  # 예수금총액
    bfdy_chck_amt: str | None = None  # 전일수표금액
    thdt_chck_amt: str | None = None  # 당일수표금액
    rlth_uwdl_dpos_amt: str | None = None  # 실물인수도예치금액
    brkg_mgna_cash: str | None = None  # 위탁증거금현금
    wdrw_psbl_tot_amt: str | None = None  # 인출가능총금액
    ord_psbl_cash: str | None = None  # 주문가능현금
    ord_psbl_tota: str | None = None  # 주문가능총액
    dnca_sbst: str | None = None  # 예수금대용
    scts_sbst_amt: str | None = None  # 유가증권대용금액
    frcr_evlu_amt: str | None = None  # 외화평가금액
    brkg_mgna_sbst: str | None = None  # 위탁증거금대용
    sbst_rlse_psbl_amt: str | None = None  # 대용해제가능금액
    mtnc_rt: str | None = None  # 유지비율
    add_mgna_tota: str | None = None  # 추가증거금총액
    add_mgna_cash: str | None = None  # 추가증거금현금
    rcva: str | None = None  # 미수금
    futr_trad_pfls: str | None = None  # 선물매매손익
    opt_trad_pfls_amt: str | None = None  # 옵션매매손익금액
    trad_pfls_smtl: str | None = None  # 매매손익합계
    futr_evlu_pfls_amt: str | None = None  # 선물평가손익금액
    opt_evlu_pfls_amt: str | None = None  # 옵션평가손익금액
    evlu_pfls_smtl: str | None = None  # 평가손익합계
    excc_dfpa: str | None = None  # 정산차금
    opt_dfpa: str | None = None  # 옵션차금
    brkg_fee: str | None = None  # 위탁수수료
    nxdy_dnca: str | None = None  # 익일예수금
    prsm_dpast_amt: str | None = None  # 추정예탁자산금액
    cash_mntn_amt: str | None = None  # 현금유지금액
    hack_acdt_acnt_move_amt: str | None = None  # 해킹사고계좌이전금액

class InquireDepositResponse(KisCommonResponse):
    """응답 본문."""

    output: InquireDepositResponse_OutputItem | None = None  # 응답상세

class InquireDepositExecutor(ApiExecutor[InquireDepositRequest, InquireDepositResponse]):
    """선물옵션 총자산현황[v1_국내선물-014]."""

    # 선물옵션 총자산현황 API 입니다.

    PATH = "/uapi/domestic-futureoption/v1/trading/inquire-deposit"
    METHOD = "GET"
    RESPONSE_TYPE = InquireDepositResponse
    TR_ID = "CTRP6550R"
