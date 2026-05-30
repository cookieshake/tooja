"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class DaytimeOrderRvsecnclRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호 — 계좌번호 체계(8-2)의 앞 8자리
    ACNT_PRDT_CD: str  # 계좌상품코드 — 계좌번호 체계(8-2)의 뒤 2자리
    OVRS_EXCG_CD: str  # 해외거래소코드 — NASD:나스닥 / NYSE:뉴욕 / AMEX:아멕스
    PDNO: str  # 상품번호 — 종목코드
    ORGN_ODNO: str  # 원주문번호 — '정정 또는 취소할 원주문번호(매매 TR의 주문번호) - 해외주식 주문체결내역api (/uapi/overseas-stock/v1/trading/inquire-nccs)에서 odno(주문번호) 참조'
    RVSE_CNCL_DVSN_CD: str  # 정정취소구분코드 — '01 : 정정 02 : 취소'
    ORD_QTY: str  # 주문수량
    OVRS_ORD_UNPR: str  # 해외주문단가 — 소수점 포함, 1주당 가격
    CTAC_TLNO: str  # 연락전화번호 — " "
    MGCO_APTM_ODNO: str  # 운용사지정주문번호 — " "
    ORD_SVR_DVSN_CD: str  # 주문서버구분코드 — "0"

class DaytimeOrderRvsecnclResponse_OutputItem(KisBaseModel):
    """nested item."""

    KRX_FWDG_ORD_ORGNO: str | None = None  # 한국거래소전송주문조직번호 — 주문시 한국투자증권 시스템에서 지정된 영업점코드
    ODNO: str | None = None  # 주문번호 — 주문시 한국투자증권 시스템에서 채번된 주문번호
    ORD_TMD: str | None = None  # 주문시각 — 주문시각(시분초HHMMSS)

class DaytimeOrderRvsecnclResponse(KisCommonResponse):
    """응답 본문."""

    output: DaytimeOrderRvsecnclResponse_OutputItem | None = None  # 응답상세

class DaytimeOrderRvsecnclExecutor(ApiExecutor[DaytimeOrderRvsecnclRequest, DaytimeOrderRvsecnclResponse]):
    """해외주식 미국주간정정취소[v1_해외주식-027]."""

    # 해외주식 미국주간정정취소 API입니다. * 미국주식 주간거래 시 아래 참고 부탁드립니다. . 포럼 &gt; FAQ &gt; 미국주식 주간거래 시 어떤 API를 사용해야 하나요? * 미국주간거래의 경우, 모든 미국 종목 매매가 지원되지 않습니다. 일부 종목만 매매 가능한 점 유의 부탁드립니다. * 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고) https://securities.koreain

    PATH = "/uapi/overseas-stock/v1/trading/daytime-order-rvsecncl"
    METHOD = "POST"
    RESPONSE_TYPE = DaytimeOrderRvsecnclResponse
    TR_ID = "TTTS6038U"
