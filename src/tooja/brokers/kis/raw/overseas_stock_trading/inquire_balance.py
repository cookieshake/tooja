"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireBalanceRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    OVRS_EXCG_CD: str  # 해외거래소코드 — [모의] NASD : 나스닥 NYSE : 뉴욕 AMEX : 아멕스 [실전] NASD : 미국전체 NAS : 나스닥 NYSE : 뉴욕 AMEX : 아멕스 [모의/실전 공통] SEHK : 홍콩 SHAA : 중국상해 SZAA : 중국심천 
    TR_CRCY_CD: str  # 거래통화코드 — USD : 미국달러 HKD : 홍콩달러 CNY : 중국위안화 JPY : 일본엔화 VND : 베트남동
    CTX_AREA_FK200: str | None = None  # 연속조회검색조건200 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK200값 : 다음페이지 조회시(2번째부터)
    CTX_AREA_NK200: str | None = None  # 연속조회키200 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200값 : 다음페이지 조회시(2번째부터)

class InquireBalanceResponse_Output1Item(KisBaseModel):
    """nested item."""

    cano: str | None = None  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    acnt_prdt_cd: str | None = None  # 계좌상품코드
    prdt_type_cd: str | None = None  # 상품유형코드
    ovrs_pdno: str | None = None  # 해외상품번호
    ovrs_item_name: str | None = None  # 해외종목명
    frcr_evlu_pfls_amt: str | None = None  # 외화평가손익금액 — 해당 종목의 매입금액과 평가금액의 외회기준 비교 손익
    evlu_pfls_rt: str | None = None  # 평가손익율 — 해당 종목의 평가손익을 기준으로 한 수익률
    pchs_avg_pric: str | None = None  # 매입평균가격 — 해당 종목의 매수 평균 단가
    ovrs_cblc_qty: str | None = None  # 해외잔고수량
    ord_psbl_qty: str | None = None  # 주문가능수량 — 매도 가능한 주문 수량
    frcr_pchs_amt1: str | None = None  # 외화매입금액1 — 해당 종목의 외화 기준 매입금액
    ovrs_stck_evlu_amt: str | None = None  # 해외주식평가금액 — 해당 종목의 외화 기준 평가금액
    now_pric2: str | None = None  # 현재가격2 — 해당 종목의 현재가
    tr_crcy_cd: str | None = None  # 거래통화코드 — USD : 미국달러 HKD : 홍콩달러 CNY : 중국위안화 JPY : 일본엔화 VND : 베트남동
    ovrs_excg_cd: str | None = None  # 해외거래소코드 — NASD : 나스닥 NYSE : 뉴욕 AMEX : 아멕스 SEHK : 홍콩 SHAA : 중국상해 SZAA : 중국심천 TKSE : 일본 HASE : 하노이거래소 VNSE : 호치민거래소
    loan_type_cd: str | None = None  # 대출유형코드 — 00 : 해당사항없음 01 : 자기융자일반형 03 : 자기융자투자형 05 : 유통융자일반형 06 : 유통융자투자형 07 : 자기대주 09 : 유통대주 10 : 현금 11 : 주식담보대출 12 : 수익증권담보대출 13 : ELS담보대출 
    loan_dt: str | None = None  # 대출일자 — 대출 실행일자
    expd_dt: str | None = None  # 만기일자 — 대출 만기일자

class InquireBalanceResponse_Output2Item(KisBaseModel):
    """nested item."""

    frcr_pchs_amt1: str | None = None  # 외화매입금액1
    ovrs_rlzt_pfls_amt: str | None = None  # 해외실현손익금액
    ovrs_tot_pfls: str | None = None  # 해외총손익
    rlzt_erng_rt: str | None = None  # 실현수익율
    tot_evlu_pfls_amt: str | None = None  # 총평가손익금액
    tot_pftrt: str | None = None  # 총수익률
    frcr_buy_amt_smtl1: str | None = None  # 외화매수금액합계1
    ovrs_rlzt_pfls_amt2: str | None = None  # 해외실현손익금액2
    frcr_buy_amt_smtl2: str | None = None  # 외화매수금액합계2

class InquireBalanceResponse(KisCommonResponse):
    """응답 본문."""

    ctx_area_fk200: str | None = None  # 연속조회검색조건200
    ctx_area_nk200: str | None = None  # 연속조회키200
    output1: list[str] = []  # 응답상세1
    output2: InquireBalanceResponse_Output2Item | None = None  # 응답상세2

class InquireBalanceExecutor(ApiExecutor[InquireBalanceRequest, InquireBalanceResponse]):
    """해외주식 잔고[v1_해외주식-006]."""

    # 해외주식 잔고를 조회하는 API 입니다. 한국투자 HTS(eFriend Plus) &gt; [7600] 해외주식 종합주문 화면의 좌측 하단 '실시간잔고' 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 다만 미국주간거래 가능종목에 대해서는 frcr_evlu_pfls_amt(외화평가손익금액), evlu_pfls_rt(평가손익율), ovrs_stck_evlu_amt(해외주식평가금액), now_p

    PATH = "/uapi/overseas-stock/v1/trading/inquire-balance"
    METHOD = "GET"
    RESPONSE_TYPE = InquireBalanceResponse
    TR_ID = "TTTS3012R"
    TR_ID_VIRTUAL = "VTTS3012R"
