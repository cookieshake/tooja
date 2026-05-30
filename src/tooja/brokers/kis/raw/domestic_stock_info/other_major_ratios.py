"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OtherMajorRatiosRequest(KisBaseModel):
    """요청."""

    fid_input_iscd: str  # 입력 종목코드 — 000660 : 종목코드
    fid_div_cls_code: str  # 분류 구분 코드 — 0: 년, 1: 분기
    fid_cond_mrkt_div_code: str  # 조건 시장 분류 코드 — J

class OtherMajorRatiosResponse_OutputItem(KisBaseModel):
    """nested item."""

    stac_yymm: str | None = None  # 결산 년월
    payout_rate: str | None = None  # 배당 성향 — 비정상 출력되는 데이터로 무시
    eva: str | None = None  # EVA
    ebitda: str | None = None  # EBITDA
    ev_ebitda: str | None = None  # EV_EBITDA

class OtherMajorRatiosResponse(KisCommonResponse):
    """응답 본문."""

    output: list[OtherMajorRatiosResponse_OutputItem] = []  # 응답상세 — array

class OtherMajorRatiosExecutor(ApiExecutor[OtherMajorRatiosRequest, OtherMajorRatiosResponse]):
    """국내주식 기타주요비율[v1_국내주식-082]."""

    # 국내주식 기타주요비율 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0635] 재무분석종합 화면의 하단 '9. 기타주요비율' 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/finance/other-major-ratios"
    METHOD = "GET"
    RESPONSE_TYPE = OtherMajorRatiosResponse
    TR_ID = "FHKST66430500"
