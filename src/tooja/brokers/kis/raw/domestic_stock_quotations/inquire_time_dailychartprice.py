"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireTimeDailychartpriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — J:KRX, NX:NXT, UN:통합
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목코드 (ex 005930 삼성전자)
    FID_INPUT_HOUR_1: str  # 입력 시간1 — 입력 시간(ex 13시 130000)
    FID_INPUT_DATE_1: str  # 입력 날짜1 — 입력 날짜(20241023)
    FID_PW_DATA_INCU_YN: str  # 과거 데이터 포함 여부
    FID_FAKE_TICK_INCU_YN: str | None = None  # 허봉 포함 여부 — 공백 필수 입력

class InquireTimeDailychartpriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    stck_prdy_clpr: str | None = None  # 주식 전일 종가
    acml_vol: str | None = None  # 누적 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    stck_prpr: str | None = None  # 주식 현재가

class InquireTimeDailychartpriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자
    stck_cntg_hour: str | None = None  # 주식 체결 시간
    stck_prpr: str | None = None  # 주식 현재가
    stck_oprc: str | None = None  # 주식 시가2
    stck_hgpr: str | None = None  # 주식 최고가
    stck_lwpr: str | None = None  # 주식 최저가
    cntg_vol: str | None = None  # 체결 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금

class InquireTimeDailychartpriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireTimeDailychartpriceResponse_Output1Item | None = None  # 응답상세
    output2: list[InquireTimeDailychartpriceResponse_Output2Item] = []  # 응답상세 — array

class InquireTimeDailychartpriceExecutor(ApiExecutor[InquireTimeDailychartpriceRequest, InquireTimeDailychartpriceResponse]):
    """주식일별분봉조회 [국내주식-213]."""

    # 주식일별분봉조회 API입니다. 실전계좌의 경우, 한 번의 호출에 최대 120건까지 확인 가능하며, FID_INPUT_DATE_1, FID_INPUT_HOUR_1 이용하여 과거일자 분봉조회 가능합니다. ※ 과거 분봉 조회 시, 당사 서버에서 보관하고 있는 만큼의 데이터만 확인이 가능합니다. (최대 1년 분봉 보관)

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-time-dailychartprice"
    METHOD = "GET"
    RESPONSE_TYPE = InquireTimeDailychartpriceResponse
    TR_ID = "FHKST03010230"
