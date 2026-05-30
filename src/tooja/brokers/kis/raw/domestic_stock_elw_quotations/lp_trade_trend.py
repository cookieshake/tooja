"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class LpTradeTrendRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — 시장구분(W)
    FID_INPUT_ISCD: str  # 입력종목코드 — 입력종목코드(ex 52K577(미래 K577KOSDAQ150콜)

class LpTradeTrendResponse_Output1Item(KisBaseModel):
    """nested item."""

    elw_prpr: str | None = None  # ELW현재가
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_vrss: str | None = None  # 전일대비
    prdy_ctrt: str | None = None  # 전일대비율
    acml_vol: str | None = None  # 누적거래량
    prdy_vol: str | None = None  # 전일거래량
    stck_cnvr_rate: str | None = None  # 주식전환비율
    prit: str | None = None  # 패리티
    lvrg_val: str | None = None  # 레버리지값
    gear: str | None = None  # 기어링
    prls_qryr_rate: str | None = None  # 손익분기비율
    cfp: str | None = None  # 자본지지점
    invl_val: str | None = None  # 내재가치값
    tmvl_val: str | None = None  # 시간가치값
    acpr: str | None = None  # 행사가
    elw_ko_barrier: str | None = None  # 조기종료발생기준가격

class LpTradeTrendResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식영업일자
    elw_prpr: str | None = None  # ELW현재가
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_vrss: str | None = None  # 전일대비
    prdy_ctrt: str | None = None  # 전일대비율
    lp_seln_qty: str | None = None  # LP매도수량
    lp_seln_avrg_unpr: str | None = None  # LP매도평균단가
    lp_shnu_qty: str | None = None  # LP매수수량
    lp_shnu_avrg_unpr: str | None = None  # LP매수평균단가
    lp_hvol: str | None = None  # LP보유량
    lp_hldn_rate: str | None = None  # LP보유비율
    prsn_deal_qty: str | None = None  # 개인매매수량
    apprch_rate: str | None = None  # 접근도

class LpTradeTrendResponse(KisCommonResponse):
    """응답 본문."""

    output1: LpTradeTrendResponse_Output1Item | None = None  # 응답상세
    output2: list[LpTradeTrendResponse_Output2Item] = []  # 응답상세 — array

class LpTradeTrendExecutor(ApiExecutor[LpTradeTrendRequest, LpTradeTrendResponse]):
    """ELW LP매매추이 [국내주식-182]."""

    # ELW LP매매추이 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0376] ELW LP매매추이 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/elw/v1/quotations/lp-trade-trend"
    METHOD = "GET"
    RESPONSE_TYPE = LpTradeTrendResponse
    TR_ID = "FHPEW03760000"
