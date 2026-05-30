"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class UpdownRateRequest(KisBaseModel):
    """요청."""

    KEYB: str  # NEXT KEY BUFF — 공백
    AUTH: str  # 사용자권한정보 — 공백
    EXCD: str  # 거래소코드 — 'NYS : 뉴욕, NAS : 나스닥, AMS : 아멕스 HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 '
    GUBN: str  # 상승율/하락율 구분 — 0(하락율), 1(상승율)
    NDAY: str  # N일자값 — N일전 : 0(당일), 1(2일), 2(3일), 3(5일), 4(10일), 5(20일전), 6(30일), 7(60일), 8(120일), 9(1년)
    VOL_RANG: str  # 거래량조건 — 0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)

class UpdownRateResponse_Output1Item(KisBaseModel):
    """nested item."""

    zdiv: str | None = None  # 소수점자리수
    stat: str | None = None  # 거래상태정보
    crec: str | None = None  # 현재Count
    trec: str | None = None  # 전체조회종목수
    nrec: str | None = None  # RecordCount

class UpdownRateResponse_Output2Item(KisBaseModel):
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
    n_base: str | None = None  # 기준가격
    n_diff: str | None = None  # 기준가격대비
    n_rate: str | None = None  # 기준가격대비율
    rank: str | None = None  # 순위
    ename: str | None = None  # 영문종목명
    e_ordyn: str | None = None  # 매매가능

class UpdownRateResponse(KisCommonResponse):
    """응답 본문."""

    output1: UpdownRateResponse_Output1Item | None = None  # 응답상세
    output2: list[UpdownRateResponse_Output2Item] = []  # 응답상세 — array

class UpdownRateExecutor(ApiExecutor[UpdownRateRequest, UpdownRateResponse]):
    """해외주식 상승율/하락율[해외주식-041]."""

    # 해외주식 상승율/하락율 API입니다. 한국투자 HTS(eFriend Plus) &gt; [7629] 상승율/하락율 화면 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/overseas-stock/v1/ranking/updown-rate"
    METHOD = "GET"
    RESPONSE_TYPE = UpdownRateResponse
    TR_ID = "HHDFS76290000"
