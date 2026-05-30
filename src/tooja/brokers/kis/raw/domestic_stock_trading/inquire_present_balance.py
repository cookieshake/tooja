"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePresentBalanceRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드 — 29
    USER_DVSN_CD: str  # 사용자구분코드 — 00
    CTX_AREA_FK100: str  # 연속조회검색조건100
    CTX_AREA_NK100: str  # 연속조회키100
    PRCS_DVSN_CD: str | None = None  # 처리구분코드 — 00 : 보유 주식 전체 조회 01 : 보유 주식 중 0주 주식 숨김

class InquirePresentBalanceResponse_Output1Item(KisBaseModel):
    """nested item."""

    cblc_dvsn: str | None = None  # 잔고구분
    cblc_dvsn_name: str | None = None  # 잔고구분명
    pdno: str | None = None  # 상품번호
    prdt_name: str | None = None  # 상품명
    hldg_qty: str | None = None  # 보유수량
    slpsb_qty: str | None = None  # 매도가능수량
    pchs_avg_pric: str | None = None  # 매입평균가격
    evlu_pfls_amt: str | None = None  # 평가손익금액
    evlu_pfls_rt: str | None = None  # 평가손익율
    prpr: str | None = None  # 현재가
    evlu_amt: str | None = None  # 평가금액
    pchs_amt: str | None = None  # 매입금액
    cblc_weit: str | None = None  # 잔고비중

class InquirePresentBalanceResponse_Output2Item(KisBaseModel):
    """nested item."""

    pchs_amt_smtl_amt: str | None = None  # 매입금액합계금액
    evlu_amt_smtl_amt: str | None = None  # 평가금액합계금액
    evlu_pfls_smtl_amt: str | None = None  # 평가손익합계금액
    trad_pfls_smtl: str | None = None  # 매매손익합계
    thdt_tot_pfls_amt: str | None = None  # 당일총손익금액
    pftrt: str | None = None  # 수익률

class InquirePresentBalanceResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[InquirePresentBalanceResponse_Output1Item] = []  # 응답상세1 — Array
    output2: list[InquirePresentBalanceResponse_Output2Item] = []  # 응답상세2 — Array

class InquirePresentBalanceExecutor(ApiExecutor[InquirePresentBalanceRequest, InquirePresentBalanceResponse]):
    """퇴직연금 체결기준잔고[v1_국내주식-032]."""

    # ​※ 55번 계좌(DC가입자계좌)의 경우 해당 API 이용이 불가합니다. KIS Developers API의 경우 HTS ID에 반드시 연결되어있어야만 API 신청 및 앱정보 발급이 가능한 서비스로 개발되어서 실물계좌가 아닌 55번 계좌는 API 이용이 불가능한 점 양해 부탁드립니다.

    PATH = "/uapi/domestic-stock/v1/trading/pension/inquire-present-balance"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePresentBalanceResponse
    TR_ID = "TTTC2202R"
