"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireAskingPriceRequest(KisBaseModel):
    """요청."""

    AUTH: str  # 사용자권한정보 — 공백
    EXCD: str  # 거래소코드 — NYS : 뉴욕 NAS : 나스닥 AMS : 아멕스 HKS : 홍콩 SHS : 상해 SZS : 심천 HSX : 호치민 HNX : 하노이 TSE : 도쿄 BAY : 뉴욕(주간) BAQ : 나스닥(주간) BAA : 아멕스(주간)
    SYMB: str  # 종목코드 — 종목코드 예)TSLA

class InquireAskingPriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    rsym: str | None = None  # 실시간조회종목코드
    zdiv: str | None = None  # 소수점자리수
    curr: str | None = None  # 통화
    base: str | None = None  # 전일종가
    open: str | None = None  # 시가
    high: str | None = None  # 고가
    low: str | None = None  # 저가
    last: str | None = None  # 현재가
    dymd: str | None = None  # 호가일자
    dhms: str | None = None  # 호가시간
    bvol: str | None = None  # 매수호가총잔량
    avol: str | None = None  # 매도호가총잔량
    bdvl: str | None = None  # 매수호가총잔량대비
    advl: str | None = None  # 매도호가총잔량대비
    code: str | None = None  # 종목코드
    ropen: str | None = None  # 시가율
    rhigh: str | None = None  # 고가율
    rlow: str | None = None  # 저가율
    rclose: str | None = None  # 현재가율

class InquireAskingPriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    pbid1: str | None = None  # 매수호가가격1
    pask1: str | None = None  # 매도호가가격1
    vbid1: str | None = None  # 매수호가잔량1
    vask1: str | None = None  # 매도호가잔량1
    dbid1: str | None = None  # 매수호가대비1
    dask1: str | None = None  # 매도호가대비1
    pbid2: str | None = None  # 매수호가가격2 — 미국 거래소만 수신
    pask2: str | None = None  # 매도호가가격2 — 미국 거래소만 수신
    vbid2: str | None = None  # 매수호가잔량2 — 미국 거래소만 수신
    vask2: str | None = None  # 매도호가잔량2 — 미국 거래소만 수신
    dbid2: str | None = None  # 매수호가대비2 — 미국 거래소만 수신
    dask2: str | None = None  # 매도호가대비2 — 미국 거래소만 수신
    pbid3: str | None = None  # 매수호가가격3 — 미국 거래소만 수신
    pask3: str | None = None  # 매도호가가격3 — 미국 거래소만 수신
    vbid3: str | None = None  # 매수호가잔량3 — 미국 거래소만 수신
    vask3: str | None = None  # 매도호가잔량3 — 미국 거래소만 수신
    dbid3: str | None = None  # 매수호가대비3 — 미국 거래소만 수신
    dask3: str | None = None  # 매도호가대비3 — 미국 거래소만 수신
    pbid4: str | None = None  # 매수호가가격4 — 미국 거래소만 수신
    pask4: str | None = None  # 매도호가가격4 — 미국 거래소만 수신
    vbid4: str | None = None  # 매수호가잔량4 — 미국 거래소만 수신
    vask4: str | None = None  # 매도호가잔량4 — 미국 거래소만 수신
    dbid4: str | None = None  # 매수호가대비4 — 미국 거래소만 수신
    dask4: str | None = None  # 매도호가대비4 — 미국 거래소만 수신
    pbid5: str | None = None  # 매수호가가격5 — 미국 거래소만 수신
    pask5: str | None = None  # 매도호가가격5 — 미국 거래소만 수신
    vbid5: str | None = None  # 매수호가잔량5 — 미국 거래소만 수신
    vask5: str | None = None  # 매도호가잔량5 — 미국 거래소만 수신
    dbid5: str | None = None  # 매수호가대비5 — 미국 거래소만 수신
    dask5: str | None = None  # 매도호가대비5 — 미국 거래소만 수신
    pbid6: str | None = None  # 매수호가가격6 — 미국 거래소만 수신
    pask6: str | None = None  # 매도호가가격6 — 미국 거래소만 수신
    vbid6: str | None = None  # 매수호가잔량6 — 미국 거래소만 수신
    vask6: str | None = None  # 매도호가잔량6 — 미국 거래소만 수신
    dbid6: str | None = None  # 매수호가대비6 — 미국 거래소만 수신
    dask6: str | None = None  # 매도호가대비6 — 미국 거래소만 수신
    pbid7: str | None = None  # 매수호가가격7 — 미국 거래소만 수신
    pask7: str | None = None  # 매도호가가격7 — 미국 거래소만 수신
    vbid7: str | None = None  # 매수호가잔량7 — 미국 거래소만 수신
    vask7: str | None = None  # 매도호가잔량7 — 미국 거래소만 수신
    dbid7: str | None = None  # 매수호가대비7 — 미국 거래소만 수신
    dask7: str | None = None  # 매도호가대비7 — 미국 거래소만 수신
    pbid8: str | None = None  # 매수호가가격8 — 미국 거래소만 수신
    pask8: str | None = None  # 매도호가가격8 — 미국 거래소만 수신
    vbid8: str | None = None  # 매수호가잔량8 — 미국 거래소만 수신
    vask8: str | None = None  # 매도호가잔량8 — 미국 거래소만 수신
    dbid8: str | None = None  # 매수호가대비8 — 미국 거래소만 수신
    dask8: str | None = None  # 매도호가대비8 — 미국 거래소만 수신
    pbid9: str | None = None  # 매수호가가격9 — 미국 거래소만 수신
    pask9: str | None = None  # 매도호가가격9 — 미국 거래소만 수신
    vbid9: str | None = None  # 매수호가잔량9 — 미국 거래소만 수신
    vask9: str | None = None  # 매도호가잔량9 — 미국 거래소만 수신
    dbid9: str | None = None  # 매수호가대비9 — 미국 거래소만 수신
    dask9: str | None = None  # 매도호가대비9 — 미국 거래소만 수신
    pbid10: str | None = None  # 매수호가가격10 — 미국 거래소만 수신
    pask10: str | None = None  # 매도호가가격10 — 미국 거래소만 수신
    vbid10: str | None = None  # 매수호가잔량10 — 미국 거래소만 수신
    vask10: str | None = None  # 매도호가잔량10 — 미국 거래소만 수신
    dbid10: str | None = None  # 매수호가대비10 — 미국 거래소만 수신
    dask10: str | None = None  # 매도호가대비10 — 미국 거래소만 수신

class InquireAskingPriceResponse_Output3Item(KisBaseModel):
    """nested item."""

    vstm: str | None = None  # VCMStart시간 — 데이터 없음
    vetm: str | None = None  # VCMEnd시간 — 데이터 없음
    csbp: str | None = None  # CAS/VCM기준가 — 데이터 없음
    cshi: str | None = None  # CAS/VCMHighprice — 데이터 없음
    cslo: str | None = None  # CAS/VCMLowprice — 데이터 없음
    iep: str | None = None  # IEP — 데이터 없음
    iev: str | None = None  # IEV — 데이터 없음

class InquireAskingPriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireAskingPriceResponse_Output1Item | None = None  # 응답상세
    output2: list[str] = []  # 응답상세
    output3: list[InquireAskingPriceResponse_Output3Item] = []  # 응답상세

class InquireAskingPriceExecutor(ApiExecutor[InquireAskingPriceRequest, InquireAskingPriceResponse]):
    """해외주식 현재가 호가 [해외주식-033]."""

    # 해외주식 현재가 호가 API입니다. 미국 거래소는 10호가, 그 외 국가 거래소는 1호가만 제공됩니다. 한국투자 HTS(eFriend Plus) &gt; [7620] 해외주식 현재가 화면에서 "왼쪽 호가 창" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 해외주식 시세는 무료시세(지연시세)만이 제공되며, API로는 유료시세(실시간시세)를 받아보실 수 없습니다. ※ 지연시세 지연시간 : 미국

    PATH = "/uapi/overseas-price/v1/quotations/inquire-asking-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquireAskingPriceResponse
    TR_ID = "HHDFS76200100"
