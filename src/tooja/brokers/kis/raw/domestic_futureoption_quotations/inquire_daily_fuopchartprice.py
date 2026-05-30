"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireDailyFuopchartpriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # FID 조건 시장 분류 코드 — F: 지수선물, O:지수옵션 JF: 주식선물, JO:주식옵션, CF: 상품선물(금), 금리선물(국채), 통화선물(달러) CM: 야간선물, EU: 야간옵션
    FID_INPUT_ISCD: str  # 종목코드 — 종목번호 (지수선물:6자리, 지수옵션 9자리)
    FID_INPUT_DATE_1: str  # 조회 시작일자 — 조회 시작일자 (ex. 20220401)
    FID_INPUT_DATE_2: str  # 조회 종료일자 — 조회 종료일자 (ex. 20220524) ※ 주(W), 월(M), 년(Y) 봉 조회 시에 아래 참고 ㅁ FID_INPUT_DATE_2 가 현재일 까지일때 . 주봉 조회 : 해당 주의 첫번째 영업일이 포함되어야함 . 월봉 조회 : 해당
    FID_PERIOD_DIV_CODE: str  # 기간분류코드 — D:일봉 W:주봉, M:월봉, Y:년봉

class InquireDailyFuopchartpriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: dict | None = None  # 상세기본정보
    _futs_prdy_vrss: str | None = None  # 전일 대비
    _prdy_vrss_sign: str | None = None  # 전일 대비 부호
    _futs_prdy_ctrt: str | None = None  # 선물 전일 대비율
    _futs_prdy_clpr: str | None = None  # 선물 전일 종가
    _acml_vol: str | None = None  # 누적 거래량
    _acml_tr_pbmn: str | None = None  # 누적 거래 대금
    _hts_kor_isnm: str | None = None  # HTS 한글 종목명
    _futs_prpr: str | None = None  # 현재가
    _futs_shrn_iscd: str | None = None  # 단축 종목코드
    _prdy_vol: str | None = None  # 전일 거래량
    _futs_mxpr: str | None = None  # 상한가
    _futs_llam: str | None = None  # 하한가
    _futs_oprc: str | None = None  # 시가
    _futs_hgpr: str | None = None  # 최고가
    _futs_lwpr: str | None = None  # 최저가
    _futs_prdy_oprc: str | None = None  # 전일 시가
    _futs_prdy_hgpr: str | None = None  # 전일 최고가
    _futs_prdy_lwpr: str | None = None  # 전일 최저가
    _futs_askp: str | None = None  # 매도호가
    _futs_bidp: str | None = None  # 매수호가
    _basis: str | None = None  # 베이시스
    _kospi200_nmix: str | None = None  # KOSPI200 지수
    _kospi200_prdy_vrss: str | None = None  # KOSPI200 전일 대비
    _kospi200_prdy_ctrt: str | None = None  # KOSPI200 전일 대비율
    _kospi200_prdy_vrss_sign: str | None = None  # 전일 대비 부호
    _hts_otst_stpl_qty: str | None = None  # HTS 미결제 약정 수량
    _otst_stpl_qty_icdc: str | None = None  # 미결제 약정 수량 증감
    _tday_rltv: str | None = None  # 당일 체결강도
    _hts_thpr: str | None = None  # HTS 이론가
    _dprt: str | None = None  # 괴리율
    output2: list | None = None  # 기간별 조회데이터 (배열)
    _stck_bsop_date: str | None = None  # 영업 일자
    _futs_prpr: str | None = None  # 현재가
    _futs_oprc: str | None = None  # 시가
    _futs_hgpr: str | None = None  # 최고가
    _futs_lwpr: str | None = None  # 최저가
    _acml_vol: str | None = None  # 누적 거래량
    _acml_tr_pbmn: str | None = None  # 누적 거래 대금
    _mod_yn: str | None = None  # 변경 여부

class InquireDailyFuopchartpriceExecutor(ApiExecutor[InquireDailyFuopchartpriceRequest, InquireDailyFuopchartpriceResponse]):
    """선물옵션기간별시세(일/주/월/년)[v1_국내선물-008]."""

    # (지수)선물옵션 기간별시세 데이터(일/주/월/년) 조회 (최대 100건 조회) 실전계좌의 경우, 한 번의 호출에 최대 100건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다. 모의계좌의 경우, 한 번의 호출에 최대 100건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다.

    PATH = "/uapi/domestic-futureoption/v1/quotations/inquire-daily-fuopchartprice"
    METHOD = "GET"
    RESPONSE_TYPE = InquireDailyFuopchartpriceResponse
    TR_ID = "FHKIF03020100"
