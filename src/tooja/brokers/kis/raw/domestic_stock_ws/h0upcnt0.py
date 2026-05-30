"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0upcnt0Message(KisBaseModel):
    """WS 메시지 1건."""

    bsop_hour: str  # 영업 시간
    prpr_nmix: str  # 현재가 지수
    prdy_vrss_sign: str  # 전일 대비 부호
    bstp_nmix_prdy_vrss: str  # 업종 지수 전일 대비
    acml_vol: str  # 누적 거래량
    acml_tr_pbmn: str  # 누적 거래 대금
    pcas_vol: str  # 건별 거래량
    pcas_tr_pbmn: str  # 건별 거래 대금
    prdy_ctrt: str  # 전일 대비율
    oprc_nmix: str  # 시가 지수
    nmix_hgpr: str  # 지수 최고가
    nmix_lwpr: str  # 지수 최저가
    oprc_vrss_nmix_prpr: str  # 시가 대비 지수 현재가
    oprc_vrss_nmix_sign: str  # 시가 대비 지수 부호
    hgpr_vrss_nmix_prpr: str  # 최고가 대비 지수 현재가
    hgpr_vrss_nmix_sign: str  # 최고가 대비 지수 부호
    lwpr_vrss_nmix_prpr: str  # 최저가 대비 지수 현재가
    lwpr_vrss_nmix_sign: str  # 최저가 대비 지수 부호
    prdy_clpr_vrss_oprc_rate: str  # 전일 종가 대비 시가2 비율
    prdy_clpr_vrss_hgpr_rate: str  # 전일 종가 대비 최고가 비율
    prdy_clpr_vrss_lwpr_rate: str  # 전일 종가 대비 최저가 비율
    uplm_issu_cnt: str  # 상한 종목 수
    ascn_issu_cnt: str  # 상승 종목 수
    stnr_issu_cnt: str  # 보합 종목 수
    down_issu_cnt: str  # 하락 종목 수
    lslm_issu_cnt: str  # 하한 종목 수
    qtqt_ascn_issu_cnt: str  # 기세 상승 종목수
    qtqt_down_issu_cnt: str  # 기세 하락 종목수
    tick_vrss: str  # TICK대비

class H0upcnt0Subscriber(WsSubscriber[H0upcnt0Message]):
    """국내지수 실시간체결 [실시간-026]."""

    TR_ID = "H0UPCNT0"
    RESPONSE_TYPE = H0upcnt0Message
    COLUMNS = ("bsop_hour", "prpr_nmix", "prdy_vrss_sign", "bstp_nmix_prdy_vrss", "acml_vol", "acml_tr_pbmn", "pcas_vol", "pcas_tr_pbmn", "prdy_ctrt", "oprc_nmix", "nmix_hgpr", "nmix_lwpr", "oprc_vrss_nmix_prpr", "oprc_vrss_nmix_sign", "hgpr_vrss_nmix_prpr", "hgpr_vrss_nmix_sign", "lwpr_vrss_nmix_prpr", "lwpr_vrss_nmix_sign", "prdy_clpr_vrss_oprc_rate", "prdy_clpr_vrss_hgpr_rate", "prdy_clpr_vrss_lwpr_rate", "uplm_issu_cnt", "ascn_issu_cnt", "stnr_issu_cnt", "down_issu_cnt", "lslm_issu_cnt", "qtqt_ascn_issu_cnt", "qtqt_down_issu_cnt", "tick_vrss",)
