"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePsblSellRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드
    PDNO: str  # 종목번호 — 보유종목 코드 ex)000660

class InquirePsblSellResponse_Output1Item(KisBaseModel):
    """nested item."""

    pdno: str | None = None  # 상품번호
    prdt_name: str | None = None  # 상품명
    buy_qty: str | None = None  # 매수수량
    sll_qty: str | None = None  # 매도수량
    cblc_qty: str | None = None  # 잔고수량
    nsvg_qty: str | None = None  # 비저축수량
    ord_psbl_qty: str | None = None  # 주문가능수량
    pchs_avg_pric: str | None = None  # 매입평균가격
    pchs_amt: str | None = None  # 매입금액
    now_pric: str | None = None  # 현재가
    evlu_amt: str | None = None  # 평가금액
    evlu_pfls_amt: str | None = None  # 평가손익금액
    evlu_pfls_rt: str | None = None  # 평가손익율

class InquirePsblSellResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquirePsblSellResponse_Output1Item | None = None  # 응답상세

class InquirePsblSellExecutor(ApiExecutor[InquirePsblSellRequest, InquirePsblSellResponse]):
    """매도가능수량조회 [국내주식-165]."""

    # 매도가능수량조회 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0971] 주식 매도 화면에서 종목코드 입력 후 "가능" 클릭 시 매도가능수량이 확인되는 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 특정종목 매도가능수량 확인 시, 매도주문 내시려는 주문종목(PDNO)으로 API 호출 후 output &gt; ord_psbl_qty(주문가능수량) 확인하실 수 있습니다.

    PATH = "/uapi/domestic-stock/v1/trading/inquire-psbl-sell"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePsblSellResponse
    TR_ID = "TTTC8408R"
