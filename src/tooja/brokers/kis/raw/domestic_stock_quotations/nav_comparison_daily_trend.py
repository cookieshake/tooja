"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class NavComparisonDailyTrendRequest(KisBaseModel):
    """요청."""

    fid_cond_mrkt_div_code: str  # FID 조건 시장 분류 코드 — J 입력
    fid_input_iscd: str  # FID 입력 종목코드 — 종목코드 (6자리)
    fid_input_date_1: str  # FID 입력 날짜1 — 조회 시작일자 (ex. 20240101)
    fid_input_date_2: str  # FID 입력 날짜2 — 조회 종료일자 (ex. 20240220)

class NavComparisonDailyTrendResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자
    stck_clpr: str | None = None  # 주식 종가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    cntg_vol: str | None = None  # 체결 거래량
    dprt: str | None = None  # 괴리율
    nav_vrss_prpr: str | None = None  # NAV 대비 현재가
    nav: str | None = None  # NAV
    nav_prdy_vrss_sign: str | None = None  # NAV 전일 대비 부호
    nav_prdy_vrss: str | None = None  # NAV 전일 대비
    nav_prdy_ctrt: str | None = None  # NAV 전일 대비율

class NavComparisonDailyTrendResponse(KisCommonResponse):
    """응답 본문."""

    output: list[NavComparisonDailyTrendResponse_OutputItem] = []  # 응답상세 — array

class NavComparisonDailyTrendExecutor(ApiExecutor[NavComparisonDailyTrendRequest, NavComparisonDailyTrendResponse]):
    """NAV 비교추이(일)[v1_국내주식-071]."""

    # NAV 비교추이(일) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0244] ETF/ETN 비교추이(NAV/IIV) 좌측 화면 "일별" 비교추이 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 실전계좌의 경우, 한 번의 호출에 최대 100건까지 확인 가능합니다.

    PATH = "/uapi/etfetn/v1/quotations/nav-comparison-daily-trend"
    METHOD = "GET"
    RESPONSE_TYPE = NavComparisonDailyTrendResponse
    TR_ID = "FHPST02440200"
