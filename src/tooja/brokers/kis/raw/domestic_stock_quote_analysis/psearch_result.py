"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class PsearchResultRequest(KisBaseModel):
    """요청."""

    user_id: str  # 사용자 HTS ID
    seq: str  # 사용자조건 키값 — 종목조건검색 목록조회 API의 output인 'seq'을 이용 (0 부터 시작)

class PsearchResultResponse_Output2Item(KisBaseModel):
    """nested item."""

    code: str | None = None  # 종목코드
    name: str | None = None  # 종목명
    daebi: str | None = None  # 전일대비부호 — 1. 상한 2. 상승 3. 보합 4. 하한 5. 하락
    price: str | None = None  # 현재가
    chgrate: str | None = None  # 등락율
    acml_vol: str | None = None  # 거래량
    trade_amt: str | None = None  # 거래대금
    change: str | None = None  # 전일대비
    cttr: str | None = None  # 체결강도
    open: str | None = None  # 시가
    high: str | None = None  # 고가
    low: str | None = None  # 저가
    high52: str | None = None  # 52주최고가
    low52: str | None = None  # 52주최저가
    expprice: str | None = None  # 예상체결가
    expchange: str | None = None  # 예상대비
    expchggrate: str | None = None  # 예상등락률
    expcvol: str | None = None  # 예상체결수량
    chgrate2: str | None = None  # 전일거래량대비율
    expdaebi: str | None = None  # 예상대비부호
    recprice: str | None = None  # 기준가
    uplmtprice: str | None = None  # 상한가
    dnlmtprice: str | None = None  # 하한가
    stotprice: str | None = None  # 시가총액

class PsearchResultResponse(KisCommonResponse):
    """응답 본문."""

    output2: list[PsearchResultResponse_Output2Item] = []  # 응답상세 — Array

class PsearchResultExecutor(ApiExecutor[PsearchResultRequest, PsearchResultResponse]):
    """종목조건검색조회 [국내주식-039]."""

    # HTS(efriend Plus) [0110] 조건검색에서 등록 및 서버저장한 나의 조건 목록을 확인할 수 있는 API입니다. 종목조건검색 목록조회 API(/uapi/domestic-stock/v1/quotations/psearch-title)의 output인 'seq'을 종목조건검색조회 API(/uapi/domestic-stock/v1/quotations/psearch-result)의 input으로 사용하시면 됩니다. ※ 시스

    PATH = "/uapi/domestic-stock/v1/quotations/psearch-result"
    METHOD = "GET"
    RESPONSE_TYPE = PsearchResultResponse
    TR_ID = "HHKST03900400"
