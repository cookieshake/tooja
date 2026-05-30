"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0eucni0Message(KisBaseModel):
    """WS 메시지 1건."""

    CUST_ID: str  # 고객 ID
    ACNT_NO: str  # 계좌번호
    ODER_NO: str  # 주문번호
    OODER_NO: str  # 원주문번호
    SELN_BYOV_CLS: str  # 매도매수구분
    RCTF_CLS: str  # 정정구분
    ODER_KIND2: str  # 주문종류2
    STCK_SHRN_ISCD: str  # 주식 단축 종목코드
    CNTG_QTY: str  # 체결 수량
    CNTG_UNPR: str  # 체결단가
    STCK_CNTG_HOUR: str  # 주식 체결 시간
    RFUS_YN: str  # 거부여부
    CNTG_YN: str  # 체결여부
    ACPT_YN: str  # 접수여부
    BRNC_NO: str  # 지점번호
    ODER_QTY: str  # 주문수량
    ACNT_NAME: str  # 계좌명
    CNTG_ISNM: str  # 체결종목명
    ODER_COND: str  # 주문조건

class H0eucni0Subscriber(WsSubscriber[H0eucni0Message]):
    """KRX야간옵션실시간체결통보 [실시간-067]."""

    TR_ID = "H0MFCNI0"
    RESPONSE_TYPE = H0eucni0Message
    COLUMNS = ("CUST_ID", "ACNT_NO", "ODER_NO", "OODER_NO", "SELN_BYOV_CLS", "RCTF_CLS", "ODER_KIND2", "STCK_SHRN_ISCD", "CNTG_QTY", "CNTG_UNPR", "STCK_CNTG_HOUR", "RFUS_YN", "CNTG_YN", "ACPT_YN", "BRNC_NO", "ODER_QTY", "ACNT_NAME", "CNTG_ISNM", "ODER_COND",)
