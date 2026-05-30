"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class ExpIndexTrendRequest(KisBaseModel):
    """요청."""

    FID_MKOP_CLS_CODE: str  # 장운영 구분 코드 — 1: 장시작전, 2: 장마감
    FID_INPUT_HOUR_1: str  # 입력 시간1 — 10(10초), 30(30초), 60(1분), 600(10분)
    FID_INPUT_ISCD: str  # 입력 종목코드 — 0000:전체, 0001:코스피, 1001:코스닥, 2001:코스피200, 4001: KRX100
    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — 시장구분코드 (주식 U)

class ExpIndexTrendResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_cntg_hour: str | None = None  # 주식 단축 종목코드
    bstp_nmix_prpr: str | None = None  # HTS 한글 종목명
    prdy_vrss_sign: str | None = None  # 주식 현재가
    bstp_nmix_prdy_vrss: str | None = None  # 전일 대비
    prdy_ctrt: str | None = None  # 전일 대비 부호
    acml_vol: str | None = None  # 전일 대비율
    acml_tr_pbmn: str | None = None  # 기준가 대비 현재가

class ExpIndexTrendResponse(KisCommonResponse):
    """응답 본문."""

    output: list[ExpIndexTrendResponse_OutputItem] = []  # 응답상세 — array

class ExpIndexTrendExecutor(ApiExecutor[ExpIndexTrendRequest, ExpIndexTrendResponse]):
    """국내주식 예상체결지수 추이[국내주식-121]."""

    # 국내주식 예상체결지수 추이 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0184] 예상체결지수 추이 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/exp-index-trend"
    METHOD = "GET"
    RESPONSE_TYPE = ExpIndexTrendResponse
    TR_ID = "FHPST01840000"
