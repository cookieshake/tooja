"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireMemberDailyRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — J: KRX, NX: NXT, UN: 통합
    FID_INPUT_ISCD: str  # 입력종목코드 — 주식종목코드입력
    FID_INPUT_ISCD_2: str  # 회원사코드 — 회원사코드 (kis developers 포탈 사이트 포럼-> FAQ -> 종목정보 다운로드(국내) > 회원사 참조)
    FID_INPUT_DATE_1: str  # 입력날짜1 — 날짜 ~
    FID_INPUT_DATE_2: str  # 입력날짜2 — ~ 날짜
    FID_SCTN_CLS_CODE: str  # 구간구분코드 — 공백

class InquireMemberDailyResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식영업일자
    total_seln_qty: str | None = None  # 총매도수량
    total_shnu_qty: str | None = None  # 총매수2수량
    ntby_qty: str | None = None  # 순매수수량
    stck_prpr: str | None = None  # 주식현재가
    prdy_vrss: str | None = None  # 전일대비
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_ctrt: str | None = None  # 전일대비율
    acml_vol: str | None = None  # 누적거래량

class InquireMemberDailyResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InquireMemberDailyResponse_OutputItem] = []  # 응답상세 — array

class InquireMemberDailyExecutor(ApiExecutor[InquireMemberDailyRequest, InquireMemberDailyResponse]):
    """주식현재가 회원사 종목매매동향 [국내주식-197]."""

    # 주식현재가 회원사 종목매매동향 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0454] 증권사 종목매매동향 화면을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-member-daily"
    METHOD = "GET"
    RESPONSE_TYPE = InquireMemberDailyResponse
    TR_ID = "FHPST04540000"
