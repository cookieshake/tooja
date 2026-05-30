"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class Hdfsasp1Message(KisBaseModel):
    """WS 메시지 1건."""

    RSYM: str  # 실시간종목코드 — '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨'
    SYMB: str  # 종목코드
    ZDIV: str  # 소수점자리수
    XYMD: str  # 현지일자
    XHMS: str  # 현지시간
    KYMD: str  # 한국일자
    KHMS: str  # 한국시간
    BVOL: str  # 매수총잔량
    AVOL: str  # 매도총잔량
    BDVL: str  # 매수총잔량대비
    ADVL: str  # 매도총잔량대비
    PBID1: str  # 매수호가1
    PASK1: str  # 매도호가1
    VBID1: str  # 매수잔량1
    VASK1: str  # 매도잔량1
    DBID1: str  # 매수잔량대비1
    DASK1: str  # 매도잔량대비1

class Hdfsasp1Subscriber(WsSubscriber[Hdfsasp1Message]):
    """해외주식 지연호가(아시아)[실시간-008]."""

    TR_ID = "HDFSASP1"
    RESPONSE_TYPE = Hdfsasp1Message
    COLUMNS = ("RSYM", "SYMB", "ZDIV", "XYMD", "XHMS", "KYMD", "KHMS", "BVOL", "AVOL", "BDVL", "ADVL", "PBID1", "PASK1", "VBID1", "VASK1", "DBID1", "DASK1",)
