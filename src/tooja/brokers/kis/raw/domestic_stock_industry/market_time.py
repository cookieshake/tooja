"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class MarketTimeRequest(KisBaseModel):
    """요청."""

    pass

class MarketTimeResponse_Output1Item(KisBaseModel):
    """nested item."""

    date1: str | None = None  # 영업일1
    date2: str | None = None  # 영업일2
    date3: str | None = None  # 영업일3 — 영업일 당일
    date4: str | None = None  # 영업일4
    date5: str | None = None  # 영업일5
    today: str | None = None  # 오늘일자
    time: str | None = None  # 현재시간
    s_time: str | None = None  # 장시작시간
    e_time: str | None = None  # 장마감시간

class MarketTimeResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[MarketTimeResponse_Output1Item] = []  # 응답상세 — array

class MarketTimeExecutor(ApiExecutor[MarketTimeRequest, MarketTimeResponse]):
    """국내선물 영업일조회 [국내주식-160]."""

    # 국내선물 영업일조회 API입니다. 한국투자 HTS(eFriend Plus) &gt; [1938] 시가총액순위 화면 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. API호출 시 body 혹은 params로 입력하는 사항이 없습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/market-time"
    METHOD = "GET"
    RESPONSE_TYPE = MarketTimeResponse
    TR_ID = "HHMCM000002C0"
