"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OrderRvsecnclRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    ORGN_ORD_DT: str  # 원주문일자 — 원 주문 시 출력되는 ORD_DT 값을 입력 (현지거래일)
    ORGN_ODNO: str  # 원주문번호 — 정정/취소시 주문번호(ODNO) 8자리를 문자열처럼 "0"을 포함해서 전송 (원 주문 시 출력된 ODNO 값 활용) (ex. ORGN_ODNO : 00360686)
    FM_LIMIT_ORD_PRIC: str | None = None  # FMLIMIT주문가격 — OTFM3002U(해외선물옵션주문정정)만 사용
    FM_STOP_ORD_PRIC: str | None = None  # FMSTOP주문가격 — OTFM3002U(해외선물옵션주문정정)만 사용
    FM_LQD_LMT_ORD_PRIC: str | None = None  # FM청산LIMIT주문가격 — OTFM3002U(해외선물옵션주문정정)만 사용
    FM_LQD_STOP_ORD_PRIC: str | None = None  # FM청산STOP주문가격 — OTFM3002U(해외선물옵션주문정정)만 사용
    FM_HDGE_ORD_SCRN_YN: str  # FM_HEDGE주문화면여부 — N
    FM_MKPR_CVSN_YN: str | None = None  # FM시장가전환여부 — OTFM3003U(해외선물옵션주문취소)만 사용 ※ FM_MKPR_CVSN_YN 항목에 'Y'로 설정하여 취소주문을 접수할 경우, 주문 취소확인이 들어오면 원장에서 시장가주문을 하나 또 내줌

class OrderRvsecnclResponse_OutputItem(KisBaseModel):
    """nested item."""

    ORD_DT: str | None = None  # 주문일자 — YYYYMMDD(ex. 20230811)
    ODNO: str | None = None  # 주문번호 — 접수한 주문의 일련번호(ex. 00360686) * 정정/취소시 문자열처럼 "0"을 포함해서 전송 (ex. ORGN_ODNO : 00360686)

class OrderRvsecnclResponse(KisCommonResponse):
    """응답 본문."""

    output: OrderRvsecnclResponse_OutputItem | None = None

class OrderRvsecnclExecutor(ApiExecutor[OrderRvsecnclRequest, OrderRvsecnclResponse]):
    """해외선물옵션 정정취소주문 [v1_해외선물-002, 003]."""

    # 해외선물옵션 정정취소주문 API 입니다. ※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다. (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...)

    PATH = "/uapi/overseas-futureoption/v1/trading/order-rvsecncl"
    METHOD = "POST"
    RESPONSE_TYPE = OrderRvsecnclResponse
    TR_ID = "OTFM3002U"
