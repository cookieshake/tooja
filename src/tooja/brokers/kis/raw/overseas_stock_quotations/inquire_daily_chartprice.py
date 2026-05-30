"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireDailyChartpriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # FID 조건 시장 분류 코드 — N: 해외지수, X 환율, I: 국채, S:금선물
    FID_INPUT_ISCD: str  # FID 입력 종목코드 — 종목코드 ※ 해외주식 마스터 코드 참조 (포럼 > FAQ > 종목정보 다운로드(해외) > 해외지수) ※ 해당 API로 미국주식 조회 시, 다우30, 나스닥100, S&P500 종목만 조회 가능합니다. 더 많은 미국주식 종목 시
    FID_INPUT_DATE_1: str  # FID 입력 날짜1 — 시작일자(YYYYMMDD)
    FID_INPUT_DATE_2: str  # FID 입력 날짜2 — 종료일자(YYYYMMDD)
    FID_PERIOD_DIV_CODE: str  # FID 기간 분류 코드 — D:일, W:주, M:월, Y:년

class InquireDailyChartpriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    ovrs_nmix_prdy_vrss: str | None = None  # 전일 대비 — 16(11.4) 정수부분 11자리, 소수부분 4자리
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율 — 11(8.2) 정수부분 8자리, 소수부분 2자리
    ovrs_nmix_prdy_clpr: str | None = None  # 전일 종가 — 16(11.4) 정수부분 11자리, 소수부분 4자리
    acml_vol: str | None = None  # 누적 거래량
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    ovrs_nmix_prpr: str | None = None  # 현재가 — 16(11.4) 정수부분 11자리, 소수부분 4자리
    stck_shrn_iscd: str | None = None  # 단축 종목코드
    prdy_vol: str | None = None  # 전일 거래량
    ovrs_prod_oprc: str | None = None  # 시가 — 16(11.4) 정수부분 11자리, 소수부분 4자리
    ovrs_prod_hgpr: str | None = None  # 최고가 — 16(11.4) 정수부분 11자리, 소수부분 4자리
    ovrs_prod_lwpr: str | None = None  # 최저가 — 16(11.4) 정수부분 11자리, 소수부분 4자리

class InquireDailyChartpriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 영업 일자
    ovrs_nmix_prpr: str | None = None  # 현재가 — 16(11.4) 정수부분 11자리, 소수부분 4자리
    ovrs_nmix_oprc: str | None = None  # 시가 — 16(11.4) 정수부분 11자리, 소수부분 4자리
    ovrs_nmix_hgpr: str | None = None  # 최고가 — 16(11.4) 정수부분 11자리, 소수부분 4자리
    ovrs_nmix_lwpr: str | None = None  # 최저가 — 16(11.4) 정수부분 11자리, 소수부분 4자리
    acml_vol: str | None = None  # 누적 거래량
    mod_yn: str | None = None  # 변경 여부

class InquireDailyChartpriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireDailyChartpriceResponse_Output1Item | None = None  # 응답상세1 — 기본정보
    output2: list[InquireDailyChartpriceResponse_Output2Item] = []  # 응답상세2 — 일자별 정보

class InquireDailyChartpriceExecutor(ApiExecutor[InquireDailyChartpriceRequest, InquireDailyChartpriceResponse]):
    """해외주식 종목/지수/환율기간별시세(일/주/월/년)[v1_해외주식-012]."""

    # 해외주식 종목/지수/환율기간별시세(일/주/월/년) API입니다. 해외지수 당일 시세의 경우 지연시세 or 종가시세가 제공됩니다. ※ 해당 API로 미국주식 조회 시, 다우30, 나스닥100, S&P500 종목만 조회 가능합니다. 더 많은 미국주식 종목 시세를 이용할 시에는, 해외주식기간별시세 API 사용 부탁드립니다.

    PATH = "/uapi/overseas-price/v1/quotations/inquire-daily-chartprice"
    METHOD = "GET"
    RESPONSE_TYPE = InquireDailyChartpriceResponse
    TR_ID = "FHKST03030100"
