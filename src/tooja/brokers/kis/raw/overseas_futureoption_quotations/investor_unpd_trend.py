"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InvestorUnpdTrendRequest(KisBaseModel):
    """요청."""

    PROD_ISCD: str  # 상품 — 금리 (GE, ZB, ZF,ZN,ZT), 금속(GC, PA, PL,SI, HG), 농산물(CC, CT,KC, OJ, SB, ZC,ZL, ZM, ZO, ZR, ZS, ZW), 에너지(CL, HO, NG, WBS), 지수(ES, NQ, TF, Y
    BSOP_DATE: str  # 일자 — 기준일(ex)20240513)
    UPMU_GUBUN: str  # 구분 — 0(수량), 1(증감)
    CTS_KEY: str  # CTS_KEY — 공백

class InvestorUnpdTrendResponse_Output1Item(KisBaseModel):
    """nested item."""

    row_cnt: str | None = None  # 응답레코드카운트

class InvestorUnpdTrendResponse_Output2Item(KisBaseModel):
    """nested item."""

    prod_iscd: str | None = None  # 상품
    cftc_iscd: str | None = None  # CFTC코드
    bsop_date: str | None = None  # 일자
    bidp_spec: str | None = None  # 매수투기
    askp_spec: str | None = None  # 매도투기
    spread_spec: str | None = None  # 스프레드투기
    bidp_hedge: str | None = None  # 매수헤지
    askp_hedge: str | None = None  # 매도헤지
    hts_otst_smtn: str | None = None  # 미결제합계
    bidp_missing: str | None = None  # 매수누락
    askp_missing: str | None = None  # 매도누락
    bidp_spec_cust: str | None = None  # 매수투기고객
    askp_spec_cust: str | None = None  # 매도투기고객
    spread_spec_cust: str | None = None  # 스프레드투기고객
    bidp_hedge_cust: str | None = None  # 매수헤지고객
    askp_hedge_cust: str | None = None  # 매도헤지고객
    cust_smtn: str | None = None  # 고객합계

class InvestorUnpdTrendResponse(KisCommonResponse):
    """응답 본문."""

    output1: InvestorUnpdTrendResponse_Output1Item | None = None  # 응답상세
    output2: list[InvestorUnpdTrendResponse_Output2Item] = []  # 응답상세 — array

class InvestorUnpdTrendExecutor(ApiExecutor[InvestorUnpdTrendRequest, InvestorUnpdTrendResponse]):
    """해외선물 미결제추이 [해외선물-029]."""

    # 해외선물 미결제추이 API입니다. 한국투자 HTS(eFriend Plus) &gt; [1959] 해외선물 미결제추이의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/overseas-futureoption/v1/quotations/investor-unpd-trend"
    METHOD = "GET"
    RESPONSE_TYPE = InvestorUnpdTrendResponse
    TR_ID = "HHDDB95030000"
