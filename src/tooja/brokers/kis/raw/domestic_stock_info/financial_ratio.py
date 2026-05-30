"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class FinancialRatioRequest(KisBaseModel):
    """요청."""

    FID_DIV_CLS_CODE: str  # 분류 구분 코드 — 0: 년, 1: 분기
    fid_cond_mrkt_div_code: str  # 조건 시장 분류 코드 — J
    fid_input_iscd: str  # 입력 종목코드 — 000660 : 종목코드

class FinancialRatioResponse_OutputItem(KisBaseModel):
    """nested item."""

    stac_yymm: str | None = None  # 결산 년월
    grs: str | None = None  # 매출액 증가율
    bsop_prfi_inrt: str | None = None  # 영업 이익 증가율 — 적자지속, 흑자전환, 적자전환인 경우 0으로 표시
    ntin_inrt: str | None = None  # 순이익 증가율
    roe_val: str | None = None  # ROE 값
    eps: str | None = None  # EPS
    sps: str | None = None  # 주당매출액
    bps: str | None = None  # BPS
    rsrv_rate: str | None = None  # 유보 비율
    lblt_rate: str | None = None  # 부채 비율

class FinancialRatioResponse(KisCommonResponse):
    """응답 본문."""

    output: list[FinancialRatioResponse_OutputItem] = []  # 응답상세 — array

class FinancialRatioExecutor(ApiExecutor[FinancialRatioRequest, FinancialRatioResponse]):
    """국내주식 재무비율[v1_국내주식-080]."""

    # 국내주식 재무비율 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0635] 재무분석종합 화면의 우측의 '재무 비율' 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/finance/financial-ratio"
    METHOD = "GET"
    RESPONSE_TYPE = FinancialRatioResponse
    TR_ID = "FHKST66430300"
