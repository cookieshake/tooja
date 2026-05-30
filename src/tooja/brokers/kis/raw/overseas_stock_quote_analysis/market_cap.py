"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class MarketCapRequest(KisBaseModel):
    """요청."""

    KEYB: str  # NEXT KEY BUFF — 공백
    AUTH: str  # 사용자권한정보 — 공백
    EXCD: str  # 거래소코드 — 'NYS : 뉴욕, NAS : 나스닥, AMS : 아멕스 HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 '
    VOL_RANG: str  # 거래량조건 — 0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)

class MarketCapResponse_Output1Item(KisBaseModel):
    """nested item."""

    zdiv: str | None = None  # 소수점자리수
    stat: str | None = None  # 거래상태정보
    crec: str | None = None  # 현재조회종목수
    trec: str | None = None  # 전체조회종목수
    nrec: str | None = None  # RecordCount

class MarketCapResponse_Output2Item(KisBaseModel):
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
    shar: str | None = None  # 상장주식수
    tomv: str | None = None  # 시가총액
    grav: str | None = None  # 비중
    rank: str | None = None  # 순위
    ename: str | None = None  # 영문종목명
    e_ordyn: str | None = None  # 매매가능

class MarketCapResponse(KisCommonResponse):
    """응답 본문."""

    output1: MarketCapResponse_Output1Item | None = None  # 응답상세
    output2: list[MarketCapResponse_Output2Item] = []  # 응답상세 — array

class MarketCapExecutor(ApiExecutor[MarketCapRequest, MarketCapResponse]):
    """해외주식 시가총액순위[해외주식-047]."""

    # 해외주식 시가총액순위 API입니다. 한국투자 HTS(eFriend Plus) &gt; [7635] 시가총액순위 화면 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/overseas-stock/v1/ranking/market-cap"
    METHOD = "GET"
    RESPONSE_TYPE = MarketCapResponse
    TR_ID = "HHDFS76350100"
