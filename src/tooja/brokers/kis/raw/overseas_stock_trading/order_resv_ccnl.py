"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OrderResvCcnlRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    RSYN_ORD_RCIT_DT: str  # 해외주문접수일자
    OVRS_RSVN_ODNO: str  # 해외예약주문번호 — 해외주식_예약주문접수 API Output ODNO(주문번호) 참고

class OrderResvCcnlResponse_OutputItem(KisBaseModel):
    """nested item."""

    OVRS_RSVN_ODNO: str | None = None  # 해외예약주문번호

class OrderResvCcnlResponse(KisCommonResponse):
    """응답 본문."""

    output: OrderResvCcnlResponse_OutputItem | None = None  # 응답상세

class OrderResvCcnlExecutor(ApiExecutor[OrderResvCcnlRequest, OrderResvCcnlResponse]):
    """해외주식 예약주문접수취소[v1_해외주식-004]."""

    # 접수된 미국주식 예약주문을 취소하기 위한 API입니다. (해외주식 예약주문접수 시 Return 받은 ODNO를 참고하여 API를 호출하세요.) * 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고) https://securities.koreainvestment.com/main/bond/research/_static/TF03ca010001.jsp ※ POST API의 경우 BODY값의 key값들

    PATH = "/uapi/overseas-stock/v1/trading/order-resv-ccnl"
    METHOD = "POST"
    RESPONSE_TYPE = OrderResvCcnlResponse
    TR_ID = "TTTT3017U"
    TR_ID_VIRTUAL = "VTTT3017U"
