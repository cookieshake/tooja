"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel, SDecimal
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0stcnt0Message(KisBaseModel):
    """WS 메시지 1건."""

    MKSC_SHRN_ISCD: str  # 유가증권 단축 종목코드
    STCK_CNTG_HOUR: str  # 주식 체결 시간
    STCK_PRPR: SDecimal = None  # 주식 현재가 — 체결가격
    PRDY_VRSS_SIGN: str  # 전일 대비 부호 — 1 : 상한 2 : 상승 3 : 보합 4 : 하한 5 : 하락
    PRDY_VRSS: SDecimal = None  # 전일 대비
    PRDY_CTRT: SDecimal = None  # 전일 대비율
    WGHN_AVRG_STCK_PRC: SDecimal = None  # 가중 평균 주식 가격
    STCK_OPRC: SDecimal = None  # 주식 시가
    STCK_HGPR: SDecimal = None  # 주식 최고가
    STCK_LWPR: SDecimal = None  # 주식 최저가
    ASKP1: SDecimal = None  # 매도호가1
    BIDP1: SDecimal = None  # 매수호가1
    CNTG_VOL: SDecimal = None  # 체결 거래량
    ACML_VOL: SDecimal = None  # 누적 거래량
    ACML_TR_PBMN: SDecimal = None  # 누적 거래 대금
    SELN_CNTG_CSNU: SDecimal = None  # 매도 체결 건수
    SHNU_CNTG_CSNU: SDecimal = None  # 매수 체결 건수
    NTBY_CNTG_CSNU: SDecimal = None  # 순매수 체결 건수
    CTTR: SDecimal = None  # 체결강도
    SELN_CNTG_SMTN: SDecimal = None  # 총 매도 수량
    SHNU_CNTG_SMTN: SDecimal = None  # 총 매수 수량
    CCLD_DVSN: str  # 체결구분 — 1:매수(+) 3:장전 5:매도(-)
    SHNU_RATE: SDecimal = None  # 매수비율
    PRDY_VOL_VRSS_ACML_VOL_RATE: SDecimal = None  # 전일 거래량 대비 등락율
    OPRC_HOUR: str  # 시가 시간
    OPRC_VRSS_PRPR_SIGN: str  # 시가대비구분 — 1 : 상한 2 : 상승 3 : 보합 4 : 하한 5 : 하락
    OPRC_VRSS_PRPR: SDecimal = None  # 시가대비
    HGPR_HOUR: str  # 최고가 시간
    HGPR_VRSS_PRPR_SIGN: str  # 고가대비구분 — 1 : 상한 2 : 상승 3 : 보합 4 : 하한 5 : 하락
    HGPR_VRSS_PRPR: SDecimal = None  # 고가대비
    LWPR_HOUR: str  # 최저가 시간
    LWPR_VRSS_PRPR_SIGN: str  # 저가대비구분 — 1 : 상한 2 : 상승 3 : 보합 4 : 하한 5 : 하락
    LWPR_VRSS_PRPR: SDecimal = None  # 저가대비
    BSOP_DATE: str  # 영업 일자
    NEW_MKOP_CLS_CODE: str  # 신 장운영 구분 코드 — (1) 첫 번째 비트 1 : 장개시전 2 : 장중 3 : 장종료후 4 : 시간외단일가 7 : 일반Buy-in 8 : 당일Buy-in (2) 두 번째 비트 0 : 보통 1 : 종가 2 : 대량 3 : 바스켓 7 : 정리매매 8 
    TRHT_YN: str  # 거래정지 여부 — Y : 정지 N : 정상거래
    ASKP_RSQN1: SDecimal = None  # 매도호가 잔량1
    BIDP_RSQN1: SDecimal = None  # 매수호가 잔량1
    TOTAL_ASKP_RSQN: SDecimal = None  # 총 매도호가 잔량
    TOTAL_BIDP_RSQN: SDecimal = None  # 총 매수호가 잔량
    VOL_TNRT: SDecimal = None  # 거래량 회전율
    PRDY_SMNS_HOUR_ACML_VOL: SDecimal = None  # 전일 동시간 누적 거래량
    PRDY_SMNS_HOUR_ACML_VOL_RATE: SDecimal = None  # 전일 동시간 누적 거래량 비율
    HOUR_CLS_CODE: str  # 시간 구분 코드 — 0 : 장중 A : 장후예상 B : 장전예상 C : 9시이후의 예상가, VI발동 D : 시간외 단일가 예상
    MRKT_TRTM_CLS_CODE: str  # 임의종료구분코드
    VI_STND_PRC: SDecimal = None  # 정적VI발동기준가

class H0stcnt0Subscriber(WsSubscriber[H0stcnt0Message]):
    """국내주식 실시간체결가 (KRX) [실시간-003]."""

    TR_ID = "H0STCNT0"
    RESPONSE_TYPE = H0stcnt0Message
    COLUMNS = ("MKSC_SHRN_ISCD", "STCK_CNTG_HOUR", "STCK_PRPR", "PRDY_VRSS_SIGN", "PRDY_VRSS", "PRDY_CTRT", "WGHN_AVRG_STCK_PRC", "STCK_OPRC", "STCK_HGPR", "STCK_LWPR", "ASKP1", "BIDP1", "CNTG_VOL", "ACML_VOL", "ACML_TR_PBMN", "SELN_CNTG_CSNU", "SHNU_CNTG_CSNU", "NTBY_CNTG_CSNU", "CTTR", "SELN_CNTG_SMTN", "SHNU_CNTG_SMTN", "CCLD_DVSN", "SHNU_RATE", "PRDY_VOL_VRSS_ACML_VOL_RATE", "OPRC_HOUR", "OPRC_VRSS_PRPR_SIGN", "OPRC_VRSS_PRPR", "HGPR_HOUR", "HGPR_VRSS_PRPR_SIGN", "HGPR_VRSS_PRPR", "LWPR_HOUR", "LWPR_VRSS_PRPR_SIGN", "LWPR_VRSS_PRPR", "BSOP_DATE", "NEW_MKOP_CLS_CODE", "TRHT_YN", "ASKP_RSQN1", "BIDP_RSQN1", "TOTAL_ASKP_RSQN", "TOTAL_BIDP_RSQN", "VOL_TNRT", "PRDY_SMNS_HOUR_ACML_VOL", "PRDY_SMNS_HOUR_ACML_VOL_RATE", "HOUR_CLS_CODE", "MRKT_TRTM_CLS_CODE", "VI_STND_PRC",)
