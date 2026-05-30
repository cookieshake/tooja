"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class CountriesHolidayRequest(KisBaseModel):
    """요청."""

    TRAD_DT: str  # 기준일자 — 기준일자(YYYYMMDD)
    CTX_AREA_NK: str  # 연속조회키 — 공백으로 입력
    CTX_AREA_FK: str  # 연속조회검색조건 — 공백으로 입력

class CountriesHolidayResponse_OutputItem(KisBaseModel):
    """nested item."""

    prdt_type_cd: str | None = None  # 상품유형코드 — 512 미국 나스닥 / 513 미국 뉴욕거래소 / 529 미국 아멕스 515 일본 501 홍콩 / 543 홍콩CNY / 558 홍콩USD 507 베트남 하노이거래소 / 508 베트남 호치민거래소 551 중국 상해A / 552 중국 심천
    tr_natn_cd: str | None = None  # 거래국가코드 — 840 미국 / 392 일본 / 344 홍콩 704 베트남 / 156 중국
    tr_natn_name: str | None = None  # 거래국가명
    natn_eng_abrv_cd: str | None = None  # 국가영문약어코드 — US 미국 / JP 일본 / HK 홍콩 VN 베트남 / CN 중국
    tr_mket_cd: str | None = None  # 거래시장코드
    tr_mket_name: str | None = None  # 거래시장명
    acpl_sttl_dt: str | None = None  # 현지결제일자 — 현지결제일자(YYYYMMDD)
    dmst_sttl_dt: str | None = None  # 국내결제일자 — 국내결제일자(YYYYMMDD)

class CountriesHolidayResponse(KisCommonResponse):
    """응답 본문."""

    output: CountriesHolidayResponse_OutputItem | None = None  # 응답상세1

class CountriesHolidayExecutor(ApiExecutor[CountriesHolidayRequest, CountriesHolidayResponse]):
    """해외결제일자조회[해외주식-017]."""

    # 해외결제일자조회 API입니다.

    PATH = "/uapi/overseas-stock/v1/quotations/countries-holiday"
    METHOD = "GET"
    RESPONSE_TYPE = CountriesHolidayResponse
    TR_ID = "CTOS5011R"
