"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OrderResvRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    PDNO: str  # 종목코드(6자리)
    ORD_QTY: str  # 주문수량 — 주문주식수
    ORD_UNPR: str  # 주문단가 — 1주당 가격 * 장전 시간외, 시장가의 경우 1주당 가격을 공란으로 비우지 않음 "0"으로 입력 권고
    SLL_BUY_DVSN_CD: str  # 매도매수구분코드 — 01 : 매도 02 : 매수
    ORD_DVSN_CD: str  # 주문구분코드 — 00 : 지정가 01 : 시장가 02 : 조건부지정가 05 : 장전 시간외
    ORD_OBJT_CBLC_DVSN_CD: str  # 주문대상잔고구분코드 — [매도매수구분코드 01:매도/02:매수시 사용] 10 : 현금 [매도매수구분코드 01:매도시 사용] 12 : 주식담보대출 14 : 대여상환 21 : 자기융자신규 22 : 유통대주신규 23 : 유통융자신규 24 : 자기대주신규 2
    LOAN_DT: str | None = None  # 대출일자
    RSVN_ORD_END_DT: str | None = None  # 예약주문종료일자 — (YYYYMMDD) 현재 일자보다 이후로 설정해야 함 * RSVN_ORD_END_DT(예약주문종료일자)를 안 넣으면 다음날 주문처리되고 예약주문은 종료됨 * RSVN_ORD_END_DT(예약주문종료일자)는 익영업일부터 달력일 기준으
    LDNG_DT: str | None = None  # 대여일자

class OrderResvResponse_OutputItem(KisBaseModel):
    """nested item."""

    rsvn_ord_seq: str | None = None  # 예약주문 순번

class OrderResvResponse(KisCommonResponse):
    """응답 본문."""

    msg: str | None = None  # 응답메세지
    output: list[OrderResvResponse_OutputItem] = []  # 응답상세 — Array

class OrderResvExecutor(ApiExecutor[OrderResvRequest, OrderResvResponse]):
    """주식예약주문[v1_국내주식-017]."""

    # 국내주식 예약주문 매수/매도 API 입니다. ※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다. (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...) ※ 유의사항 1. 예약주문 가능시간 : 15시 40분 ~ 다음 영업일 7시 30분 (단, 서버 초기화 작업 시 예약주문 불가 : 23시 40분 ~ 00시 10분) ※ 예약주문 처리내역은 통보되지 않으므로 주문처리

    PATH = "/uapi/domestic-stock/v1/trading/order-resv"
    METHOD = "POST"
    RESPONSE_TYPE = OrderResvResponse
    TR_ID = "CTSC0008U"
