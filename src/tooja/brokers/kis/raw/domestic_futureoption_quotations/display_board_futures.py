"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class DisplayBoardFuturesRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — 시장구분코드 (F: 선물)
    FID_COND_SCR_DIV_CODE: str  # 조건 화면 분류 코드 — Unique key(20503)
    FID_COND_MRKT_CLS_CODE: str  # 조건 시장 구분 코드 — 공백: KOSPI200 MKI: 미니KOSPI200 WKM: KOSPI200위클리(월) WKI: KOSPI200위클리(목) KQI: KOSDAQ150

class DisplayBoardFuturesResponse_Output1Item(KisBaseModel):
    """nested item."""

    futs_shrn_iscd: str | None = None  # 선물 단축 종목코드
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    futs_prpr: str | None = None  # 선물 현재가
    futs_prdy_vrss: str | None = None  # 선물 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    futs_prdy_ctrt: str | None = None  # 선물 전일 대비율
    hts_thpr: str | None = None  # HTS 이론가
    acml_vol: str | None = None  # 누적 거래량
    futs_askp: str | None = None  # 선물 매도호가
    futs_bidp: str | None = None  # 선물 매수호가
    hts_otst_stpl_qty: str | None = None  # HTS 미결제 약정 수량
    futs_hgpr: str | None = None  # 선물 최고가
    futs_lwpr: str | None = None  # 선물 최저가
    hts_rmnn_dynu: str | None = None  # HTS 잔존 일수
    total_askp_rsqn: str | None = None  # 총 매도호가 잔량
    total_bidp_rsqn: str | None = None  # 총 매수호가 잔량
    futs_antc_cnpr: str | None = None  # 선물예상체결가
    futs_antc_cntg_vrss: str | None = None  # 선물예상체결대비
    antc_cntg_vrss_sign: str | None = None  # 예상 체결 대비 부호
    antc_cntg_prdy_ctrt: str | None = None  # 예상 체결 전일 대비율

class DisplayBoardFuturesResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[DisplayBoardFuturesResponse_Output1Item] = []  # 응답상세 — array

class DisplayBoardFuturesExecutor(ApiExecutor[DisplayBoardFuturesRequest, DisplayBoardFuturesResponse]):
    """국내옵션전광판_선물[국내선물-023]."""

    # 국내옵션전광판_선물 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0503] 선물옵션 종합시세(Ⅰ) 화면의 "하단" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-futureoption/v1/quotations/display-board-futures"
    METHOD = "GET"
    RESPONSE_TYPE = DisplayBoardFuturesResponse
    TR_ID = "FHPIF05030200"
