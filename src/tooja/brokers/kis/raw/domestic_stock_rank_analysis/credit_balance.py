"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class CreditBalanceRequest(KisBaseModel):
    """요청."""

    FID_COND_SCR_DIV_CODE: str  # 조건 화면 분류 코드 — Unique key(11701)
    FID_INPUT_ISCD: str  # 입력 종목코드 — 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200,
    FID_OPTION: str  # 증가율기간 — 2~999
    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — 시장구분코드 (주식 J)
    FID_RANK_SORT_CLS_CODE: str  # 순위 정렬 구분 코드 — '(융자)0:잔고비율 상위, 1: 잔고수량 상위, 2: 잔고금액 상위, 3: 잔고비율 증가상위, 4: 잔고비율 감소상위 (대주)5:잔고비율 상위, 6: 잔고수량 상위, 7: 잔고금액 상위, 8: 잔고비율 증가상위, 9: 잔고비

class CreditBalanceResponse_Output1Item(KisBaseModel):
    """nested item."""

    bstp_cls_code: str | None = None  # 업종 구분 코드
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    stnd_date1: str | None = None  # 기준 일자1
    stnd_date2: str | None = None  # 기준 일자2

class CreditBalanceResponse_Output2Item(KisBaseModel):
    """nested item."""

    mksc_shrn_iscd: str | None = None  # 유가증권 단축 종목코드
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    whol_loan_rmnd_stcn: str | None = None  # 전체 융자 잔고 주수
    whol_loan_rmnd_amt: str | None = None  # 전체 융자 잔고 금액
    whol_loan_rmnd_rate: str | None = None  # 전체 융자 잔고 비율
    whol_stln_rmnd_stcn: str | None = None  # 전체 대주 잔고 주수
    whol_stln_rmnd_amt: str | None = None  # 전체 대주 잔고 금액
    whol_stln_rmnd_rate: str | None = None  # 전체 대주 잔고 비율
    nday_vrss_loan_rmnd_inrt: str | None = None  # N일 대비 융자 잔고 증가율
    nday_vrss_stln_rmnd_inrt: str | None = None  # N일 대비 대주 잔고 증가율

class CreditBalanceResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[CreditBalanceResponse_Output1Item] = []  # 응답상세 — array
    output2: list[CreditBalanceResponse_Output2Item] = []  # 응답상세 — array

class CreditBalanceExecutor(ApiExecutor[CreditBalanceRequest, CreditBalanceResponse]):
    """국내주식 신용잔고 상위[국내주식-109]."""

    # 국내주식 신용잔고 상위 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0475] 신용잔고 상위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 최대 30건 확인 가능하며, 다음 조회가 불가합니다. ※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다. 종목조건검색 API

    PATH = "/uapi/domestic-stock/v1/ranking/credit-balance"
    METHOD = "GET"
    RESPONSE_TYPE = CreditBalanceResponse
    TR_ID = "FHKST17010000"
