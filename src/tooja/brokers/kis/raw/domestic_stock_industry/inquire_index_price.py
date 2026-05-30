"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireIndexPriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # FID 조건 시장 분류 코드 — 업종(U)
    FID_INPUT_ISCD: str  # FID 입력 종목코드 — 코스피(0001), 코스닥(1001), 코스피200(2001) ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조)

class InquireIndexPriceResponse_OutputItem(KisBaseModel):
    """nested item."""

    bstp_nmix_prpr: str | None = None  # 업종 지수 현재가
    bstp_nmix_prdy_vrss: str | None = None  # 업종 지수 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    bstp_nmix_prdy_ctrt: str | None = None  # 업종 지수 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    prdy_vol: str | None = None  # 전일 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    prdy_tr_pbmn: str | None = None  # 전일 거래 대금
    bstp_nmix_oprc: str | None = None  # 업종 지수 시가2
    prdy_nmix_vrss_nmix_oprc: str | None = None  # 전일 지수 대비 지수 시가2
    oprc_vrss_prpr_sign: str | None = None  # 시가2 대비 현재가 부호
    bstp_nmix_oprc_prdy_ctrt: str | None = None  # 업종 지수 시가2 전일 대비율
    bstp_nmix_hgpr: str | None = None  # 업종 지수 최고가
    prdy_nmix_vrss_nmix_hgpr: str | None = None  # 전일 지수 대비 지수 최고가
    hgpr_vrss_prpr_sign: str | None = None  # 최고가 대비 현재가 부호
    bstp_nmix_hgpr_prdy_ctrt: str | None = None  # 업종 지수 최고가 전일 대비율
    bstp_nmix_lwpr: str | None = None  # 업종 지수 최저가
    prdy_clpr_vrss_lwpr: str | None = None  # 전일 종가 대비 최저가
    lwpr_vrss_prpr_sign: str | None = None  # 최저가 대비 현재가 부호
    prdy_clpr_vrss_lwpr_rate: str | None = None  # 전일 종가 대비 최저가 비율
    ascn_issu_cnt: str | None = None  # 상승 종목 수
    uplm_issu_cnt: str | None = None  # 상한 종목 수
    stnr_issu_cnt: str | None = None  # 보합 종목 수
    down_issu_cnt: str | None = None  # 하락 종목 수
    lslm_issu_cnt: str | None = None  # 하한 종목 수
    dryy_bstp_nmix_hgpr: str | None = None  # 연중업종지수최고가
    dryy_hgpr_vrss_prpr_rate: str | None = None  # 연중 최고가 대비 현재가 비율
    dryy_bstp_nmix_hgpr_date: str | None = None  # 연중업종지수최고가일자
    dryy_bstp_nmix_lwpr: str | None = None  # 연중업종지수최저가
    dryy_lwpr_vrss_prpr_rate: str | None = None  # 연중 최저가 대비 현재가 비율
    dryy_bstp_nmix_lwpr_date: str | None = None  # 연중업종지수최저가일자
    total_askp_rsqn: str | None = None  # 총 매도호가 잔량
    total_bidp_rsqn: str | None = None  # 총 매수호가 잔량
    seln_rsqn_rate: str | None = None  # 매도 잔량 비율
    shnu_rsqn_rate: str | None = None  # 매수2 잔량 비율
    ntby_rsqn: str | None = None  # 순매수 잔량

class InquireIndexPriceResponse(KisCommonResponse):
    """응답 본문."""

    output: InquireIndexPriceResponse_OutputItem | None = None  # 응답상세1

class InquireIndexPriceExecutor(ApiExecutor[InquireIndexPriceRequest, InquireIndexPriceResponse]):
    """국내업종 현재지수[v1_국내주식-063]."""

    # 국내업종 현재지수 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0210] 업종 현재지수 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-index-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquireIndexPriceResponse
    TR_ID = "FHPUP02100000"
