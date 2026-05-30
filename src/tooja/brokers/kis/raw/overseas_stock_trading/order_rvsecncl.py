"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OrderRvsecnclRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    OVRS_EXCG_CD: str  # 해외거래소코드 — NASD : 나스닥 NYSE : 뉴욕 AMEX : 아멕스 SEHK : 홍콩 SHAA : 중국상해 SZAA : 중국심천 TKSE : 일본 HASE : 베트남 하노이 VNSE : 베트남 호치민
    PDNO: str  # 상품번호
    ORGN_ODNO: str  # 원주문번호 — 정정 또는 취소할 원주문번호 (해외주식_주문 API ouput ODNO or 해외주식 미체결내역 API output ODNO 참고)
    RVSE_CNCL_DVSN_CD: str  # 정정취소구분코드 — 01 : 정정 02 : 취소
    ORD_QTY: str  # 주문수량
    OVRS_ORD_UNPR: str  # 해외주문단가 — 취소주문 시, "0" 입력
    MGCO_APTM_ODNO: str | None = None  # 운용사지정주문번호
    ORD_SVR_DVSN_CD: str | None = None  # 주문서버구분코드 — "0"(Default)

class OrderRvsecnclResponse_OutputItem(KisBaseModel):
    """nested item."""

    KRX_FWDG_ORD_ORGNO: str | None = None  # 한국거래소전송주문조직번호 — 주문시 한국투자증권 시스템에서 지정된 영업점코드
    ODNO: str | None = None  # 주문번호 — 주문시 한국투자증권 시스템에서 채번된 주문번호
    ORD_TMD: str | None = None  # 주문시각 — 주문시각(시분초HHMMSS)

class OrderRvsecnclResponse(KisCommonResponse):
    """응답 본문."""

    output: OrderRvsecnclResponse_OutputItem | None = None  # 응답상세

class OrderRvsecnclExecutor(ApiExecutor[OrderRvsecnclRequest, OrderRvsecnclResponse]):
    """해외주식 정정취소주문[v1_해외주식-003]."""

    # 접수된 해외주식 주문을 정정하거나 취소하기 위한 API입니다. (해외주식주문 시 Return 받은 ODNO를 참고하여 API를 호출하세요.) * 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고) https://securities.koreainvestment.com/main/bond/research/_static/TF03ca010001.jsp * 해외 거래소 운영시간 외 API 호출 시 에러가

    PATH = "/uapi/overseas-stock/v1/trading/order-rvsecncl"
    METHOD = "POST"
    RESPONSE_TYPE = OrderRvsecnclResponse
    TR_ID = "TTTT1004U"
    TR_ID_VIRTUAL = "VTTT1004U"
