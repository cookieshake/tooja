"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OrderResvListRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    INQR_STRT_DT: str  # 조회시작일자 — 조회시작일자(YYYYMMDD)
    INQR_END_DT: str  # 조회종료일자 — 조회종료일자(YYYYMMDD)
    INQR_DVSN_CD: str  # 조회구분코드 — 00 : 전체 01 : 일반해외주식 02 : 미니스탁
    PRDT_TYPE_CD: str  # 상품유형코드 — [tr_id=TTTT3039R인 경우] 공백 입력 시 미국주식 전체조회 [tr_id=TTTS3014R인 경우] 공백 입력 시 아시아주식 전체조회 512 : 미국 나스닥 / 513 : 미국 뉴욕거래소 / 529 : 미국 아멕스 515 :
    OVRS_EXCG_CD: str  # 해외거래소코드 — [tr_id=TTTT3039R인 경우] 공백 입력 시 미국주식 전체조회 [tr_id=TTTS3014R인 경우] 공백 입력 시 아시아주식 전체조회 NASD : 나스닥 / NYSE : 뉴욕 / AMEX : 아멕스 SEHK : 홍콩 / S
    CTX_AREA_FK200: str  # 연속조회검색조건200 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK200값 : 다음페이지 조회시(2번째부터)
    CTX_AREA_NK200: str  # 연속조회키200 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200값 : 다음페이지 조회시(2번째부터)

class OrderResvListResponse_OutputItem(KisBaseModel):
    """nested item."""

    cncl_yn: str | None = None  # 취소여부
    rsvn_ord_rcit_dt: str | None = None  # 예약주문접수일자
    ovrs_rsvn_odno: str | None = None  # 해외예약주문번호
    ord_dt: str | None = None  # 주문일자
    ord_gno_brno: str | None = None  # 주문채번지점번호
    odno: str | None = None  # 주문번호
    sll_buy_dvsn_cd: str | None = None  # 매도매수구분코드
    sll_buy_dvsn_cd_name: str | None = None  # 매도매수구분명
    ovrs_rsvn_ord_stat_cd: str | None = None  # 해외예약주문상태코드
    ovrs_rsvn_ord_stat_cd_name: str | None = None  # 해외예약주문상태코드명
    pdno: str | None = None  # 상품번호
    prdt_type_cd: str | None = None  # 상품유형코드
    prdt_name: str | None = None  # 상품명
    ord_rcit_tmd: str | None = None  # 주문접수시각
    ord_fwdg_tmd: str | None = None  # 주문전송시각
    tr_dvsn_name: str | None = None  # 거래구분명
    ovrs_excg_cd: str | None = None  # 해외거래소코드
    tr_mket_name: str | None = None  # 거래시장명
    ord_stfno: str | None = None  # 주문직원번호
    ft_ord_qty: str | None = None  # FT주문수량
    ft_ord_unpr3: str | None = None  # FT주문단가3
    ft_ccld_qty: str | None = None  # FT체결수량
    nprc_rson_text: str | None = None  # 미처리사유내용
    splt_buy_attr_name: str | None = None  # 분할매수속성명 — 정규장 종료 주문 시에는 '정규장 종료', 시간 입력 시에는 from ~ to 시간 표시

class OrderResvListResponse(KisCommonResponse):
    """응답 본문."""

    ctx_area_fk200: str | None = None  # 연속조회검색조건200
    ctx_area_nk200: str | None = None  # 연속조회키200
    output: OrderResvListResponse_OutputItem | None = None  # 응답상세1

class OrderResvListExecutor(ApiExecutor[OrderResvListRequest, OrderResvListResponse]):
    """해외주식 예약주문조회[v1_해외주식-013]."""

    # 해외주식 예약주문 조회 API입니다. ※ 모의투자는 사용 불가합니다. * 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고) https://securities.koreainvestment.com/main/bond/research/_static/TF03ca010001.jsp

    PATH = "/uapi/overseas-stock/v1/trading/order-resv-list"
    METHOD = "GET"
    RESPONSE_TYPE = OrderResvListResponse
    TR_ID = "TTTT3039R"
