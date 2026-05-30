"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OptAskingPriceRequest(KisBaseModel):
    """요청."""

    SRS_CD: str  # 종목명 — 예)OESM24 C5340

class OptAskingPriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    open_price: str | None = None  # 시가
    high_price: str | None = None  # 고가
    lowp_rice: str | None = None  # 저가
    last_price: str | None = None  # 현재가
    sttl_price: str | None = None  # 정산가
    vol: str | None = None  # 거래량
    prev_diff_price: str | None = None  # 전일대비가
    prev_diff_rate: str | None = None  # 전일대비율
    quot_date: str | None = None  # 호가수신일자
    quot_time: str | None = None  # 호가수신시각

class OptAskingPriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    bid_qntt: str | None = None  # 매수수량
    bid_num: str | None = None  # 매수번호
    bid_price: str | None = None  # 매수호가
    ask_qntt: str | None = None  # 매도수량
    ask_num: str | None = None  # 매도번호
    ask_price: str | None = None  # 매도호가

class OptAskingPriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: OptAskingPriceResponse_Output1Item | None = None  # 응답상세
    output2: list[OptAskingPriceResponse_Output2Item] = []  # 응답상세 — array (1호가~ 5호가 순서대로 표시)

class OptAskingPriceExecutor(ApiExecutor[OptAskingPriceRequest, OptAskingPriceResponse]):
    """해외옵션 호가 [해외선물-033]."""

    # 해외옵션 호가 API입니다. 한국투자 HTS(eFriend Plus) &gt; [5501] 해외선물옵션 현재가 화면 의 "왼쪽 상단 현재가" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/overseas-futureoption/v1/quotations/opt-asking-price"
    METHOD = "GET"
    RESPONSE_TYPE = OptAskingPriceResponse
    TR_ID = "HHDFO86000000"
