"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireInvestorTimeByMarketRequest(KisBaseModel):
    """요청."""

    fid_input_iscd: str  # 시장구분 — 코스피: KSP, 코스닥:KSQ, 선물,콜옵션,풋옵션 : K2I, 주식선물:999, ETF: ETF, ELW:ELW, ETN: ETN, 미니: MKI, 위클리월 : WKM, 위클리목: WKI 코스닥150: KQI
    fid_input_iscd_2: str  # 업종구분 — - fid_input_iscd: KSP(코스피) 혹은 KSQ(코스닥)인 경우 코스피(0001_종합, .…0027_제조업 ) 코스닥(1001_종합, …. 1041_IT부품) ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조

class InquireInvestorTimeByMarketResponse_OutputItem(KisBaseModel):
    """nested item."""

    frgn_seln_vol: str | None = None  # 외국인 매도 거래량
    frgn_shnu_vol: str | None = None  # 외국인 매수2 거래량
    frgn_ntby_qty: str | None = None  # 외국인 순매수 수량
    frgn_seln_tr_pbmn: str | None = None  # 외국인 매도 거래 대금
    frgn_shnu_tr_pbmn: str | None = None  # 외국인 매수2 거래 대금
    frgn_ntby_tr_pbmn: str | None = None  # 외국인 순매수 거래 대금
    prsn_seln_vol: str | None = None  # 개인 매도 거래량
    prsn_shnu_vol: str | None = None  # 개인 매수2 거래량
    prsn_ntby_qty: str | None = None  # 개인 순매수 수량
    prsn_seln_tr_pbmn: str | None = None  # 개인 매도 거래 대금
    prsn_shnu_tr_pbmn: str | None = None  # 개인 매수2 거래 대금
    prsn_ntby_tr_pbmn: str | None = None  # 개인 순매수 거래 대금
    orgn_seln_vol: str | None = None  # 기관계 매도 거래량
    orgn_shnu_vol: str | None = None  # 기관계 매수2 거래량
    orgn_ntby_qty: str | None = None  # 기관계 순매수 수량
    orgn_seln_tr_pbmn: str | None = None  # 기관계 매도 거래 대금
    orgn_shnu_tr_pbmn: str | None = None  # 기관계 매수2 거래 대금
    orgn_ntby_tr_pbmn: str | None = None  # 기관계 순매수 거래 대금
    scrt_seln_vol: str | None = None  # 증권 매도 거래량
    scrt_shnu_vol: str | None = None  # 증권 매수2 거래량
    scrt_ntby_qty: str | None = None  # 증권 순매수 수량
    scrt_seln_tr_pbmn: str | None = None  # 증권 매도 거래 대금
    scrt_shnu_tr_pbmn: str | None = None  # 증권 매수2 거래 대금
    scrt_ntby_tr_pbmn: str | None = None  # 증권 순매수 거래 대금
    ivtr_seln_vol: str | None = None  # 투자신탁 매도 거래량
    ivtr_shnu_vol: str | None = None  # 투자신탁 매수2 거래량
    ivtr_ntby_qty: str | None = None  # 투자신탁 순매수 수량
    ivtr_seln_tr_pbmn: str | None = None  # 투자신탁 매도 거래 대금
    ivtr_shnu_tr_pbmn: str | None = None  # 투자신탁 매수2 거래 대금
    ivtr_ntby_tr_pbmn: str | None = None  # 투자신탁 순매수 거래 대금
    pe_fund_seln_tr_pbmn: str | None = None  # 사모 펀드 매도 거래 대금
    pe_fund_seln_vol: str | None = None  # 사모 펀드 매도 거래량
    pe_fund_ntby_vol: str | None = None  # 사모 펀드 순매수 거래량
    pe_fund_shnu_tr_pbmn: str | None = None  # 사모 펀드 매수2 거래 대금
    pe_fund_shnu_vol: str | None = None  # 사모 펀드 매수2 거래량
    pe_fund_ntby_tr_pbmn: str | None = None  # 사모 펀드 순매수 거래 대금
    bank_seln_vol: str | None = None  # 은행 매도 거래량
    bank_shnu_vol: str | None = None  # 은행 매수2 거래량
    bank_ntby_qty: str | None = None  # 은행 순매수 수량
    bank_seln_tr_pbmn: str | None = None  # 은행 매도 거래 대금
    bank_shnu_tr_pbmn: str | None = None  # 은행 매수2 거래 대금
    bank_ntby_tr_pbmn: str | None = None  # 은행 순매수 거래 대금
    insu_seln_vol: str | None = None  # 보험 매도 거래량
    insu_shnu_vol: str | None = None  # 보험 매수2 거래량
    insu_ntby_qty: str | None = None  # 보험 순매수 수량
    insu_seln_tr_pbmn: str | None = None  # 보험 매도 거래 대금
    insu_shnu_tr_pbmn: str | None = None  # 보험 매수2 거래 대금
    insu_ntby_tr_pbmn: str | None = None  # 보험 순매수 거래 대금
    mrbn_seln_vol: str | None = None  # 종금 매도 거래량
    mrbn_shnu_vol: str | None = None  # 종금 매수2 거래량
    mrbn_ntby_qty: str | None = None  # 종금 순매수 수량
    mrbn_seln_tr_pbmn: str | None = None  # 종금 매도 거래 대금
    mrbn_shnu_tr_pbmn: str | None = None  # 종금 매수2 거래 대금
    mrbn_ntby_tr_pbmn: str | None = None  # 종금 순매수 거래 대금
    fund_seln_vol: str | None = None  # 기금 매도 거래량
    fund_shnu_vol: str | None = None  # 기금 매수2 거래량
    fund_ntby_qty: str | None = None  # 기금 순매수 수량
    fund_seln_tr_pbmn: str | None = None  # 기금 매도 거래 대금
    fund_shnu_tr_pbmn: str | None = None  # 기금 매수2 거래 대금
    fund_ntby_tr_pbmn: str | None = None  # 기금 순매수 거래 대금
    etc_orgt_seln_vol: str | None = None  # 기타 단체 매도 거래량
    etc_orgt_shnu_vol: str | None = None  # 기타 단체 매수2 거래량
    etc_orgt_ntby_vol: str | None = None  # 기타 단체 순매수 거래량
    etc_orgt_seln_tr_pbmn: str | None = None  # 기타 단체 매도 거래 대금
    etc_orgt_shnu_tr_pbmn: str | None = None  # 기타 단체 매수2 거래 대금
    etc_orgt_ntby_tr_pbmn: str | None = None  # 기타 단체 순매수 거래 대금
    etc_corp_seln_vol: str | None = None  # 기타 법인 매도 거래량
    etc_corp_shnu_vol: str | None = None  # 기타 법인 매수2 거래량
    etc_corp_ntby_vol: str | None = None  # 기타 법인 순매수 거래량
    etc_corp_seln_tr_pbmn: str | None = None  # 기타 법인 매도 거래 대금
    etc_corp_shnu_tr_pbmn: str | None = None  # 기타 법인 매수2 거래 대금
    etc_corp_ntby_tr_pbmn: str | None = None  # 기타 법인 순매수 거래 대금

class InquireInvestorTimeByMarketResponse(KisCommonResponse):
    """응답 본문."""

    output: InquireInvestorTimeByMarketResponse_OutputItem | None = None  # 응답상세

class InquireInvestorTimeByMarketExecutor(ApiExecutor[InquireInvestorTimeByMarketRequest, InquireInvestorTimeByMarketResponse]):
    """시장별 투자자매매동향(시세)[v1_국내주식-074]."""

    # 시장별 투자자매매동향(시세성) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0403] 시장별 시간동향 의 상단 표 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-investor-time-by-market"
    METHOD = "GET"
    RESPONSE_TYPE = InquireInvestorTimeByMarketResponse
    TR_ID = "FHPTJ04030000"
