"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class ChkHolidayRequest(KisBaseModel):
    """요청."""

    BASS_DT: str  # 기준일자 — 기준일자(YYYYMMDD)
    CTX_AREA_NK: str  # 연속조회키 — 공백으로 입력
    CTX_AREA_FK: str  # 연속조회검색조건 — 공백으로 입력

class ChkHolidayResponse_OutputItem(KisBaseModel):
    """nested item."""

    bass_dt: str | None = None  # 기준일자 — 기준일자(YYYYMMDD)
    wday_dvsn_cd: str | None = None  # 요일구분코드 — 01:일요일, 02:월요일, 03:화요일, 04:수요일, 05:목요일, 06:금요일, 07:토요일
    bzdy_yn: str | None = None  # 영업일여부 — Y/N 금융기관이 업무를 하는 날
    tr_day_yn: str | None = None  # 거래일여부 — Y/N 증권 업무가 가능한 날(입출금, 이체 등의 업무 포함)
    opnd_yn: str | None = None  # 개장일여부 — Y/N 주식시장이 개장되는 날 * 주문을 넣고자 할 경우 개장일여부(opnd_yn)를 사용
    sttl_day_yn: str | None = None  # 결제일여부 — Y/N 주식 거래에서 실제로 주식을 인수하고 돈을 지불하는 날

class ChkHolidayResponse(KisCommonResponse):
    """응답 본문."""

    output: ChkHolidayResponse_OutputItem | None = None  # 응답상세1

class ChkHolidayExecutor(ApiExecutor[ChkHolidayRequest, ChkHolidayResponse]):
    """국내휴장일조회[국내주식-040]."""

    # (★중요) 국내휴장일조회(TCA0903R) 서비스는 당사 원장서비스와 연관되어 있어 단시간 내 다수 호출시 서비스에 영향을 줄 수 있어 가급적 1일 1회 호출 부탁드립니다. 국내휴장일조회 API입니다. 영업일, 거래일, 개장일, 결제일 여부를 조회할 수 있습니다. 주문을 넣을 수 있는지 확인하고자 하실 경우 개장일여부(opnd_yn)을 사용하시면 됩니다.

    PATH = "/uapi/domestic-stock/v1/quotations/chk-holiday"
    METHOD = "GET"
    RESPONSE_TYPE = ChkHolidayResponse
    TR_ID = "CTCA0903R"
