"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class FrgnmemPchsTrendRequest(KisBaseModel):
    """요청."""

    FID_INPUT_ISCD: str  # 조건시장분류코드 — 종목코드(ex) 005930(삼성전자))
    FID_INPUT_ISCD_2: str  # 조건화면분류코드 — 외국계 전체(99999)
    FID_COND_MRKT_DIV_CODE: str  # 시장구분코드 — J (KRX만 지원)

class FrgnmemPchsTrendResponse_OutputItem(KisBaseModel):
    """nested item."""

    bsop_hour: str | None = None  # 영업시간
    stck_prpr: str | None = None  # 주식현재가
    prdy_vrss: str | None = None  # 전일대비
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_ctrt: str | None = None  # 전일대비율
    acml_vol: str | None = None  # 누적거래량
    frgn_seln_vol: str | None = None  # 외국인매도거래량
    frgn_shnu_vol: str | None = None  # 외국인매수2거래량
    glob_ntby_qty: str | None = None  # 외국계순매수수량
    frgn_ntby_qty_icdc: str | None = None  # 외국인순매수수량증감

class FrgnmemPchsTrendResponse(KisCommonResponse):
    """응답 본문."""

    output: list[FrgnmemPchsTrendResponse_OutputItem] = []  # 응답상세 — array

class FrgnmemPchsTrendExecutor(ApiExecutor[FrgnmemPchsTrendRequest, FrgnmemPchsTrendResponse]):
    """종목별 외국계 순매수추이 [국내주식-164]."""

    # 종목별 외국계 순매수추이 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0433] 종목별 외국계 순매수추이 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/frgnmem-pchs-trend"
    METHOD = "GET"
    RESPONSE_TYPE = FrgnmemPchsTrendResponse
    TR_ID = "FHKST644400C0"
