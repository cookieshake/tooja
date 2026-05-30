"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class TradprtByamtRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — J: KRX, NX: NXT, UN: 통합
    FID_COND_SCR_DIV_CODE: str  # 조건화면분류코드 — Uniquekey(11119)
    FID_INPUT_ISCD: str  # 입력종목코드 — 종목코드(ex)(005930 (삼성전자))

class TradprtByamtResponse_OutputItem(KisBaseModel):
    """nested item."""

    prpr_name: str | None = None  # 가격명
    smtn_avrg_prpr: str | None = None  # 합계 평균가격
    acml_vol: str | None = None  # 합계 거래량
    whol_ntby_qty_rate: str | None = None  # 합계 순매수비율
    ntby_cntg_csnu: str | None = None  # 합계 순매수건수
    seln_cnqn_smtn: str | None = None  # 매도 거래량
    whol_seln_vol_rate: str | None = None  # 매도 거래량비율
    seln_cntg_csnu: str | None = None  # 매도 건수
    shnu_cnqn_smtn: str | None = None  # 매수 거래량
    whol_shun_vol_rate: str | None = None  # 매수 거래량비율
    shnu_cntg_csnu: str | None = None  # 매수 건수

class TradprtByamtResponse(KisCommonResponse):
    """응답 본문."""

    output: list[TradprtByamtResponse_OutputItem] = []  # 응답상세 — array

class TradprtByamtExecutor(ApiExecutor[TradprtByamtRequest, TradprtByamtResponse]):
    """국내주식 체결금액별 매매비중 [국내주식-192]."""

    # 국내주식 체결금액별 매매비중 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0135] 체결금액별 매매비중 화면의 "상단 표" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/tradprt-byamt"
    METHOD = "GET"
    RESPONSE_TYPE = TradprtByamtResponse
    TR_ID = "FHKST111900C0"
