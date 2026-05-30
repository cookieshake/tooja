"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class VolatilityTrendMinuteRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — W(Unique key)
    FID_INPUT_ISCD: str  # 입력종목코드 — ex) 58J297(KBJ297삼성전자콜)
    FID_HOUR_CLS_CODE: str  # 시간구분코드 — '60(1분), 180(3분), 300(5분), 600(10분), 1800(30분), 3600(60분) '
    FID_PW_DATA_INCU_YN: str  # 과거데이터 포함 여부 — N(과거데이터포함X),Y(과거데이터포함O)

class VolatilityTrendMinuteResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자
    stck_cntg_hour: str | None = None  # 주식 체결 시간
    stck_prpr: str | None = None  # 주식 현재가
    elw_oprc: str | None = None  # ELW 시가2
    elw_hgpr: str | None = None  # ELW 최고가
    elw_lwpr: str | None = None  # ELW 최저가
    hts_ints_vltl: str | None = None  # HTS 내재 변동성
    hist_vltl: str | None = None  # 역사적 변동성

class VolatilityTrendMinuteResponse(KisCommonResponse):
    """응답 본문."""

    output: list[VolatilityTrendMinuteResponse_OutputItem] = []  # 응답상세 — array

class VolatilityTrendMinuteExecutor(ApiExecutor[VolatilityTrendMinuteRequest, VolatilityTrendMinuteResponse]):
    """ELW 변동성 추이(분별) [국내주식-179]."""

    # ELW 변동성 추이(분별) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0284] ELW 변동성 추이 화면의 "분별" 변동성 추이 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/elw/v1/quotations/volatility-trend-minute"
    METHOD = "GET"
    RESPONSE_TYPE = VolatilityTrendMinuteResponse
    TR_ID = "FHPEW02840300"
