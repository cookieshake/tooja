"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireDailyTradeVolumeRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # FID 조건 시장 분류 코드 — J: KRX, NX: NXT, UN: 통합
    FID_INPUT_ISCD: str  # FID 입력 종목코드 — 005930
    FID_INPUT_DATE_1: str  # FID 입력 날짜1 — from
    FID_INPUT_DATE_2: str  # FID 입력 날짜2 — to
    FID_PERIOD_DIV_CODE: str  # FID 기간 분류 코드 — D

class InquireDailyTradeVolumeResponse_Output1Item(KisBaseModel):
    """nested item."""

    shnu_cnqn_smtn: str | None = None  # 매수 체결량 합계
    seln_cnqn_smtn: str | None = None  # 매도 체결량 합계

class InquireDailyTradeVolumeResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 거래상태정보
    total_seln_qty: str | None = None  # 총 매도 수량
    total_shnu_qty: str | None = None  # 총 매수 수량

class InquireDailyTradeVolumeResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireDailyTradeVolumeResponse_Output1Item | None = None  # 응답상세
    output2: list[InquireDailyTradeVolumeResponse_Output2Item] = []  # 응답상세2 — array

class InquireDailyTradeVolumeExecutor(ApiExecutor[InquireDailyTradeVolumeRequest, InquireDailyTradeVolumeResponse]):
    """종목별일별매수매도체결량 [v1_국내주식-056]."""

    # 종목별일별매수매도체결량 API입니다. 실전계좌의 경우, 한 번의 호출에 최대 100건까지 확인 가능합니다. 국내주식 종목의 일별 매수체결량, 매도체결량 데이터를 확인할 수 있습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-daily-trade-volume"
    METHOD = "GET"
    RESPONSE_TYPE = InquireDailyTradeVolumeResponse
    TR_ID = "FHKST03010800"
