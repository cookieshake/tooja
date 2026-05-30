"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class Hdfscnt0Message(KisBaseModel):
    """WS 메시지 1건."""

    RSYM: str  # 실시간종목코드 — '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨'
    SYMB: str  # 종목코드
    ZDIV: str  # 수수점자리수
    TYMD: str  # 현지영업일자
    XYMD: str  # 현지일자
    XHMS: str  # 현지시간
    KYMD: str  # 한국일자
    KHMS: str  # 한국시간
    OPEN: str  # 시가
    HIGH: str  # 고가
    LOW: str  # 저가
    LAST: str  # 현재가
    SIGN: str  # 대비구분
    DIFF: str  # 전일대비
    RATE: str  # 등락율
    PBID: str  # 매수호가
    PASK: str  # 매도호가
    VBID: str  # 매수잔량
    VASK: str  # 매도잔량
    EVOL: str  # 체결량
    TVOL: str  # 거래량
    TAMT: str  # 거래대금
    BIVL: str  # 매도체결량 — 매수호가가 매도주문 수량을 따라가서 체결된것을 표현하여 BIVL 이라는 표현을 사용
    ASVL: str  # 매수체결량 — 매도호가가 매수주문 수량을 따라가서 체결된것을 표현하여 ASVL 이라는 표현을 사용
    STRN: str  # 체결강도
    MTYP: str  # 시장구분 1:장중,2:장전,3:장후

class Hdfscnt0Subscriber(WsSubscriber[Hdfscnt0Message]):
    """해외주식 실시간지연체결가[실시간-007]."""

    TR_ID = "HDFSCNT0"
    RESPONSE_TYPE = Hdfscnt0Message
    COLUMNS = ("RSYM", "SYMB", "ZDIV", "TYMD", "XYMD", "XHMS", "KYMD", "KHMS", "OPEN", "HIGH", "LOW", "LAST", "SIGN", "DIFF", "RATE", "PBID", "PASK", "VBID", "VASK", "EVOL", "TVOL", "TAMT", "BIVL", "ASVL", "STRN", "MTYP",)
