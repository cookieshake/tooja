"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePsblRvsecnclRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    CTX_AREA_FK100: str  # 연속조회검색조건100 — '공란 : 최초 조회시는 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)'
    CTX_AREA_NK100: str  # 연속조회키100 — '공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)'
    INQR_DVSN_1: str  # 조회구분1 — '0 주문 1 종목'
    INQR_DVSN_2: str  # 조회구분2 — '0 전체 1 매도 2 매수'

class InquirePsblRvsecnclResponse_OutputItem(KisBaseModel):
    """nested item."""

    ord_gno_brno: str | None = None  # 주문채번지점번호 — 주문시 한국투자증권 시스템에서 지정된 영업점코드
    odno: str | None = None  # 주문번호 — 주문시 한국투자증권 시스템에서 채번된 주문번호
    orgn_odno: str | None = None  # 원주문번호 — 정정/취소주문 인경우 원주문번호
    ord_dvsn_name: str | None = None  # 주문구분명
    pdno: str | None = None  # 상품번호 — 종목번호(뒤 6자리만 해당)
    prdt_name: str | None = None  # 상품명 — 종목명
    rvse_cncl_dvsn_name: str | None = None  # 정정취소구분명 — 정정 또는 취소 여부 표시
    ord_qty: str | None = None  # 주문수량
    ord_unpr: str | None = None  # 주문단가 — 1주당 주문가격
    ord_tmd: str | None = None  # 주문시각 — 주문시각(시분초HHMMSS)
    tot_ccld_qty: str | None = None  # 총체결수량 — 주문 수량 중 체결된 수량
    tot_ccld_amt: str | None = None  # 총체결금액 — 주문금액 중 체결금액
    psbl_qty: str | None = None  # 가능수량 — 정정/취소 주문 가능 수량
    sll_buy_dvsn_cd: str | None = None  # 매도매수구분코드 — 01 : 매도 / 02 : 매수
    ord_dvsn_cd: str | None = None  # 주문구분코드 — [KRX] 00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정
    mgco_aptm_odno: str | None = None  # 운용사지정주문번호
    excg_dvsn_cd: str | None = None  # 거래소구분코드
    excg_id_dvsn_cd: str | None = None  # 거래소ID구분코드
    excg_id_dvsn_name: str | None = None  # 거래소ID구분명
    stpm_cndt_pric: str | None = None  # 스톱지정가조건가격
    stpm_efct_occr_yn: str | None = None  # 스톱지정가효력발생여부

class InquirePsblRvsecnclResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InquirePsblRvsecnclResponse_OutputItem] = []  # 응답상세 — array

class InquirePsblRvsecnclExecutor(ApiExecutor[InquirePsblRvsecnclRequest, InquirePsblRvsecnclResponse]):
    """주식정정취소가능주문조회[v1_국내주식-004]."""

    # 주식정정취소가능주문조회 API입니다. 한 번의 호출에 최대 50건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다. ※ 주식주문(정정취소) 호출 전에 반드시 주식정정취소가능주문조회 호출을 통해 정정취소가능수량(output &gt; psbl_qty)을 확인하신 후 정정취소주문 내시기 바랍니다.

    PATH = "/uapi/domestic-stock/v1/trading/inquire-psbl-rvsecncl"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePsblRvsecnclResponse
    TR_ID = "TTTC0084R"
