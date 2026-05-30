"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0nxasp0Message(KisBaseModel):
    """WS 메시지 1건."""

    MKSC_SHRN_ISCD: str  # 유가증권 단축 종목코드
    BSOP_HOUR: str  # 영업 시간
    HOUR_CLS_CODE: str  # 시간 구분 코드
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
    ASKP_RSQN1: str  # 매도호가 잔량1
    ASKP_RSQN2: str  # 매도호가 잔량2
    ASKP_RSQN3: str  # 매도호가 잔량3
    ASKP_RSQN4: str  # 매도호가 잔량4
    ASKP_RSQN5: str  # 매도호가 잔량5
    ASKP_RSQN6: str  # 매도호가 잔량6
    ASKP_RSQN7: str  # 매도호가 잔량7
    ASKP_RSQN8: str  # 매도호가 잔량8
    ASKP_RSQN9: str  # 매도호가 잔량9
    ASKP_RSQN10: str  # 매도호가 잔량10
    BIDP_RSQN1: str  # 매수호가 잔량1
    BIDP_RSQN2: str  # 매수호가 잔량2
    BIDP_RSQN3: str  # 매수호가 잔량3
    BIDP_RSQN4: str  # 매수호가 잔량4
    BIDP_RSQN5: str  # 매수호가 잔량5
    BIDP_RSQN6: str  # 매수호가 잔량6
    BIDP_RSQN7: str  # 매수호가 잔량7
    BIDP_RSQN8: str  # 매수호가 잔량8
    BIDP_RSQN9: str  # 매수호가 잔량9
    BIDP_RSQN10: str  # 매수호가 잔량10
    TOTAL_ASKP_RSQN: str  # 총 매도호가 잔량
    TOTAL_BIDP_RSQN: str  # 총 매수호가 잔량
    OVTM_TOTAL_ASKP_RSQN: str  # 시간외 총 매도호가 잔량
    OVTM_TOTAL_BIDP_RSQN: str  # 시간외 총 매수호가 잔량
    ANTC_CNPR: str  # 예상 체결가
    ANTC_CNQN: str  # 예상 체결량
    ANTC_VOL: str  # 예상 거래량
    ANTC_CNTG_VRSS: str  # 예상 체결 대비
    ANTC_CNTG_VRSS_SIGN: str  # 예상 체결 대비 부호
    ANTC_CNTG_PRDY_CTRT: str  # 예상 체결 전일 대비율
    ACML_VOL: str  # 누적 거래량
    TOTAL_ASKP_RSQN_ICDC: str  # 총 매도호가 잔량 증감
    TOTAL_BIDP_RSQN_ICDC: str  # 총 매수호가 잔량 증감
    OVTM_TOTAL_ASKP_ICDC: str  # 시간외 총 매도호가 증감
    OVTM_TOTAL_BIDP_ICDC: str  # 시간외 총 매수호가 증감
    STCK_DEAL_CLS_CODE: str  # 주식 매매 구분 코드
    KMID_PRC: str  # KRX 중간가
    KMID_TOTAL_RSQN: str  # KRX 중간가잔량합계수량
    KMID_CLS_CODE: str  # KRX 중간가 매수매도 구분
    NMID_PRC: str  # NXT 중간가
    NMID_TOTAL_RSQN: str  # NXT 중간가잔량합계수량
    NMID_CLS_CODE: str  # NXT 중간가 매수매도 구분

class H0nxasp0Subscriber(WsSubscriber[H0nxasp0Message]):
    """국내주식 실시간호가 (NXT)."""

    TR_ID = "H0NXASP0"
    RESPONSE_TYPE = H0nxasp0Message
    COLUMNS = ("MKSC_SHRN_ISCD", "BSOP_HOUR", "HOUR_CLS_CODE", "ASKP1", "ASKP2", "ASKP3", "ASKP4", "ASKP5", "ASKP6", "ASKP7", "ASKP8", "ASKP9", "ASKP10", "BIDP1", "BIDP2", "BIDP3", "BIDP4", "BIDP5", "BIDP6", "BIDP7", "BIDP8", "BIDP9", "BIDP10", "ASKP_RSQN1", "ASKP_RSQN2", "ASKP_RSQN3", "ASKP_RSQN4", "ASKP_RSQN5", "ASKP_RSQN6", "ASKP_RSQN7", "ASKP_RSQN8", "ASKP_RSQN9", "ASKP_RSQN10", "BIDP_RSQN1", "BIDP_RSQN2", "BIDP_RSQN3", "BIDP_RSQN4", "BIDP_RSQN5", "BIDP_RSQN6", "BIDP_RSQN7", "BIDP_RSQN8", "BIDP_RSQN9", "BIDP_RSQN10", "TOTAL_ASKP_RSQN", "TOTAL_BIDP_RSQN", "OVTM_TOTAL_ASKP_RSQN", "OVTM_TOTAL_BIDP_RSQN", "ANTC_CNPR", "ANTC_CNQN", "ANTC_VOL", "ANTC_CNTG_VRSS", "ANTC_CNTG_VRSS_SIGN", "ANTC_CNTG_PRDY_CTRT", "ACML_VOL", "TOTAL_ASKP_RSQN_ICDC", "TOTAL_BIDP_RSQN_ICDC", "OVTM_TOTAL_ASKP_ICDC", "OVTM_TOTAL_BIDP_ICDC", "STCK_DEAL_CLS_CODE", "KMID_PRC", "KMID_TOTAL_RSQN", "KMID_CLS_CODE", "NMID_PRC", "NMID_TOTAL_RSQN", "NMID_CLS_CODE",)
