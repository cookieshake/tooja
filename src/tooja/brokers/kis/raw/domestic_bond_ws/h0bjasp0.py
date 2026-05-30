"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0bjasp0Message(KisBaseModel):
    """WS 메시지 1건."""

    STND_ISCD: str  # 표준종목코드
    STCK_CNTG_HOUR: str  # 주식체결시간
    ASKP_ERT1: str  # 매도호가수익률
    BIDP_ERT1: str  # 매수호가수익률1
    ASKP1: str  # 매도호가1
    BIDP1: str  # 매수호가1
    ASKP_RSQN1: str  # 매도호가잔량1
    BIDP_RSQN1: str  # 매수호가잔량1
    ASKP_ERT2: str  # 매도호가수익률2
    BIDP_ERT2: str  # 매수호가수익률2
    ASKP2: str  # 매도호가2
    BIDP2: str  # 매수호가2
    ASKP_RSQN2: str  # 매도호가잔량2
    BIDP_RSQN2: str  # 매수호가잔량2
    ASKP_ERT3: str  # 매도호가수익률3
    BIDP_ERT3: str  # 매수호가수익률3
    ASKP3: str  # 매도호가3
    BIDP3: str  # 매수호가3
    ASKP_RSQN3: str  # 매도호가잔량3
    BIDP_RSQN3: str  # 매수호가잔량3
    ASKP_ERT4: str  # 매도호가수익률4
    BIDP_ERT4: str  # 매수호가수익률4
    ASKP4: str  # 매도호가4
    BIDP4: str  # 매수호가4
    ASKP_RSQN4: str  # 매도호가잔량4
    BIDP_RSQN4: str  # 매수호가잔량4
    ASKP_ERT5: str  # 매도호가수익률5
    BIDP_ERT5: str  # 매수호가수익률5
    ASKP5: str  # 매도호가5
    BIDP5: str  # 매수호가5
    ASKP_RSQN52: str  # 매도호가잔량5
    BIDP_RSQN53: str  # 매수호가잔량5
    TOTAL_ASKP_RSQN: str  # 총매도호가잔량
    TOTAL_BIDP_RSQN: str  # 총매수호가잔량

class H0bjasp0Subscriber(WsSubscriber[H0bjasp0Message]):
    """일반채권 실시간호가 [실시간-053]."""

    TR_ID = "H0BJCNT0"
    RESPONSE_TYPE = H0bjasp0Message
    COLUMNS = ("STND_ISCD", "STCK_CNTG_HOUR", "ASKP_ERT1", "BIDP_ERT1", "ASKP1", "BIDP1", "ASKP_RSQN1", "BIDP_RSQN1", "ASKP_ERT2", "BIDP_ERT2", "ASKP2", "BIDP2", "ASKP_RSQN2", "BIDP_RSQN2", "ASKP_ERT3", "BIDP_ERT3", "ASKP3", "BIDP3", "ASKP_RSQN3", "BIDP_RSQN3", "ASKP_ERT4", "BIDP_ERT4", "ASKP4", "BIDP4", "ASKP_RSQN4", "BIDP_RSQN4", "ASKP_ERT5", "BIDP_ERT5", "ASKP5", "BIDP5", "ASKP_RSQN52", "BIDP_RSQN53", "TOTAL_ASKP_RSQN", "TOTAL_BIDP_RSQN",)
