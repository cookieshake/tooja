"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class SellRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드
    ORD_DVSN: str  # 주문구분 — '01: 종목별 (매수일자, 매수순번 공백입력) 02: 일자별 (매수순번: 0 입력) 03: 체결가별 '
    PDNO: str  # 상품번호
    ORD_QTY2: str  # 주문수량2 — SAMT_MKET_PTCI_YN(소액시장참여여부) : N(일반시장) 입력 시 10단위 입력
    BOND_ORD_UNPR: str  # 주문단가
    SPRX_YN: str  # 분리과세여부 — N: 종합과세, Y:분리과세
    BUY_DT: str  # 매수일자 — (잔고조회 참조)
    BUY_SEQ: str  # 매수순번 — (잔고조회 참조)
    SAMT_MKET_PTCI_YN: str  # 소액시장참여여부 — N: 일반시장, Y: 소액시장
    SLL_AGCO_OPPS_SLL_YN: str  # 매도대행사반대매도여부 — N
    BOND_RTL_MKET_YN: str  # 채권소매시장여부 — N
    MGCO_APTM_ODNO: str  # 운용사지정주문번호 — 공백
    ORD_SVR_DVSN_CD: str  # 주문서버구분코드 — Unique key(0)
    CTAC_TLNO: str  # 연락전화번호

class SellResponse_OutputItem(KisBaseModel):
    """nested item."""

    krx_fwdg_ord_orgno: str | None = None  # 한국거래소전송주문조직번호
    odno: str | None = None  # 주문번호
    ord_tmd: str | None = None  # 주문시각

class SellResponse(KisCommonResponse):
    """응답 본문."""

    output: SellResponse_OutputItem | None = None  # 응답상세

class SellExecutor(ApiExecutor[SellRequest, SellResponse]):
    """장내채권 매도주문 [국내주식-123]."""

    # 장내채권 매도주문 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0978] 장내채권주문 '채권매도' 탭의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-bond/v1/trading/sell"
    METHOD = "POST"
    RESPONSE_TYPE = SellResponse
    TR_ID = "TTTC0958U"
