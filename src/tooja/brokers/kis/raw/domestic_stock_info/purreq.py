"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class PurreqRequest(KisBaseModel):
    """요청."""

    SHT_CD: str  # 종목코드 — 공백: 전체, 특정종목 조회시 : 종목코드
    T_DT: str  # 조회일자To — ~ 일자
    F_DT: str  # 조회일자From — 일자 ~
    CTS: str  # CTS — 공백

class PurreqResponse_Output1Item(KisBaseModel):
    """nested item."""

    record_date: str | None = None  # 기준일
    sht_cd: str | None = None  # 종목코드
    isin_name: str | None = None  # 종목명
    stk_kind: str | None = None  # 주식종류
    opp_opi_rcpt_term: str | None = None  # 반대의사접수시한
    buy_req_rcpt_term: str | None = None  # 매수청구접수시한
    buy_req_price: str | None = None  # 매수청구가격
    buy_amt_pay_dt: str | None = None  # 매수대금지급일
    get_meet_dt: str | None = None  # 주총일

class PurreqResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[PurreqResponse_Output1Item] = []  # 응답상세 — array

class PurreqExecutor(ApiExecutor[PurreqRequest, PurreqResponse]):
    """예탁원정보(주식매수청구일정)[국내주식-146]."""

    # 예탁원정보(주식매수청구일정) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0663] 주식매수청구 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.

    PATH = "/uapi/domestic-stock/v1/ksdinfo/purreq"
    METHOD = "GET"
    RESPONSE_TYPE = PurreqResponse
    TR_ID = "HHKDB669103C0"
