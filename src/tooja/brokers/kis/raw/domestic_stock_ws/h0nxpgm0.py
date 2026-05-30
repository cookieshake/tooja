"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0nxpgm0Message(KisBaseModel):
    """WS 메시지 1건."""

    MKSC_SHRN_ISCD: str  # 유가증권 단축 종목코드
    STCK_CNTG_HOUR: str  # 주식 체결 시간
    SELN_CNQN: str  # 매도 체결량
    SELN_TR_PBMN: str  # 매도 거래 대금
    SHNU_CNQN: str  # 매수2 체결량
    SHNU_TR_PBMN: str  # 매수2 거래 대금
    NTBY_CNQN: str  # 순매수 체결량
    NTBY_TR_PBMN: str  # 순매수 거래 대금
    SELN_RSQN: str  # 매도호가잔량
    SHNU_RSQN: str  # 매수호가잔량
    WHOL_NTBY_QTY: str  # 전체순매수호가잔량

class H0nxpgm0Subscriber(WsSubscriber[H0nxpgm0Message]):
    """국내주식 실시간프로그램매매 (NXT)."""

    TR_ID = "H0NXPGM0"
    RESPONSE_TYPE = H0nxpgm0Message
    COLUMNS = ("MKSC_SHRN_ISCD", "STCK_CNTG_HOUR", "SELN_CNQN", "SELN_TR_PBMN", "SHNU_CNQN", "SHNU_TR_PBMN", "NTBY_CNQN", "NTBY_TR_PBMN", "SELN_RSQN", "SHNU_RSQN", "WHOL_NTBY_QTY",)
