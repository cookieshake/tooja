"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class BalanceSheetRequest(KisBaseModel):
    """요청."""

    FID_DIV_CLS_CODE: str  # 분류 구분 코드 — 0: 년, 1: 분기
    fid_cond_mrkt_div_code: str  # 조건 시장 분류 코드 — J
    fid_input_iscd: str  # 입력 종목코드 — 000660 : 종목코드

class BalanceSheetResponse_OutputItem(KisBaseModel):
    """nested item."""

    stac_yymm: str | None = None  # 결산 년월
    cras: str | None = None  # 유동자산
    fxas: str | None = None  # 고정자산
    total_aset: str | None = None  # 자산총계
    flow_lblt: str | None = None  # 유동부채
    fix_lblt: str | None = None  # 고정부채
    total_lblt: str | None = None  # 부채총계
    cpfn: str | None = None  # 자본금
    cfp_surp: str | None = None  # 자본 잉여금 — 출력되지 않는 데이터(99.99 로 표시)
    prfi_surp: str | None = None  # 이익 잉여금 — 출력되지 않는 데이터(99.99 로 표시)
    total_cptl: str | None = None  # 자본총계

class BalanceSheetResponse(KisCommonResponse):
    """응답 본문."""

    output: list[BalanceSheetResponse_OutputItem] = []  # 응답상세 — array

class BalanceSheetExecutor(ApiExecutor[BalanceSheetRequest, BalanceSheetResponse]):
    """국내주식 대차대조표[v1_국내주식-078]."""

    # 국내주식 대차대조표 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0635] 재무분석종합 화면의 하단 '1. 대차대조표' 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/finance/balance-sheet"
    METHOD = "GET"
    RESPONSE_TYPE = BalanceSheetResponse
    TR_ID = "FHKST66430100"
