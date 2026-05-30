"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePaymtStdrBalanceRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드
    BASS_DT: str  # 기준일자
    WCRC_FRCR_DVSN_CD: str  # 원화외화구분코드 — 01(원화기준),02(외화기준)
    INQR_DVSN_CD: str  # 조회구분코드 — 00(전체), 01(일반), 02(미니스탁)

class InquirePaymtStdrBalanceResponse_Output1Item(KisBaseModel):
    """nested item."""

    pdno: str | None = None  # 상품번호
    prdt_name: str | None = None  # 상품명
    cblc_qty13: str | None = None  # 잔고수량13
    ord_psbl_qty1: str | None = None  # 주문가능수량1
    avg_unpr3: str | None = None  # 평균단가3
    ovrs_now_pric1: str | None = None  # 해외현재가격1
    frcr_pchs_amt: str | None = None  # 외화매입금액
    frcr_evlu_amt2: str | None = None  # 외화평가금액2
    evlu_pfls_amt2: str | None = None  # 평가손익금액2
    bass_exrt: str | None = None  # 기준환율
    oprt_dtl_dtime: str | None = None  # 조작상세일시
    buy_crcy_cd: str | None = None  # 매수통화코드
    thdt_sll_ccld_qty1: str | None = None  # 당일매도체결수량1
    thdt_buy_ccld_qty1: str | None = None  # 당일매수체결수량1
    evlu_pfls_rt1: str | None = None  # 평가손익율1
    tr_mket_name: str | None = None  # 거래시장명
    natn_kor_name: str | None = None  # 국가한글명
    std_pdno: str | None = None  # 표준상품번호
    mgge_qty: str | None = None  # 담보수량
    loan_rmnd: str | None = None  # 대출잔액
    prdt_type_cd: str | None = None  # 상품유형코드
    ovrs_excg_cd: str | None = None  # 해외거래소코드
    scts_dvsn_name: str | None = None  # 유가증권구분명
    ldng_cblc_qty: str | None = None  # 대여잔고수량

class InquirePaymtStdrBalanceResponse_Output2Item(KisBaseModel):
    """nested item."""

    crcy_cd: str | None = None  # 통화코드
    crcy_cd_name: str | None = None  # 통화코드명
    frcr_dncl_amt_2: str | None = None  # 외화예수금액2
    frst_bltn_exrt: str | None = None  # 최초고시환율
    frcr_evlu_amt2: str | None = None  # 외화평가금액2

class InquirePaymtStdrBalanceResponse_Output3Item(KisBaseModel):
    """nested item."""

    pchs_amt_smtl_amt: str | None = None  # 매입금액합계금액
    tot_evlu_pfls_amt: str | None = None  # 총평가손익금액
    evlu_erng_rt1: str | None = None  # 평가수익율1
    tot_dncl_amt: str | None = None  # 총예수금액
    wcrc_evlu_amt_smtl: str | None = None  # 원화평가금액합계
    tot_asst_amt2: str | None = None  # 총자산금액2
    frcr_cblc_wcrc_evlu_amt_smtl: str | None = None  # 외화잔고원화평가금액합계
    tot_loan_amt: str | None = None  # 총대출금액
    tot_ldng_evlu_amt: str | None = None  # 총대여평가금액

class InquirePaymtStdrBalanceResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[InquirePaymtStdrBalanceResponse_Output1Item] = []  # 응답상세 — array
    output2: list[InquirePaymtStdrBalanceResponse_Output2Item] = []  # 응답상세 — array
    output3: InquirePaymtStdrBalanceResponse_Output3Item | None = None  # 응답상세

class InquirePaymtStdrBalanceExecutor(ApiExecutor[InquirePaymtStdrBalanceRequest, InquirePaymtStdrBalanceResponse]):
    """해외주식 결제기준잔고 [해외주식-064]."""

    # 해외주식 결제기준잔고 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0829] 해외 결제기준잔고 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 적용환율은 당일 매매기준이며, 현재가의 경우 지연된 시세로 평가되므로 실제매도금액과 상이할 수 있습니다. ※ 주문가능수량 : 보유수량 - 미결제 매도수량 ※ 매입금액 계산 시 결제일의 최초고시환율을 적용하므로, 금일 

    PATH = "/uapi/overseas-stock/v1/trading/inquire-paymt-stdr-balance"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePaymtStdrBalanceResponse
    TR_ID = "CTRP6010R"
