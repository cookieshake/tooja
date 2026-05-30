"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class FluctuationRequest(KisBaseModel):
    """요청."""

    fid_rsfl_rate2: str  # 등락 비율2 — 공백 입력 시 전체 (~ 비율
    fid_cond_mrkt_div_code: str  # 조건 시장 분류 코드 — 시장구분코드 (J:KRX, NX:NXT)
    fid_cond_scr_div_code: str  # 조건 화면 분류 코드 — Unique key( 20170 )
    fid_input_iscd: str  # 입력 종목코드 — 0000(전체) 코스피(0001), 코스닥(1001), 코스피200(2001)
    fid_rank_sort_cls_code: str  # 순위 정렬 구분 코드 — 0:상승율순 1:하락율순 2:시가대비상승율 3:시가대비하락율 4:변동율
    fid_input_cnt_1: str  # 입력 수1 — 0:전체 , 누적일수 입력
    fid_prc_cls_code: str  # 가격 구분 코드 — 'fid_rank_sort_cls_code :0 상승율 순일때 (0:저가대비, 1:종가대비) fid_rank_sort_cls_code :1 하락율 순일때 (0:고가대비, 1:종가대비) fid_rank_sort_cls_code : 기
    fid_input_price_1: str  # 입력 가격1 — 공백 입력 시 전체 (가격 ~)
    fid_input_price_2: str  # 입력 가격2 — 공백 입력 시 전체 (~ 가격)
    fid_vol_cnt: str  # 거래량 수 — 공백 입력 시 전체 (거래량 ~)
    fid_trgt_cls_code: str  # 대상 구분 코드 — 0:전체
    fid_trgt_exls_cls_code: str  # 대상 제외 구분 코드 — 0:전체
    fid_div_cls_code: str  # 분류 구분 코드 — 0:전체
    fid_rsfl_rate1: str  # 등락 비율1 — 공백 입력 시 전체 (비율 ~)

class FluctuationResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_shrn_iscd: str | None = None  # 주식 단축 종목코드
    data_rank: str | None = None  # 데이터 순위
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    stck_hgpr: str | None = None  # 주식 최고가
    hgpr_hour: str | None = None  # 최고가 시간
    acml_hgpr_date: str | None = None  # 누적 최고가 일자
    stck_lwpr: str | None = None  # 주식 최저가
    lwpr_hour: str | None = None  # 최저가 시간
    acml_lwpr_date: str | None = None  # 누적 최저가 일자
    lwpr_vrss_prpr_rate: str | None = None  # 최저가 대비 현재가 비율
    dsgt_date_clpr_vrss_prpr_rate: str | None = None  # 지정 일자 종가 대비 현재가 비
    cnnt_ascn_dynu: str | None = None  # 연속 상승 일수
    hgpr_vrss_prpr_rate: str | None = None  # 최고가 대비 현재가 비율
    cnnt_down_dynu: str | None = None  # 연속 하락 일수
    oprc_vrss_prpr_sign: str | None = None  # 시가2 대비 현재가 부호
    oprc_vrss_prpr: str | None = None  # 시가2 대비 현재가
    oprc_vrss_prpr_rate: str | None = None  # 시가2 대비 현재가 비율
    prd_rsfl: str | None = None  # 기간 등락
    prd_rsfl_rate: str | None = None  # 기간 등락 비율

class FluctuationResponse(KisCommonResponse):
    """응답 본문."""

    output: list[FluctuationResponse_OutputItem] = []  # 응답상세 — array

class FluctuationExecutor(ApiExecutor[FluctuationRequest, FluctuationResponse]):
    """국내주식 등락률 순위[v1_국내주식-088]."""

    # 국내주식 등락률 순위 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0170] 등락률 순위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 최대 30건 확인 가능하며, 다음 조회가 불가합니다. ※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다. 종목조건검색 API는 

    PATH = "/uapi/domestic-stock/v1/ranking/fluctuation"
    METHOD = "GET"
    RESPONSE_TYPE = FluctuationResponse
    TR_ID = "FHPST01700000"
