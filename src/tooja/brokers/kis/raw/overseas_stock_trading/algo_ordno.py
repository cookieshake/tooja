"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class AlgoOrdnoRequest(KisBaseModel):
    """요청."""

    TRAD_DT: str  # 거래일자 — YYYYMMDD
    CANO: str  # 계좌번호 — 종합계좌번호 (8자리)
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌상품코드 (2자리) : 주식계좌는 01
    CTX_AREA_NK200: str | None = None  # 연속조회키200
    CTX_AREA_FK200: str | None = None  # 연속조회조건200

class AlgoOrdnoResponse_OutputItem(KisBaseModel):
    """nested item."""

    odno: str | None = None  # 주문번호
    trad_dvsn_name: str | None = None  # 매매구분명
    pdno: str | None = None  # 상품번호
    item_name: str | None = None  # 종목명
    ft_ord_qty: str | None = None  # FT주문수량
    ft_ord_unpr3: str | None = None  # FT주문단가
    splt_buy_attr_name: str | None = None  # 분할매수속성명
    ft_ccld_qty: str | None = None  # FT체결수량
    ord_gno_brno: str | None = None  # 주문채번지점번호

class AlgoOrdnoResponse(KisCommonResponse):
    """응답 본문."""

    output: list[AlgoOrdnoResponse_OutputItem] = []  # 응답상세
    ctx_area_fk200: str | None = None  # 연속조회검색조건200
    ctx_area_nk200: str | None = None  # 연속조회키200

class AlgoOrdnoExecutor(ApiExecutor[AlgoOrdnoRequest, AlgoOrdnoResponse]):
    """해외주식 지정가주문번호조회  [해외주식-071]."""

    # TWAP, VWAP 주문에 대한 주문번호를 조회하는 API

    PATH = "/uapi/overseas-stock/v1/trading/algo-ordno"
    METHOD = "GET"
    RESPONSE_TYPE = AlgoOrdnoResponse
    TR_ID = "TTTS6058R"
