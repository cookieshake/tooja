"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0iocnt0Message(KisBaseModel):
    """WS 메시지 1건."""

    BSOP_HOUR: str  # 영업 시간
    OPTN_PRPR: str  # 옵션 현재가
    PRDY_VRSS_SIGN: str  # 전일 대비 부호
    OPTN_PRDY_VRSS: str  # 옵션 전일 대비
    PRDY_CTRT: str  # 전일 대비율
    OPTN_OPRC: str  # 옵션 시가2
    OPTN_HGPR: str  # 옵션 최고가
    OPTN_LWPR: str  # 옵션 최저가
    LAST_CNQN: str  # 최종 거래량
    ACML_VOL: str  # 누적 거래량
    ACML_TR_PBMN: str  # 누적 거래 대금
    HTS_THPR: str  # HTS 이론가
    HTS_OTST_STPL_QTY: str  # HTS 미결제 약정 수량
    OTST_STPL_QTY_ICDC: str  # 미결제 약정 수량 증감
    OPRC_HOUR: str  # 시가 시간
    OPRC_VRSS_PRPR_SIGN: str  # 시가2 대비 현재가 부호
    OPRC_VRSS_NMIX_PRPR: str  # 시가 대비 지수 현재가
    HGPR_HOUR: str  # 최고가 시간
    HGPR_VRSS_PRPR_SIGN: str  # 최고가 대비 현재가 부호
    HGPR_VRSS_NMIX_PRPR: str  # 최고가 대비 지수 현재가
    LWPR_HOUR: str  # 최저가 시간
    LWPR_VRSS_PRPR_SIGN: str  # 최저가 대비 현재가 부호
    LWPR_VRSS_NMIX_PRPR: str  # 최저가 대비 지수 현재가
    SHNU_RATE: str  # 매수2 비율
    PRMM_VAL: str  # 프리미엄 값
    INVL_VAL: str  # 내재가치 값
    TMVL_VAL: str  # 시간가치 값
    DELTA: str  # 델타
    GAMA: str  # 감마
    VEGA: str  # 베가
    THETA: str  # 세타
    RHO: str  # 로우
    HTS_INTS_VLTL: str  # HTS 내재 변동성
    ESDG: str  # 괴리도
    OTST_STPL_RGBF_QTY_ICDC: str  # 미결제 약정 직전 수량 증감
    THPR_BASIS: str  # 이론 베이시스
    UNAS_HIST_VLTL: str  # 역사적변동성
    CTTR: str  # 체결강도
    DPRT: str  # 괴리율
    MRKT_BASIS: str  # 시장 베이시스
    OPTN_ASKP1: str  # 옵션 매도호가1
    OPTN_BIDP1: str  # 옵션 매수호가1
    ASKP_RSQN1: str  # 매도호가 잔량1
    BIDP_RSQN1: str  # 매수호가 잔량1
    SELN_CNTG_CSNU: str  # 매도 체결 건수
    SHNU_CNTG_CSNU: str  # 매수 체결 건수
    NTBY_CNTG_CSNU: str  # 순매수 체결 건수
    SELN_CNTG_SMTN: str  # 총 매도 수량
    SHNU_CNTG_SMTN: str  # 총 매수 수량
    TOTAL_ASKP_RSQN: str  # 총 매도호가 잔량
    TOTAL_BIDP_RSQN: str  # 총 매수호가 잔량
    PRDY_VOL_VRSS_ACML_VOL_RATE: str  # 전일 거래량 대비 등락율
    AVRG_VLTL: str  # 평균 변동성
    DSCS_LRQN_VOL: str  # 협의대량누적 거래량
    DYNM_MXPR: str  # 실시간상한가
    DYNM_LLAM: str  # 실시간하한가
    DYNM_PRC_LIMT_YN: str  # 실시간가격제한구분

class H0iocnt0Subscriber(WsSubscriber[H0iocnt0Message]):
    """지수옵션  실시간체결가[실시간-014]."""

    TR_ID = "H0IOCNT0"
    RESPONSE_TYPE = H0iocnt0Message
    COLUMNS = ("BSOP_HOUR", "OPTN_PRPR", "PRDY_VRSS_SIGN", "OPTN_PRDY_VRSS", "PRDY_CTRT", "OPTN_OPRC", "OPTN_HGPR", "OPTN_LWPR", "LAST_CNQN", "ACML_VOL", "ACML_TR_PBMN", "HTS_THPR", "HTS_OTST_STPL_QTY", "OTST_STPL_QTY_ICDC", "OPRC_HOUR", "OPRC_VRSS_PRPR_SIGN", "OPRC_VRSS_NMIX_PRPR", "HGPR_HOUR", "HGPR_VRSS_PRPR_SIGN", "HGPR_VRSS_NMIX_PRPR", "LWPR_HOUR", "LWPR_VRSS_PRPR_SIGN", "LWPR_VRSS_NMIX_PRPR", "SHNU_RATE", "PRMM_VAL", "INVL_VAL", "TMVL_VAL", "DELTA", "GAMA", "VEGA", "THETA", "RHO", "HTS_INTS_VLTL", "ESDG", "OTST_STPL_RGBF_QTY_ICDC", "THPR_BASIS", "UNAS_HIST_VLTL", "CTTR", "DPRT", "MRKT_BASIS", "OPTN_ASKP1", "OPTN_BIDP1", "ASKP_RSQN1", "BIDP_RSQN1", "SELN_CNTG_CSNU", "SHNU_CNTG_CSNU", "NTBY_CNTG_CSNU", "SELN_CNTG_SMTN", "SHNU_CNTG_SMTN", "TOTAL_ASKP_RSQN", "TOTAL_BIDP_RSQN", "PRDY_VOL_VRSS_ACML_VOL_RATE", "AVRG_VLTL", "DSCS_LRQN_VOL", "DYNM_MXPR", "DYNM_LLAM", "DYNM_PRC_LIMT_YN",)
