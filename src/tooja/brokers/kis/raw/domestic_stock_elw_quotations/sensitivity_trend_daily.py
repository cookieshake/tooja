"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class SensitivityTrendDailyRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — 시장구분코드 (W)
    FID_INPUT_ISCD: str  # 입력종목코드 — ex)(58J438(KBJ438삼성전자풋)

class SensitivityTrendDailyResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식영업일자
    elw_prpr: str | None = None  # ELW현재가
    prdy_vrss: str | None = None  # 전일대비
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_ctrt: str | None = None  # 전일대비율
    hts_thpr: str | None = None  # HTS이론가
    delta_val: str | None = None  # 델타값
    gama: str | None = None  # 감마
    theta: str | None = None  # 세타
    vega: str | None = None  # 베가
    rho: str | None = None  # 로우

class SensitivityTrendDailyResponse(KisCommonResponse):
    """응답 본문."""

    output: list[SensitivityTrendDailyResponse_OutputItem] = []  # 응답상세 — array

class SensitivityTrendDailyExecutor(ApiExecutor[SensitivityTrendDailyRequest, SensitivityTrendDailyResponse]):
    """ELW 민감도 추이(일별) [국내주식-176]."""

    # ELW 민감도 추이(일별) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0283] ELW 민감도 추이 화면의 "일자별" 민감도추이 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/elw/v1/quotations/sensitivity-trend-daily"
    METHOD = "GET"
    RESPONSE_TYPE = SensitivityTrendDailyResponse
    TR_ID = "FHPEW02830200"
