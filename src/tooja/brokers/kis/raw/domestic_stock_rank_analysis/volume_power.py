"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class VolumePowerRequest(KisBaseModel):
    """요청."""

    fid_trgt_exls_cls_code: str  # 대상 제외 구분 코드 — 0 : 전체
    fid_cond_mrkt_div_code: str  # 조건 시장 분류 코드 — 시장구분코드 (J:KRX, NX:NXT)
    fid_cond_scr_div_code: str  # 조건 화면 분류 코드 — Unique key( 20168 )
    fid_input_iscd: str  # 입력 종목코드 — 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
    fid_div_cls_code: str  # 분류 구분 코드 — 0: 전체, 1: 보통주 2: 우선주
    fid_input_price_1: str  # 입력 가격1 — 입력값 없을때 전체 (가격 ~)
    fid_input_price_2: str  # 입력 가격2 — 입력값 없을때 전체 (~ 가격)
    fid_vol_cnt: str  # 거래량 수 — 입력값 없을때 전체 (거래량 ~)
    fid_trgt_cls_code: str  # 대상 구분 코드 — 0 : 전체

class VolumePowerResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_shrn_iscd: str | None = None  # 주식 단축 종목코드
    data_rank: str | None = None  # 데이터 순위
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    tday_rltv: str | None = None  # 당일 체결강도
    seln_cnqn_smtn: str | None = None  # 매도 체결량 합계
    shnu_cnqn_smtn: str | None = None  # 매수2 체결량 합계

class VolumePowerResponse(KisCommonResponse):
    """응답 본문."""

    output: list[VolumePowerResponse_OutputItem] = []  # 응답상세 — array

class VolumePowerExecutor(ApiExecutor[VolumePowerRequest, VolumePowerResponse]):
    """국내주식 체결강도 상위[v1_국내주식-101]."""

    # 국내주식 체결강도 상위 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0168] 체결강도 상위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 최대 30건 확인 가능하며, 다음 조회가 불가합니다. ※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다. 종목조건검색 API

    PATH = "/uapi/domestic-stock/v1/ranking/volume-power"
    METHOD = "GET"
    RESPONSE_TYPE = VolumePowerResponse
    TR_ID = "FHPST01680000"
