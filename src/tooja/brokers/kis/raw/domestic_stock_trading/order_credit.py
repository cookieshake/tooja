"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OrderCreditRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    PDNO: str  # 상품번호 — 종목코드(6자리)
    SLL_TYPE: str | None = None  # 매도유형 — 공란 입력
    CRDT_TYPE: str  # 신용유형 — [매도] 22 : 유통대주신규, 24 : 자기대주신규, 25 : 자기융자상환, 27 : 유통융자상환 [매수] 21 : 자기융자신규, 23 : 유통융자신규 , 26 : 유통대주상환, 28 : 자기대주상환
    LOAN_DT: str  # 대출일자 — [신용매수] 신규 대출로, 오늘날짜(yyyyMMdd)) 입력 [신용매도] 매도할 종목의 대출일자(yyyyMMdd)) 입력
    ORD_DVSN: str  # 주문구분 — [KRX] 00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정가 
    ORD_QTY: str  # 주문수량
    ORD_UNPR: str  # 주문단가 — 1주당 가격 * 장전 시간외, 장후 시간외, 시장가의 경우 1주당 가격을 공란으로 비우지 않음 "0"으로 입력 권고
    RSVN_ORD_YN: str | None = None  # 예약주문여부 — 정규 증권시장이 열리지 않는 시간 (15:10분 ~ 익일 7:30분) 에 주문을 미리 설정 하여 다음 영업일 또는 설정한 기간 동안 아침 동시 호가에 주문하는 것 Y : 예약주문 N : 신용주문
    EMGC_ORD_YN: str | None = None  # 비상주문여부
    PGTR_DVSN: str | None = None  # 프로그램매매구분
    MGCO_APTM_ODNO: str | None = None  # 운용사지정주문번호
    LQTY_TR_NGTN_DTL_NO: str | None = None  # 대량거래협상상세번호
    LQTY_TR_AGMT_NO: str | None = None  # 대량거래협정번호
    LQTY_TR_NGTN_ID: str | None = None  # 대량거래협상자Id
    LP_ORD_YN: str | None = None  # LP주문여부
    MDIA_ODNO: str | None = None  # 매체주문번호
    ORD_SVR_DVSN_CD: str | None = None  # 주문서버구분코드
    PGM_NMPR_STMT_DVSN_CD: str | None = None  # 프로그램호가신고구분코드
    CVRG_SLCT_RSON_CD: str | None = None  # 반대매매선정사유코드
    CVRG_SEQ: str | None = None  # 반대매매순번
    EXCG_ID_DVSN_CD: str | None = None  # 거래소ID구분코드 — 한국거래소 : KRX 대체거래소 (넥스트레이드) : NXT SOR (Smart Order Routing) : SOR → 미입력시 KRX로 진행되며, 모의투자는 KRX만 가능
    CNDT_PRIC: str | None = None  # 조건가격 — 스탑지정가호가에서 사용

class OrderCreditResponse_OutputItem(KisBaseModel):
    """nested item."""

    krx_fwdg_ord_orgno: str | None = None  # 한국거래소전송주문조직번호
    odno: str | None = None  # 주문번호
    ord_tmd: str | None = None  # 주문시간

class OrderCreditResponse(KisCommonResponse):
    """응답 본문."""

    output: OrderCreditResponse_OutputItem | None = None  # 응답상세 — single

class OrderCreditExecutor(ApiExecutor[OrderCreditRequest, OrderCreditResponse]):
    """주식주문(신용)[v1_국내주식-002]."""

    # 국내주식주문(신용) API입니다. ※ 모의투자는 사용 불가합니다. ※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다. (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...)

    PATH = "/uapi/domestic-stock/v1/trading/order-credit"
    METHOD = "POST"
    RESPONSE_TYPE = OrderCreditResponse
    TR_ID = "TTTC0051U"
