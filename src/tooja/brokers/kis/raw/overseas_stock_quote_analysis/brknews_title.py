"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class BrknewsTitleRequest(KisBaseModel):
    """요청."""

    FID_NEWS_OFER_ENTP_CODE: str  # 뉴스제공업체코드 — 뉴스제공업체구분=>0:전체조회
    FID_COND_MRKT_CLS_CODE: str  # 조건시장구분코드 — 공백
    FID_INPUT_ISCD: str  # 입력종목코드 — 공백
    FID_TITL_CNTT: str  # 제목내용 — 공백
    FID_INPUT_DATE_1: str  # 입력날짜1 — 공백
    FID_INPUT_HOUR_1: str  # 입력시간1 — 공백
    FID_RANK_SORT_CLS_CODE: str  # 순위정렬구분코드 — 공백
    FID_INPUT_SRNO: str  # 입력일련번호 — 공백
    FID_COND_SCR_DIV_CODE: str  # 조건화면분류코드 — 화면번호:11801

class BrknewsTitleResponse_OutputItem(KisBaseModel):
    """nested item."""

    cntt_usiq_srno: str | None = None  # 내용조회용일련번호
    news_ofer_entp_code: str | None = None  # 뉴스제공업체코드
    data_dt: str | None = None  # 작성일자
    data_tm: str | None = None  # 작성시간
    hts_pbnt_titl_cntt: str | None = None  # HTS공시제목내용
    news_lrdv_code: str | None = None  # 뉴스대구분
    dorg: str | None = None  # 자료원
    iscd1: str | None = None  # 종목코드1
    iscd2: str | None = None  # 종목코드2
    iscd3: str | None = None  # 종목코드3
    iscd4: str | None = None  # 종목코드4
    iscd5: str | None = None  # 종목코드5
    iscd6: str | None = None  # 종목코드6
    iscd7: str | None = None  # 종목코드7
    iscd8: str | None = None  # 종목코드8
    iscd9: str | None = None  # 종목코드9
    iscd10: str | None = None  # 종목코드10
    kor_isnm1: str | None = None  # 한글종목명1
    kor_isnm2: str | None = None  # 한글종목명2
    kor_isnm3: str | None = None  # 한글종목명3
    kor_isnm4: str | None = None  # 한글종목명4
    kor_isnm5: str | None = None  # 한글종목명5
    kor_isnm6: str | None = None  # 한글종목명6
    kor_isnm7: str | None = None  # 한글종목명7
    kor_isnm8: str | None = None  # 한글종목명8
    kor_isnm9: str | None = None  # 한글종목명9
    kor_isnm10: str | None = None  # 한글종목명10

class BrknewsTitleResponse(KisCommonResponse):
    """응답 본문."""

    output: list[BrknewsTitleResponse_OutputItem] = []  # 응답상세 — array

class BrknewsTitleExecutor(ApiExecutor[BrknewsTitleRequest, BrknewsTitleResponse]):
    """해외속보(제목) [해외주식-055]."""

    # 해외속보(제목) API입니다. 한국투자 HTS(eFriend Plus) &gt; [7704] 해외속보 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 최대 100건까지 조회 가능합니다.

    PATH = "/uapi/overseas-price/v1/quotations/brknews-title"
    METHOD = "GET"
    RESPONSE_TYPE = BrknewsTitleResponse
    TR_ID = "FHKST01011801"
