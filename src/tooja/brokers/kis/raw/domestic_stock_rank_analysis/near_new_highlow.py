"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class NearNewHighlowRequest(KisBaseModel):
    """요청."""

    fid_aply_rang_vol: str  # 적용 범위 거래량 — 0: 전체, 100: 100주 이상
    fid_cond_mrkt_div_code: str  # 조건 시장 분류 코드 — 시장구분코드 (주식 J)
    fid_cond_scr_div_code: str  # 조건 화면 분류 코드 — Unique key(20187)
    fid_div_cls_code: str  # 분류 구분 코드 — 0:전체, 1:관리종목, 2:투자주의, 3:투자경고
    fid_input_cnt_1: str  # 입력 수1 — 괴리율 최소
    fid_input_cnt_2: str  # 입력 수2 — 괴리율 최대
    fid_prc_cls_code: str  # 가격 구분 코드 — 0:신고근접, 1:신저근접
    fid_input_iscd: str  # 입력 종목코드 — 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
    fid_trgt_cls_code: str  # 대상 구분 코드 — 0: 전체
    fid_trgt_exls_cls_code: str  # 대상 제외 구분 코드 — 0:전체, 1:관리종목, 2:투자주의, 3:투자경고, 4:투자위험예고, 5:투자위험, 6:보통주, 7:우선주
    fid_aply_rang_prc_1: str  # 적용 범위 가격1 — 가격 ~
    fid_aply_rang_prc_2: str  # 적용 범위 가격2 — ~ 가격

class NearNewHighlowResponse_OutputItem(KisBaseModel):
    """nested item."""

    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    mksc_shrn_iscd: str | None = None  # 유가증권 단축 종목코드
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_vrss: str | None = None  # 전일 대비
    prdy_ctrt: str | None = None  # 전일 대비율
    askp: str | None = None  # 매도호가
    askp_rsqn1: str | None = None  # 매도호가 잔량1
    bidp: str | None = None  # 매수호가
    bidp_rsqn1: str | None = None  # 매수호가 잔량1
    acml_vol: str | None = None  # 누적 거래량
    new_hgpr: str | None = None  # 신 최고가
    hprc_near_rate: str | None = None  # 고가 근접 비율
    new_lwpr: str | None = None  # 신 최저가
    lwpr_near_rate: str | None = None  # 저가 근접 비율
    stck_sdpr: str | None = None  # 주식 기준가

class NearNewHighlowResponse(KisCommonResponse):
    """응답 본문."""

    output: list[NearNewHighlowResponse_OutputItem] = []  # 응답상세 — array

class NearNewHighlowExecutor(ApiExecutor[NearNewHighlowRequest, NearNewHighlowResponse]):
    """국내주식 신고/신저근접종목 상위[v1_국내주식-105]."""

    # 국내주식 신고/신저근접종목 상위 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0187] 신고/신저 근접종목 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 최대 30건 확인 가능하며, 다음 조회가 불가합니다. ※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다. 종목

    PATH = "/uapi/domestic-stock/v1/ranking/near-new-highlow"
    METHOD = "GET"
    RESPONSE_TYPE = NearNewHighlowResponse
    TR_ID = "FHPST01870000"
