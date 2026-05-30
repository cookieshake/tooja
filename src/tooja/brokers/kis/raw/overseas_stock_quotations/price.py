"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class PriceRequest(KisBaseModel):
    """요청."""

    AUTH: str  # 사용자권한정보 — "" (Null 값 설정)
    EXCD: str  # 거래소코드 — HKS : 홍콩 NYS : 뉴욕 NAS : 나스닥 AMS : 아멕스 TSE : 도쿄 SHS : 상해 SZS : 심천 SHI : 상해지수 SZI : 심천지수 HSX : 호치민 HNX : 하노이 BAY : 뉴욕(주간) BAQ : 나스닥(주간
    SYMB: str  # 종목코드

class PriceResponse_OutputItem(KisBaseModel):
    """nested item."""

    rsym: str | None = None  # 실시간조회종목코드 — D+시장구분(3자리)+종목코드 예) DNASAAPL : D+NAS(나스닥)+AAPL(애플) [시장구분] NYS : 뉴욕, NAS : 나스닥, AMS : 아멕스 , TSE : 도쿄, HKS : 홍콩, SHS : 상해, SZS : 심
    zdiv: str | None = None  # 소수점자리수
    base: str | None = None  # 전일종가 — 전일의 종가
    pvol: str | None = None  # 전일거래량 — 전일의 거래량
    last: str | None = None  # 현재가 — 당일 조회시점의 현재 가격
    sign: str | None = None  # 대비기호 — 1 : 상한 2 : 상승 3 : 보합 4 : 하한 5 : 하락
    diff: str | None = None  # 대비 — 전일 종가와 당일 현재가의 차이 (당일 현재가-전일 종가)
    rate: str | None = None  # 등락율 — 전일 대비 / 당일 현재가 * 100
    tvol: str | None = None  # 거래량 — 당일 조회시점까지 전체 거래량
    tamt: str | None = None  # 거래대금 — 당일 조회시점까지 전체 거래금액
    ordy: str | None = None  # 매수가능여부 — 매수주문 가능 종목 여부

class PriceResponse(KisCommonResponse):
    """응답 본문."""

    output: PriceResponse_OutputItem | None = None  # 응답상세

class PriceExecutor(ApiExecutor[PriceRequest, PriceResponse]):
    """해외주식 현재체결가[v1_해외주식-009]."""

    # 해외주식종목의 현재체결가를 확인하는 API 입니다. 해외주식 시세는 무료시세(지연시세)만이 제공되며, API로는 유료시세(실시간시세)를 받아보실 수 없습니다. ※ 지연시세 지연시간 : 미국 - 실시간무료(0분 지연, 나스닥 마켓센터에서 거래되는 호가 및 호가 잔량 정보) 홍콩, 베트남, 중국, 일본 - 15분지연 미국의 경우 0분 지연 시세로 제공되나, 장중 당일 시가는 상이할 수 있으며, 익일 정정 표시됩니다. [미국주식시세

    PATH = "/uapi/overseas-price/v1/quotations/price"
    METHOD = "GET"
    RESPONSE_TYPE = PriceResponse
    TR_ID = "HHDFS00000300"
