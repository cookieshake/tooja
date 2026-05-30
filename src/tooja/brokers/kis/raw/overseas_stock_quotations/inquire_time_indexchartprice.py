"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireTimeIndexchartpriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — N 해외지수 X 환율 KX 원화환율
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목번호(ex. TSLA)
    FID_HOUR_CLS_CODE: str  # 시간 구분 코드 — 0: 정규장, 1: 시간외
    FID_PW_DATA_INCU_YN: str  # 과거 데이터 포함 여부 — Y/N

class InquireTimeIndexchartpriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    ovrs_nmix_prdy_vrss: str | None = None  # 해외 지수 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    prdy_ctrt: str | None = None  # 전일 대비율
    ovrs_nmix_prdy_clpr: str | None = None  # 해외 지수 전일 종가
    acml_vol: str | None = None  # 누적 거래량
    ovrs_nmix_prpr: str | None = None  # 해외 지수 현재가
    stck_shrn_iscd: str | None = None  # 주식 단축 종목코드
    ovrs_prod_oprc: str | None = None  # 해외 상품 시가2 — 시가
    ovrs_prod_hgpr: str | None = None  # 해외 상품 최고가 — 최고가
    ovrs_prod_lwpr: str | None = None  # 해외 상품 최저가 — 최저가

class InquireTimeIndexchartpriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자 — 영업 일자
    stck_cntg_hour: str | None = None  # 주식 체결 시간 — 체결 시간
    optn_prpr: str | None = None  # 옵션 현재가 — 현재가
    optn_oprc: str | None = None  # 옵션 시가2 — 시가
    optn_hgpr: str | None = None  # 옵션 최고가 — 최고가
    optn_lwpr: str | None = None  # 옵션 최저가 — 최저가
    cntg_vol: str | None = None  # 체결 거래량

class InquireTimeIndexchartpriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireTimeIndexchartpriceResponse_Output1Item | None = None  # 응답상세
    output2: list[InquireTimeIndexchartpriceResponse_Output2Item] = []  # 응답상세2 — array

class InquireTimeIndexchartpriceExecutor(ApiExecutor[InquireTimeIndexchartpriceRequest, InquireTimeIndexchartpriceResponse]):
    """해외지수분봉조회[v1_해외주식-031]."""

    # 해외지수분봉조회 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0303] 해외지수 종합차트 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 실전계좌의 경우, 한 번의 호출에 최대 102건까지 확인 가능합니다.

    PATH = "/uapi/overseas-price/v1/quotations/inquire-time-indexchartprice"
    METHOD = "GET"
    RESPONSE_TYPE = InquireTimeIndexchartpriceResponse
    TR_ID = "FHKST03030200"
