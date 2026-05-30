"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InvestOpbysecRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — J(시장 구분 코드)
    FID_COND_SCR_DIV_CODE: str  # 조건화면분류코드 — 16634(Primary key)
    FID_INPUT_ISCD: str  # 입력종목코드 — 회원사코드 (kis developers 포탈 사이트 포럼-> FAQ -> 종목정보 다운로드(국내) 참조)
    FID_DIV_CLS_CODE: str  # 분류구분코드 — 전체(0) 매수(1) 중립(2) 매도(3)
    FID_INPUT_DATE_1: str  # 입력날짜1 — 이후 ~
    FID_INPUT_DATE_2: str  # 입력날짜2 — ~ 이전

class InvestOpbysecResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식영업일자
    stck_shrn_iscd: str | None = None  # 주식단축종목코드
    hts_kor_isnm: str | None = None  # HTS한글종목명
    invt_opnn: str | None = None  # 투자의견
    invt_opnn_cls_code: str | None = None  # 투자의견구분코드
    rgbf_invt_opnn: str | None = None  # 직전투자의견
    rgbf_invt_opnn_cls_code: str | None = None  # 직전투자의견구분코드
    mbcr_name: str | None = None  # 회원사명
    stck_prpr: str | None = None  # 주식현재가
    prdy_vrss: str | None = None  # 전일대비
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_ctrt: str | None = None  # 전일대비율
    hts_goal_prc: str | None = None  # HTS목표가격
    stck_prdy_clpr: str | None = None  # 주식전일종가
    stft_esdg: str | None = None  # 주식선물괴리도
    dprt: str | None = None  # 괴리율

class InvestOpbysecResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InvestOpbysecResponse_OutputItem] = []  # 응답상세 — array

class InvestOpbysecExecutor(ApiExecutor[InvestOpbysecRequest, InvestOpbysecResponse]):
    """국내주식 증권사별 투자의견 [국내주식-189]."""

    # 국내주식 증권사별 투자의견 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0608] 증권사별 투자의견 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 한 번의 호출에 20건까지 조회가 가능하기에, 일자 파라미터(FID_INPUT_DATE_1, FID_INPUT_DATE_2)를 조절하여 다음 데이터 조회하시기 바랍니다.

    PATH = "/uapi/domestic-stock/v1/quotations/invest-opbysec"
    METHOD = "GET"
    RESPONSE_TYPE = InvestOpbysecResponse
    TR_ID = "FHKST663400C0"
