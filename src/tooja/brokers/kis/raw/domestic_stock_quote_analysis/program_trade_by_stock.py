"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class ProgramTradeByStockRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — KRX : J , NXT : NX, 통합 : UN
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목코드

class ProgramTradeByStockResponse_OutputItem(KisBaseModel):
    """nested item."""

    bsop_hour: str | None = None  # 영업 시간
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    whol_smtn_seln_vol: str | None = None  # 전체 합계 매도 거래량
    whol_smtn_shnu_vol: str | None = None  # 전체 합계 매수2 거래량
    whol_smtn_ntby_qty: str | None = None  # 전체 합계 순매수 수량
    whol_smtn_seln_tr_pbmn: str | None = None  # 전체 합계 매도 거래 대금
    whol_smtn_shnu_tr_pbmn: str | None = None  # 전체 합계 매수2 거래 대금
    whol_smtn_ntby_tr_pbmn: str | None = None  # 전체 합계 순매수 거래 대금
    whol_ntby_vol_icdc: str | None = None  # 전체 순매수 거래량 증감
    whol_ntby_tr_pbmn_icdc: str | None = None  # 전체 순매수 거래 대금 증감

class ProgramTradeByStockResponse(KisCommonResponse):
    """응답 본문."""

    output: list[ProgramTradeByStockResponse_OutputItem] = []  # 응답상세 — array

class ProgramTradeByStockExecutor(ApiExecutor[ProgramTradeByStockRequest, ProgramTradeByStockResponse]):
    """종목별 프로그램매매추이(체결)[v1_국내주식-044]."""

    # 국내주식 종목별 프로그램매매추이(체결) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0465] 종목별 프로그램 매매추이 화면(혹은 한국투자 MTS &gt; 국내 현재가 &gt; 기타수급 &gt; 프로그램) 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/program-trade-by-stock"
    METHOD = "GET"
    RESPONSE_TYPE = ProgramTradeByStockResponse
    TR_ID = "FHPPG04650101"
