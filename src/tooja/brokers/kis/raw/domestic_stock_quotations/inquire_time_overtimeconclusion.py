"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireTimeOvertimeconclusionRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — J : 주식, ETF, ETN
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목번호 (6자리) ETN의 경우, Q로 시작 (EX. Q500001)
    FID_HOUR_CLS_CODE: str  # 시간 구분 코드 — 1 : 시간외 (Default)

class InquireTimeOvertimeconclusionResponse_Output1Item(KisBaseModel):
    """nested item."""

    ovtm_untp_prpr: str | None = None  # 시간외 단일가 현재가
    ovtm_untp_prdy_vrss: str | None = None  # 시간외 단일가 전일 대비
    ovtm_untp_prdy_vrss_sign: str | None = None  # 시간외 단일가 전일 대비 부호
    ovtm_untp_prdy_ctrt: str | None = None  # 시간외 단일가 전일 대비율
    ovtm_untp_vol: str | None = None  # 시간외 단일가 거래량
    ovtm_untp_tr_pbmn: str | None = None  # 시간외 단일가 거래 대금
    ovtm_untp_mxpr: str | None = None  # 시간외 단일가 상한가
    ovtm_untp_llam: str | None = None  # 시간외 단일가 하한가
    ovtm_untp_oprc: str | None = None  # 시간외 단일가 시가2
    ovtm_untp_hgpr: str | None = None  # 시간외 단일가 최고가
    ovtm_untp_lwpr: str | None = None  # 시간외 단일가 최저가
    ovtm_untp_antc_cnpr: str | None = None  # 시간외 단일가 예상 체결가
    ovtm_untp_antc_cntg_vrss: str | None = None  # 시간외 단일가 예상 체결 대비
    ovtm_untp_antc_cntg_vrss_sign: str | None = None  # 시간외 단일가 예상 체결 대비
    ovtm_untp_antc_cntg_ctrt: str | None = None  # 시간외 단일가 예상 체결 대비율
    ovtm_untp_antc_vol: str | None = None  # 시간외 단일가 예상 거래량
    uplm_sign: str | None = None  # 상한 부호
    lslm_sign: str | None = None  # 하한 부호

class InquireTimeOvertimeconclusionResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_cntg_hour: str | None = None  # 주식 체결 시간
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    askp: str | None = None  # 매도호가
    bidp: str | None = None  # 매수호가
    acml_vol: str | None = None  # 누적 거래량
    cntg_vol: str | None = None  # 체결 거래량

class InquireTimeOvertimeconclusionResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireTimeOvertimeconclusionResponse_Output1Item | None = None  # 응답상세1 — 기본정보
    output2: list[InquireTimeOvertimeconclusionResponse_Output2Item] = []  # 응답상세2 — Array 시간별체결 정보

class InquireTimeOvertimeconclusionExecutor(ApiExecutor[InquireTimeOvertimeconclusionRequest, InquireTimeOvertimeconclusionResponse]):
    """주식현재가 시간외시간별체결[v1_국내주식-025]."""

    # 주식현재가 시간외시간별체결 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0231] 시간외 시간별체결의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-time-overtimeconclusion"
    METHOD = "GET"
    RESPONSE_TYPE = InquireTimeOvertimeconclusionResponse
    TR_ID = "FHPST02310000"
