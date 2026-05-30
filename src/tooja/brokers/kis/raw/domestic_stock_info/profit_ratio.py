"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class ProfitRatioRequest(KisBaseModel):
    """요청."""

    fid_input_iscd: str  # 입력 종목코드 — 000660 : 종목코드
    FID_DIV_CLS_CODE: str  # 분류 구분 코드 — 0: 년, 1: 분기
    fid_cond_mrkt_div_code: str  # 조건 시장 분류 코드 — J

class ProfitRatioResponse_OutputItem(KisBaseModel):
    """nested item."""

    stac_yymm: str | None = None  # 결산 년월
    cptl_ntin_rate: str | None = None  # 총자본 순이익율
    self_cptl_ntin_inrt: str | None = None  # 자기자본 순이익율
    sale_ntin_rate: str | None = None  # 매출액 순이익율
    sale_totl_rate: str | None = None  # 매출액 총이익율

class ProfitRatioResponse(KisCommonResponse):
    """응답 본문."""

    output: list[ProfitRatioResponse_OutputItem] = []  # 응답상세 — array

class ProfitRatioExecutor(ApiExecutor[ProfitRatioRequest, ProfitRatioResponse]):
    """국내주식 수익성비율[v1_국내주식-081]."""

    # 국내주식 수익성비율 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0635] 재무분석종합 화면의 하단 '4. 수익성비율' 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/finance/profit-ratio"
    METHOD = "GET"
    RESPONSE_TYPE = ProfitRatioResponse
    TR_ID = "FHKST66430400"
