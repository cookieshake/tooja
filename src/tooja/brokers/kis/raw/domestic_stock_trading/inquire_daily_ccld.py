"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireDailyCcldRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    INQR_STRT_DT: str  # 조회시작일자 — YYYYMMDD
    INQR_END_DT: str  # 조회종료일자 — YYYYMMDD
    SLL_BUY_DVSN_CD: str  # 매도매수구분코드 — 00 : 전체 / 01 : 매도 / 02 : 매수
    PDNO: str | None = None  # 상품번호 — 종목번호(6자리)
    ORD_GNO_BRNO: str  # 주문채번지점번호 — 주문시 한국투자증권 시스템에서 지정된 영업점코드
    ODNO: str | None = None  # 주문번호 — 주문시 한국투자증권 시스템에서 채번된 주문번호
    CCLD_DVSN: str  # 체결구분 — '00 전체 01 체결 02 미체결'
    INQR_DVSN: str  # 조회구분 — '00 역순 01 정순'
    INQR_DVSN_1: str  # 조회구분1 — '없음: 전체 1: ELW 2: 프리보드'
    INQR_DVSN_3: str  # 조회구분3 — '00 전체 01 현금 02 신용 03 담보 04 대주 05 대여 06 자기융자신규/상환 07 유통융자신규/상환'
    EXCG_ID_DVSN_CD: str  # 거래소ID구분코드 — 한국거래소 : KRX 대체거래소 (NXT) : NXT SOR (Smart Order Routing) : SOR ALL : 전체 ※ 모의투자는 KRX만 제공
    CTX_AREA_FK100: str  # 연속조회검색조건100 — '공란 : 최초 조회시는 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)'
    CTX_AREA_NK100: str  # 연속조회키100 — '공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)'

class InquireDailyCcldResponse_Output1Item(KisBaseModel):
    """nested item."""

    ord_dt: str | None = None  # 주문일자
    ord_gno_brno: str | None = None  # 주문채번지점번호
    odno: str | None = None  # 주문번호
    orgn_odno: str | None = None  # 원주문번호
    ord_dvsn_name: str | None = None  # 주문구분명
    sll_buy_dvsn_cd: str | None = None  # 매도매수구분코드
    sll_buy_dvsn_cd_name: str | None = None  # 매도매수구분코드명
    pdno: str | None = None  # 상품번호
    prdt_name: str | None = None  # 상품명
    ord_qty: str | None = None  # 주문수량
    ord_unpr: str | None = None  # 주문단가
    ord_tmd: str | None = None  # 주문시각
    tot_ccld_qty: str | None = None  # 총체결수량
    avg_prvs: str | None = None  # 평균가
    cncl_yn: str | None = None  # 취소여부
    tot_ccld_amt: str | None = None  # 총체결금액
    loan_dt: str | None = None  # 대출일자
    ordr_empno: str | None = None  # 주문자사번
    ord_dvsn_cd: str | None = None  # 주문구분코드
    cnc_cfrm_qty: str | None = None  # 취소확인수량
    rmn_qty: str | None = None  # 잔여수량
    rjct_qty: str | None = None  # 거부수량
    ccld_cndt_name: str | None = None  # 체결조건명
    inqr_ip_addr: str | None = None  # 조회IP주소
    cpbc_ordp_ord_rcit_dvsn_cd: str | None = None  # 전산주문표주문접수구분코드
    cpbc_ordp_infm_mthd_dvsn_cd: str | None = None  # 전산주문표통보방법구분코드
    infm_tmd: str | None = None  # 통보시각
    ctac_tlno: str | None = None  # 연락전화번호
    prdt_type_cd: str | None = None  # 상품유형코드
    excg_dvsn_cd: str | None = None  # 거래소구분코드
    cpbc_ordp_mtrl_dvsn_cd: str | None = None  # 전산주문표자료구분코드
    ord_orgno: str | None = None  # 주문조직번호
    rsvn_ord_end_dt: str | None = None  # 예약주문종료일자
    excg_id_dvsn_Cd: str | None = None  # 거래소ID구분코드
    stpm_cndt_pric: str | None = None  # 스톱지정가조건가격
    stpm_efct_occr_dtmd: str | None = None  # 스톱지정가효력발생상세시각

class InquireDailyCcldResponse_Output2Item(KisBaseModel):
    """nested item."""

    tot_ord_qty: str | None = None  # 총주문수량
    tot_ccld_qty: str | None = None  # 총체결수량
    tot_ccld_amt: str | None = None  # 매입평균가격
    prsm_tlex_smtl: str | None = None  # 총체결금액
    pchs_avg_pric: str | None = None  # 추정제비용합계

class InquireDailyCcldResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[InquireDailyCcldResponse_Output1Item] = []  # 응답상세 — array
    output2: InquireDailyCcldResponse_Output2Item | None = None  # 응답상세 — single

class InquireDailyCcldExecutor(ApiExecutor[InquireDailyCcldRequest, InquireDailyCcldResponse]):
    """주식일별주문체결조회[v1_국내주식-005]."""

    # 주식일별주문체결조회 API입니다. 실전계좌의 경우, 한 번의 호출에 최대 100건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다. 모의계좌의 경우, 한 번의 호출에 최대 15건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다. * 다만, 3개월 이전 체결내역 조회(CTSC9115R) 의 경우, 장중에는 많은 거래량으로 인해 순간적으로 DB가 밀렸거나 응답을 늦게 받거나 하는 등의 이

    PATH = "/uapi/domestic-stock/v1/trading/inquire-daily-ccld"
    METHOD = "GET"
    RESPONSE_TYPE = InquireDailyCcldResponse
    # Spec lists tr_id as "(3개월이내) VTTC0081R (3개월이전) VTSC9215R"; the codegen
    # mis-parsed it to "3". We query intraday only -> 3-month-inside variant.
    TR_ID = "TTTC0081R"
    TR_ID_VIRTUAL = "VTTC0081R"
