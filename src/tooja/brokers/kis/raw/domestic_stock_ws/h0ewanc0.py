"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0ewanc0Message(KisBaseModel):
    """WS 메시지 1건."""

    MKSC_SHRN_ISCD: str  # 유가증권단축종목코드
    STCK_CNTG_HOUR: str  # 주식체결시간
    STCK_PRPR: str  # 주식현재가
    PRDY_VRSS_SIGN: str  # 전일대비부호
    PRDY_VRSS: str  # 전일대비
    PRDY_CTRT: str  # 전일대비율
    WGHN_AVRG_STCK_PRC: str  # 가중평균주식가격
    STCK_OPRC: str  # 주식시가2
    STCK_HGPR: str  # 주식최고가
    STCK_LWPR: str  # 주식최저가
    ASKP1: str  # 매도호가1
    BIDP1: str  # 매수호가1
    CNTG_VOL: str  # 체결거래량
    ACML_VOL: str  # 누적거래량
    ACML_TR_PBMN: str  # 누적거래대금
    SELN_CNTG_CSNU: str  # 매도체결건수
    SHNU_CNTG_CSNU: str  # 매수체결건수
    NTBY_CNTG_CSNU: str  # 순매수체결건수
    CTTR: str  # 체결강도
    SELN_CNTG_SMTN: str  # 총매도수량
    SHNU_CNTG_SMTN: str  # 총매수수량
    CNTG_CLS_CODE: str  # 체결구분코드
    SHNU_RATE: str  # 매수2비율
    PRDY_VOL_VRSS_ACML_VOL_RATE: str  # 전일거래량대비등락율
    OPRC_HOUR: str  # 시가시간
    OPRC_VRSS_PRPR_SIGN: str  # 시가2대비현재가부호
    OPRC_VRSS_PRPR: str  # 시가2대비현재가
    HGPR_HOUR: str  # 최고가시간
    HGPR_VRSS_PRPR_SIGN: str  # 최고가대비현재가부호
    HGPR_VRSS_PRPR: str  # 최고가대비현재가
    LWPR_HOUR: str  # 최저가시간
    LWPR_VRSS_PRPR_SIGN: str  # 최저가대비현재가부호
    LWPR_VRSS_PRPR: str  # 최저가대비현재가
    BSOP_DATE: str  # 영업일자
    NEW_MKOP_CLS_CODE: str  # 신장운영구분코드
    TRHT_YN: str  # 거래정지여부
    ASKP_RSQN1: str  # 매도호가잔량1
    BIDP_RSQN1: str  # 매수호가잔량1
    TOTAL_ASKP_RSQN: str  # 총매도호가잔량
    TOTAL_BIDP_RSQN: str  # 총매수호가잔량
    TMVL_VAL: str  # 시간가치값
    PRIT: str  # 패리티
    PRMM_VAL: str  # 프리미엄값
    GEAR: str  # 기어링
    PRLS_QRYR_RATE: str  # 손익분기비율
    INVL_VAL: str  # 내재가치값
    PRMM_RATE: str  # 프리미엄비율
    CFP: str  # 자본지지점
    LVRG_VAL: str  # 레버리지값
    DELTA: str  # 델타
    GAMA: str  # 감마
    VEGA: str  # 베가
    THETA: str  # 세타
    RHO: str  # 로우
    HTS_INTS_VLTL: str  # HTS내재변동성
    HTS_THPR: str  # HTS이론가
    VOL_TNRT: str  # 거래량회전율
    LP_HVOL: str  # LP보유량
    LP_HLDN_RATE: str  # LP보유비율

class H0ewanc0Subscriber(WsSubscriber[H0ewanc0Message]):
    """ELW 실시간예상체결 [실시간-063]."""

    TR_ID = "H0EWANC0"
    RESPONSE_TYPE = H0ewanc0Message
    COLUMNS = ("MKSC_SHRN_ISCD", "STCK_CNTG_HOUR", "STCK_PRPR", "PRDY_VRSS_SIGN", "PRDY_VRSS", "PRDY_CTRT", "WGHN_AVRG_STCK_PRC", "STCK_OPRC", "STCK_HGPR", "STCK_LWPR", "ASKP1", "BIDP1", "CNTG_VOL", "ACML_VOL", "ACML_TR_PBMN", "SELN_CNTG_CSNU", "SHNU_CNTG_CSNU", "NTBY_CNTG_CSNU", "CTTR", "SELN_CNTG_SMTN", "SHNU_CNTG_SMTN", "CNTG_CLS_CODE", "SHNU_RATE", "PRDY_VOL_VRSS_ACML_VOL_RATE", "OPRC_HOUR", "OPRC_VRSS_PRPR_SIGN", "OPRC_VRSS_PRPR", "HGPR_HOUR", "HGPR_VRSS_PRPR_SIGN", "HGPR_VRSS_PRPR", "LWPR_HOUR", "LWPR_VRSS_PRPR_SIGN", "LWPR_VRSS_PRPR", "BSOP_DATE", "NEW_MKOP_CLS_CODE", "TRHT_YN", "ASKP_RSQN1", "BIDP_RSQN1", "TOTAL_ASKP_RSQN", "TOTAL_BIDP_RSQN", "TMVL_VAL", "PRIT", "PRMM_VAL", "GEAR", "PRLS_QRYR_RATE", "INVL_VAL", "PRMM_RATE", "CFP", "LVRG_VAL", "DELTA", "GAMA", "VEGA", "THETA", "RHO", "HTS_INTS_VLTL", "HTS_THPR", "VOL_TNRT", "LP_HVOL", "LP_HLDN_RATE",)
