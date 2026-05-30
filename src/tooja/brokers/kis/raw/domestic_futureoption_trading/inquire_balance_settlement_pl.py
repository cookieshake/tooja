"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireBalanceSettlementPlRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    INQR_DT: str  # 조회일자 — 조회일자(YYYYMMDD)
    CTX_AREA_FK200: str  # 연속조회검색조건200
    CTX_AREA_NK200: str  # 연속조회키200

class InquireBalanceSettlementPlResponse_Output2Item(KisBaseModel):
    """nested item."""

    nxdy_dnca: str | None = None  # 익일예수금
    mmga_cash: str | None = None  # 유지증거금현금
    brkg_mgna_cash: str | None = None  # 위탁증거금현금
    opt_buy_chgs: str | None = None  # 옵션매수대금
    opt_lqd_evlu_amt: str | None = None  # 옵션청산평가금액
    dnca_sbst: str | None = None  # 예수금대용
    mmga_tota: str | None = None  # 유지증거금총액
    brkg_mgna_tota: str | None = None  # 위탁증거금총액
    opt_sll_chgs: str | None = None  # 옵션매도대금
    fee: str | None = None  # 수수료
    thdt_dfpa: str | None = None  # 당일차금
    rnwl_dfpa: str | None = None  # 갱신차금
    dnca_cash: str | None = None  # 예수금현금

class InquireBalanceSettlementPlResponse_Output1Item(KisBaseModel):
    """nested item."""

    pdno: str | None = None  # 상품번호
    prdt_name: str | None = None  # 상품명
    trad_dvsn_name: str | None = None  # 매매구분명
    bfdy_cblc_qty: str | None = None  # 전일잔고수량
    new_qty: str | None = None  # 신규수량
    mnpl_rpch_qty: str | None = None  # 전매환매수량
    cblc_qty: str | None = None  # 잔고수량
    cblc_amt: str | None = None  # 잔고금액
    trad_pfls_amt: str | None = None  # 매매손익금액
    evlu_amt: str | None = None  # 평가금액
    evlu_pfls_amt: str | None = None  # 평가손익금액

class InquireBalanceSettlementPlResponse(KisCommonResponse):
    """응답 본문."""

    output2: InquireBalanceSettlementPlResponse_Output2Item | None = None  # 응답상세
    output1: list[str] = []  # 응답상세2 — array

class InquireBalanceSettlementPlExecutor(ApiExecutor[InquireBalanceSettlementPlRequest, InquireBalanceSettlementPlResponse]):
    """선물옵션 잔고정산손익내역[v1_국내선물-013]."""

    # 선물옵션 잔고정산손익내역 API입니다.

    PATH = "/uapi/domestic-futureoption/v1/trading/inquire-balance-settlement-pl"
    METHOD = "GET"
    RESPONSE_TYPE = InquireBalanceSettlementPlResponse
    TR_ID = "CTFO6117R"
