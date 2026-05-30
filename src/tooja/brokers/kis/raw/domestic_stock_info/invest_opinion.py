"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InvestOpinionRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — J(시장 구분 코드)
    FID_COND_SCR_DIV_CODE: str  # 조건화면분류코드 — 16633(Primary key)
    FID_INPUT_ISCD: str  # 입력종목코드 — 종목코드(ex) 005930(삼성전자))
    FID_INPUT_DATE_1: str  # 입력날짜1 — 이후 ~(ex) 0020231113)
    FID_INPUT_DATE_2: str  # 입력날짜2 — ~ 이전(ex) 0020240513)

class InvestOpinionResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식영업일자
    invt_opnn: str | None = None  # 투자의견
    invt_opnn_cls_code: str | None = None  # 투자의견구분코드
    rgbf_invt_opnn: str | None = None  # 직전투자의견
    rgbf_invt_opnn_cls_code: str | None = None  # 직전투자의견구분코드
    mbcr_name: str | None = None  # 회원사명
    hts_goal_prc: str | None = None  # HTS목표가격
    stck_prdy_clpr: str | None = None  # 주식전일종가
    stck_nday_esdg: str | None = None  # 주식N일괴리도
    nday_dprt: str | None = None  # N일괴리율
    stft_esdg: str | None = None  # 주식선물괴리도
    dprt: str | None = None  # 괴리율

class InvestOpinionResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InvestOpinionResponse_OutputItem] = []  # 응답상세 — array

class InvestOpinionExecutor(ApiExecutor[InvestOpinionRequest, InvestOpinionResponse]):
    """국내주식 종목투자의견 [국내주식-188]."""

    # 국내주식 종목투자의견 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0605] 종목투자의견 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 한 번의 호출에 100건까지 조회가 가능하기에, 일자 파라미터(FID_INPUT_DATE_1, FID_INPUT_DATE_2)를 조절하여 다음 데이터 조회하시기 바랍니다.

    PATH = "/uapi/domestic-stock/v1/quotations/invest-opinion"
    METHOD = "GET"
    RESPONSE_TYPE = InvestOpinionResponse
    TR_ID = "FHKST663300C0"
