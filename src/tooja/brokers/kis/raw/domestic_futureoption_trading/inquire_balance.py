"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireBalanceRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    MGNA_DVSN: str  # 증거금 구분 — 01 : 개시 02 : 유지
    EXCC_STAT_CD: str  # 정산상태코드 — 1 : 정산 (정산가격으로 잔고 조회) 2 : 본정산 (매입가격으로 잔고 조회)
    CTX_AREA_FK200: str  # 연속조회검색조건200 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK200값 : 다음페이지 조회시(2번째부터)
    CTX_AREA_NK200: str  # 연속조회키200 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200값 : 다음페이지 조회시(2번째부터)

class InquireBalanceResponse_Output1Item(KisBaseModel):
    """nested item."""

    cano: str | None = None  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    acnt_prdt_cd: str | None = None  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    pdno: str | None = None  # 상품번호 — 선물옵션종목코드
    prdt_type_cd: str | None = None  # 상품유형코드
    shtn_pdno: str | None = None  # 단축상품번호 — 단축상품번호 (예: 101P09)
    prdt_name: str | None = None  # 상품명
    sll_buy_dvsn_name: str | None = None  # 매도매수구분명 — 매도/매수 구분의 명칭 - 매수잔고를 가진 경우, "매수" 혹은 "BUY"로 출력 - 매도잔고를 가진 경우, "매도" 혹은 "SLL"로 출력 - 당일 잔고를 청산하여 잔고를 가지고 있지 않은 경우 빈칸으로 출력
    cblc_qty: str | None = None  # 잔고수량 — 보유한 종목의 수량
    excc_unpr: str | None = None  # 정산단가 — 당일 종가로 정산한 가격
    ccld_avg_unpr1: str | None = None  # 체결평균단가1 — 보유한 종목의 평균 체결 가격
    idx_clpr: str | None = None  # 지수종가
    pchs_amt: str | None = None  # 매입금액 — 보유 종목을 매수한 금액
    evlu_amt: str | None = None  # 평가금액 — 보유 종목을 현재가로 평가하여 산출한 금액
    evlu_pfls_amt: str | None = None  # 평가손익금액 — 매입금액과 평가금액을 비교한 손익
    trad_pfls_amt: str | None = None  # 매매손익금액 — 매수와 매도가 완료된 수량에 대한 실현 손익
    lqd_psbl_qty: str | None = None  # 청산가능수량 — 청산 가능한 수량

class InquireBalanceResponse_Output2Item(KisBaseModel):
    """nested item."""

    dnca_cash: str | None = None  # 예수금현금 — 원화로 보유한 현금 (현금미수금액, 수수료미수금액 차감)
    frcr_dncl_amt: str | None = None  # 외화예수금액 — 외화로 보유한 현금
    dnca_sbst: str | None = None  # 예수금대용 — 주식대용금액+채권대용금액+전일대용매도대용금액+당일대용매도대용금액
    tot_dncl_amt: str | None = None  # 총예수금액 — 상기 3개 예수금 항목의 합계 금액
    tot_ccld_amt: str | None = None  # 총체결금액 — 체결된 주문의 합계금액
    cash_mgna: str | None = None  # 현금증거금 — 원화 현금 중 주문증거금으로 사용된 금액
    sbst_mgna: str | None = None  # 대용증거금 — 대용 예수금 중 주문증거금으로 사용된 금액
    mgna_tota: str | None = None  # 증거금총액 — 증거금으로 사용된 항목의 합계 금액
    opt_dfpa: str | None = None  # 옵션차금 — 당일옵션매도금에서 당일옵션매수금을 차감한 금액
    thdt_dfpa: str | None = None  # 당일차금 — 당일의 각 매수거래에 대하여 1에 의하여 산출한 금액의 합계액과 당일의 각 매도거래에 대하여 2에 의하여 산출한 금액의 합계액을 합산한 금액 1. 매수거래수량*(당일의 정산가격-체결가격)*최소가격변동금액*환산승수 2. 매도거래수량*(체결가
    rnwl_dfpa: str | None = None  # 갱신차금 — 직전 거래일의 매수미결제약정에 대하여 1에 의하여 산출한 금액과 직전거래일의 매도미결제약정에 대하여 2에 의하여 산출한 금액을 합산한 금액 1. 매수미결제약정*(당일의 정산가격-직전거래일의 정산가격)*최소가격변동 금액*환산승수 2. 매도미
    fee: str | None = None  # 수수료 — 체결된 주문에 의한 매매수수료
    nxdy_dnca: str | None = None  # 익일예수금 — 당일 매매내역을 근거로 익일(결제일) 고객님 계좌에 있는 현금
    nxdy_dncl_amt: str | None = None  # 익일예수금액
    prsm_dpast: str | None = None  # 추정예탁자산 — 보유한 잔고를 정산 기준으로 평가한 금액과 예수금을 합한 금액
    prsm_dpast_amt: str | None = None  # 추정예탁자산금액
    pprt_ord_psbl_cash: str | None = None  # 적정주문가능현금 — 미수없는 주문가능금액
    add_mgna_cash: str | None = None  # 추가증거금현금 — 장 종료 후 예탁평가액이 유지증거금을 하회할 경우 또는 예탁현금이 결제금액 보다 적은 경우 고객이 추가적으로 납부해야 하는 증거금
    add_mgna_tota: str | None = None  # 추가증거금총액
    futr_trad_pfls_amt: str | None = None  # 선물매매손익금액 — 선물 매수와 매도가 완료된 수량에 대한 실현 손익
    opt_trad_pfls_amt: str | None = None  # 옵션매매손익금액 — 옵션 매수와 매도가 완료된 수량에 대한 실현 손익
    futr_evlu_pfls_amt: str | None = None  # 선물평가손익금액 — 선물 잔고의 매입가격 또는 정산가격과 평가금액을 비교한 손익
    opt_evlu_pfls_amt: str | None = None  # 옵션평가손익금액 — 옵션 잔고의 매입가격 또는 정산가격과 평가금액을 비교한 손익
    trad_pfls_amt_smtl: str | None = None  # 매매손익금액합계 — 선물매매손익금액과 옵션매매손익금액을 합한 금액
    evlu_pfls_amt_smtl: str | None = None  # 평가손익금액합계 — 선물평가손익금액과 옵션평가손익금액을 합한 금액
    wdrw_psbl_tot_amt: str | None = None  # 인출가능총금액 — 출금 가능한 현금(예탁현금+예탁대용-예탁증거금총액)
    ord_psbl_cash: str | None = None  # 주문가능현금 — 예수금현금에서 현금증거금을 차감한 금액
    ord_psbl_sbst: str | None = None  # 주문가능대용 — 예수금대용에서 대용증거금을 차감한 금액
    ord_psbl_tota: str | None = None  # 주문가능총액 — 주문가능현금과 주문가능대용을 합한 금액
    pchs_amt_smtl: str | None = None  # 매입금액합계 — 종목별 매입금액의 합계 금액
    evlu_amt_smtl: str | None = None  # 평가금액합계 — 종목별 평가금액의 합계 금액

class InquireBalanceResponse(KisCommonResponse):
    """응답 본문."""

    ctx_area_fk200: str | None = None  # 연속조회검색조건200
    ctx_area_nk200: str | None = None  # 연속조회키200
    output1: list[str] = []  # 응답상세1
    output2: InquireBalanceResponse_Output2Item | None = None  # 응답상세2

class InquireBalanceExecutor(ApiExecutor[InquireBalanceRequest, InquireBalanceResponse]):
    """선물옵션 잔고현황[v1_국내선물-004]."""

    # 선물옵션 잔고현황 API입니다. 한 번의 호출에 최대 20건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다.

    PATH = "/uapi/domestic-futureoption/v1/trading/inquire-balance"
    METHOD = "GET"
    RESPONSE_TYPE = InquireBalanceResponse
    TR_ID = "CTFO6118R"
    TR_ID_VIRTUAL = "VTFO6118R"
