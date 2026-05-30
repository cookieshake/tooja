"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireBalanceRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드
    INQR_CNDT: str  # 조회조건 — 00: 전체, 01: 상품번호단위
    PDNO: str  # 상품번호 — 공백
    BUY_DT: str  # 매수일자 — 공백
    CTX_AREA_FK200: str  # 연속조회검색조건200
    CTX_AREA_NK200: str  # 연속조회키200

class InquireBalanceResponse_OutputItem(KisBaseModel):
    """nested item."""

    pdno: str | None = None  # 상품번호
    prdt_name: str | None = None  # 상품명
    buy_dt: str | None = None  # 매수일자
    buy_sqno: str | None = None  # 매수일련번호
    cblc_qty: str | None = None  # 잔고수량
    agrx_qty: str | None = None  # 종합과세수량
    sprx_qty: str | None = None  # 분리과세수량
    exdt: str | None = None  # 만기일
    buy_erng_rt: str | None = None  # 매수수익율
    buy_unpr: str | None = None  # 매수단가
    buy_amt: str | None = None  # 매수금액
    ord_psbl_qty: str | None = None  # 주문가능수량

class InquireBalanceResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InquireBalanceResponse_OutputItem] = []  # 응답상세 — array

class InquireBalanceExecutor(ApiExecutor[InquireBalanceRequest, InquireBalanceResponse]):
    """장내채권 잔고조회  [국내주식-198]."""

    # 장내채권 잔고조회 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0979] 장내채권종합주문 화면의 "왼쪽 하단 잔고" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-bond/v1/trading/inquire-balance"
    METHOD = "GET"
    RESPONSE_TYPE = InquireBalanceResponse
    TR_ID = "CTSC8407R"
