"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireDailyIndexchartpriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — 업종 : U
    FID_INPUT_ISCD: str  # 업종 상세코드 — '0001 : 종합 0002 : 대형주 ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조)'
    FID_INPUT_DATE_1: str  # 조회 시작일자 — 조회 시작일자 (ex. 20220501)
    FID_INPUT_DATE_2: str  # 조회 종료일자 — 조회 종료일자 (ex. 20220530)
    FID_PERIOD_DIV_CODE: str  # ' 기간분류코드' — ' D:일봉 W:주봉, M:월봉, Y:년봉'

class InquireDailyIndexchartpriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    bstp_nmix_prdy_ctrt: str | None = None  # 업종 지수 전일 대비율
    prdy_nmix: str | None = None  # 전일 지수
    acml_vol: str | None = None  # 누적 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    bstp_nmix_prpr: str | None = None  # 업종 지수 현재가
    bstp_cls_code: str | None = None  # 업종 구분 코드
    prdy_vol: str | None = None  # 전일 거래량
    bstp_nmix_oprc: str | None = None  # 업종 지수 시가2
    bstp_nmix_hgpr: str | None = None  # 업종 지수 최고가
    bstp_nmix_lwpr: str | None = None  # 업종 지수 최저가
    futs_prdy_oprc: str | None = None  # 선물 전일 시가
    futs_prdy_hgpr: str | None = None  # 선물 전일 최고가
    futs_prdy_lwpr: str | None = None  # 선물 전일 최저가

class InquireDailyIndexchartpriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자
    bstp_nmix_prpr: str | None = None  # 업종 지수 현재가
    bstp_nmix_oprc: str | None = None  # 업종 지수 시가2
    bstp_nmix_hgpr: str | None = None  # 업종 지수 최고가
    bstp_nmix_lwpr: str | None = None  # 업종 지수 최저가
    acml_vol: str | None = None  # 누적 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    mod_yn: str | None = None  # 변경 여부

class InquireDailyIndexchartpriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireDailyIndexchartpriceResponse_Output1Item | None = None  # 응답상세 — Single
    output2: list[InquireDailyIndexchartpriceResponse_Output2Item] = []  # 응답상세 — Array

class InquireDailyIndexchartpriceExecutor(ApiExecutor[InquireDailyIndexchartpriceRequest, InquireDailyIndexchartpriceResponse]):
    """국내주식업종기간별시세(일/주/월/년)[v1_국내주식-021]."""

    # 국내주식 업종기간별시세(일/주/월/년) API입니다. 실전계좌/모의계좌의 경우, 한 번의 호출에 최대 50건까지 확인 가능합니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-daily-indexchartprice"
    METHOD = "GET"
    RESPONSE_TYPE = InquireDailyIndexchartpriceResponse
    TR_ID = "FHKUP03500100"
