"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class ForfeitRequest(KisBaseModel):
    """요청."""

    SHT_CD: str  # 종목코드 — 공백: 전체, 특정종목 조회시 : 종목코드
    T_DT: str  # 조회일자To — ~ 일자
    F_DT: str  # 조회일자From — 일자 ~
    CTS: str  # CTS — 공백

class ForfeitResponse_Output1Item(KisBaseModel):
    """nested item."""

    record_date: str | None = None  # 기준일
    sht_cd: str | None = None  # 종목코드
    isin_name: str | None = None  # 종목명
    subscr_dt: str | None = None  # 청약일
    subscr_price: str | None = None  # 공모가
    subscr_stk_qty: str | None = None  # 공모주식수
    refund_dt: str | None = None  # 환불일
    list_dt: str | None = None  # 상장/등록일
    lead_mgr: str | None = None  # 주간사

class ForfeitResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[ForfeitResponse_Output1Item] = []  # 응답상세 — array

class ForfeitExecutor(ApiExecutor[ForfeitRequest, ForfeitResponse]):
    """예탁원정보(실권주일정)[국내주식-152]."""

    # 예탁원정보(실권주일정) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0668] 실권주 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.

    PATH = "/uapi/domestic-stock/v1/ksdinfo/forfeit"
    METHOD = "GET"
    RESPONSE_TYPE = ForfeitResponse
    TR_ID = "HHKDB669109C0"
