"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireCcnlRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    STRT_ORD_DT: str  # 시작주문일자 — 주문내역 조회 시작 일자, YYYYMMDD
    END_ORD_DT: str  # 종료주문일자 — 주문내역 조회 마지막 일자, YYYYMMDD
    SLL_BUY_DVSN_CD: str  # 매도매수구분코드 — 00 : 전체 01 : 매도 02 : 매수
    CCLD_NCCS_DVSN: str  # 체결미체결구분 — 00 : 전체 01 : 체결 02 : 미체결
    SORT_SQN: str  # 정렬순서 — AS : 정순 DS : 역순
    STRT_ODNO: str  # 시작주문번호 — 조회 시작 번호 입력
    PDNO: str  # 상품번호 — 공란 시, 전체 조회 선물 6자리 (예: 101S03) 옵션 9자리 (예: 201S03370)
    MKET_ID_CD: str  # 시장ID코드 — 공란(Default)
    CTX_AREA_FK200: str  # 연속조회검색조건200 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK200값 : 다음페이지 조회시(2번째부터)
    CTX_AREA_NK200: str  # 연속조회키200 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200값 : 다음페이지 조회시(2번째부터)

class InquireCcnlResponse_Output1Item(KisBaseModel):
    """nested item."""

    ord_gno_brno: str | None = None  # 주문채번지점번호 — 계좌 개설 시 관리점으로 선택한 영업점의 고유번호
    cano: str | None = None  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    csac_name: str | None = None  # 종합계좌명 — 계좌의 고객명
    acnt_prdt_cd: str | None = None  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    ord_dt: str | None = None  # 주문일자 — 주문의 접수일자
    odno: str | None = None  # 주문번호 — 접수한 주문의 일련번호
    orgn_odno: str | None = None  # 원주문번호 — 정정 또는 취소 대상 주문의 일련번호
    sll_buy_dvsn_cd: str | None = None  # 매도매수구분코드 — 00 : 전체 01 : 매도 02 : 매수
    trad_dvsn_name: str | None = None  # 매매구분명 — 매도/매수 등 구분값
    nmpr_type_cd: str | None = None  # 호가유형코드 — 01 : 지정가 02 : 시장가 03 : 조건부 04 : 최유리
    nmpr_type_name: str | None = None  # 호가유형명 — 호가 유형의 명칭
    pdno: str | None = None  # 상품번호 — 선물옵션종목코드
    prdt_name: str | None = None  # 상품명
    prdt_type_cd: str | None = None  # 상품유형코드
    ord_qty: str | None = None  # 주문수량 — 주문 수량
    ord_idx: str | None = None  # 주문지수 — 주문 가격
    qty: str | None = None  # 잔량 — 주문 체결되지 않고 남은 수량
    ord_tmd: str | None = None  # 주문시각 — 주문 접수 시간
    tot_ccld_qty: str | None = None  # 총체결수량 — 주문 체결된 수량
    avg_idx: str | None = None  # 평균지수 — 체결된 주문 수량의 평균 체결 가격
    tot_ccld_amt: str | None = None  # 총체결금액 — 체결된 주문의 합계금액
    rjct_qty: str | None = None  # 거부수량 — 접수된 주문이 정상 처리되지 못하고 거부된 수량
    ingr_trad_rjct_rson_cd: str | None = None  # 장내매매거부사유코드 — 정상 처리되지 못하고 거부된 주문의 사유코드
    ingr_trad_rjct_rson_name: str | None = None  # 장내매매거부사유명 — 정상 처리되지 못하고 거부된 주문의 사유
    ord_stfno: str | None = None  # 주문직원번호 — 주문 접수한 직원의 사번 또는 온라인 주문 시 매체 유형코드
    sprd_item_yn: str | None = None  # 스프레드종목여부 — 스프레드 종목 여부 구분값
    ord_ip_addr: str | None = None  # 주문IP주소 — 주문 시 사용한 매체의 IP 주소

class InquireCcnlResponse_Output2Item(KisBaseModel):
    """nested item."""

    tot_ord_qty: str | None = None  # 총주문수량 — 전체 주문 수량
    tot_ccld_amt_smtl: str | None = None  # 총체결금액합계 — 체결된 주문 전체의 합계 금액
    tot_ccld_qty_smtl: str | None = None  # 총체결수량합계 — 체결된 주문 전체의 합계 수량
    fee_smtl: str | None = None  # 수수료합계 — 체결된 주문에 대한 매매수수료의 합계 금액
    ctac_tlno: str | None = None  # 연락전화번호 — 고객의 연락 가능한 전화번호

class InquireCcnlResponse(KisCommonResponse):
    """응답 본문."""

    ctx_area_fk200: str | None = None  # 연속조회검색조건200
    ctx_area_nk200: str | None = None  # 연속조회키200
    output1: list[str] = []  # 응답상세1
    output2: InquireCcnlResponse_Output2Item | None = None  # 응답상세2

class InquireCcnlExecutor(ApiExecutor[InquireCcnlRequest, InquireCcnlResponse]):
    """선물옵션 주문체결내역조회[v1_국내선물-003]."""

    # 선물옵션 주문체결내역조회 API입니다. 한 번의 호출에 최대 100건​까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다.

    PATH = "/uapi/domestic-futureoption/v1/trading/inquire-ccnl"
    METHOD = "GET"
    RESPONSE_TYPE = InquireCcnlResponse
    TR_ID = "TTTO5201R"
    TR_ID_VIRTUAL = "VTTO5201R"
