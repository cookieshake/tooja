"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OrderRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    OVRS_FUTR_FX_PDNO: str  # 해외선물FX상품번호
    SLL_BUY_DVSN_CD: str  # 매도매수구분코드 — 01 : 매도 02 : 매수
    FM_LQD_USTL_CCLD_DT: str | None = None  # FM청산미결제체결일자 — 빈칸 (hedge청산만 이용)
    FM_LQD_USTL_CCNO: str | None = None  # FM청산미결제체결번호 — 빈칸 (hedge청산만 이용)
    PRIC_DVSN_CD: str  # 가격구분코드 — 1.지정, 2. 시장, 3. STOP, 4 S/L
    FM_LIMIT_ORD_PRIC: str  # FMLIMIT주문가격 — 지정가인 경우 가격 입력 * 시장가, STOP주문인 경우, 빈칸("") 입력
    FM_STOP_ORD_PRIC: str  # FMSTOP주문가격 — STOP 주문 가격 입력 * 시장가, 지정가인 경우, 빈칸("") 입력
    FM_ORD_QTY: str  # FM주문수량
    FM_LQD_LMT_ORD_PRIC: str | None = None  # FM청산LIMIT주문가격 — 빈칸 (hedge청산만 이용)
    FM_LQD_STOP_ORD_PRIC: str | None = None  # FM청산STOP주문가격 — 빈칸 (hedge청산만 이용)
    CCLD_CNDT_CD: str  # 체결조건코드 — 일반적으로 6 (EOD, 지정가) GTD인 경우 5, 시장가인 경우만 2
    CPLX_ORD_DVSN_CD: str  # 복합주문구분코드 — 0 (hedge청산만 이용)
    ECIS_RSVN_ORD_YN: str  # 행사예약주문여부 — N
    FM_HDGE_ORD_SCRN_YN: str  # FM_HEDGE주문화면여부 — N

class OrderResponse_OutputItem(KisBaseModel):
    """nested item."""

    ORD_DT: str | None = None  # 주문일자
    ODNO: str | None = None  # 주문번호 — 접수한 주문의 일련번호(ex. 00360686) * 정정/취소시 문자열처럼 "0"을 포함해서 전송 (ex. ORGN_ODNO : 00360686)

class OrderResponse(KisCommonResponse):
    """응답 본문."""

    output: OrderResponse_OutputItem | None = None

class OrderExecutor(ApiExecutor[OrderRequest, OrderResponse]):
    """해외선물옵션 주문 [v1_해외선물-001]."""

    # 해외선물옵션 주문 API 입니다. ※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다. (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...) ※ 종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다. https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info

    PATH = "/uapi/overseas-futureoption/v1/trading/order"
    METHOD = "POST"
    RESPONSE_TYPE = OrderResponse
    TR_ID = "OTFM3001U"
