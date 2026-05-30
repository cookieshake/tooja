"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0unmko0Message(KisBaseModel):
    """WS 메시지 1건."""

    TRHT_YN: str  # 거래정지 여부
    TR_SUSP_REAS_CNTT: str  # 거래 정지 사유 내용
    MKOP_CLS_CODE: str  # 장운영 구분 코드
    ANTC_MKOP_CLS_CODE: str  # 예상 장운영 구분 코드
    MRKT_TRTM_CLS_CODE: str  # 임의연장구분코드
    DIVI_APP_CLS_CODE: str  # 동시호가배분처리구분코드
    ISCD_STAT_CLS_CODE: str  # 종목상태구분코드
    VI_CLS_CODE: str  # VI적용구분코드
    OVTM_VI_CLS_CODE: str  # 시간외단일가VI적용구분코드
    EXCH_CLS_CODE: str  # 거래소 구분코드

class H0unmko0Subscriber(WsSubscriber[H0unmko0Message]):
    """국내주식 장운영정보 (통합)."""

    TR_ID = "H0UNMKO0"
    RESPONSE_TYPE = H0unmko0Message
    COLUMNS = ("TRHT_YN", "TR_SUSP_REAS_CNTT", "MKOP_CLS_CODE", "ANTC_MKOP_CLS_CODE", "MRKT_TRTM_CLS_CODE", "DIVI_APP_CLS_CODE", "ISCD_STAT_CLS_CODE", "VI_CLS_CODE", "OVTM_VI_CLS_CODE", "EXCH_CLS_CODE",)
