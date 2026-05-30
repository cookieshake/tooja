"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OvertimeFluctuationRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — 시장구분코드 (J: 주식)
    FID_MRKT_CLS_CODE: str  # 시장 구분 코드 — 공백 입력
    FID_COND_SCR_DIV_CODE: str  # 조건 화면 분류 코드 — Unique key(20234)
    FID_INPUT_ISCD: str  # 입력 종목코드 — 0000(전체), 0001(코스피), 1001(코스닥)
    FID_DIV_CLS_CODE: str  # 분류 구분 코드 — 1(상한가), 2(상승률), 3(보합),4(하한가),5(하락률)
    FID_INPUT_PRICE_1: str  # 입력 가격1 — 입력값 없을때 전체 (가격 ~)
    FID_INPUT_PRICE_2: str  # 입력 가격2 — 입력값 없을때 전체 (~ 가격)
    FID_VOL_CNT: str  # 거래량 수 — 입력값 없을때 전체 (거래량 ~)
    FID_TRGT_CLS_CODE: str  # 대상 구분 코드 — 공백 입력
    FID_TRGT_EXLS_CLS_CODE: str  # 대상 제외 구분 코드 — 공백 입력

class OvertimeFluctuationResponse_Output1Item(KisBaseModel):
    """nested item."""

    ovtm_untp_uplm_issu_cnt: str | None = None  # 시간외 단일가 상한 종목 수
    ovtm_untp_ascn_issu_cnt: str | None = None  # 시간외 단일가 상승 종목 수
    ovtm_untp_stnr_issu_cnt: str | None = None  # 시간외 단일가 보합 종목 수
    ovtm_untp_lslm_issu_cnt: str | None = None  # 시간외 단일가 하한 종목 수
    ovtm_untp_down_issu_cnt: str | None = None  # 시간외 단일가 하락 종목 수
    ovtm_untp_acml_vol: str | None = None  # 시간외 단일가 누적 거래량
    ovtm_untp_acml_tr_pbmn: str | None = None  # 시간외 단일가 누적 거래대금
    ovtm_untp_exch_vol: str | None = None  # 시간외 단일가 거래소 거래량
    ovtm_untp_exch_tr_pbmn: str | None = None  # 시간외 단일가 거래소 거래대금
    ovtm_untp_kosdaq_vol: str | None = None  # 시간외 단일가 KOSDAQ 거래량
    ovtm_untp_kosdaq_tr_pbmn: str | None = None  # 시간외 단일가 KOSDAQ 거래대금

class OvertimeFluctuationResponse_Output2Item(KisBaseModel):
    """nested item."""

    mksc_shrn_iscd: str | None = None  # 유가증권 단축 종목코드
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    ovtm_untp_prpr: str | None = None  # 시간외 단일가 현재가
    ovtm_untp_prdy_vrss: str | None = None  # 시간외 단일가 전일 대비
    ovtm_untp_prdy_vrss_sign: str | None = None  # 시간외 단일가 전일 대비 부호
    ovtm_untp_prdy_ctrt: str | None = None  # 시간외 단일가 전일 대비율
    ovtm_untp_askp1: str | None = None  # 시간외 단일가 매도호가1
    ovtm_untp_seln_rsqn: str | None = None  # 시간외 단일가 매도 잔량
    ovtm_untp_bidp1: str | None = None  # 시간외 단일가 매수호가1
    ovtm_untp_shnu_rsqn: str | None = None  # 시간외 단일가 매수 잔량
    ovtm_untp_vol: str | None = None  # 시간외 단일가 거래량
    ovtm_vrss_acml_vol_rlim: str | None = None  # 시간외 대비 누적 거래량 비중
    stck_prpr: str | None = None  # 주식 현재가
    acml_vol: str | None = None  # 누적 거래량
    bidp: str | None = None  # 매수호가
    askp: str | None = None  # 매도호가

class OvertimeFluctuationResponse(KisCommonResponse):
    """응답 본문."""

    output1: OvertimeFluctuationResponse_Output1Item | None = None  # 응답상세
    output2: list[OvertimeFluctuationResponse_Output2Item] = []  # 응답상세 — array

class OvertimeFluctuationExecutor(ApiExecutor[OvertimeFluctuationRequest, OvertimeFluctuationResponse]):
    """국내주식 시간외등락율순위 [국내주식-138]."""

    # 국내주식 시간외등락율순위 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0234] 시간외 등락률순위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 최대 30건 확인 가능하며, 다음 조회가 불가합니다.

    PATH = "/uapi/domestic-stock/v1/ranking/overtime-fluctuation"
    METHOD = "GET"
    RESPONSE_TYPE = OvertimeFluctuationResponse
    TR_ID = "FHPST02340000"
