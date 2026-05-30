"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class Hdfff1c0Message(KisBaseModel):
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
    PRCE_TP: str  # 가격구분코드 — 1:Limit, 2:Market, 3:Stop(Stop가격시 시장가)
    FM_EXCG_RCIT_DVSN_CD: str  # FM거래소접수구분코드 — 01:접수전, 02:응답, 03:거부
    ORD_QTY: str  # 주문수량
    FM_LMT_PRIC: str  # FMLIMIT가격
    FM_STOP_ORD_PRIC: str  # FMSTOP주문가격
    TOT_CCLD_QTY: str  # 총체결수량
    TOT_CCLD_UV: str  # 총체결단가
    ORD_REMQ: str  # 잔량
    FM_ORD_GRP_DT: str  # FM주문그룹일자 — 주문일자(ORD_DT)와 동일
    ORD_GRP_STNO: str  # 주문그룹번호
    ORD_DTL_DTIME: str  # 주문상세일시
    OPRT_DTL_DTIME: str  # 조작상세일시
    WORK_EMPL: str  # 주문자
    CRCY_CD: str  # 통화코드
    LQD_YN: str  # 청산여부(Y/N)
    LQD_LMT_PRIC: str  # 청산LIMIT가격
    LQD_STOP_PRIC: str  # 청산STOP가격
    TRD_COND: str  # 체결조건코드
    TERM_ORD_VALD_DTIME: str  # 기간주문유효상세일시
    SPEC_TP: str  # 계좌청산유형구분코드
    ECIS_RSVN_ORD_YN: str  # 행사예약주문여부
    AUTO_ORD_DVSN_CD: str  # 자동주문 전략구분
    FUOP_ITEM_DVSN_CD: str  # 선물옵션종목구분코드

class Hdfff1c0Subscriber(WsSubscriber[Hdfff1c0Message]):
    """해외선물옵션 실시간주문내역통보[실시간-019]."""

    TR_ID = "HDFFF1C0"
    RESPONSE_TYPE = Hdfff1c0Message
    COLUMNS = ("ACCT_NO", "ORD_DT", "ODNO", "ORGN_ORD_DT", "ORGN_ODNO", "SERIES", "RVSE_CNCL_DVSN_CD", "SLL_BUY_DVSN_CD", "CPLX_ORD_DVSN_CD", "PRCE_TP", "FM_EXCG_RCIT_DVSN_CD", "ORD_QTY", "FM_LMT_PRIC", "FM_STOP_ORD_PRIC", "TOT_CCLD_QTY", "TOT_CCLD_UV", "ORD_REMQ", "FM_ORD_GRP_DT", "ORD_GRP_STNO", "ORD_DTL_DTIME", "OPRT_DTL_DTIME", "WORK_EMPL", "CRCY_CD", "LQD_YN", "LQD_LMT_PRIC", "LQD_STOP_PRIC", "TRD_COND", "TERM_ORD_VALD_DTIME", "SPEC_TP", "ECIS_RSVN_ORD_YN", "AUTO_ORD_DVSN_CD", "FUOP_ITEM_DVSN_CD",)
