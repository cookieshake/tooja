"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireDailyOvertimepriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # FID 조건 시장 분류 코드 — J : 주식, ETF, ETN
    FID_INPUT_ISCD: str  # FID 입력 종목코드 — 종목번호 (6자리) ETN의 경우, Q로 시작 (EX. Q500001)

class InquireDailyOvertimepriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    ovtm_untp_prpr: str | None = None  # 시간외 단일가 현재가
    ovtm_untp_prdy_vrss: str | None = None  # 시간외 단일가 전일 대비
    ovtm_untp_prdy_vrss_sign: str | None = None  # 시간외 단일가 전일 대비 부호
    ovtm_untp_prdy_ctrt: str | None = None  # 시간외 단일가 전일 대비율 — 11(8.2)
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
    ovtm_untp_antc_cntg_ctrt: str | None = None  # 시간외 단일가 예상 체결 대비율 — 11(8.2)
    ovtm_untp_antc_vol: str | None = None  # 시간외 단일가 예상 거래량

class InquireDailyOvertimepriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자
    ovtm_untp_prpr: str | None = None  # 시간외 단일가 현재가
    ovtm_untp_prdy_vrss: str | None = None  # 시간외 단일가 전일 대비
    ovtm_untp_prdy_vrss_sign: str | None = None  # 시간외 단일가 전일 대비 부호
    ovtm_untp_prdy_ctrt: str | None = None  # 시간외 단일가 전일 대비율 — 11(8.2)
    ovtm_untp_vol: str | None = None  # 시간외 단일가 거래량
    stck_clpr: str | None = None  # 주식 종가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율 — 11(8.2)
    acml_vol: str | None = None  # 누적 거래량
    ovtm_untp_tr_pbmn: str | None = None  # 시간외 단일가 거래대금

class InquireDailyOvertimepriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireDailyOvertimepriceResponse_Output1Item | None = None  # 응답상세1 — 기본정보
    output2: list[InquireDailyOvertimepriceResponse_Output2Item] = []  # 응답상세2 — Array 일자별 정보

class InquireDailyOvertimepriceExecutor(ApiExecutor[InquireDailyOvertimepriceRequest, InquireDailyOvertimepriceResponse]):
    """주식현재가 시간외일자별주가[v1_국내주식-026]."""

    # 주식현재가 시간외일자별주가 API입니다. (최근일 30건만 조회 가능) 한국투자 HTS(eFriend Plus) &gt; [0232] 시간외 일자별주가의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-daily-overtimeprice"
    METHOD = "GET"
    RESPONSE_TYPE = InquireDailyOvertimepriceResponse
    TR_ID = "FHPST02320000"
