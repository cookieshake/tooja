"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireCcnlBstimeRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    ORD_DT: str  # 주문일자 — 주문일자(YYYYMMDD)
    FUOP_TR_STRT_TMD: str  # 선물옵션거래시작시각 — 선물옵션거래시작시간(HHMMSS)
    FUOP_TR_END_TMD: str  # 선물옵션거래종료시각 — 선물옵션거래종료시간(HHMMSS)
    CTX_AREA_FK200: str  # 연속조회검색조건200
    CTX_AREA_NK200: str  # 연속조회키200

class InquireCcnlBstimeResponse_Output1Item(KisBaseModel):
    """nested item."""

    pdno: str | None = None  # 상품번호
    prdt_name: str | None = None  # 상품명
    odno: str | None = None  # 주문번호
    tr_type_name: str | None = None  # 거래유형명
    last_sttldt: str | None = None  # 최종결제일
    ccld_idx: str | None = None  # 체결지수
    ccld_qty: str | None = None  # 체결량
    trad_amt: str | None = None  # 매매금액
    fee: str | None = None  # 수수료
    ccld_btwn: str | None = None  # 체결시간

class InquireCcnlBstimeResponse_Output2Item(KisBaseModel):
    """nested item."""

    tot_ccld_qty_smtl: str | None = None  # 총체결수량합계
    tot_ccld_amt_smtl: str | None = None  # 총체결금액합계
    fee_adjt: str | None = None  # 수수료조정
    fee_smtl: str | None = None  # 수수료합계

class InquireCcnlBstimeResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[str] = []  # 응답상세 — array
    output2: InquireCcnlBstimeResponse_Output2Item | None = None  # 응답상세2

class InquireCcnlBstimeExecutor(ApiExecutor[InquireCcnlBstimeRequest, InquireCcnlBstimeResponse]):
    """선물옵션 기준일체결내역[v1_국내선물-016]."""

    # 선물옵션 기준일체결내역 API입니다.

    PATH = "/uapi/domestic-futureoption/v1/trading/inquire-ccnl-bstime"
    METHOD = "GET"
    RESPONSE_TYPE = InquireCcnlBstimeResponse
    TR_ID = "CTFO5139R"
