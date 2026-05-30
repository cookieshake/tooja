"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class ListInfoRequest(KisBaseModel):
    """요청."""

    SHT_CD: str  # 종목코드 — 공백: 전체, 특정종목 조회시 : 종목코드
    T_DT: str  # 조회일자To — ~ 일자
    F_DT: str  # 조회일자From — 일자 ~
    CTS: str  # CTS — 공백

class ListInfoResponse_Output1Item(KisBaseModel):
    """nested item."""

    list_dt: str | None = None  # 상장/등록일
    sht_cd: str | None = None  # 종목코드
    isin_name: str | None = None  # 종목명
    stk_kind: str | None = None  # 주식종류
    issue_type: str | None = None  # 사유
    issue_stk_qty: str | None = None  # 상장주식수
    tot_issue_stk_qty: str | None = None  # 총발행주식수
    issue_price: str | None = None  # 발행가

class ListInfoResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[ListInfoResponse_Output1Item] = []  # 응답상세 — array

class ListInfoExecutor(ApiExecutor[ListInfoRequest, ListInfoResponse]):
    """예탁원정보(상장정보일정)[국내주식-150]."""

    # 예탁원정보(상장정보일정) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0666] 상장정보 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.

    PATH = "/uapi/domestic-stock/v1/ksdinfo/list-info"
    METHOD = "GET"
    RESPONSE_TYPE = ListInfoResponse
    TR_ID = "HHKDB669107C0"
