"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireAskingPriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # FID 조건 시장 분류 코드 — F: 지수선물, O:지수옵션 JF: 주식선물, JO:주식옵션 CF: 상품선물(금), 금리선물(국채), 통화선물(달러) CM: 야간선물, EU: 야간옵션
    FID_INPUT_ISCD: str  # FID 입력 종목코드 — 종목코드 (예: 101S03)

class InquireAskingPriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    hts_kor_isnm: str | None = None  # HTS 한글 종목명 — 종목명
    futs_prpr: str | None = None  # 선물 현재가 — 선물의 현재가격
    prdy_vrss_sign: str | None = None  # 전일 대비 부호 — 1 : 상한 2 : 상승 3 : 보합 4 : 하한 5 : 하락
    futs_prdy_vrss: str | None = None  # 선물 전일 대비 — 선물의 전일 종가와 당일 현재가의 차이 (당일 현재가-전일 종가)
    futs_prdy_ctrt: str | None = None  # 선물 전일 대비율 — 선물 전일 대비 / 당일 현재가 * 100
    acml_vol: str | None = None  # 누적 거래량 — 당일 조회시점까지 전체 거래량
    futs_prdy_clpr: str | None = None  # 선물 전일 종가 — 해당 선물 종목의 전일 종가
    futs_shrn_iscd: str | None = None  # 선물 단축 종목코드

class InquireAskingPriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    futs_askp1: str | None = None  # 선물 매도호가1 — 해당 종목의 매도호가 중 1번째 낮은 호가
    futs_askp2: str | None = None  # 선물 매도호가2 — 해당 종목의 매도호가 중 2번째 낮은 호가
    futs_askp3: str | None = None  # 선물 매도호가3 — 해당 종목의 매도호가 중 3번째 낮은 호가
    futs_askp4: str | None = None  # 선물 매도호가4 — 해당 종목의 매도호가 중 4번째 낮은 호가
    futs_askp5: str | None = None  # 선물 매도호가5 — 해당 종목의 매도호가 중 5번째 낮은 호가
    futs_bidp1: str | None = None  # 선물 매수호가1 — 해당 종목의 매수호가 중 가장 높은 호가
    futs_bidp2: str | None = None  # 선물 매수호가1 — 해당 종목의 매수호가 중 2번째 높은 호가
    futs_bidp3: str | None = None  # 선물 매수호가3 — 해당 종목의 매수호가 중 3번째 높은 호가
    futs_bidp4: str | None = None  # 선물 매수호가4 — 해당 종목의 매수호가 중 4번째 높은 호가
    futs_bidp5: str | None = None  # 선물 매수호가5 — 해당 종목의 매수호가 중 5번째 높은 호가
    askp_rsqn1: str | None = None  # 매도호가 잔량1 — 매도호가 1의 미체결수량
    askp_rsqn2: str | None = None  # 매도호가 잔량2 — 매도호가 2의 미체결수량
    askp_rsqn3: str | None = None  # 매도호가 잔량3 — 매도호가 3의 미체결수량
    askp_rsqn4: str | None = None  # 매도호가 잔량4 — 매도호가 4의 미체결수량
    askp_rsqn5: str | None = None  # 매도호가 잔량5 — 매도호가 5의 미체결수량
    bidp_rsqn1: str | None = None  # 매수호가 잔량1 — 매수호가 1의 미체결수량
    bidp_rsqn2: str | None = None  # 매수호가 잔량2 — 매수호가 2의 미체결수량
    bidp_rsqn3: str | None = None  # 매수호가 잔량3 — 매수호가 3의 미체결수량
    bidp_rsqn4: str | None = None  # 매수호가 잔량4 — 매수호가 4의 미체결수량
    bidp_rsqn5: str | None = None  # 매수호가 잔량5 — 매수호가 5의 미체결수량
    askp_csnu1: str | None = None  # 매도호가 건수1 — 매도호가 1의 미체결 주문 건수
    askp_csnu2: str | None = None  # 매도호가 건수2 — 매도호가 2의 미체결 주문 건수
    askp_csnu3: str | None = None  # 매도호가 건수3 — 매도호가 3의 미체결 주문 건수
    askp_csnu4: str | None = None  # 매도호가 건수4 — 매도호가 4의 미체결 주문 건수
    askp_csnu5: str | None = None  # 매도호가 건수5 — 매도호가 5의 미체결 주문 건수
    bidp_csnu1: str | None = None  # 매수호가 건수1 — 매수호가 1의 미체결 주문 건수
    bidp_csnu2: str | None = None  # 매수호가 건수2 — 매수호가 2의 미체결 주문 건수
    bidp_csnu3: str | None = None  # 매수호가 건수3 — 매수호가 3의 미체결 주문 건수
    bidp_csnu4: str | None = None  # 매수호가 건수4 — 매수호가 4의 미체결 주문 건수
    bidp_csnu5: str | None = None  # 매수호가 건수5 — 매수호가 5의 미체결 주문 건수
    total_askp_rsqn: str | None = None  # 총 매도호가 잔량 — 매도호가 1~5의 잔량 합계
    total_bidp_rsqn: str | None = None  # 총 매수호가 잔량 — 매수호가 1~5의 잔량 합계
    total_askp_csnu: str | None = None  # 총 매도호가 건수 — 매도호가 1~5의 미체결 주문 건수 합계
    total_bidp_csnu: str | None = None  # 총 매수호가 건수 — 매수호가 1~5의 미체결 주문 건수 합계
    aspr_acpt_hour: str | None = None  # 호가 접수 시간 — 가장 최근 호가의 접수 시간

class InquireAskingPriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireAskingPriceResponse_Output1Item | None = None  # 응답상세1
    output2: list[InquireAskingPriceResponse_Output2Item] = []  # 응답상세2 — Array

class InquireAskingPriceExecutor(ApiExecutor[InquireAskingPriceRequest, InquireAskingPriceResponse]):
    """선물옵션 시세호가[v1_국내선물-007]."""

    # 선물옵션 시세호가 API입니다.

    PATH = "/uapi/domestic-futureoption/v1/quotations/inquire-asking-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquireAskingPriceResponse
    TR_ID = "FHMIF10010000"
