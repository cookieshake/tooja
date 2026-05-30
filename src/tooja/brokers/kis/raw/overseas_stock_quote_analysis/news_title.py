"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class NewsTitleRequest(KisBaseModel):
    """요청."""

    INFO_GB: str  # 뉴스구분 — 전체: 공백
    CLASS_CD: str  # 중분류 — 전체: 공백
    NATION_CD: str  # 국가코드 — 전체: 공백 CN(중국), HK(홍콩), US(미국)
    EXCHANGE_CD: str  # 거래소코드 — 전체: 공백
    SYMB: str  # 종목코드 — 전체: 공백
    DATA_DT: str  # 조회일자 — 전체: 공백 특정일자(YYYYMMDD) ex. 20240502
    DATA_TM: str  # 조회시간 — 전체: 공백 전체: 공백 특정시간(HHMMSS) ex. 093500
    CTS: str  # 다음키 — 공백 입력

class NewsTitleResponse_Outblock1Item(KisBaseModel):
    """nested item."""

    info_gb: str | None = None  # 뉴스구분
    news_key: str | None = None  # 뉴스키
    data_dt: str | None = None  # 조회일자
    data_tm: str | None = None  # 조회시간
    class_cd: str | None = None  # 중분류
    class_name: str | None = None  # 중분류명
    source: str | None = None  # 자료원
    nation_cd: str | None = None  # 국가코드
    exchange_cd: str | None = None  # 거래소코드
    symb: str | None = None  # 종목코드
    symb_name: str | None = None  # 종목명
    title: str | None = None  # 제목

class NewsTitleResponse(KisCommonResponse):
    """응답 본문."""

    outblock1: list[NewsTitleResponse_Outblock1Item] = []  # 응답상세 — array

class NewsTitleExecutor(ApiExecutor[NewsTitleRequest, NewsTitleResponse]):
    """해외뉴스종합(제목) [해외주식-053]."""

    # 해외뉴스종합(제목) API입니다. 한국투자 HTS(eFriend Plus) &gt; [7702] 해외뉴스종합 화면의 "우측 상단 뉴스목록" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/overseas-price/v1/quotations/news-title"
    METHOD = "GET"
    RESPONSE_TYPE = NewsTitleResponse
    TR_ID = "HHPSTH60100C1"
