"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class CompInterestRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — Unique key(I)
    FID_COND_SCR_DIV_CODE: str  # 조건화면분류코드 — Unique key(20702)
    FID_DIV_CLS_CODE: str  # 분류구분코드 — 1: 해외금리지표
    FID_DIV_CLS_CODE1: str  # 분류구분코드 — 공백 : 전체

class CompInterestResponse_Output1Item(KisBaseModel):
    """nested item."""

    bcdt_code: str | None = None  # 자료코드
    hts_kor_isnm: str | None = None  # HTS한글종목명
    bond_mnrt_prpr: str | None = None  # 채권금리현재가
    prdy_vrss_sign: str | None = None  # 전일대비부호
    bond_mnrt_prdy_vrss: str | None = None  # 채권금리전일대비
    prdy_ctrt: str | None = None  # 전일대비율
    stck_bsop_date: str | None = None  # 주식영업일자

class CompInterestResponse_Output2Item(KisBaseModel):
    """nested item."""

    bcdt_code: str | None = None  # 자료코드
    hts_kor_isnm: str | None = None  # HTS한글종목명
    bond_mnrt_prpr: str | None = None  # 채권금리현재가
    prdy_vrss_sign: str | None = None  # 전일대비부호
    bond_mnrt_prdy_vrss: str | None = None  # 채권금리전일대비
    bstp_nmix_prdy_ctrt: str | None = None  # 업종지수전일대비율
    stck_bsop_date: str | None = None  # 주식영업일자

class CompInterestResponse(KisCommonResponse):
    """응답 본문."""

    output1: CompInterestResponse_Output1Item | None = None  # 응답상세 — array
    output2: list[CompInterestResponse_Output2Item] = []  # 응답상세 — array

class CompInterestExecutor(ApiExecutor[CompInterestRequest, CompInterestResponse]):
    """금리 종합(국내채권/금리) [국내주식-155]."""

    # 금리 종합(국내채권/금리) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0702] 금리 종합 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 11:30 이후에 신규데이터가 수신되는 점 참고하시기 바랍니다.

    PATH = "/uapi/domestic-stock/v1/quotations/comp-interest"
    METHOD = "GET"
    RESPONSE_TYPE = CompInterestResponse
    TR_ID = "FHPST07020000"
