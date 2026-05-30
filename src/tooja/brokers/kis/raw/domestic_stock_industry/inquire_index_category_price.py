"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireIndexCategoryPriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # FID 조건 시장 분류 코드 — 시장구분코드 (업종 U)
    FID_INPUT_ISCD: str  # FID 입력 종목코드 — 코스피(0001), 코스닥(1001), 코스피200(2001) ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조)
    FID_COND_SCR_DIV_CODE: str  # FID 조건 화면 분류 코드 — Unique key( 20214 )
    FID_MRKT_CLS_CODE: str  # FID 시장 구분 코드 — 시장구분코드(K:거래소, Q:코스닥, K2:코스피200)
    FID_BLNG_CLS_CODE: str  # FID 소속 구분 코드 — 시장구분코드에 따라 아래와 같이 입력 시장구분코드(K:거래소) 0:전업종, 1:기타구분, 2:자본금구분 3:상업별구분 시장구분코드(Q:코스닥) 0:전업종, 1:기타구분, 2:벤처구분 3:일반구분 시장구분코드(K2:코스닥) 0

class InquireIndexCategoryPriceResponse_Output1Item(KisBaseModel):
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

class InquireIndexCategoryPriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    bstp_cls_code: str | None = None  # 업종 구분 코드
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    bstp_nmix_prpr: str | None = None  # 업종 지수 현재가
    bstp_nmix_prdy_vrss: str | None = None  # 업종 지수 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    bstp_nmix_prdy_ctrt: str | None = None  # 업종 지수 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    acml_vol_rlim: str | None = None  # 누적 거래량 비중
    acml_tr_pbmn_rlim: str | None = None  # 누적 거래 대금 비중

class InquireIndexCategoryPriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireIndexCategoryPriceResponse_Output1Item | None = None  # 응답상세1
    output2: list[InquireIndexCategoryPriceResponse_Output2Item] = []  # 응답상세2 — array

class InquireIndexCategoryPriceExecutor(ApiExecutor[InquireIndexCategoryPriceRequest, InquireIndexCategoryPriceResponse]):
    """국내업종 구분별전체시세[v1_국내주식-066]."""

    # 국내업종 구분별전체시세 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0214] 업종 전체시세 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-index-category-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquireIndexCategoryPriceResponse
    TR_ID = "FHPUP02140000"
