"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class DailypriceRequest(KisBaseModel):
    """요청."""

    AUTH: str  # 사용자권한정보 — "" (Null 값 설정)
    EXCD: str  # 거래소코드 — HKS : 홍콩 NYS : 뉴욕 NAS : 나스닥 AMS : 아멕스 TSE : 도쿄 SHS : 상해 SZS : 심천 SHI : 상해지수 SZI : 심천지수 HSX : 호치민 HNX : 하노이
    SYMB: str  # 종목코드 — 종목코드 (ex. TSLA)
    GUBN: str  # 일/주/월구분 — 0 : 일 1 : 주 2 : 월
    BYMD: str  # 조회기준일자 — 조회기준일자(YYYYMMDD) ※ 공란 설정 시, 기준일 오늘 날짜로 설정
    MODP: str  # 수정주가반영여부 — 0 : 미반영 1 : 반영
    KEYB: str | None = None  # NEXT KEY BUFF — 응답시 다음값이 있으면 값이 셋팅되어 있으므로 다음 조회시 응답값 그대로 셋팅

class DailypriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    rsym: str | None = None  # 실시간조회종목코드 — D+시장구분(3자리)+종목코드 예) DNASAAPL : D+NAS(나스닥)+AAPL(애플) [시장구분] NYS : 뉴욕, NAS : 나스닥, AMS : 아멕스 , TSE : 도쿄, HKS : 홍콩, SHS : 상해, SZS : 심
    zdiv: str | None = None  # 소수점자리수
    nrec: str | None = None  # 전일종가

class DailypriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    xymd: str | None = None  # 일자(YYYYMMDD)
    clos: str | None = None  # 종가 — 해당 일자의 종가
    sign: str | None = None  # 대비기호 — 1 : 상한 2 : 상승 3 : 보합 4 : 하한 5 : 하락
    diff: str | None = None  # 대비 — 해당 일자의 종가와 해당 전일 종가의 차이 (해당일 종가-해당 전일 종가)
    rate: str | None = None  # 등락율 — 해당 전일 대비 / 해당일 종가 * 100
    open: str | None = None  # 시가 — 해당일 최초 거래가격
    high: str | None = None  # 고가 — 해당일 가장 높은 거래가격
    low: str | None = None  # 저가 — 해당일 가장 낮은 거래가격
    tvol: str | None = None  # 거래량 — 해당일 거래량
    tamt: str | None = None  # 거래대금 — 해당일 거래대금
    pbid: str | None = None  # 매수호가 — 마지막 체결이 발생한 시점의 매수호가 * 해당 일자 거래량 0인 경우 값이 수신되지 않음
    vbid: str | None = None  # 매수호가잔량 — * 해당 일자 거래량 0인 경우 값이 수신되지 않음
    pask: str | None = None  # 매도호가 — 마지막 체결이 발생한 시점의 매도호가 * 해당 일자 거래량 0인 경우 값이 수신되지 않음
    vask: str | None = None  # 매도호가잔량 — * 해당 일자 거래량 0인 경우 값이 수신되지 않음

class DailypriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: DailypriceResponse_Output1Item | None = None  # 응답상세1
    output2: list[DailypriceResponse_Output2Item] = []  # 응답상세2

class DailypriceExecutor(ApiExecutor[DailypriceRequest, DailypriceResponse]):
    """해외주식 기간별시세[v1_해외주식-010]."""

    # 해외주식의 기간별시세를 확인하는 API 입니다. 실전계좌/모의계좌의 경우, 한 번의 호출에 최대 100건까지 확인 가능합니다. 해외주식 시세는 무료시세(지연체결가)만이 제공되며, API로는 유료시세(실시간체결가)를 받아보실 수 없습니다. 해외주식 시세는 무료시세(지연시세)만이 제공되며, API로는 유료시세(실시간시세)를 받아보실 수 없습니다. ※ 지연시세 지연시간 : 미국 - 실시간무료(0분 지연, 나스닥 마켓센터에서 거래되는

    PATH = "/uapi/overseas-price/v1/quotations/dailyprice"
    METHOD = "GET"
    RESPONSE_TYPE = DailypriceResponse
    TR_ID = "HHDFS76240000"
