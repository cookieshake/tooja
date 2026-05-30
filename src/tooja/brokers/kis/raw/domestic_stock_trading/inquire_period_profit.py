"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePeriodProfitRequest(KisBaseModel):
    """요청."""

    ACNT_PRDT_CD: str  # 계좌상품코드
    CANO: str  # 종합계좌번호
    INQR_STRT_DT: str  # 조회시작일자
    PDNO: str  # 상품번호 — ""공란입력 시, 전체
    CTX_AREA_NK100: str  # 연속조회키100
    INQR_END_DT: str  # 조회종료일자
    SORT_DVSN: str  # 정렬구분 — 00: 최근 순, 01: 과거 순, 02: 최근 순
    INQR_DVSN: str  # 조회구분 — 00 입력
    CBLC_DVSN: str  # 잔고구분 — 00: 전체
    CTX_AREA_FK100: str  # 연속조회검색조건100

class InquirePeriodProfitResponse_Output1Item(KisBaseModel):
    """nested item."""

    trad_dt: str | None = None  # 매매일자
    buy_amt: str | None = None  # 매수금액
    sll_amt: str | None = None  # 매도금액
    rlzt_pfls: str | None = None  # 실현손익
    fee: str | None = None  # 수수료
    loan_int: str | None = None  # 대출이자
    tl_tax: str | None = None  # 제세금
    pfls_rt: str | None = None  # 손익률
    sll_qty1: str | None = None  # 매도수량1
    buy_qty1: str | None = None  # 매수수량1

class InquirePeriodProfitResponse_Output2Item(KisBaseModel):
    """nested item."""

    sll_qty_smtl: str | None = None  # 매도수량합계
    sll_tr_amt_smtl: str | None = None  # 매도거래금액합계
    sll_fee_smtl: str | None = None  # 매도수수료합계
    sll_tltx_smtl: str | None = None  # 매도제세금합계
    sll_excc_amt_smtl: str | None = None  # 매도정산금액합계
    buy_qty_smtl: str | None = None  # 매수수량합계
    buy_tr_amt_smtl: str | None = None  # 매수거래금액합계
    buy_fee_smtl: str | None = None  # 매수수수료합계
    buy_tax_smtl: str | None = None  # 매수제세금합계
    buy_excc_amt_smtl: str | None = None  # 매수정산금액합계
    tot_qty: str | None = None  # 총수량
    tot_tr_amt: str | None = None  # 총거래금액
    tot_fee: str | None = None  # 총수수료
    tot_tltx: str | None = None  # 총제세금
    tot_excc_amt: str | None = None  # 총정산금액
    tot_rlzt_pfls: str | None = None  # 총실현손익 — ※ HTS[0856] 기간별 매매손익 '일별' 화면의 우측 하단 '총손익률' 항목은 기간별매매손익현황조회(TTTC8715R) > output2 > tot_pftrt(총수익률) 으로 확인 가능
    loan_int: str | None = None  # 대출이자

class InquirePeriodProfitResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[InquirePeriodProfitResponse_Output1Item] = []  # 응답상세 — array
    output2: InquirePeriodProfitResponse_Output2Item | None = None  # 응답상세2

class InquirePeriodProfitExecutor(ApiExecutor[InquirePeriodProfitRequest, InquirePeriodProfitResponse]):
    """기간별손익일별합산조회[v1_국내주식-052]."""

    # 기간별손익일별합산조회 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0856] 기간별 매매손익 화면 에서 "일별" 클릭 시의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/trading/inquire-period-profit"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePeriodProfitResponse
    TR_ID = "TTTC8708R"
