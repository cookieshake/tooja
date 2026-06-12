"""Auto-generated from apiportal spec — do not edit by hand.

NOTE: the KIS spec marks `output` as A0002 (scalar array) even though it has
child rows, so the codegen emitted `list[str]`. Typed to the generated row
item class to match the wire. (generate.py now handles A0002-with-children;
kept here so a regen before the next full review doesn't regress.)
"""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireCcnlRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    PDNO: str  # 상품번호 — 전종목일 경우 "%" 입력 ※ 모의투자계좌의 경우 ""(전체 조회)만 가능
    ORD_STRT_DT: str  # 주문시작일자 — YYYYMMDD 형식 (현지시각 기준)
    ORD_END_DT: str  # 주문종료일자 — YYYYMMDD 형식 (현지시각 기준)
    SLL_BUY_DVSN: str  # 매도매수구분 — 00 : 전체 01 : 매도 02 : 매수 ※ 모의투자계좌의 경우 "00"(전체 조회)만 가능
    CCLD_NCCS_DVSN: str  # 체결미체결구분 — 00 : 전체 01 : 체결 02 : 미체결 ※ 모의투자계좌의 경우 "00"(전체 조회)만 가능
    OVRS_EXCG_CD: str  # 해외거래소코드 — 전종목일 경우 "%" 입력 NASD : 미국시장 전체(나스닥, 뉴욕, 아멕스) NYSE : 뉴욕 AMEX : 아멕스 SEHK : 홍콩 SHAA : 중국상해 SZAA : 중국심천 TKSE : 일본 HASE : 베트남 하노이 VNSE :
    SORT_SQN: str  # 정렬순서 — DS : 정순 AS : 역순 ※ 모의투자계좌의 경우 정렬순서 사용불가(Default : DS(정순))
    ORD_DT: str  # 주문일자 — "" (Null 값 설정)
    ORD_GNO_BRNO: str  # 주문채번지점번호 — "" (Null 값 설정)
    ODNO: str  # 주문번호 — "" (Null 값 설정) ※ 주문번호로 검색 불가능합니다. 반드시 ""(Null 값 설정) 바랍니다.
    CTX_AREA_NK200: str  # 연속조회키200 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200값 : 다음페이지 조회시(2번째부터)
    CTX_AREA_FK200: str  # 연속조회검색조건200 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK200값 : 다음페이지 조회시(2번째부터)

class InquireCcnlResponse_OutputItem(KisBaseModel):
    """nested item."""

    ord_dt: str | None = None  # 주문일자 — 주문접수 일자 (현지시각 기준)
    ord_gno_brno: str | None = None  # 주문채번지점번호 — 계좌 개설 시 관리점으로 선택한 영업점의 고유번호
    odno: str | None = None  # 주문번호 — 접수한 주문의 일련번호 ※ 정정취소주문 시, 해당 값 odno(주문번호) 넣어서 사용
    orgn_odno: str | None = None  # 원주문번호 — 정정 또는 취소 대상 주문의 일련번호
    sll_buy_dvsn_cd: str | None = None  # 매도매수구분코드 — 01 : 매도 02 : 매수
    sll_buy_dvsn_cd_name: str | None = None  # 매도매수구분코드명
    rvse_cncl_dvsn: str | None = None  # 정정취소구분 — 01 : 정정 02 : 취소
    rvse_cncl_dvsn_name: str | None = None  # 정정취소구분명
    pdno: str | None = None  # 상품번호
    prdt_name: str | None = None  # 상품명
    ft_ord_qty: str | None = None  # FT주문수량 — 주문수량
    ft_ord_unpr3: str | None = None  # FT주문단가3 — 주문가격
    ft_ccld_qty: str | None = None  # FT체결수량 — 체결된 수량
    ft_ccld_unpr3: str | None = None  # FT체결단가3 — 체결된 가격
    ft_ccld_amt3: str | None = None  # FT체결금액3 — 체결된 금액
    nccs_qty: str | None = None  # 미체결수량
    prcs_stat_name: str | None = None  # 처리상태명 — 완료, 거부, 전송
    rjct_rson: str | None = None  # 거부사유 — 정상 처리되지 못하고 거부된 주문의 사유
    rjct_rson_name: str | None = None  # 거부사유명
    ord_tmd: str | None = None  # 주문시각 — 주문 접수 시간
    tr_mket_name: str | None = None  # 거래시장명
    tr_natn: str | None = None  # 거래국가
    tr_natn_name: str | None = None  # 거래국가명
    ovrs_excg_cd: str | None = None  # 해외거래소코드 — NASD : 나스닥 NYSE : 뉴욕 AMEX : 아멕스 SEHK : 홍콩 SHAA : 중국상해 SZAA : 중국심천 TKSE : 일본 HASE : 베트남 하노이 VNSE : 베트남 호치민
    tr_crcy_cd: str | None = None  # 거래통화코드
    dmst_ord_dt: str | None = None  # 국내주문일자
    thco_ord_tmd: str | None = None  # 당사주문시각
    loan_type_cd: str | None = None  # 대출유형코드 — 00 : 해당사항없음 01 : 자기융자일반형 03 : 자기융자투자형 05 : 유통융자일반형 06 : 유통융자투자형 07 : 자기대주 09 : 유통대주 10 : 현금 11 : 주식담보대출 12 : 수익증권담보대출 13 : ELS담보대출 
    loan_dt: str | None = None  # 대출일자
    mdia_dvsn_name: str | None = None  # 매체구분명 — ex) OpenAPI, 모바일
    usa_amk_exts_rqst_yn: str | None = None  # 미국애프터마켓연장신청여부 — Y/N
    splt_buy_attr_name: str | None = None  # 분할매수/매도속성명 — 정규장 종료 주문 시에는 '정규장 종료', 시간 입력 시에는 from ~ to 시간 표시

class InquireCcnlResponse(KisCommonResponse):
    """응답 본문."""

    ctx_area_fk200: str | None = None  # 연속조회검색조건200
    ctx_area_nk200: str | None = None  # 연속조회키200
    output: list[InquireCcnlResponse_OutputItem] = []  # 응답상세

class InquireCcnlExecutor(ApiExecutor[InquireCcnlRequest, InquireCcnlResponse]):
    """해외주식 주문체결내역[v1_해외주식-007]."""

    # 일정 기간의 해외주식 주문 체결 내역을 확인하는 API입니다. 실전계좌의 경우, 한 번의 호출에 최대 20건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다. 모의계좌의 경우, 한 번의 호출에 최대 15건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다. * 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고) https://securities.kore

    PATH = "/uapi/overseas-stock/v1/trading/inquire-ccnl"
    METHOD = "GET"
    RESPONSE_TYPE = InquireCcnlResponse
    TR_ID = "TTTS3035R"
    TR_ID_VIRTUAL = "VTTS3035R"
