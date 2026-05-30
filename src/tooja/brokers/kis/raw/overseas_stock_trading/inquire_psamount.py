"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePsamountRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    OVRS_EXCG_CD: str  # 해외거래소코드 — NASD : 나스닥 / NYSE : 뉴욕 / AMEX : 아멕스 SEHK : 홍콩 / SHAA : 중국상해 / SZAA : 중국심천 TKSE : 일본 / HASE : 하노이거래소 / VNSE : 호치민거래소
    OVRS_ORD_UNPR: str  # 해외주문단가 — 해외주문단가 (23.8) 정수부분 23자리, 소수부분 8자리
    ITEM_CD: str  # 종목코드

class InquirePsamountResponse_OutputItem(KisBaseModel):
    """nested item."""

    tr_crcy_cd: str | None = None  # 거래통화코드 — 18.2
    ord_psbl_frcr_amt: str | None = None  # 주문가능외화금액 — 18.2
    sll_ruse_psbl_amt: str | None = None  # 매도재사용가능금액 — 가능금액 산정 시 사용
    ovrs_ord_psbl_amt: str | None = None  # 해외주문가능금액 — - 한국투자 앱 해외주식 주문화면내 "외화" 인경우 주문가능금액
    max_ord_psbl_qty: str | None = None  # 최대주문가능수량 — - 한국투자 앱 해외주식 주문화면내 "외화" 인경우 주문가능수량 - 매수 시 수량단위 절사해서 사용 예 : (100주단위) 545 주 -> 500 주 / (10주단위) 545 주 -> 540 주
    echm_af_ord_psbl_amt: str | None = None  # 환전이후주문가능금액 — 사용되지 않는 사항(0으로 출력)
    echm_af_ord_psbl_qty: str | None = None  # 환전이후주문가능수량 — 사용되지 않는 사항(0으로 출력)
    ord_psbl_qty: str | None = None  # 주문가능수량 — 22(20.1)
    exrt: str | None = None  # 환율 — 25(18.6)
    frcr_ord_psbl_amt1: str | None = None  # 외화주문가능금액1 — - 한국투자 앱 해외주식 주문화면내 "통합" 인경우 주문가능금액
    ovrs_max_ord_psbl_qty: str | None = None  # 해외최대주문가능수량 — - 한국투자 앱 해외주식 주문화면내 "통합" 인경우 주문가능수량 - 매수 시 수량단위 절사해서 사용 예 : (100주단위) 545 주 -> 500 주 / (10주단위) 545 주 -> 540 주

class InquirePsamountResponse(KisCommonResponse):
    """응답 본문."""

    output: InquirePsamountResponse_OutputItem | None = None  # 응답상세1

class InquirePsamountExecutor(ApiExecutor[InquirePsamountRequest, InquirePsamountResponse]):
    """해외주식 매수가능금액조회[v1_해외주식-014]."""

    # 해외주식 매수가능금액조회 API입니다. * 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고) https://securities.koreainvestment.com/main/bond/research/_static/TF03ca010001.jsp

    PATH = "/uapi/overseas-stock/v1/trading/inquire-psamount"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePsamountResponse
    TR_ID = "TTTS3007R"
    TR_ID_VIRTUAL = "VTTS3007R"
