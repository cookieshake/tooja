"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class MonthlyCcnlRequest(KisBaseModel):
    """요청."""

    SRS_CD: str  # 종목코드 — 예) 6AM24
    EXCH_CD: str  # 거래소코드 — 예) CME
    START_DATE_TIME: str  # 조회시작일시 — 공백
    CLOSE_DATE_TIME: str  # 조회종료일시 — 예) 20240402
    QRY_TP: str  # 조회구분 — Q : 최초조회시 , P : 다음키(INDEX_KEY) 입력하여 조회시
    QRY_CNT: str  # 요청개수 — 예) 30 (최대 40)
    QRY_GAP: str  # 묶음개수 — 공백 (분만 사용)
    INDEX_KEY: str  # 이전조회KEY — 공백

class MonthlyCcnlResponse_Output1Item(KisBaseModel):
    """nested item."""

    tret_cnt: str | None = None  # 자료개수
    last_n_cnt: str | None = None  # N틱최종개수
    index_key: str | None = None  # 이전조회KEY

class MonthlyCcnlResponse_Output2Item(KisBaseModel):
    """nested item."""

    data_date: str | None = None  # 일자
    data_time: str | None = None  # 시각
    open_price: str | None = None  # 시가
    high_price: str | None = None  # 고가
    low_price: str | None = None  # 저가
    last_price: str | None = None  # 체결가격
    last_qntt: str | None = None  # 체결수량
    vol: str | None = None  # 누적거래수량
    prev_diff_flag: str | None = None  # 전일대비구분
    prev_diff_price: str | None = None  # 전일대비가격
    prev_diff_rate: str | None = None  # 전일대비율

class MonthlyCcnlResponse(KisCommonResponse):
    """응답 본문."""

    output1: MonthlyCcnlResponse_Output1Item | None = None  # 응답상세
    output2: list[MonthlyCcnlResponse_Output2Item] = []  # 응답상세 — array

class MonthlyCcnlExecutor(ApiExecutor[MonthlyCcnlRequest, MonthlyCcnlResponse]):
    """해외선물 체결추이(월간)[해외선물-020]."""

    # 해외선물옵션 체결추이(월간) API입니다. 한국투자 HTS(eFriend Plus) &gt; [5502] 해외선물옵션 체결추이 화면에서 "월간" 선택 시 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. (중요) 해외선물시세 출력값을 해석하실 때 ffcode.mst(해외선물종목마스터 파일)에 있는 sCalcDesz(계산 소수점) 값을 활용하셔야 정확한 값을 받아오실 수 있습니다. - ffcod

    PATH = "/uapi/overseas-futureoption/v1/quotations/monthly-ccnl"
    METHOD = "GET"
    RESPONSE_TYPE = MonthlyCcnlResponse
    TR_ID = "HHDFC55020300"
