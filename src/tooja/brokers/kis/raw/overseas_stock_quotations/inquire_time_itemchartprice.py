"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireTimeItemchartpriceRequest(KisBaseModel):
    """요청."""

    AUTH: str  # 사용자권한정보 — "" 공백으로 입력
    EXCD: str  # 거래소코드 — NYS : 뉴욕 NAS : 나스닥 AMS : 아멕스 HKS : 홍콩 SHS : 상해 SZS : 심천 HSX : 호치민 HNX : 하노이 TSE : 도쿄 ※ 주간거래는 최대 1일치 분봉만 조회 가능 BAY : 뉴욕(주간) BAQ : 나스닥
    SYMB: str  # 종목코드 — 종목코드(ex. TSLA)
    NMIN: str  # 분갭 — 분단위(1: 1분봉, 2: 2분봉, ...)
    PINC: str  # 전일포함여부 — 0:당일 1:전일포함 ※ 다음조회 시 반드시 "1"로 입력
    NEXT: str  # 다음여부 — 처음조회 시, "" 공백 입력 다음조회 시, "1" 입력
    NREC: str  # 요청갯수 — 레코드요청갯수 (최대 120)
    FILL: str  # 미체결채움구분 — "" 공백으로 입력
    KEYB: str  # NEXT KEY BUFF — 처음 조회 시, "" 공백 입력 다음 조회 시, 이전 조회 결과의 마지막 분봉 데이터를 이용하여, 1분 전 혹은 n분 전의 시간을 입력 (형식: YYYYMMDDHHMMSS, ex. 20241014140100)

class InquireTimeItemchartpriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    rsym: str | None = None  # 실시간종목코드
    zdiv: str | None = None  # 소수점자리수
    stim: str | None = None  # 장시작현지시간
    etim: str | None = None  # 장종료현지시간
    sktm: str | None = None  # 장시작한국시간
    ektm: str | None = None  # 장종료한국시간
    next: str | None = None  # 다음가능여부
    more: str | None = None  # 추가데이타여부
    nrec: str | None = None  # 레코드갯수

class InquireTimeItemchartpriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    tymd: str | None = None  # 현지영업일자
    xymd: str | None = None  # 현지기준일자
    xhms: str | None = None  # 현지기준시간
    kymd: str | None = None  # 한국기준일자
    khms: str | None = None  # 한국기준시간
    open: str | None = None  # 시가
    high: str | None = None  # 고가
    low: str | None = None  # 저가
    last: str | None = None  # 종가
    evol: str | None = None  # 체결량
    eamt: str | None = None  # 체결대금

class InquireTimeItemchartpriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[InquireTimeItemchartpriceResponse_Output1Item] = []  # 응답상세
    output2: InquireTimeItemchartpriceResponse_Output2Item | None = None  # 응답상세2 — array

class InquireTimeItemchartpriceExecutor(ApiExecutor[InquireTimeItemchartpriceRequest, InquireTimeItemchartpriceResponse]):
    """해외주식분봉조회[v1_해외주식-030]."""

    # 해외주식분봉조회 API입니다. 실전계좌의 경우, 한 번의 호출에 최근 120건까지 확인 가능합니다. NEXT 및 KEYB 값을 사용하여 데이터를 계속해서 다음 조회할 수 있으며, 최대 다음조회 가능 기간은 약 1개월입니다. ※ 해외주식분봉조회 조회 방법 params . 초기 조회: - PINC: "1" 입력 - NEXT: 처음 조회 시, "" 공백 입력 - KEYB: 처음 조회 시, "" 공백 입력 . 다음 조회: - PINC

    PATH = "/uapi/overseas-price/v1/quotations/inquire-time-itemchartprice"
    METHOD = "GET"
    RESPONSE_TYPE = InquireTimeItemchartpriceResponse
    TR_ID = "HHDFS76950200"
