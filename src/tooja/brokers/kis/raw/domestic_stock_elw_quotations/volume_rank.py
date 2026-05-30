"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class VolumeRankRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — W
    FID_COND_SCR_DIV_CODE: str  # 조건화면분류코드 — 20278
    FID_UNAS_INPUT_ISCD: str  # 기초자산입력종목코드 — 000000
    FID_INPUT_ISCD: str  # 발행사 — 00000(전체), 00003(한국투자증권) , 00017(KB증권), 00005(미래에셋주식회사)'
    FID_INPUT_RMNN_DYNU_1: str  # 입력잔존일수
    FID_DIV_CLS_CODE: str  # 콜풋구분코드 — 0(전체), 1(콜), 2(풋)
    FID_INPUT_PRICE_1: str  # 가격(이상) — 거래가격1(이상)
    FID_INPUT_PRICE_2: str  # 가격(이하) — 거래가격1(이하)
    FID_INPUT_VOL_1: str  # 거래량(이상) — 거래량1(이상)
    FID_INPUT_VOL_2: str  # 거래량(이하) — 거래량1(이하)
    FID_INPUT_DATE_1: str  # 조회기준일 — 입력날짜(기준가 조회기준)
    FID_RANK_SORT_CLS_CODE: str  # 순위정렬구분코드 — 0: 거래량순 1: 평균거래증가율 2: 평균거래회전율 3:거래금액순 4: 순매수잔량순 5: 순매도잔량순
    FID_BLNG_CLS_CODE: str  # 소속구분코드 — 0: 전체
    FID_INPUT_ISCD_2: str  # LP발행사 — 0000
    FID_INPUT_DATE_2: str  # 만기일-최종거래일조회 — 공백

class VolumeRankResponse_OutputItem(KisBaseModel):
    """nested item."""

    elw_kor_isnm: str | None = None  # ELW한글종목명
    elw_shrn_iscd: str | None = None  # ELW단축종목코드
    elw_prpr: str | None = None  # ELW현재가
    prdy_vrss: str | None = None  # 전일대비
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_ctrt: str | None = None  # 전일대비율
    lstn_stcn: str | None = None  # 상장주수
    acml_vol: str | None = None  # 누적거래량
    n_prdy_vol: str | None = None  # N전일거래량
    n_prdy_vol_vrss: str | None = None  # N전일거래량대비
    vol_inrt: str | None = None  # 거래량증가율
    vol_tnrt: str | None = None  # 거래량회전율
    nday_vol_tnrt: str | None = None  # N일거래량회전율
    acml_tr_pbmn: str | None = None  # 누적거래대금
    n_prdy_tr_pbmn: str | None = None  # N전일거래대금
    n_prdy_tr_pbmn_vrss: str | None = None  # N전일거래대금대비
    total_askp_rsqn: str | None = None  # 총매도호가잔량
    total_bidp_rsqn: str | None = None  # 총매수호가잔량
    ntsl_rsqn: str | None = None  # 순매도잔량
    ntby_rsqn: str | None = None  # 순매수잔량
    seln_rsqn_rate: str | None = None  # 매도잔량비율
    shnu_rsqn_rate: str | None = None  # 매수2잔량비율
    stck_cnvr_rate: str | None = None  # 주식전환비율
    hts_rmnn_dynu: str | None = None  # HTS잔존일수
    invl_val: str | None = None  # 내재가치값
    tmvl_val: str | None = None  # 시간가치값
    acpr: str | None = None  # 행사가
    lp_mbcr_name: str | None = None  # LP회원사명
    unas_isnm: str | None = None  # 기초자산명
    stck_last_tr_date: str | None = None  # 최종거래일
    unas_shrn_iscd: str | None = None  # 기초자산코드
    prdy_vol: str | None = None  # 전일거래량
    lp_hldn_rate: str | None = None  # LP보유비율
    prit: str | None = None  # 패리티
    prls_qryr_stpr_prc: str | None = None  # 손익분기주가가격
    delta_val: str | None = None  # 델타값
    theta: str | None = None  # 세타
    prls_qryr_rate: str | None = None  # 손익분기비율
    stck_lstn_date: str | None = None  # 주식상장일자
    hts_ints_vltl: str | None = None  # HTS내재변동성
    lvrg_val: str | None = None  # 레버리지값
    lp_ntby_qty: str | None = None  # LP순매도량

class VolumeRankResponse(KisCommonResponse):
    """응답 본문."""

    output: list[VolumeRankResponse_OutputItem] = []  # 응답상세 — array

class VolumeRankExecutor(ApiExecutor[VolumeRankRequest, VolumeRankResponse]):
    """ELW 거래량순위[국내주식-168]."""

    # ELW 거래량순위 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0278] ELW 거래량순위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/elw/v1/ranking/volume-rank"
    METHOD = "GET"
    RESPONSE_TYPE = VolumeRankResponse
    TR_ID = "FHPEW02780000"
