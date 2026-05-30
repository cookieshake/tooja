"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0bicnt0Message(KisBaseModel):
    """WS 메시지 1건."""

    NMIX_ID: str  # 지수ID
    STND_DATE1: str  # 기준일자1
    TRNM_HOUR: str  # 전송시간
    TOTL_ERNN_NMIX_OPRC: str  # 총수익지수시가지수
    TOTL_ERNN_NMIX_HGPR: str  # 총수익지수최고가
    TOTL_ERNN_NMIX_LWPR: str  # 총수익지수최저가
    TOTL_ERNN_NMIX: str  # 총수익지수
    PRDY_TOTL_ERNN_NMIX: str  # 전일총수익지수
    TOTL_ERNN_NMIX_PRDY_VRSS: str  # 총수익지수전일대비
    TOTL_ERNN_NMIX_PRDY_VRSS_SIGN: str  # 총수익지수전일대비부호
    TOTL_ERNN_NMIX_PRDY_CTRT: str  # 총수익지수전일대비율
    CLEN_PRC_NMIX: str  # 순가격지수
    MRKT_PRC_NMIX: str  # 시장가격지수
    BOND_CALL_RNVS_NMIX: str  # Call재투자지수
    BOND_ZERO_RNVS_NMIX: str  # Zero재투자지수
    BOND_FUTS_THPR: str  # 선물이론가격
    BOND_AVRG_DRTN_VAL: str  # 평균듀레이션
    BOND_AVRG_CNVX_VAL: str  # 평균컨벡서티
    BOND_AVRG_YTM_VAL: str  # 평균YTM
    BOND_AVRG_FRDL_YTM_VAL: str  # 평균선도YTM

class H0bicnt0Subscriber(WsSubscriber[H0bicnt0Message]):
    """채권지수 실시간체결가 [실시간-060]."""

    TR_ID = "H0BICNT0"
    RESPONSE_TYPE = H0bicnt0Message
    COLUMNS = ("NMIX_ID", "STND_DATE1", "TRNM_HOUR", "TOTL_ERNN_NMIX_OPRC", "TOTL_ERNN_NMIX_HGPR", "TOTL_ERNN_NMIX_LWPR", "TOTL_ERNN_NMIX", "PRDY_TOTL_ERNN_NMIX", "TOTL_ERNN_NMIX_PRDY_VRSS", "TOTL_ERNN_NMIX_PRDY_VRSS_SIGN", "TOTL_ERNN_NMIX_PRDY_CTRT", "CLEN_PRC_NMIX", "MRKT_PRC_NMIX", "BOND_CALL_RNVS_NMIX", "BOND_ZERO_RNVS_NMIX", "BOND_FUTS_THPR", "BOND_AVRG_DRTN_VAL", "BOND_AVRG_CNVX_VAL", "BOND_AVRG_YTM_VAL", "BOND_AVRG_FRDL_YTM_VAL",)
