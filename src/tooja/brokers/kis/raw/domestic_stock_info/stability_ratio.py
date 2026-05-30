"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class StabilityRatioRequest(KisBaseModel):
    """요청."""

    fid_input_iscd: str  # 입력 종목코드 — 000660 : 종목코드
    fid_div_cls_code: str  # 분류 구분 코드 — 0: 년, 1: 분기
    fid_cond_mrkt_div_code: str  # 조건 시장 분류 코드 — J

class StabilityRatioResponse_OutputItem(KisBaseModel):
    """nested item."""

    stac_yymm: str | None = None  # 결산 년월
    lblt_rate: str | None = None  # 부채 비율
    bram_depn: str | None = None  # 차입금 의존도
    crnt_rate: str | None = None  # 유동 비율
    quck_rate: str | None = None  # 당좌 비율

class StabilityRatioResponse(KisCommonResponse):
    """응답 본문."""

    output: list[StabilityRatioResponse_OutputItem] = []  # 응답상세 — array

class StabilityRatioExecutor(ApiExecutor[StabilityRatioRequest, StabilityRatioResponse]):
    """국내주식 안정성비율[v1_국내주식-083]."""

    # 국내주식 안정성비율 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0635] 재무분석종합 화면의 하단 '5. 안정성비율' 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/finance/stability-ratio"
    METHOD = "GET"
    RESPONSE_TYPE = StabilityRatioResponse
    TR_ID = "FHKST66430600"
