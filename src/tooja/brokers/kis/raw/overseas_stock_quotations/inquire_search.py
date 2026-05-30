"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireSearchRequest(KisBaseModel):
    """요청."""

    AUTH: str  # 사용자권한정보 — "" (Null 값 설정)
    EXCD: str  # 거래소코드 — NYS : 뉴욕, NAS : 나스닥, AMS : 아멕스 HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄
    CO_YN_PRICECUR: str | None = None  # 현재가선택조건 — 해당조건 사용시(1), 미사용시 필수항목아님
    CO_ST_PRICECUR: str | None = None  # 현재가시작범위가 — 단위: 각국통화(JPY, USD, HKD, CNY, VND)
    CO_EN_PRICECUR: str | None = None  # 현재가끝범위가 — 단위: 각국통화(JPY, USD, HKD, CNY, VND)
    CO_YN_RATE: str | None = None  # 등락율선택조건 — 해당조건 사용시(1), 미사용시 필수항목아님
    CO_ST_RATE: str | None = None  # 등락율시작율 — %
    CO_EN_RATE: str | None = None  # 등락율끝율 — %
    CO_YN_VALX: str | None = None  # 시가총액선택조건 — 해당조건 사용시(1), 미사용시 필수항목아님
    CO_ST_VALX: str | None = None  # 시가총액시작액 — 단위: 천
    CO_EN_VALX: str | None = None  # 시가총액끝액 — 단위: 천
    CO_YN_SHAR: str | None = None  # 발행주식수선택조건 — 해당조건 사용시(1), 미사용시 필수항목아님
    CO_ST_SHAR: str | None = None  # 발행주식시작수 — 단위: 천
    CO_EN_SHAR: str | None = None  # 발행주식끝수 — 단위: 천
    CO_YN_VOLUME: str | None = None  # 거래량선택조건 — 해당조건 사용시(1), 미사용시 필수항목아님
    CO_ST_VOLUME: str | None = None  # 거래량시작량 — 단위: 주
    CO_EN_VOLUME: str | None = None  # 거래량끝량 — 단위: 주
    CO_YN_AMT: str | None = None  # 거래대금선택조건 — 해당조건 사용시(1), 미사용시 필수항목아님
    CO_ST_AMT: str | None = None  # 거래대금시작금 — 단위: 천
    CO_EN_AMT: str | None = None  # 거래대금끝금 — 단위: 천
    CO_YN_EPS: str | None = None  # EPS선택조건 — 해당조건 사용시(1), 미사용시 필수항목아님
    CO_ST_EPS: str | None = None  # EPS시작
    CO_EN_EPS: str | None = None  # EPS끝
    CO_YN_PER: str | None = None  # PER선택조건 — 해당조건 사용시(1), 미사용시 필수항목아님
    CO_ST_PER: str | None = None  # PER시작
    CO_EN_PER: str | None = None  # PER끝
    KEYB: str | None = None  # NEXT KEY BUFF — "" 공백 입력

class InquireSearchResponse_Output1Item(KisBaseModel):
    """nested item."""

    zdiv: str | None = None  # 소수점자리수
    stat: str | None = None  # 거래상태정보
    crec: str | None = None  # 현재조회종목수
    trec: str | None = None  # 전체조회종목수
    nrec: str | None = None  # Record Count

class InquireSearchResponse_Output2Item(KisBaseModel):
    """nested item."""

    rsym: str | None = None  # 실시간조회심볼 — 실시간조회심볼 D+시장구분(3자리)+종목코드 예) DNASAAPL : D+NAS(나스닥)+AAPL(애플) [시장구분] NYS : 뉴욕, NAS : 나스닥, AMS : 아멕스 , TSE : 도쿄, HKS : 홍콩, SHS : 상해, S
    excd: str | None = None  # 거래소코드
    name: str | None = None  # 종목명
    symb: str | None = None  # 종목코드
    last: str | None = None  # 현재가
    shar: str | None = None  # 발행주식 — 발행주식수(단위: 천)
    valx: str | None = None  # 시가총액 — 시가총액(단위: 천)
    plow: str | None = None  # 저가
    phigh: str | None = None  # 고가
    popen: str | None = None  # 시가
    tvol: str | None = None  # 거래량 — 거래량(단위: 주)
    rate: str | None = None  # 등락율 — 등락율(%)
    diff: str | None = None  # 대비
    sign: str | None = None  # 기호
    avol: str | None = None  # 거래대금 — 거래대금(단위: 천)
    eps: str | None = None  # EPS
    per: str | None = None  # PER
    rank: str | None = None  # 순위
    ename: str | None = None  # 영문종목명
    e_ordyn: str | None = None  # 매매가능 — 가능 : O

class InquireSearchResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireSearchResponse_Output1Item | None = None  # 응답상세1
    output2: list[InquireSearchResponse_Output2Item] = []  # 응답상세2 — 조회결과 상세

class InquireSearchExecutor(ApiExecutor[InquireSearchRequest, InquireSearchResponse]):
    """해외주식조건검색[v1_해외주식-015]."""

    # 해외주식 조건검색 API입니다. 한국투자 HTS(eFriend Plus) &gt; [7641] 해외주식 조건검색 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 현재 조건검색 결과값은 최대 100개까지 조회 가능합니다. 다음 조회(100개 이후의 값) 기능에 대해서는 개선검토 중에 있습니다. ※ 지연시세 지연시간 : 미국 - 실시간무료(0분지연) / 홍콩, 베트남, 중국, 일본 - 1

    PATH = "/uapi/overseas-price/v1/quotations/inquire-search"
    METHOD = "GET"
    RESPONSE_TYPE = InquireSearchResponse
    TR_ID = "HHDFS76410000"
