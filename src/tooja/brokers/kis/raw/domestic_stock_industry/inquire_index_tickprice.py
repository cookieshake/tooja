"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireIndexTickpriceRequest(KisBaseModel):
    """요청."""

    FID_INPUT_ISCD: str  # 입력 종목코드 — 0001:거래소, 1001:코스닥, 2001:코스피200, 3003:KSQ150
    FID_COND_MRKT_DIV_CODE: str  # 시장 분류 코드 — 시장구분코드 (업종 U)

class InquireIndexTickpriceResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_cntg_hour: str | None = None  # 주식 체결 시간
    bstp_nmix_prpr: str | None = None  # 업종 지수 현재가
    bstp_nmix_prdy_vrss: str | None = None  # 업종 지수 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    bstp_nmix_prdy_ctrt: str | None = None  # 업종 지수 전일 대비율
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    acml_vol: str | None = None  # 누적 거래량
    cntg_vol: str | None = None  # 체결 거래량

class InquireIndexTickpriceResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InquireIndexTickpriceResponse_OutputItem] = []  # 응답상세 — array

class InquireIndexTickpriceExecutor(ApiExecutor[InquireIndexTickpriceRequest, InquireIndexTickpriceResponse]):
    """국내업종 시간별지수(초)[국내주식-064]."""

    # 국내업종 시간별지수(초) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0211] 업종 시간별지수 화면에서 우측 '10초' 선택 시의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-index-tickprice"
    METHOD = "GET"
    RESPONSE_TYPE = InquireIndexTickpriceResponse
    TR_ID = "FHPUP02110100"
