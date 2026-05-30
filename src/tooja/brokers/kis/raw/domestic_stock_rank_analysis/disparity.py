"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class DisparityRequest(KisBaseModel):
    """요청."""

    fid_input_price_2: str  # 입력 가격2 — 입력값 없을때 전체 (~ 가격)
    fid_cond_mrkt_div_code: str  # 조건 시장 분류 코드 — 시장구분코드 (J:KRX, NX:NXT)
    fid_cond_scr_div_code: str  # 조건 화면 분류 코드 — Unique key( 20178 )
    fid_div_cls_code: str  # 분류 구분 코드 — 0: 전체, 1:관리종목, 2:투자주의, 3:투자경고, 4:투자위험예고, 5:투자위험, 6:보톧주, 7:우선주
    fid_rank_sort_cls_code: str  # 순위 정렬 구분 코드 — 0: 이격도상위순, 1:이격도하위순
    fid_hour_cls_code: str  # 시간 구분 코드 — 5:이격도5, 10:이격도10, 20:이격도20, 60:이격도60, 120:이격도120
    fid_input_iscd: str  # 입력 종목코드 — 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
    fid_trgt_cls_code: str  # 대상 구분 코드 — 0 : 전체
    fid_trgt_exls_cls_code: str  # 대상 제외 구분 코드 — 0 : 전체
    fid_input_price_1: str  # 입력 가격1 — 입력값 없을때 전체 (가격 ~)
    fid_vol_cnt: str  # 거래량 수 — 입력값 없을때 전체 (거래량 ~)

class DisparityResponse_OutputItem(KisBaseModel):
    """nested item."""

    mksc_shrn_iscd: str | None = None  # 유가증권 단축 종목코드
    data_rank: str | None = None  # 데이터 순위
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_ctrt: str | None = None  # 전일 대비율
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    acml_vol: str | None = None  # 누적 거래량
    d5_dsrt: str | None = None  # 5일 이격도
    d10_dsrt: str | None = None  # 10일 이격도
    d20_dsrt: str | None = None  # 20일 이격도
    d60_dsrt: str | None = None  # 60일 이격도
    d120_dsrt: str | None = None  # 120일 이격도

class DisparityResponse(KisCommonResponse):
    """응답 본문."""

    output: list[DisparityResponse_OutputItem] = []  # 응답상세 — array

class DisparityExecutor(ApiExecutor[DisparityRequest, DisparityResponse]):
    """국내주식 이격도 순위[v1_국내주식-095]."""

    # 국내주식 이격도 순위 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0178] 이격도 순위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 최대 30건 확인 가능하며, 다음 조회가 불가합니다. ※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다. 종목조건검색 API는 

    PATH = "/uapi/domestic-stock/v1/ranking/disparity"
    METHOD = "GET"
    RESPONSE_TYPE = DisparityResponse
    TR_ID = "FHPST01780000"
