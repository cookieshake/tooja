"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class DividendRateRequest(KisBaseModel):
    """요청."""

    CTS_AREA: str  # CTS_AREA — 공백
    GB1: str  # KOSPI — 0:전체, 1:코스피, 2: 코스피200, 3: 코스닥,
    UPJONG: str  # 업종구분 — '코스피(0001:종합, 0002:대형주.…0027:제조업 ), 코스닥(1001:종합, …. 1041:IT부품 코스피200 (2001:KOSPI200, 2007:KOSPI100, 2008:KOSPI50)'
    GB2: str  # 종목선택 — 0:전체, 6:보통주, 7:우선주
    GB3: str  # 배당구분 — 1:주식배당, 2: 현금배당
    F_DT: str  # 기준일From
    T_DT: str  # 기준일To
    GB4: str  # 결산/중간배당 — 0:전체, 1:결산배당, 2:중간배당

class DividendRateResponse_Output1Item(KisBaseModel):
    """nested item."""

    rank: str | None = None  # 순위
    sht_cd: str | None = None  # 종목코드
    isin_name: str | None = None  # 종목명
    record_date: str | None = None  # 기준일
    per_sto_divi_amt: str | None = None  # 현금/주식배당금
    divi_rate: str | None = None  # 현금/주식배당률(%)
    divi_kind: str | None = None  # 배당종류

class DividendRateResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[DividendRateResponse_Output1Item] = []  # 응답상세 — array

class DividendRateExecutor(ApiExecutor[DividendRateRequest, DividendRateResponse]):
    """국내주식 배당률 상위[국내주식-106]."""

    # 국내주식 배당률 상위 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0188] 배당률 상위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 최대 30건 확인 가능하며, 다음 조회가 불가합니다. ※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다. 종목조건검색 API는 

    PATH = "/uapi/domestic-stock/v1/ranking/dividend-rate"
    METHOD = "GET"
    RESPONSE_TYPE = DividendRateResponse
    TR_ID = "HHKDB13470100"
