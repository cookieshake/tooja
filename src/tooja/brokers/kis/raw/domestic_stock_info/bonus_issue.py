"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class BonusIssueRequest(KisBaseModel):
    """요청."""

    CTS: str  # CTS — 공백
    F_DT: str  # 조회일자From — 일자 ~
    T_DT: str  # 조회일자To — ~ 일자
    SHT_CD: str  # 종목코드 — 공백: 전체, 특정종목 조회시 : 종목코드

class BonusIssueResponse_Output1Item(KisBaseModel):
    """nested item."""

    record_date: str | None = None  # 기준일
    sht_cd: str | None = None  # 종목코드
    isin_name: str | None = None  # 종목명
    fix_rate: str | None = None  # 확정배정율
    odd_rec_price: str | None = None  # 단주기준가
    right_dt: str | None = None  # 권리락일
    odd_pay_dt: str | None = None  # 단주대금지급일
    list_date: str | None = None  # 상장/등록일
    tot_issue_stk_qty: str | None = None  # 발행주식
    issue_stk_qty: str | None = None  # 발행할주식
    stk_kind: str | None = None  # 주식종류

class BonusIssueResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[BonusIssueResponse_Output1Item] = []  # 응답상세 — array

class BonusIssueExecutor(ApiExecutor[BonusIssueRequest, BonusIssueResponse]):
    """예탁원정보(무상증자일정) [국내주식-144]."""

    # 예탁원정보(무상증자일정) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0656] 무상증자 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.

    PATH = "/uapi/domestic-stock/v1/ksdinfo/bonus-issue"
    METHOD = "GET"
    RESPONSE_TYPE = BonusIssueResponse
    TR_ID = "HHKDB669101C0"
