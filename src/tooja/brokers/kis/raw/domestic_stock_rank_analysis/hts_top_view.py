"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class HtsTopViewRequest(KisBaseModel):
    """요청."""

    pass

class HtsTopViewResponse_Output1Item(KisBaseModel):
    """nested item."""

    mrkt_div_cls_code: str | None = None  # 시장구분 — J : 코스피, Q : 코스닥
    mksc_shrn_iscd: str | None = None  # 종목코드

class HtsTopViewResponse(KisCommonResponse):
    """응답 본문."""

    output1: HtsTopViewResponse_Output1Item | None = None  # 응답상세

class HtsTopViewExecutor(ApiExecutor[HtsTopViewRequest, HtsTopViewResponse]):
    """HTS조회상위20종목 [국내주식-214]."""

    # HTS조회상위20종목 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0158] 조회종목상위 화면의 "종목명", "종목코드" 표시 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/ranking/hts-top-view"
    METHOD = "GET"
    RESPONSE_TYPE = HtsTopViewResponse
    TR_ID = "HHMCM000100C0"
