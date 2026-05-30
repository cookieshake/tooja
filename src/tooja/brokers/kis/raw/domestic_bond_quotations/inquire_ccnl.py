"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireCcnlRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — B (업종코드)
    FID_INPUT_ISCD: str  # 입력종목코드 — 채권종목코드(ex KR2033022D33)

class InquireCcnlResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_cntg_hour: str | None = None  # 주식 체결 시간
    bond_prpr: str | None = None  # 채권 현재가
    bond_prdy_vrss: str | None = None  # 채권 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    cntg_vol: str | None = None  # 체결 거래량
    acml_vol: str | None = None  # 누적 거래량

class InquireCcnlResponse(KisCommonResponse):
    """응답 본문."""

    output: InquireCcnlResponse_OutputItem | None = None  # 응답상세

class InquireCcnlExecutor(ApiExecutor[InquireCcnlRequest, InquireCcnlResponse]):
    """장내채권현재가(체결) [국내주식-201]."""

    # 장내채권현재가(체결) API입니다 장내채권의 체결데이터를 확인할 수 있습니다.

    PATH = "/uapi/domestic-bond/v1/quotations/inquire-ccnl"
    METHOD = "GET"
    RESPONSE_TYPE = InquireCcnlResponse
    TR_ID = "FHKBJ773403C0"
