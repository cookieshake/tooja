"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireAskingPriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — B: 장내
    FID_INPUT_ISCD: str  # 입력 종목코드 — 채권종목코드 ex. KR2088012A16

class InquireAskingPriceResponse_OutputItem(KisBaseModel):
    """nested item."""

    aspr_acpt_hour: str | None = None  # 호가 접수 시간
    bond_askp1: str | None = None  # 채권 매도호가1
    bond_askp2: str | None = None  # 채권 매도호가2
    bond_askp3: str | None = None  # 채권 매도호가3
    bond_askp4: str | None = None  # 채권 매도호가4
    bond_askp5: str | None = None  # 채권 매도호가5
    bond_bidp1: str | None = None  # 채권 매수호가1
    bond_bidp2: str | None = None  # 채권 매수호가2
    bond_bidp3: str | None = None  # 채권 매수호가3
    bond_bidp4: str | None = None  # 채권 매수호가4
    bond_bidp5: str | None = None  # 채권 매수호가5
    askp_rsqn1: str | None = None  # 매도호가 잔량1
    askp_rsqn2: str | None = None  # 매도호가 잔량2
    askp_rsqn3: str | None = None  # 매도호가 잔량3
    askp_rsqn4: str | None = None  # 매도호가 잔량4
    askp_rsqn5: str | None = None  # 매도호가 잔량5
    bidp_rsqn1: str | None = None  # 매수호가 잔량1
    bidp_rsqn2: str | None = None  # 매수호가 잔량2
    bidp_rsqn3: str | None = None  # 매수호가 잔량3
    bidp_rsqn4: str | None = None  # 매수호가 잔량4
    bidp_rsqn5: str | None = None  # 매수호가 잔량5
    total_askp_rsqn: str | None = None  # 총 매도호가 잔량
    total_bidp_rsqn: str | None = None  # 총 매수호가 잔량
    ntby_aspr_rsqn: str | None = None  # 순매수 호가 잔량
    seln_ernn_rate1: str | None = None  # 매도 수익 비율1
    seln_ernn_rate2: str | None = None  # 매도 수익 비율2
    seln_ernn_rate3: str | None = None  # 매도 수익 비율3
    seln_ernn_rate4: str | None = None  # 매도 수익 비율4
    seln_ernn_rate5: str | None = None  # 매도 수익 비율5
    shnu_ernn_rate1: str | None = None  # 매수2 수익 비율1
    shnu_ernn_rate2: str | None = None  # 매수2 수익 비율2
    shnu_ernn_rate3: str | None = None  # 매수2 수익 비율3
    shnu_ernn_rate4: str | None = None  # 매수2 수익 비율4
    shnu_ernn_rate5: str | None = None  # 매수2 수익 비율5

class InquireAskingPriceResponse(KisCommonResponse):
    """응답 본문."""

    output: InquireAskingPriceResponse_OutputItem | None = None  # 응답상세

class InquireAskingPriceExecutor(ApiExecutor[InquireAskingPriceRequest, InquireAskingPriceResponse]):
    """장내채권현재가(호가) [국내주식-132]."""

    # 장내채권현재가(호가) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0978] 장내채권주문 "우측 호가창" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-bond/v1/quotations/inquire-asking-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquireAskingPriceResponse
    TR_ID = "FHKBJ773401C0"
