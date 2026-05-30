"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0upanc0Message(KisBaseModel):
    """WS 메시지 1건."""

    BSOP_HOUR: str  # 영업 시간
    PRPR_NMIX: str  # 현재가 지수
    PRDY_VRSS_SIGN: str  # 전일 대비 부호
    BSTP_NMIX_PRDY_VRSS: str  # 업종 지수 전일 대비
    ACML_VOL: str  # 누적 거래량
    ACML_TR_PBMN: str  # 누적 거래 대금
    PCAS_VOL: str  # 건별 거래량
    PCAS_TR_PBMN: str  # 건별 거래 대금
    PRDY_CTRT: str  # 전일 대비율
    OPRC_NMIX: str  # 시가 지수
    NMIX_HGPR: str  # 지수 최고가
    NMIX_LWPR: str  # 지수 최저가
    OPRC_VRSS_NMIX_PRPR: str  # 시가 대비 지수 현재가
    OPRC_VRSS_NMIX_SIGN: str  # 시가 대비 지수 부호
    HGPR_VRSS_NMIX_PRPR: str  # 최고가 대비 지수 현재가
    HGPR_VRSS_NMIX_SIGN: str  # 최고가 대비 지수 부호
    LWPR_VRSS_NMIX_PRPR: str  # 최저가 대비 지수 현재가
    LWPR_VRSS_NMIX_SIGN: str  # 최저가 대비 지수 부호
    PRDY_CLPR_VRSS_OPRC_RATE: str  # 전일 종가 대비 시가2 비율
    PRDY_CLPR_VRSS_HGPR_RATE: str  # 전일 종가 대비 최고가 비율
    PRDY_CLPR_VRSS_LWPR_RATE: str  # 전일 종가 대비 최저가 비율
    UPLM_ISSU_CNT: str  # 상한 종목 수
    ASCN_ISSU_CNT: str  # 상승 종목 수
    STNR_ISSU_CNT: str  # 보합 종목 수
    DOWN_ISSU_CNT: str  # 하락 종목 수
    LSLM_ISSU_CNT: str  # 하한 종목 수
    QTQT_ASCN_ISSU_CNT: str  # 기세 상승 종목수
    QTQT_DOWN_ISSU_CNT: str  # 기세 하락 종목수
    TICK_VRSS: str  # TICK대비

class H0upanc0Subscriber(WsSubscriber[H0upanc0Message]):
    """국내지수 실시간예상체결 [실시간-027]."""

    TR_ID = "H0UPANC0"
    RESPONSE_TYPE = H0upanc0Message
    COLUMNS = ("BSOP_HOUR", "PRPR_NMIX", "PRDY_VRSS_SIGN", "BSTP_NMIX_PRDY_VRSS", "ACML_VOL", "ACML_TR_PBMN", "PCAS_VOL", "PCAS_TR_PBMN", "PRDY_CTRT", "OPRC_NMIX", "NMIX_HGPR", "NMIX_LWPR", "OPRC_VRSS_NMIX_PRPR", "OPRC_VRSS_NMIX_SIGN", "HGPR_VRSS_NMIX_PRPR", "HGPR_VRSS_NMIX_SIGN", "LWPR_VRSS_NMIX_PRPR", "LWPR_VRSS_NMIX_SIGN", "PRDY_CLPR_VRSS_OPRC_RATE", "PRDY_CLPR_VRSS_HGPR_RATE", "PRDY_CLPR_VRSS_LWPR_RATE", "UPLM_ISSU_CNT", "ASCN_ISSU_CNT", "STNR_ISSU_CNT", "DOWN_ISSU_CNT", "LSLM_ISSU_CNT", "QTQT_ASCN_ISSU_CNT", "QTQT_DOWN_ISSU_CNT", "TICK_VRSS",)
