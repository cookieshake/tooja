"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePsblRvsecnclRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드
    ORD_DT: str  # 주문일자
    ODNO: str  # 주문번호
    CTX_AREA_FK200: str  # 연속조회검색조건200
    CTX_AREA_NK200: str  # 연속조회키200

class InquirePsblRvsecnclResponse_OutputItem(KisBaseModel):
    """nested item."""

    odno: str | None = None  # 주문번호
    pdno: str | None = None  # 상품번호
    rvse_cncl_dvsn_name: str | None = None  # 정정취소구분명
    ord_qty: str | None = None  # 주문수량
    bond_ord_unpr: str | None = None  # 채권주문단가
    ord_tmd: str | None = None  # 주문시각
    tot_ccld_qty: str | None = None  # 총체결수량
    tot_ccld_amt: str | None = None  # 총체결금액
    ord_psbl_qty: str | None = None  # 주문가능수량
    orgn_odno: str | None = None  # 원주문번호
    sll_buy_dvsn_cd: str | None = None  # 매도매수구분코드
    ord_dvsn_cd: str | None = None  # 주문구분코드
    mgco_aptm_odno: str | None = None  # 운용사지정주문번호
    samt_mket_ptci_yn: str | None = None  # 소액시장참여여부
    prdt_abrv_name: str | None = None  # 상품약어명

class InquirePsblRvsecnclResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InquirePsblRvsecnclResponse_OutputItem] = []  # 응답상세 — array

class InquirePsblRvsecnclExecutor(ApiExecutor[InquirePsblRvsecnclRequest, InquirePsblRvsecnclResponse]):
    """채권정정취소가능주문조회  [국내주식-126]."""

    # 채권정정취소가능주문조회 API입니다. 정정취소가능한 채권주문 목록을 확인할 수 있습니다.

    PATH = "/uapi/domestic-bond/v1/trading/inquire-psbl-rvsecncl"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePsblRvsecnclResponse
    TR_ID = "CTSC8035R"
