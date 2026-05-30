"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0euasp0Message(KisBaseModel):
    """WS 메시지 1건."""

    OPTN_SHRN_ISCD: str  # 옵션단축종목코드
    BSOP_HOUR: str  # 영업시간
    OPTN_ASKP1: str  # 옵션매도호가1
    OPTN_ASKP2: str  # 옵션매도호가2
    OPTN_ASKP3: str  # 옵션매도호가3
    OPTN_ASKP4: str  # 옵션매도호가4
    OPTN_ASKP5: str  # 옵션매도호가5
    OPTN_BIDP1: str  # 옵션매수호가1
    OPTN_BIDP2: str  # 옵션매수호가2
    OPTN_BIDP3: str  # 옵션매수호가3
    OPTN_BIDP4: str  # 옵션매수호가4
    OPTN_BIDP5: str  # 옵션매수호가5
    ASKP_CSNU1: str  # 매도호가건수1
    ASKP_CSNU2: str  # 매도호가건수2
    ASKP_CSNU3: str  # 매도호가건수3
    ASKP_CSNU4: str  # 매도호가건수4
    ASKP_CSNU5: str  # 매도호가건수5
    BIDP_CSNU1: str  # 매수호가건수1
    BIDP_CSNU2: str  # 매수호가건수2
    BIDP_CSNU3: str  # 매수호가건수3
    BIDP_CSNU4: str  # 매수호가건수4
    BIDP_CSNU5: str  # 매수호가건수5
    ASKP_RSQN1: str  # 매도호가잔량1
    ASKP_RSQN2: str  # 매도호가잔량2
    ASKP_RSQN3: str  # 매도호가잔량3
    ASKP_RSQN4: str  # 매도호가잔량4
    ASKP_RSQN5: str  # 매도호가잔량5
    BIDP_RSQN1: str  # 매수호가잔량1
    BIDP_RSQN2: str  # 매수호가잔량2
    BIDP_RSQN3: str  # 매수호가잔량3
    BIDP_RSQN4: str  # 매수호가잔량4
    BIDP_RSQN5: str  # 매수호가잔량5
    TOTAL_ASKP_CSNU: str  # 총매도호가건수
    TOTAL_BIDP_CSNU: str  # 총매수호가건수
    TOTAL_ASKP_RSQN: str  # 총매도호가잔량
    TOTAL_BIDP_RSQN: str  # 총매수호가잔량
    TOTAL_ASKP_RSQN_ICDC: str  # 총매도호가잔량증감
    TOTAL_BIDP_RSQN_ICDC: str  # 총매수호가잔량증감

class H0euasp0Subscriber(WsSubscriber[H0euasp0Message]):
    """KRX야간옵션 실시간호가 [실시간-033]."""

    TR_ID = "H0EUASP0"
    RESPONSE_TYPE = H0euasp0Message
    COLUMNS = ("OPTN_SHRN_ISCD", "BSOP_HOUR", "OPTN_ASKP1", "OPTN_ASKP2", "OPTN_ASKP3", "OPTN_ASKP4", "OPTN_ASKP5", "OPTN_BIDP1", "OPTN_BIDP2", "OPTN_BIDP3", "OPTN_BIDP4", "OPTN_BIDP5", "ASKP_CSNU1", "ASKP_CSNU2", "ASKP_CSNU3", "ASKP_CSNU4", "ASKP_CSNU5", "BIDP_CSNU1", "BIDP_CSNU2", "BIDP_CSNU3", "BIDP_CSNU4", "BIDP_CSNU5", "ASKP_RSQN1", "ASKP_RSQN2", "ASKP_RSQN3", "ASKP_RSQN4", "ASKP_RSQN5", "BIDP_RSQN1", "BIDP_RSQN2", "BIDP_RSQN3", "BIDP_RSQN4", "BIDP_RSQN5", "TOTAL_ASKP_CSNU", "TOTAL_BIDP_CSNU", "TOTAL_ASKP_RSQN", "TOTAL_BIDP_RSQN", "TOTAL_ASKP_RSQN_ICDC", "TOTAL_BIDP_RSQN_ICDC",)
