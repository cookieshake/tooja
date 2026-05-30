"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class ForeignInstitutionTotalRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 시장 분류 코드 — V(Default)
    FID_COND_SCR_DIV_CODE: str  # 조건 화면 분류 코드 — 16449(Default)
    FID_INPUT_ISCD: str  # 입력 종목코드 — 0000:전체, 0001:코스피, 1001:코스닥 ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조)
    FID_DIV_CLS_CODE: str  # 분류 구분 코드 — 0: 수량정열, 1: 금액정열
    FID_RANK_SORT_CLS_CODE: str  # 순위 정렬 구분 코드 — 0: 순매수상위, 1: 순매도상위
    FID_ETC_CLS_CODE: str  # 기타 구분 정렬 — 0:전체 1:외국인 2:기관계 3:기타

class ForeignInstitutionTotalResponse_OutputItem(KisBaseModel):
    """nested item."""

    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    mksc_shrn_iscd: str | None = None  # 유가증권 단축 종목코드
    ntby_qty: str | None = None  # 순매수 수량
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_vrss: str | None = None  # 전일 대비
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    frgn_ntby_qty: str | None = None  # 외국인 순매수 수량
    orgn_ntby_qty: str | None = None  # 기관계 순매수 수량
    ivtr_ntby_qty: str | None = None  # 투자신탁 순매수 수량
    bank_ntby_qty: str | None = None  # 은행 순매수 수량
    insu_ntby_qty: str | None = None  # 보험 순매수 수량
    mrbn_ntby_qty: str | None = None  # 종금 순매수 수량
    fund_ntby_qty: str | None = None  # 기금 순매수 수량
    etc_orgt_ntby_vol: str | None = None  # 기타 단체 순매수 거래량
    etc_corp_ntby_vol: str | None = None  # 기타 법인 순매수 거래량
    frgn_ntby_tr_pbmn: str | None = None  # 외국인 순매수 거래 대금 — frgn_ntby_tr_pbmn ~ etc_corp_ntby_tr_pbmn (단위 : 백만원, 수량*현재가)
    orgn_ntby_tr_pbmn: str | None = None  # 기관계 순매수 거래 대금
    ivtr_ntby_tr_pbmn: str | None = None  # 투자신탁 순매수 거래 대금
    bank_ntby_tr_pbmn: str | None = None  # 은행 순매수 거래 대금
    insu_ntby_tr_pbmn: str | None = None  # 보험 순매수 거래 대금
    mrbn_ntby_tr_pbmn: str | None = None  # 종금 순매수 거래 대금
    fund_ntby_tr_pbmn: str | None = None  # 기금 순매수 거래 대금
    etc_orgt_ntby_tr_pbmn: str | None = None  # 기타 단체 순매수 거래 대금
    etc_corp_ntby_tr_pbmn: str | None = None  # 기타 법인 순매수 거래 대금

class ForeignInstitutionTotalResponse(KisCommonResponse):
    """응답 본문."""

    Output: ForeignInstitutionTotalResponse_OutputItem | None = None  # 응답상세1

class ForeignInstitutionTotalExecutor(ApiExecutor[ForeignInstitutionTotalRequest, ForeignInstitutionTotalResponse]):
    """국내기관_외국인 매매종목가집계[국내주식-037]."""

    # 국내기관_외국인 매매종목가집계 API입니다. HTS(efriend Plus) [0440] 외국인/기관 매매종목 가집계 화면을 API로 구현한 사항으로 화면을 함께 보시면 기능 이해가 쉽습니다. 증권사 직원이 장중에 집계/입력한 자료를 단순 누계한 수치로서, 입력시간은 외국인 09:30, 11:20, 13:20, 14:30 / 기관종합 10:00, 11:20, 13:20, 14:30 이며, 입력한 시간은 ±10분정도 차이가 발생

    PATH = "/uapi/domestic-stock/v1/quotations/foreign-institution-total"
    METHOD = "GET"
    RESPONSE_TYPE = ForeignInstitutionTotalResponse
    TR_ID = "FHPTJ04400000"
