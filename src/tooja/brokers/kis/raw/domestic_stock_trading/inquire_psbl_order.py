"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePsblOrderRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    PDNO: str  # 상품번호 — 종목번호(6자리) * PDNO, ORD_UNPR 공란 입력 시, 매수수량 없이 매수금액만 조회됨
    ORD_UNPR: str  # 주문단가 — 1주당 가격 * 시장가(ORD_DVSN:01)로 조회 시, 공란으로 입력 * PDNO, ORD_UNPR 공란 입력 시, 매수수량 없이 매수금액만 조회됨
    ORD_DVSN: str  # 주문구분 — * 특정 종목 전량매수 시 가능수량을 확인할 경우 00:지정가는 증거금율이 반영되지 않으므로 증거금율이 반영되는 01: 시장가로 조회 * 다만, 조건부지정가 등 특정 주문구분(ex.IOC)으로 주문 시 가능수량을 확인할 경우 주문 시와 동
    CMA_EVLU_AMT_ICLD_YN: str  # CMA평가금액포함여부 — Y : 포함 N : 포함하지 않음
    OVRS_ICLD_YN: str  # 해외포함여부 — Y : 포함 N : 포함하지 않음

class InquirePsblOrderResponse_OutputItem(KisBaseModel):
    """nested item."""

    ord_psbl_cash: str | None = None  # 주문가능현금 — 예수금으로 계산된 주문가능금액
    ord_psbl_sbst: str | None = None  # 주문가능대용
    ruse_psbl_amt: str | None = None  # 재사용가능금액 — 전일/금일 매도대금으로 계산된 주문가능금액
    fund_rpch_chgs: str | None = None  # 펀드환매대금
    psbl_qty_calc_unpr: str | None = None  # 가능수량계산단가
    nrcvb_buy_amt: str | None = None  # 미수없는매수금액 — 미수를 사용하지 않으실 경우 nrcvb_buy_amt(미수없는매수금액)을 확인
    nrcvb_buy_qty: str | None = None  # 미수없는매수수량 — 미수를 사용하지 않으실 경우 nrcvb_buy_qty(미수없는매수수량)을 확인 * 특정 종목 전량매수 시 가능수량을 확인하실 경우 조회 시 ORD_DVSN:01(시장가)로 지정 필수 * 다만, 조건부지정가 등 특정 주문구분(ex.I
    max_buy_amt: str | None = None  # 최대매수금액 — 미수를 사용하시는 경우 max_buy_amt(최대매수금액)를 확인
    max_buy_qty: str | None = None  # 최대매수수량 — 미수를 사용하시는 경우 max_buy_qty(최대매수수량)를 확인 * 특정 종목 전량매수 시 가능수량을 확인하실 경우 조회 시 ORD_DVSN:01(시장가)로 지정 필수 * 다만, 조건부지정가 등 특정 주문구분(ex.IOC)으로 주문 
    cma_evlu_amt: str | None = None  # CMA평가금액
    ovrs_re_use_amt_wcrc: str | None = None  # 해외재사용금액원화
    ord_psbl_frcr_amt_wcrc: str | None = None  # 주문가능외화금액원화

class InquirePsblOrderResponse(KisCommonResponse):
    """응답 본문."""

    output: InquirePsblOrderResponse_OutputItem | None = None  # 응답상세 — Single

class InquirePsblOrderExecutor(ApiExecutor[InquirePsblOrderRequest, InquirePsblOrderResponse]):
    """매수가능조회[v1_국내주식-007]."""

    # 매수가능 조회 API입니다. 실전계좌/모의계좌의 경우, 한 번의 호출에 최대 1건까지 확인 가능합니다. 1) 매수가능금액 확인 . 미수 사용 X: nrcvb_buy_amt(미수없는매수금액) 확인 . 미수 사용 O: max_buy_amt(최대매수금액) 확인 2) 매수가능수량 확인 . 특정 종목 전량매수 시 가능수량을 확인하실 경우 ORD_DVSN:00(지정가)는 종목증거금율이 반영되지 않습니다. 따라서 "반드시" ORD_DVSN

    PATH = "/uapi/domestic-stock/v1/trading/inquire-psbl-order"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePsblOrderResponse
    TR_ID = "TTTC8908R"
    TR_ID_VIRTUAL = "VTTC8908R"
