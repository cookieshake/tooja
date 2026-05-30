"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class ExpClosingPriceRequest(KisBaseModel):
    """요청."""

    FID_RANK_SORT_CLS_CODE: str  # 순위 정렬 구분 코드 — 0:전체, 1:상한가마감예상, 2:하한가마감예상, 3:직전대비상승률상위 ,4:직전대비하락률상위
    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — 시장구분코드 (주식 J)
    FID_COND_SCR_DIV_CODE: str  # 조건 화면 분류 코드 — Unique key(11173)
    FID_INPUT_ISCD: str  # 입력 종목코드 — 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
    FID_BLNG_CLS_CODE: str  # 소속 구분 코드 — 0:전체, 1:종가범위연장

class ExpClosingPriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    stck_shrn_iscd: str | None = None  # 주식 단축 종목코드
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    sdpr_vrss_prpr: str | None = None  # 기준가 대비 현재가
    sdpr_vrss_prpr_rate: str | None = None  # 기준가 대비 현재가 비율
    cntg_vol: str | None = None  # 체결 거래량

class ExpClosingPriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[ExpClosingPriceResponse_Output1Item] = []  # 응답상세 — array

class ExpClosingPriceExecutor(ApiExecutor[ExpClosingPriceRequest, ExpClosingPriceResponse]):
    """국내주식 장마감 예상체결가[국내주식-120]."""

    # 국내주식 장마감 예상체결가 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0183] 장마감 예상체결가 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/exp-closing-price"
    METHOD = "GET"
    RESPONSE_TYPE = ExpClosingPriceResponse
    TR_ID = "FHKST117300C0"
