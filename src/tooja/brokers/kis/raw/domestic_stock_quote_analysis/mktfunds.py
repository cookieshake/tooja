"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class MktfundsRequest(KisBaseModel):
    """요청."""

    FID_INPUT_DATE_1: str  # 입력날짜1

class MktfundsResponse_OutputItem(KisBaseModel):
    """nested item."""

    bsop_date: str | None = None  # 영업일자
    bstp_nmix_prpr: str | None = None  # 업종지수현재가
    bstp_nmix_prdy_vrss: str | None = None  # 업종지수전일대비
    prdy_vrss_sign: str | None = None  # 전일대비부호 — 1. 상한 2. 상승 3. 보합 4. 하한 5. 하락
    prdy_ctrt: str | None = None  # 전일대비율
    hts_avls: str | None = None  # HTS시가총액 — 단위: 백만원
    cust_dpmn_amt: str | None = None  # 고객예탁금금액 — 단위: 억원
    cust_dpmn_amt_prdy_vrss: str | None = None  # 고객예탁금금액전일대비
    amt_tnrt: str | None = None  # 금액회전율
    uncl_amt: str | None = None  # 미수금액 — 단위: 억원
    crdt_loan_rmnd: str | None = None  # 신용융자잔고 — 단위: 억원
    futs_tfam_amt: str | None = None  # 선물예수금금액 — 단위: 억원
    sttp_amt: str | None = None  # 주식형금액 — 단위: 억원
    mxtp_amt: str | None = None  # 혼합형금액 — 단위: 억원
    bntp_amt: str | None = None  # 채권형금액 — 단위: 억원
    mmf_amt: str | None = None  # MMF금액 — 단위: 억원
    secu_lend_amt: str | None = None  # 담보대출잔고금액 — 단위: 억원

class MktfundsResponse(KisCommonResponse):
    """응답 본문."""

    output: list[MktfundsResponse_OutputItem] = []  # 응답상세 — array

class MktfundsExecutor(ApiExecutor[MktfundsRequest, MktfundsResponse]):
    """국내 증시자금 종합 [국내주식-193]."""

    # 국내 증시자금 종합 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0470] 증시자금 종합 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. (단위: 억원) ※ 해당자료는 금융투자협회의 자료를 제공하고 있으며, 오류와 지연이 발생할 수 있습니다. ※ 위 정보에 의한 투자판단의 최종책임은 정보이용자에게 있으며, 당사와 한국금융투자협회는 어떠한 법적인 책임도 지지 않사오

    PATH = "/uapi/domestic-stock/v1/quotations/mktfunds"
    METHOD = "GET"
    RESPONSE_TYPE = MktfundsResponse
    TR_ID = "FHKST649100C0"
