"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InvestorProgramTradeTodayRequest(KisBaseModel):
    """요청."""

    EXCH_DIV_CLS_CODE: str  # 거래소 구분 코드 — J : KRX, NX : NXT, UN : 통합
    MRKT_DIV_CLS_CODE: str  # 시장 구분 코드 — 1:코스피, 4:코스닥

class InvestorProgramTradeTodayResponse_Output1Item(KisBaseModel):
    """nested item."""

    invr_cls_code: str | None = None  # 투자자코드
    all_seln_qty: str | None = None  # 전체매도수량
    all_seln_amt: str | None = None  # 전체매도대금
    invr_cls_name: str | None = None  # 투자자 구분 명
    all_shnu_qty: str | None = None  # 전체매수수량
    all_shnu_amt: str | None = None  # 전체매수대금
    all_ntby_amt: str | None = None  # 전체순매수대금
    arbt_seln_qty: str | None = None  # 차익매도수량
    all_ntby_qty: str | None = None  # 전체순매수수량
    arbt_shnu_qty: str | None = None  # 차익매수수량
    arbt_ntby_qty: str | None = None  # 차익순매수수량
    arbt_seln_amt: str | None = None  # 차익매도대금
    arbt_shnu_amt: str | None = None  # 차익매수대금
    arbt_ntby_amt: str | None = None  # 차익순매수대금
    nabt_seln_qty: str | None = None  # 비차익매도수량
    nabt_shnu_qty: str | None = None  # 비차익매수수량
    nabt_ntby_qty: str | None = None  # 비차익순매수수량
    nabt_seln_amt: str | None = None  # 비차익매도대금
    nabt_shnu_amt: str | None = None  # 비차익매수대금
    nabt_ntby_amt: str | None = None  # 비차익순매수대금

class InvestorProgramTradeTodayResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[InvestorProgramTradeTodayResponse_Output1Item] = []  # 응답상세 — array

class InvestorProgramTradeTodayExecutor(ApiExecutor[InvestorProgramTradeTodayRequest, InvestorProgramTradeTodayResponse]):
    """프로그램매매 투자자매매동향(당일) [국내주식-116]."""

    # 프로그램매매 투자자매매동향(당일) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0466] 프로그램매매 투자자별 동향 화면 의 "당일동향" 표의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/investor-program-trade-today"
    METHOD = "GET"
    RESPONSE_TYPE = InvestorProgramTradeTodayResponse
    TR_ID = "HHPPG046600C1"
