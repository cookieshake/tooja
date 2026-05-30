"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class DailyCreditBalanceRequest(KisBaseModel):
    """요청."""

    fid_cond_mrkt_div_code: str  # 시장 분류 코드 — 시장구분코드 (주식 J)
    fid_cond_scr_div_code: str  # 화면 분류 코드 — Unique key(20476)
    fid_input_iscd: str  # 종목코드 — 종목코드 (ex 005930)
    fid_input_date_1: str  # 결제일자 — 결제일자 (ex 20240313)

class DailyCreditBalanceResponse_OutputItem(KisBaseModel):
    """nested item."""

    deal_date: str | None = None  # 매매 일자
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_vrss: str | None = None  # 전일 대비
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    stlm_date: str | None = None  # 결제 일자
    whol_loan_new_stcn: str | None = None  # 전체 융자 신규 주수 — 단위: 주
    whol_loan_rdmp_stcn: str | None = None  # 전체 융자 상환 주수 — 단위: 주
    whol_loan_rmnd_stcn: str | None = None  # 전체 융자 잔고 주수 — 단위: 주
    whol_loan_new_amt: str | None = None  # 전체 융자 신규 금액 — 단위: 만원
    whol_loan_rdmp_amt: str | None = None  # 전체 융자 상환 금액 — 단위: 만원
    whol_loan_rmnd_amt: str | None = None  # 전체 융자 잔고 금액 — 단위: 만원
    whol_loan_rmnd_rate: str | None = None  # 전체 융자 잔고 비율
    whol_loan_gvrt: str | None = None  # 전체 융자 공여율
    whol_stln_new_stcn: str | None = None  # 전체 대주 신규 주수 — 단위: 주
    whol_stln_rdmp_stcn: str | None = None  # 전체 대주 상환 주수 — 단위: 주
    whol_stln_rmnd_stcn: str | None = None  # 전체 대주 잔고 주수 — 단위: 주
    whol_stln_new_amt: str | None = None  # 전체 대주 신규 금액 — 단위: 만원
    whol_stln_rdmp_amt: str | None = None  # 전체 대주 상환 금액 — 단위: 만원
    whol_stln_rmnd_amt: str | None = None  # 전체 대주 잔고 금액 — 단위: 만원
    whol_stln_rmnd_rate: str | None = None  # 전체 대주 잔고 비율
    whol_stln_gvrt: str | None = None  # 전체 대주 공여율
    stck_oprc: str | None = None  # 주식 시가2
    stck_hgpr: str | None = None  # 주식 최고가
    stck_lwpr: str | None = None  # 주식 최저가

class DailyCreditBalanceResponse(KisCommonResponse):
    """응답 본문."""

    output: list[DailyCreditBalanceResponse_OutputItem] = []  # 응답상세 — array

class DailyCreditBalanceExecutor(ApiExecutor[DailyCreditBalanceRequest, DailyCreditBalanceResponse]):
    """국내주식 신용잔고 일별추이[국내주식-110]."""

    # 국내주식 신용잔고 일별추이 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0476] 국내주식 신용잔고 일별추이 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 한 번의 호출에 최대 30건 확인 가능하며, fid_input_date_1 을 입력하여 다음 조회가 가능합니다. ※ 상환수량은 "매도상환수량+현금상환수량"의 합계 수치입니다.

    PATH = "/uapi/domestic-stock/v1/quotations/daily-credit-balance"
    METHOD = "GET"
    RESPONSE_TYPE = DailyCreditBalanceResponse
    TR_ID = "FHPST04760000"
