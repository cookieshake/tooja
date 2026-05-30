"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePsblOrderRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드
    PDNO: str  # 상품번호
    BOND_ORD_UNPR: str  # 채권주문단가
    SAMT_MKET_PTCI_YN: str  # 소액시장참여여부 — Y(소액시장) N (일반시장)

class InquirePsblOrderResponse_OutputItem(KisBaseModel):
    """nested item."""

    ord_psbl_cash: str | None = None  # 주문가능현금
    ord_psbl_sbst: str | None = None  # 주문가능대용
    ruse_psbl_amt: str | None = None  # 재사용가능금액
    bond_ord_unpr2: str | None = None  # 채권주문단가2
    buy_psbl_amt: str | None = None  # 매수가능금액
    buy_psbl_qty: str | None = None  # 매수가능수량 — 매수가능수량(buy_psbl_qty) = 매수가능금액(buy_psbl_amt) / 채권주문단가2(bond_ord_unpr2) * 10
    cma_evlu_amt: str | None = None  # CMA평가금액

class InquirePsblOrderResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InquirePsblOrderResponse_OutputItem] = []  # 응답상세 — array

class InquirePsblOrderExecutor(ApiExecutor[InquirePsblOrderRequest, InquirePsblOrderResponse]):
    """장내채권 매수가능조회 [국내주식-199]."""

    # 장내채권 매수가능조회 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0978] 장내채권주문 화면의 "왼쪽 하단 증거금 사용가능 내역 / 주문가능금액 및 수량" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ (중요) 채권의 경우 주식과 달리, 매수가능수량(buy_psbl_qty) = 매수가능금액(buy_psbl_amt) / 채권주문단가2(bond_ord_unpr2) *

    PATH = "/uapi/domestic-bond/v1/trading/inquire-psbl-order"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePsblOrderResponse
    TR_ID = "TTTC8910R"
