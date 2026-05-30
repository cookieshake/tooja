"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class UdrlAssetPriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — 시장구분(W)
    FID_COND_SCR_DIV_CODE: str  # 조건화면분류코드 — Uniquekey(11541)
    FID_MRKT_CLS_CODE: str  # 시장구분코드 — 전체(A),콜(C),풋(P)
    FID_INPUT_ISCD: str  # 입력종목코드 — '00000(전체), 00003(한국투자증권) , 00017(KB증권), 00005(미래에셋주식회사)'
    FID_UNAS_INPUT_ISCD: str  # 기초자산입력종목코드
    FID_VOL_CNT: str  # 거래량수 — 전일거래량(정수량미만)
    FID_TRGT_EXLS_CLS_CODE: str  # 대상제외구분코드 — 거래불가종목제외(0:미체크,1:체크)
    FID_INPUT_PRICE_1: str  # 입력가격1 — 가격~원이상
    FID_INPUT_PRICE_2: str  # 입력가격2 — 가격~월이하
    FID_INPUT_VOL_1: str  # 입력거래량1 — 거래량~계약이상
    FID_INPUT_VOL_2: str  # 입력거래량2 — 거래량~계약이하
    FID_INPUT_RMNN_DYNU_1: str  # 입력잔존일수1 — 잔존일(~일이상)
    FID_INPUT_RMNN_DYNU_2: str  # 입력잔존일수2 — 잔존일(~일이하)
    FID_OPTION: str  # 옵션 — 옵션상태(0:없음,1:ATM,2:ITM,3:OTM)
    FID_INPUT_OPTION_1: str  # 입력옵션1
    FID_INPUT_OPTION_2: str  # 입력옵션2

class UdrlAssetPriceResponse_OutputItem(KisBaseModel):
    """nested item."""

    elw_shrn_iscd: str | None = None  # ELW단축종목코드
    hts_kor_isnm: str | None = None  # HTS한글종목명
    elw_prpr: str | None = None  # ELW현재가
    prdy_vrss: str | None = None  # 전일대비
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_ctrt: str | None = None  # 전일대비율
    acml_vol: str | None = None  # 누적거래량
    acpr: str | None = None  # 행사가
    prls_qryr_stpr_prc: str | None = None  # 손익분기주가가격
    hts_rmnn_dynu: str | None = None  # HTS잔존일수
    hts_ints_vltl: str | None = None  # HTS내재변동성
    stck_cnvr_rate: str | None = None  # 주식전환비율
    lp_hvol: str | None = None  # LP보유량
    lp_rlim: str | None = None  # LP비중
    lvrg_val: str | None = None  # 레버리지값
    gear: str | None = None  # 기어링
    delta_val: str | None = None  # 델타값
    gama: str | None = None  # 감마
    vega: str | None = None  # 베가
    theta: str | None = None  # 세타
    prls_qryr_rate: str | None = None  # 손익분기비율
    cfp: str | None = None  # 자본지지점
    prit: str | None = None  # 패리티
    invl_val: str | None = None  # 내재가치값
    tmvl_val: str | None = None  # 시간가치값
    hts_thpr: str | None = None  # HTS이론가
    stck_lstn_date: str | None = None  # 주식상장일자
    stck_last_tr_date: str | None = None  # 주식최종거래일자
    lp_ntby_qty: str | None = None  # LP순매도량

class UdrlAssetPriceResponse(KisCommonResponse):
    """응답 본문."""

    output: list[UdrlAssetPriceResponse_OutputItem] = []  # 응답상세 — array

class UdrlAssetPriceExecutor(ApiExecutor[UdrlAssetPriceRequest, UdrlAssetPriceResponse]):
    """ELW 기초자산별 종목시세 [국내주식-186]."""

    # ELW 기초자산별 종목시세 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0288] ELW 기초자산별 ELW 시세 화면의 "우측 기초자산별 종목 리스트" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/elw/v1/quotations/udrl-asset-price"
    METHOD = "GET"
    RESPONSE_TYPE = UdrlAssetPriceResponse
    TR_ID = "FHKEW154101C0"
