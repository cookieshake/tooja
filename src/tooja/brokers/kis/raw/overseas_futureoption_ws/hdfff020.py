"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class Hdfff020Message(KisBaseModel):
    """WS 메시지 1건."""

    SERIES_CD: str  # 종목코드 — '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨'
    BSNS_DATE: str  # 영업일자
    MRKT_OPEN_DATE: str  # 장개시일자
    MRKT_OPEN_TIME: str  # 장개시시각
    MRKT_CLOSE_DATE: str  # 장종료일자
    MRKT_CLOSE_TIME: str  # 장종료시각
    PREV_PRICE: str  # 전일종가 — 전일종가, 체결가격, 전일대비가, 시가, 고가, 저가 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고
    RECV_DATE: str  # 수신일자
    RECV_TIME: str  # 수신시각 — 수신시각(recv_time) = 실제 체결시각
    ACTIVE_FLAG: str  # 본장_전산장구분
    LAST_PRICE: str  # 체결가격
    LAST_QNTT: str  # 체결수량
    PREV_DIFF_PRICE: str  # 전일대비가
    PREV_DIFF_RATE: str  # 등락률
    OPEN_PRICE: str  # 시가
    HIGH_PRICE: str  # 고가
    LOW_PRICE: str  # 저가
    VOL: str  # 누적거래량
    PREV_SIGN: str  # 전일대비부호
    QUOTSIGN: str  # 체결구분 — 2:매수체결 5:매도체결
    RECV_TIME2: str  # 수신시각2 만분의일초
    PSTTL_PRICE: str  # 전일정산가
    PSTTL_SIGN: str  # 전일정산가대비
    PSTTL_DIFF_PRICE: str  # 전일정산가대비가격
    PSTTL_DIFF_RATE: str  # 전일정산가대비율

class Hdfff020Subscriber(WsSubscriber[Hdfff020Message]):
    """해외선물옵션 실시간체결가[실시간-017]."""

    TR_ID = "HDFFF020"
    RESPONSE_TYPE = Hdfff020Message
    COLUMNS = ("SERIES_CD", "BSNS_DATE", "MRKT_OPEN_DATE", "MRKT_OPEN_TIME", "MRKT_CLOSE_DATE", "MRKT_CLOSE_TIME", "PREV_PRICE", "RECV_DATE", "RECV_TIME", "ACTIVE_FLAG", "LAST_PRICE", "LAST_QNTT", "PREV_DIFF_PRICE", "PREV_DIFF_RATE", "OPEN_PRICE", "HIGH_PRICE", "LOW_PRICE", "VOL", "PREV_SIGN", "QUOTSIGN", "RECV_TIME2", "PSTTL_PRICE", "PSTTL_SIGN", "PSTTL_DIFF_PRICE", "PSTTL_DIFF_RATE",)
