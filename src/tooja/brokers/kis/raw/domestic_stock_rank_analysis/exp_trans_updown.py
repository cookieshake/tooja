"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class ExpTransUpdownRequest(KisBaseModel):
    """요청."""

    fid_rank_sort_cls_code: str  # 순위 정렬 구분 코드 — 0:상승률1:상승폭2:보합3:하락율4:하락폭5:체결량6:거래대금
    fid_cond_mrkt_div_code: str  # 조건 시장 분류 코드 — 시장구분코드 (주식 J)
    fid_cond_scr_div_code: str  # 조건 화면 분류 코드 — Unique key(20182)
    fid_input_iscd: str  # 입력 종목코드 — 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
    fid_div_cls_code: str  # 분류 구분 코드 — 0:전체 1:보통주 2:우선주
    fid_aply_rang_prc_1: str  # 적용 범위 가격1 — 입력값 없을때 전체 (가격 ~)
    fid_vol_cnt: str  # 거래량 수 — 입력값 없을때 전체 (거래량 ~)
    fid_pbmn: str  # 거래대금 — 입력값 없을때 전체 (거래대금 ~) 천원단위
    fid_blng_cls_code: str  # 소속 구분 코드 — 0: 전체
    fid_mkop_cls_code: str  # 장운영 구분 코드 — 0:장전예상1:장마감예상

class ExpTransUpdownResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_shrn_iscd: str | None = None  # 주식 단축 종목코드
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    stck_sdpr: str | None = None  # 주식 기준가
    seln_rsqn: str | None = None  # 매도 잔량
    askp: str | None = None  # 매도호가
    bidp: str | None = None  # 매수호가
    shnu_rsqn: str | None = None  # 매수2 잔량
    cntg_vol: str | None = None  # 체결 거래량
    antc_tr_pbmn: str | None = None  # 체결 거래대금
    total_askp_rsqn: str | None = None  # 총 매도호가 잔량
    total_bidp_rsqn: str | None = None  # 총 매수호가 잔량

class ExpTransUpdownResponse(KisCommonResponse):
    """응답 본문."""

    output: list[ExpTransUpdownResponse_OutputItem] = []  # 응답상세 — array

class ExpTransUpdownExecutor(ApiExecutor[ExpTransUpdownRequest, ExpTransUpdownResponse]):
    """국내주식 예상체결 상승/하락상위[v1_국내주식-103]."""

    # 국내주식 예상체결 상승/하락상위 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0182] 예상체결 상승/하락상위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 최대 30건 확인 가능하며, 다음 조회가 불가합니다. ※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다. 

    PATH = "/uapi/domestic-stock/v1/ranking/exp-trans-updown"
    METHOD = "GET"
    RESPONSE_TYPE = ExpTransUpdownResponse
    TR_ID = "FHPST01820000"
