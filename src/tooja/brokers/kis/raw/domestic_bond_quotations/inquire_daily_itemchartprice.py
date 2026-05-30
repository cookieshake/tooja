"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireDailyItemchartpriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 구분 코드 — Unique key(B)
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목코드

class InquireDailyItemchartpriceResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식영업일자
    bond_oprc: str | None = None  # 채권시가2
    bond_hgpr: str | None = None  # 채권고가
    bond_lwpr: str | None = None  # 채권저가
    bond_prpr: str | None = None  # 채권현재가
    acml_vol: str | None = None  # 누적거래량

class InquireDailyItemchartpriceResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InquireDailyItemchartpriceResponse_OutputItem] = []  # 응답상세 — array

class InquireDailyItemchartpriceExecutor(ApiExecutor[InquireDailyItemchartpriceRequest, InquireDailyItemchartpriceResponse]):
    """장내채권 기간별시세(일) [국내주식-159]."""

    # 장내채권 기간별시세(일) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0979] 장내채권종합주문 화면 가운데 "일별" 클릭 시 시세 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 최근 30건까지 데이터 확인이 가능합니다.

    PATH = "/uapi/domestic-bond/v1/quotations/inquire-daily-itemchartprice"
    METHOD = "GET"
    RESPONSE_TYPE = InquireDailyItemchartpriceResponse
    TR_ID = "FHKBJ773701C0"
