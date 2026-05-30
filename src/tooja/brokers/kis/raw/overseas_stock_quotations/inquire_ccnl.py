"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireCcnlRequest(KisBaseModel):
    """요청."""

    EXCD: str  # 거래소명 — 'NYS : 뉴욕, NAS : 나스닥, AMS : 아멕스 HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 '
    AUTH: str  # 사용자권한정보 — 공백
    KEYB: str  # NEXT KEY BUFF — 공백
    TDAY: str  # 당일전일구분 — 0:전일, 1:당일
    SYMB: str  # 종목코드 — 해외종목코드

class InquireCcnlResponse_Output2Item(KisBaseModel):
    """nested item."""

    khms: str | None = None  # 한국기준시간
    last: str | None = None  # 체결가
    sign: str | None = None  # 기호
    diff: str | None = None  # 대비
    rate: str | None = None  # 등락율
    evol: str | None = None  # 체결량
    tvol: str | None = None  # 거래량
    mtyp: str | None = None  # 시장구분 — 0: 장중 1:장전 2:장후
    pbid: str | None = None  # 매수호가
    pask: str | None = None  # 매도호가
    vpow: str | None = None  # 체결강도

class InquireCcnlResponse_Output1Item(KisBaseModel):
    """nested item."""

    rsym: str | None = None  # 실시간조회종목코드
    ZDIV: str | None = None  # 소수점자리수
    NREC: str | None = None  # Record Count

class InquireCcnlResponse(KisCommonResponse):
    """응답 본문."""

    output2: list[InquireCcnlResponse_Output2Item] = []  # 응답상세 — array
    output1: InquireCcnlResponse_Output1Item | None = None  # 응답상세

class InquireCcnlExecutor(ApiExecutor[InquireCcnlRequest, InquireCcnlResponse]):
    """해외주식 체결추이[해외주식-037]."""

    # 해외주식 체결추이 API입니다. 한국투자 HTS(eFriend Plus) &gt; [7625] 해외주식 체결추이 화면 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/overseas-price/v1/quotations/inquire-ccnl"
    METHOD = "GET"
    RESPONSE_TYPE = InquireCcnlResponse
    TR_ID = "HHDFS76200300"
