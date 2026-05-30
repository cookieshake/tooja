"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0zfasp0Message(KisBaseModel):
    """WS 메시지 1건."""

    BSOP_HOUR: str  # 영업시간
    ASKP1: str  # 매도호가1
    ASKP2: str  # 매도호가2
    ASKP3: str  # 매도호가3
    ASKP4: str  # 매도호가4
    ASKP5: str  # 매도호가5
    ASKP6: str  # 매도호가6
    ASKP7: str  # 매도호가7
    ASKP8: str  # 매도호가8
    ASKP9: str  # 매도호가9
    ASKP10: str  # 매도호가10
    BIDP1: str  # 매수호가1
    BIDP2: str  # 매수호가2
    BIDP3: str  # 매수호가3
    BIDP4: str  # 매수호가4
    BIDP5: str  # 매수호가5
    BIDP6: str  # 매수호가6
    BIDP7: str  # 매수호가7
    BIDP8: str  # 매수호가8
    BIDP9: str  # 매수호가9
    BIDP10: str  # 매수호가10
    ASKP_CSNU1: str  # 매도호가건수1
    ASKP_CSNU2: str  # 매도호가건수2
    ASKP_CSNU3: str  # 매도호가건수3
    ASKP_CSNU4: str  # 매도호가건수4
    ASKP_CSNU5: str  # 매도호가건수5
    ASKP_CSNU6: str  # 매도호가건수6
    ASKP_CSNU7: str  # 매도호가건수7
    ASKP_CSNU8: str  # 매도호가건수8
    ASKP_CSNU9: str  # 매도호가건수9
    ASKP_CSNU10: str  # 매도호가건수10
    BIDP_CSNU1: str  # 매수호가건수1
    BIDP_CSNU2: str  # 매수호가건수2
    BIDP_CSNU3: str  # 매수호가건수3
    BIDP_CSNU4: str  # 매수호가건수4
    BIDP_CSNU5: str  # 매수호가건수5
    BIDP_CSNU6: str  # 매수호가건수6
    BIDP_CSNU7: str  # 매수호가건수7
    BIDP_CSNU8: str  # 매수호가건수8
    BIDP_CSNU9: str  # 매수호가건수9
    BIDP_CSNU10: str  # 매수호가건수10
    ASKP_RSQN1: str  # 매도호가잔량1
    ASKP_RSQN2: str  # 매도호가잔량2
    ASKP_RSQN3: str  # 매도호가잔량3
    ASKP_RSQN4: str  # 매도호가잔량4
    ASKP_RSQN5: str  # 매도호가잔량5
    ASKP_RSQN6: str  # 매도호가잔량6
    ASKP_RSQN7: str  # 매도호가잔량7
    ASKP_RSQN8: str  # 매도호가잔량8
    ASKP_RSQN9: str  # 매도호가잔량9
    ASKP_RSQN10: str  # 매도호가잔량10
    BIDP_RSQN1: str  # 매수호가잔량1
    BIDP_RSQN2: str  # 매수호가잔량2
    BIDP_RSQN3: str  # 매수호가잔량3
    BIDP_RSQN4: str  # 매수호가잔량4
    BIDP_RSQN5: str  # 매수호가잔량5
    BIDP_RSQN6: str  # 매수호가잔량6
    BIDP_RSQN7: str  # 매수호가잔량7
    BIDP_RSQN8: str  # 매수호가잔량8
    BIDP_RSQN9: str  # 매수호가잔량9
    BIDP_RSQN10: str  # 매수호가잔량10
    TOTAL_ASKP_CSNU: str  # 총매도호가건수
    TOTAL_BIDP_CSNU: str  # 총매수호가건수
    TOTAL_ASKP_RSQN: str  # 총매도호가잔량
    TOTAL_BIDP_RSQN: str  # 총매수호가잔량
    TOTAL_ASKP_RSQN_ICDC: str  # 총매도호가잔량증감
    TOTAL_BIDP_RSQN_ICDC: str  # 총매수호가잔량증감

class H0zfasp0Subscriber(WsSubscriber[H0zfasp0Message]):
    """주식선물 실시간호가 [실시간-030]."""

    TR_ID = "H0ZFASP0"
    RESPONSE_TYPE = H0zfasp0Message
    COLUMNS = ("BSOP_HOUR", "ASKP1", "ASKP2", "ASKP3", "ASKP4", "ASKP5", "ASKP6", "ASKP7", "ASKP8", "ASKP9", "ASKP10", "BIDP1", "BIDP2", "BIDP3", "BIDP4", "BIDP5", "BIDP6", "BIDP7", "BIDP8", "BIDP9", "BIDP10", "ASKP_CSNU1", "ASKP_CSNU2", "ASKP_CSNU3", "ASKP_CSNU4", "ASKP_CSNU5", "ASKP_CSNU6", "ASKP_CSNU7", "ASKP_CSNU8", "ASKP_CSNU9", "ASKP_CSNU10", "BIDP_CSNU1", "BIDP_CSNU2", "BIDP_CSNU3", "BIDP_CSNU4", "BIDP_CSNU5", "BIDP_CSNU6", "BIDP_CSNU7", "BIDP_CSNU8", "BIDP_CSNU9", "BIDP_CSNU10", "ASKP_RSQN1", "ASKP_RSQN2", "ASKP_RSQN3", "ASKP_RSQN4", "ASKP_RSQN5", "ASKP_RSQN6", "ASKP_RSQN7", "ASKP_RSQN8", "ASKP_RSQN9", "ASKP_RSQN10", "BIDP_RSQN1", "BIDP_RSQN2", "BIDP_RSQN3", "BIDP_RSQN4", "BIDP_RSQN5", "BIDP_RSQN6", "BIDP_RSQN7", "BIDP_RSQN8", "BIDP_RSQN9", "BIDP_RSQN10", "TOTAL_ASKP_CSNU", "TOTAL_BIDP_CSNU", "TOTAL_ASKP_RSQN", "TOTAL_BIDP_RSQN", "TOTAL_ASKP_RSQN_ICDC", "TOTAL_BIDP_RSQN_ICDC",)
