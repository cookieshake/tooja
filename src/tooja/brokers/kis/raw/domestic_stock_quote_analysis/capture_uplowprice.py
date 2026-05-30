"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class CaptureUplowpriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — 시장구분(J)
    FID_COND_SCR_DIV_CODE: str  # 조건화면분류코드 — 11300(Unique key)
    FID_PRC_CLS_CODE: str  # 상하한가 구분코드 — 0(상한가),1(하한가)
    FID_DIV_CLS_CODE: str  # 분류구분코드 — '0(상하한가종목),6(8%상하한가 근접), 5(10%상하한가 근접), 1(15%상하한가 근접),2(20%상하한가 근접), 3(25%상하한가 근접)'
    FID_INPUT_ISCD: str  # 입력종목코드 — 전체(0000), 코스피(0001),코스닥(1001)
    FID_TRGT_CLS_CODE: str  # 대상구분코드 — 공백 입력
    FID_TRGT_EXLS_CLS_CODE: str  # 대상제외구분코드 — 공백 입력
    FID_INPUT_PRICE_1: str  # 입력가격1 — 공백 입력
    FID_INPUT_PRICE_2: str  # 입력가격2 — 공백 입력
    FID_VOL_CNT: str  # 거래량수 — 공백 입력

class CaptureUplowpriceResponse_OutputItem(KisBaseModel):
    """nested item."""

    mksc_shrn_iscd: str | None = None  # 유가증권단축종목코드
    hts_kor_isnm: str | None = None  # HTS한글종목명
    stck_prpr: str | None = None  # 주식현재가
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_vrss: str | None = None  # 전일대비
    prdy_ctrt: str | None = None  # 전일대비율
    acml_vol: str | None = None  # 누적거래량
    total_askp_rsqn: str | None = None  # 총매도호가잔량
    total_bidp_rsqn: str | None = None  # 총매수호가잔량
    askp_rsqn1: str | None = None  # 매도호가잔량1
    bidp_rsqn1: str | None = None  # 매수호가잔량1
    prdy_vol: str | None = None  # 전일거래량
    seln_cnqn: str | None = None  # 매도체결량
    shnu_cnqn: str | None = None  # 매수2체결량
    stck_llam: str | None = None  # 주식하한가
    stck_mxpr: str | None = None  # 주식상한가
    prdy_vrss_vol_rate: str | None = None  # 전일대비거래량비율

class CaptureUplowpriceResponse(KisCommonResponse):
    """응답 본문."""

    output: list[CaptureUplowpriceResponse_OutputItem] = []  # 응답상세 — array

class CaptureUplowpriceExecutor(ApiExecutor[CaptureUplowpriceRequest, CaptureUplowpriceResponse]):
    """국내주식 상하한가 포착 [국내주식-190]."""

    # 국내주식 상하한가 포착 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0917] 실시간 상하한가 포착 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/capture-uplowprice"
    METHOD = "GET"
    RESPONSE_TYPE = CaptureUplowpriceResponse
    TR_ID = "FHKST130000C0"
