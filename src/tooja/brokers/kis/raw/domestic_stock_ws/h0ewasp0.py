"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0ewasp0Message(KisBaseModel):
    """WS 메시지 1건."""

    MKSC_SHRN_ISCD: str  # 유가증권단축종목코드
    BSOP_HOUR: str  # 영업시간
    HOUR_CLS_CODE: str  # 시간구분코드
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
    TOTAL_ASKP_RSQN: str  # 총매도호가잔량
    TOTAL_BIDP_RSQN: str  # 총매수호가잔량
    ANTC_CNPR: str  # 예상체결가
    ANTC_CNQN: str  # 예상체결량
    ANTC_CNTG_VRSS_SIGN: str  # 예상체결대비부호
    ANTC_CNTG_VRSS: str  # 예상체결대비
    ANTC_CNTG_PRDY_CTRT: str  # 예상체결전일대비율
    LP_ASKP_RSQN1: str  # LP매도호가잔량1
    LP_ASKP_RSQN2: str  # LP매도호가잔량2
    LP_ASKP_RSQN3: str  # LP매도호가잔량3
    LP_BIDP_RSQN4: str  # LP매수호가잔량4
    LP_ASKP_RSQN4: str  # LP매도호가잔량4
    LP_BIDP_RSQN5: str  # LP매수호가잔량5
    LP_ASKP_RSQN5: str  # LP매도호가잔량5
    LP_BIDP_RSQN6: str  # LP매수호가잔량6
    LP_ASKP_RSQN6: str  # LP매도호가잔량6
    LP_BIDP_RSQN7: str  # LP매수호가잔량7
    LP_ASKP_RSQN7: str  # LP매도호가잔량7
    LP_ASKP_RSQN8: str  # LP매도호가잔량8
    LP_BIDP_RSQN8: str  # LP매수호가잔량8
    LP_ASKP_RSQN9: str  # LP매도호가잔량9
    LP_BIDP_RSQN9: str  # LP매수호가잔량9
    LP_ASKP_RSQN10: str  # LP매도호가잔량10
    LP_BIDP_RSQN10: str  # LP매수호가잔량10
    LP_BIDP_RSQN1: str  # LP매수호가잔량1
    LP_TOTAL_ASKP_RSQN: str  # LP총매도호가잔량
    LP_BIDP_RSQN2: str  # LP매수호가잔량2
    LP_TOTAL_BIDP_RSQN: str  # LP총매수호가잔량
    LP_BIDP_RSQN3: str  # LP매수호가잔량3
    ANTC_VOL: str  # 예상거래량

class H0ewasp0Subscriber(WsSubscriber[H0ewasp0Message]):
    """ELW 실시간호가 [실시간-062]."""

    TR_ID = "H0EWASP0"
    RESPONSE_TYPE = H0ewasp0Message
    COLUMNS = ("MKSC_SHRN_ISCD", "BSOP_HOUR", "HOUR_CLS_CODE", "ASKP1", "ASKP2", "ASKP3", "ASKP4", "ASKP5", "ASKP6", "ASKP7", "ASKP8", "ASKP9", "ASKP10", "BIDP1", "BIDP2", "BIDP3", "BIDP4", "BIDP5", "BIDP6", "BIDP7", "BIDP8", "BIDP9", "BIDP10", "ASKP_RSQN1", "ASKP_RSQN2", "ASKP_RSQN3", "ASKP_RSQN4", "ASKP_RSQN5", "ASKP_RSQN6", "ASKP_RSQN7", "ASKP_RSQN8", "ASKP_RSQN9", "ASKP_RSQN10", "BIDP_RSQN1", "BIDP_RSQN2", "BIDP_RSQN3", "BIDP_RSQN4", "BIDP_RSQN5", "BIDP_RSQN6", "BIDP_RSQN7", "BIDP_RSQN8", "BIDP_RSQN9", "BIDP_RSQN10", "TOTAL_ASKP_RSQN", "TOTAL_BIDP_RSQN", "ANTC_CNPR", "ANTC_CNQN", "ANTC_CNTG_VRSS_SIGN", "ANTC_CNTG_VRSS", "ANTC_CNTG_PRDY_CTRT", "LP_ASKP_RSQN1", "LP_ASKP_RSQN2", "LP_ASKP_RSQN3", "LP_BIDP_RSQN4", "LP_ASKP_RSQN4", "LP_BIDP_RSQN5", "LP_ASKP_RSQN5", "LP_BIDP_RSQN6", "LP_ASKP_RSQN6", "LP_BIDP_RSQN7", "LP_ASKP_RSQN7", "LP_ASKP_RSQN8", "LP_BIDP_RSQN8", "LP_ASKP_RSQN9", "LP_BIDP_RSQN9", "LP_ASKP_RSQN10", "LP_BIDP_RSQN10", "LP_BIDP_RSQN1", "LP_TOTAL_ASKP_RSQN", "LP_BIDP_RSQN2", "LP_TOTAL_BIDP_RSQN", "LP_BIDP_RSQN3", "ANTC_VOL",)
