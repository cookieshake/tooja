"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0zfanc0Message(KisBaseModel):
    """WS 메시지 1건."""

    FUTS_SHRN_ISCD: str  # 선물단축종목코드
    BSOP_HOUR: str  # 영업시간
    ANTC_CNPR: str  # 예상체결가
    ANTC_CNTG_VRSS: str  # 예상체결대비
    ANTC_CNTG_VRSS_SIGN: str  # 예상체결대비부호
    ANTC_CNTG_PRDY_CTRT: str  # 예상체결전일대비율
    ANTC_MKOP_CLS_CODE: str  # 예상장운영구분코드
    ANTC_CNQN: str  # 예상체결수량

class H0zfanc0Subscriber(WsSubscriber[H0zfanc0Message]):
    """주식선물 실시간예상체결 [실시간-031]."""

    TR_ID = "H0ZFANC0"
    RESPONSE_TYPE = H0zfanc0Message
    COLUMNS = ("FUTS_SHRN_ISCD", "BSOP_HOUR", "ANTC_CNPR", "ANTC_CNTG_VRSS", "ANTC_CNTG_VRSS_SIGN", "ANTC_CNTG_PRDY_CTRT", "ANTC_MKOP_CLS_CODE", "ANTC_CNQN",)
