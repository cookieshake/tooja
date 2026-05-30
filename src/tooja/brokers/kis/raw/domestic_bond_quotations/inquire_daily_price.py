"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireDailyPriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — B (업종코드)
    FID_INPUT_ISCD: str  # 입력종목코드 — 채권종목코드(ex KR2033022D33)

class InquireDailyPriceResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식영업일자
    bond_prpr: str | None = None  # 채권현재가
    bond_prdy_vrss: str | None = None  # 채권전일대비
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_ctrt: str | None = None  # 전일대비율
    acml_vol: str | None = None  # 누적거래량
    bond_oprc: str | None = None  # 채권시가2
    bond_hgpr: str | None = None  # 채권고가
    bond_lwpr: str | None = None  # 채권저가

class InquireDailyPriceResponse(KisCommonResponse):
    """응답 본문."""

    output: InquireDailyPriceResponse_OutputItem | None = None  # 응답상세

class InquireDailyPriceExecutor(ApiExecutor[InquireDailyPriceRequest, InquireDailyPriceResponse]):
    """장내채권현재가(일별) [국내주식-202]."""

    # 장내채권현재가(일별) API입니다. 장내채권의 일별 시세데이터를 최근 100건까지 확인할 수 있습니다.

    PATH = "/uapi/domestic-bond/v1/quotations/inquire-daily-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquireDailyPriceResponse
    TR_ID = "FHKBJ773404C0"
