"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireTimeOptchartpriceRequest(KisBaseModel):
    """요청."""

    SRS_CD: str  # 종목코드 — ex) OESU24 C5500 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션/해외주식옵션" 참고
    EXCH_CD: str  # 거래소코드 — 종목코드에 맞는 거래소 코드 ex) CME
    START_DATE_TIME: str  # 조회시작일시 — "" 공란 입력
    CLOSE_DATE_TIME: str  # 조회종료일시 — "" 공란 입력 ※ 날짜 입력해도 처리 안됨
    QRY_TP: str  # 조회구분 — Q : 최초조회시 , P : 다음키(INDEX_KEY) 입력하여 조회시
    QRY_CNT: str  # 요청개수 — 예) 120 (최대 120)
    QRY_GAP: str  # 묶음개수 — 1: 1분봉, 5: 5분봉 ...
    INDEX_KEY: str  # 이전조회KEY — 다음조회(QRY_TP를 P로 입력) 시, 이전 호출의 "output1 > index_key" 기입하여 조회

class InquireTimeOptchartpriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    ret_cnt: str | None = None  # 자료개수
    last_n_cnt: str | None = None  # N틱최종개수
    index_key: str | None = None  # 이전조회KEY

class InquireTimeOptchartpriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    data_date: str | None = None  # 일자
    data_time: str | None = None  # 시간
    open_price: str | None = None  # 시가
    high_price: str | None = None  # 고가
    low_price: str | None = None  # 저가
    last_price: str | None = None  # 체결가격 — 체결가격 ※ focode.mst, fostkcode.mst* 의 sCalcDesz(계산 소수점) 값 참고 * 포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션/해외주식옵션
    last_qntt: str | None = None  # 체결수량
    vol: str | None = None  # 누적거래수량
    prev_diff_flag: str | None = None  # 전일대비구분
    prev_diff_price: str | None = None  # 전일대비가격
    prev_diff_rate: str | None = None  # 전일대비율

class InquireTimeOptchartpriceResponse(KisCommonResponse):
    """응답 본문."""

    output2: InquireTimeOptchartpriceResponse_Output2Item | None = None  # 응답상세
    output1: list[InquireTimeOptchartpriceResponse_Output1Item] = []  # 응답상세 — array

class InquireTimeOptchartpriceExecutor(ApiExecutor[InquireTimeOptchartpriceRequest, InquireTimeOptchartpriceResponse]):
    """해외옵션 분봉조회 [해외선물-040]."""

    # 해외옵션 분봉조회 API입니다. 한 번의 호출에 120건까지 확인 가능하며, QRY_TP, INDEX_KEY 를 이용하여 다음조회 가능합니다. ※ 다음조회 방법 (처음조회) "QRY_TP":"Q", "QRY_CNT":"120", "INDEX_KEY":"" (다음조회) "QRY_TP":"P", "QRY_CNT":"120", "INDEX_KEY":"20240902 5" ◀ 이전 호출의 "output1 &gt; index_key" 

    PATH = "/uapi/overseas-futureoption/v1/quotations/inquire-time-optchartprice"
    METHOD = "GET"
    RESPONSE_TYPE = InquireTimeOptchartpriceResponse
    TR_ID = "HHDFO55020400"
