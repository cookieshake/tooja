"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class CompProgramTradeTodayRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 시장 분류 코드 — KRX : J , NXT : NX, 통합 : UN
    FID_MRKT_CLS_CODE: str  # 시장 구분 코드 — K:코스피, Q:코스닥
    FID_SCTN_CLS_CODE: str  # 구간 구분 코드 — 공백 입력
    FID_INPUT_ISCD: str  # 입력 종목코드 — 공백 입력
    FID_COND_MRKT_DIV_CODE1: str  # 시장 분류코드1 — 공백 입력
    FID_INPUT_HOUR_1: str  # 입력 시간1 — 공백 입력

class CompProgramTradeTodayResponse_Output1Item(KisBaseModel):
    """nested item."""

    bsop_hour: str | None = None  # 영업 시간
    arbt_smtn_seln_tr_pbmn: str | None = None  # 차익 합계 매도 거래 대금
    arbt_smtm_seln_tr_pbmn_rate: str | None = None  # 차익 합계 매도 거래대금 비율
    arbt_smtn_shnu_tr_pbmn: str | None = None  # 차익 합계 매수2 거래 대금
    arbt_smtm_shun_tr_pbmn_rate: str | None = None  # 차익합계매수거래대금비율
    nabt_smtn_seln_tr_pbmn: str | None = None  # 비차익 합계 매도 거래 대금
    nabt_smtm_seln_tr_pbmn_rate: str | None = None  # 비차익 합계 매도 거래대금 비율
    nabt_smtn_shnu_tr_pbmn: str | None = None  # 비차익 합계 매수2 거래 대금
    nabt_smtm_shun_tr_pbmn_rate: str | None = None  # 비차익합계매수거래대금비율
    arbt_smtn_ntby_tr_pbmn: str | None = None  # 차익 합계 순매수 거래 대금
    arbt_smtm_ntby_tr_pbmn_rate: str | None = None  # 차익 합계 순매수 거래대금 비율
    nabt_smtn_ntby_tr_pbmn: str | None = None  # 비차익 합계 순매수 거래 대금
    nabt_smtm_ntby_tr_pbmn_rate: str | None = None  # 비차익 합계 순매수 거래대금 비
    whol_smtn_ntby_tr_pbmn: str | None = None  # 전체 합계 순매수 거래 대금
    whol_ntby_tr_pbmn_rate: str | None = None  # 전체 순매수 거래대금 비율
    bstp_nmix_prpr: str | None = None  # 업종 지수 현재가
    bstp_nmix_prdy_vrss: str | None = None  # 업종 지수 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호

class CompProgramTradeTodayResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[CompProgramTradeTodayResponse_Output1Item] = []  # 응답상세 — array

class CompProgramTradeTodayExecutor(ApiExecutor[CompProgramTradeTodayRequest, CompProgramTradeTodayResponse]):
    """프로그램매매 종합현황(시간) [국내주식-114]."""

    # 프로그램매매 종합현황(시간) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0460] 프로그램매매 종합현황 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 장시간(09:00~15:30) 동안의 최근 30분간의 데이터 확인이 가능하며, 다음조회가 불가합니다. ※ 장시간(09:00~15:30) 이후에는 bsop_hour 에 153000 ~ 170000 까지의 시간데

    PATH = "/uapi/domestic-stock/v1/quotations/comp-program-trade-today"
    METHOD = "GET"
    RESPONSE_TYPE = CompProgramTradeTodayResponse
    TR_ID = "FHPPG04600101"
