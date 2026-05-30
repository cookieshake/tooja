"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0mfasp0Message(KisBaseModel):
    """WS 메시지 1건."""

    FUTS_SHRN_ISCD: str  # 선물 단축 종목코드
    BSOP_HOUR: str  # 영업 시간
    FUTS_ASKP1: str  # 선물 매도호가1
    FUTS_ASKP2: str  # 선물 매도호가2
    FUTS_ASKP3: str  # 선물 매도호가3
    FUTS_ASKP4: str  # 선물 매도호가4
    FUTS_ASKP5: str  # 선물 매도호가5
    FUTS_BIDP1: str  # 선물 매수호가1
    FUTS_BIDP2: str  # 선물 매수호가2
    FUTS_BIDP3: str  # 선물 매수호가3
    FUTS_BIDP4: str  # 선물 매수호가4
    FUTS_BIDP5: str  # 선물 매수호가5
    ASKP_CSNU1: str  # 매도호가 건수1
    ASKP_CSNU2: str  # 매도호가 건수2
    ASKP_CSNU3: str  # 매도호가 건수3
    ASKP_CSNU4: str  # 매도호가 건수4
    ASKP_CSNU5: str  # 매도호가 건수5
    BIDP_CSNU1: str  # 매수호가 건수1
    BIDP_CSNU2: str  # 매수호가 건수2
    BIDP_CSNU3: str  # 매수호가 건수3
    BIDP_CSNU4: str  # 매수호가 건수4
    BIDP_CSNU5: str  # 매수호가 건수5
    ASKP_RSQN1: str  # 매도호가 잔량1
    ASKP_RSQN2: str  # 매도호가 잔량2
    ASKP_RSQN3: str  # 매도호가 잔량3
    ASKP_RSQN4: str  # 매도호가 잔량4
    ASKP_RSQN5: str  # 매도호가 잔량5
    BIDP_RSQN1: str  # 매수호가 잔량1
    BIDP_RSQN2: str  # 매수호가 잔량2
    BIDP_RSQN3: str  # 매수호가 잔량3
    BIDP_RSQN4: str  # 매수호가 잔량4
    BIDP_RSQN5: str  # 매수호가 잔량5
    TOTAL_ASKP_CSNU: str  # 총 매도호가 건수
    TOTAL_BIDP_CSNU: str  # 총 매수호가 건수
    TOTAL_ASKP_RSQN: str  # 총 매도호가 잔량
    TOTAL_BIDP_RSQN: str  # 총 매수호가 잔량
    TOTAL_ASKP_RSQN_ICDC: str  # 총 매도호가 잔량 증감
    TOTAL_BIDP_RSQN_ICDC: str  # 총 매수호가 잔량 증감

class H0mfasp0Subscriber(WsSubscriber[H0mfasp0Message]):
    """KRX야간선물 실시간호가 [실시간-065]."""

    TR_ID = "H0MFASP0"
    RESPONSE_TYPE = H0mfasp0Message
    COLUMNS = ("FUTS_SHRN_ISCD", "BSOP_HOUR", "FUTS_ASKP1", "FUTS_ASKP2", "FUTS_ASKP3", "FUTS_ASKP4", "FUTS_ASKP5", "FUTS_BIDP1", "FUTS_BIDP2", "FUTS_BIDP3", "FUTS_BIDP4", "FUTS_BIDP5", "ASKP_CSNU1", "ASKP_CSNU2", "ASKP_CSNU3", "ASKP_CSNU4", "ASKP_CSNU5", "BIDP_CSNU1", "BIDP_CSNU2", "BIDP_CSNU3", "BIDP_CSNU4", "BIDP_CSNU5", "ASKP_RSQN1", "ASKP_RSQN2", "ASKP_RSQN3", "ASKP_RSQN4", "ASKP_RSQN5", "BIDP_RSQN1", "BIDP_RSQN2", "BIDP_RSQN3", "BIDP_RSQN4", "BIDP_RSQN5", "TOTAL_ASKP_CSNU", "TOTAL_BIDP_CSNU", "TOTAL_ASKP_RSQN", "TOTAL_BIDP_RSQN", "TOTAL_ASKP_RSQN_ICDC", "TOTAL_BIDP_RSQN_ICDC",)
