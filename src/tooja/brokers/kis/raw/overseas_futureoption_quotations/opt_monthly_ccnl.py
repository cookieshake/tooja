"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OptMonthlyCcnlRequest(KisBaseModel):
    """요청."""

    SRS_CD: str  # 종목코드 — ex) OESU24 C5500 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션/해외주식옵션" 참고
    EXCH_CD: str  # 거래소코드 — 종목코드에 맞는 거래소 코드 ex) CME
    START_DATE_TIME: str  # 조회시작일시 — "" 공란 입력
    CLOSE_DATE_TIME: str  # 조회종료일시 — "" 공란 입력
    QRY_TP: str  # 조회구분 — Q
    QRY_CNT: str  # 요청개수 — 예) 20 (최대 120)
    QRY_GAP: str  # 묶음개수 — "" 공란 입력
    INDEX_KEY: str  # 이전조회KEY — "" 공란 입력

class OptMonthlyCcnlResponse_Output1Item(KisBaseModel):
    """nested item."""

    ret_cnt: str | None = None  # 자료개수
    last_n_cnt: str | None = None  # N틱최종개수
    index_key: str | None = None  # 이전조회KEY

class OptMonthlyCcnlResponse_Output2Item(KisBaseModel):
    """nested item."""

    data_date: str | None = None  # 일자 — 과거일자 ~ 최근일자 순으로 조회됨
    data_time: str | None = None  # 시간 — ""
    open_price: str | None = None  # 시가
    high_price: str | None = None  # 고가
    low_price: str | None = None  # 저가
    last_price: str | None = None  # 체결가격 — 체결가격 ※ focode.mst, fostkcode.mst* 의 sCalcDesz(계산 소수점) 값 참고 * 포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션/해외주식옵션
    last_qntt: str | None = None  # 체결수량
    vol: str | None = None  # 누적거래수량
    prev_diff_flag: str | None = None  # 전일대비구분
    prev_diff_price: str | None = None  # 전일대비가격
    prev_diff_rate: str | None = None  # 전일대비율

class OptMonthlyCcnlResponse(KisCommonResponse):
    """응답 본문."""

    output1: OptMonthlyCcnlResponse_Output1Item | None = None  # 응답상세
    output2: list[OptMonthlyCcnlResponse_Output2Item] = []  # 응답상세 — array

class OptMonthlyCcnlExecutor(ApiExecutor[OptMonthlyCcnlRequest, OptMonthlyCcnlResponse]):
    """해외옵션 체결추이(월간) [해외선물-039]."""

    # 해외옵션 체결추이(월간) API입니다. 최근 120건까지 데이터 확인이 가능합니다. (START_DATE_TIME, CLOSE_DATE_TIME은 공란 입력) (중요) 해외옵션시세 출력값을 해석하실 때 focode.mst(해외지수옵션 종목마스터파일), fostkcode.mst(해외주식옵션 종목마스터파일)에 있는 sCalcDesz(계산 소수점) 값을 활용하셔야 정확한 값을 받아오실 수 있습니다. - focode.mst(해외지수옵

    PATH = "/uapi/overseas-futureoption/v1/quotations/opt-monthly-ccnl"
    METHOD = "GET"
    RESPONSE_TYPE = OptMonthlyCcnlResponse
    TR_ID = "HHDFO55020300"
