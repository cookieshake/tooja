"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class FrgnmemTradeEstimateRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — 시장구분코드 (J)
    FID_COND_SCR_DIV_CODE: str  # 조건화면분류코드 — Uniquekey (16441)
    FID_INPUT_ISCD: str  # 입력종목코드 — 0000(전체), 1001(코스피), 2001(코스닥)
    FID_RANK_SORT_CLS_CODE: str  # 순위정렬구분코드 — 0(금액순), 1(수량순)
    FID_RANK_SORT_CLS_CODE_2: str  # 순위정렬구분코드2 — 0(매수순), 1(매도순)

class FrgnmemTradeEstimateResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_shrn_iscd: str | None = None  # 주식단축종목코드
    hts_kor_isnm: str | None = None  # HTS한글종목명
    glob_ntsl_qty: str | None = None  # 외국계순매도수량
    stck_prpr: str | None = None  # 주식현재가
    prdy_vrss: str | None = None  # 전일대비
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_ctrt: str | None = None  # 전일대비율
    acml_vol: str | None = None  # 누적거래량
    glob_total_seln_qty: str | None = None  # 외국계총매도수량
    glob_total_shnu_qty: str | None = None  # 외국계총매수2수량

class FrgnmemTradeEstimateResponse(KisCommonResponse):
    """응답 본문."""

    output: list[FrgnmemTradeEstimateResponse_OutputItem] = []  # 응답상세 — array

class FrgnmemTradeEstimateExecutor(ApiExecutor[FrgnmemTradeEstimateRequest, FrgnmemTradeEstimateResponse]):
    """외국계 매매종목 가집계 [국내주식-161]."""

    # 외국계 매매종목 가집계 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0430] 외국계 매매종목 가집계 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/frgnmem-trade-estimate"
    METHOD = "GET"
    RESPONSE_TYPE = FrgnmemTradeEstimateResponse
    TR_ID = "FHKST644100C0"
