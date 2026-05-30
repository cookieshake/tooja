"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0stmbc0Message(KisBaseModel):
    """WS 메시지 1건."""

    SELN2_MBCR_NAME1: str  # 매도2회원사명1
    SELN2_MBCR_NAME2: str  # 매도2회원사명2
    SELN2_MBCR_NAME3: str  # 매도2회원사명3
    SELN2_MBCR_NAME4: str  # 매도2회원사명4
    SELN2_MBCR_NAME5: str  # 매도2회원사명5
    BYOV_MBCR_NAME1: str  # 매수회원사명1
    BYOV_MBCR_NAME2: str  # 매수회원사명2
    BYOV_MBCR_NAME3: str  # 매수회원사명3
    BYOV_MBCR_NAME4: str  # 매수회원사명4
    BYOV_MBCR_NAME5: str  # 매수회원사명5
    TOTAL_SELN_QTY1: str  # 총매도수량1
    TOTAL_SELN_QTY2: str  # 총매도수량2
    TOTAL_SELN_QTY3: str  # 총매도수량3
    TOTAL_SELN_QTY4: str  # 총매도수량4
    TOTAL_SELN_QTY5: str  # 총매도수량5
    TOTAL_SHNU_QTY1: str  # 총매수2수량1
    TOTAL_SHNU_QTY2: str  # 총매수2수량2
    TOTAL_SHNU_QTY3: str  # 총매수2수량3
    TOTAL_SHNU_QTY4: str  # 총매수2수량4
    TOTAL_SHNU_QTY5: str  # 총매수2수량5
    SELN_MBCR_GLOB_YN_1: str  # 매도거래원구분1
    SELN_MBCR_GLOB_YN_2: str  # 매도거래원구분2
    SELN_MBCR_GLOB_YN_3: str  # 매도거래원구분3
    SELN_MBCR_GLOB_YN_4: str  # 매도거래원구분4
    SELN_MBCR_GLOB_YN_5: str  # 매도거래원구분5
    SHNU_MBCR_GLOB_YN_1: str  # 매수거래원구분1
    SHNU_MBCR_GLOB_YN_2: str  # 매수거래원구분2
    SHNU_MBCR_GLOB_YN_3: str  # 매수거래원구분3
    SHNU_MBCR_GLOB_YN_4: str  # 매수거래원구분4
    SHNU_MBCR_GLOB_YN_5: str  # 매수거래원구분5
    SELN_MBCR_NO1: str  # 매도거래원코드1
    SELN_MBCR_NO2: str  # 매도거래원코드2
    SELN_MBCR_NO3: str  # 매도거래원코드3
    SELN_MBCR_NO4: str  # 매도거래원코드4
    SELN_MBCR_NO5: str  # 매도거래원코드5
    SHNU_MBCR_NO1: str  # 매수거래원코드1
    SHNU_MBCR_NO2: str  # 매수거래원코드2
    SHNU_MBCR_NO3: str  # 매수거래원코드3
    SHNU_MBCR_NO4: str  # 매수거래원코드4
    SHNU_MBCR_NO5: str  # 매수거래원코드5
    SELN_MBCR_RLIM1: str  # 매도회원사비중1
    SELN_MBCR_RLIM2: str  # 매도회원사비중2
    SELN_MBCR_RLIM3: str  # 매도회원사비중3
    SELN_MBCR_RLIM4: str  # 매도회원사비중4
    SELN_MBCR_RLIM5: str  # 매도회원사비중5
    SHNU_MBCR_RLIM1: str  # 매수2회원사비중1
    SHNU_MBCR_RLIM2: str  # 매수2회원사비중2
    SHNU_MBCR_RLIM3: str  # 매수2회원사비중3
    SHNU_MBCR_RLIM4: str  # 매수2회원사비중4
    SHNU_MBCR_RLIM5: str  # 매수2회원사비중5
    SELN_QTY_ICDC1: str  # 매도수량증감1
    SELN_QTY_ICDC2: str  # 매도수량증감2
    SELN_QTY_ICDC3: str  # 매도수량증감3
    SELN_QTY_ICDC4: str  # 매도수량증감4
    SELN_QTY_ICDC5: str  # 매도수량증감5
    SHNU_QTY_ICDC1: str  # 매수2수량증감1
    SHNU_QTY_ICDC2: str  # 매수2수량증감2
    SHNU_QTY_ICDC3: str  # 매수2수량증감3
    SHNU_QTY_ICDC4: str  # 매수2수량증감4
    SHNU_QTY_ICDC5: str  # 매수2수량증감5
    GLOB_TOTAL_SELN_QTY: str  # 외국계총매도수량
    GLOB_TOTAL_SHNU_QTY: str  # 외국계총매수2수량
    GLOB_TOTAL_SELN_QTY_ICDC: str  # 외국계총매도수량증감
    GLOB_TOTAL_SHNU_QTY_ICDC: str  # 외국계총매수2수량증감
    GLOB_NTBY_QTY: str  # 외국계순매수수량
    GLOB_SELN_RLIM: str  # 외국계매도비중
    GLOB_SHNU_RLIM: str  # 외국계매수2비중
    SELN2_MBCR_ENG_NAME1: str  # 매도2영문회원사명1
    SELN2_MBCR_ENG_NAME2: str  # 매도2영문회원사명2
    SELN2_MBCR_ENG_NAME3: str  # 매도2영문회원사명3
    SELN2_MBCR_ENG_NAME4: str  # 매도2영문회원사명4
    SELN2_MBCR_ENG_NAME5: str  # 매도2영문회원사명5
    BYOV_MBCR_ENG_NAME1: str  # 매수영문회원사명1
    BYOV_MBCR_ENG_NAME2: str  # 매수영문회원사명2
    BYOV_MBCR_ENG_NAME3: str  # 매수영문회원사명3
    BYOV_MBCR_ENG_NAME4: str  # 매수영문회원사명4
    BYOV_MBCR_ENG_NAME5: str  # 매수영문회원사명5

class H0stmbc0Subscriber(WsSubscriber[H0stmbc0Message]):
    """국내주식 실시간회원사 (KRX) [실시간-047]."""

    TR_ID = "H0STMBC0"
    RESPONSE_TYPE = H0stmbc0Message
    COLUMNS = ("SELN2_MBCR_NAME1", "SELN2_MBCR_NAME2", "SELN2_MBCR_NAME3", "SELN2_MBCR_NAME4", "SELN2_MBCR_NAME5", "BYOV_MBCR_NAME1", "BYOV_MBCR_NAME2", "BYOV_MBCR_NAME3", "BYOV_MBCR_NAME4", "BYOV_MBCR_NAME5", "TOTAL_SELN_QTY1", "TOTAL_SELN_QTY2", "TOTAL_SELN_QTY3", "TOTAL_SELN_QTY4", "TOTAL_SELN_QTY5", "TOTAL_SHNU_QTY1", "TOTAL_SHNU_QTY2", "TOTAL_SHNU_QTY3", "TOTAL_SHNU_QTY4", "TOTAL_SHNU_QTY5", "SELN_MBCR_GLOB_YN_1", "SELN_MBCR_GLOB_YN_2", "SELN_MBCR_GLOB_YN_3", "SELN_MBCR_GLOB_YN_4", "SELN_MBCR_GLOB_YN_5", "SHNU_MBCR_GLOB_YN_1", "SHNU_MBCR_GLOB_YN_2", "SHNU_MBCR_GLOB_YN_3", "SHNU_MBCR_GLOB_YN_4", "SHNU_MBCR_GLOB_YN_5", "SELN_MBCR_NO1", "SELN_MBCR_NO2", "SELN_MBCR_NO3", "SELN_MBCR_NO4", "SELN_MBCR_NO5", "SHNU_MBCR_NO1", "SHNU_MBCR_NO2", "SHNU_MBCR_NO3", "SHNU_MBCR_NO4", "SHNU_MBCR_NO5", "SELN_MBCR_RLIM1", "SELN_MBCR_RLIM2", "SELN_MBCR_RLIM3", "SELN_MBCR_RLIM4", "SELN_MBCR_RLIM5", "SHNU_MBCR_RLIM1", "SHNU_MBCR_RLIM2", "SHNU_MBCR_RLIM3", "SHNU_MBCR_RLIM4", "SHNU_MBCR_RLIM5", "SELN_QTY_ICDC1", "SELN_QTY_ICDC2", "SELN_QTY_ICDC3", "SELN_QTY_ICDC4", "SELN_QTY_ICDC5", "SHNU_QTY_ICDC1", "SHNU_QTY_ICDC2", "SHNU_QTY_ICDC3", "SHNU_QTY_ICDC4", "SHNU_QTY_ICDC5", "GLOB_TOTAL_SELN_QTY", "GLOB_TOTAL_SHNU_QTY", "GLOB_TOTAL_SELN_QTY_ICDC", "GLOB_TOTAL_SHNU_QTY_ICDC", "GLOB_NTBY_QTY", "GLOB_SELN_RLIM", "GLOB_SHNU_RLIM", "SELN2_MBCR_ENG_NAME1", "SELN2_MBCR_ENG_NAME2", "SELN2_MBCR_ENG_NAME3", "SELN2_MBCR_ENG_NAME4", "SELN2_MBCR_ENG_NAME5", "BYOV_MBCR_ENG_NAME1", "BYOV_MBCR_ENG_NAME2", "BYOV_MBCR_ENG_NAME3", "BYOV_MBCR_ENG_NAME4", "BYOV_MBCR_ENG_NAME5",)
