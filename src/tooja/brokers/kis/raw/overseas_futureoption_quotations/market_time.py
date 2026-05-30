"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class MarketTimeRequest(KisBaseModel):
    """요청."""

    FM_PDGR_CD: str  # FM상품군코드 — 공백
    FM_CLAS_CD: str  # FM클래스코드 — '공백(전체), 001(통화), 002(금리), 003(지수), 004(농산물),005(축산물),006(금속),007(에너지)'
    FM_EXCG_CD: str  # FM거래소코드 — 'CME(CME), EUREX(EUREX), HKEx(HKEx), ICE(ICE), SGX(SGX), OSE(OSE), ASX(ASX), CBOE(CBOE), MDEX(MDEX), NYSE(NYSE), BMF(BMF),FTX(FTX)
    OPT_YN: str  # 옵션여부 — %(전체), N(선물), Y(옵션)
    CTX_AREA_NK200: str  # 연속조회키200
    CTX_AREA_FK200: str  # 연속조회검색조건200

class MarketTimeResponse_OutputItem(KisBaseModel):
    """nested item."""

    fm_pdgr_cd: str | None = None  # FM상품군코드
    fm_pdgr_name: str | None = None  # FM상품군명
    fm_excg_cd: str | None = None  # FM거래소코드
    fm_excg_name: str | None = None  # FM거래소명
    fuop_dvsn_name: str | None = None  # 선물옵션구분명
    fm_clas_cd: str | None = None  # FM클래스코드
    fm_clas_name: str | None = None  # FM클래스명
    am_mkmn_strt_tmd: str | None = None  # 오전장운영시작시각
    am_mkmn_end_tmd: str | None = None  # 오전장운영종료시각
    pm_mkmn_strt_tmd: str | None = None  # 오후장운영시작시각
    pm_mkmn_end_tmd: str | None = None  # 오후장운영종료시각
    mkmn_nxdy_strt_tmd: str | None = None  # 장운영익일시작시각
    mkmn_nxdy_end_tmd: str | None = None  # 장운영익일종료시각
    base_mket_strt_tmd: str | None = None  # 기본시장시작시각
    base_mket_end_tmd: str | None = None  # 기본시장종료시각

class MarketTimeResponse(KisCommonResponse):
    """응답 본문."""

    output: list[MarketTimeResponse_OutputItem] = []  # 응답상세

class MarketTimeExecutor(ApiExecutor[MarketTimeRequest, MarketTimeResponse]):
    """해외선물옵션 장운영시간 [해외선물-030]."""

    # 해외선물 장운영시간 API입니다. 한국투자 HTS(eFriend Plus) &gt; [6773] 해외선물 장운영시간 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/overseas-futureoption/v1/quotations/market-time"
    METHOD = "GET"
    RESPONSE_TYPE = MarketTimeResponse
    TR_ID = "OTFM2229R"
