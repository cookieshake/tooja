"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class VolatilityTrendCcnlRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — W(Unique key)
    FID_INPUT_ISCD: str  # 입력종목코드 — ex) 58J297(KBJ297삼성전자콜)

class VolatilityTrendCcnlResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_cntg_hour: str | None = None  # 주식체결시간
    elw_prpr: str | None = None  # ELW현재가
    prdy_vrss: str | None = None  # 전일대비
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_ctrt: str | None = None  # 전일대비율
    bidp: str | None = None  # 매수호가
    askp: str | None = None  # 매도호가
    acml_vol: str | None = None  # 누적거래량
    hts_ints_vltl: str | None = None  # HTS내재변동성

class VolatilityTrendCcnlResponse(KisCommonResponse):
    """응답 본문."""

    output: list[VolatilityTrendCcnlResponse_OutputItem] = []  # 응답상세

class VolatilityTrendCcnlExecutor(ApiExecutor[VolatilityTrendCcnlRequest, VolatilityTrendCcnlResponse]):
    """ELW 변동성추이(체결) [국내주식-177]."""

    # ELW 변동성 추이(체결) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0284] ELW 변동성 추이 화면의 "시간별" 변동성 추이 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/elw/v1/quotations/volatility-trend-ccnl"
    METHOD = "GET"
    RESPONSE_TYPE = VolatilityTrendCcnlResponse
    TR_ID = "FHPEW02840100"
