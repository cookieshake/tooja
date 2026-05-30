"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireTimeFuopchartpriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # FID 조건 시장 분류 코드 — F: 지수선물, O:지수옵션 JF: 주식선물, JO:주식옵션, CF: 상품선물(금), 금리선물(국채), 통화선물(달러) CM: 야간선물, EU: 야간옵션
    FID_INPUT_ISCD: str  # FID 입력 종목코드 — 종목번호 (지수선물:6자리, 지수옵션 9자리)
    FID_HOUR_CLS_CODE: str  # FID 시간 구분 코드 — FID 시간 구분 코드(30: 30초, 60: 1분, 3600: 1시간)
    FID_PW_DATA_INCU_YN: str  # FID 과거 데이터 포함 여부 — Y(과거) / N (당일)
    FID_FAKE_TICK_INCU_YN: str  # FID 허봉 포함 여부 — N으로 입력
    FID_INPUT_DATE_1: str  # FID 입력 날짜1 — 입력 날짜 기준으로 이전 기간 조회(YYYYMMDD) ex) 20230908 입력 시, 2023년 9월 8일부터 일자 역순으로 조회
    FID_INPUT_HOUR_1: str  # FID 입력 시간1 — 입력 시간 기준으로 이전 시간 조회(HHMMSS) ex) 093000 입력 시, 오전 9시 30분부터 역순으로 분봉 조회 * CM(야간선물), EU(야간옵션)인 경우, 자정 이후 시간은 +24시간으로 입력 ex) 253000 입

class InquireTimeFuopchartpriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    futs_prdy_vrss: str | None = None  # 선물 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    futs_prdy_ctrt: str | None = None  # 선물 전일 대비율
    futs_prdy_clpr: str | None = None  # 선물 전일 종가
    prdy_nmix: str | None = None  # 전일 지수
    acml_vol: str | None = None  # 누적 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    futs_prpr: str | None = None  # 선물 현재가
    futs_shrn_iscd: str | None = None  # 선물 단축 종목코드
    prdy_vol: str | None = None  # 전일 거래량
    futs_mxpr: str | None = None  # 선물 상한가
    futs_llam: str | None = None  # 선물 하한가
    futs_oprc: str | None = None  # 선물 시가2
    futs_hgpr: str | None = None  # 선물 최고가
    futs_lwpr: str | None = None  # 선물 최저가
    futs_prdy_oprc: str | None = None  # 선물 전일 시가
    futs_prdy_hgpr: str | None = None  # 선물 전일 최고가
    futs_prdy_lwpr: str | None = None  # 선물 전일 최저가
    futs_askp: str | None = None  # 선물 매도호가
    futs_bidp: str | None = None  # 선물 매수호가
    basis: str | None = None  # 베이시스
    kospi200_nmix: str | None = None  # KOSPI200 지수
    kospi200_prdy_vrss: str | None = None  # KOSPI200 전일 대비
    kospi200_prdy_ctrt: str | None = None  # KOSPI200 전일 대비율
    kospi200_prdy_vrss_sign: str | None = None  # KOSPI200 전일 대비 부호
    hts_otst_stpl_qty: str | None = None  # HTS 미결제 약정 수량
    otst_stpl_qty_icdc: str | None = None  # 미결제 약정 수량 증감
    tday_rltv: str | None = None  # 당일 체결강도
    hts_thpr: str | None = None  # HTS 이론가
    dprt: str | None = None  # 괴리율

class InquireTimeFuopchartpriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자
    stck_cntg_hour: str | None = None  # 주식 체결 시간 — CM(야간선물), EU(야간옵션)인 경우, 자정 이후 시간은 +24시간으로 표시 ex) "260000"인 경우, 오전 4시를 의미
    futs_prpr: str | None = None  # 선물 현재가
    futs_oprc: str | None = None  # 선물 시가2
    futs_hgpr: str | None = None  # 선물 최고가
    futs_lwpr: str | None = None  # 선물 최저가
    cntg_vol: str | None = None  # 체결 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금

class InquireTimeFuopchartpriceResponse(KisCommonResponse):
    """응답 본문."""

    Output1: list[InquireTimeFuopchartpriceResponse_Output1Item] = []  # 응답상세
    Output2: InquireTimeFuopchartpriceResponse_Output2Item | None = None  # 응답상세2 — array

class InquireTimeFuopchartpriceExecutor(ApiExecutor[InquireTimeFuopchartpriceRequest, InquireTimeFuopchartpriceResponse]):
    """선물옵션 분봉조회[v1_국내선물-012]."""

    # 선물옵션 분봉조회 API입니다. 실전계좌의 경우, 한 번의 호출에 최대 102건까지 확인 가능하며, FID_INPUT_DATE_1(입력날짜), FID_INPUT_HOUR_1(입력시간)을 이용하여 다음조회 가능합니다.

    PATH = "/uapi/domestic-futureoption/v1/quotations/inquire-time-fuopchartprice"
    METHOD = "GET"
    RESPONSE_TYPE = InquireTimeFuopchartpriceResponse
    TR_ID = "FHKIF03020200"
