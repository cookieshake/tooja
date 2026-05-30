"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class ExpirationStocksRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — W 입력
    FID_COND_SCR_DIV_CODE: str  # 조건화면분류코드 — 11547 입력
    FID_INPUT_DATE_1: str  # 입력날짜1 — 입력날짜 ~ (ex) 20240402)
    FID_INPUT_DATE_2: str  # 입력날짜2 — ~입력날짜 (ex) 20240408)
    FID_DIV_CLS_CODE: str  # 분류구분코드 — 0(콜),1(풋),2(전체)
    FID_ETC_CLS_CODE: str  # 기타구분코드 — 공백 입력
    FID_UNAS_INPUT_ISCD: str  # 기초자산입력종목코드 — 000000(전체), 2001(KOSPI 200), 기초자산코드(종목코드 ex. 삼성전자-005930)
    FID_INPUT_ISCD_2: str  # 발행회사코드 — 00000(전체), 00003(한국투자증권), 00017(KB증권), 00005(미래에셋증권)
    FID_BLNG_CLS_CODE: str  # 결제방법 — 0(전체),1(일반),2(조기종료)
    FID_INPUT_OPTION_1: str  # 입력옵션1 — 공백 입력

class ExpirationStocksResponse_Output1Item(KisBaseModel):
    """nested item."""

    elw_shrn_iscd: str | None = None  # ELW단축종목코드
    elw_kor_isnm: str | None = None  # ELW한글종목명
    unas_isnm: str | None = None  # 기초자산종목명
    unas_prpr: str | None = None  # 기초자산현재가
    acpr: str | None = None  # 행사가
    stck_cnvr_rate: str | None = None  # 주식전환비율
    elw_prpr: str | None = None  # ELW현재가
    stck_lstn_date: str | None = None  # 주식상장일자
    stck_last_tr_date: str | None = None  # 주식최종거래일자
    total_rdmp_amt: str | None = None  # 총상환금액
    rdmp_amt: str | None = None  # 상환금액
    lstn_stcn: str | None = None  # 상장주수
    lp_hvol: str | None = None  # LP보유량
    ccls_paym_prc: str | None = None  # 확정지급2가격
    mtrt_vltn_amt: str | None = None  # 만기평가금액
    evnt_prd_fin_date: str | None = None  # 행사2기간종료일자
    stlm_date: str | None = None  # 결제일자
    pblc_prc: str | None = None  # 발행가격
    unas_shrn_iscd: str | None = None  # 기초자산단축종목코드
    stnd_iscd: str | None = None  # 표준종목코드
    rdmp_ask_amt: str | None = None  # 상환청구금액

class ExpirationStocksResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[ExpirationStocksResponse_Output1Item] = []  # 응답상세 — array

class ExpirationStocksExecutor(ApiExecutor[ExpirationStocksRequest, ExpirationStocksResponse]):
    """ELW 만기예정/만기종목 [국내주식-184]."""

    # ELW 만기예정/만기종목 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0290] ELW 만기예정/만기종목 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 최근 100건까지 데이터 조회 가능합니다.

    PATH = "/uapi/elw/v1/quotations/expiration-stocks"
    METHOD = "GET"
    RESPONSE_TYPE = ExpirationStocksResponse
    TR_ID = "FHKEW154700C0"
