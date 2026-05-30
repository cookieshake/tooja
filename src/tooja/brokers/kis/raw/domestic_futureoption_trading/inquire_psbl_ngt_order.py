"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePsblNgtOrderRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드
    PDNO: str  # 상품번호
    PRDT_TYPE_CD: str  # 상품유형코드 — 301 : 선물옵션
    SLL_BUY_DVSN_CD: str  # 매도매수구분코드 — 01 : 매도 , 02 : 매수
    UNIT_PRICE: str  # 주문가격1
    ORD_DVSN_CD: str  # 주문구분코드 — '01 : 지정가 02 : 시장가 03 : 조건부 04 : 최유리, 10 : 지정가(IOC) 11 : 지정가(FOK) 12 : 시장가(IOC) 13 : 시장가(FOK) 14 : 최유리(IOC) 15 : 최유리(FOK)'

class InquirePsblNgtOrderResponse_OutputItem(KisBaseModel):
    """nested item."""

    max_ord_psbl_qty: str | None = None  # 최대주문가능수량 — 최대주문가능수량 (신규 TR 미사용 필드)
    tot_psbl_qty: str | None = None  # 최대주문가능수량
    lqd_psbl_qty: str | None = None  # 청산가능수량
    lqd_psbl_qty_1: str | None = None  # 청산가능수량 — 신규 TR 사용 필드
    ord_psbl_qty: str | None = None  # 주문가능수량
    bass_idx: str | None = None  # 기준지수 — 신규 TR 사용 필드

class InquirePsblNgtOrderResponse(KisCommonResponse):
    """응답 본문."""

    output: InquirePsblNgtOrderResponse_OutputItem | None = None  # 응답상세1

class InquirePsblNgtOrderExecutor(ApiExecutor[InquirePsblNgtOrderRequest, InquirePsblNgtOrderResponse]):
    """(야간)선물옵션 주문가능 조회 [국내선물-011]."""

    # (야간)선물옵션 주문가능 조회 API입니다.

    PATH = "/uapi/domestic-futureoption/v1/trading/inquire-psbl-ngt-order"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePsblNgtOrderResponse
    TR_ID = "JTCE1004R"
