"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class DailyShortSaleRequest(KisBaseModel):
    """요청."""

    FID_INPUT_DATE_2: str  # 입력 날짜2 — ~ 누적
    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — 시장구분코드 (주식 J)
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목코드
    FID_INPUT_DATE_1: str  # 입력 날짜1 — 공백시 전체 (기간 ~)

class DailyShortSaleResponse_Output1Item(KisBaseModel):
    """nested item."""

    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    prdy_vol: str | None = None  # 전일 거래량

class DailyShortSaleResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자
    stck_clpr: str | None = None  # 주식 종가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    stnd_vol_smtn: str | None = None  # 기준 거래량 합계
    ssts_cntg_qty: str | None = None  # 공매도 체결 수량
    ssts_vol_rlim: str | None = None  # 공매도 거래량 비중
    acml_ssts_cntg_qty: str | None = None  # 누적 공매도 체결 수량
    acml_ssts_cntg_qty_rlim: str | None = None  # 누적 공매도 체결 수량 비중
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    stnd_tr_pbmn_smtn: str | None = None  # 기준 거래대금 합계
    ssts_tr_pbmn: str | None = None  # 공매도 거래 대금
    ssts_tr_pbmn_rlim: str | None = None  # 공매도 거래대금 비중
    acml_ssts_tr_pbmn: str | None = None  # 누적 공매도 거래 대금
    acml_ssts_tr_pbmn_rlim: str | None = None  # 누적 공매도 거래 대금 비중
    stck_oprc: str | None = None  # 주식 시가2
    stck_hgpr: str | None = None  # 주식 최고가
    stck_lwpr: str | None = None  # 주식 최저가
    avrg_prc: str | None = None  # 평균가격

class DailyShortSaleResponse(KisCommonResponse):
    """응답 본문."""

    output1: DailyShortSaleResponse_Output1Item | None = None  # 응답상세
    output2: list[DailyShortSaleResponse_Output2Item] = []  # 응답상세 — array

class DailyShortSaleExecutor(ApiExecutor[DailyShortSaleRequest, DailyShortSaleResponse]):
    """국내주식 공매도 일별추이[국내주식-134]."""

    PATH = "/uapi/domestic-stock/v1/quotations/daily-short-sale"
    METHOD = "GET"
    RESPONSE_TYPE = DailyShortSaleResponse
    TR_ID = "FHPST04830000"
