"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0bjcnt0Message(KisBaseModel):
    """WS 메시지 1건."""

    STND_ISCD: str  # 표준종목코드
    BOND_ISNM: str  # 채권종목명
    STCK_CNTG_HOUR: str  # 주식체결시간
    PRDY_VRSS_SIGN: str  # 전일대비부호
    PRDY_VRSS: str  # 전일대비
    PRDY_CTRT: str  # 전일대비율
    STCK_PRPR: str  # 현재가
    CNTG_VOL: str  # 체결거래량
    STCK_OPRC: str  # 시가
    STCK_HGPR: str  # 고가
    STCK_LWPR: str  # 저가
    STCK_PRDY_CLPR: str  # 전일종가
    BOND_CNTG_ERT: str  # 현재수익률
    OPRC_ERT: str  # 시가수익률
    HGPR_ERT: str  # 고가수익률
    LWPR_ERT: str  # 저가수익률
    ACML_VOL: str  # 누적거래량
    PRDY_VOL: str  # 전일거래량
    CNTG_TYPE_CLS_CODE: str  # 체결유형코드

class H0bjcnt0Subscriber(WsSubscriber[H0bjcnt0Message]):
    """일반채권 실시간체결가 [실시간-052]."""

    TR_ID = "H0BJCNT0"
    RESPONSE_TYPE = H0bjcnt0Message
    COLUMNS = ("STND_ISCD", "BOND_ISNM", "STCK_CNTG_HOUR", "PRDY_VRSS_SIGN", "PRDY_VRSS", "PRDY_CTRT", "STCK_PRPR", "CNTG_VOL", "STCK_OPRC", "STCK_HGPR", "STCK_LWPR", "STCK_PRDY_CLPR", "BOND_CNTG_ERT", "OPRC_ERT", "HGPR_ERT", "LWPR_ERT", "ACML_VOL", "PRDY_VOL", "CNTG_TYPE_CLS_CODE",)
