"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireTimeItemconclusionRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — J:KRX, NX:NXT, UN:통합
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목코드 (ex 005930 삼성전자)
    FID_INPUT_HOUR_1: str  # 입력 시간1 — 입력시간

class InquireTimeItemconclusionResponse_Output1Item(KisBaseModel):
    """nested item."""

    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    prdy_vol: str | None = None  # 전일 거래량
    rprs_mrkt_kor_name: str | None = None  # 대표 시장 한글 명

class InquireTimeItemconclusionResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_cntg_hour: str | None = None  # 주식 체결 시간
    stck_pbpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    askp: str | None = None  # 매도호가
    bidp: str | None = None  # 매수호가
    tday_rltv: str | None = None  # 당일 체결강도
    acml_vol: str | None = None  # 누적 거래량
    cnqn: str | None = None  # 체결량

class InquireTimeItemconclusionResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireTimeItemconclusionResponse_Output1Item | None = None  # 응답상세 — single
    output2: InquireTimeItemconclusionResponse_Output2Item | None = None  # 응답상세 — single

class InquireTimeItemconclusionExecutor(ApiExecutor[InquireTimeItemconclusionRequest, InquireTimeItemconclusionResponse]):
    """주식현재가 당일시간대별체결[v1_국내주식-023]."""

    # 주식현재가 당일시간대별체결 API입니다. * FID_INPUT_HOUR_1 를 이용하여 과거시간대 체결데이터 확인 가능

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-time-itemconclusion"
    METHOD = "GET"
    RESPONSE_TYPE = InquireTimeItemconclusionResponse
    TR_ID = "FHPST01060000"
