"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePeriodProfitRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    OVRS_EXCG_CD: str  # 해외거래소코드 — 공란 : 전체, NASD : 미국, SEHK : 홍콩, SHAA : 중국, TKSE : 일본, HASE : 베트남
    NATN_CD: str  # 국가코드 — 공란(Default)
    CRCY_CD: str  # 통화코드 — 공란 : 전체 USD : 미국달러, HKD : 홍콩달러, CNY : 중국위안화, JPY : 일본엔화, VND : 베트남동
    PDNO: str  # 상품번호 — 공란 : 전체
    INQR_STRT_DT: str  # 조회시작일자 — YYYYMMDD
    INQR_END_DT: str  # 조회종료일자 — YYYYMMDD
    WCRC_FRCR_DVSN_CD: str  # 원화외화구분코드 — 01 : 외화, 02 : 원화
    CTX_AREA_FK200: str  # 연속조회검색조건200
    CTX_AREA_NK200: str  # 연속조회키200

class InquirePeriodProfitResponse_Output1Item(KisBaseModel):
    """nested item."""

    trad_day: str | None = None  # 매매일
    ovrs_pdno: str | None = None  # 해외상품번호
    ovrs_item_name: str | None = None  # 해외종목명
    slcl_qty: str | None = None  # 매도청산수량
    pchs_avg_pric: str | None = None  # 매입평균가격
    frcr_pchs_amt1: str | None = None  # 외화매입금액1
    avg_sll_unpr: str | None = None  # 평균매도단가
    frcr_sll_amt_smtl1: str | None = None  # 외화매도금액합계1
    stck_sll_tlex: str | None = None  # 주식매도제비용
    ovrs_rlzt_pfls_amt: str | None = None  # 해외실현손익금액
    pftrt: str | None = None  # 수익률
    exrt: str | None = None  # 환율
    ovrs_excg_cd: str | None = None  # 해외거래소코드
    frst_bltn_exrt: str | None = None  # 최초고시환율

class InquirePeriodProfitResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_sll_amt_smtl: str | None = None  # 주식매도금액합계 — WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시
    stck_buy_amt_smtl: str | None = None  # 주식매수금액합계 — WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시
    smtl_fee1: str | None = None  # 합계수수료1 — WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시
    excc_dfrm_amt: str | None = None  # 정산지급금액 — WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시
    ovrs_rlzt_pfls_tot_amt: str | None = None  # 해외실현손익총금액 — WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시
    tot_pftrt: str | None = None  # 총수익률
    bass_dt: str | None = None  # 기준일자
    exrt: str | None = None  # 환율

class InquirePeriodProfitResponse(KisCommonResponse):
    """응답 본문."""

    Output1: list[InquirePeriodProfitResponse_Output1Item] = []  # 응답상세 — array
    Output2: InquirePeriodProfitResponse_Output2Item | None = None  # 응답상세2

class InquirePeriodProfitExecutor(ApiExecutor[InquirePeriodProfitRequest, InquirePeriodProfitResponse]):
    """해외주식 기간손익[v1_해외주식-032]."""

    # 해외주식 기간손익 API입니다. 한국투자 HTS(eFriend Plus) &gt; [7717] 해외 기간손익 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. * 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고) https://securities.koreainvestment.com/main/bond/research/_static/TF03ca010001

    PATH = "/uapi/overseas-stock/v1/trading/inquire-period-profit"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePeriodProfitResponse
    TR_ID = "TTTS3039R"
