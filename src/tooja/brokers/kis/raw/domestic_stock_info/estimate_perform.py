"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class EstimatePerformRequest(KisBaseModel):
    """요청."""

    SHT_CD: str  # 종목코드 — ex) 265520

class EstimatePerformResponse_Output1Item(KisBaseModel):
    """nested item."""

    sht_cd: str | None = None  # ELW단축종목코드
    item_kor_nm: str | None = None  # HTS한글종목명
    name1: str | None = None  # ELW현재가
    name2: str | None = None  # 전일대비
    estdate: str | None = None  # 전일대비부호
    rcmd_name: str | None = None  # 전일대비율
    capital: str | None = None  # 누적거래량
    forn_item_lmtrt: str | None = None  # 행사가

class EstimatePerformResponse_Output2Item(KisBaseModel):
    """nested item."""

    data1: str | None = None  # DATA1 — 결산연월(outblock4) 참조
    data2: str | None = None  # DATA2 — 결산연월(outblock4) 참조
    data3: str | None = None  # DATA3 — 결산연월(outblock4) 참조
    data4: str | None = None  # DATA4 — 결산연월(outblock4) 참조
    data5: str | None = None  # DATA5 — 결산연월(outblock4) 참조

class EstimatePerformResponse_Output3Item(KisBaseModel):
    """nested item."""

    data1: str | None = None  # DATA1 — 결산연월(outblock4) 참조
    data2: str | None = None  # DATA2 — 결산연월(outblock4) 참조
    data3: str | None = None  # DATA3 — 결산연월(outblock4) 참조
    data4: str | None = None  # DATA4 — 결산연월(outblock4) 참조
    data5: str | None = None  # DATA5 — 결산연월(outblock4) 참조

class EstimatePerformResponse_Output4Item(KisBaseModel):
    """nested item."""

    dt: str | None = None  # 결산년월 — DATA1 ~5 결산월 정보

class EstimatePerformResponse(KisCommonResponse):
    """응답 본문."""

    output1: EstimatePerformResponse_Output1Item | None = None  # 응답상세
    output2: list[EstimatePerformResponse_Output2Item] = []  # 응답상세 — '(추정손익계산서-6개 array) 매출액, 매출액증감율, 영업이익, 영업이익증감율, 순이익, 순이익증감율,'
    output3: list[EstimatePerformResponse_Output3Item] = []  # 응답상세 — '(투자지표-8개 array) EBITDA(십억원), EPS(원), EPS 증감율(0.1%), PER(배, 0.1%), EV/EBITDA(배, 0.1), ROE(0.1%), 부채비율(0.1%), 이자보상배율(0.1%)'
    output4: list[EstimatePerformResponse_Output4Item] = []  # 응답상세 — array

class EstimatePerformExecutor(ApiExecutor[EstimatePerformRequest, EstimatePerformResponse]):
    """국내주식 종목추정실적 [국내주식-187]."""

    # 국내주식 종목추정실적 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0613] 종목추정실적 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 본 화면의 추정실적 및 투자의견은 당월 초의 애널리스트의 의견사항이므로 월중 변동 사항이 있을 수 있음을 유의하시기 바랍니다. ※ 종목별 수익추정은 리서치본부에서 매월 발표되는 거래소, 코스닥 160여개 기업에 한정합니다. 

    PATH = "/uapi/domestic-stock/v1/quotations/estimate-perform"
    METHOD = "GET"
    RESPONSE_TYPE = EstimatePerformResponse
    TR_ID = "HHKST668300C0"
