"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireIndexTimepriceRequest(KisBaseModel):
    """요청."""

    FID_INPUT_HOUR_1: str  # ?입력 시간1 — 초단위, 60(1분), 300(5분), 600(10분)
    FID_INPUT_ISCD: str  # 입력 종목코드 — 0001:거래소, 1001:코스닥, 2001:코스피200, 3003:KSQ150
    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — 시장구분코드 (업종 U)

class InquireIndexTimepriceResponse_OutputItem(KisBaseModel):
    """nested item."""

    bsop_hour: str | None = None  # 영업 시간
    bstp_nmix_prpr: str | None = None  # 업종 지수 현재가
    bstp_nmix_prdy_vrss: str | None = None  # 업종 지수 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    bstp_nmix_prdy_ctrt: str | None = None  # 업종 지수 전일 대비율
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    acml_vol: str | None = None  # 누적 거래량
    cntg_vol: str | None = None  # 체결 거래량

class InquireIndexTimepriceResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InquireIndexTimepriceResponse_OutputItem] = []  # 응답상세 — array

class InquireIndexTimepriceExecutor(ApiExecutor[InquireIndexTimepriceRequest, InquireIndexTimepriceResponse]):
    """국내업종 시간별지수(분)[국내주식-119]."""

    # 국내업종 시간별지수(분) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0211] 업종 시간별지수 화면에서 우측 '1분' 선택 시의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-index-timeprice"
    METHOD = "GET"
    RESPONSE_TYPE = InquireIndexTimepriceResponse
    TR_ID = "FHPUP02110200"
