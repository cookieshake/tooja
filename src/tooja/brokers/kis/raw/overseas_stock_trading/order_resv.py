"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OrderResvRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    SLL_BUY_DVSN_CD: str | None = None  # 매도매수구분코드 — tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 사용 01 : 매도 02 : 매수
    RVSE_CNCL_DVSN_CD: str  # 정정취소구분코드 — tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 사용 00 : "매도/매수 주문"시 필수 항목 02 : 취소
    PDNO: str  # 상품번호
    PRDT_TYPE_CD: str  # 상품유형코드 — tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 사용 515 : 일본 501 : 홍콩 / 543 : 홍콩CNY / 558 : 홍콩USD 507 : 베트남 하노이거래소 / 508 : 베트남 호치민거래소 551 
    OVRS_EXCG_CD: str  # 해외거래소코드 — NASD : 나스닥 NYSE : 뉴욕 AMEX : 아멕스 SEHK : 홍콩 SHAA : 중국상해 SZAA : 중국심천 TKSE : 일본 HASE : 베트남 하노이 VNSE : 베트남 호치민
    FT_ORD_QTY: str  # FT주문수량
    FT_ORD_UNPR3: str  # FT주문단가3
    ORD_SVR_DVSN_CD: str | None = None  # 주문서버구분코드 — "0"(Default)
    RSVN_ORD_RCIT_DT: str | None = None  # 예약주문접수일자 — tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 사용
    ORD_DVSN: str | None = None  # 주문구분 — tr_id가 TTTT3014U(미국 예약 매수 주문)인 경우만 사용 00 : 지정가 35 : TWAP 36 : VWAP tr_id가 TTTT3016U(미국 예약 매도 주문)인 경우만 사용 00 : 지정가 31 : MOO(장개시시장가) 35
    OVRS_RSVN_ODNO: str | None = None  # 해외예약주문번호 — tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 사용
    ALGO_ORD_TMD_DVSN_CD: str | None = None  # 알고리즘주문시간구분코드 — ※ TWAP, VWAP 주문에서만 사용. 예약주문은 시간입력 불가하여 02로 값 고정 ※ 정규장 종료 10분전까지 가능

class OrderResvResponse_OutputItem(KisBaseModel):
    """nested item."""

    ODNO: str | None = None  # 한국거래소전송주문조직번호 — tr_id가 TTTT3016U(미국 예약 매도 주문) / TTTT3014U(미국 예약 매수 주문)인 경우만 출력
    RSVN_ORD_RCIT_DT: str | None = None  # 예약주문접수일자 — tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 출력
    OVRS_RSVN_ODNO: str | None = None  # 해외예약주문번호 — tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 출력

class OrderResvResponse(KisCommonResponse):
    """응답 본문."""

    output: OrderResvResponse_OutputItem | None = None  # 응답상세

class OrderResvExecutor(ApiExecutor[OrderResvRequest, OrderResvResponse]):
    """해외주식 예약주문접수[v1_해외주식-002]."""

    # 미국거래소 운영시간 외 미국주식을 예약 매매하기 위한 API입니다. * 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고) https://securities.koreainvestment.com/main/bond/research/_static/TF03ca010001.jsp ※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다. (EX. "CANO" : "12345678"

    PATH = "/uapi/overseas-stock/v1/trading/order-resv"
    METHOD = "POST"
    RESPONSE_TYPE = OrderResvResponse
    TR_ID = "TTTT3014U"
    TR_ID_VIRTUAL = "VTTT3014U"
