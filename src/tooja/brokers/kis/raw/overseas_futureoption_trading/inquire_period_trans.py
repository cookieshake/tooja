"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePeriodTransRequest(KisBaseModel):
    """요청."""

    INQR_TERM_FROM_DT: str  # 조회기간FROM일자
    INQR_TERM_TO_DT: str  # 조회기간TO일자
    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    ACNT_TR_TYPE_CD: str  # 계좌거래유형코드 — 1: 전체, 2:입출금 , 3: 결제
    CRCY_CD: str  # 통화코드 — '%%% : 전체 TUS: TOT_USD / TKR: TOT_KRW KRW: 한국 / USD: 미국 EUR: EUR / HKD: 홍콩 CNY: 중국 / JPY: 일본 VND: 베트남 '
    CTX_AREA_FK100: str  # 연속조회검색조건100 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK100값 : 다음페이지 조회시(2번째부터)
    CTX_AREA_NK100: str  # 연속조회키100 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100값 : 다음페이지 조회시(2번째부터)
    PWD_CHK_YN: str  # 비밀번호체크여부 — 공란(Default)

class InquirePeriodTransResponse_OutputItem(KisBaseModel):
    """nested item."""

    bass_dt: str | None = None  # 기준일자
    cano: str | None = None  # 종합계좌번호
    acnt_prdt_cd: str | None = None  # 계좌상품코드
    fm_ldgr_inog_seq: str | None = None  # FM원장출납순번
    acnt_tr_type_name: str | None = None  # 계좌거래유형명
    crcy_cd: str | None = None  # 통화코드
    tr_itm_name: str | None = None  # 거래항목명
    fm_iofw_amt: str | None = None  # FM입출금액
    fm_fee: str | None = None  # FM수수료
    fm_tax_amt: str | None = None  # FM세금금액
    fm_sttl_amt: str | None = None  # FM결제금액
    fm_bf_dncl_amt: str | None = None  # FM이전예수금액
    fm_dncl_amt: str | None = None  # FM예수금액
    fm_rcvb_occr_amt: str | None = None  # FM미수발생금액
    fm_rcvb_pybk_amt: str | None = None  # FM미수변제금액
    ovdu_int_pybk_amt: str | None = None  # 연체이자변제금액
    rmks_text: str | None = None  # 비고내용

class InquirePeriodTransResponse(KisCommonResponse):
    """응답 본문."""

    output: list[InquirePeriodTransResponse_OutputItem] = []  # 응답상세1 — Array

class InquirePeriodTransExecutor(ApiExecutor[InquirePeriodTransRequest, InquirePeriodTransResponse]):
    """해외선물옵션 기간계좌거래내역[해외선물-014]."""

    # 해외선물옵션 기간계좌거래내역 API입니다.

    PATH = "/uapi/overseas-futureoption/v1/trading/inquire-period-trans"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePeriodTransResponse
    TR_ID = "OTFM3114R"
