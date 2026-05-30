"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class IndustryPriceRequest(KisBaseModel):
    """요청."""

    AUTH: str  # 사용자권한정보 — 공백
    EXCD: str  # 거래소코드 — 'NYS : 뉴욕, NAS : 나스닥, AMS : 아멕스 HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 '

class IndustryPriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    nrec: str | None = None  # RecordCount

class IndustryPriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    icod: str | None = None  # 업종코드
    name: str | None = None  # 업종명

class IndustryPriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: IndustryPriceResponse_Output1Item | None = None  # 응답상세
    output2: list[IndustryPriceResponse_Output2Item] = []  # 응답상세 — array

class IndustryPriceExecutor(ApiExecutor[IndustryPriceRequest, IndustryPriceResponse]):
    """해외주식 업종별코드조회[해외주식-049]."""

    # 해외주식 업종별코드조회 API입니다.

    PATH = "/uapi/overseas-price/v1/quotations/industry-price"
    METHOD = "GET"
    RESPONSE_TYPE = IndustryPriceResponse
    TR_ID = "HHDFS76370100"
