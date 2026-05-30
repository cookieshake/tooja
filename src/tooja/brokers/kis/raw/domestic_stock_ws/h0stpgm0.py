"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0stpgm0Message(KisBaseModel):
    """WS 메시지 1건."""

    STCK_CNTG_HOUR: str  # 주식체결시간
    SELN_CNQN: str  # 매도체결량
    SELN_TR_PBMN: str  # 매도거래대금
    SHNU_CNQN: str  # 매수2체결량
    SHNU_TR_PBMN: str  # 매수2거래대금
    NTBY_CNQN: str  # 순매수체결량
    NTBY_TR_PBMN: str  # 순매수거래대금
    SELN_RSQN: str  # 매도호가잔량
    SHNU_RSQN: str  # 매수호가잔량
    WHOL_NTBY_QTY: str  # 전체순매수호가잔량

class H0stpgm0Subscriber(WsSubscriber[H0stpgm0Message]):
    """국내주식 실시간프로그램매매 (KRX) [실시간-048]."""

    TR_ID = "H0STPGM0"
    RESPONSE_TYPE = H0stpgm0Message
    COLUMNS = ("STCK_CNTG_HOUR", "SELN_CNQN", "SELN_TR_PBMN", "SHNU_CNQN", "SHNU_TR_PBMN", "NTBY_CNQN", "NTBY_TR_PBMN", "SELN_RSQN", "SHNU_RSQN", "WHOL_NTBY_QTY",)
