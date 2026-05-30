"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireCcnlRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — J:KRX, NX:NXT, UN:통합
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목코드 (ex 005930 삼성전자)

class InquireCcnlResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_cntg_hour: str | None = None  # 주식 체결 시간
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    cntg_vol: str | None = None  # 체결 거래량
    tday_rltv: str | None = None  # 당일 체결강도
    prdy_ctrt: str | None = None  # 전일 대비율

class InquireCcnlResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InquireCcnlResponse_OutputItem] = []  # 응답상세 — array

class InquireCcnlExecutor(ApiExecutor[InquireCcnlRequest, InquireCcnlResponse]):
    """주식현재가 체결[v1_국내주식-009]."""

    # 주식현재가 체결 API입니다. 한국투자 HTS(eFriend Plus) &gt; [010] 현재가 화면 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 더 많은 체결데이터 확인이 필요할 경우 주식현재가 당일시간대별체결 API를 이용하세요 (FID_INPUT_HOUR_1 를 이용하여 과거시간대 체결데이터 확인 가능)

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-ccnl"
    METHOD = "GET"
    RESPONSE_TYPE = InquireCcnlResponse
    TR_ID = "FHKST01010300"
