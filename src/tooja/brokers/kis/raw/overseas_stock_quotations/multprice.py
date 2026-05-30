"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class MultpriceRequest(KisBaseModel):
    """요청."""

    AUTH: str  # 사용자권한정보 — 공백 입력 필수
    NREC: str  # 종목요청개수 — 최대 10
    EXCD_01___10: str  # 거래소코드 — HKS : 홍콩 NYS : 뉴욕 NAS : 나스닥 AMS : 아멕스 TSE : 도쿄 SHS : 상해 SZS : 심천 SHI : 상해지수 SZI : 심천지수 HSX : 호치민 HNX : 하노이 BAY : 뉴욕(주간) BAQ : 나스닥(주간
    SYMB_01___10: str  # 종목코드 — API 문서 -> 종목정보파일 -> 마스터 파일 참조

class MultpriceResponse_OutputItem(KisBaseModel):
    """nested item."""

    nrec: str | None = None  # Output 개수

class MultpriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    rsym: str | None = None  # 실시간조회심볼
    excd: str | None = None  # 거래소코드
    symb: str | None = None  # 종목코드
    knam: str | None = None  # 종목명
    exnm: str | None = None  # 거래소명
    nnam: str | None = None  # 국가명
    stat1: str | None = None  # 실 지 휴 정 재
    stat2: str | None = None  # 실시간 지연15분 휴장 거래정지 거래재개
    zdiv: str | None = None  # 소수점자리수
    last: str | None = None  # Last Price
    sign: str | None = None  # 대비기호
    diff: str | None = None  # 대비
    rate: str | None = None  # 등락율
    open: str | None = None  # 시가
    high: str | None = None  # 고가
    low: str | None = None  # 저가
    pbid: str | None = None  # Bid Price
    pask: str | None = None  # Ask Price
    vbid: str | None = None  # 매수호가잔량
    vask: str | None = None  # 매도호가잔량
    bvol: str | None = None  # 매수호가총잔량
    avol: str | None = None  # 매도호가총잔량
    evol: str | None = None  # 체결량
    tvol: str | None = None  # 거래량
    tamt: str | None = None  # 거래대금
    powx: str | None = None  # 체결강도
    xhms: str | None = None  # 현지기준시간(HHMMSS)
    khms: str | None = None  # 한국기준시간(HHMMSS)
    curr: str | None = None  # 통화코드
    base: str | None = None  # Base Price
    pvol: str | None = None  # Previous Volume
    pamt: str | None = None  # 전일거래대금
    popen: str | None = None  # 전일시가
    phigh: str | None = None  # 전일고가
    plow: str | None = None  # 전일저가
    shar: str | None = None  # 상장주수
    mcap: str | None = None  # 자본금
    tomv: str | None = None  # 시가총액
    h52p: str | None = None  # 52주최고가
    l52p: str | None = None  # 52주최저가
    h52d: str | None = None  # 52주최고일자
    l52d: str | None = None  # 52주최저일자
    hanp: str | None = None  # High Anual Price
    lanp: str | None = None  # Low Anual Price
    hand: str | None = None  # 연중최고일자
    land: str | None = None  # 연중최저일자
    bnit: str | None = None  # 매매단위
    t_xprc: str | None = None  # 원환산당일가격

class MultpriceResponse(KisCommonResponse):
    """응답 본문."""

    output: MultpriceResponse_OutputItem | None = None  # 응답상세
    output2: list[MultpriceResponse_Output2Item] = []  # 응답상세 — Array

class MultpriceExecutor(ApiExecutor[MultpriceRequest, MultpriceResponse]):
    """해외주식 복수종목 시세조회."""

    # ※ 지연시세 지연시간 : 미국 - 실시간무료(0분 지연, 나스닥 마켓센터에서 거래되는 호가 및 호가 잔량 정보) 홍콩, 베트남, 중국, 일본 - 15분지연 미국의 경우 0분 지연 시세로 제공되나, 장중 당일 시가는 상이할 수 있으며, 익일 정정 표시됩니다. [미국주식시세 이용시 유의사항] ■ 무료 실시간 시세(나스닥 토탈뷰)를 별도 신청없이 제공하고 있으며, 유료 시세 서비스를 신청하시더라도 OpenAPI의 경우 무료 시세로만

    PATH = "/uapi/overseas-price/v1/quotations/multprice"
    METHOD = "GET"
    RESPONSE_TYPE = MultpriceResponse
    TR_ID = "HHDFS76220000"
