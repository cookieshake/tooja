"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class VolatilityTrendDailyRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — 시장구분코드 (W)
    FID_INPUT_ISCD: str  # 입력종목코드 — ex) 58J297(KBJ297삼성전자콜)

class VolatilityTrendDailyResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자
    elw_prpr: str | None = None  # ELW 현재가
    prdy_vrss: str | None = None  # 전일대비
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_ctrt: str | None = None  # 전일대비율
    elw_oprc: str | None = None  # elw 시가2
    elw_hgpr: str | None = None  # elw 최고가
    elw_lwpr: str | None = None  # elw 최저가
    acml_vol: str | None = None  # 누적 거래량
    d10_hist_vltl: str | None = None  # 10일 역사적 변동성
    d20_hist_vltl: str | None = None  # 20일 역사적 변동성
    d30_hist_vltl: str | None = None  # 30일 역사적 변동성
    d60_hist_vltl: str | None = None  # 60일 역사적 변동성
    d90_hist_vltl: str | None = None  # 90일 역사적 변동성
    hts_ints_vltl: str | None = None  # HTS 내재 변동성

class VolatilityTrendDailyResponse(KisCommonResponse):
    """응답 본문."""

    output: list[VolatilityTrendDailyResponse_OutputItem] = []  # 응답상세 — array

class VolatilityTrendDailyExecutor(ApiExecutor[VolatilityTrendDailyRequest, VolatilityTrendDailyResponse]):
    """ELW 변동성 추이(일별) [국내주식-178]."""

    # ELW 변동성 추이(일별) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0284] ELW 변동성 추이 화면의 "일별" 변동성 추이 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/elw/v1/quotations/volatility-trend-daily"
    METHOD = "GET"
    RESPONSE_TYPE = VolatilityTrendDailyResponse
    TR_ID = "FHPEW02840200"
