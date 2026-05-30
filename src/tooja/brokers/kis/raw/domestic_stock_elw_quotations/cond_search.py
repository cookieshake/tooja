"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class CondSearchRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — ELW(W)
    FID_COND_SCR_DIV_CODE: str  # 조건화면분류코드 — 화면번호(11510)
    FID_RANK_SORT_CLS_CODE: str  # 순위정렬구분코드 — '정렬1정렬안함(0)종목코드(1)현재가(2)대비율(3)거래량(4)행사가격(5) 전환비율(6)상장일(7)만기일(8)잔존일수(9)레버리지(10)'
    FID_INPUT_CNT_1: str  # 입력수1 — 정렬1기준 - 상위(1)하위(2)
    FID_RANK_SORT_CLS_CODE_2: str  # 순위정렬구분코드2 — 정렬2
    FID_INPUT_CNT_2: str  # 입력수2 — 정렬2기준 - 상위(1)하위(2)
    FID_RANK_SORT_CLS_CODE_3: str  # 순위정렬구분코드3 — 정렬3
    FID_INPUT_CNT_3: str  # 입력수3 — 정렬3기준 - 상위(1)하위(2)
    FID_TRGT_CLS_CODE: str  # 대상구분코드 — 0:발행회사종목코드,1:기초자산종목코드,2:FID시장구분코드,3:FID입력날짜1(상장일), 4:FID입력날짜2(만기일),5:LP회원사종목코드,6:행사가기초자산비교>=(1) <=(2), 7:잔존일 이상 이하, 8:현재가, 9:전일대비율,
    FID_INPUT_ISCD: str  # 입력종목코드 — 발행사종목코드전체(00000)
    FID_UNAS_INPUT_ISCD: str  # 기초자산입력종목코드
    FID_MRKT_CLS_CODE: str  # 시장구분코드 — 권리유형전체(A)콜(CO)풋(PO)
    FID_INPUT_DATE_1: str  # 입력날짜1 — 상장일전체(0)금일(1)7일이하(2)8~30일(3)31~90일(4)
    FID_INPUT_DATE_2: str  # 입력날짜2 — 만기일전체(0)1개월(1)1~2(2)2~3(3)3~6(4)6~9(5)9~12(6)12이상(7)
    FID_INPUT_ISCD_2: str  # 입력종목코드2
    FID_ETC_CLS_CODE: str  # 기타구분코드 — 행사가전체(0)>=(1)
    FID_INPUT_RMNN_DYNU_1: str  # 입력잔존일수1 — 잔존일이상
    FID_INPUT_RMNN_DYNU_2: str  # 입력잔존일수2 — 잔존일이하
    FID_PRPR_CNT1: str  # 현재가수1 — 현재가이상
    FID_PRPR_CNT2: str  # 현재가수2 — 현재가이하
    FID_RSFL_RATE1: str  # 등락비율1 — 전일대비율이상
    FID_RSFL_RATE2: str  # 등락비율2 — 전일대비율이하
    FID_VOL1: str  # 거래량1 — 거래량이상
    FID_VOL2: str  # 거래량2 — 거래량이하
    FID_APLY_RANG_PRC_1: str  # 적용범위가격1 — 최종거래일from
    FID_APLY_RANG_PRC_2: str  # 적용범위가격2 — 최종거래일to
    FID_LVRG_VAL1: str  # 레버리지값1
    FID_LVRG_VAL2: str  # 레버리지값2
    FID_VOL3: str  # 거래량3 — LP종료일from
    FID_VOL4: str  # 거래량4 — LP종료일to
    FID_INTS_VLTL1: str  # 내재변동성1 — 내재변동성이상
    FID_INTS_VLTL2: str  # 내재변동성2 — 내재변동성이하
    FID_PRMM_VAL1: str  # 프리미엄값1 — 프리미엄이상
    FID_PRMM_VAL2: str  # 프리미엄값2 — 프리미엄이하
    FID_GEAR1: str  # 기어링1 — 기어링이상
    FID_GEAR2: str  # 기어링2 — 기어링이하
    FID_PRLS_QRYR_RATE1: str  # 손익분기비율1 — 손익분기이상
    FID_PRLS_QRYR_RATE2: str  # 손익분기비율2 — 손익분기이하
    FID_DELTA1: str  # 델타1 — 델타이상
    FID_DELTA2: str  # 델타2 — 델타이하
    FID_ACPR1: str  # 행사가1
    FID_ACPR2: str  # 행사가2
    FID_STCK_CNVR_RATE1: str  # 주식전환비율1 — 전환비율이상
    FID_STCK_CNVR_RATE2: str  # 주식전환비율2 — 전환비율이하
    FID_DIV_CLS_CODE: str  # 분류구분코드 — 0:전체,1:일반,2:조기종료
    FID_PRIT1: str  # 패리티1 — 패리티이상
    FID_PRIT2: str  # 패리티2 — 패리티이하
    FID_CFP1: str  # 자본지지점1 — 배리어이상
    FID_CFP2: str  # 자본지지점2 — 배리어이하
    FID_INPUT_NMIX_PRICE_1: str  # 지수가격1 — LP보유비율이상
    FID_INPUT_NMIX_PRICE_2: str  # 지수가격2 — LP보유비율이하
    FID_EGEA_VAL1: str  # E기어링값1 — 접근도이상
    FID_EGEA_VAL2: str  # E기어링값2 — 접근도이하
    FID_INPUT_DVDN_ERT: str  # 배당수익율 — 손익분기점이상
    FID_INPUT_HIST_VLTL: str  # 역사적변동성 — 손익분기점이하
    FID_THETA1: str  # 세타1 — MONEYNESS이상
    FID_THETA2: str  # 세타2 — MONEYNESS이하

class CondSearchResponse_Output1Item(KisBaseModel):
    """nested item."""

    bond_shrn_iscd: str | None = None  # 채권단축종목코드
    hts_kor_isnm: str | None = None  # HTS한글종목명
    rght_type_name: str | None = None  # 권리유형명
    elw_prpr: str | None = None  # ELW현재가
    prdy_vrss: str | None = None  # 전일대비
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_ctrt: str | None = None  # 전일대비율
    acml_vol: str | None = None  # 누적거래량
    acpr: str | None = None  # 행사가
    stck_cnvr_rate: str | None = None  # 주식전환비율
    stck_lstn_date: str | None = None  # 주식상장일자
    stck_last_tr_date: str | None = None  # 주식최종거래일자
    hts_rmnn_dynu: str | None = None  # HTS잔존일수
    unas_isnm: str | None = None  # 기초자산종목명
    unas_prpr: str | None = None  # 기초자산현재가
    unas_prdy_vrss: str | None = None  # 기초자산전일대비
    unas_prdy_vrss_sign: str | None = None  # 기초자산전일대비부호
    unas_prdy_ctrt: str | None = None  # 기초자산전일대비율
    unas_acml_vol: str | None = None  # 기초자산누적거래량
    moneyness: str | None = None  # MONEYNESS
    atm_cls_name: str | None = None  # ATM구분명
    prit: str | None = None  # 패리티
    delta_val: str | None = None  # 델타값
    hts_ints_vltl: str | None = None  # HTS내재변동성
    tmvl_val: str | None = None  # 시간가치값
    gear: str | None = None  # 기어링
    lvrg_val: str | None = None  # 레버리지값
    prls_qryr_rate: str | None = None  # 손익분기비율
    cfp: str | None = None  # 자본지지점
    lstn_stcn: str | None = None  # 상장주수
    pblc_co_name: str | None = None  # 발행회사명
    lp_mbcr_name: str | None = None  # LP회원사명
    lp_hldn_rate: str | None = None  # LP보유비율
    elw_rght_form: str | None = None  # ELW권리형태
    elw_ko_barrier: str | None = None  # 조기종료발생기준가격
    apprch_rate: str | None = None  # 접근도
    unas_shrn_iscd: str | None = None  # 기초자산단축종목코드
    mtrt_date: str | None = None  # 만기일자
    prmm_val: str | None = None  # 프리미엄값
    stck_lp_fin_date: str | None = None  # 주식LP종료일자
    tick_conv_prc: str | None = None  # 틱환산가
    prls_qryr_stpr_prc: str | None = None  # 손익분기주가가격
    lp_hvol: str | None = None  # LP보유량

class CondSearchResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[CondSearchResponse_Output1Item] = []  # 응답상세 — array

class CondSearchExecutor(ApiExecutor[CondSearchRequest, CondSearchResponse]):
    """ELW 종목검색 [국내주식-166]."""

    # ELW 종목검색 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0291] ELW 종목검색 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 한 번의 호출에 최대 100건까지 확인 가능합니다.

    PATH = "/uapi/elw/v1/quotations/cond-search"
    METHOD = "GET"
    RESPONSE_TYPE = CondSearchResponse
    TR_ID = "FHKEW15100000"
