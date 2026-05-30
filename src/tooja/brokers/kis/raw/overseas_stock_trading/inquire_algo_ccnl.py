"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireAlgoCcnlRequest(KisBaseModel):
    """요청."""

    CANO: str  # 계좌번호 — 종합계좌번호 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 상품코드 2자리 (주식계좌 : 01)
    ORD_DT: str  # 주문일자 — 주문일자 (YYYYMMDD)
    ORD_GNO_BRNO: str | None = None  # 주문채번지점번호 — TTS6058R 조회 시 해당 주문번호(odno)의 ord_gno_brno 입력
    ODNO: str  # 주문번호 — 지정가주문번호 (TTTS6058R)에서 조회된 주문번호 입력
    TTLZ_ICLD_YN: str | None = None  # 집계포함여부
    CTX_AREA_NK200: str | None = None  # 연속조회키200 — 연속조회 시 사용
    CTX_AREA_FK200: str | None = None  # 연속조회조건200 — 연속조회 시 사용

class InquireAlgoCcnlResponse_OutputItem(KisBaseModel):
    """nested item."""

    CCLD_SEQ: str | None = None  # 체결순번
    CCLD_BTWN: str | None = None  # 체결시간 — HHMMSS
    PDNO: str | None = None  # 상품번호
    ITEM_NAME: str | None = None  # 종목명
    FT_CCLD_QTY: str | None = None  # FT체결수량
    FT_CCLD_UNPR3: str | None = None  # FT체결단가
    FT_CCLD_AMT3: str | None = None  # FT체결금액

class InquireAlgoCcnlResponse_Output3Item(KisBaseModel):
    """nested item."""

    ODNO: str | None = None  # 주문번호
    TRAD_DVSN_NAME: str | None = None  # 매매구분명
    PDNO: str | None = None  # 상품번호
    ITEM_NAME: str | None = None  # 종목명
    FT_ORD_QTY: str | None = None  # FT주문수량
    FT_ORD_UNPR3: str | None = None  # FT주문단가
    ORD_TMD: str | None = None  # 주문시각
    SPLT_BUY_ATTR_NAME: str | None = None  # 분할매수속성명
    FT_CCLD_QTY: str | None = None  # FT체결수량
    TR_CRCY: str | None = None  # 거래통화
    FT_CCLD_UNPR3: str | None = None  # FT체결단가
    FT_CCLD_AMT3: str | None = None  # FT체결금액
    CCLD_CNT: str | None = None  # 체결건수

class InquireAlgoCcnlResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InquireAlgoCcnlResponse_OutputItem] = []  # 응답상세
    output3: list[InquireAlgoCcnlResponse_Output3Item] = []  # 응답상세3

class InquireAlgoCcnlExecutor(ApiExecutor[InquireAlgoCcnlRequest, InquireAlgoCcnlResponse]):
    """해외주식 지정가체결내역조회 [해외주식-070]."""

    # 해외주식 TWAP, VWAP 주문에 대한 체결내역 조회 API로 지정가 주문번호조회 API를 수행 후 조회해야합니다

    PATH = "/uapi/overseas-stock/v1/trading/inquire-algo-ccnl"
    METHOD = "GET"
    RESPONSE_TYPE = InquireAlgoCcnlResponse
    TR_ID = "TTTS6059R"
