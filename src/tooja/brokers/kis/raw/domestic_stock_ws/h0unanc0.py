"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0unanc0Message(KisBaseModel):
    """WS 메시지 1건."""

    MKSC_SHRN_ISCD: str  # 유가증권단축종목코드
    STCK_CNTG_HOUR: str  # 주식체결시간
    STCK_PRPR: str  # 주식현재가
    PRDY_VRSS_SIGN: str  # 전일대비구분
    PRDY_VRSS: str  # 전일대비
    PRDY_CTRT: str  # 등락율
    WGHN_AVRG_STCK_PRC: str  # 가중평균주식가격
    STCK_OPRC: str  # 시가
    STCK_HGPR: str  # 고가
    STCK_LWPR: str  # 저가
    ASKP1: str  # 매도호가
    BIDP1: str  # 매수호가
    CNTG_VOL: str  # 거래량
    ACML_VOL: str  # 누적거래량
    ACML_TR_PBMN: str  # 누적거래대금
    SELN_CNTG_CSNU: str  # 매도체결건수
    SHNU_CNTG_CSNU: str  # 매수체결건수
    NTBY_CNTG_CSNU: str  # 순매수체결건수
    CTTR: str  # 체결강도
    SELN_CNTG_SMTN: str  # 총매도수량
    SHNU_CNTG_SMTN: str  # 총매수수량
    CNTG_CLS_CODE: str  # 체결구분
    SHNU_RATE: str  # 매수비율
    PRDY_VOL_VRSS_ACML_VOL_RATE: str  # 전일거래량대비등락율
    OPRC_HOUR: str  # 시가시간
    OPRC_VRSS_PRPR_SIGN: str  # 시가대비구분
    OPRC_VRSS_PRPR: str  # 시가대비
    HGPR_HOUR: str  # 최고가시간
    HGPR_VRSS_PRPR_SIGN: str  # 고가대비구분
    HGPR_VRSS_PRPR: str  # 고가대비
    LWPR_HOUR: str  # 최저가시간
    LWPR_VRSS_PRPR_SIGN: str  # 저가대비구분
    LWPR_VRSS_PRPR: str  # 저가대비
    BSOP_DATE: str  # 영업일자
    NEW_MKOP_CLS_CODE: str  # 신장운영구분코드
    TRHT_YN: str  # 거래정지여부
    ASKP_RSQN1: str  # 매도호가잔량1
    BIDP_RSQN1: str  # 매수호가잔량1
    TOTAL_ASKP_RSQN: str  # 총매도호가잔량
    TOTAL_BIDP_RSQN: str  # 총매수호가잔량
    VOL_TNRT: str  # 거래량회전율
    PRDY_SMNS_HOUR_ACML_VOL: str  # 전일동시간누적거래량
    PRDY_SMNS_HOUR_ACML_VOL_RATE: str  # 전일동시간누적거래량비율
    HOUR_CLS_CODE: str  # 시간구분코드
    MRKT_TRTM_CLS_CODE: str  # 임의종료구분코드
    VI_STND_PRC: str  # VI 상태값

class H0unanc0Subscriber(WsSubscriber[H0unanc0Message]):
    """국내주식 실시간예상체결 (통합)."""

    TR_ID = "H0UNANC0"
    RESPONSE_TYPE = H0unanc0Message
    COLUMNS = ("MKSC_SHRN_ISCD", "STCK_CNTG_HOUR", "STCK_PRPR", "PRDY_VRSS_SIGN", "PRDY_VRSS", "PRDY_CTRT", "WGHN_AVRG_STCK_PRC", "STCK_OPRC", "STCK_HGPR", "STCK_LWPR", "ASKP1", "BIDP1", "CNTG_VOL", "ACML_VOL", "ACML_TR_PBMN", "SELN_CNTG_CSNU", "SHNU_CNTG_CSNU", "NTBY_CNTG_CSNU", "CTTR", "SELN_CNTG_SMTN", "SHNU_CNTG_SMTN", "CNTG_CLS_CODE", "SHNU_RATE", "PRDY_VOL_VRSS_ACML_VOL_RATE", "OPRC_HOUR", "OPRC_VRSS_PRPR_SIGN", "OPRC_VRSS_PRPR", "HGPR_HOUR", "HGPR_VRSS_PRPR_SIGN", "HGPR_VRSS_PRPR", "LWPR_HOUR", "LWPR_VRSS_PRPR_SIGN", "LWPR_VRSS_PRPR", "BSOP_DATE", "NEW_MKOP_CLS_CODE", "TRHT_YN", "ASKP_RSQN1", "BIDP_RSQN1", "TOTAL_ASKP_RSQN", "TOTAL_BIDP_RSQN", "VOL_TNRT", "PRDY_SMNS_HOUR_ACML_VOL", "PRDY_SMNS_HOUR_ACML_VOL_RATE", "HOUR_CLS_CODE", "MRKT_TRTM_CLS_CODE", "VI_STND_PRC",)
