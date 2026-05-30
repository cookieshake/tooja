"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel, SDecimal
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0stasp0Message(KisBaseModel):
    """WS 메시지 1건."""

    MKSC_SHRN_ISCD: str  # 유가증권 단축 종목코드
    BSOP_HOUR: str  # 영업 시간
    HOUR_CLS_CODE: str  # 시간 구분 코드 — 0 : 장중 A : 장후예상 B : 장전예상 C : 9시이후의 예상가, VI발동 D : 시간외 단일가 예상
    ASKP1: SDecimal = None  # 매도호가1
    ASKP2: SDecimal = None  # 매도호가2
    ASKP3: SDecimal = None  # 매도호가3
    ASKP4: SDecimal = None  # 매도호가4
    ASKP5: SDecimal = None  # 매도호가5
    ASKP6: SDecimal = None  # 매도호가6
    ASKP7: SDecimal = None  # 매도호가7
    ASKP8: SDecimal = None  # 매도호가8
    ASKP9: SDecimal = None  # 매도호가9
    ASKP10: SDecimal = None  # 매도호가10
    BIDP1: SDecimal = None  # 매수호가1
    BIDP2: SDecimal = None  # 매수호가2
    BIDP3: SDecimal = None  # 매수호가3
    BIDP4: SDecimal = None  # 매수호가4
    BIDP5: SDecimal = None  # 매수호가5
    BIDP6: SDecimal = None  # 매수호가6
    BIDP7: SDecimal = None  # 매수호가7
    BIDP8: SDecimal = None  # 매수호가8
    BIDP9: SDecimal = None  # 매수호가9
    BIDP10: SDecimal = None  # 매수호가10
    ASKP_RSQN1: SDecimal = None  # 매도호가 잔량1
    ASKP_RSQN2: SDecimal = None  # 매도호가 잔량2
    ASKP_RSQN3: SDecimal = None  # 매도호가 잔량3
    ASKP_RSQN4: SDecimal = None  # 매도호가 잔량4
    ASKP_RSQN5: SDecimal = None  # 매도호가 잔량5
    ASKP_RSQN6: SDecimal = None  # 매도호가 잔량6
    ASKP_RSQN7: SDecimal = None  # 매도호가 잔량7
    ASKP_RSQN8: SDecimal = None  # 매도호가 잔량8
    ASKP_RSQN9: SDecimal = None  # 매도호가 잔량9
    ASKP_RSQN10: SDecimal = None  # 매도호가 잔량10
    BIDP_RSQN1: SDecimal = None  # 매수호가 잔량1
    BIDP_RSQN2: SDecimal = None  # 매수호가 잔량2
    BIDP_RSQN3: SDecimal = None  # 매수호가 잔량3
    BIDP_RSQN4: SDecimal = None  # 매수호가 잔량4
    BIDP_RSQN5: SDecimal = None  # 매수호가 잔량5
    BIDP_RSQN6: SDecimal = None  # 매수호가 잔량6
    BIDP_RSQN7: SDecimal = None  # 매수호가 잔량7
    BIDP_RSQN8: SDecimal = None  # 매수호가 잔량8
    BIDP_RSQN9: SDecimal = None  # 매수호가 잔량9
    BIDP_RSQN10: SDecimal = None  # 매수호가 잔량10
    TOTAL_ASKP_RSQN: SDecimal = None  # 총 매도호가 잔량
    TOTAL_BIDP_RSQN: SDecimal = None  # 총 매수호가 잔량
    OVTM_TOTAL_ASKP_RSQN: SDecimal = None  # 시간외 총 매도호가 잔량
    OVTM_TOTAL_BIDP_RSQN: SDecimal = None  # 시간외 총 매수호가 잔량
    ANTC_CNPR: SDecimal = None  # 예상 체결가 — 동시호가 등 특정 조건하에서만 발생
    ANTC_CNQN: SDecimal = None  # 예상 체결량 — 동시호가 등 특정 조건하에서만 발생
    ANTC_VOL: SDecimal = None  # 예상 거래량 — 동시호가 등 특정 조건하에서만 발생
    ANTC_CNTG_VRSS: SDecimal = None  # 예상 체결 대비 — 동시호가 등 특정 조건하에서만 발생
    ANTC_CNTG_VRSS_SIGN: str  # 예상 체결 대비 부호 — 동시호가 등 특정 조건하에서만 발생 1 : 상한 2 : 상승 3 : 보합 4 : 하한 5 : 하락
    ANTC_CNTG_PRDY_CTRT: SDecimal = None  # 예상 체결 전일 대비율
    ACML_VOL: SDecimal = None  # 누적 거래량
    TOTAL_ASKP_RSQN_ICDC: SDecimal = None  # 총 매도호가 잔량 증감
    TOTAL_BIDP_RSQN_ICDC: SDecimal = None  # 총 매수호가 잔량 증감
    OVTM_TOTAL_ASKP_ICDC: SDecimal = None  # 시간외 총 매도호가 증감
    OVTM_TOTAL_BIDP_ICDC: SDecimal = None  # 시간외 총 매수호가 증감
    STCK_DEAL_CLS_CODE: str  # 주식 매매 구분 코드 — 사용 X (삭제된 값)

class H0stasp0Subscriber(WsSubscriber[H0stasp0Message]):
    """국내주식 실시간호가 (KRX) [실시간-004]."""

    TR_ID = "H0STASP0"
    RESPONSE_TYPE = H0stasp0Message
    COLUMNS = ("MKSC_SHRN_ISCD", "BSOP_HOUR", "HOUR_CLS_CODE", "ASKP1", "ASKP2", "ASKP3", "ASKP4", "ASKP5", "ASKP6", "ASKP7", "ASKP8", "ASKP9", "ASKP10", "BIDP1", "BIDP2", "BIDP3", "BIDP4", "BIDP5", "BIDP6", "BIDP7", "BIDP8", "BIDP9", "BIDP10", "ASKP_RSQN1", "ASKP_RSQN2", "ASKP_RSQN3", "ASKP_RSQN4", "ASKP_RSQN5", "ASKP_RSQN6", "ASKP_RSQN7", "ASKP_RSQN8", "ASKP_RSQN9", "ASKP_RSQN10", "BIDP_RSQN1", "BIDP_RSQN2", "BIDP_RSQN3", "BIDP_RSQN4", "BIDP_RSQN5", "BIDP_RSQN6", "BIDP_RSQN7", "BIDP_RSQN8", "BIDP_RSQN9", "BIDP_RSQN10", "TOTAL_ASKP_RSQN", "TOTAL_BIDP_RSQN", "OVTM_TOTAL_ASKP_RSQN", "OVTM_TOTAL_BIDP_RSQN", "ANTC_CNPR", "ANTC_CNQN", "ANTC_VOL", "ANTC_CNTG_VRSS", "ANTC_CNTG_VRSS_SIGN", "ANTC_CNTG_PRDY_CTRT", "ACML_VOL", "TOTAL_ASKP_RSQN_ICDC", "TOTAL_BIDP_RSQN_ICDC", "OVTM_TOTAL_ASKP_ICDC", "OVTM_TOTAL_BIDP_ICDC", "STCK_DEAL_CLS_CODE",)
