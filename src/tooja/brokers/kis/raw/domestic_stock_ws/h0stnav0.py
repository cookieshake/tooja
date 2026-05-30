"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0stnav0Message(KisBaseModel):
    """WS 메시지 1건."""

    MKSC_SHRN_ISCD: str  # 유가증권단축종목코드
    NAV: str  # NAV
    NAV_PRDY_VRSS_SIGN: str  # NAV전일대비부호
    NAV_PRDY_VRSS: str  # NAV전일대비
    NAV_PRDY_CTRT: str  # NAV전일대비율
    OPRC_NAV: str  # NAV시가
    HPRC_NAV: str  # NAV고가
    LPRC_NAV: str  # NAV저가

class H0stnav0Subscriber(WsSubscriber[H0stnav0Message]):
    """국내ETF NAV추이 [실시간-051]."""

    TR_ID = "H0STNAV0"
    RESPONSE_TYPE = H0stnav0Message
    COLUMNS = ("MKSC_SHRN_ISCD", "NAV", "NAV_PRDY_VRSS_SIGN", "NAV_PRDY_VRSS", "NAV_PRDY_CTRT", "OPRC_NAV", "HPRC_NAV", "LPRC_NAV",)
