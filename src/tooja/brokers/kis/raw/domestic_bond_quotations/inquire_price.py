"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — B (업종코드)
    FID_INPUT_ISCD: str  # 입력종목코드 — 채권종목코드(ex KR2033022D33)

class InquirePriceResponse_OutputItem(KisBaseModel):
    """nested item."""

    stnd_iscd: str | None = None  # 표준종목코드
    hts_kor_isnm: str | None = None  # HTS한글종목명
    bond_prpr: str | None = None  # 채권현재가
    prdy_vrss_sign: str | None = None  # 전일대비부호
    bond_prdy_vrss: str | None = None  # 채권전일대비
    prdy_ctrt: str | None = None  # 전일대비율
    acml_vol: str | None = None  # 누적거래량
    bond_prdy_clpr: str | None = None  # 채권전일종가
    bond_oprc: str | None = None  # 채권시가2
    bond_hgpr: str | None = None  # 채권고가
    bond_lwpr: str | None = None  # 채권저가
    ernn_rate: str | None = None  # 수익비율
    oprc_ert: str | None = None  # 시가2수익률
    hgpr_ert: str | None = None  # 최고가수익률
    lwpr_ert: str | None = None  # 최저가수익률
    bond_mxpr: str | None = None  # 채권상한가
    bond_llam: str | None = None  # 채권하한가

class InquirePriceResponse(KisCommonResponse):
    """응답 본문."""

    output: InquirePriceResponse_OutputItem | None = None  # 응답상세

class InquirePriceExecutor(ApiExecutor[InquirePriceRequest, InquirePriceResponse]):
    """장내채권현재가(시세) [국내주식-200]."""

    # 장내채권현재가(시세) API입니다. 장내채권의 기본시세(시가,고가,저가,종가)를 확인할 수 있습니다.

    PATH = "/uapi/domestic-bond/v1/quotations/inquire-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePriceResponse
    TR_ID = "FHKBJ773400C0"
