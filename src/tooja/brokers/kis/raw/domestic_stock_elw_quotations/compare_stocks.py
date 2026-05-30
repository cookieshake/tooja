"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class CompareStocksRequest(KisBaseModel):
    """요청."""

    FID_COND_SCR_DIV_CODE: str  # 조건화면분류코드 — 11517(Primary key)
    FID_INPUT_ISCD: str  # 입력종목코드 — 종목코드(ex)005930(삼성전자))

class CompareStocksResponse_OutputItem(KisBaseModel):
    """nested item."""

    elw_shrn_iscd: str | None = None  # ELW단축종목코드
    elw_kor_isnm: str | None = None  # ELW한글종목명

class CompareStocksResponse(KisCommonResponse):
    """응답 본문."""

    output: CompareStocksResponse_OutputItem | None = None  # 응답상세

class CompareStocksExecutor(ApiExecutor[CompareStocksRequest, CompareStocksResponse]):
    """ELW 비교대상종목조회 [국내주식-183]."""

    # ELW 비교대상종목조회 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0288] ELW 기초자산별 ELW 시세의 좌측 화면 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/elw/v1/quotations/compare-stocks"
    METHOD = "GET"
    RESPONSE_TYPE = CompareStocksResponse
    TR_ID = "FHKEW151701C0"
