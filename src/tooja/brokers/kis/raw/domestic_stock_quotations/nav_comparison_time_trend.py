"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class NavComparisonTimeTrendRequest(KisBaseModel):
    """요청."""

    fid_hour_cls_code: str  # FID 시간 구분 코드 — 1분 :60, 3분: 180 … 120분:7200
    fid_cond_mrkt_div_code: str  # FID 조건 시장 분류 코드 — E - 고정값
    fid_input_iscd: str  # FID 입력 종목코드 — 종목코드

class NavComparisonTimeTrendResponse_OutputItem(KisBaseModel):
    """nested item."""

    bsop_hour: str | None = None  # 영업 시간
    nav: str | None = None  # NAV
    nav_prdy_vrss_sign: str | None = None  # NAV 전일 대비 부호
    nav_prdy_vrss: str | None = None  # NAV 전일 대비
    nav_prdy_ctrt: str | None = None  # NAV 전일 대비율
    nav_vrss_prpr: str | None = None  # NAV 대비 현재가
    dprt: str | None = None  # 괴리율
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    cntg_vol: str | None = None  # 체결 거래량

class NavComparisonTimeTrendResponse(KisCommonResponse):
    """응답 본문."""

    output: list[NavComparisonTimeTrendResponse_OutputItem] = []  # 응답상세 — array

class NavComparisonTimeTrendExecutor(ApiExecutor[NavComparisonTimeTrendRequest, NavComparisonTimeTrendResponse]):
    """NAV 비교추이(분)[v1_국내주식-070]."""

    # NAV 비교추이(분) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0244] ETF/ETN 비교추이(NAV/IIV) 좌측 화면 "분별" 비교추이 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 실전계좌의 경우, 한 번의 호출에 최근 30건까지 확인 가능합니다.

    PATH = "/uapi/etfetn/v1/quotations/nav-comparison-time-trend"
    METHOD = "GET"
    RESPONSE_TYPE = NavComparisonTimeTrendResponse
    TR_ID = "FHPST02440100"
