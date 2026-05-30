"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class PubOfferRequest(KisBaseModel):
    """요청."""

    SHT_CD: str  # 종목코드 — 공백: 전체, 특정종목 조회시 : 종목코드
    CTS: str  # CTS — 공백
    F_DT: str  # 조회일자From — 일자 ~
    T_DT: str  # 조회일자To — ~ 일자

class PubOfferResponse_Output1Item(KisBaseModel):
    """nested item."""

    record_date: str | None = None  # 기준일
    sht_cd: str | None = None  # 종목코드
    isin_name: str | None = None  # 종목명
    fix_subscr_pri: str | None = None  # 공모가
    face_value: str | None = None  # 액면가
    subscr_dt: str | None = None  # 청약기간
    pay_dt: str | None = None  # 납입일
    refund_dt: str | None = None  # 환불일
    list_dt: str | None = None  # 상장/등록일
    lead_mgr: str | None = None  # 주간사
    pub_bf_cap: str | None = None  # 공모전자본금
    pub_af_cap: str | None = None  # 공모후자본금
    assign_stk_qty: str | None = None  # 당사배정물량

class PubOfferResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[PubOfferResponse_Output1Item] = []  # 응답상세 — array

class PubOfferExecutor(ApiExecutor[PubOfferRequest, PubOfferResponse]):
    """예탁원정보(공모주청약일정)[국내주식-151]."""

    # 예탁원정보(공모주청약일정) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0667] 공모주청약 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.

    PATH = "/uapi/domestic-stock/v1/ksdinfo/pub-offer"
    METHOD = "GET"
    RESPONSE_TYPE = PubOfferResponse
    TR_ID = "HHKDB669108C0"
