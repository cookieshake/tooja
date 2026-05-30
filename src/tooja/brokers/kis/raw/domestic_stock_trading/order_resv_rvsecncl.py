"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OrderResvRvsecnclRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — [정정/취소] 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — [정정/취소] 계좌번호 체계(8-2)의 뒤 2자리
    PDNO: str  # 종목코드(6자리) — [정정]
    ORD_QTY: str  # 주문수량 — [정정] 주문주식수
    ORD_UNPR: str  # 주문단가 — [정정] 1주당 가격 * 장전 시간외, 시장가의 경우 1주당 가격을 공란으로 비우지 않음 "0"으로 입력 권고
    SLL_BUY_DVSN_CD: str  # 매도매수구분코드 — [정정] 01 : 매도 02 : 매수
    ORD_DVSN_CD: str  # 주문구분코드 — [정정] 00 : 지정가 01 : 시장가 02 : 조건부지정가 05 : 장전 시간외
    ORD_OBJT_CBLC_DVSN_CD: str  # 주문대상잔고구분코드 — [정정] 10 : 현금 12 : 주식담보대출 14 : 대여상환 21 : 자기융자신규 22 : 유통대주신규 23 : 유통융자신규 24 : 자기대주신규 25 : 자기융자상환 26 : 유통대주상환 27 : 유통융자상환 28 : 자기대
    LOAN_DT: str | None = None  # 대출일자 — [정정]
    RSVN_ORD_END_DT: str | None = None  # 예약주문종료일자 — [정정]
    CTAL_TLNO: str | None = None  # 연락전화번호 — [정정]
    RSVN_ORD_SEQ: str  # 예약주문순번 — [정정/취소]
    RSVN_ORD_ORGNO: str | None = None  # 예약주문조직번호 — [정정/취소]
    RSVN_ORD_ORD_DT: str | None = None  # 예약주문주문일자 — [정정/취소]

class OrderResvRvsecnclResponse_OutputItem(KisBaseModel):
    """nested item."""

    nrml_prcs_yn: str | None = None  # 정상처리여부

class OrderResvRvsecnclResponse(KisCommonResponse):
    """응답 본문."""

    msg: str | None = None  # 응답메세지
    output: list[str] = []  # 응답상세

class OrderResvRvsecnclExecutor(ApiExecutor[OrderResvRvsecnclRequest, OrderResvRvsecnclResponse]):
    """주식예약주문정정취소[v1_국내주식-018,019]."""

    # 국내주식 예약주문 정정/취소 API 입니다. * 정정주문은 취소주문에 비해 필수 입력값이 추가 됩니다. 하단의 입력값을 참조하시기 바랍니다. ※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다. (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...)

    PATH = "/uapi/domestic-stock/v1/trading/order-resv-rvsecncl"
    METHOD = "POST"
    RESPONSE_TYPE = OrderResvRvsecnclResponse
    TR_ID = "CTSC0009U"
