"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class VolatilityTrendTickRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — W(Unique key)
    FID_INPUT_ISCD: str  # 입력종목코드 — ex) 58J297(KBJ297삼성전자콜)

class VolatilityTrendTickResponse_OutputItem(KisBaseModel):
    """nested item."""

    bsop_date: str | None = None  # 주식영업일자
    stck_cntg_hour: str | None = None  # ELW현재가
    elw_prpr: str | None = None  # 전일대비
    hts_ints_vltl: str | None = None  # 전일대비부호

class VolatilityTrendTickResponse(KisCommonResponse):
    """응답 본문."""

    output: list[VolatilityTrendTickResponse_OutputItem] = []  # 응답상세 — array

class VolatilityTrendTickExecutor(ApiExecutor[VolatilityTrendTickRequest, VolatilityTrendTickResponse]):
    """ELW 변동성 추이(틱) [국내주식-180]."""

    # ELW 변동성 추이(틱) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0284] ELW 변동성 추이 화면의 "틱 차트" 변동성 추이 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/elw/v1/quotations/volatility-trend-tick"
    METHOD = "GET"
    RESPONSE_TYPE = VolatilityTrendTickResponse
    TR_ID = "FHPEW02840400"
