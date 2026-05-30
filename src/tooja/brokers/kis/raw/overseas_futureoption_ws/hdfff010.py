"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class Hdfff010Message(KisBaseModel):
    """WS 메시지 1건."""

    RECV_DATE: str  # 수신일자
    RECV_TIME: str  # 수신시각
    PREV_PRICE: str  # 전일종가 — 전일종가, 매수1호가~매도5호가 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고
    BID_QNTT_1: str  # 매수1수량
    BID_NUM_1: str  # 매수1번호
    BID_PRICE_1: str  # 매수1호가
    ASK_QNTT_1: str  # 매도1수량
    ASK_NUM_1: str  # 매도1번호
    ASK_PRICE_1: str  # 매도1호가
    BID_QNTT_2: str  # 매수2수량
    BID_NUM_2: str  # 매수2번호
    BID_PRICE_2: str  # 매수2호가
    ASK_QNTT_2: str  # 매도2수량
    ASK_NUM_2: str  # 매도2번호
    ASK_PRICE_2: str  # 매도2호가
    BID_QNTT_3: str  # 매수3수량
    BID_NUM_3: str  # 매수3번호
    BID_PRICE_3: str  # 매수3호가
    ASK_QNTT_3: str  # 매도3수량
    ASK_NUM_3: str  # 매도3번호
    ASK_PRICE_3: str  # 매도3호가
    BID_QNTT_4: str  # 매수4수량
    BID_NUM_4: str  # 매수4번호
    BID_PRICE_4: str  # 매수4호가
    ASK_QNTT_4: str  # 매도4수량
    ASK_NUM_4: str  # 매도4번호
    ASK_PRICE_4: str  # 매도4호가
    BID_QNTT_5: str  # 매수5수량
    BID_NUM_5: str  # 매수5번호
    BID_PRICE_5: str  # 매수5호가
    ASK_QNTT_5: str  # 매도5수량
    ASK_NUM_5: str  # 매도5번호
    ASK_PRICE_5: str  # 매도5호가
    STTL_PRICE: str  # 전일정산가

class Hdfff010Subscriber(WsSubscriber[Hdfff010Message]):
    """해외선물옵션 실시간호가[실시간-018]."""

    TR_ID = "HDFFF010"
    RESPONSE_TYPE = Hdfff010Message
    COLUMNS = ("RECV_DATE", "RECV_TIME", "PREV_PRICE", "BID_QNTT_1", "BID_NUM_1", "BID_PRICE_1", "ASK_QNTT_1", "ASK_NUM_1", "ASK_PRICE_1", "BID_QNTT_2", "BID_NUM_2", "BID_PRICE_2", "ASK_QNTT_2", "ASK_NUM_2", "ASK_PRICE_2", "BID_QNTT_3", "BID_NUM_3", "BID_PRICE_3", "ASK_QNTT_3", "ASK_NUM_3", "ASK_PRICE_3", "BID_QNTT_4", "BID_NUM_4", "BID_PRICE_4", "ASK_QNTT_4", "ASK_NUM_4", "ASK_PRICE_4", "BID_QNTT_5", "BID_NUM_5", "BID_PRICE_5", "ASK_QNTT_5", "ASK_NUM_5", "ASK_PRICE_5", "STTL_PRICE",)
