"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireViStatusRequest(KisBaseModel):
    """요청."""

    FID_DIV_CLS_CODE: str  # FID 분류 구분 코드 — 0:전체 1:상승 2:하락
    FID_COND_SCR_DIV_CODE: str  # FID 조건 화면 분류 코드 — 20139
    FID_MRKT_CLS_CODE: str  # FID 시장 구분 코드 — 0:전체 K:거래소 Q:코스닥
    FID_INPUT_ISCD: str  # FID 입력 종목코드
    FID_RANK_SORT_CLS_CODE: str  # FID 순위 정렬 구분 코드 — 0:전체1:정적2:동적3:정적&동적
    FID_INPUT_DATE_1: str  # FID 입력 날짜1 — 영업일
    FID_TRGT_CLS_CODE: str  # FID 대상 구분 코드
    FID_TRGT_EXLS_CLS_CODE: str  # FID 대상 제외 구분 코드

class InquireViStatusResponse_OutputItem(KisBaseModel):
    """nested item."""

    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    mksc_shrn_iscd: str | None = None  # 유가증권 단축 종목코드
    vi_cls_code: str | None = None  # VI발동상태 — Y: 발동 / N: 해제
    bsop_date: str | None = None  # 영업 일자
    cntg_vi_hour: str | None = None  # VI발동시간
    vi_cncl_hour: str | None = None  # VI해제시간
    vi_kind_code: str | None = None  # VI종류코드 — 1:정적 2:동적 3:정적&동적
    vi_prc: str | None = None  # VI발동가격
    vi_stnd_prc: str | None = None  # 정적VI발동기준가격
    vi_dprt: str | None = None  # 정적VI발동괴리율 — %
    vi_dmc_stnd_prc: str | None = None  # 동적VI발동기준가격
    vi_dmc_dprt: str | None = None  # 동적VI발동괴리율 — %
    vi_count: str | None = None  # VI발동횟수

class InquireViStatusResponse(KisCommonResponse):
    """응답 본문."""

    output: InquireViStatusResponse_OutputItem | None = None  # 응답상세

class InquireViStatusExecutor(ApiExecutor[InquireViStatusRequest, InquireViStatusResponse]):
    """변동성완화장치(VI) 현황 [v1_국내주식-055]."""

    # HTS(eFriend Plus) [0139] 변동성 완화장치(VI) 현황 데이터를 확인할 수 있는 API입니다. 최근 30건까지 확인 가능합니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-vi-status"
    METHOD = "GET"
    RESPONSE_TYPE = InquireViStatusResponse
    TR_ID = "FHPST01390000"
