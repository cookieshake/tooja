"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class PriceFluctRequest(KisBaseModel):
    """요청."""

    KEYB: str  # NEXT KEY BUFF — 공백
    AUTH: str  # 사용자권한정보 — 공백
    EXCD: str  # 거래소코드 — 'NYS : 뉴욕, NAS : 나스닥, AMS : 아멕스 HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 '
    GUBN: str  # 급등/급락구분 — 0(급락), 1(급등)
    MINX: str  # N분전콤보값 — N분전 : 0(1분전), 1(2분전), 2(3분전), 3(5분전), 4(10분전), 5(15분전), 6(20분전), 7(30분전), 8(60분전), 9(120분전)
    VOL_RANG: str  # 거래량조건 — 0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)

class PriceFluctResponse_Output1Item(KisBaseModel):
    """nested item."""

    zdiv: str | None = None  # 소수점자리수
    stat: str | None = None  # 거래상태
    nrec: str | None = None  # RecordCount

class PriceFluctResponse_Output2Item(KisBaseModel):
    """nested item."""

    rsym: str | None = None  # 실시간조회심볼
    excd: str | None = None  # 거래소코드
    symb: str | None = None  # 종목코드
    knam: str | None = None  # 종목명
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
    enam: str | None = None  # 영문종목명
    e_ordyn: str | None = None  # 매매가능

class PriceFluctResponse(KisCommonResponse):
    """응답 본문."""

    output1: PriceFluctResponse_Output1Item | None = None  # 응답상세
    output2: list[PriceFluctResponse_Output2Item] = []  # 응답상세 — array

class PriceFluctExecutor(ApiExecutor[PriceFluctRequest, PriceFluctResponse]):
    """해외주식 가격급등락[해외주식-038]."""

    # 해외주식 가격급등락 API입니다. 한국투자 HTS(eFriend Plus) &gt; [7626] 가격급등락 화면 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/overseas-stock/v1/ranking/price-fluct"
    METHOD = "GET"
    RESPONSE_TYPE = PriceFluctResponse
    TR_ID = "HHDFS76260000"
