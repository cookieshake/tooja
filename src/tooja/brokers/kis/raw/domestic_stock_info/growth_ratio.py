"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class GrowthRatioRequest(KisBaseModel):
    """요청."""

    fid_input_iscd: str  # 입력 종목코드 — ex : 000660
    fid_div_cls_code: str  # 분류 구분 코드 — 0: 년, 1: 분기
    fid_cond_mrkt_div_code: str  # 조건 시장 분류 코드 — 시장구분코드 (주식 J)

class GrowthRatioResponse_OutputItem(KisBaseModel):
    """nested item."""

    stac_yymm: str | None = None  # 결산 년월
    grs: str | None = None  # 매출액 증가율
    bsop_prfi_inrt: str | None = None  # 영업 이익 증가율
    equt_inrt: str | None = None  # 자기자본 증가율
    totl_aset_inrt: str | None = None  # 총자산 증가율

class GrowthRatioResponse(KisCommonResponse):
    """응답 본문."""

    output: list[GrowthRatioResponse_OutputItem] = []  # 응답상세 — array

class GrowthRatioExecutor(ApiExecutor[GrowthRatioRequest, GrowthRatioResponse]):
    """국내주식 성장성비율[v1_국내주식-085]."""

    # 국내주식 성장성비율 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0635] 재무분석종합 화면의 하단 '7.성장성비율' 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/finance/growth-ratio"
    METHOD = "GET"
    RESPONSE_TYPE = GrowthRatioResponse
    TR_ID = "FHKST66430800"
