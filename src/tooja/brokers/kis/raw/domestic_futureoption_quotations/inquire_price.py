"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # FID 조건 시장 분류 코드 — F: 지수선물, O:지수옵션 JF: 주식선물, JO:주식옵션 CF: 상품선물(금), 금리선물(국채), 통화선물(달러) CM: 야간선물, EU: 야간옵션
    FID_INPUT_ISCD: str  # FID 입력 종목코드 — 종목코드 (예: 101S03)

class InquirePriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    hts_kor_isnm: str | None = None  # HTS 한글 종목명 — 종목명
    futs_prpr: str | None = None  # 선물 현재가 — 선물의 현재가격
    futs_prdy_vrss: str | None = None  # 선물 전일 대비 — 선물의 전일 종가와 당일 현재가의 차이 (당일 현재가-전일 종가)
    prdy_vrss_sign: str | None = None  # 전일 대비 부호 — 1 : 상한 2 : 상승 3 : 보합 4 : 하한 5 : 하락
    futs_prdy_clpr: str | None = None  # 선물 전일 종가 — 해당 선물 종목의 전일 종가
    futs_prdy_ctrt: str | None = None  # 선물 전일 대비율 — 선물 전일 대비 / 당일 현재가 * 100
    acml_vol: str | None = None  # 누적 거래량 — 당일 조회시점까지 전체 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금 — 당일 조회시점까지 전체 거래금액
    hts_otst_stpl_qty: str | None = None  # HTS 미결제 약정 수량 — 현재까지 반대매매로 청산되지 않은 계약수
    otst_stpl_qty_icdc: str | None = None  # 미결제 약정 수량 증감 — 전일대비 미결제 약정 수량의 증감
    futs_oprc: str | None = None  # 선물 시가2 — 당일 최초 거래가격
    futs_hgpr: str | None = None  # 선물 최고가 — 당일 조회 시점까지 가장 높은 거래가격
    futs_lwpr: str | None = None  # 선물 최저가 — 당일 조회 시점까지 가장 낮은 거래가격
    futs_mxpr: str | None = None  # 선물 상한가 — 당일 거래 가능한 최고 가격
    futs_llam: str | None = None  # 선물 하한가 — 당일 거래 가능한 최저 가격
    basis: str | None = None  # 베이시스 — 이론베이시스 선물 이론가격과 현물가격과의 차이
    futs_sdpr: str | None = None  # 선물 기준가
    hts_thpr: str | None = None  # HTS 이론가 — 해당 월물의 이론적 가치를 계산한 것으로 주가지수 선물 이론가격은 (주가지수 선물 이론가격 = 주가지수 + 기간이자비용 - 기간배당수입) 로 계산
    dprt: str | None = None  # 괴리율 — 현재의 시장가가 이론가격으로부터 얼마나 벗어나 있는지에 대한 측정 자료 괴리도 = (현재가 - 이론가격)
    crbr_aply_mxpr: str | None = None  # 서킷브레이커 적용 상한가
    crbr_aply_llam: str | None = None  # 서킷브레이커 적용 하한가
    futs_last_tr_date: str | None = None  # 선물 최종 거래 일자 — 해당 선물 종목의 마지막 거래일
    hts_rmnn_dynu: str | None = None  # HTS 잔존 일수 — 최종 거래일까지 남은 일수
    futs_lstn_medm_hgpr: str | None = None  # 선물 상장 중 최고가 — 해당 선물 종목의 상장일 이후 최고 거래가격
    futs_lstn_medm_lwpr: str | None = None  # 선물 상장 중 최저가 — 해당 선물 종목의 상장일 이후 최저 거래가격
    delta_val: str | None = None  # 델타 값 — 옵션 종목의 지표값
    gama: str | None = None  # 감마 — 옵션 종목의 지표값
    theta: str | None = None  # 세타 — 옵션 종목의 지표값
    vega: str | None = None  # 베가 — 옵션 종목의 지표값
    rho: str | None = None  # 로우 — 옵션 종목의 지표값
    hist_vltl: str | None = None  # 역사적 변동성 — 옵션 종목의 지표값
    hts_ints_vltl: str | None = None  # HTS 내재 변동성 — 옵션 종목의 지표값
    mrkt_basis: str | None = None  # 시장 베이시스 — 시장베이시스 현재 시장에서 형성된 선물가격과 현물가격과의 차이
    acpr: str | None = None  # 행사가 — 옵션의 행사가격

class InquirePriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    bstp_cls_code: str | None = None  # 업종 구분 코드
    hts_kor_isnm: str | None = None  # HTS 한글 종목명 — 종목명
    bstp_nmix_prpr: str | None = None  # 업종 지수 현재가
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    bstp_nmix_prdy_vrss: str | None = None  # 업종 지수 전일 대비
    bstp_nmix_prdy_ctrt: str | None = None  # 업종 지수 전일 대비율

class InquirePriceResponse_Output3Item(KisBaseModel):
    """nested item."""

    bstp_cls_code: str | None = None  # 업종 구분 코드
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    bstp_nmix_prpr: str | None = None  # 업종 지수 현재가
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    bstp_nmix_prdy_vrss: str | None = None  # 업종 지수 전일 대비
    bstp_nmix_prdy_ctrt: str | None = None  # 업종 지수 전일 대비율

class InquirePriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquirePriceResponse_Output1Item | None = None  # 응답상세1
    output2: InquirePriceResponse_Output2Item | None = None  # 응답상세2
    output3: InquirePriceResponse_Output3Item | None = None  # 응답상세3

class InquirePriceExecutor(ApiExecutor[InquirePriceRequest, InquirePriceResponse]):
    """선물옵션 시세[v1_국내선물-006]."""

    # 선물옵션 시세 API입니다. ※ 종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다. https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info

    PATH = "/uapi/domestic-futureoption/v1/quotations/inquire-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePriceResponse
    TR_ID = "FHMIF10000000"
