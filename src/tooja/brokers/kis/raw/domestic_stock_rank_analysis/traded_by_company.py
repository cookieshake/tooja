"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class TradedByCompanyRequest(KisBaseModel):
    """요청."""

    fid_trgt_exls_cls_code: str  # 대상 제외 구분 코드 — 0: 전체
    fid_cond_mrkt_div_code: str  # 조건 시장 분류 코드 — 시장구분코드 (J:KRX, NX:NXT)
    fid_cond_scr_div_code: str  # 조건 화면 분류 코드 — Unique key(20186)
    fid_div_cls_code: str  # 분류 구분 코드 — 0:전체, 1:관리종목, 2:투자주의, 3:투자경고, 4:투자위험예고, 5:투자위험, 6:보통주, 7:우선주
    fid_rank_sort_cls_code: str  # 순위 정렬 구분 코드 — 0:매도상위,1:매수상위
    fid_input_date_1: str  # 입력 날짜1 — 기간~
    fid_input_date_2: str  # 입력 날짜2 — ~기간
    fid_input_iscd: str  # 입력 종목코드 — 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
    fid_trgt_cls_code: str  # 대상 구분 코드 — 0: 전체
    fid_aply_rang_vol: str  # 적용 범위 거래량 — 0: 전체, 100: 100주 이상
    fid_aply_rang_prc_2: str  # 적용 범위 가격2 — ~ 가격
    fid_aply_rang_prc_1: str  # 적용 범위 가격1 — 가격 ~

class TradedByCompanyResponse_OutputItem(KisBaseModel):
    """nested item."""

    data_rank: str | None = None  # 데이터 순위
    mksc_shrn_iscd: str | None = None  # 유가증권 단축 종목코드
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_vrss: str | None = None  # 전일 대비
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    seln_cnqn_smtn: str | None = None  # 매도 체결량 합계
    shnu_cnqn_smtn: str | None = None  # 매수2 체결량 합계
    ntby_cnqn: str | None = None  # 순매수 체결량

class TradedByCompanyResponse(KisCommonResponse):
    """응답 본문."""

    output: list[TradedByCompanyResponse_OutputItem] = []  # 응답상세 — array

class TradedByCompanyExecutor(ApiExecutor[TradedByCompanyRequest, TradedByCompanyResponse]):
    """국내주식 당사매매종목 상위[v1_국내주식-104]."""

    # 국내주식 당사매매종목 상위 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0186] 당사매매종목 상위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 최대 30건 확인 가능하며, 다음 조회가 불가합니다. ※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다. 종목조건검색

    PATH = "/uapi/domestic-stock/v1/ranking/traded-by-company"
    METHOD = "GET"
    RESPONSE_TYPE = TradedByCompanyResponse
    TR_ID = "FHPST01860000"
