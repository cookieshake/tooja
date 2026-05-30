"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class MergerSplitRequest(KisBaseModel):
    """요청."""

    CTS: str  # CTS — 공백
    F_DT: str  # 조회일자From — 일자 ~
    T_DT: str  # 조회일자To — ~ 일자
    SHT_CD: str  # 종목코드 — 공백: 전체, 특정종목 조회시 : 종목코드

class MergerSplitResponse_Output1Item(KisBaseModel):
    """nested item."""

    record_date: str | None = None  # 기준일
    sht_cd: str | None = None  # 종목코드
    opp_cust_cd: str | None = None  # 피합병(피분할)회사코드
    opp_cust_nm: str | None = None  # 피합병(피분할)회사명
    cust_cd: str | None = None  # 합병(분할)회사코드
    cust_nm: str | None = None  # 합병(분할)회사명
    merge_type: str | None = None  # 합병사유
    merge_rate: str | None = None  # 비율
    td_stop_dt: str | None = None  # 매매거래정지기간
    list_dt: str | None = None  # 상장/등록일
    odd_amt_pay_dt: str | None = None  # 단주대금지급일
    tot_issue_stk_qty: str | None = None  # 발행주식
    issue_stk_qty: str | None = None  # 발행할주식
    seq: str | None = None  # 연번

class MergerSplitResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[MergerSplitResponse_Output1Item] = []  # 응답상세 — array

class MergerSplitExecutor(ApiExecutor[MergerSplitRequest, MergerSplitResponse]):
    """예탁원정보(합병/분할일정)[국내주식-147]."""

    # 예탁원정보(합병/분할일정) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0664] 합병/분할 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.

    PATH = "/uapi/domestic-stock/v1/ksdinfo/merger-split"
    METHOD = "GET"
    RESPONSE_TYPE = MergerSplitResponse
    TR_ID = "HHKDB669104C0"
