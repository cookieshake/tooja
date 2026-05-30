"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InvestorTrendEstimateRequest(KisBaseModel):
    """요청."""

    MKSC_SHRN_ISCD: str  # 종목코드

class InvestorTrendEstimateResponse_Output2Item(KisBaseModel):
    """nested item."""

    bsop_hour_gb: str | None = None  # 입력구분 — 1: 09시 30분 입력 2: 10시 00분 입력 3: 11시 20분 입력 4: 13시 20분 입력 5: 14시 30분 입력
    frgn_fake_ntby_qty: str | None = None  # 외국인수량(가집계)
    orgn_fake_ntby_qty: str | None = None  # 기관수량(가집계)
    sum_fake_ntby_qty: str | None = None  # 합산수량(가집계)

class InvestorTrendEstimateResponse(KisCommonResponse):
    """응답 본문."""

    output2: list[InvestorTrendEstimateResponse_Output2Item] = []  # 응답상세 — Array

class InvestorTrendEstimateExecutor(ApiExecutor[InvestorTrendEstimateRequest, InvestorTrendEstimateResponse]):
    """종목별 외인기관 추정가집계[v1_국내주식-046]."""

    # 국내주식 종목별 외국인, 기관 추정가집계 API입니다. 한국투자 MTS &gt; 국내 현재가 &gt; 투자자 &gt; 투자자동향 탭 &gt; 왼쪽구분을 '추정(주)'로 선택 시 확인 가능한 데이터를 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 증권사 직원이 장중에 집계/입력한 자료를 단순 누계한 수치로서, 입력시간은 외국인 09:30, 11:20, 13:20, 14:30 / 기관종합 10:00,

    PATH = "/uapi/domestic-stock/v1/quotations/investor-trend-estimate"
    METHOD = "GET"
    RESPONSE_TYPE = InvestorTrendEstimateResponse
    TR_ID = "HHPTJ04160200"
