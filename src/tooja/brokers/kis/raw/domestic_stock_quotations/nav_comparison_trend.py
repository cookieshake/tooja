"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class NavComparisonTrendRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — J
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목코드

class NavComparisonTrendResponse_Output1Item(KisBaseModel):
    """nested item."""

    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    stck_prdy_clpr: str | None = None  # 주식 전일 종가
    stck_oprc: str | None = None  # 주식 시가2
    stck_hgpr: str | None = None  # 주식 최고가
    stck_lwpr: str | None = None  # 주식 최저가
    stck_mxpr: str | None = None  # 주식 상한가
    stck_llam: str | None = None  # 주식 하한가

class NavComparisonTrendResponse_Output2Item(KisBaseModel):
    """nested item."""

    nav: str | None = None  # NAV
    nav_prdy_vrss_sign: str | None = None  # NAV 전일 대비 부호
    nav_prdy_vrss: str | None = None  # NAV 전일 대비
    nav_prdy_ctrt: str | None = None  # NAV 전일 대비율
    prdy_clpr_nav: str | None = None  # NAV전일종가
    oprc_nav: str | None = None  # NAV시가
    hprc_nav: str | None = None  # NAV고가
    lprc_nav: str | None = None  # NAV저가

class NavComparisonTrendResponse(KisCommonResponse):
    """응답 본문."""

    output1: NavComparisonTrendResponse_Output1Item | None = None  # 응답상세
    output2: NavComparisonTrendResponse_Output2Item | None = None  # 응답상세

class NavComparisonTrendExecutor(ApiExecutor[NavComparisonTrendRequest, NavComparisonTrendResponse]):
    """NAV 비교추이(종목)[v1_국내주식-069]."""

    # NAV 비교추이(종목) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0244] ETF/ETN 비교추이(NAV/IIV) 좌측 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/etfetn/v1/quotations/nav-comparison-trend"
    METHOD = "GET"
    RESPONSE_TYPE = NavComparisonTrendResponse
    TR_ID = "FHPST02440000"
