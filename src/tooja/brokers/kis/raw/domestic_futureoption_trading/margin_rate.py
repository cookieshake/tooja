"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class MarginRateRequest(KisBaseModel):
    """요청."""

    BASS_DT: str  # 기준일자 — 날짜 입력) ex) 20260313
    BAST_ID: str  # 기초자산ID — 공백 입력
    CTX_AREA_NK200: str  # 연속조회키200 — 다음 조회 시 필요, 입력 후 header tr_cont : N 설정 필수

class MarginRateResponse_OutputItem(KisBaseModel):
    """nested item."""

    bast_id: str | None = None  # 기초자산ID
    bast_name: str | None = None  # 기초자산명
    brkg_mgna_rt: str | None = None  # 위탁증거금율 — 소수점 8자리까지 표현
    tr_mgna_rt: str | None = None  # 거래증거금율 — 소수점 8자리까지 표현
    bast_pric: str | None = None  # 기초자산가격 — 소수점 8자리까지 표현
    tr_mtpl_idx: str | None = None  # 거래승수지수 — 소수점 8자리까지 표현
    ctrt_per_futr_mgna: str | None = None  # 계약당선물증거금 — 소수점 8자리까지 표현

class MarginRateResponse(KisCommonResponse):
    """응답 본문."""

    output: list[MarginRateResponse_OutputItem] = []  # 응답상세 — Array

class MarginRateExecutor(ApiExecutor[MarginRateRequest, MarginRateResponse]):
    """선물옵션 증거금률."""

    # ※ 승수, 계약당 선물 증거금은 최근월물 기준으로 표기되며, 월물에 따라 상이할 수 있습니다. ※ 계약당 선물 증거금은 선물 1계약 기준 신규 주문증거금이며 스프레드 증거금은 조회되지 않습니다. ※ 2023.05.24일부터 조회 가능하며, 익영업일 기준 증거금은 17:00~18:00시에 조회됩니다. ※ 데이터는 하루에 한 번 고정된 이후 데이터 변동이 없으므로 조회가 제한되는 점 이용에 참고 부탁드립니다.

    PATH = "/uapi/domestic-futureoption/v1/quotations/margin-rate"
    METHOD = "GET"
    RESPONSE_TYPE = MarginRateResponse
    TR_ID = "TTTO6032R"
