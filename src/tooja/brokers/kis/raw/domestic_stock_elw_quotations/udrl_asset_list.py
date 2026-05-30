"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class UdrlAssetListRequest(KisBaseModel):
    """요청."""

    FID_COND_SCR_DIV_CODE: str  # 조건화면분류코드 — 11541(Primary key)
    FID_RANK_SORT_CLS_CODE: str  # 순위정렬구분코드 — 0(종목명순), 1(콜발행종목순), 2(풋발행종목순), 3(전일대비 상승율순), 4(전일대비 하락율순), 5(현재가 크기순), 6(종목코드순)
    FID_INPUT_ISCD: str  # 입력종목코드 — 00000(전체), 00003(한국투자증권), 00017(KB증권), 00005(미래에셋)

class UdrlAssetListResponse_OutputItem(KisBaseModel):
    """nested item."""

    unas_shrn_iscd: str | None = None  # 기초자산단축종목코드
    unas_isnm: str | None = None  # 기초자산종목명
    unas_prpr: str | None = None  # 기초자산현재가
    unas_prdy_vrss: str | None = None  # 기초자산전일대비
    unas_prdy_vrss_sign: str | None = None  # 기초자산전일대비부호
    unas_prdy_ctrt: str | None = None  # 기초자산전일대비율

class UdrlAssetListResponse(KisCommonResponse):
    """응답 본문."""

    output: list[UdrlAssetListResponse_OutputItem] = []  # 응답상세 — array

class UdrlAssetListExecutor(ApiExecutor[UdrlAssetListRequest, UdrlAssetListResponse]):
    """ELW 기초자산 목록조회 [국내주식-185]."""

    # ELW 기초자산 목록조회 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0288] ELW 기초자산별 ELW 시세 화면 의 "왼쪽 기초자산 목록" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/elw/v1/quotations/udrl-asset-list"
    METHOD = "GET"
    RESPONSE_TYPE = UdrlAssetListResponse
    TR_ID = "FHKEW154100C0"
