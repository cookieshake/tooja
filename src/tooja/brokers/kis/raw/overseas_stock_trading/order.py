"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OrderRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    OVRS_EXCG_CD: str  # 해외거래소코드 — NASD : 나스닥 NYSE : 뉴욕 AMEX : 아멕스 SEHK : 홍콩 SHAA : 중국상해 SZAA : 중국심천 TKSE : 일본 HASE : 베트남 하노이 VNSE : 베트남 호치민
    PDNO: str  # 상품번호 — 종목코드
    ORD_QTY: str  # 주문수량 — 주문수량 (해외거래소 별 최소 주문수량 및 주문단위 확인 필요)
    OVRS_ORD_UNPR: str  # 해외주문단가 — 1주당 가격 * 시장가의 경우 1주당 가격을 공란으로 비우지 않음 "0"으로 입력
    CTAC_TLNO: str | None = None  # 연락전화번호
    MGCO_APTM_ODNO: str | None = None  # 운용사지정주문번호
    SLL_TYPE: str | None = None  # 판매유형 — 제거 : 매수 00 : 매도
    ORD_SVR_DVSN_CD: str  # 주문서버구분코드 — "0"(Default)
    ORD_DVSN: str  # 주문구분 — [Header tr_id TTTT1002U(미국 매수 주문)] 00 : 지정가 32 : LOO(장개시지정가) 34 : LOC(장마감지정가) 35 : TWAP (시간가중평균) 36 : VWAP (거래량가중평균) * 모의투자 VTTT1002U
    START_TIME: str | None = None  # 시작시간 — ※ TWAP, VWAP 주문유형이고 알고리즘주문시간구분코드가 00일때 사용 ※ YYMMDD 형태로 입력 ※ 시간 입력 시 정규장 종료 5분전까지 입력 가능
    END_TIME: str | None = None  # 종료시간 — ※ TWAP, VWAP 주문유형이고 알고리즘주문시간구분코드가 00일때 사용 ※ YYMMDD 형태로 입력 ※ 시간 입력 시 정규장 종료 5분전까지 입력 가능
    ALGO_ORD_TMD_DVSN_CD: str | None = None  # 알고리즘주문시간구분코드 — 00 : 분할주문 시간 직접입력 , 02 : 정규장 종료시까지

class OrderResponse_OutputItem(KisBaseModel):
    """nested item."""

    KRX_FWDG_ORD_ORGNO: str | None = None  # 한국거래소전송주문조직번호 — 주문시 한국투자증권 시스템에서 지정된 영업점코드
    ODNO: str | None = None  # 주문번호 — 주문시 한국투자증권 시스템에서 채번된 주문번호
    ORD_TMD: str | None = None  # 주문시각 — 주문시각(시분초HHMMSS)

class OrderResponse(KisCommonResponse):
    """응답 본문."""

    output: OrderResponse_OutputItem | None = None  # 응답상세

class OrderExecutor(ApiExecutor[OrderRequest, OrderResponse]):
    """해외주식 주문[v1_해외주식-001]."""

    # 해외주식 주문 API입니다. * 모의투자의 경우, 모든 해외 종목 매매가 지원되지 않습니다. 일부 종목만 매매 가능한 점 유의 부탁드립니다. * 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고) https://securities.koreainvestment.com/main/bond/research/_static/TF03ca010001.jsp * 해외 거래소 운영시간 외 API 호출 시 에러가

    PATH = "/uapi/overseas-stock/v1/trading/order"
    METHOD = "POST"
    RESPONSE_TYPE = OrderResponse
    TR_ID = "TTTT1002U"
    TR_ID_VIRTUAL = "VTTT1002U"
