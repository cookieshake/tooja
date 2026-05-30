"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class FinanceRatioRequest(KisBaseModel):
    """요청."""

    fid_trgt_cls_code: str  # 대상 구분 코드 — 0 : 전체
    fid_cond_mrkt_div_code: str  # 조건 시장 분류 코드 — 시장구분코드 (J:KRX, NX:NXT)
    fid_cond_scr_div_code: str  # 조건 화면 분류 코드 — Unique key( 20175 )
    fid_input_iscd: str  # 입력 종목코드 — 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
    fid_div_cls_code: str  # 분류 구분 코드 — 0 : 전체
    fid_input_price_1: str  # 입력 가격1 — 입력값 없을때 전체 (가격 ~)
    fid_input_price_2: str  # 입력 가격2 — 입력값 없을때 전체 (~ 가격)
    fid_vol_cnt: str  # 거래량 수 — 입력값 없을때 전체 (거래량 ~)
    fid_input_option_1: str  # 입력 옵션1 — 회계년도 입력 (ex 2023)
    fid_input_option_2: str  # 입력 옵션2 — 0: 1/4분기 , 1: 반기, 2: 3/4분기, 3: 결산
    fid_rank_sort_cls_code: str  # 순위 정렬 구분 코드 — 7: 수익성 분석, 11 : 안정성 분석, 15: 성장성 분석, 20: 활동성 분석
    fid_blng_cls_code: str  # 소속 구분 코드 — 0
    fid_trgt_exls_cls_code: str  # 대상 제외 구분 코드 — 0 : 전체

class FinanceRatioResponse_OutputItem(KisBaseModel):
    """nested item."""

    data_rank: str | None = None  # 데이터 순위
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    mksc_shrn_iscd: str | None = None  # 유가증권 단축 종목코드
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    cptl_op_prfi: str | None = None  # 총자본경상이익율
    cptl_ntin_rate: str | None = None  # 총자본 순이익율
    sale_totl_rate: str | None = None  # 매출액 총이익율
    sale_ntin_rate: str | None = None  # 매출액 순이익율
    bis: str | None = None  # 자기자본비율
    lblt_rate: str | None = None  # 부채 비율
    bram_depn: str | None = None  # 차입금 의존도
    rsrv_rate: str | None = None  # 유보 비율
    grs: str | None = None  # 매출액 증가율
    op_prfi_inrt: str | None = None  # 경상 이익 증가율
    bsop_prfi_inrt: str | None = None  # 영업 이익 증가율
    ntin_inrt: str | None = None  # 순이익 증가율
    equt_inrt: str | None = None  # 자기자본 증가율
    cptl_tnrt: str | None = None  # 총자본회전율
    sale_bond_tnrt: str | None = None  # 매출 채권 회전율
    totl_aset_inrt: str | None = None  # 총자산 증가율
    stac_month: str | None = None  # 결산 월
    stac_month_cls_code: str | None = None  # 결산 월 구분 코드
    iqry_csnu: str | None = None  # 조회 건수

class FinanceRatioResponse(KisCommonResponse):
    """응답 본문."""

    output: list[FinanceRatioResponse_OutputItem] = []  # 응답상세 — array

class FinanceRatioExecutor(ApiExecutor[FinanceRatioRequest, FinanceRatioResponse]):
    """국내주식 재무비율 순위[v1_국내주식-092]."""

    # 국내주식 재무비율 순위 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0175] 재무비율순위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 최대 30건 확인 가능하며, 다음 조회가 불가합니다. ※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다. 종목조건검색 API는

    PATH = "/uapi/domestic-stock/v1/ranking/finance-ratio"
    METHOD = "GET"
    RESPONSE_TYPE = FinanceRatioResponse
    TR_ID = "FHPST01750000"
