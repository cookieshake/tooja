"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0stmko0Message(KisBaseModel):
    """WS 메시지 1건."""

    TRHT_YN: str  # 거래정지여부
    TR_SUSP_REAS_CNTT: str  # 거래정지사유내용
    MKOP_CLS_CODE: str  # 장운영구분코드 — 110 장전 동시호가 개시 112 장개시 121 장후 동시호가 개시 129 장마감 130 장개시전시간외개시 139 장개시전시간외종료 140 시간외 종가 매매 개시 146 장종료후시간외 체결지시 149 시간외 종가 매매 종료 150 시
    ANTC_MKOP_CLS_CODE: str  # 예상장운영구분코드 — 112 장전예상종료 121 장후예상시작 129 장후예상종료 311 장전예상시작
    MRKT_TRTM_CLS_CODE: str  # 임의연장구분코드 — 1 시초동시 임의종료 지정 2 시초동시 임의종료 해제 3 마감동시 임의종료 지정 4 마감동시 임의종료 해제 5 시간외단일가임의종료 지정 6 시간외단일가임의종료 해제
    DIVI_APP_CLS_CODE: str  # 동시호가배분처리구분코드 — divi_app_cls_code[0] 1: 배분개시 2: 배분해제 divi_app_cls_code[1] 1: 매수상한 2: 매수하한 3: 매도상한 4: 매도하한
    ISCD_STAT_CLS_CODE: str  # 종목상태구분코드 — 51 관리종목 지정 종목 52 시장경고 구분이 '투자위험'인 종목 53 시장경고 구분이 '투자경고'인 종목 54 시장경고 구분이 '투자주의'인 종목 55 당사 신용가능 종목 57 당사 증거금률이 100인 종목 58 거래정지 지정된 
    VI_CLS_CODE: str  # VI적용구분코드 — Y VI적용된 종목 N VI적용되지 않은 종목
    OVTM_VI_CLS_CODE: str  # 시간외단일가VI적용구분코드 — Y 시간외단일가VI 적용된 종목 N 시간외단일가VI 적용되지 않은 종목
    EXCH_CLS_CODE: str  # 거래소구분코드

class H0stmko0Subscriber(WsSubscriber[H0stmko0Message]):
    """국내주식 장운영정보 (KRX) [실시간-049]."""

    TR_ID = "H0STMKO0"
    RESPONSE_TYPE = H0stmko0Message
    COLUMNS = ("TRHT_YN", "TR_SUSP_REAS_CNTT", "MKOP_CLS_CODE", "ANTC_MKOP_CLS_CODE", "MRKT_TRTM_CLS_CODE", "DIVI_APP_CLS_CODE", "ISCD_STAT_CLS_CODE", "VI_CLS_CODE", "OVTM_VI_CLS_CODE", "EXCH_CLS_CODE",)
