"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class Hdfff2c0Message(KisBaseModel):
    """WS 메시지 1건."""

    ACCT_NO: str  # 계좌번호
    ORD_DT: str  # 주문일자
    ODNO: str  # 주문번호
    ORGN_ORD_DT: str  # 원주문일자
    ORGN_ODNO: str  # 원주문번호
    SERIES: str  # 종목명
    RVSE_CNCL_DVSN_CD: str  # 정정취소구분코드 — 해당없음 : 00 , 정정 : 01 , 취소 : 02
    SLL_BUY_DVSN_CD: str  # 매도매수구분코드 — 01 : 매도, 02 : 매수
    CPLX_ORD_DVSN_CD: str  # 복합주문구분코드 — 0 (hedge청산만 이용)
    PRCE_TP: str  # 가격구분코드
    FM_EXCG_RCIT_DVSN_CD: str  # FM거래소접수구분코드
    ORD_QTY: str  # 주문수량
    FM_LMT_PRIC: str  # FMLIMIT가격
    FM_STOP_ORD_PRIC: str  # FMSTOP주문가격
    TOT_CCLD_QTY: str  # 총체결수량 — 동일한 주문건에 대한 누적된 체결수량 (하나의 주문건에 여러건의 체결내역 발생)
    TOT_CCLD_UV: str  # 총체결단가
    ORD_REMQ: str  # 잔량
    FM_ORD_GRP_DT: str  # FM주문그룹일자
    ORD_GRP_STNO: str  # 주문그룹번호
    ORD_DTL_DTIME: str  # 주문상세일시
    OPRT_DTL_DTIME: str  # 조작상세일시
    WORK_EMPL: str  # 주문자
    CCLD_DT: str  # 체결일자
    CCNO: str  # 체결번호
    API_CCNO: str  # API 체결번호
    CCLD_QTY: str  # 체결수량 — 매 체결 단위 체결수량임 (여러건 체결내역 누적 체결수량인 총체결수량과 다름)
    FM_CCLD_PRIC: str  # FM체결가격
    CRCY_CD: str  # 통화코드
    TRST_FEE: str  # 위탁수수료
    ORD_MDIA_ONLINE_YN: str  # 주문매체온라인여부
    FM_CCLD_AMT: str  # FM체결금액
    FUOP_ITEM_DVSN_CD: str  # 선물옵션종목구분코드

class Hdfff2c0Subscriber(WsSubscriber[Hdfff2c0Message]):
    """해외선물옵션 실시간체결내역통보[실시간-020]."""

    TR_ID = "HDFFF2C0"
    RESPONSE_TYPE = Hdfff2c0Message
    COLUMNS = ("ACCT_NO", "ORD_DT", "ODNO", "ORGN_ORD_DT", "ORGN_ODNO", "SERIES", "RVSE_CNCL_DVSN_CD", "SLL_BUY_DVSN_CD", "CPLX_ORD_DVSN_CD", "PRCE_TP", "FM_EXCG_RCIT_DVSN_CD", "ORD_QTY", "FM_LMT_PRIC", "FM_STOP_ORD_PRIC", "TOT_CCLD_QTY", "TOT_CCLD_UV", "ORD_REMQ", "FM_ORD_GRP_DT", "ORD_GRP_STNO", "ORD_DTL_DTIME", "OPRT_DTL_DTIME", "WORK_EMPL", "CCLD_DT", "CCNO", "API_CCNO", "CCLD_QTY", "FM_CCLD_PRIC", "CRCY_CD", "TRST_FEE", "ORD_MDIA_ONLINE_YN", "FM_CCLD_AMT", "FUOP_ITEM_DVSN_CD",)
