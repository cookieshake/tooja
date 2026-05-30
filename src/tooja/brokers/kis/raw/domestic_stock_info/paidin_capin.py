"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class PaidinCapinRequest(KisBaseModel):
    """요청."""

    CTS: str  # CTS — 공백
    GB1: str  # 조회구분 — 1(청약일별), 2(기준일별)
    F_DT: str  # 조회일자From — 일자 ~
    T_DT: str  # 조회일자To — ~ 일자
    SHT_CD: str  # 종목코드 — 공백(전체), 특정종목 조회시(종목코드)

class PaidinCapinResponse_OutputItem(KisBaseModel):
    """nested item."""

    record_date: str | None = None  # 기준일
    sht_cd: str | None = None  # 종목코드
    isin_name: str | None = None  # 종목명
    tot_issue_stk_qty: str | None = None  # 발행주식
    issue_stk_qty: str | None = None  # 발행할주식
    fix_rate: str | None = None  # 확정배정율
    disc_rate: str | None = None  # 할인율
    fix_price: str | None = None  # 발행예정가
    right_dt: str | None = None  # 권리락일
    sub_term_ft: str | None = None  # 청약기간
    sub_term: str | None = None  # 청약기간
    list_date: str | None = None  # 상장/등록일
    stk_kind: str | None = None  # 주식종류

class PaidinCapinResponse(KisCommonResponse):
    """응답 본문."""

    output: list[PaidinCapinResponse_OutputItem] = []  # 응답상세 — array

class PaidinCapinExecutor(ApiExecutor[PaidinCapinRequest, PaidinCapinResponse]):
    """예탁원정보(유상증자일정) [국내주식-143]."""

    # 예탁원정보(유상증자일정) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0655] 유상증자 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.

    PATH = "/uapi/domestic-stock/v1/ksdinfo/paidin-capin"
    METHOD = "GET"
    RESPONSE_TYPE = PaidinCapinResponse
    TR_ID = "HHKDB669100C0"
