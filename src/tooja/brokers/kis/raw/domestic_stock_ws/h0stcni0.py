"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0stcni0Message(KisBaseModel):
    """WS 메시지 1건."""

    CUST_ID: str  # 고객 ID
    ACNT_NO: str  # 계좌번호
    ODER_NO: str  # 주문번호
    OODER_NO: str  # 원주문번호
    SELN_BYOV_CLS: str  # 매도매수구분 — 01 : 매도 02 : 매수
    RCTF_CLS: str  # 정정구분 — 0:정상 1:정정 2:취소
    ODER_KIND: str  # 주문종류 — [KRX] 00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정가 
    ODER_COND: str  # 주문조건 — 0:없음 1:IOC 2:FOK
    STCK_SHRN_ISCD: str  # 주식 단축 종목코드
    CNTG_QTY: str  # 체결 수량
    CNTG_UNPR: str  # 체결단가
    STCK_CNTG_HOUR: str  # 주식 체결 시간
    RFUS_YN: str  # 거부여부 — 0 : 승인 1 : 거부
    CNTG_YN: str  # 체결여부 — 1 : 주문,정정,취소,거부 2 : 체결
    ACPT_YN: str  # 접수여부 — 1 : 주문접수 2 : 확인 3 : 취소(FOK/IOC)
    BRNC_NO: str  # 지점번호
    ODER_QTY: str  # 주문수량
    ACNT_NAME: str  # 계좌명
    ORD_COND_PRC: str  # 호가조건가격 — 스톱지정가 시 표시
    ORD_EXG_GB: str  # 주문거래소 구분 — 1:KRX, 2:NXT, 3:SOR-KRX, 4:SOR-NXT
    POPUP_YN: str  # 실시간체결창 표시여부 — Y/N
    FILLER: str  # 필러
    CRDT_CLS: str  # 신용구분
    CRDT_LOAN_DATE: str  # 신용대출일자
    CNTG_ISNM40: str  # 체결종목명
    ODER_PRC: str  # 주문가격

class H0stcni0Subscriber(WsSubscriber[H0stcni0Message]):
    """국내주식 실시간체결통보 [실시간-005]."""

    TR_ID = "H0STCNI0"
    RESPONSE_TYPE = H0stcni0Message
    COLUMNS = ("CUST_ID", "ACNT_NO", "ODER_NO", "OODER_NO", "SELN_BYOV_CLS", "RCTF_CLS", "ODER_KIND", "ODER_COND", "STCK_SHRN_ISCD", "CNTG_QTY", "CNTG_UNPR", "STCK_CNTG_HOUR", "RFUS_YN", "CNTG_YN", "ACPT_YN", "BRNC_NO", "ODER_QTY", "ACNT_NAME", "ORD_COND_PRC", "ORD_EXG_GB", "POPUP_YN", "FILLER", "CRDT_CLS", "CRDT_LOAN_DATE", "CNTG_ISNM40", "ODER_PRC",)
