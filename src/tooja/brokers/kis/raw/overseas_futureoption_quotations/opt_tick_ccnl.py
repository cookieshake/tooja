"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OptTickCcnlRequest(KisBaseModel):
    """요청."""

    SRS_CD: str  # 종목코드 — ex) OESU24 C5500 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션/해외주식옵션" 참고
    EXCH_CD: str  # 거래소코드 — 종목코드에 맞는 거래소 코드 ex) CME
    START_DATE_TIME: str  # 조회시작일시 — "" 공란 입력
    CLOSE_DATE_TIME: str  # 조회종료일시 — "" 공란 입력 ※ 날짜 입력해도 처리 안됨
    QRY_TP: str  # 조회구분 — Q : 최초조회시 , P : 다음키(INDEX_KEY) 입력하여 조회시
    QRY_CNT: str  # 요청개수 — 예) 30 (최대 40)
    QRY_GAP: str  # 묶음개수 — 공백
    INDEX_KEY: str  # 이전조회KEY — 다음조회(QRY_TP를 P로 입력) 시, 이전 호출의 "output1 > index_key" 기입하여 조회

class OptTickCcnlResponse_Output1Item(KisBaseModel):
    """nested item."""

    ret_cnt: str | None = None  # 자료개수
    last_n_cnt: str | None = None  # N틱최종개수
    index_key: str | None = None  # 이전조회KEY

class OptTickCcnlResponse_Output2Item(KisBaseModel):
    """nested item."""

    data_date: str | None = None  # 일자 — 과거일자 ~ 최근일자 순으로 조회됨
    data_time: str | None = None  # 시간 — HHMMSS
    open_price: str | None = None  # 시가
    high_price: str | None = None  # 고가
    low_price: str | None = None  # 저가
    last_price: str | None = None  # 체결가격 — 체결가격 ※ focode.mst, fostkcode.mst* 의 sCalcDesz(계산 소수점) 값 참고 * 포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션/해외주식옵션
    last_qntt: str | None = None  # 체결수량
    vol: str | None = None  # 누적거래수량
    prev_diff_flag: str | None = None  # 전일대비구분
    prev_diff_price: str | None = None  # 전일대비가격
    prev_diff_rate: str | None = None  # 전일대비율

class OptTickCcnlResponse(KisCommonResponse):
    """응답 본문."""

    output1: OptTickCcnlResponse_Output1Item | None = None  # 응답상세
    output2: list[OptTickCcnlResponse_Output2Item] = []  # 응답상세 — array

class OptTickCcnlExecutor(ApiExecutor[OptTickCcnlRequest, OptTickCcnlResponse]):
    """해외옵션 체결추이(틱) [해외선물-038]."""

    # 해외옵션 체결추이(틱) API입니다. 한 번의 호출에 40건까지 확인 가능하며, QRY_TP, INDEX_KEY 를 이용하여 다음조회 가능합니다. ※ 다음조회 방법 (처음조회) "QRY_TP":"Q", "QRY_CNT":"40", "INDEX_KEY":"" (다음조회) "QRY_TP":"P", "QRY_CNT":"40", "INDEX_KEY":"20240906 221" ◀ 이전 호출의 "output1 &gt; index_key

    PATH = "/uapi/overseas-futureoption/v1/quotations/opt-tick-ccnl"
    METHOD = "GET"
    RESPONSE_TYPE = OptTickCcnlResponse
    TR_ID = "HHDFO55020200"
