"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class RightsByIceRequest(KisBaseModel):
    """요청."""

    NCOD: str  # 국가코드 — CN:중국 HK:홍콩 US:미국 JP:일본 VN:베트남
    SYMB: str  # 심볼 — 종목코드
    ST_YMD: str  # 일자 시작일 — 미입력 시, 오늘-3개월 기간지정 시, 종료일 입력(ex. 20240514) ※ 조회기간 기준일 입력시 참고 - 상환: 상환일자, 조기상환: 조기상환일자, 티커변경: 적용일, 그 외: 발표일
    ED_YMD: str  # 일자 종료일 — 미입력 시, 오늘+3개월 기간지정 시, 종료일 입력(ex. 20240514) ※ 조회기간 기준일 입력시 참고 - 상환: 상환일자, 조기상환: 조기상환일자, 티커변경: 적용일, 그 외: 발표일

class RightsByIceResponse_Output1Item(KisBaseModel):
    """nested item."""

    anno_dt: str | None = None  # ICE공시일
    ca_title: str | None = None  # 권리유형
    div_lock_dt: str | None = None  # 배당락일
    pay_dt: str | None = None  # 지급일
    record_dt: str | None = None  # 기준일
    validity_dt: str | None = None  # 효력일자
    local_end_dt: str | None = None  # 현지지시마감일
    lock_dt: str | None = None  # 권리락일
    delist_dt: str | None = None  # 상장폐지일
    redempt_dt: str | None = None  # 상환일자
    early_redempt_dt: str | None = None  # 조기상환일자
    effective_dt: str | None = None  # 적용일

class RightsByIceResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[RightsByIceResponse_Output1Item] = []  # 응답상세 — array

class RightsByIceExecutor(ApiExecutor[RightsByIceRequest, RightsByIceResponse]):
    """해외주식 권리종합 [해외주식-050]."""

    # 해외주식 권리종합 API입니다. 한국투자 HTS(eFriend Plus) &gt; [7833] 해외주식 권리(ICE제공) 화면의 "전체" 탭 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 조회기간 기준일 입력시 참고 - 상환: 상환일자, 조기상환: 조기상환일자, 티커변경: 적용일, 그 외: 발표일

    PATH = "/uapi/overseas-price/v1/quotations/rights-by-ice"
    METHOD = "GET"
    RESPONSE_TYPE = RightsByIceResponse
    TR_ID = "HHDFS78330900"
