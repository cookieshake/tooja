"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OrderRvsecnclRequest(KisBaseModel):
    """요청."""

    ORD_PRCS_DVSN_CD: str  # 주문처리구분코드 — 02 : 주문전송
    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    RVSE_CNCL_DVSN_CD: str  # 정정취소구분코드 — 01 : 정정 02 : 취소
    ORGN_ODNO: str  # 원주문번호 — 정정 혹은 취소할 주문의 번호
    ORD_QTY: str  # 주문수량 — [Header tr_id TTTO1103U(선물옵션 정정취소 주간)] 전량일경우 0으로 입력 [Header tr_id JTCE1002U(선물옵션 정정취소 야간)] 일부수량 정정 및 취소 불가, 주문수량 반드시 입력 (공백 불가) 일부 미체
    UNIT_PRICE: str  # 주문가격1 — 시장가나 최유리의 경우 0으로 입력 (취소 시에도 0 입력)
    NMPR_TYPE_CD: str  # 호가유형코드 — 01 : 지정가 02 : 시장가 03 : 조건부 04 : 최유리
    KRX_NMPR_CNDT_CD: str  # 한국거래소호가조건코드 — 취소시 0으로 입력 정정시 0 : 없음 3 : IOC 4 : FOK
    RMN_QTY_YN: str  # 잔여수량여부 — Y : 전량 N : 일부
    FUOP_ITEM_DVSN_CD: str | None = None  # 선물옵션종목구분코드 — [Header tr_id TTTO1103U(선물옵션 정정취소 주간)] 공란(Default) [Header tr_id JTCE1002U(선물옵션 정정취소 야간)] 01 : 선물 02 : 콜옵션 03 : 풋옵션 04 : 스프레드
    ORD_DVSN_CD: str  # 주문구분코드 — [정정] 01 : 지정가 02 : 시장가 03 : 조건부 04 : 최유리, 10 : 지정가(IOC) 11 : 지정가(FOK) 12 : 시장가(IOC) 13 : 시장가(FOK) 14 : 최유리(IOC) 15 : 최유리(FOK) [취소] 

class OrderRvsecnclResponse_OutputItem(KisBaseModel):
    """nested item."""

    ACNT_NAME: str | None = None  # 계좌명 — 계좌의 고객명
    TRAD_DVSN_NAME: str | None = None  # 매매구분명 — 매도/매수 등 구분값
    ITEM_NAME: str | None = None  # 종목명 — 주문 종목 명칭
    ORD_TMD: str | None = None  # 주문시각 — 주문 접수 시간
    ORD_GNO_BRNO: str | None = None  # 주문채번지점번호 — 계좌 개설 시 관리점으로 선택한 영업점의 고유번호
    ORGN_ODNO: str | None = None  # 원주문번호 — 정정 또는 취소 대상 주문의 일련번호
    ODNO: str | None = None  # 주문번호 — 접수한 주문(정정 또는 취소)의 일련번호

class OrderRvsecnclResponse(KisCommonResponse):
    """응답 본문."""

    output: list[str] = []  # 응답상세

class OrderRvsecnclExecutor(ApiExecutor[OrderRvsecnclRequest, OrderRvsecnclResponse]):
    """선물옵션 정정취소주문[v1_국내선물-002]."""

    # 선물옵션 주문 건에 대하여 정정 및 취소하는 API입니다. 단, 이미 체결된 건은 정정 및 취소가 불가합니다. ※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다. (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...)

    PATH = "/uapi/domestic-futureoption/v1/trading/order-rvsecncl"
    METHOD = "POST"
    RESPONSE_TYPE = OrderRvsecnclResponse
    TR_ID = "TTTO1103U"
    TR_ID_VIRTUAL = "VTTO1103U"
