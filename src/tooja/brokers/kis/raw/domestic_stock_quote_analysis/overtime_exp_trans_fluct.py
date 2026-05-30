"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OvertimeExpTransFluctRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — 시장구분코드 (J: 주식)
    FID_COND_SCR_DIV_CODE: str  # 조건 화면 분류 코드 — Unique key(11186)
    FID_INPUT_ISCD: str  # 입력 종목코드 — 0000(전체), 0001(코스피), 1001(코스닥)
    FID_RANK_SORT_CLS_CODE: str  # 순위 정렬 구분 코드 — 0(상승률), 1(상승폭), 2(보합), 3(하락률), 4(하락폭)
    FID_DIV_CLS_CODE: str  # 분류 구분 코드 — '0(전체), 1(관리종목), 2(투자주의), 3(투자경고), 4(투자위험예고), 5(투자위험), 6(보통주), 7(우선주)'
    FID_INPUT_PRICE_1: str  # 입력 가격1 — 가격 ~
    FID_INPUT_PRICE_2: str  # 입력 가격2 — 공백
    FID_INPUT_VOL_1: str  # 입력 거래량 — 거래량 ~

class OvertimeExpTransFluctResponse_OutputItem(KisBaseModel):
    """nested item."""

    data_rank: str | None = None  # 데이터 순위
    iscd_stat_cls_code: str | None = None  # 종목 상태 구분 코드
    stck_shrn_iscd: str | None = None  # 주식 단축 종목코드
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    ovtm_untp_antc_cnpr: str | None = None  # 시간외 단일가 예상 체결가
    ovtm_untp_antc_cntg_vrss: str | None = None  # 시간외 단일가 예상 체결 대비
    ovtm_untp_antc_cntg_vrsssign: str | None = None  # 시간외 단일가 예상 체결 대비
    ovtm_untp_antc_cntg_ctrt: str | None = None  # 시간외 단일가 예상 체결 대비율
    ovtm_untp_askp_rsqn1: str | None = None  # 시간외 단일가 매도호가 잔량1
    ovtm_untp_bidp_rsqn1: str | None = None  # 시간외 단일가 매수호가 잔량1
    ovtm_untp_antc_cnqn: str | None = None  # 시간외 단일가 예상 체결량
    itmt_vol: str | None = None  # 장중 거래량
    stck_prpr: str | None = None  # 주식 현재가

class OvertimeExpTransFluctResponse(KisCommonResponse):
    """응답 본문."""

    output: OvertimeExpTransFluctResponse_OutputItem | None = None  # 응답상세

class OvertimeExpTransFluctExecutor(ApiExecutor[OvertimeExpTransFluctRequest, OvertimeExpTransFluctResponse]):
    """국내주식 시간외예상체결등락률 [국내주식-140]."""

    # 국내주식 시간외예상체결등락률 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0236] 시간외 예상체결등락률 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/ranking/overtime-exp-trans-fluct"
    METHOD = "GET"
    RESPONSE_TYPE = OvertimeExpTransFluctResponse
    TR_ID = "FHKST11860000"
