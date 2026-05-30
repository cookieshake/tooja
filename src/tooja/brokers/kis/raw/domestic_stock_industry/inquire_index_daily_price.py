"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireIndexDailyPriceRequest(KisBaseModel):
    """요청."""

    FID_PERIOD_DIV_CODE: str  # FID 기간 분류 코드 — 일/주/월 구분코드 ( D:일별 , W:주별, M:월별 )
    FID_COND_MRKT_DIV_CODE: str  # FID 조건 시장 분류 코드 — 시장구분코드 (업종 U)
    FID_INPUT_ISCD: str  # FID 입력 종목코드 — 코스피(0001), 코스닥(1001), 코스피200(2001) ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조)
    FID_INPUT_DATE_1: str  # FID 입력 날짜1 — 입력 날짜(ex. 20240223)

class InquireIndexDailyPriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    bstp_nmix_prpr: str | None = None  # 업종 지수 현재가
    bstp_nmix_prdy_vrss: str | None = None  # 업종 지수 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    bstp_nmix_prdy_ctrt: str | None = None  # 업종 지수 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    bstp_nmix_oprc: str | None = None  # 업종 지수 시가2
    bstp_nmix_hgpr: str | None = None  # 업종 지수 최고가
    bstp_nmix_lwpr: str | None = None  # 업종 지수 최저가
    prdy_vol: str | None = None  # 전일 거래량
    ascn_issu_cnt: str | None = None  # 상승 종목 수
    down_issu_cnt: str | None = None  # 하락 종목 수
    stnr_issu_cnt: str | None = None  # 보합 종목 수
    uplm_issu_cnt: str | None = None  # 상한 종목 수
    lslm_issu_cnt: str | None = None  # 하한 종목 수
    prdy_tr_pbmn: str | None = None  # 전일 거래 대금
    dryy_bstp_nmix_hgpr_date: str | None = None  # 연중업종지수최고가일자
    dryy_bstp_nmix_hgpr: str | None = None  # 연중업종지수최고가
    dryy_bstp_nmix_lwpr: str | None = None  # 연중업종지수최저가
    dryy_bstp_nmix_lwpr_date: str | None = None  # 연중업종지수최저가일자

class InquireIndexDailyPriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자
    bstp_nmix_prpr: str | None = None  # 업종 지수 현재가
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    bstp_nmix_prdy_vrss: str | None = None  # 업종 지수 전일 대비
    bstp_nmix_prdy_ctrt: str | None = None  # 업종 지수 전일 대비율
    bstp_nmix_oprc: str | None = None  # 업종 지수 시가2
    bstp_nmix_hgpr: str | None = None  # 업종 지수 최고가
    bstp_nmix_lwpr: str | None = None  # 업종 지수 최저가
    acml_vol_rlim: str | None = None  # 누적 거래량 비중
    acml_vol: str | None = None  # 누적 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    invt_new_psdg: str | None = None  # 투자 신 심리도
    d20_dsrt: str | None = None  # 20일 이격도

class InquireIndexDailyPriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireIndexDailyPriceResponse_Output1Item | None = None  # 응답상세1
    output2: list[InquireIndexDailyPriceResponse_Output2Item] = []  # 응답상세2 — array

class InquireIndexDailyPriceExecutor(ApiExecutor[InquireIndexDailyPriceRequest, InquireIndexDailyPriceResponse]):
    """국내업종 일자별지수[v1_국내주식-065]."""

    # 국내업종 일자별지수 API입니다. 한 번의 조회에 100건까지 확인 가능합니다. 한국투자 HTS(eFriend Plus) &gt; [0212] 업종 일자별지수 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-index-daily-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquireIndexDailyPriceResponse
    TR_ID = "FHPUP02120000"
