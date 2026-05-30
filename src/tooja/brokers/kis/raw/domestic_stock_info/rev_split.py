"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class RevSplitRequest(KisBaseModel):
    """요청."""

    SHT_CD: str  # 종목코드 — 공백: 전체, 특정종목 조회시 : 종목코드
    CTS: str  # CTS — 공백
    F_DT: str  # 조회일자From — 일자 ~
    T_DT: str  # 조회일자To — ~ 일자
    MARKET_GB: str  # 시장구분 — 0:전체, 1:코스피, 2:코스닥

class RevSplitResponse_Output1Item(KisBaseModel):
    """nested item."""

    record_date: str | None = None  # 기준일
    sht_cd: str | None = None  # 종목코드
    isin_name: str | None = None  # 종목명
    inter_bf_face_amt: str | None = None  # 변경전액면가
    inter_af_face_amt: str | None = None  # 변경후액면가
    td_stop_dt: str | None = None  # 매매거래정지기간
    list_dt: str | None = None  # 상장/등록일

class RevSplitResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[RevSplitResponse_Output1Item] = []  # 응답상세 — array

class RevSplitExecutor(ApiExecutor[RevSplitRequest, RevSplitResponse]):
    """예탁원정보(액면교체일정)[국내주식-148]."""

    # 예탁원정보(액면교체일정) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0657] 액면교체 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.

    PATH = "/uapi/domestic-stock/v1/ksdinfo/rev-split"
    METHOD = "GET"
    RESPONSE_TYPE = RevSplitResponse
    TR_ID = "HHKDB669105C0"
