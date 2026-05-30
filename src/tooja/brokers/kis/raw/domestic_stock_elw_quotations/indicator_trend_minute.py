"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class IndicatorTrendMinuteRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — 시장구분코드 (W)
    FID_INPUT_ISCD: str  # 입력종목코드 — ex) 58J297(KBJ297삼성전자콜)
    FID_HOUR_CLS_CODE: str  # 시간구분코드 — '60(1분), 180(3분), 300(5분), 600(10분), 1800(30분), 3600(60분), 7200(60분) '
    FID_PW_DATA_INCU_YN: str  # 과거데이터 포함 여부 — N(과거데이터포함X),Y(과거데이터포함O)

class IndicatorTrendMinuteResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식영업일자
    stck_cntg_hour: str | None = None  # 주식체결시간
    elw_prpr: str | None = None  # ELW현재가
    elw_oprc: str | None = None  # ELW시가2
    elw_hgpr: str | None = None  # ELW최고가
    elw_lwpr: str | None = None  # ELW최저가
    lvrg_val: str | None = None  # 레버리지값
    gear: str | None = None  # 기어링
    prmm_val: str | None = None  # 프리미엄값
    invl_val: str | None = None  # 내재가치값
    prit: str | None = None  # 패리티
    acml_vol: str | None = None  # 누적거래량
    cntg_vol: str | None = None  # 체결거래량

class IndicatorTrendMinuteResponse(KisCommonResponse):
    """응답 본문."""

    output: list[IndicatorTrendMinuteResponse_OutputItem] = []  # 응답상세 — array

class IndicatorTrendMinuteExecutor(ApiExecutor[IndicatorTrendMinuteRequest, IndicatorTrendMinuteResponse]):
    """ELW 투자지표추이(분별) [국내주식-174]."""

    # ELW 투자지표추이(분별) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0274] ELW 투자지표추이 화면 데이터의 "분별 비교추이" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/elw/v1/quotations/indicator-trend-minute"
    METHOD = "GET"
    RESPONSE_TYPE = IndicatorTrendMinuteResponse
    TR_ID = "FHPEW02740300"
