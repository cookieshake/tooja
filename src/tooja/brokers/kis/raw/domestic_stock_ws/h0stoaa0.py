"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0stoaa0Message(KisBaseModel):
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
    BIDP1: str  # 매수호가1
    BIDP2: str  # 매수호가2
    BIDP3: str  # 매수호가3
    BIDP4: str  # 매수호가4
    BIDP5: str  # 매수호가5
    BIDP6: str  # 매수호가6
    BIDP7: str  # 매수호가7
    BIDP8: str  # 매수호가8
    BIDP9: str  # 매수호가9
    ASKP_RSQN1: str  # 매도호가잔량1
    ASKP_RSQN2: str  # 매도호가잔량2
    ASKP_RSQN3: str  # 매도호가잔량3
    ASKP_RSQN4: str  # 매도호가잔량4
    ASKP_RSQN5: str  # 매도호가잔량5
    ASKP_RSQN6: str  # 매도호가잔량6
    ASKP_RSQN7: str  # 매도호가잔량7
    ASKP_RSQN8: str  # 매도호가잔량8
    ASKP_RSQN9: str  # 매도호가잔량9
    BIDP_RSQN1: str  # 매수호가잔량1
    BIDP_RSQN2: str  # 매수호가잔량2
    BIDP_RSQN3: str  # 매수호가잔량3
    BIDP_RSQN4: str  # 매수호가잔량4
    BIDP_RSQN5: str  # 매수호가잔량5
    BIDP_RSQN6: str  # 매수호가잔량6
    BIDP_RSQN7: str  # 매수호가잔량7
    BIDP_RSQN8: str  # 매수호가잔량8
    BIDP_RSQN9: str  # 매수호가잔량9
    TOTAL_ASKP_RSQN: str  # 총매도호가잔량
    TOTAL_BIDP_RSQN: str  # 총매수호가잔량
    OVTM_TOTAL_ASKP_RSQN: str  # 시간외총매도호가잔량
    OVTM_TOTAL_BIDP_RSQN: str  # 시간외총매수호가잔량
    ANTC_CNPR: str  # 예상체결가
    ANTC_CNQN: str  # 예상체결량
    ANTC_VOL: str  # 예상거래량
    ANTC_CNTG_VRSS: str  # 예상체결대비
    ANTC_CNTG_VRSS_SIGN: str  # 예상체결대비부호
    ANTC_CNTG_PRDY_CTRT: str  # 예상체결전일대비율
    ACML_VOL: str  # 누적거래량
    TOTAL_ASKP_RSQN_ICDC: str  # 총매도호가잔량증감
    TOTAL_BIDP_RSQN_ICDC: str  # 총매수호가잔량증감
    OVTM_TOTAL_ASKP_ICDC: str  # 시간외총매도호가증감
    OVTM_TOTAL_BIDP_ICDC: str  # 시간외총매수호가증감

class H0stoaa0Subscriber(WsSubscriber[H0stoaa0Message]):
    """국내주식 시간외 실시간호가 (KRX) [실시간-025]."""

    TR_ID = "H0STOAA0"
    RESPONSE_TYPE = H0stoaa0Message
    COLUMNS = ("MKSC_SHRN_ISCD", "BSOP_HOUR", "HOUR_CLS_CODE", "ASKP1", "ASKP2", "ASKP3", "ASKP4", "ASKP5", "ASKP6", "ASKP7", "ASKP8", "ASKP9", "BIDP1", "BIDP2", "BIDP3", "BIDP4", "BIDP5", "BIDP6", "BIDP7", "BIDP8", "BIDP9", "ASKP_RSQN1", "ASKP_RSQN2", "ASKP_RSQN3", "ASKP_RSQN4", "ASKP_RSQN5", "ASKP_RSQN6", "ASKP_RSQN7", "ASKP_RSQN8", "ASKP_RSQN9", "BIDP_RSQN1", "BIDP_RSQN2", "BIDP_RSQN3", "BIDP_RSQN4", "BIDP_RSQN5", "BIDP_RSQN6", "BIDP_RSQN7", "BIDP_RSQN8", "BIDP_RSQN9", "TOTAL_ASKP_RSQN", "TOTAL_BIDP_RSQN", "OVTM_TOTAL_ASKP_RSQN", "OVTM_TOTAL_BIDP_RSQN", "ANTC_CNPR", "ANTC_CNQN", "ANTC_VOL", "ANTC_CNTG_VRSS", "ANTC_CNTG_VRSS_SIGN", "ANTC_CNTG_PRDY_CTRT", "ACML_VOL", "TOTAL_ASKP_RSQN_ICDC", "TOTAL_BIDP_RSQN_ICDC", "OVTM_TOTAL_ASKP_ICDC", "OVTM_TOTAL_BIDP_ICDC",)
