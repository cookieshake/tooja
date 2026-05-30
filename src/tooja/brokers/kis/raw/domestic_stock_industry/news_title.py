"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class NewsTitleRequest(KisBaseModel):
    """요청."""

    FID_NEWS_OFER_ENTP_CODE: str  # 뉴스 제공 업체 코드 — 공백 필수 입력
    FID_COND_MRKT_CLS_CODE: str  # 조건 시장 구분 코드 — 공백 필수 입력
    FID_INPUT_ISCD: str  # 입력 종목코드 — 공백: 전체, 종목코드 : 해당코드가 등록된 뉴스
    FID_TITL_CNTT: str  # 제목 내용 — 공백 필수 입력
    FID_INPUT_DATE_1: str  # 입력 날짜 — 공백: 현재기준, 조회일자(ex 00YYYYMMDD)
    FID_INPUT_HOUR_1: str  # 입력 시간 — 공백: 현재기준, 조회시간(ex 0000HHMMSS)
    FID_RANK_SORT_CLS_CODE: str  # 순위 정렬 구분 코드 — 공백 필수 입력
    FID_INPUT_SRNO: str  # 입력 일련번호 — 공백 필수 입력

class NewsTitleResponse_OutputItem(KisBaseModel):
    """nested item."""

    cntt_usiq_srno: str | None = None  # 내용 조회용 일련번호
    news_ofer_entp_code: str | None = None  # 뉴스 제공 업체 코드 — '2' /* 한경 news */ '3' /* 사용안함 */ '4' /* 이데일리 */ '5' /* 머니투데이 */ '6' /* 연합뉴스 */ '7' /* 인포스탁 */ '8' /* 아시아경제 */ '9' /* 뉴스핌 */ 'A
    data_dt: str | None = None  # 작성일자
    data_tm: str | None = None  # 작성시간
    hts_pbnt_titl_cntt: str | None = None  # HTS 공시 제목 내용
    news_lrdv_code: str | None = None  # 뉴스 대구분 — 1:0:종합 1:FGHIN:공시 2:F:거래소 3:01:수시공시 3:02:공정공시 3:03:시장조치 3:04:신고사항 3:05:정기공시 3:06:특수공시 3:07:발행공시 3:08:지분공시 3:09:워런트공시 3:10:의결권행사공시 3
    dorg: str | None = None  # 자료원
    iscd1: str | None = None  # 종목 코드1
    iscd2: str | None = None  # 종목 코드2
    iscd3: str | None = None  # 종목 코드3
    iscd4: str | None = None  # 종목 코드4
    iscd5: str | None = None  # 종목 코드5

class NewsTitleResponse(KisCommonResponse):
    """응답 본문."""

    output: NewsTitleResponse_OutputItem | None = None  # 응답상세

class NewsTitleExecutor(ApiExecutor[NewsTitleRequest, NewsTitleResponse]):
    """종합 시황/공시(제목) [국내주식-141]."""

    # 종합 시황/공시(제목) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0601] 종합 시황/공시 화면의 "우측 상단 리스트" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/news-title"
    METHOD = "GET"
    RESPONSE_TYPE = NewsTitleResponse
    TR_ID = "FHKST01011800"
