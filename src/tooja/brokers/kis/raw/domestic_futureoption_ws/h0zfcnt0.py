"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0zfcnt0Message(KisBaseModel):
    """WS 메시지 1건."""

    BSOP_HOUR: str  # 영업시간
    STCK_PRPR: str  # 주식현재가
    PRDY_VRSS_SIGN: str  # 전일대비부호
    PRDY_VRSS: str  # 전일대비
    FUTS_PRDY_CTRT: str  # 선물전일대비율
    STCK_OPRC: str  # 주식시가2
    STCK_HGPR: str  # 주식최고가
    STCK_LWPR: str  # 주식최저가
    LAST_CNQN: str  # 최종거래량
    ACML_VOL: str  # 누적거래량
    ACML_TR_PBMN: str  # 누적거래대금
    HTS_THPR: str  # HTS이론가
    MRKT_BASIS: str  # 시장베이시스
    DPRT: str  # 괴리율
    NMSC_FCTN_STPL_PRC: str  # 근월물약정가
    FMSC_FCTN_STPL_PRC: str  # 원월물약정가
    SPEAD_PRC: str  # 스프레드1
    HTS_OTST_STPL_QTY: str  # HTS미결제약정수량
    OTST_STPL_QTY_ICDC: str  # 미결제약정수량증감
    OPRC_HOUR: str  # 시가시간
    OPRC_VRSS_PRPR_SIGN: str  # 시가2대비현재가부호
    OPRC_VRSS_PRPR: str  # 시가2대비현재가
    HGPR_HOUR: str  # 최고가시간
    HGPR_VRSS_PRPR_SIGN: str  # 최고가대비현재가부호
    HGPR_VRSS_PRPR: str  # 최고가대비현재가
    LWPR_HOUR: str  # 최저가시간
    LWPR_VRSS_PRPR_SIGN: str  # 최저가대비현재가부호
    LWPR_VRSS_PRPR: str  # 최저가대비현재가
    SHNU_RATE: str  # 매수2비율
    CTTR: str  # 체결강도
    ESDG: str  # 괴리도
    OTST_STPL_RGBF_QTY_ICDC: str  # 미결제약정직전수량증감
    THPR_BASIS: str  # 이론베이시스
    ASKP1: str  # 매도호가1
    BIDP1: str  # 매수호가1
    ASKP_RSQN1: str  # 매도호가잔량1
    BIDP_RSQN1: str  # 매수호가잔량1
    SELN_CNTG_CSNU: str  # 매도체결건수
    SHNU_CNTG_CSNU: str  # 매수체결건수
    NTBY_CNTG_CSNU: str  # 순매수체결건수
    SELN_CNTG_SMTN: str  # 총매도수량
    SHNU_CNTG_SMTN: str  # 총매수수량
    TOTAL_ASKP_RSQN: str  # 총매도호가잔량
    TOTAL_BIDP_RSQN: str  # 총매수호가잔량
    PRDY_VOL_VRSS_ACML_VOL_RATE: str  # 전일거래량대비등락율
    DYNM_MXPR: str  # 실시간상한가
    DYNM_LLAM: str  # 실시간하한가
    DYNM_PRC_LIMT_YN: str  # 실시간가격제한구분

class H0zfcnt0Subscriber(WsSubscriber[H0zfcnt0Message]):
    """주식선물 실시간체결가 [실시간-029]."""

    TR_ID = "H0ZFCNT0"
    RESPONSE_TYPE = H0zfcnt0Message
    COLUMNS = ("BSOP_HOUR", "STCK_PRPR", "PRDY_VRSS_SIGN", "PRDY_VRSS", "FUTS_PRDY_CTRT", "STCK_OPRC", "STCK_HGPR", "STCK_LWPR", "LAST_CNQN", "ACML_VOL", "ACML_TR_PBMN", "HTS_THPR", "MRKT_BASIS", "DPRT", "NMSC_FCTN_STPL_PRC", "FMSC_FCTN_STPL_PRC", "SPEAD_PRC", "HTS_OTST_STPL_QTY", "OTST_STPL_QTY_ICDC", "OPRC_HOUR", "OPRC_VRSS_PRPR_SIGN", "OPRC_VRSS_PRPR", "HGPR_HOUR", "HGPR_VRSS_PRPR_SIGN", "HGPR_VRSS_PRPR", "LWPR_HOUR", "LWPR_VRSS_PRPR_SIGN", "LWPR_VRSS_PRPR", "SHNU_RATE", "CTTR", "ESDG", "OTST_STPL_RGBF_QTY_ICDC", "THPR_BASIS", "ASKP1", "BIDP1", "ASKP_RSQN1", "BIDP_RSQN1", "SELN_CNTG_CSNU", "SHNU_CNTG_CSNU", "NTBY_CNTG_CSNU", "SELN_CNTG_SMTN", "SHNU_CNTG_SMTN", "TOTAL_ASKP_RSQN", "TOTAL_BIDP_RSQN", "PRDY_VOL_VRSS_ACML_VOL_RATE", "DYNM_MXPR", "DYNM_LLAM", "DYNM_PRC_LIMT_YN",)
