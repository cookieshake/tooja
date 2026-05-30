"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OrderRvsecnclRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — -
    ACNT_PRDT_CD: str  # 계좌상품코드 — -
    PDNO: str  # 상품번호 — -
    ORGN_ODNO: str  # 원주문번호 — -
    ORD_QTY2: str  # 주문수량2 — 원주문이 일반시장 주문일 시 10단위 입력
    BOND_ORD_UNPR: str  # 채권주문단가 — -
    QTY_ALL_ORD_YN: str  # 잔량전부주문여부 — Y: 잔량전부(주문수량 입력안함),
    RVSE_CNCL_DVSN_CD: str  # 정정취소구분코드 — 01: 정정, 02: 취소
    MGCO_APTM_ODNO: str  # 운용사지정주문번호 — 공백
    ORD_SVR_DVSN_CD: str  # 주문서버구분코드 — Unique key(0)
    CTAC_TLNO: str  # 연락전화번호 — -

class OrderRvsecnclResponse_OutputItem(KisBaseModel):
    """nested item."""

    krx_fwdg_ord_orgno: str | None = None  # 한국거래소전송주문조직번호
    odno: str | None = None  # 주문번호
    ord_tmd: str | None = None  # 주문시각

class OrderRvsecnclResponse(KisCommonResponse):
    """응답 본문."""

    output: OrderRvsecnclResponse_OutputItem | None = None  # 응답상세

class OrderRvsecnclExecutor(ApiExecutor[OrderRvsecnclRequest, OrderRvsecnclResponse]):
    """장내채권 정정취소주문 [국내주식-125]."""

    # 장내채권 정정취소주문 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0978] 장내채권주문 '채권정정/취소' 탭의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-bond/v1/trading/order-rvsecncl"
    METHOD = "POST"
    RESPONSE_TYPE = OrderRvsecnclResponse
    TR_ID = "TTTC0953U"
