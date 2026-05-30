"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class QuickChangeRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — 시장구분코드 (W)
    FID_COND_SCR_DIV_CODE: str  # 조건화면분류코드 — Unique key(20287)
    FID_UNAS_INPUT_ISCD: str  # 기초자산입력종목코드 — '000000(전체), 2001(코스피200) , 3003(코스닥150), 005930(삼성전자) '
    FID_INPUT_ISCD: str  # 발행사 — '00000(전체), 00003(한국투자증권) , 00017(KB증권), 00005(미래에셋주식회사)'
    FID_MRKT_CLS_CODE: str  # 시장구분코드 — Unique key(A)
    FID_INPUT_PRICE_1: str  # 가격(이상)
    FID_INPUT_PRICE_2: str  # 가격(이하)
    FID_INPUT_VOL_1: str  # 거래량(이상)
    FID_INPUT_VOL_2: str  # 거래량(이하)
    FID_HOUR_CLS_CODE: str  # 시간구분코드 — 1(분), 2(일)
    FID_INPUT_HOUR_1: str  # 입력 일 또는 분
    FID_INPUT_HOUR_2: str  # 기준시간(분 선택 시)
    FID_RANK_SORT_CLS_CODE: str  # 순위정렬구분코드 — '1(가격급등), 2(가격급락), 3(거래량급증) , 4(매수잔량급증), 5(매도잔량급증)'
    FID_BLNG_CLS_CODE: str  # 결재방법 — 0(전체), 1(일반), 2(조기종료)

class QuickChangeResponse_OutputItem(KisBaseModel):
    """nested item."""

    elw_shrn_iscd: str | None = None  # ELW단축종목코드
    elw_kor_isnm: str | None = None  # ELW한글종목명
    elw_prpr: str | None = None  # ELW현재가
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_vrss: str | None = None  # 전일대비
    prdy_ctrt: str | None = None  # 전일대비율
    askp: str | None = None  # 매도호가
    bidp: str | None = None  # 매수호가
    total_askp_rsqn: str | None = None  # 총매도호가잔량
    total_bidp_rsqn: str | None = None  # 총매수호가잔량
    acml_vol: str | None = None  # 누적거래량
    stnd_val: str | None = None  # 기준값
    stnd_val_vrss: str | None = None  # 기준값대비
    stnd_val_ctrt: str | None = None  # 기준값대비율

class QuickChangeResponse(KisCommonResponse):
    """응답 본문."""

    output: list[QuickChangeResponse_OutputItem] = []  # 응답상세 — array

class QuickChangeExecutor(ApiExecutor[QuickChangeRequest, QuickChangeResponse]):
    """ELW 당일급변종목[국내주식-171]."""

    # ELW 당일급변종목 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0287] ELW 당일급변종목 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/elw/v1/ranking/quick-change"
    METHOD = "GET"
    RESPONSE_TYPE = QuickChangeResponse
    TR_ID = "FHPEW02870000"
