"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class ForeignMarginRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드

class ForeignMarginResponse_OutputItem(KisBaseModel):
    """nested item."""

    natn_name: str | None = None  # 국가명
    crcy_cd: str | None = None  # 통화코드
    frcr_dncl_amt1: str | None = None  # 외화예수금액
    ustl_buy_amt: str | None = None  # 미결제매수금액
    ustl_sll_amt: str | None = None  # 미결제매도금액
    frcr_rcvb_amt: str | None = None  # 외화미수금액
    frcr_mgn_amt: str | None = None  # 외화증거금액
    frcr_gnrl_ord_psbl_amt: str | None = None  # 외화일반주문가능금액
    frcr_ord_psbl_amt1: str | None = None  # 외화주문가능금액 — 원화주문가능환산금액
    itgr_ord_psbl_amt: str | None = None  # 통합주문가능금액
    bass_exrt: str | None = None  # 기준환율

class ForeignMarginResponse(KisCommonResponse):
    """응답 본문."""

    output: list[ForeignMarginResponse_OutputItem] = []  # 응답상세 — array

class ForeignMarginExecutor(ApiExecutor[ForeignMarginRequest, ForeignMarginResponse]):
    """해외증거금 통화별조회 [해외주식-035]."""

    # 해외증거금 통화별조회 API입니다. 한국투자 HTS(eFriend Plus) &gt; [7718] 해외주식 증거금상세 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/overseas-stock/v1/trading/foreign-margin"
    METHOD = "GET"
    RESPONSE_TYPE = ForeignMarginResponse
    TR_ID = "TTTC2101R"
