"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireNgtCcnlRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    STRT_ORD_DT: str  # 시작주문일자
    END_ORD_DT: str  # 종료주문일자 — 조회하려는 마지막 일자 다음일자로 조회 (ex. 20221011 까지의 내역을 조회하고자 할 경우, 20221012로 종료주문일자 설정)
    SLL_BUY_DVSN_CD: str  # 매도매수구분코드 — 공란 : default (00: 전체 ,01 : 매도, 02 : 매수)
    CCLD_NCCS_DVSN: str  # 체결미체결구분 — 00 : 전체 01 : 체결 02 : 미체결
    SORT_SQN: str  # 정렬순서 — 공란 : default (DS : 정순, 그외 : 역순)
    STRT_ODNO: str  # 시작주문번호 — 공란 : default
    PDNO: str  # 상품번호 — 공란 : default
    MKET_ID_CD: str  # 시장ID코드 — 공란 : default
    FUOP_DVSN_CD: str  # 선물옵션구분코드 — 공란 : 전체, 01 : 선물, 02 : 옵션
    SCRN_DVSN: str  # 화면구분 — 02(Default)
    CTX_AREA_FK200: str  # 연속조회검색조건200 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK200값 : 다음페이지 조회시(2번째부터)
    CTX_AREA_NK200: str  # 연속조회키200 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200값 : 다음페이지 조회시(2번째부터)

class InquireNgtCcnlResponse_Output2Item(KisBaseModel):
    """nested item."""

    tot_ord_qty: str | None = None  # 총주문수량
    tot_ccld_qty: str | None = None  # 총체결수량
    tot_ccld_qty_SMTL: str | None = None  # 총체결수량 — 신규 TR 사용 필드
    tot_ccld_amt: str | None = None  # 총체결금액
    tot_ccld_amt_SMTL: str | None = None  # 총체결금액 — 신규 TR 사용 필드
    fee: str | None = None  # 수수료
    ctac_tlno: str | None = None  # 연락전화번호 — 신규 TR 사용 필드

class InquireNgtCcnlResponse_Output1Item(KisBaseModel):
    """nested item."""

    ord_gno_brno: str | None = None  # 주문채번지점번호
    cano: str | None = None  # 종합계좌번호
    csac_name: str | None = None  # 종합계좌명
    acnt_prdt_cd: str | None = None  # 계좌상품코드
    ord_dt: str | None = None  # 주문일자
    odno: str | None = None  # 주문번호
    orgn_odno: str | None = None  # 원주문번호
    sll_buy_dvsn_cd: str | None = None  # 매도매수구분코드
    trad_dvsn_name: str | None = None  # 매매구분명
    nmpr_type_name: str | None = None  # 호가유형명
    pdno: str | None = None  # 상품번호
    prdt_name: str | None = None  # 상품명
    prdt_type_cd: str | None = None  # 상품유형코드
    ord_qty: str | None = None  # 주문수량
    ord_idx4: str | None = None  # 주문지수 — 신규 TR 사용 필드
    qty: str | None = None  # 잔량
    ord_tmd: str | None = None  # 주문시각
    tot_ccld_qty: str | None = None  # 총체결수량
    avg_idx: str | None = None  # 평균지수
    tot_ccld_amt: str | None = None  # 총체결금액
    rjct_qty: str | None = None  # 거부수량
    ingr_trad_rjct_rson_cd: str | None = None  # 장내매매거부사유코드
    ingr_trad_rjct_rson_name: str | None = None  # 장내매매거부사유명
    ord_stfno: str | None = None  # 주문직원번호
    sprd_item_yn: str | None = None  # 스프레드종목여부
    ord_ip_addr: str | None = None  # 주문IP주소

class InquireNgtCcnlResponse(KisCommonResponse):
    """응답 본문."""

    output2: InquireNgtCcnlResponse_Output2Item | None = None  # 응답상세1
    output1: list[InquireNgtCcnlResponse_Output1Item] = []  # 응답상세2 — 시간별체결 정보

class InquireNgtCcnlExecutor(ApiExecutor[InquireNgtCcnlRequest, InquireNgtCcnlResponse]):
    """(야간)선물옵션 주문체결 내역조회 [국내선물-009]."""

    # (야간)선물옵션 주문체결 내역조회 API입니다. 1. 야간 시장이 종료(06:00)된 이후 약 06:10경 야간시장의 주문체결내역이 주간으로 이관됩니다. &gt; 주간 API를 사용한다면 야간 장 중 주문체결내역을 실시간으로 조회할 수 없습니다. &gt; 주문체결내역의 이관이 완료되는 시점부터 주간 테이블에서 야간의 주문체결내역을 조회할 수 있습니다. 2. KRX야간시장의 경우 주문일자는 (T+1)일 입니다. &gt; 금요일의

    PATH = "/uapi/domestic-futureoption/v1/trading/inquire-ngt-ccnl"
    METHOD = "GET"
    RESPONSE_TYPE = InquireNgtCcnlResponse
    TR_ID = "JTCE5005R"
