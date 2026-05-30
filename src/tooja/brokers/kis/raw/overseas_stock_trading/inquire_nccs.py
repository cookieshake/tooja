"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireNccsRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    OVRS_EXCG_CD: str  # 해외거래소코드 — NASD : 나스닥 NYSE : 뉴욕 AMEX : 아멕스 SEHK : 홍콩 SHAA : 중국상해 SZAA : 중국심천 TKSE : 일본 HASE : 베트남 하노이 VNSE : 베트남 호치민 * NASD 인 경우만 미국전체로 조회되며 
    SORT_SQN: str  # 정렬순서 — DS : 정순 그외 : 역순 [header tr_id: TTTS3018R] ""(공란)
    CTX_AREA_FK200: str  # 연속조회검색조건200 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK200값 : 다음페이지 조회시(2번째부터)
    CTX_AREA_NK200: str  # 연속조회키200 — 공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200값 : 다음페이지 조회시(2번째부터)

class InquireNccsResponse_OutputItem(KisBaseModel):
    """nested item."""

    ord_dt: str | None = None  # 주문일자 — 주문접수 일자
    ord_gno_brno: str | None = None  # 주문채번지점번호 — 계좌 개설 시 관리점으로 선택한 영업점의 고유번호
    odno: str | None = None  # 주문번호 — 접수한 주문의 일련번호
    orgn_odno: str | None = None  # 원주문번호 — 정정 또는 취소 대상 주문의 일련번호
    pdno: str | None = None  # 상품번호 — 종목코드
    prdt_name: str | None = None  # 상품명 — 종목명
    sll_buy_dvsn_cd: str | None = None  # 매도매수구분코드 — 01 : 매도 02 : 매수
    sll_buy_dvsn_cd_name: str | None = None  # 매도매수구분코드명 — 매수매도구분명
    rvse_cncl_dvsn_cd: str | None = None  # 정정취소구분코드 — 01 : 정정 02 : 취소
    rvse_cncl_dvsn_cd_name: str | None = None  # 정정취소구분코드명 — 정정취소구분명
    rjct_rson: str | None = None  # 거부사유 — 정상 처리되지 못하고 거부된 주문의 사유
    rjct_rson_name: str | None = None  # 거부사유명 — 정상 처리되지 못하고 거부된 주문의 사유명
    ord_tmd: str | None = None  # 주문시각 — 주문 접수 시간
    tr_mket_name: str | None = None  # 거래시장명
    tr_crcy_cd: str | None = None  # 거래통화코드 — USD : 미국달러 HKD : 홍콩달러 CNY : 중국위안화 JPY : 일본엔화 VND : 베트남동
    natn_cd: str | None = None  # 국가코드
    natn_kor_name: str | None = None  # 국가한글명
    ft_ord_qty: str | None = None  # FT주문수량 — 주문수량
    ft_ccld_qty: str | None = None  # FT체결수량 — 체결된 수량
    nccs_qty: str | None = None  # 미체결수량
    ft_ord_unpr3: str | None = None  # FT주문단가3 — 주문가격
    ft_ccld_unpr3: str | None = None  # FT체결단가3 — 체결된 가격
    ft_ccld_amt3: str | None = None  # FT체결금액3 — 체결된 금액
    ovrs_excg_cd: str | None = None  # 해외거래소코드 — NASD : 나스닥 NYSE : 뉴욕 AMEX : 아멕스 SEHK : 홍콩 SHAA : 중국상해 SZAA : 중국심천 TKSE : 일본 HASE : 베트남 하노이 VNSE : 베트남 호치민
    prcs_stat_name: str | None = None  # 처리상태명 — ""
    loan_type_cd: str | None = None  # 대출유형코드 — 00 해당사항없음 01 자기융자일반형 03 자기융자투자형 05 유통융자일반형 06 유통융자투자형 07 자기대주 09 유통대주 10 현금 11 주식담보대출 12 수익증권담보대출 13 ELS담보대출 14 채권담보대출 15 해외주식담보대출 
    loan_dt: str | None = None  # 대출일자 — 대출 실행일자
    usa_amk_exts_rqst_yn: str | None = None  # 미국애프터마켓연장신청여부 — Y/N
    splt_buy_attr_name: str | None = None  # 분할매수속성명 — 정규장 종료 주문 시에는 '정규장 종료', 시간 입력 시에는 from ~ to 시간 표시됨

class InquireNccsResponse(KisCommonResponse):
    """응답 본문."""

    ctx_area_fk200: str | None = None  # 연속조회검색조건200
    ctx_area_nk200: str | None = None  # 연속조회키200
    output: list[str] = []  # 응답상세

class InquireNccsExecutor(ApiExecutor[InquireNccsRequest, InquireNccsResponse]):
    """해외주식 미체결내역[v1_해외주식-005]."""

    # 접수된 해외주식 주문 중 체결되지 않은 미체결 내역을 조회하는 API입니다. 실전계좌의 경우, 한 번의 호출에 최대 40건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다. ※ 해외주식 미체결내역 API 모의투자에서는 사용이 불가합니다. 모의투자로 해외주식 미체결내역 확인시에는 해외주식 주문체결내역[v1_해외주식-007] API 조회하셔서 nccs_qty(미체결수량)으로 해외주식 미체결수량을 조회하실 수 

    PATH = "/uapi/overseas-stock/v1/trading/inquire-nccs"
    METHOD = "GET"
    RESPONSE_TYPE = InquireNccsResponse
    TR_ID = "TTTS3018R"
