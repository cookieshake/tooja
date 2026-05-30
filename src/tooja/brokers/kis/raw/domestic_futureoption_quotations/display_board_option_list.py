"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class DisplayBoardOptionListRequest(KisBaseModel):
    """요청."""

    FID_COND_SCR_DIV_CODE: str  # 조건 화면 분류 코드 — Unique key(509)
    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — 공백
    FID_COND_MRKT_CLS_CODE: str  # 조건 시장 구분 코드 — 공백

class DisplayBoardOptionListResponse_Output1Item(KisBaseModel):
    """nested item."""

    mtrt_yymm_code: str | None = None  # 만기 년월 코드
    mtrt_yymm: str | None = None  # 만기 년월

class DisplayBoardOptionListResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[DisplayBoardOptionListResponse_Output1Item] = []  # 응답상세 — array

class DisplayBoardOptionListExecutor(ApiExecutor[DisplayBoardOptionListRequest, DisplayBoardOptionListResponse]):
    """국내옵션전광판_옵션월물리스트[국내선물-020]."""

    # 국내업종 국내옵션전광판_옵션월물리스트 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0503] 선물옵션 종합시세(Ⅰ) 화면의 "월물리스트 목록 확인" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-futureoption/v1/quotations/display-board-option-list"
    METHOD = "GET"
    RESPONSE_TYPE = DisplayBoardOptionListResponse
    TR_ID = "FHPIO056104C0"
