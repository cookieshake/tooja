"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class CompProgramTradeDailyRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 시장 분류 코드 — J : KRX, NX : NXT, UN : 통합
    FID_MRKT_CLS_CODE: str  # 시장 구분 코드 — K:코스피, Q:코스닥
    FID_INPUT_DATE_1: str  # 검색시작일 — 공백 입력, 입력 시 ~ 입력일자까지 조회됨 * 8개월 이상 과거 조회 불가
    FID_INPUT_DATE_2: str  # 검색종료일 — 공백 입력

class CompProgramTradeDailyResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자
    nabt_entm_seln_tr_pbmn: str | None = None  # 비차익 위탁 매도 거래 대금
    nabt_onsl_seln_vol: str | None = None  # 비차익 자기 매도 거래량
    whol_onsl_seln_tr_pbmn: str | None = None  # 전체 자기 매도 거래 대금
    arbt_smtn_shnu_vol: str | None = None  # 차익 합계 매수2 거래량
    nabt_smtn_shnu_tr_pbmn: str | None = None  # 비차익 합계 매수2 거래 대금
    arbt_entm_ntby_qty: str | None = None  # 차익 위탁 순매수 수량
    nabt_entm_ntby_tr_pbmn: str | None = None  # 비차익 위탁 순매수 거래 대금
    arbt_entm_seln_vol: str | None = None  # 차익 위탁 매도 거래량
    nabt_entm_seln_vol_rate: str | None = None  # 비차익 위탁 매도 거래량 비율
    nabt_onsl_seln_vol_rate: str | None = None  # 비차익 자기 매도 거래량 비율
    whol_onsl_seln_tr_pbmn_rate: str | None = None  # 전체 자기 매도 거래 대금 비율
    arbt_smtm_shun_vol_rate: str | None = None  # 차익 합계 매수 거래량 비율
    nabt_smtm_shun_tr_pbmn_rate: str | None = None  # 비차익 합계 매수 거래대금 비율
    arbt_entm_ntby_qty_rate: str | None = None  # 차익 위탁 순매수 수량 비율
    nabt_entm_ntby_tr_pbmn_rate: str | None = None  # 비차익 위탁 순매수 거래 대금
    arbt_entm_seln_vol_rate: str | None = None  # 차익 위탁 매도 거래량 비율
    nabt_entm_seln_tr_pbmn_rate: str | None = None  # 비차익 위탁 매도 거래 대금 비
    nabt_onsl_seln_tr_pbmn: str | None = None  # 비차익 자기 매도 거래 대금
    whol_smtn_seln_vol: str | None = None  # 전체 합계 매도 거래량
    arbt_smtn_shnu_tr_pbmn: str | None = None  # 차익 합계 매수2 거래 대금
    whol_entm_shnu_vol: str | None = None  # 전체 위탁 매수2 거래량
    arbt_entm_ntby_tr_pbmn: str | None = None  # 차익 위탁 순매수 거래 대금
    nabt_onsl_ntby_qty: str | None = None  # 비차익 자기 순매수 수량
    arbt_entm_seln_tr_pbmn: str | None = None  # 차익 위탁 매도 거래 대금
    nabt_onsl_seln_tr_pbmn_rate: str | None = None  # 비차익 자기 매도 거래 대금 비
    whol_seln_vol_rate: str | None = None  # 전체 매도 거래량 비율
    arbt_smtm_shun_tr_pbmn_rate: str | None = None  # 차익 합계 매수 거래대금 비율
    whol_entm_shnu_vol_rate: str | None = None  # 전체 위탁 매수 거래량 비율
    arbt_entm_ntby_tr_pbmn_rate: str | None = None  # 차익 위탁 순매수 거래 대금 비
    nabt_onsl_ntby_qty_rate: str | None = None  # 비차익 자기 순매수 수량 비율
    arbt_entm_seln_tr_pbmn_rate: str | None = None  # 차익 위탁 매도 거래 대금 비율
    nabt_smtn_seln_vol: str | None = None  # 비차익 합계 매도 거래량
    whol_smtn_seln_tr_pbmn: str | None = None  # 전체 합계 매도 거래 대금
    nabt_entm_shnu_vol: str | None = None  # 비차익 위탁 매수2 거래량
    whol_entm_shnu_tr_pbmn: str | None = None  # 전체 위탁 매수2 거래 대금
    arbt_onsl_ntby_qty: str | None = None  # 차익 자기 순매수 수량
    nabt_onsl_ntby_tr_pbmn: str | None = None  # 비차익 자기 순매수 거래 대금
    arbt_onsl_seln_tr_pbmn: str | None = None  # 차익 자기 매도 거래 대금
    nabt_smtm_seln_vol_rate: str | None = None  # 비차익 합계 매도 거래량 비율
    whol_seln_tr_pbmn_rate: str | None = None  # 전체 매도 거래대금 비율
    nabt_entm_shnu_vol_rate: str | None = None  # 비차익 위탁 매수 거래량 비율
    whol_entm_shnu_tr_pbmn_rate: str | None = None  # 전체 위탁 매수 거래 대금 비율
    arbt_onsl_ntby_qty_rate: str | None = None  # 차익 자기 순매수 수량 비율
    nabt_onsl_ntby_tr_pbmn_rate: str | None = None  # 비차익 자기 순매수 거래 대금
    arbt_onsl_seln_tr_pbmn_rate: str | None = None  # 차익 자기 매도 거래 대금 비율
    nabt_smtn_seln_tr_pbmn: str | None = None  # 비차익 합계 매도 거래 대금
    arbt_entm_shnu_vol: str | None = None  # 차익 위탁 매수2 거래량
    nabt_entm_shnu_tr_pbmn: str | None = None  # 비차익 위탁 매수2 거래 대금
    whol_onsl_shnu_vol: str | None = None  # 전체 자기 매수2 거래량
    arbt_onsl_ntby_tr_pbmn: str | None = None  # 차익 자기 순매수 거래 대금
    nabt_smtn_ntby_qty: str | None = None  # 비차익 합계 순매수 수량
    arbt_onsl_seln_vol: str | None = None  # 차익 자기 매도 거래량
    nabt_smtm_seln_tr_pbmn_rate: str | None = None  # 비차익 합계 매도 거래대금 비율
    arbt_entm_shnu_vol_rate: str | None = None  # 차익 위탁 매수 거래량 비율
    nabt_entm_shnu_tr_pbmn_rate: str | None = None  # 비차익 위탁 매수 거래 대금 비
    whol_onsl_shnu_tr_pbmn: str | None = None  # 전체 자기 매수2 거래 대금
    arbt_onsl_ntby_tr_pbmn_rate: str | None = None  # 차익 자기 순매수 거래 대금 비
    nabt_smtm_ntby_qty_rate: str | None = None  # 비차익 합계 순매수 수량 비율
    arbt_onsl_seln_vol_rate: str | None = None  # 차익 자기 매도 거래량 비율
    whol_entm_seln_vol: str | None = None  # 전체 위탁 매도 거래량
    arbt_entm_shnu_tr_pbmn: str | None = None  # 차익 위탁 매수2 거래 대금
    nabt_onsl_shnu_vol: str | None = None  # 비차익 자기 매수2 거래량
    whol_onsl_shnu_tr_pbmn_rate: str | None = None  # 전체 자기 매수 거래 대금 비율
    arbt_smtn_ntby_qty: str | None = None  # 차익 합계 순매수 수량
    nabt_smtn_ntby_tr_pbmn: str | None = None  # 비차익 합계 순매수 거래 대금
    arbt_smtn_seln_vol: str | None = None  # 차익 합계 매도 거래량
    whol_entm_seln_tr_pbmn: str | None = None  # 전체 위탁 매도 거래 대금
    arbt_entm_shnu_tr_pbmn_rate: str | None = None  # 차익 위탁 매수 거래 대금 비율
    nabt_onsl_shnu_vol_rate: str | None = None  # 비차익 자기 매수 거래량 비율
    whol_onsl_shnu_vol_rate: str | None = None  # 전체 자기 매수 거래량 비율
    arbt_smtm_ntby_qty_rate: str | None = None  # 차익 합계 순매수 수량 비율
    nabt_smtm_ntby_tr_pbmn_rate: str | None = None  # 비차익 합계 순매수 거래대금 비
    arbt_smtm_seln_vol_rate: str | None = None  # 차익 합계 매도 거래량 비율
    whol_entm_seln_vol_rate: str | None = None  # 전체 위탁 매도 거래량 비율
    arbt_onsl_shnu_vol: str | None = None  # 차익 자기 매수2 거래량
    nabt_onsl_shnu_tr_pbmn: str | None = None  # 비차익 자기 매수2 거래 대금
    whol_smtn_shnu_vol: str | None = None  # 전체 합계 매수2 거래량
    arbt_smtn_ntby_tr_pbmn: str | None = None  # 차익 합계 순매수 거래 대금
    whol_entm_ntby_qty: str | None = None  # 전체 위탁 순매수 수량
    arbt_smtn_seln_tr_pbmn: str | None = None  # 차익 합계 매도 거래 대금
    whol_entm_seln_tr_pbmn_rate: str | None = None  # 전체 위탁 매도 거래 대금 비율
    arbt_onsl_shnu_vol_rate: str | None = None  # 차익 자기 매수 거래량 비율
    nabt_onsl_shnu_tr_pbmn_rate: str | None = None  # 비차익 자기 매수 거래 대금 비
    whol_shun_vol_rate: str | None = None  # 전체 매수 거래량 비율
    arbt_smtm_ntby_tr_pbmn_rate: str | None = None  # 차익 합계 순매수 거래대금 비율
    whol_entm_ntby_qty_rate: str | None = None  # 전체 위탁 순매수 수량 비율
    arbt_smtm_seln_tr_pbmn_rate: str | None = None  # 차익 합계 매도 거래대금 비율
    whol_onsl_seln_vol: str | None = None  # 전체 자기 매도 거래량
    arbt_onsl_shnu_tr_pbmn: str | None = None  # 차익 자기 매수2 거래 대금
    nabt_smtn_shnu_vol: str | None = None  # 비차익 합계 매수2 거래량
    whol_smtn_shnu_tr_pbmn: str | None = None  # 전체 합계 매수2 거래 대금
    nabt_entm_ntby_qty: str | None = None  # 비차익 위탁 순매수 수량
    whol_entm_ntby_tr_pbmn: str | None = None  # 전체 위탁 순매수 거래 대금
    nabt_entm_seln_vol: str | None = None  # 비차익 위탁 매도 거래량
    whol_onsl_seln_vol_rate: str | None = None  # 전체 자기 매도 거래량 비율
    arbt_onsl_shnu_tr_pbmn_rate: str | None = None  # 차익 자기 매수 거래 대금 비율
    nabt_smtm_shun_vol_rate: str | None = None  # 비차익 합계 매수 거래량 비율
    whol_shun_tr_pbmn_rate: str | None = None  # 전체 매수 거래대금 비율
    nabt_entm_ntby_qty_rate: str | None = None  # 비차익 위탁 순매수 수량 비율

class CompProgramTradeDailyResponse(KisCommonResponse):
    """응답 본문."""

    output: list[CompProgramTradeDailyResponse_OutputItem] = []  # 응답상세 — array

class CompProgramTradeDailyExecutor(ApiExecutor[CompProgramTradeDailyRequest, CompProgramTradeDailyResponse]):
    """프로그램매매 종합현황(일별)[국내주식-115]."""

    # 프로그램매매 종합현황(일별) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0460] 프로그램매매 종합현황 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. * 8개월 이상 과거 조회는 불가하며 에러메시지가 발생합니다.

    PATH = "/uapi/domestic-stock/v1/quotations/comp-program-trade-daily"
    METHOD = "GET"
    RESPONSE_TYPE = CompProgramTradeDailyResponse
    TR_ID = "FHPPG04600001"
