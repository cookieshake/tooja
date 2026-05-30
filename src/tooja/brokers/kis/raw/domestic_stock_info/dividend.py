"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class DividendRequest(KisBaseModel):
    """요청."""

    CTS: str  # CTS — 공백
    GB1: str  # 조회구분 — 0:배당전체, 1:결산배당, 2:중간배당
    F_DT: str  # 조회일자From — 일자 ~
    T_DT: str  # 조회일자To — ~ 일자
    SHT_CD: str  # 종목코드 — 공백: 전체, 특정종목 조회시 : 종목코드
    HIGH_GB: str  # 고배당여부 — 공백

class DividendResponse_Output1Item(KisBaseModel):
    """nested item."""

    record_date: str | None = None  # 기준일
    sht_cd: str | None = None  # 종목코드
    isin_name: str | None = None  # 종목명
    divi_kind: str | None = None  # 배당종류
    face_val: str | None = None  # 액면가
    per_sto_divi_amt: str | None = None  # 현금배당금
    divi_rate: str | None = None  # 현금배당률(%)
    stk_divi_rate: str | None = None  # 주식배당률(%)
    divi_pay_dt: str | None = None  # 배당금지급일
    stk_div_pay_dt: str | None = None  # 주식배당지급일
    odd_pay_dt: str | None = None  # 단주대금지급일
    stk_kind: str | None = None  # 주식종류
    high_divi_gb: str | None = None  # 고배당종목여부

class DividendResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[DividendResponse_Output1Item] = []  # 응답상세 — array

class DividendExecutor(ApiExecutor[DividendRequest, DividendResponse]):
    """예탁원정보(배당일정)[국내주식-145]."""

    # 예탁원정보(배당일정) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0658] 배당 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다. '주식배당지급일'은 배당주식의 주식교부일자를 말합니다. 배당주식의 계좌입고는 배당주식 상장일인데 일반적으로 주권교부일의 익영업일입니다.

    PATH = "/uapi/domestic-stock/v1/ksdinfo/dividend"
    METHOD = "GET"
    RESPONSE_TYPE = DividendResponse
    TR_ID = "HHKDB669102C0"
