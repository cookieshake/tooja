"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InvestorTradeByStockDailyRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — J:KRX, NX:NXT, UN:통합
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목번호 (6자리)
    FID_INPUT_DATE_1: str  # 입력 날짜1 — 입력 날짜(20250812) (해당일 조회는 장 종료 후 정상 조회 가능)
    FID_ORG_ADJ_PRC: str  # 수정주가 원주가 가격 — 공란 입력
    FID_ETC_CLS_CODE: str  # 기타 구분 코드 — "1" 입력

class InvestorTradeByStockDailyResponse_Output1Item(KisBaseModel):
    """nested item."""

    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    prdy_vol: str | None = None  # 전일 거래량
    rprs_mrkt_kor_name: str | None = None  # 대표 시장 한글 명

class InvestorTradeByStockDailyResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자
    stck_clpr: str | None = None  # 주식 종가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량 — 단위 : 주
    acml_tr_pbmn: str | None = None  # 누적 거래 대금 — 단위 : 백만원
    stck_oprc: str | None = None  # 주식 시가2
    stck_hgpr: str | None = None  # 주식 최고가
    stck_lwpr: str | None = None  # 주식 최저가
    frgn_ntby_qty: str | None = None  # 외국인 순매수 수량 — 단위 : 주
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
    etc_corp_ntby_vol: str | None = None  # 기타 법인 순매수 거래량
    etc_orgt_ntby_vol: str | None = None  # 기타 단체 순매수 거래량
    frgn_reg_ntby_pbmn: str | None = None  # 외국인 등록 순매수 대금 — 단위 : 백만원
    frgn_ntby_tr_pbmn: str | None = None  # 외국인 순매수 거래 대금
    frgn_nreg_ntby_pbmn: str | None = None  # 외국인 비등록 순매수 대금
    prsn_ntby_tr_pbmn: str | None = None  # 개인 순매수 거래 대금
    orgn_ntby_tr_pbmn: str | None = None  # 기관계 순매수 거래 대금
    scrt_ntby_tr_pbmn: str | None = None  # 증권 순매수 거래 대금
    pe_fund_ntby_tr_pbmn: str | None = None  # 사모 펀드 순매수 거래 대금
    ivtr_ntby_tr_pbmn: str | None = None  # 투자신탁 순매수 거래 대금
    bank_ntby_tr_pbmn: str | None = None  # 은행 순매수 거래 대금
    insu_ntby_tr_pbmn: str | None = None  # 보험 순매수 거래 대금
    mrbn_ntby_tr_pbmn: str | None = None  # 종금 순매수 거래 대금
    fund_ntby_tr_pbmn: str | None = None  # 기금 순매수 거래 대금
    etc_ntby_tr_pbmn: str | None = None  # 기타 순매수 거래 대금
    etc_corp_ntby_tr_pbmn: str | None = None  # 기타 법인 순매수 거래 대금
    etc_orgt_ntby_tr_pbmn: str | None = None  # 기타 단체 순매수 거래 대금
    frgn_seln_vol: str | None = None  # 외국인 매도 거래량
    frgn_shnu_vol: str | None = None  # 외국인 매수2 거래량
    frgn_seln_tr_pbmn: str | None = None  # 외국인 매도 거래 대금
    frgn_shnu_tr_pbmn: str | None = None  # 외국인 매수2 거래 대금
    frgn_reg_askp_qty: str | None = None  # 외국인 등록 매도 수량
    frgn_reg_bidp_qty: str | None = None  # 외국인 등록 매수 수량
    frgn_reg_askp_pbmn: str | None = None  # 외국인 등록 매도 대금
    frgn_reg_bidp_pbmn: str | None = None  # 외국인 등록 매수 대금
    frgn_nreg_askp_qty: str | None = None  # 외국인 비등록 매도 수량
    frgn_nreg_bidp_qty: str | None = None  # 외국인 비등록 매수 수량
    frgn_nreg_askp_pbmn: str | None = None  # 외국인 비등록 매도 대금
    frgn_nreg_bidp_pbmn: str | None = None  # 외국인 비등록 매수 대금
    prsn_seln_vol: str | None = None  # 개인 매도 거래량
    prsn_shnu_vol: str | None = None  # 개인 매수2 거래량
    prsn_seln_tr_pbmn: str | None = None  # 개인 매도 거래 대금
    prsn_shnu_tr_pbmn: str | None = None  # 개인 매수2 거래 대금
    orgn_seln_vol: str | None = None  # 기관계 매도 거래량
    orgn_shnu_vol: str | None = None  # 기관계 매수2 거래량
    orgn_seln_tr_pbmn: str | None = None  # 기관계 매도 거래 대금
    orgn_shnu_tr_pbmn: str | None = None  # 기관계 매수2 거래 대금
    scrt_seln_vol: str | None = None  # 증권 매도 거래량
    scrt_shnu_vol: str | None = None  # 증권 매수2 거래량
    scrt_seln_tr_pbmn: str | None = None  # 증권 매도 거래 대금
    scrt_shnu_tr_pbmn: str | None = None  # 증권 매수2 거래 대금
    ivtr_seln_vol: str | None = None  # 투자신탁 매도 거래량
    ivtr_shnu_vol: str | None = None  # 투자신탁 매수2 거래량
    ivtr_seln_tr_pbmn: str | None = None  # 투자신탁 매도 거래 대금
    ivtr_shnu_tr_pbmn: str | None = None  # 투자신탁 매수2 거래 대금
    pe_fund_seln_tr_pbmn: str | None = None  # 사모 펀드 매도 거래 대금
    pe_fund_seln_vol: str | None = None  # 사모 펀드 매도 거래량
    pe_fund_shnu_tr_pbmn: str | None = None  # 사모 펀드 매수2 거래 대금
    pe_fund_shnu_vol: str | None = None  # 사모 펀드 매수2 거래량
    bank_seln_vol: str | None = None  # 은행 매도 거래량
    bank_shnu_vol: str | None = None  # 은행 매수2 거래량
    bank_seln_tr_pbmn: str | None = None  # 은행 매도 거래 대금
    bank_shnu_tr_pbmn: str | None = None  # 은행 매수2 거래 대금
    insu_seln_vol: str | None = None  # 보험 매도 거래량
    insu_shnu_vol: str | None = None  # 보험 매수2 거래량
    insu_seln_tr_pbmn: str | None = None  # 보험 매도 거래 대금
    insu_shnu_tr_pbmn: str | None = None  # 보험 매수2 거래 대금
    mrbn_seln_vol: str | None = None  # 종금 매도 거래량
    mrbn_shnu_vol: str | None = None  # 종금 매수2 거래량
    mrbn_seln_tr_pbmn: str | None = None  # 종금 매도 거래 대금
    mrbn_shnu_tr_pbmn: str | None = None  # 종금 매수2 거래 대금
    fund_seln_vol: str | None = None  # 기금 매도 거래량
    fund_shnu_vol: str | None = None  # 기금 매수2 거래량
    fund_seln_tr_pbmn: str | None = None  # 기금 매도 거래 대금
    fund_shnu_tr_pbmn: str | None = None  # 기금 매수2 거래 대금
    etc_seln_vol: str | None = None  # 기타 매도 거래량
    etc_shnu_vol: str | None = None  # 기타 매수2 거래량
    etc_seln_tr_pbmn: str | None = None  # 기타 매도 거래 대금
    etc_shnu_tr_pbmn: str | None = None  # 기타 매수2 거래 대금
    etc_orgt_seln_vol: str | None = None  # 기타 단체 매도 거래량
    etc_orgt_shnu_vol: str | None = None  # 기타 단체 매수2 거래량
    etc_orgt_seln_tr_pbmn: str | None = None  # 기타 단체 매도 거래 대금
    etc_orgt_shnu_tr_pbmn: str | None = None  # 기타 단체 매수2 거래 대금
    etc_corp_seln_vol: str | None = None  # 기타 법인 매도 거래량
    etc_corp_shnu_vol: str | None = None  # 기타 법인 매수2 거래량
    etc_corp_seln_tr_pbmn: str | None = None  # 기타 법인 매도 거래 대금
    etc_corp_shnu_tr_pbmn: str | None = None  # 기타 법인 매수2 거래 대금
    bold_yn: str | None = None  # BOLD 여부

class InvestorTradeByStockDailyResponse(KisCommonResponse):
    """응답 본문."""

    output1: InvestorTradeByStockDailyResponse_Output1Item | None = None  # 응답상세
    output2: list[InvestorTradeByStockDailyResponse_Output2Item] = []  # 응답상세 — array

class InvestorTradeByStockDailyExecutor(ApiExecutor[InvestorTradeByStockDailyRequest, InvestorTradeByStockDailyResponse]):
    """종목별 투자자매매동향(일별)."""

    # 국내주식 종목별 투자자매매동향(일별) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0416] 종목별 일별동향 화면 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 단위 : 금액(백만원) 수량(주) 당일 데이터는 15:40이후에 데이터가 가집계 및 산출되어 15:40부터 조회가능하며, 데이터 산출의 경우 산출 시간대는 일정하지 않을 수 있음을 참고 부탁드립니다. 추가로

    PATH = "/uapi/domestic-stock/v1/quotations/investor-trade-by-stock-daily"
    METHOD = "GET"
    RESPONSE_TYPE = InvestorTradeByStockDailyResponse
    TR_ID = "FHPTJ04160001"
