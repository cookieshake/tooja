"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class IntstockGrouplistRequest(KisBaseModel):
    """요청."""

    TYPE: str  # 관심종목구분코드 — Unique key(1)
    FID_ETC_CLS_CODE: str  # FID 기타 구분 코드 — Unique key(00)
    USER_ID: str  # 사용자 ID — HTS_ID 입력

class IntstockGrouplistResponse_Output2Item(KisBaseModel):
    """nested item."""

    date: str | None = None  # 일자
    trnm_hour: str | None = None  # 전송 시간
    data_rank: str | None = None  # 데이터 순위
    inter_grp_code: str | None = None  # 관심 그룹 코드
    inter_grp_name: str | None = None  # 관심 그룹 명
    ask_cnt: str | None = None  # 요청 개수

class IntstockGrouplistResponse(KisCommonResponse):
    """응답 본문."""

    output2: IntstockGrouplistResponse_Output2Item | None = None  # 응답상세

class IntstockGrouplistExecutor(ApiExecutor[IntstockGrouplistRequest, IntstockGrouplistResponse]):
    """관심종목 그룹조회 [국내주식-204]."""

    # 관심종목 그룹조회 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0161] 관심종목 화면 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ① 관심종목 그룹조회 → ② 관심종목 그룹별 종목조회 → ③ 관심종목(멀티종목) 시세조회 순서대로 호출하셔서 관심종목 시세 조회 가능합니다. ※ 한 번의 호출에 최대 30종목의 시세 확인 가능합니다. 한국투자증권 Github 에서 관심종

    PATH = "/uapi/domestic-stock/v1/quotations/intstock-grouplist"
    METHOD = "GET"
    RESPONSE_TYPE = IntstockGrouplistResponse
    TR_ID = "HHKCM113004C7"
