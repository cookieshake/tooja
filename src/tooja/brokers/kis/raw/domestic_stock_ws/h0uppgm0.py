"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0uppgm0Message(KisBaseModel):
    """WS 메시지 1건."""

    BSOP_HOUR: str  # 영업 시간
    ARBT_SELN_ENTM_CNQN: str  # 차익 매도 위탁 체결량
    ARBT_SELN_ONSL_CNQN: str  # 차익 매도 자기 체결량
    ARBT_SHNU_ENTM_CNQN: str  # 차익 매수2 위탁 체결량
    ARBT_SHNU_ONSL_CNQN: str  # 차익 매수2 자기 체결량
    NABT_SELN_ENTM_CNQN: str  # 비차익 매도 위탁 체결량
    NABT_SELN_ONSL_CNQN: str  # 비차익 매도 자기 체결량
    NABT_SHNU_ENTM_CNQN: str  # 비차익 매수2 위탁 체결량
    NABT_SHNU_ONSL_CNQN: str  # 비차익 매수2 자기 체결량
    ARBT_SELN_ENTM_CNTG_AMT: str  # 차익 매도 위탁 체결 금액
    ARBT_SELN_ONSL_CNTG_AMT: str  # 차익 매도 자기 체결 금액
    ARBT_SHNU_ENTM_CNTG_AMT: str  # 차익 매수2 위탁 체결 금액
    ARBT_SHNU_ONSL_CNTG_AMT: str  # 차익 매수2 자기 체결 금액
    NABT_SELN_ENTM_CNTG_AMT: str  # 비차익 매도 위탁 체결 금액
    NABT_SELN_ONSL_CNTG_AMT: str  # 비차익 매도 자기 체결 금액
    NABT_SHNU_ENTM_CNTG_AMT: str  # 비차익 매수2 위탁 체결 금액
    NABT_SHNU_ONSL_CNTG_AMT: str  # 비차익 매수2 자기 체결 금액
    ARBT_SMTN_SELN_VOL: str  # 차익 합계 매도 거래량
    ARBT_SMTM_SELN_VOL_RATE: str  # 차익 합계 매도 거래량 비율
    ARBT_SMTN_SELN_TR_PBMN: str  # 차익 합계 매도 거래 대금
    ARBT_SMTM_SELN_TR_PBMN_RATE: str  # 차익 합계 매도 거래대금 비율
    ARBT_SMTN_SHNU_VOL: str  # 차익 합계 매수2 거래량
    ARBT_SMTM_SHNU_VOL_RATE: str  # 차익 합계 매수 거래량 비율
    ARBT_SMTN_SHNU_TR_PBMN: str  # 차익 합계 매수2 거래 대금
    ARBT_SMTM_SHNU_TR_PBMN_RATE: str  # 차익 합계 매수 거래대금 비율
    ARBT_SMTN_NTBY_QTY: str  # 차익 합계 순매수 수량
    ARBT_SMTM_NTBY_QTY_RATE: str  # 차익 합계 순매수 수량 비율
    ARBT_SMTN_NTBY_TR_PBMN: str  # 차익 합계 순매수 거래 대금
    ARBT_SMTM_NTBY_TR_PBMN_RATE: str  # 차익 합계 순매수 거래대금 비율
    NABT_SMTN_SELN_VOL: str  # 비차익 합계 매도 거래량
    NABT_SMTM_SELN_VOL_RATE: str  # 비차익 합계 매도 거래량 비율
    NABT_SMTN_SELN_TR_PBMN: str  # 비차익 합계 매도 거래 대금
    NABT_SMTM_SELN_TR_PBMN_RATE: str  # 비차익 합계 매도 거래대금 비율
    NABT_SMTN_SHNU_VOL: str  # 비차익 합계 매수2 거래량
    NABT_SMTM_SHNU_VOL_RATE: str  # 비차익 합계 매수 거래량 비율
    NABT_SMTN_SHNU_TR_PBMN: str  # 비차익 합계 매수2 거래 대금
    NABT_SMTM_SHNU_TR_PBMN_RATE: str  # 비차익 합계 매수 거래대금 비율
    NABT_SMTN_NTBY_QTY: str  # 비차익 합계 순매수 수량
    NABT_SMTM_NTBY_QTY_RATE: str  # 비차익 합계 순매수 수량 비율
    NABT_SMTN_NTBY_TR_PBMN: str  # 비차익 합계 순매수 거래 대금
    NABT_SMTM_NTBY_TR_PBMN_RATE: str  # 비차익 합계 순매수 거래대금 비
    WHOL_ENTM_SELN_VOL: str  # 전체 위탁 매도 거래량
    ENTM_SELN_VOL_RATE: str  # 위탁 매도 거래량 비율
    WHOL_ENTM_SELN_TR_PBMN: str  # 전체 위탁 매도 거래 대금
    ENTM_SELN_TR_PBMN_RATE: str  # 위탁 매도 거래대금 비율
    WHOL_ENTM_SHNU_VOL: str  # 전체 위탁 매수2 거래량
    ENTM_SHNU_VOL_RATE: str  # 위탁 매수 거래량 비율
    WHOL_ENTM_SHNU_TR_PBMN: str  # 전체 위탁 매수2 거래 대금
    ENTM_SHNU_TR_PBMN_RATE: str  # 위탁 매수 거래대금 비율
    WHOL_ENTM_NTBY_QT: str  # 전체 위탁 순매수 수량
    ENTM_NTBY_QTY_RAT: str  # 위탁 순매수 수량 비율
    WHOL_ENTM_NTBY_TR_PBMN: str  # 전체 위탁 순매수 거래 대금
    ENTM_NTBY_TR_PBMN_RATE: str  # 위탁 순매수 금액 비율
    WHOL_ONSL_SELN_VOL: str  # 전체 자기 매도 거래량
    ONSL_SELN_VOL_RATE: str  # 자기 매도 거래량 비율
    WHOL_ONSL_SELN_TR_PBMN: str  # 전체 자기 매도 거래 대금
    ONSL_SELN_TR_PBMN_RATE: str  # 자기 매도 거래대금 비율
    WHOL_ONSL_SHNU_VOL: str  # 전체 자기 매수2 거래량
    ONSL_SHNU_VOL_RATE: str  # 자기 매수 거래량 비율
    WHOL_ONSL_SHNU_TR_PBMN: str  # 전체 자기 매수2 거래 대금
    ONSL_SHNU_TR_PBMN_RATE: str  # 자기 매수 거래대금 비율
    WHOL_ONSL_NTBY_QTY: str  # 전체 자기 순매수 수량
    ONSL_NTBY_QTY_RATE: str  # 자기 순매수량 비율
    WHOL_ONSL_NTBY_TR_PBMN: str  # 전체 자기 순매수 거래 대금
    ONSL_NTBY_TR_PBMN_RATE: str  # 자기 순매수 대금 비율
    TOTAL_SELN_QTY: str  # 총 매도 수량
    WHOL_SELN_VOL_RATE: str  # 전체 매도 거래량 비율
    TOTAL_SELN_TR_PBMN: str  # 총 매도 거래 대금
    WHOL_SELN_TR_PBMN_RATE: str  # 전체 매도 거래대금 비율
    SHNU_CNTG_SMTN: str  # 총 매수 수량
    WHOL_SHUN_VOL_RATE: str  # 전체 매수 거래량 비율
    TOTAL_SHNU_TR_PBMN: str  # 총 매수2 거래 대금
    WHOL_SHUN_TR_PBMN_RATE: str  # 전체 매수 거래대금 비율
    WHOL_NTBY_QTY: str  # 전체 순매수 수량
    WHOL_SMTM_NTBY_QTY_RATE: str  # 전체 합계 순매수 수량 비율
    WHOL_NTBY_TR_PBMN: str  # 전체 순매수 거래 대금
    WHOL_NTBY_TR_PBMN_RATE: str  # 전체 순매수 거래대금 비율
    ARBT_ENTM_NTBY_QTY: str  # 차익 위탁 순매수 수량
    ARBT_ENTM_NTBY_TR_PBMN: str  # 차익 위탁 순매수 거래 대금
    ARBT_ONSL_NTBY_QTY: str  # 차익 자기 순매수 수량
    ARBT_ONSL_NTBY_TR_PBMN: str  # 차익 자기 순매수 거래 대금
    NABT_ENTM_NTBY_QTY: str  # 비차익 위탁 순매수 수량
    NABT_ENTM_NTBY_TR_PBMN: str  # 비차익 위탁 순매수 거래 대금
    NABT_ONSL_NTBY_QTY: str  # 비차익 자기 순매수 수량
    NABT_ONSL_NTBY_TR_PBMN: str  # 비차익 자기 순매수 거래 대금
    ACML_VOL: str  # 누적 거래량
    ACML_TR_PBMN: str  # 누적 거래 대금

class H0uppgm0Subscriber(WsSubscriber[H0uppgm0Message]):
    """국내지수 실시간프로그램매매 [실시간-028]."""

    TR_ID = "H0UPPGM0"
    RESPONSE_TYPE = H0uppgm0Message
    COLUMNS = ("BSOP_HOUR", "ARBT_SELN_ENTM_CNQN", "ARBT_SELN_ONSL_CNQN", "ARBT_SHNU_ENTM_CNQN", "ARBT_SHNU_ONSL_CNQN", "NABT_SELN_ENTM_CNQN", "NABT_SELN_ONSL_CNQN", "NABT_SHNU_ENTM_CNQN", "NABT_SHNU_ONSL_CNQN", "ARBT_SELN_ENTM_CNTG_AMT", "ARBT_SELN_ONSL_CNTG_AMT", "ARBT_SHNU_ENTM_CNTG_AMT", "ARBT_SHNU_ONSL_CNTG_AMT", "NABT_SELN_ENTM_CNTG_AMT", "NABT_SELN_ONSL_CNTG_AMT", "NABT_SHNU_ENTM_CNTG_AMT", "NABT_SHNU_ONSL_CNTG_AMT", "ARBT_SMTN_SELN_VOL", "ARBT_SMTM_SELN_VOL_RATE", "ARBT_SMTN_SELN_TR_PBMN", "ARBT_SMTM_SELN_TR_PBMN_RATE", "ARBT_SMTN_SHNU_VOL", "ARBT_SMTM_SHNU_VOL_RATE", "ARBT_SMTN_SHNU_TR_PBMN", "ARBT_SMTM_SHNU_TR_PBMN_RATE", "ARBT_SMTN_NTBY_QTY", "ARBT_SMTM_NTBY_QTY_RATE", "ARBT_SMTN_NTBY_TR_PBMN", "ARBT_SMTM_NTBY_TR_PBMN_RATE", "NABT_SMTN_SELN_VOL", "NABT_SMTM_SELN_VOL_RATE", "NABT_SMTN_SELN_TR_PBMN", "NABT_SMTM_SELN_TR_PBMN_RATE", "NABT_SMTN_SHNU_VOL", "NABT_SMTM_SHNU_VOL_RATE", "NABT_SMTN_SHNU_TR_PBMN", "NABT_SMTM_SHNU_TR_PBMN_RATE", "NABT_SMTN_NTBY_QTY", "NABT_SMTM_NTBY_QTY_RATE", "NABT_SMTN_NTBY_TR_PBMN", "NABT_SMTM_NTBY_TR_PBMN_RATE", "WHOL_ENTM_SELN_VOL", "ENTM_SELN_VOL_RATE", "WHOL_ENTM_SELN_TR_PBMN", "ENTM_SELN_TR_PBMN_RATE", "WHOL_ENTM_SHNU_VOL", "ENTM_SHNU_VOL_RATE", "WHOL_ENTM_SHNU_TR_PBMN", "ENTM_SHNU_TR_PBMN_RATE", "WHOL_ENTM_NTBY_QT", "ENTM_NTBY_QTY_RAT", "WHOL_ENTM_NTBY_TR_PBMN", "ENTM_NTBY_TR_PBMN_RATE", "WHOL_ONSL_SELN_VOL", "ONSL_SELN_VOL_RATE", "WHOL_ONSL_SELN_TR_PBMN", "ONSL_SELN_TR_PBMN_RATE", "WHOL_ONSL_SHNU_VOL", "ONSL_SHNU_VOL_RATE", "WHOL_ONSL_SHNU_TR_PBMN", "ONSL_SHNU_TR_PBMN_RATE", "WHOL_ONSL_NTBY_QTY", "ONSL_NTBY_QTY_RATE", "WHOL_ONSL_NTBY_TR_PBMN", "ONSL_NTBY_TR_PBMN_RATE", "TOTAL_SELN_QTY", "WHOL_SELN_VOL_RATE", "TOTAL_SELN_TR_PBMN", "WHOL_SELN_TR_PBMN_RATE", "SHNU_CNTG_SMTN", "WHOL_SHUN_VOL_RATE", "TOTAL_SHNU_TR_PBMN", "WHOL_SHUN_TR_PBMN_RATE", "WHOL_NTBY_QTY", "WHOL_SMTM_NTBY_QTY_RATE", "WHOL_NTBY_TR_PBMN", "WHOL_NTBY_TR_PBMN_RATE", "ARBT_ENTM_NTBY_QTY", "ARBT_ENTM_NTBY_TR_PBMN", "ARBT_ONSL_NTBY_QTY", "ARBT_ONSL_NTBY_TR_PBMN", "NABT_ENTM_NTBY_QTY", "NABT_ENTM_NTBY_TR_PBMN", "NABT_ONSL_NTBY_QTY", "NABT_ONSL_NTBY_TR_PBMN", "ACML_VOL", "ACML_TR_PBMN",)
