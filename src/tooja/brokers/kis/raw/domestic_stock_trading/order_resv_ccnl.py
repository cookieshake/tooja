"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OrderResvCcnlRequest(KisBaseModel):
    """요청."""

    RSVN_ORD_ORD_DT: str  # 예약주문시작일자
    RSVN_ORD_END_DT: str  # 예약주문종료일자
    RSVN_ORD_SEQ: str  # 예약주문순번
    TMNL_MDIA_KIND_CD: str  # 단말매체종류코드 — "00" 입력
    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    PRCS_DVSN_CD: str  # 처리구분코드 — 0: 전체 1: 처리내역 2: 미처리내역
    CNCL_YN: str  # 취소여부 — "Y" 유효한 주문만 조회
    PDNO: str  # 상품번호 — 종목코드(6자리) (공백 입력 시 전체 조회)
    SLL_BUY_DVSN_CD: str  # 매도매수구분코드
    CTX_AREA_FK200: str  # 연속조회검색조건200 — 다음 페이지 조회시 사용
    CTX_AREA_NK200: str  # 연속조회키200 — 다음 페이지 조회시 사용

class OrderResvCcnlResponse_OutputItem(KisBaseModel):
    """nested item."""

    rsvn_ord_seq: str | None = None  # 예약주문 순번
    rsvn_ord_ord_dt: str | None = None  # 예약주문주문일자
    rsvn_ord_rcit_dt: str | None = None  # 예약주문접수일자
    pdno: str | None = None  # 상품번호
    ord_dvsn_cd: str | None = None  # 주문구분코드
    ord_rsvn_qty: str | None = None  # 주문예약수량
    tot_ccld_qty: str | None = None  # 총체결수량
    cncl_ord_dt: str | None = None  # 취소주문일자
    ord_tmd: str | None = None  # 주문시각
    ctac_tlno: str | None = None  # 연락전화번호
    rjct_rson2: str | None = None  # 거부사유2
    odno: str | None = None  # 주문번호
    rsvn_ord_rcit_tmd: str | None = None  # 예약주문접수시각
    kor_item_shtn_name: str | None = None  # 한글종목단축명
    sll_buy_dvsn_cd: str | None = None  # 매도매수구분코드
    ord_rsvn_unpr: str | None = None  # 주문예약단가
    tot_ccld_amt: str | None = None  # 총체결금액
    loan_dt: str | None = None  # 대출일자
    cncl_rcit_tmd: str | None = None  # 취소접수시각
    prcs_rslt: str | None = None  # 처리결과
    ord_dvsn_name: str | None = None  # 주문구분명
    tmnl_mdia_kind_cd: str | None = None  # 단말매체종류코드
    rsvn_end_dt: str | None = None  # 예약종료일자

class OrderResvCcnlResponse(KisCommonResponse):
    """응답 본문."""

    output: list[str] = []  # 응답상세

class OrderResvCcnlExecutor(ApiExecutor[OrderResvCcnlRequest, OrderResvCcnlResponse]):
    """주식예약주문조회[v1_국내주식-020]."""

    # 국내예약주문 처리내역 조회 API 입니다. 실전계좌/모의계좌의 경우, 한 번의 호출에 최대 20건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다.

    PATH = "/uapi/domestic-stock/v1/trading/order-resv-ccnl"
    METHOD = "GET"
    RESPONSE_TYPE = OrderResvCcnlResponse
    TR_ID = "CTSC0004R"
