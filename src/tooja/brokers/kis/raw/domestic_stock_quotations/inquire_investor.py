"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireInvestorRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — J : KRX, NX : NXT, UN : 통합
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목코드 (ex 005930 삼성전자)

class InquireInvestorResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자
    stck_clpr: str | None = None  # 주식 종가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prsn_ntby_qty: str | None = None  # 개인 순매수 수량
    frgn_ntby_qty: str | None = None  # 외국인 순매수 수량
    orgn_ntby_qty: str | None = None  # 기관계 순매수 수량
    prsn_ntby_tr_pbmn: str | None = None  # 개인 순매수 거래 대금
    frgn_ntby_tr_pbmn: str | None = None  # 외국인 순매수 거래 대금
    orgn_ntby_tr_pbmn: str | None = None  # 기관계 순매수 거래 대금
    prsn_shnu_vol: str | None = None  # 개인 매수2 거래량
    frgn_shnu_vol: str | None = None  # 외국인 매수2 거래량
    orgn_shnu_vol: str | None = None  # 기관계 매수2 거래량
    prsn_shnu_tr_pbmn: str | None = None  # 개인 매수2 거래 대금
    frgn_shnu_tr_pbmn: str | None = None  # 외국인 매수2 거래 대금
    orgn_shnu_tr_pbmn: str | None = None  # 기관계 매수2 거래 대금
    prsn_seln_vol: str | None = None  # 개인 매도 거래량
    frgn_seln_vol: str | None = None  # 외국인 매도 거래량
    orgn_seln_vol: str | None = None  # 기관계 매도 거래량
    prsn_seln_tr_pbmn: str | None = None  # 개인 매도 거래 대금
    frgn_seln_tr_pbmn: str | None = None  # 외국인 매도 거래 대금
    orgn_seln_tr_pbmn: str | None = None  # 기관계 매도 거래 대금

class InquireInvestorResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InquireInvestorResponse_OutputItem] = []  # 응답상세 — Array

class InquireInvestorExecutor(ApiExecutor[InquireInvestorRequest, InquireInvestorResponse]):
    """주식현재가 투자자[v1_국내주식-012]."""

    # 주식현재가 투자자 API입니다. 개인, 외국인, 기관 등 투자 정보를 확인할 수 있습니다. [유의사항] - 외국인은 외국인(외국인투자등록 고유번호가 있는 경우)+기타 외국인을 지칭합니다. - 당일 데이터는 장 종료 후 제공됩니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-investor"
    METHOD = "GET"
    RESPONSE_TYPE = InquireInvestorResponse
    TR_ID = "FHKST01010900"
