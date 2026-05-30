"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class NewHighlowRequest(KisBaseModel):
    """요청."""

    KEYB: str  # NEXT KEY BUFF — 공백
    AUTH: str  # 사용자권한정보 — 공백
    EXCD: str  # 거래소코드 — 'NYS : 뉴욕, NAS : 나스닥, AMS : 아멕스 HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 '
    GUBN: str  # 신고/신저 구분 — 신고(1) 신저(0)
    GUBN2: str  # 일시돌파/돌파 구분 — 일시돌파(0) 돌파유지(1)
    NDAY: str  # N일자값 — N일전 : 0(5일), 1(10일), 2(20일), 3(30일), 4(60일), 5(120일전), 6(52주), 7(1년)
    VOL_RANG: str  # 거래량조건 — 0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)

class NewHighlowResponse_Output1Item(KisBaseModel):
    """nested item."""

    zdiv: str | None = None  # 소수점자리수
    stat: str | None = None  # 거래상태정보
    nrec: str | None = None  # RecordCount

class NewHighlowResponse_Output2Item(KisBaseModel):
    """nested item."""

    rsym: str | None = None  # 실시간조회심볼
    excd: str | None = None  # 거래소코드
    symb: str | None = None  # 종목코드
    name: str | None = None  # 종목명
    last: str | None = None  # 현재가
    sign: str | None = None  # 기호
    diff: str | None = None  # 대비
    rate: str | None = None  # 등락율
    tvol: str | None = None  # 거래량
    pask: str | None = None  # 매도호가
    pbid: str | None = None  # 매수호가
    n_base: str | None = None  # 기준가
    n_diff: str | None = None  # 기준가대비
    n_rate: str | None = None  # 기준가대비율
    ename: str | None = None  # 영문종목명
    e_ordyn: str | None = None  # 매매가능

class NewHighlowResponse(KisCommonResponse):
    """응답 본문."""

    output1: NewHighlowResponse_Output1Item | None = None  # 응답상세
    output2: list[NewHighlowResponse_Output2Item] = []  # 응답상세 — array

class NewHighlowExecutor(ApiExecutor[NewHighlowRequest, NewHighlowResponse]):
    """해외주식 신고/신저가[해외주식-042]."""

    # "해외주식 신고/신저가 API입니다. 한국투자 HTS(eFriend Plus) &gt; [7630] 신고/신저가 화면 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다."

    PATH = "/uapi/overseas-stock/v1/ranking/new-highlow"
    METHOD = "GET"
    RESPONSE_TYPE = NewHighlowResponse
    TR_ID = "HHDFS76300000"
