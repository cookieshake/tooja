"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class UpdownRateRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 사용자권한정보 — 시장구분코드 (W)
    FID_COND_SCR_DIV_CODE: str  # 거래소코드 — Unique key(20277)
    FID_UNAS_INPUT_ISCD: str  # 상승율/하락율 구분 — '000000(전체), 2001(코스피200) , 3003(코스닥150), 005930(삼성전자) '
    FID_INPUT_ISCD: str  # N일자값 — '00000(전체), 00003(한국투자증권) , 00017(KB증권), 00005(미래에셋주식회사)'
    FID_INPUT_RMNN_DYNU_1: str  # 거래량조건 — '0(전체), 1(1개월이하), 2(1개월~2개월), 3(2개월~3개월), 4(3개월~6개월), 5(6개월~9개월),6(9개월~12개월), 7(12개월이상)'
    FID_DIV_CLS_CODE: str  # NEXT KEY BUFF — 0(전체), 1(콜), 2(풋)
    FID_INPUT_PRICE_1: str  # 사용자권한정보
    FID_INPUT_PRICE_2: str  # 거래소코드
    FID_INPUT_VOL_1: str  # 상승율/하락율 구분
    FID_INPUT_VOL_2: str  # N일자값
    FID_INPUT_DATE_1: str  # 거래량조건
    FID_RANK_SORT_CLS_CODE: str  # NEXT KEY BUFF — '0(상승율), 1(하락율), 2(시가대비상승율) , 3(시가대비하락율), 4(변동율)'
    FID_BLNG_CLS_CODE: str  # 사용자권한정보 — 0(전체)
    FID_INPUT_DATE_2: str  # 거래소코드

class UpdownRateResponse_OutputItem(KisBaseModel):
    """nested item."""

    hts_kor_isnm: str | None = None  # HTS한글종목명
    elw_shrn_iscd: str | None = None  # ELW단축종목코드
    elw_prpr: str | None = None  # ELW현재가
    prdy_vrss: str | None = None  # 전일대비
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_ctrt: str | None = None  # 전일대비율
    acml_vol: str | None = None  # 누적거래량
    stck_sdpr: str | None = None  # 주식기준가
    sdpr_vrss_prpr_sign: str | None = None  # 기준가대비현재가부호
    sdpr_vrss_prpr: str | None = None  # 기준가대비현재가
    sdpr_vrss_prpr_rate: str | None = None  # 기준가대비현재가비율
    stck_oprc: str | None = None  # 주식시가2
    oprc_vrss_prpr_sign: str | None = None  # 시가2대비현재가부호
    oprc_vrss_prpr: str | None = None  # 시가2대비현재가
    oprc_vrss_prpr_rate: str | None = None  # 시가2대비현재가비율
    stck_hgpr: str | None = None  # 주식최고가
    stck_lwpr: str | None = None  # 주식최저가
    prd_rsfl_sign: str | None = None  # 기간등락부호
    prd_rsfl: str | None = None  # 기간등락
    prd_rsfl_rate: str | None = None  # 기간등락비율
    stck_cnvr_rate: str | None = None  # 주식전환비율
    hts_rmnn_dynu: str | None = None  # HTS잔존일수
    acpr: str | None = None  # 행사가
    unas_isnm: str | None = None  # 기초자산명
    unas_shrn_iscd: str | None = None  # 기초자산코드
    lp_hldn_rate: str | None = None  # LP보유비율
    prit: str | None = None  # 패리티
    prls_qryr_stpr_prc: str | None = None  # 손익분기주가가격
    delta_val: str | None = None  # 델타값
    theta: str | None = None  # 세타
    prls_qryr_rate: str | None = None  # 손익분기비율
    stck_lstn_date: str | None = None  # 주식상장일자
    stck_last_tr_date: str | None = None  # 주식최종거래일자
    hts_ints_vltl: str | None = None  # HTS내재변동성
    lvrg_val: str | None = None  # 레버리지값

class UpdownRateResponse(KisCommonResponse):
    """응답 본문."""

    output: list[UpdownRateResponse_OutputItem] = []  # 응답상세 — array

class UpdownRateExecutor(ApiExecutor[UpdownRateRequest, UpdownRateResponse]):
    """ELW 상승률순위[국내주식-167]."""

    # ELW 상승률순위 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0277] ELW 상승률순위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/elw/v1/ranking/updown-rate"
    METHOD = "GET"
    RESPONSE_TYPE = UpdownRateResponse
    TR_ID = "FHPEW02770000"
