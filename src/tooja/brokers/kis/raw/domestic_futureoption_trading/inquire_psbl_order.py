"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePsblOrderRequest(KisBaseModel):
    """요청."""

    CANO: str | None = None  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str | None = None  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    PDNO: str | None = None  # 상품번호 — 선물옵션종목코드 선물 6자리 (예: 101S03) 옵션 9자리 (예: 201S03370)
    SLL_BUY_DVSN_CD: str | None = None  # 매도매수구분코드 — 01 : 매도 02 : 매수
    UNIT_PRICE: str | None = None  # 주문가격1 — 주문가격 ※ 주문가격 '0'일 경우 - 옵션매수 : 현재가 - 그 이외 : 기준가
    ORD_DVSN_CD: str | None = None  # 주문구분코드 — 01 : 지정가 02 : 시장가 03 : 조건부 04 : 최유리, 10 : 지정가(IOC) 11 : 지정가(FOK) 12 : 시장가(IOC) 13 : 시장가(FOK) 14 : 최유리(IOC) 15 : 최유리(FOK)

class InquirePsblOrderResponse_OutputItem(KisBaseModel):
    """nested item."""

    tot_psbl_qty: str | None = None  # 총가능수량
    lqd_psbl_qty1: str | None = None  # 청산가능수량1 — 청산가능수량
    ord_psbl_qty: str | None = None  # 주문가능수량
    bass_idx: str | None = None  # 기준지수

class InquirePsblOrderResponse(KisCommonResponse):
    """응답 본문."""

    output: list[str] = []  # 응답상세

class InquirePsblOrderExecutor(ApiExecutor[InquirePsblOrderRequest, InquirePsblOrderResponse]):
    """선물옵션 주문가능[v1_국내선물-005]."""

    # 선물옵션 주문가능 API입니다. 주문가능 내역과 수량을 확인하실 수 있습니다.

    PATH = "/uapi/domestic-futureoption/v1/trading/inquire-psbl-order"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePsblOrderResponse
    TR_ID = "TTTO5105R"
    TR_ID_VIRTUAL = "VTTO5105R"
