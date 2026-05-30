"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class DisplayBoardTopRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — 시장구분코드 (F: 선물)
    FID_INPUT_ISCD: str  # 입력 종목코드 — 선물최근월물 ex)(101V06)
    FID_COND_MRKT_DIV_CODE1: str  # 조건 시장 분류 코드 — 공백
    FID_COND_SCR_DIV_CODE: str  # 조건 화면 분류 코드 — 공백
    FID_MTRT_CNT: str  # 만기 수 — 공백
    FID_COND_MRKT_CLS_CODE: str  # 조건 시장 구분 코드 — 공백

class DisplayBoardTopResponse_Output1Item(KisBaseModel):
    """nested item."""

    unas_prpr: str | None = None  # 기초자산 현재가
    unas_prdy_vrss: str | None = None  # 기초자산 전일 대비
    unas_prdy_vrss_sign: str | None = None  # 기초자산 전일 대비 부호
    unas_prdy_ctrt: str | None = None  # 기초자산 전일 대비율
    unas_acml_vol: str | None = None  # 기초자산 누적 거래량
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    futs_prpr: str | None = None  # 선물 현재가
    futs_prdy_vrss: str | None = None  # 선물 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    futs_prdy_ctrt: str | None = None  # 선물 전일 대비율

class DisplayBoardTopResponse_Output2Item(KisBaseModel):
    """nested item."""

    hts_rmnn_dynu: str | None = None  # HTS 잔존 일수

class DisplayBoardTopResponse(KisCommonResponse):
    """응답 본문."""

    output1: DisplayBoardTopResponse_Output1Item | None = None  # 응답상세
    output2: list[DisplayBoardTopResponse_Output2Item] = []  # 응답상세 — array

class DisplayBoardTopExecutor(ApiExecutor[DisplayBoardTopRequest, DisplayBoardTopResponse]):
    """국내선물 기초자산 시세[국내선물-021]."""

    # 국내선물 기초자산 시세 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0503] 선물옵션 종합시세(Ⅰ) 화면의 "상단 바" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-futureoption/v1/quotations/display-board-top"
    METHOD = "GET"
    RESPONSE_TYPE = DisplayBoardTopResponse
    TR_ID = "FHPIF05030000"
