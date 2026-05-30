"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class Hdfsasp0Message(KisBaseModel):
    """WS 메시지 1건."""

    SYMB: str  # 종목코드
    ZDIV: str  # 소숫점자리수
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
    PBID2: str  # 매수호가2
    PASK2: str  # 매도호가2
    VBID2: str  # 매수잔량2
    VASK2: str  # 매도잔량2
    DBID2: str  # 매수잔량대비2
    DASK2: str  # 매도잔량대비2
    PBID3: str  # 매수호가3
    PBID3: str  # 매수호가3
    PASK3: str  # 매도호가3
    PASK3: str  # 매도호가3
    VBID3: str  # 매수잔량3
    VBID3: str  # 매수잔량3
    VASK3: str  # 매도잔량3
    VASK3: str  # 매도잔량3
    DBID3: str  # 매수잔량대비3
    DBID3: str  # 매수잔량대비3
    DASK3: str  # 매도잔량대비3
    DASK3: str  # 매도잔량대비3
    PBID4: str  # 매수호가4
    PASK4: str  # 매도호가4
    VBID4: str  # 매수잔량4
    VASK4: str  # 매도잔량4
    DBID4: str  # 매수잔량대비4
    DASK4: str  # 매도잔량대비4
    PBID5: str  # 매수호가5
    PASK5: str  # 매도호가5
    VBID5: str  # 매수잔량5
    VASK5: str  # 매도잔량5
    DBID5: str  # 매수잔량대비5
    DASK5: str  # 매도잔량대비5
    PBID6: str  # 매수호가6
    PASK6: str  # 매도호가6
    VBID6: str  # 매수잔량6
    VASK6: str  # 매도잔량6
    DBID6: str  # 매수잔량대비6
    DASK6: str  # 매도잔량대비6
    PBID7: str  # 매수호가7
    PASK7: str  # 매도호가7
    VBID7: str  # 매수잔량7
    VASK7: str  # 매도잔량7
    DBID7: str  # 매수잔량대비7
    DASK7: str  # 매도잔량대비7
    PBID8: str  # 매수호가8
    PASK8: str  # 매도호가8
    VBID8: str  # 매수잔량8
    VASK8: str  # 매도잔량8
    DBID8: str  # 매수잔량대비8
    DASK8: str  # 매도잔량대비8
    PBID9: str  # 매수호가9
    PASK9: str  # 매도호가9
    VBID9: str  # 매수잔량9
    VASK9: str  # 매도잔량9
    DBID9: str  # 매수잔량대비9
    DASK9: str  # 매도잔량대비9
    PBID10: str  # 매수호가10
    PASK10: str  # 매도호가10
    VBID10: str  # 매수잔량10
    VASK10: str  # 매도잔량10
    DBID10: str  # 매수잔량대비10
    DASK10: str  # 매도잔량대비10

class Hdfsasp0Subscriber(WsSubscriber[Hdfsasp0Message]):
    """해외주식 실시간호가[실시간-021]."""

    TR_ID = "HDFSASP0"
    RESPONSE_TYPE = Hdfsasp0Message
    COLUMNS = ("SYMB", "ZDIV", "XYMD", "XHMS", "KYMD", "KHMS", "BVOL", "AVOL", "BDVL", "ADVL", "PBID1", "PASK1", "VBID1", "VASK1", "DBID1", "DASK1", "PBID2", "PASK2", "VBID2", "VASK2", "DBID2", "DASK2", "PBID3", "PBID3", "PASK3", "PASK3", "VBID3", "VBID3", "VASK3", "VASK3", "DBID3", "DBID3", "DASK3", "DASK3", "PBID4", "PASK4", "VBID4", "VASK4", "DBID4", "DASK4", "PBID5", "PASK5", "VBID5", "VASK5", "DBID5", "DASK5", "PBID6", "PASK6", "VBID6", "VASK6", "DBID6", "DASK6", "PBID7", "PASK7", "VBID7", "VASK7", "DBID7", "DASK7", "PBID8", "PASK8", "VBID8", "VASK8", "DBID8", "DASK8", "PBID9", "PASK9", "VBID9", "VASK9", "DBID9", "DASK9", "PBID10", "PASK10", "VBID10", "VASK10", "DBID10", "DASK10",)
