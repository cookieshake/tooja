"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class CapDcrsRequest(KisBaseModel):
    """요청."""

    CTS: str  # CTS — 공백
    F_DT: str  # 조회일자From — 일자 ~
    T_DT: str  # 조회일자To — ~ 일자
    SHT_CD: str  # 종목코드 — 공백: 전체, 특정종목 조회시 : 종목코드

class CapDcrsResponse_Output1Item(KisBaseModel):
    """nested item."""

    record_date: str | None = None  # 기준일
    sht_cd: str | None = None  # 종목코드
    isin_name: str | None = None  # 종목명
    stk_kind: str | None = None  # 주식종류
    reduce_cap_type: str | None = None  # 감자구분
    reduce_cap_rate: str | None = None  # 감자배정율
    comp_way: str | None = None  # 계산방법
    td_stop_dt: str | None = None  # 매매거래정지기간
    list_dt: str | None = None  # 상장/등록일

class CapDcrsResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[CapDcrsResponse_Output1Item] = []  # 응답상세 — array

class CapDcrsExecutor(ApiExecutor[CapDcrsRequest, CapDcrsResponse]):
    """예탁원정보(자본감소일정)[국내주식-149]."""

    # 예탁원정보(자본감소일정) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0665] 자본감소 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.

    PATH = "/uapi/domestic-stock/v1/ksdinfo/cap-dcrs"
    METHOD = "GET"
    RESPONSE_TYPE = CapDcrsResponse
    TR_ID = "HHKDB669106C0"
