"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OrderRequest(KisBaseModel):
    """요청."""

    ORD_PRCS_DVSN_CD: str  # 주문처리구분코드 — 02 : 주문전송
    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    SLL_BUY_DVSN_CD: str  # 매도매수구분코드 — 01 : 매도 02 : 매수
    SHTN_PDNO: str  # 단축상품번호 — 종목번호 선물 6자리 (예: A01603) 옵션 9자리 (예: B01603955)
    ORD_QTY: str  # 주문수량
    UNIT_PRICE: str  # 주문가격1 — 시장가나 최유리 지정가인 경우 0으로 입력
    NMPR_TYPE_CD: str | None = None  # 호가유형코드 — ※ ORD_DVSN_CD(주문구분코드)를 입력한 경우 ""(공란)으로 입력해도 됨 01 : 지정가 02 : 시장가 03 : 조건부 04 : 최유리
    KRX_NMPR_CNDT_CD: str | None = None  # 한국거래소호가조건코드 — ※ ORD_DVSN_CD(주문구분코드)를 입력한 경우 ""(공란)으로 입력해도 됨 0 : 없음 3 : IOC 4 : FOK
    CTAC_TLNO: str | None = None  # 연락전화번호 — 고객의 연락 가능한 전화번호
    FUOP_ITEM_DVSN_CD: str | None = None  # 선물옵션종목구분코드 — 공란(Default)
    ORD_DVSN_CD: str  # 주문구분코드 — 01 : 지정가 02 : 시장가 03 : 조건부 04 : 최유리, 10 : 지정가(IOC) 11 : 지정가(FOK) 12 : 시장가(IOC) 13 : 시장가(FOK) 14 : 최유리(IOC) 15 : 최유리(FOK)

class OrderResponse_OutputItem(KisBaseModel):
    """nested item."""

    ACNT_NAME: str | None = None  # 계좌명 — 계좌의 고객명
    TRAD_DVSN_NAME: str | None = None  # 매매구분명 — 매도/매수 등 구분값
    ITEM_NAME: str | None = None  # 종목명 — 주문 종목 명칭
    ORD_TMD: str | None = None  # 주문시각 — 주문 접수 시간
    ORD_GNO_BRNO: str | None = None  # 주문채번지점번호 — 계좌 개설 시 관리점으로 선택한 영업점의 고유번호
    ODNO: str | None = None  # 주문번호 — 접수한 주문의 일련번호

class OrderResponse(KisCommonResponse):
    """응답 본문."""

    output: list[str] = []  # 응답상세

class OrderExecutor(ApiExecutor[OrderRequest, OrderResponse]):
    """선물옵션 주문[v1_국내선물-001]."""

    # ​선물옵션 주문 API입니다. * 선물옵션 운영시간 외 API 호출 시 애러가 발생하오니 운영시간을 확인해주세요. ※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다. (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...) ※ 종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다. https://github.com/koreainvestm

    PATH = "/uapi/domestic-futureoption/v1/trading/order"
    METHOD = "POST"
    RESPONSE_TYPE = OrderResponse
    TR_ID = "TTTO1101U"
    TR_ID_VIRTUAL = "VTTO1101U"
