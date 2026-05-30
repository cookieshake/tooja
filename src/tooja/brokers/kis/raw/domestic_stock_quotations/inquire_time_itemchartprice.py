"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireTimeItemchartpriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — J:KRX, NX:NXT, UN:통합
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목코드 (ex 005930 삼성전자)
    FID_INPUT_HOUR_1: str  # 입력 시간1 — 입력시간
    FID_PW_DATA_INCU_YN: str  # 과거 데이터 포함 여부
    FID_ETC_CLS_CODE: str  # 기타 구분 코드

class InquireTimeItemchartpriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    prdy_vrss: str | None = None  # 전일 대비 — 전일 대비 변동 (+-변동차이)
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율 — 소수점 두자리까지 제공
    stck_prdy_clpr: str | None = None  # 전일대비 종가
    acml_vol: str | None = None  # 누적 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래대금
    hts_kor_isnm: str | None = None  # 한글 종목명 — 한글 종목명 (HTS 기준)
    stck_prpr: str | None = None  # 주식 현재가

class InquireTimeItemchartpriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업일자
    stck_cntg_hour: str | None = None  # 주식 체결시간
    stck_prpr: str | None = None  # 주식 현재가
    stck_oprc: str | None = None  # 주식 시가
    stck_hgpr: str | None = None  # 주식 최고가
    stck_lwpr: str | None = None  # 주식 최저가
    cntg_vol: str | None = None  # 체결 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래대금

class InquireTimeItemchartpriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireTimeItemchartpriceResponse_Output1Item | None = None  # 응답상세
    output2: list[InquireTimeItemchartpriceResponse_Output2Item] = []  # 응답상세 — Array

class InquireTimeItemchartpriceExecutor(ApiExecutor[InquireTimeItemchartpriceRequest, InquireTimeItemchartpriceResponse]):
    """주식당일분봉조회[v1_국내주식-022]."""

    # 주식당일분봉조회 API입니다. 실전계좌/모의계좌의 경우, 한 번의 호출에 최대 30건까지 확인 가능합니다. ※ 당일 분봉 데이터만 제공됩니다. (전일자 분봉 미제공) ※ input &gt; FID_INPUT_HOUR_1 에 미래일시 입력 시에 현재가로 조회됩니다. ex) 오전 10시에 113000 입력 시에 오전 10시~11시30분 사이의 데이터가 오전 10시 값으로 조회됨 ※ output2의 첫번째 배열의 체결량(cntg_v

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice"
    METHOD = "GET"
    RESPONSE_TYPE = InquireTimeItemchartpriceResponse
    TR_ID = "FHKST03010200"
