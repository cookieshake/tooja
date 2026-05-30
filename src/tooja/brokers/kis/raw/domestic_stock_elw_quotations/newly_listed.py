"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class NewlyListedRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — 시장구분코드 (W)
    FID_COND_SCR_DIV_CODE: str  # 조건화면분류코드 — Unique key(11548)
    FID_DIV_CLS_CODE: str  # 분류구분코드 — 전체(02), 콜(00), 풋(01)
    FID_UNAS_INPUT_ISCD: str  # 기초자산입력종목코드 — 'ex) 000000(전체), 2001(코스피200) , 3003(코스닥150), 005930(삼성전자) '
    FID_INPUT_ISCD_2: str  # 입력종목코드2 — '00003(한국투자증권), 00017(KB증권), 00005(미래에셋증권)'
    FID_INPUT_DATE_1: str  # 입력날짜1 — 날짜 (ex) 20240402)
    FID_BLNC_CLS_CODE: str  # 결재방법 — 0(전체), 1(일반), 2(조기종료)

class NewlyListedResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_lstn_date: str | None = None  # 주식상장일자
    elw_kor_isnm: str | None = None  # ELW한글종목명
    elw_shrn_iscd: str | None = None  # ELW단축종목코드
    unas_isnm: str | None = None  # 기초자산종목명
    pblc_co_name: str | None = None  # 발행회사명
    lstn_stcn: str | None = None  # 상장주수
    acpr: str | None = None  # 행사가
    stck_last_tr_date: str | None = None  # 주식최종거래일자
    elw_ko_barrier: str | None = None  # 조기종료발생기준가격

class NewlyListedResponse(KisCommonResponse):
    """응답 본문."""

    output: list[NewlyListedResponse_OutputItem] = []  # 응답상세 — array

class NewlyListedExecutor(ApiExecutor[NewlyListedRequest, NewlyListedResponse]):
    """ELW 신규상장종목 [국내주식-181]."""

    # ELW 신규상장종목 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0297] ELW 신규상장종목 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/elw/v1/quotations/newly-listed"
    METHOD = "GET"
    RESPONSE_TYPE = NewlyListedResponse
    TR_ID = "FHKEW154800C0"
