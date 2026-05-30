"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireElwPriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — W
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목번호 (6자리)

class InquireElwPriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    elw_shrn_iscd: str | None = None  # ELW 단축 종목코드
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    elw_prpr: str | None = None  # ELW 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    prdy_vrss_vol_rate: str | None = None  # 전일 대비 거래량 비율
    unas_shrn_iscd: str | None = None  # 기초자산 단축 종목코드
    unas_isnm: str | None = None  # 기초자산 종목명
    unas_prpr: str | None = None  # 기초자산 현재가
    unas_prdy_vrss: str | None = None  # 기초자산 전일 대비
    unas_prdy_vrss_sign: str | None = None  # 기초자산 전일 대비 부호
    unas_prdy_ctrt: str | None = None  # 기초자산 전일 대비율
    bidp: str | None = None  # 매수호가
    askp: str | None = None  # 매도호가
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    vol_tnrt: str | None = None  # 거래량 회전율
    elw_oprc: str | None = None  # ELW 시가2
    elw_hgpr: str | None = None  # ELW 최고가
    elw_lwpr: str | None = None  # ELW 최저가
    stck_prdy_clpr: str | None = None  # 주식 전일 종가
    hts_thpr: str | None = None  # HTS 이론가
    dprt: str | None = None  # 괴리율
    atm_cls_name: str | None = None  # ATM 구분 명
    hts_ints_vltl: str | None = None  # HTS 내재 변동성
    acpr: str | None = None  # 행사가
    pvt_scnd_dmrs_prc: str | None = None  # 피벗 2차 디저항 가격
    pvt_frst_dmrs_prc: str | None = None  # 피벗 1차 디저항 가격
    pvt_pont_val: str | None = None  # 피벗 포인트 값
    pvt_frst_dmsp_prc: str | None = None  # 피벗 1차 디지지 가격
    pvt_scnd_dmsp_prc: str | None = None  # 피벗 2차 디지지 가격
    dmsp_val: str | None = None  # 디지지 값
    dmrs_val: str | None = None  # 디저항 값
    elw_sdpr: str | None = None  # ELW 기준가
    apprch_rate: str | None = None  # 접근도
    tick_conv_prc: str | None = None  # 틱환산가
    invt_epmd_cntt: str | None = None  # 투자 유의 내용

class InquireElwPriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[InquireElwPriceResponse_Output1Item] = []  # 응답상세 — array

class InquireElwPriceExecutor(ApiExecutor[InquireElwPriceRequest, InquireElwPriceResponse]):
    """ELW 현재가 시세[v1_국내주식-014]."""

    # ELW 현재가 시세 API입니다. ELW 관련 정보를 얻을 수 있습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-elw-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquireElwPriceResponse
    TR_ID = "FHKEW15010000"
