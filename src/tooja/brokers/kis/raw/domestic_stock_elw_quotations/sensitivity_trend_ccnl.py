"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class SensitivityTrendCcnlRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — 시장구분코드 (W)
    FID_INPUT_ISCD: str  # 입력종목코드 — ex) 58J297(KBJ297삼성전자콜)

class SensitivityTrendCcnlResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_cntg_hour: str | None = None  # 주식체결시간
    elw_prpr: str | None = None  # ELW현재가
    prdy_vrss: str | None = None  # 전일대비
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_ctrt: str | None = None  # 전일대비율
    hts_thpr: str | None = None  # hts 이론가
    delta_val: str | None = None  # 델타 값
    gama: str | None = None  # 감마
    theta: str | None = None  # 세타
    vega: str | None = None  # 베가
    rho: str | None = None  # 로우

class SensitivityTrendCcnlResponse(KisCommonResponse):
    """응답 본문."""

    output: list[SensitivityTrendCcnlResponse_OutputItem] = []  # 응답상세 — array

class SensitivityTrendCcnlExecutor(ApiExecutor[SensitivityTrendCcnlRequest, SensitivityTrendCcnlResponse]):
    """ELW 민감도 추이(체결) [국내주식-175]."""

    # ELW 민감도 추이(체결) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0283] ELW 민감도 추이 화면 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/elw/v1/quotations/sensitivity-trend-ccnl"
    METHOD = "GET"
    RESPONSE_TYPE = SensitivityTrendCcnlResponse
    TR_ID = "FHPEW02830100"
