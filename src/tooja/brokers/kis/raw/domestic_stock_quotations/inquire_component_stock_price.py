"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireComponentStockPriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — 시장구분코드 (J)
    FID_INPUT_ISCD: str  # 입력종목코드 — 종목코드
    FID_COND_SCR_DIV_CODE: str  # 조건화면분류코드 — Unique key( 11216 )

class InquireComponentStockPriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    etf_cnfg_issu_avls: str | None = None  # ETF구성종목시가총액
    nav: str | None = None  # NAV
    nav_prdy_vrss_sign: str | None = None  # NAV 전일 대비 부호
    nav_prdy_vrss: str | None = None  # NAV 전일 대비
    nav_prdy_ctrt: str | None = None  # NAV 전일 대비율
    etf_ntas_ttam: str | None = None  # ETF 순자산 총액
    prdy_clpr_nav: str | None = None  # NAV전일종가
    oprc_nav: str | None = None  # NAV시가
    hprc_nav: str | None = None  # NAV고가
    lprc_nav: str | None = None  # NAV저가
    etf_cu_unit_scrt_cnt: str | None = None  # ETF CU 단위 증권 수
    etf_cnfg_issu_cnt: str | None = None  # ETF 구성 종목 수

class InquireComponentStockPriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_shrn_iscd: str | None = None  # 주식 단축 종목코드
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    tday_rsfl_rate: str | None = None  # 당일 등락 비율
    prdy_vrss_vol: str | None = None  # 전일 대비 거래량
    tr_pbmn_tnrt: str | None = None  # 거래대금회전율
    hts_avls: str | None = None  # HTS 시가총액
    etf_cnfg_issu_avls: str | None = None  # ETF구성종목시가총액
    etf_cnfg_issu_rlim: str | None = None  # ETF구성종목비중
    etf_vltn_amt: str | None = None  # ETF구성종목내평가금액

class InquireComponentStockPriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireComponentStockPriceResponse_Output1Item | None = None  # 응답상세
    output2: list[InquireComponentStockPriceResponse_Output2Item] = []  # 응답상세 — array

class InquireComponentStockPriceExecutor(ApiExecutor[InquireComponentStockPriceRequest, InquireComponentStockPriceResponse]):
    """ETF 구성종목시세[국내주식-073]."""

    # ETF 구성종목시세 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0245] ETF/ETN 구성종목시세 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/etfetn/v1/quotations/inquire-component-stock-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquireComponentStockPriceResponse
    TR_ID = "FHKST121600C0"
