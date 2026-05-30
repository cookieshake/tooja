"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireDailyPriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — J:KRX, NX:NXT, UN:통합
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목코드 (ex 005930 삼성전자)
    FID_PERIOD_DIV_CODE: str  # 기간 분류 코드 — 'D : (일)최근 30거래일 W : (주)최근 30주 M : (월)최근 30개월'
    FID_ORG_ADJ_PRC: str  # 수정주가 원주가 가격 — '0 : 수정주가미반영 1 : 수정주가반영 * 수정주가는 액면분할/액면병합 등 권리 발생 시 과거 시세를 현재 주가에 맞게 보정한 가격'

class InquireDailyPriceResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자
    stck_oprc: str | None = None  # 주식 시가2
    stck_hgpr: str | None = None  # 주식 최고가
    stck_lwpr: str | None = None  # 주식 최저가
    stck_clpr: str | None = None  # 주식 종가
    acml_vol: str | None = None  # 누적 거래량
    prdy_vrss_vol_rate: str | None = None  # 전일 대비 거래량 비율 — 13(8.4)
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율 — 11(8.2)
    hts_frgn_ehrt: str | None = None  # HTS 외국인 소진율 — 11(8.2)
    frgn_ntby_qty: str | None = None  # 외국인 순매수 수량
    flng_cls_code: str | None = None  # 락 구분 코드 — '01 : 권리락 02 : 배당락 03 : 분배락 04 : 권배락 05 : 중간(분기)배당락 06 : 권리중간배당락 07 : 권리분기배당락'
    acml_prtt_rate: str | None = None  # 누적 분할 비율 — 13(8.4)

class InquireDailyPriceResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InquireDailyPriceResponse_OutputItem] = []  # 응답상세 — array

class InquireDailyPriceExecutor(ApiExecutor[InquireDailyPriceRequest, InquireDailyPriceResponse]):
    """주식현재가 일자별[v1_국내주식-010]."""

    # 주식현재가 일자별 API입니다. 일/주/월별 주가를 확인할 수 있으며 최근 30일(주,별)로 제한되어 있습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-daily-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquireDailyPriceResponse
    TR_ID = "FHKST01010400"
