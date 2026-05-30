"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class IndicatorTrendCcnlRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — 시장구분코드 (W)
    FID_INPUT_ISCD: str  # 입력종목코드 — ex) 58J297(KBJ297삼성전자콜)

class IndicatorTrendCcnlResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_cntg_hour: str | None = None  # 주식체결시간
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
    apprch_rate: str | None = None  # 접근도

class IndicatorTrendCcnlResponse(KisCommonResponse):
    """응답 본문."""

    output: list[IndicatorTrendCcnlResponse_OutputItem] = []  # 응답상세 — array

class IndicatorTrendCcnlExecutor(ApiExecutor[IndicatorTrendCcnlRequest, IndicatorTrendCcnlResponse]):
    """ELW 투자지표추이(체결) [국내주식-172]."""

    # ELW 투자지표추이(체결) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0274] ELW 투자지표추이 화면에서 "시간별 비교추이" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/elw/v1/quotations/indicator-trend-ccnl"
    METHOD = "GET"
    RESPONSE_TYPE = IndicatorTrendCcnlResponse
    TR_ID = "FHPEW02740100"
