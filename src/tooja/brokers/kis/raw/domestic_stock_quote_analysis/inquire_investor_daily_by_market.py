"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireInvestorDailyByMarketRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — 시장구분코드 (업종 U)
    FID_INPUT_ISCD: str  # 입력 종목코드 — 코스피, 코스닥 : 업종분류코드 (종목정보파일 - 업종코드 참조)
    FID_INPUT_DATE_1: str  # 입력 날짜1 — ex. 20240517
    FID_INPUT_ISCD_1: str  # 입력 종목코드 — 코스피(KSP), 코스닥(KSQ)
    FID_INPUT_DATE_2: str  # 입력 날짜2 — 입력 날짜1과 동일날짜 입력
    FID_INPUT_ISCD_2: str  # 하위 분류코드 — 코스피, 코스닥 : 업종분류코드 (종목정보파일 - 업종코드 참조)

class InquireInvestorDailyByMarketResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자
    bstp_nmix_prpr: str | None = None  # 업종 지수 현재가
    bstp_nmix_prdy_vrss: str | None = None  # 업종 지수 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    bstp_nmix_prdy_ctrt: str | None = None  # 업종 지수 전일 대비율
    bstp_nmix_oprc: str | None = None  # 업종 지수 시가2
    bstp_nmix_hgpr: str | None = None  # 업종 지수 최고가
    bstp_nmix_lwpr: str | None = None  # 업종 지수 최저가
    stck_prdy_clpr: str | None = None  # 주식 전일 종가
    frgn_ntby_qty: str | None = None  # 외국인 순매수 수량
    frgn_reg_ntby_qty: str | None = None  # 외국인 등록 순매수 수량
    frgn_nreg_ntby_qty: str | None = None  # 외국인 비등록 순매수 수량
    prsn_ntby_qty: str | None = None  # 개인 순매수 수량
    orgn_ntby_qty: str | None = None  # 기관계 순매수 수량
    scrt_ntby_qty: str | None = None  # 증권 순매수 수량
    ivtr_ntby_qty: str | None = None  # 투자신탁 순매수 수량
    pe_fund_ntby_vol: str | None = None  # 사모 펀드 순매수 거래량
    bank_ntby_qty: str | None = None  # 은행 순매수 수량
    insu_ntby_qty: str | None = None  # 보험 순매수 수량
    mrbn_ntby_qty: str | None = None  # 종금 순매수 수량
    fund_ntby_qty: str | None = None  # 기금 순매수 수량
    etc_ntby_qty: str | None = None  # 기타 순매수 수량
    etc_orgt_ntby_vol: str | None = None  # 기타 단체 순매수 거래량
    etc_corp_ntby_vol: str | None = None  # 기타 법인 순매수 거래량
    frgn_ntby_tr_pbmn: str | None = None  # 외국인 순매수 거래 대금
    frgn_reg_ntby_pbmn: str | None = None  # 외국인 등록 순매수 대금
    frgn_nreg_ntby_pbmn: str | None = None  # 외국인 비등록 순매수 대금
    prsn_ntby_tr_pbmn: str | None = None  # 개인 순매수 거래 대금
    orgn_ntby_tr_pbmn: str | None = None  # 기관계 순매수 거래 대금
    scrt_ntby_tr_pbmn: str | None = None  # 증권 순매수 거래 대금
    ivtr_ntby_tr_pbmn: str | None = None  # 투자신탁 순매수 거래 대금
    pe_fund_ntby_tr_pbmn: str | None = None  # 사모 펀드 순매수 거래 대금
    bank_ntby_tr_pbmn: str | None = None  # 은행 순매수 거래 대금
    insu_ntby_tr_pbmn: str | None = None  # 보험 순매수 거래 대금
    mrbn_ntby_tr_pbmn: str | None = None  # 종금 순매수 거래 대금
    fund_ntby_tr_pbmn: str | None = None  # 기금 순매수 거래 대금
    etc_ntby_tr_pbmn: str | None = None  # 기타 순매수 거래 대금
    etc_orgt_ntby_tr_pbmn: str | None = None  # 기타 단체 순매수 거래 대금
    etc_corp_ntby_tr_pbmn: str | None = None  # 기타 법인 순매수 거래 대금

class InquireInvestorDailyByMarketResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InquireInvestorDailyByMarketResponse_OutputItem] = []  # 응답상세 — array

class InquireInvestorDailyByMarketExecutor(ApiExecutor[InquireInvestorDailyByMarketRequest, InquireInvestorDailyByMarketResponse]):
    """시장별 투자자매매동향(일별) [국내주식-075]."""

    # 시장별 투자자매매동향(일별) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0404] 시장별 일별동향 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-investor-daily-by-market"
    METHOD = "GET"
    RESPONSE_TYPE = InquireInvestorDailyByMarketResponse
    TR_ID = "FHPTJ04040000"
