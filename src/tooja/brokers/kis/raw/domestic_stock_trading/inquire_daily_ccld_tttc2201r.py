"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireDailyCcldTttc2201rRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드 — 29
    USER_DVSN_CD: str  # 사용자구분코드 — %%
    SLL_BUY_DVSN_CD: str  # 매도매수구분코드 — 00 : 전체 / 01 : 매도 / 02 : 매수
    CCLD_NCCS_DVSN: str  # 체결미체결구분 — %% : 전체 / 01 : 체결 / 02 : 미체결
    INQR_DVSN_3: str  # 조회구분3 — 00 : 전체
    CTX_AREA_FK100: str  # 연속조회검색조건100
    CTX_AREA_NK100: str  # 연속조회키100

class InquireDailyCcldTttc2201rResponse_OutputItem(KisBaseModel):
    """nested item."""

    ord_gno_brno: str | None = None  # 주문채번지점번호
    sll_buy_dvsn_cd: str | None = None  # 매도매수구분코드
    trad_dvsn_name: str | None = None  # 매매구분명
    odno: str | None = None  # 주문번호
    pdno: str | None = None  # 상품번호
    prdt_name: str | None = None  # 상품명
    ord_unpr: str | None = None  # 주문단가
    ord_qty: str | None = None  # 주문수량
    tot_ccld_qty: str | None = None  # 총체결수량
    nccs_qty: str | None = None  # 미체결수량
    ord_dvsn_cd: str | None = None  # 주문구분코드
    ord_dvsn_name: str | None = None  # 주문구분명
    orgn_odno: str | None = None  # 원주문번호
    ord_tmd: str | None = None  # 주문시각
    objt_cust_dvsn_name: str | None = None  # 대상고객구분명
    pchs_avg_pric: str | None = None  # 매입평균가격
    stpm_cndt_pric: str | None = None  # 스톱지정가조건가격 — 신규 API용 필드
    stpm_efct_occr_dtmd: str | None = None  # 스톱지정가효력발생상세시각 — 신규 API용 필드
    stpm_efct_occr_yn: str | None = None  # 스톱지정가효력발생여부 — 신규 API용 필드
    excg_id_dvsn_cd: str | None = None  # 거래소ID구분코드 — 신규 API용 필드

class InquireDailyCcldTttc2201rResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InquireDailyCcldTttc2201rResponse_OutputItem] = []  # 응답상세1 — Array

class InquireDailyCcldTttc2201rExecutor(ApiExecutor[InquireDailyCcldTttc2201rRequest, InquireDailyCcldTttc2201rResponse]):
    """퇴직연금 미체결내역[v1_국내주식-033]."""

    # ​※ 55번 계좌(DC가입자계좌)의 경우 해당 API 이용이 불가합니다. KIS Developers API의 경우 HTS ID에 반드시 연결되어있어야만 API 신청 및 앱정보 발급이 가능한 서비스로 개발되어서 실물계좌가 아닌 55번 계좌는 API 이용이 불가능한 점 양해 부탁드립니다.

    PATH = "/uapi/domestic-stock/v1/trading/pension/inquire-daily-ccld"
    METHOD = "GET"
    RESPONSE_TYPE = InquireDailyCcldTttc2201rResponse
    TR_ID = "TTTC2201R"
