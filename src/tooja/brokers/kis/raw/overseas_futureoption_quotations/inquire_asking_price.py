"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireAskingPriceRequest(KisBaseModel):
    """요청."""

    SRS_CD: str  # 종목명 — 종목코드

class InquireAskingPriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    open_price: str | None = None  # 시가
    high_price: str | None = None  # 고가
    lowp_rice: str | None = None  # 저가
    last_price: str | None = None  # 현재가
    prev_price: str | None = None  # 전일종가
    vol: str | None = None  # 거래량
    prev_diff_price: str | None = None  # 전일대비가
    prev_diff_rate: str | None = None  # 전일대비율
    quot_date: str | None = None  # 호가수신일자
    quot_time: str | None = None  # 호가수신시각

class InquireAskingPriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    bid_qntt: str | None = None  # 매수수량
    bid_num: str | None = None  # 매수번호
    bid_price: str | None = None  # 매수호가
    ask_qntt: str | None = None  # 매도수량
    ask_num: str | None = None  # 매도번호
    ask_price: str | None = None  # 매도호가

class InquireAskingPriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireAskingPriceResponse_Output1Item | None = None  # 응답상세
    output2: list[InquireAskingPriceResponse_Output2Item] = []  # 응답상세 — array

class InquireAskingPriceExecutor(ApiExecutor[InquireAskingPriceRequest, InquireAskingPriceResponse]):
    """해외선물 호가 [해외선물-031]."""

    # 해외선물 호가 API입니다. 한국투자 HTS(eFriend Plus) &gt; [8602] 해외선물옵션 종합주문(Ⅰ) 화면에서 "왼쪽 호가 창" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. (중요) 해외선물옵션시세 출력값을 해석하실 때 ffcode.mst(해외선물종목마스터 파일)에 있는 sCalcDesz(계산 소수점) 값을 활용하셔야 정확한 값을 받아오실 수 있습니다. - ffcode.m

    PATH = "/uapi/overseas-futureoption/v1/quotations/inquire-asking-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquireAskingPriceResponse
    TR_ID = "HHDFC86000000"
