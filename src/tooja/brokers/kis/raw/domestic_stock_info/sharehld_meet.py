"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class SharehldMeetRequest(KisBaseModel):
    """요청."""

    CTS: str  # CTS — 공백
    F_DT: str  # 조회일자From — 일자 ~
    T_DT: str  # 조회일자To — ~ 일자
    SHT_CD: str  # 종목코드 — 공백: 전체, 특정종목 조회시 : 종목코드

class SharehldMeetResponse_Output1Item(KisBaseModel):
    """nested item."""

    record_date: str | None = None  # 기준일
    sht_cd: str | None = None  # 종목코드
    isin_name: str | None = None  # 종목명
    gen_meet_dt: str | None = None  # 주총일자
    gen_meet_type: str | None = None  # 주총사유
    agenda: str | None = None  # 주총의안
    vote_tot_qty: str | None = None  # 의결권주식총수

class SharehldMeetResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[SharehldMeetResponse_Output1Item] = []  # 응답상세 — array

class SharehldMeetExecutor(ApiExecutor[SharehldMeetRequest, SharehldMeetResponse]):
    """예탁원정보(주주총회일정) [국내주식-154]."""

    # 예탁원정보(주주총회일정) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0759] 주주총회 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.

    PATH = "/uapi/domestic-stock/v1/ksdinfo/sharehld-meet"
    METHOD = "GET"
    RESPONSE_TYPE = SharehldMeetResponse
    TR_ID = "HHKDB669111C0"
