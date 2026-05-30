"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class ProgramTradeByStockDailyRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — KRX : J , NXT : NX, 통합 : UN
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목코드
    FID_INPUT_DATE_1: str  # 입력 날짜1 — 기준일 (ex 0020240308), 미입력시 당일부터 조회

class ProgramTradeByStockDailyResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자
    stck_clpr: str | None = None  # 주식 종가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    whol_smtn_seln_vol: str | None = None  # 전체 합계 매도 거래량
    whol_smtn_shnu_vol: str | None = None  # 전체 합계 매수2 거래량
    whol_smtn_ntby_qty: str | None = None  # 전체 합계 순매수 수량
    whol_smtn_seln_tr_pbmn: str | None = None  # 전체 합계 매도 거래 대금
    whol_smtn_shnu_tr_pbmn: str | None = None  # 전체 합계 매수2 거래 대금
    whol_smtn_ntby_tr_pbmn: str | None = None  # 전체 합계 순매수 거래 대금
    whol_ntby_vol_icdc: str | None = None  # 전체 순매수 거래량 증감
    whol_ntby_tr_pbmn_icdc2: str | None = None  # 전체 순매수 거래 대금 증감2

class ProgramTradeByStockDailyResponse(KisCommonResponse):
    """응답 본문."""

    output: list[ProgramTradeByStockDailyResponse_OutputItem] = []  # 응답상세 — array

class ProgramTradeByStockDailyExecutor(ApiExecutor[ProgramTradeByStockDailyRequest, ProgramTradeByStockDailyResponse]):
    """종목별 프로그램매매추이(일별) [국내주식-113]."""

    # 국내주식 종목별 프로그램매매추이(일별) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0465] 종목별 프로그램 매매추이 화면(혹은 한국투자 MTS &gt; 국내 현재가 &gt; 기타수급 &gt; 프로그램) 의 "일자별" 클릭 시 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/program-trade-by-stock-daily"
    METHOD = "GET"
    RESPONSE_TYPE = ProgramTradeByStockDailyResponse
    TR_ID = "FHPPG04650201"
