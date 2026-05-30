"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class IntstockStocklistByGroupRequest(KisBaseModel):
    """요청."""

    TYPE: str  # 관심종목구분코드 — Unique key(1)
    USER_ID: str  # 사용자 ID — HTS_ID 입력
    DATA_RANK: str  # 데이터 순위 — 공백
    INTER_GRP_CODE: str  # 관심 그룹 코드 — 관심그룹 조회 결과의 그룹 값 입력
    INTER_GRP_NAME: str  # 관심 그룹 명 — 공백
    HTS_KOR_ISNM: str  # HTS 한글 종목명 — 공백
    CNTG_CLS_CODE: str  # 체결 구분 코드 — 공백
    FID_ETC_CLS_CODE: str  # 기타 구분 코드 — Unique key(4)

class IntstockStocklistByGroupResponse_Output1Item(KisBaseModel):
    """nested item."""

    data_rank: str | None = None  # 데이터 순위
    inter_grp_name: str | None = None  # 관심 그룹 명

class IntstockStocklistByGroupResponse_Output2Item(KisBaseModel):
    """nested item."""

    fid_mrkt_cls_code: str | None = None  # FID 시장 구분 코드
    data_rank: str | None = None  # 데이터 순위
    exch_code: str | None = None  # 거래소코드
    jong_code: str | None = None  # 종목코드
    color_code: str | None = None  # 생상 코드
    memo: str | None = None  # 메모
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    fxdt_ntby_qty: str | None = None  # 기준일 순매수 수량
    cntg_unpr: str | None = None  # 체결단가
    cntg_cls_code: str | None = None  # 체결 구분 코드

class IntstockStocklistByGroupResponse(KisCommonResponse):
    """응답 본문."""

    output1: IntstockStocklistByGroupResponse_Output1Item | None = None  # 응답상세
    output2: list[IntstockStocklistByGroupResponse_Output2Item] = []  # 응답상세 — array

class IntstockStocklistByGroupExecutor(ApiExecutor[IntstockStocklistByGroupRequest, IntstockStocklistByGroupResponse]):
    """관심종목 그룹별 종목조회 [국내주식-203]."""

    # 관심종목 그룹별 종목조회 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0161] 관심종목 화면 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ① 관심종목 그룹조회 → ② 관심종목 그룹별 종목조회 → ③ 관심종목(멀티종목) 시세조회 순서대로 호출하셔서 관심종목 시세 조회 가능합니다. ※ 한 번의 호출에 최대 30종목의 시세 확인 가능합니다. 한국투자증권 Github 에서

    PATH = "/uapi/domestic-stock/v1/quotations/intstock-stocklist-by-group"
    METHOD = "GET"
    RESPONSE_TYPE = IntstockStocklistByGroupResponse
    TR_ID = "HHKCM113004C6"
