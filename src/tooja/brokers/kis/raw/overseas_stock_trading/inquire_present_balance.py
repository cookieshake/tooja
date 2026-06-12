"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePresentBalanceRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    WCRC_FRCR_DVSN_CD: str  # 원화외화구분코드 — 01 : 원화 02 : 외화
    NATN_CD: str  # 국가코드 — 000 전체 840 미국 344 홍콩 156 중국 392 일본 704 베트남
    TR_MKET_CD: str  # 거래시장코드 — [Request body NATN_CD 000 설정] 00 : 전체 [Request body NATN_CD 840 설정] 00 : 전체 01 : 나스닥(NASD) 02 : 뉴욕거래소(NYSE) 03 : 미국(PINK SHEETS) 04
    INQR_DVSN_CD: str  # 조회구분코드 — 00 : 전체 01 : 일반해외주식 02 : 미니스탁

class InquirePresentBalanceResponse_Output1Item(KisBaseModel):
    """nested item."""

    prdt_name: str | None = None  # 상품명 — 종목명
    cblc_qty13: str | None = None  # 잔고수량13 — 결제보유수량
    thdt_buy_ccld_qty1: str | None = None  # 당일매수체결수량1 — 당일 매수 체결 완료 수량
    thdt_sll_ccld_qty1: str | None = None  # 당일매도체결수량1 — 당일 매도 체결 완료 수량
    ccld_qty_smtl1: str | None = None  # 체결수량합계1 — 체결기준 현재 보유수량
    ord_psbl_qty1: str | None = None  # 주문가능수량1 — 주문 가능한 주문 수량
    frcr_pchs_amt: str | None = None  # 외화매입금액 — 해당 종목의 외화 기준 매입금액
    frcr_evlu_amt2: str | None = None  # 외화평가금액2 — 해당 종목의 외화 기준 평가금액
    evlu_pfls_amt2: str | None = None  # 평가손익금액2 — 해당 종목의 매입금액과 평가금액의 외회기준 비교 손익
    evlu_pfls_rt1: str | None = None  # 평가손익율1 — 해당 종목의 평가손익을 기준으로 한 수익률
    pdno: str | None = None  # 상품번호 — 종목코드
    bass_exrt: str | None = None  # 기준환율 — 원화 평가 시 적용 환율
    buy_crcy_cd: str | None = None  # 매수통화코드 — USD : 미국달러 HKD : 홍콩달러 CNY : 중국위안화 JPY : 일본엔화 VND : 베트남동
    ovrs_now_pric1: str | None = None  # 해외현재가격1 — 해당 종목의 현재가
    avg_unpr3: str | None = None  # 평균단가3 — 해당 종목의 매수 평균 단가
    tr_mket_name: str | None = None  # 거래시장명 — 해당 종목의 거래시장명
    natn_kor_name: str | None = None  # 국가한글명 — 거래 국가명
    pchs_rmnd_wcrc_amt: str | None = None  # 매입잔액원화금액
    thdt_buy_ccld_frcr_amt: dict | None = None  # 당일매수체결외화금액 — 당일 매수 외화금액 (Type: Object X String O)
    thdt_sll_ccld_frcr_amt: str | None = None  # 당일매도체결외화금액 — 당일 매도 외화금액
    unit_amt: str | None = None  # 단위금액
    std_pdno: str | None = None  # 표준상품번호
    prdt_type_cd: str | None = None  # 상품유형코드
    scts_dvsn_name: str | None = None  # 유가증권구분명
    loan_rmnd: str | None = None  # 대출잔액 — 대출 미상환 금액
    loan_dt: str | None = None  # 대출일자 — 대출 실행일자
    loan_expd_dt: str | None = None  # 대출만기일자 — 대출 만기일자
    ovrs_excg_cd: str | None = None  # 해외거래소코드 — NASD : 나스닥 NYSE : 뉴욕 AMEX : 아멕스 SEHK : 홍콩 SHAA : 중국상해 SZAA : 중국심천 TKSE : 일본 HASE : 하노이거래소 VNSE : 호치민거래소
    item_lnkg_excg_cd: str | None = None  # 종목연동거래소코드 — prdt_dvsn(상품구분) : 직원용 데이터(Type: String, Length:2)

class InquirePresentBalanceResponse_Output2Item(KisBaseModel):
    """nested item."""

    crcy_cd: str | None = None  # 통화코드
    crcy_cd_name: str | None = None  # 통화코드명
    frcr_buy_amt_smtl: str | None = None  # 외화매수금액합계 — 해당 통화로 매수한 종목 전체의 매수금액
    frcr_sll_amt_smtl: str | None = None  # 외화매도금액합계 — 해당 통화로 매도한 종목 전체의 매수금액
    frcr_dncl_amt_2: str | None = None  # 외화예수금액2 — 외화로 표시된 외화사용가능금액
    frst_bltn_exrt: str | None = None  # 최초고시환율
    frcr_buy_mgn_amt: str | None = None  # 외화매수증거금액 — 매수증거금으로 사용된 외화금액
    frcr_etc_mgna: str | None = None  # 외화기타증거금
    frcr_drwg_psbl_amt_1: str | None = None  # 외화출금가능금액1 — 출금가능한 외화금액
    frcr_evlu_amt2: str | None = None  # 출금가능원화금액 — 출금가능한 원화금액
    acpl_cstd_crcy_yn: str | None = None  # 현지보관통화여부
    nxdy_frcr_drwg_psbl_amt: str | None = None  # 익일외화출금가능금액

class InquirePresentBalanceResponse_Output3Item(KisBaseModel):
    """nested item."""

    pchs_amt_smtl: str | None = None  # 매입금액합계 — 해외유가증권 매수금액의 원화 환산 금액
    evlu_amt_smtl: str | None = None  # 평가금액합계 — 해외유가증권 평가금액의 원화 환산 금액
    evlu_pfls_amt_smtl: str | None = None  # 평가손익금액합계 — 해외유가증권 평가손익의 원화 환산 금액
    dncl_amt: str | None = None  # 예수금액
    cma_evlu_amt: str | None = None  # CMA평가금액
    tot_dncl_amt: str | None = None  # 총예수금액
    etc_mgna: str | None = None  # 기타증거금
    wdrw_psbl_tot_amt: str | None = None  # 인출가능총금액
    frcr_evlu_tota: str | None = None  # 외화평가총액
    evlu_erng_rt1: str | None = None  # 평가수익율1
    pchs_amt_smtl_amt: str | None = None  # 매입금액합계금액
    evlu_amt_smtl_amt: str | None = None  # 평가금액합계금액
    tot_evlu_pfls_amt: str | None = None  # 총평가손익금액
    tot_asst_amt: str | None = None  # 총자산금액
    buy_mgn_amt: str | None = None  # 매수증거금액
    mgna_tota: str | None = None  # 증거금총액
    frcr_use_psbl_amt: str | None = None  # 외화사용가능금액
    ustl_sll_amt_smtl: str | None = None  # 미결제매도금액합계
    ustl_buy_amt_smtl: str | None = None  # 미결제매수금액합계
    tot_frcr_cblc_smtl: str | None = None  # 총외화잔고합계
    tot_loan_amt: str | None = None  # 총대출금액

class InquirePresentBalanceResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[InquirePresentBalanceResponse_Output1Item] = []  # 체결기준 잔고
    output2: list[InquirePresentBalanceResponse_Output2Item] = []  # 통화별 요약
    output3: InquirePresentBalanceResponse_Output3Item | None = None  # 계좌 요약

class InquirePresentBalanceExecutor(ApiExecutor[InquirePresentBalanceRequest, InquirePresentBalanceResponse]):
    """해외주식 체결기준현재잔고[v1_해외주식-008]."""

    # 해외주식 잔고를 체결 기준으로 확인하는 API 입니다. HTS(eFriend Plus) [0839] 해외 체결기준잔고 화면을 API로 구현한 사항으로 화면을 함께 보시면 기능 이해가 쉽습니다. (※모의계좌의 경우 output3(외화평가총액 등 확인 가능)만 정상 출력됩니다. 잔고 확인을 원하실 경우에는 해외주식 잔고[v1_해외주식-006] API 사용을 부탁드립니다.) * 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크

    PATH = "/uapi/overseas-stock/v1/trading/inquire-present-balance"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePresentBalanceResponse
    TR_ID = "CTRP6504R"
    TR_ID_VIRTUAL = "VTRP6504R"
