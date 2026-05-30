"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireCreditPsamountRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    PDNO: str  # 상품번호 — 종목코드(6자리)
    ORD_UNPR: str  # 주문단가 — 1주당 가격 * 장전 시간외, 장후 시간외, 시장가의 경우 1주당 가격을 공란으로 비우지 않음 "0"으로 입력 권고
    ORD_DVSN: str  # 주문구분 — 00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 등
    CRDT_TYPE: str  # 신용유형 — 21 : 자기융자신규 23 : 유통융자신규 26 : 유통대주상환 28 : 자기대주상환 25 : 자기융자상환 27 : 유통융자상환 22 : 유통대주신규 24 : 자기대주신규
    CMA_EVLU_AMT_ICLD_YN: str  # CMA평가금액포함여부 — Y/N
    OVRS_ICLD_YN: str  # 해외포함여부 — Y/N

class InquireCreditPsamountResponse_OutputItem(KisBaseModel):
    """nested item."""

    ord_psbl_cash: str | None = None  # 주문가능현금
    ord_psbl_sbst: str | None = None  # 주문가능대용
    ruse_psbl_amt: str | None = None  # 재사용가능금액
    fund_rpch_chgs: str | None = None  # 펀드환매대금
    psbl_qty_calc_unpr: str | None = None  # 가능수량계산단가
    nrcvb_buy_amt: str | None = None  # 미수없는매수금액
    nrcvb_buy_qty: str | None = None  # 미수없는매수수량
    max_buy_amt: str | None = None  # 최대매수금액
    max_buy_qty: str | None = None  # 최대매수수량
    cma_evlu_amt: str | None = None  # CMA평가금액
    ovrs_re_use_amt_wcrc: str | None = None  # 해외재사용금액원화
    ord_psbl_frcr_amt_wcrc: str | None = None  # 주문가능외화금액원화

class InquireCreditPsamountResponse(KisCommonResponse):
    """응답 본문."""

    output: InquireCreditPsamountResponse_OutputItem | None = None  # 응답상세

class InquireCreditPsamountExecutor(ApiExecutor[InquireCreditPsamountRequest, InquireCreditPsamountResponse]):
    """신용매수가능조회[v1_국내주식-042]."""

    # 신용매수가능조회 API입니다. 신용매수주문 시 주문가능수량과 금액을 확인하실 수 있습니다.

    PATH = "/uapi/domestic-stock/v1/trading/inquire-credit-psamount"
    METHOD = "GET"
    RESPONSE_TYPE = InquireCreditPsamountResponse
    TR_ID = "TTTC8909R"
