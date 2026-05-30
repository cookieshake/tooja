"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireDailyCcldRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드
    INQR_STRT_DT: str  # 조회시작일자 — 일자 ~ (1주일 이내)
    INQR_END_DT: str  # 조회종료일자 — ~ 일자 (조회 당일)
    SLL_BUY_DVSN_CD: str  # 매도매수구분코드 — %(전체), 01(매도), 02(매수)
    SORT_SQN_DVSN: str  # 정렬순서구분 — 01(주문순서), 02(주문역순)
    PDNO: str  # 상품번호
    NCCS_YN: str  # 미체결여부 — N(전체), C(체결), Y(미체결)
    CTX_AREA_NK200: str  # 연속조회키200
    CTX_AREA_FK200: str  # 연속조회검색조건200

class InquireDailyCcldResponse_Output1Item(KisBaseModel):
    """nested item."""

    tot_ord_qty: str | None = None  # 총주문수량
    tot_ccld_qty_smtl: str | None = None  # 총체결수량합계
    tot_bond_ccld_avg_unpr: str | None = None  # 총채권체결평균단가
    tot_ccld_amt_smtl: str | None = None  # 총체결금액합계

class InquireDailyCcldResponse_Output2Item(KisBaseModel):
    """nested item."""

    ord_dt: str | None = None  # 주문일자
    odno: str | None = None  # 주문번호
    orgn_odno: str | None = None  # 원주문번호
    ord_dvsn_name: str | None = None  # 주문구분명
    sll_buy_dvsn_cd_name: str | None = None  # 매도매수구분코드명
    shtn_pdno: str | None = None  # 단축상품번호
    prdt_abrv_name: str | None = None  # 상품약어명
    ord_qty: str | None = None  # 주문수량
    bond_ord_unpr: str | None = None  # 채권주문단가
    ord_tmd: str | None = None  # 주문시각
    tot_ccld_qty: str | None = None  # 총체결수량
    bond_avg_unpr: str | None = None  # 채권평균단가
    tot_ccld_amt: str | None = None  # 총체결금액
    loan_dt: str | None = None  # 대출일자
    buy_dt: str | None = None  # 매수일자
    samt_mket_ptci_yn_name: str | None = None  # 소액시장참여여부명
    sprx_psbl_yn_ifom: str | None = None  # 분리과세가능여부알림
    ord_mdia_dvsn_name: str | None = None  # 주문매체구분명
    sll_buy_dvsn_cd: str | None = None  # 매도매수구분코드
    nccs_qty: str | None = None  # 미체결수량
    ord_gno_brno: str | None = None  # 주문채번지점번호

class InquireDailyCcldResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[InquireDailyCcldResponse_Output1Item] = []  # 응답상세
    output2: InquireDailyCcldResponse_Output2Item | None = None  # 응답상세 — array

class InquireDailyCcldExecutor(ApiExecutor[InquireDailyCcldRequest, InquireDailyCcldResponse]):
    """장내채권 주문체결내역 [국내주식-127]."""

    # 장내채권 주문체결내역 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0978] 장내채권주문 '채권주문체결' 탭의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-bond/v1/trading/inquire-daily-ccld"
    METHOD = "GET"
    RESPONSE_TYPE = InquireDailyCcldResponse
    TR_ID = "CTSC8013R"
