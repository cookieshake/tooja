"""Auto-generated from apiportal spec — do not edit by hand.

NOTE: KIS sends `output` as a bare dict when a single item is returned and as
a list when multiple — the spec annotates it as list. A `field_validator`
below normalizes the single-dict form into a one-element list. (Same quirk as
order_cash.py.)
"""

from __future__ import annotations

from pydantic import field_validator

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OrderRvsecnclRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드 — 상품유형코드
    KRX_FWDG_ORD_ORGNO: str  # 한국거래소전송주문조직번호
    ORGN_ODNO: str  # 원주문번호
    ORD_DVSN: str  # 주문구분 — [KRX] 00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정가 
    RVSE_CNCL_DVSN_CD: str  # 정정취소구분코드 — 01@정정 02@취소
    ORD_QTY: str  # 주문수량
    ORD_UNPR: str  # 주문단가
    QTY_ALL_ORD_YN: str  # 잔량전부주문여부 — 'Y@전량 N@일부'
    CNDT_PRIC: str | None = None  # 조건가격 — 스탑지정가호가에서 사용
    EXCG_ID_DVSN_CD: str | None = None  # 거래소ID구분코드 — 한국거래소 : KRX 대체거래소 (넥스트레이드) : NXT SOR (Smart Order Routing) : SOR → 미입력시 KRX로 진행되며, 모의투자는 KRX만 가능

class OrderRvsecnclResponse_OutputItem(KisBaseModel):
    """nested item.

    NOTE: KIS returns these output keys UPPER-CASE (KRX_FWDG_ORD_ORGNO / ODNO /
    ORD_TMD), like order-cash. The codegen emitted them lower-case, so every
    field parsed as None and the adapter mis-read a successful cancel as a
    rejection. Field names corrected to match the wire.
    """

    KRX_FWDG_ORD_ORGNO: str | None = None  # 한국거래소전송주문조직번호
    ODNO: str | None = None  # 주문번호
    ORD_TMD: str | None = None  # 주문시각

class OrderRvsecnclResponse(KisCommonResponse):
    """응답 본문."""

    output: list[OrderRvsecnclResponse_OutputItem] = []  # 응답상세 — single

    @field_validator("output", mode="before")
    @classmethod
    def _wrap_single(cls, v):
        return [v] if isinstance(v, dict) else v

class OrderRvsecnclExecutor(ApiExecutor[OrderRvsecnclRequest, OrderRvsecnclResponse]):
    """주식주문(정정취소)[v1_국내주식-003]."""

    # 주문 건에 대하여 정정 및 취소하는 API입니다. 단, 이미 체결된 건은 정정 및 취소가 불가합니다. ※ 정정은 원주문에 대한 주문단가 혹은 주문구분을 변경하는 사항으로, 정정이 가능한 수량은 원주문수량을 초과 할 수 없습니다. ※ 주식주문(정정취소) 호출 전에 반드시 주식정정취소가능주문조회 호출을 통해 정정취소가능수량(output &gt; psbl_qty)을 확인하신 후 정정취소주문 내시기 바랍니다. ※ POST API의 경

    PATH = "/uapi/domestic-stock/v1/trading/order-rvsecncl"
    METHOD = "POST"
    RESPONSE_TYPE = OrderRvsecnclResponse
    TR_ID = "TTTC0013U"
    TR_ID_VIRTUAL = "VTTC0013U"
