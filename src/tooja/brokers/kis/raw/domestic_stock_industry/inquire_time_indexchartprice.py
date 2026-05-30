"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireTimeIndexchartpriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # FID 조건 시장 분류 코드 — U
    FID_ETC_CLS_CODE: str  # FID 기타 구분 코드 — 0: 기본 1:장마감,시간외 제외
    FID_INPUT_ISCD: str  # FID 입력 종목코드 — 0001 : 종합 0002 : 대형주 ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조)
    FID_INPUT_HOUR_1: str  # FID 입력 시간1 — 30, 60 -> 1분, 600-> 10분, 3600 -> 1시간
    FID_PW_DATA_INCU_YN: str  # FID 과거 데이터 포함 여부 — Y (과거) / N (당일)

class InquireTimeIndexchartpriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    bstp_nmix_prdy_vrss: str | None = None  # 업종 지수 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    bstp_nmix_prdy_ctrt: str | None = None  # 업종 지수 전일 대비율
    prdy_nmix: str | None = None  # 전일 지수
    acml_vol: str | None = None  # 누적 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    bstp_nmix_prpr: str | None = None  # 업종 지수 현재가
    bstp_cls_code: str | None = None  # 업종 구분 코드
    prdy_vol: str | None = None  # 전일 거래량
    bstp_nmix_oprc: str | None = None  # 업종 지수 시가2
    bstp_nmix_hgpr: str | None = None  # 업종 지수 최고가
    bstp_nmix_lwpr: str | None = None  # 업종 지수 최저가
    futs_prdy_oprc: str | None = None  # 선물 전일 시가
    futs_prdy_hgpr: str | None = None  # 선물 전일 최고가
    futs_prdy_lwpr: str | None = None  # 선물 전일 최저가

class InquireTimeIndexchartpriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자
    stck_cntg_hour: str | None = None  # 주식 체결 시간
    bstp_nmix_prpr: str | None = None  # 업종 지수 현재가
    bstp_nmix_oprc: str | None = None  # 업종 지수 시가2
    bstp_nmix_hgpr: str | None = None  # 업종 지수 최고가
    bstp_nmix_lwpr: str | None = None  # 업종 지수 최저가
    cntg_vol: str | None = None  # 체결 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금

class InquireTimeIndexchartpriceResponse(KisCommonResponse):
    """응답 본문."""

    Output1: list[InquireTimeIndexchartpriceResponse_Output1Item] = []  # 응답상세
    Output2: InquireTimeIndexchartpriceResponse_Output2Item | None = None  # 응답상세2 — array

class InquireTimeIndexchartpriceExecutor(ApiExecutor[InquireTimeIndexchartpriceRequest, InquireTimeIndexchartpriceResponse]):
    """업종 분봉조회[v1_국내주식-045]."""

    # 업종 분봉조회 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0350] 업종 종합차트 화면의 분봉기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 실전계좌의 경우, 한 번의 호출에 최대 102건까지 확인 가능합니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-time-indexchartprice"
    METHOD = "GET"
    RESPONSE_TYPE = InquireTimeIndexchartpriceResponse
    TR_ID = "FHKUP03500200"
