"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class PsearchTitleRequest(KisBaseModel):
    """요청."""

    user_id: str  # 사용자 HTS ID

class PsearchTitleResponse_Output2Item(KisBaseModel):
    """nested item."""

    user_id: str | None = None  # HTS ID
    seq: str | None = None  # 조건키값 — 해당 값을 종목조건검색조회 API의 input으로 사용 (0번부터 시작)
    grp_nm: str | None = None  # 그룹명 — HTS(eFriend Plus) [0110] "사용자조건검색"화면을 통해 등록한 사용자조건 그룹
    condition_nm: str | None = None  # 조건명 — 등록한 사용자 조건명

class PsearchTitleResponse(KisCommonResponse):
    """응답 본문."""

    output2: list[PsearchTitleResponse_Output2Item] = []  # 응답상세 — Array

class PsearchTitleExecutor(ApiExecutor[PsearchTitleRequest, PsearchTitleResponse]):
    """종목조건검색 목록조회[국내주식-038]."""

    # HTS(efriend Plus) [0110] 조건검색에서 등록 및 서버저장한 나의 조건 목록을 확인할 수 있는 API입니다. 종목조건검색 목록조회 API(/uapi/domestic-stock/v1/quotations/psearch-title)의 output인 'seq'을 종목조건검색조회 API(/uapi/domestic-stock/v1/quotations/psearch-result)의 input으로 사용하시면 됩니다. ※ 시스

    PATH = "/uapi/domestic-stock/v1/quotations/psearch-title"
    METHOD = "GET"
    RESPONSE_TYPE = PsearchTitleResponse
    TR_ID = "HHKST03900300"
