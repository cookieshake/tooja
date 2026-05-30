"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireBalanceTttc2208rRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드 — 29
    ACCA_DVSN_CD: str  # 적립금구분코드 — 00
    INQR_DVSN: str  # 조회구분 — 00 : 전체
    CTX_AREA_FK100: str  # 연속조회검색조건100
    CTX_AREA_NK100: str  # 연속조회키100

class InquireBalanceTttc2208rResponse_Output1Item(KisBaseModel):
    """nested item."""

    cblc_dvsn_name: str | None = None  # 잔고구분명
    prdt_name: str | None = None  # 상품명
    pdno: str | None = None  # 상품번호
    item_dvsn_name: str | None = None  # 종목구분명
    thdt_buyqty: str | None = None  # 금일매수수량
    thdt_sll_qty: str | None = None  # 금일매도수량
    hldg_qty: str | None = None  # 보유수량
    ord_psbl_qty: str | None = None  # 주문가능수량
    pchs_avg_pric: str | None = None  # 매입평균가격
    pchs_amt: str | None = None  # 매입금액
    prpr: str | None = None  # 현재가
    evlu_amt: str | None = None  # 평가금액
    evlu_pfls_amt: str | None = None  # 평가손익금액
    evlu_erng_rt: str | None = None  # 평가수익율

class InquireBalanceTttc2208rResponse_Output2Item(KisBaseModel):
    """nested item."""

    dnca_tot_amt: str | None = None  # 예수금총금액
    nxdy_excc_amt: str | None = None  # 익일정산금액
    prvs_rcdl_excc_amt: str | None = None  # 가수도정산금액
    thdt_buy_amt: str | None = None  # 금일매수금액
    thdt_sll_amt: str | None = None  # 금일매도금액
    thdt_tlex_amt: str | None = None  # 금일제비용금액
    scts_evlu_amt: str | None = None  # 유가평가금액
    tot_evlu_amt: str | None = None  # 총평가금액

class InquireBalanceTttc2208rResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[InquireBalanceTttc2208rResponse_Output1Item] = []  # 응답상세 — Array
    output2: InquireBalanceTttc2208rResponse_Output2Item | None = None  # 응답상세2

class InquireBalanceTttc2208rExecutor(ApiExecutor[InquireBalanceTttc2208rRequest, InquireBalanceTttc2208rResponse]):
    """퇴직연금 잔고조회[v1_국내주식-036]."""

    # 주식, ETF, ETN만 조회 가능하며 펀드는 조회 불가합니다. ​※ 55번 계좌(DC가입자계좌)의 경우 해당 API 이용이 불가합니다. KIS Developers API의 경우 HTS ID에 반드시 연결되어있어야만 API 신청 및 앱정보 발급이 가능한 서비스로 개발되어서 실물계좌가 아닌 55번 계좌는 API 이용이 불가능한 점 양해 부탁드립니다.

    PATH = "/uapi/domestic-stock/v1/trading/pension/inquire-balance"
    METHOD = "GET"
    RESPONSE_TYPE = InquireBalanceTttc2208rResponse
    TR_ID = "TTTC2208R"
