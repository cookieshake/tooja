"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class PeriodRightsRequest(KisBaseModel):
    """요청."""

    INQR_DVSN: str  # 조회구분 — 03 입력
    CUST_RNCNO25: str  # 고객실명확인번호25 — 공란
    HMID: str  # 홈넷ID — 공란
    CANO: str  # 종합계좌번호 — 계좌번호 8자리 입력 (ex.12345678)
    ACNT_PRDT_CD: str  # 계좌상품코드 — 상품계좌번호 2자리 입력(ex. 01 or 22)
    INQR_STRT_DT: str  # 조회시작일자 — 조회시작일자(YYYYMMDD)
    INQR_END_DT: str  # 조회종료일자 — 조회종료일자(YYYYMMDD)
    RGHT_TYPE_CD: str  # 권리유형코드 — 공란
    PDNO: str  # 상품번호 — 공란
    PRDT_TYPE_CD: str  # 상품유형코드 — 공란
    CTX_AREA_NK100: str  # 연속조회키100 — 다음조회시 입력
    CTX_AREA_FK100: str  # 연속조회검색조건100 — 다음조회시 입력

class PeriodRightsResponse_Output1Item(KisBaseModel):
    """nested item."""

    acno10: str | None = None  # 계좌번호10
    rght_type_cd: str | None = None  # 권리유형코드 — 1 유상 2 무상 3 배당 4 매수청구 5 공개매수 6 주주총회 7 신주인수권증서 8 반대의사 9 신주인수권증권 11 합병 12 회사분할 13 주식교환 14 액면분할 15 액면병합 16 종목변경 17 감자 18 신구주합병 21 후합병 
    bass_dt: str | None = None  # 기준일자
    rght_cblc_type_cd: str | None = None  # 권리잔고유형코드 — 1 입고 2 출고 3 출고입고 4 출고입금 5 출고출금 10 현금입금 11 단수주대금입금 12 교부금입금 13 유상감자대금입금 14 지연이자입금 15 이자지급 16 대주권리금출금 17 분할상환 18 만기상환 19 조기상환 20 출금
    rptt_pdno: str | None = None  # 대표상품번호
    pdno: str | None = None  # 상품번호
    prdt_type_cd: str | None = None  # 상품유형코드
    shtn_pdno: str | None = None  # 단축상품번호
    prdt_name: str | None = None  # 상품명
    cblc_qty: str | None = None  # 잔고수량
    last_alct_qty: str | None = None  # 최종배정수량
    excs_alct_qty: str | None = None  # 초과배정수량
    tot_alct_qty: str | None = None  # 총배정수량
    last_ftsk_qty: str | None = None  # 최종단수주수량
    last_alct_amt: str | None = None  # 최종배정금액
    last_ftsk_chgs: str | None = None  # 최종단수주대금
    rdpt_prca: str | None = None  # 상환원금
    dlay_int_amt: str | None = None  # 지연이자금액
    lstg_dt: str | None = None  # 상장일자
    sbsc_end_dt: str | None = None  # 청약종료일자
    cash_dfrm_dt: str | None = None  # 현금지급일자
    rqst_qty: str | None = None  # 신청수량
    rqst_amt: str | None = None  # 신청금액
    rqst_dt: str | None = None  # 신청일자
    rfnd_dt: str | None = None  # 환불일자
    rfnd_amt: str | None = None  # 환불금액
    lstg_stqt: str | None = None  # 상장주수
    tax_amt: str | None = None  # 세금금액
    sbsc_unpr: str | None = None  # 청약단가

class PeriodRightsResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[PeriodRightsResponse_Output1Item] = []  # 응답상세 — array

class PeriodRightsExecutor(ApiExecutor[PeriodRightsRequest, PeriodRightsResponse]):
    """기간별계좌권리현황조회 [국내주식-211]."""

    # 기간별계좌권리현황조회 API입니다. 한국투자 HTS(eFriend Plus) &gt; [7344] 권리유형별 현황조회 화면을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/trading/period-rights"
    METHOD = "GET"
    RESPONSE_TYPE = PeriodRightsResponse
    TR_ID = "CTRGA011R"
