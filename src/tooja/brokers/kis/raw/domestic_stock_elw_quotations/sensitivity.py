"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class SensitivityRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — 시장구분코드 (W)
    FID_COND_SCR_DIV_CODE: str  # 조건화면분류코드 — Unique key(20285)
    FID_UNAS_INPUT_ISCD: str  # 기초자산입력종목코드 — '000000(전체), 2001(코스피200) , 3003(코스닥150), 005930(삼성전자) '
    FID_INPUT_ISCD: str  # 입력종목코드 — '00000(전체), 00003(한국투자증권) , 00017(KB증권), 00005(미래에셋주식회사)'
    FID_DIV_CLS_CODE: str  # 콜풋구분코드 — 0(전체), 1(콜), 2(풋)
    FID_INPUT_PRICE_1: str  # 가격(이상)
    FID_INPUT_PRICE_2: str  # 가격(이하)
    FID_INPUT_VOL_1: str  # 거래량(이상)
    FID_INPUT_VOL_2: str  # 거래량(이하)
    FID_RANK_SORT_CLS_CODE: str  # 순위정렬구분코드 — '0(이론가), 1(델타), 2(감마), 3(로), 4(베가) , 5(로) , 6(내재변동성), 7(90일변동성)'
    FID_INPUT_RMNN_DYNU_1: str  # 잔존일수(이상)
    FID_INPUT_DATE_1: str  # 조회기준일
    FID_BLNG_CLS_CODE: str  # 결재방법 — 0(전체), 1(일반), 2(조기종료)

class SensitivityResponse_OutputItem(KisBaseModel):
    """nested item."""

    elw_shrn_iscd: str | None = None  # ELW단축종목코드
    elw_kor_isnm: str | None = None  # ELW한글종목명
    elw_prpr: str | None = None  # ELW현재가
    prdy_vrss: str | None = None  # 전일대비
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_ctrt: str | None = None  # 전일대비율
    acml_vol: str | None = None  # 누적거래량
    hts_thpr: str | None = None  # HTS이론가
    delta_val: str | None = None  # 델타값
    gama: str | None = None  # 감마
    theta: str | None = None  # 세타
    vega: str | None = None  # 베가
    rho: str | None = None  # 로우
    hts_ints_vltl: str | None = None  # HTS내재변동성
    d90_hist_vltl: str | None = None  # 90일역사적변동성

class SensitivityResponse(KisCommonResponse):
    """응답 본문."""

    output: list[SensitivityResponse_OutputItem] = []  # 응답상세 — array

class SensitivityExecutor(ApiExecutor[SensitivityRequest, SensitivityResponse]):
    """ELW 민감도 순위[국내주식-170]."""

    # ELW 민감도 순위 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0285] ELW 민감도 순위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/elw/v1/ranking/sensitivity"
    METHOD = "GET"
    RESPONSE_TYPE = SensitivityResponse
    TR_ID = "FHPEW02850000"
