"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireDailyAmountFeeRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    INQR_STRT_DAY: str  # 조회시작일 — 조회시작일(YYYYMMDD)
    INQR_END_DAY: str  # 조회종료일 — 조회종료일(YYYYMMDD)
    CTX_AREA_FK200: str  # 연속조회검색조건200
    CTX_AREA_NK200: str  # 연속조회키200

class InquireDailyAmountFeeResponse_Output1Item(KisBaseModel):
    """nested item."""

    ord_dt: str | None = None  # 주문일자
    pdno: str | None = None  # 상품번호
    item_name: str | None = None  # 종목명
    sll_agrm_amt: str | None = None  # 매도약정금액
    sll_fee: str | None = None  # 매도수수료
    buy_agrm_amt: str | None = None  # 매수약정금액
    buy_fee: str | None = None  # 매수수수료
    tot_fee_smtl: str | None = None  # 총수수료합계
    trad_pfls: str | None = None  # 매매손익

class InquireDailyAmountFeeResponse_Output2Item(KisBaseModel):
    """nested item."""

    futr_agrm: str | None = None  # 선물약정
    futr_agrm_amt: str | None = None  # 선물약정금액
    futr_agrm_amt_smtl: str | None = None  # 선물약정금액합계
    futr_sll_fee_smtl: str | None = None  # 선물매도수수료합계
    futr_buy_fee_smtl: str | None = None  # 선물매수수수료합계
    futr_fee_smtl: str | None = None  # 선물수수료합계
    opt_agrm: str | None = None  # 옵션약정
    opt_agrm_amt: str | None = None  # 옵션약정금액
    opt_agrm_amt_smtl: str | None = None  # 옵션약정금액합계
    opt_sll_fee_smtl: str | None = None  # 옵션매도수수료합계
    opt_buy_fee_smtl: str | None = None  # 옵션매수수수료합계
    opt_fee_smtl: str | None = None  # 옵션수수료합계
    prdt_futr_agrm: str | None = None  # 상품선물약정
    prdt_fuop: str | None = None  # 상품선물옵션
    prdt_futr_evlu_amt: str | None = None  # 상품선물평가금액
    futr_fee: str | None = None  # 선물수수료
    opt_fee: str | None = None  # 옵션수수료
    fee: str | None = None  # 수수료
    sll_agrm_amt: str | None = None  # 매도약정금액
    buy_agrm_amt: str | None = None  # 매수약정금액
    agrm_amt_smtl: str | None = None  # 약정금액합계
    sll_fee: str | None = None  # 매도수수료
    buy_fee: str | None = None  # 매수수수료
    fee_smtl: str | None = None  # 수수료합계
    trad_pfls_smtl: str | None = None  # 매매손익합계

class InquireDailyAmountFeeResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[str] = []  # 응답상세 — array
    output2: InquireDailyAmountFeeResponse_Output2Item | None = None  # 응답상세2

class InquireDailyAmountFeeExecutor(ApiExecutor[InquireDailyAmountFeeRequest, InquireDailyAmountFeeResponse]):
    """선물옵션기간약정수수료일별[v1_국내선물-017]."""

    # 선물옵션기간약정수수료일별 API입니다.

    PATH = "/uapi/domestic-futureoption/v1/trading/inquire-daily-amount-fee"
    METHOD = "GET"
    RESPONSE_TYPE = InquireDailyAmountFeeResponse
    TR_ID = "CTFO6119R"
