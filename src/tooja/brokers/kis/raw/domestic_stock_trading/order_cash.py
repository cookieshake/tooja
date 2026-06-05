"""Auto-generated from apiportal spec — do not edit by hand.

NOTE: KIS sends `output` as a bare dict when a single item is returned and as
a list when multiple — the spec annotates it as list. A `field_validator`
below normalizes the single-dict form into a one-element list.
"""

from __future__ import annotations

from pydantic import field_validator

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OrderCashRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드 — 상품유형코드
    PDNO: str  # 상품번호 — 종목코드(6자리) , ETN의 경우 7자리 입력
    SLL_TYPE: str | None = None  # 매도유형 (매도주문 시) — 01@일반매도 02@임의매매 05@대차매도 → 미입력시 01 일반매도로 진행
    ORD_DVSN: str  # 주문구분 — [KRX] 00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정가 
    ORD_QTY: str  # 주문수량
    ORD_UNPR: str  # 주문단가 — 주문단가 시장가 등 주문시, "0"으로 입력
    CNDT_PRIC: str | None = None  # 조건가격 — 스탑지정가호가 주문 (ORD_DVSN이 22) 사용 시에만 필수
    EXCG_ID_DVSN_CD: str | None = None  # 거래소ID구분코드 — 한국거래소 : KRX 대체거래소 (넥스트레이드) : NXT SOR (Smart Order Routing) : SOR → 미입력시 KRX로 진행되며, 모의투자는 KRX만 가능

class OrderCashResponse_OutputItem(KisBaseModel):
    """nested item."""

    KRX_FWDG_ORD_ORGNO: str | None = None  # 계좌관리점코드
    ODNO: str | None = None  # 주문번호
    ORD_TMD: str | None = None  # 주문시간

class OrderCashResponse(KisCommonResponse):
    """응답 본문."""

    output: list[OrderCashResponse_OutputItem] = []  # 응답상세 — single

    @field_validator("output", mode="before")
    @classmethod
    def _wrap_single(cls, v):
        return [v] if isinstance(v, dict) else v

class OrderCashExecutor(ApiExecutor[OrderCashRequest, OrderCashResponse]):
    """주식주문(현금)[v1_국내주식-001]."""

    # 국내주식주문(현금) API 입니다. ※ TTC0012U(현금매수) 사용하셔서 미수매수 가능합니다. 단, 거래하시는 계좌가 증거금40%계좌로 신청이 되어있어야 가능합니다. ※ 신용매수는 별도의 API가 준비되어 있습니다. ※ ORD_QTY(주문수량), ORD_UNPR(주문단가) 등을 String으로 전달해야 함에 유의 부탁드립니다. ※ ORD_UNPR(주문단가)가 없는 주문은 상한가로 주문금액을 선정하고 이후 체결이되면 체결금액

    PATH = "/uapi/domestic-stock/v1/trading/order-cash"
    METHOD = "POST"
    RESPONSE_TYPE = OrderCashResponse
    TR_ID = "TTTC0011U"
    TR_ID_VIRTUAL = "VTTC0011U"
