"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePeriodTransRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드
    ERLM_STRT_DT: str  # 등록시작일자 — 입력날짜 ~ (ex) 20240420)
    ERLM_END_DT: str  # 등록종료일자 — ~입력날짜 (ex) 20240520)
    OVRS_EXCG_CD: str  # 해외거래소코드 — 공백
    PDNO: str  # 상품번호 — 공백 (전체조회), 개별종목 조회는 상품번호입력
    SLL_BUY_DVSN_CD: str  # 매도매수구분코드 — 00(전체), 01(매도), 02(매수)
    LOAN_DVSN_CD: str  # 대출구분코드 — 공백
    CTX_AREA_FK100: str  # 연속조회검색조건100 — 공백
    CTX_AREA_NK100: str  # 연속조회키100 — 공백

class InquirePeriodTransResponse_Output1Item(KisBaseModel):
    """nested item."""

    trad_dt: str | None = None  # 매매일자
    sttl_dt: str | None = None  # 결제일자
    sll_buy_dvsn_cd: str | None = None  # 매도매수구분코드
    sll_buy_dvsn_name: str | None = None  # 매도매수구분명
    pdno: str | None = None  # 상품번호
    ovrs_item_name: str | None = None  # 해외종목명
    ccld_qty: str | None = None  # 체결수량
    amt_unit_ccld_qty: str | None = None  # 금액단위체결수량
    ft_ccld_unpr2: str | None = None  # FT체결단가2
    ovrs_stck_ccld_unpr: str | None = None  # 해외주식체결단가
    tr_frcr_amt2: str | None = None  # 거래외화금액2
    tr_amt: str | None = None  # 거래금액
    frcr_excc_amt_1: str | None = None  # 외화정산금액1
    wcrc_excc_amt: str | None = None  # 원화정산금액
    dmst_frcr_fee1: str | None = None  # 국내외화수수료1
    frcr_fee1: str | None = None  # 외화수수료1
    dmst_wcrc_fee: str | None = None  # 국내원화수수료
    ovrs_wcrc_fee: str | None = None  # 해외원화수수료
    crcy_cd: str | None = None  # 통화코드
    std_pdno: str | None = None  # 표준상품번호
    erlm_exrt: str | None = None  # 등록환율
    loan_dvsn_cd: str | None = None  # 대출구분코드
    loan_dvsn_name: str | None = None  # 대출구분명

class InquirePeriodTransResponse_Output2Item(KisBaseModel):
    """nested item."""

    frcr_buy_amt_smtl: str | None = None  # 외화매수금액합계
    frcr_sll_amt_smtl: str | None = None  # 외화매도금액합계
    dmst_fee_smtl: str | None = None  # 국내수수료합계
    ovrs_fee_smtl: str | None = None  # 해외수수료합계

class InquirePeriodTransResponse(KisCommonResponse):
    """응답 본문."""

    ctx_area_fk100: str | None = None  # 연속조회검색조건100
    ctx_area_nk100: str | None = None  # 연속조회키100
    output1: list[InquirePeriodTransResponse_Output1Item] = []  # 응답상세 — array
    output2: InquirePeriodTransResponse_Output2Item | None = None  # 응답상세

class InquirePeriodTransExecutor(ApiExecutor[InquirePeriodTransRequest, InquirePeriodTransResponse]):
    """해외주식 일별거래내역 [해외주식-063]."""

    # 해외주식 일별거래내역 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0828] 해외증권 일별거래내역 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 체결가격, 매매금액, 정산금액, 수수료 원화금액은 국내 결제일까지는 예상환율로 적용되고, 국내 결제일 익일부터 확정환율로 적용됨으로 금액이 변경될 수 있습니다. ※ 해외증권 투자 및 업무문의 안내: 한국투자증권 해

    PATH = "/uapi/overseas-stock/v1/trading/inquire-period-trans"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePeriodTransResponse
    TR_ID = "CTOS4001R"
