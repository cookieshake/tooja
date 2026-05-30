"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class BuyRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드
    PDNO: str  # 상품번호
    ORD_QTY2: str  # 주문수량2 — SAMT_MKET_PTCI_YN(소액시장참여여부) : N(일반시장) 입력 시 10단위 입력
    BOND_ORD_UNPR: str  # 채권주문단가
    SAMT_MKET_PTCI_YN: str  # 소액시장참여여부 — N: 일반시장, Y: 소액시장
    BOND_RTL_MKET_YN: str  # 채권소매시장여부 — Y, N
    IDCR_STFNO: str  # 유치자직원번호 — 공백
    MGCO_APTM_ODNO: str  # 운용사지정주문번호 — 공백
    ORD_SVR_DVSN_CD: str  # 주문서버구분코드 — Unique key(0)
    CTAC_TLNO: str  # 연락전화번호

class BuyResponse_OutputItem(KisBaseModel):
    """nested item."""

    krx_fwdg_ord_orgno: str | None = None  # 한국거래소전송주문조직번호
    odno: str | None = None  # 주문번호
    ord_tmd: str | None = None  # 주문시각

class BuyResponse(KisCommonResponse):
    """응답 본문."""

    output: BuyResponse_OutputItem | None = None  # 응답상세

class BuyExecutor(ApiExecutor[BuyRequest, BuyResponse]):
    """장내채권 매수주문 [국내주식-124]."""

    # 장내채권 매수주문 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0978] 장내채권주문 '채권매수' 탭의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-bond/v1/trading/buy"
    METHOD = "POST"
    RESPONSE_TYPE = BuyResponse
    TR_ID = "TTTC0952U"
