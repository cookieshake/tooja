"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class IndicatorTrendDailyRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 시장분류코드 — W
    FID_INPUT_ISCD: str  # 종콕코드 — ex. 57K281

class IndicatorTrendDailyResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식영업일자
    elw_prpr: str | None = None  # ELW현재가
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_vrss: str | None = None  # 전일대비
    prdy_ctrt: str | None = None  # 전일대비율
    acml_vol: str | None = None  # 누적거래량
    lvrg_val: str | None = None  # 레버리지값
    gear: str | None = None  # 기어링
    tmvl_val: str | None = None  # 시간가치값
    invl_val: str | None = None  # 내재가치값
    prit: str | None = None  # 패리티
    elw_oprc: str | None = None  # ELW시가2
    elw_hgpr: str | None = None  # ELW최고가
    elw_lwpr: str | None = None  # ELW최저가
    apprch_rate: str | None = None  # 접근도

class IndicatorTrendDailyResponse(KisCommonResponse):
    """응답 본문."""

    output: list[IndicatorTrendDailyResponse_OutputItem] = []  # 응답상세 — array

class IndicatorTrendDailyExecutor(ApiExecutor[IndicatorTrendDailyRequest, IndicatorTrendDailyResponse]):
    """ELW 투자지표추이(일별) [국내주식-173]."""

    # ELW 투자지표추이(일별) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0274] ELW 투자지표추이 화면에서 "일자별 비교추이" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/elw/v1/quotations/indicator-trend-daily"
    METHOD = "GET"
    RESPONSE_TYPE = IndicatorTrendDailyResponse
    TR_ID = "FHPEW02740200"
