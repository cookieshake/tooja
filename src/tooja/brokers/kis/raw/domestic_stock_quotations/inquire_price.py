"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — J:KRX, NX:NXT, UN:통합
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목코드 (ex 005930 삼성전자) // ETN은 종목코드 6자리 앞에 Q 입력 필수

class InquirePriceResponse_OutputItem(KisBaseModel):
    """nested item."""

    iscd_stat_cls_code: str | None = None  # 종목 상태 구분 코드 — 51 : 관리종목 52 : 투자위험 53 : 투자경고 54 : 투자주의 55 : 신용가능 57 : 증거금 100% 58 : 거래정지 59 : 단기과열종목
    marg_rate: str | None = None  # 증거금 비율
    rprs_mrkt_kor_name: str | None = None  # 대표 시장 한글 명
    new_hgpr_lwpr_cls_code: str | None = None  # 신 고가 저가 구분 코드
    bstp_kor_isnm: str | None = None  # 업종 한글 종목명
    temp_stop_yn: str | None = None  # 임시 정지 여부
    oprc_rang_cont_yn: str | None = None  # 시가 범위 연장 여부
    clpr_rang_cont_yn: str | None = None  # 종가 범위 연장 여부
    crdt_able_yn: str | None = None  # 신용 가능 여부
    grmn_rate_cls_code: str | None = None  # 보증금 비율 구분 코드
    elw_pblc_yn: str | None = None  # ELW 발행 여부
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    acml_vol: str | None = None  # 누적 거래량
    prdy_vrss_vol_rate: str | None = None  # 전일 대비 거래량 비율
    stck_oprc: str | None = None  # 주식 시가2
    stck_hgpr: str | None = None  # 주식 최고가
    stck_lwpr: str | None = None  # 주식 최저가
    stck_mxpr: str | None = None  # 주식 상한가
    stck_llam: str | None = None  # 주식 하한가
    stck_sdpr: str | None = None  # 주식 기준가
    wghn_avrg_stck_prc: str | None = None  # 가중 평균 주식 가격
    hts_frgn_ehrt: str | None = None  # HTS 외국인 소진율
    frgn_ntby_qty: str | None = None  # 외국인 순매수 수량
    pgtr_ntby_qty: str | None = None  # 프로그램매매 순매수 수량
    pvt_scnd_dmrs_prc: str | None = None  # 피벗 2차 디저항 가격
    pvt_frst_dmrs_prc: str | None = None  # 피벗 1차 디저항 가격
    pvt_pont_val: str | None = None  # 피벗 포인트 값
    pvt_frst_dmsp_prc: str | None = None  # 피벗 1차 디지지 가격
    pvt_scnd_dmsp_prc: str | None = None  # 피벗 2차 디지지 가격
    dmrs_val: str | None = None  # 디저항 값
    dmsp_val: str | None = None  # 디지지 값
    cpfn: str | None = None  # 자본금
    rstc_wdth_prc: str | None = None  # 제한 폭 가격
    stck_fcam: str | None = None  # 주식 액면가
    stck_sspr: str | None = None  # 주식 대용가
    aspr_unit: str | None = None  # 호가단위
    hts_deal_qty_unit_val: str | None = None  # HTS 매매 수량 단위 값
    lstn_stcn: str | None = None  # 상장 주수
    hts_avls: str | None = None  # HTS 시가총액
    per: str | None = None  # PER
    pbr: str | None = None  # PBR
    stac_month: str | None = None  # 결산 월
    vol_tnrt: str | None = None  # 거래량 회전율
    eps: str | None = None  # EPS
    bps: str | None = None  # BPS
    d250_hgpr: str | None = None  # 250일 최고가
    d250_hgpr_date: str | None = None  # 250일 최고가 일자
    d250_hgpr_vrss_prpr_rate: str | None = None  # 250일 최고가 대비 현재가 비율
    d250_lwpr: str | None = None  # 250일 최저가
    d250_lwpr_date: str | None = None  # 250일 최저가 일자
    d250_lwpr_vrss_prpr_rate: str | None = None  # 250일 최저가 대비 현재가 비율
    stck_dryy_hgpr: str | None = None  # 주식 연중 최고가
    dryy_hgpr_vrss_prpr_rate: str | None = None  # 연중 최고가 대비 현재가 비율
    dryy_hgpr_date: str | None = None  # 연중 최고가 일자
    stck_dryy_lwpr: str | None = None  # 주식 연중 최저가
    dryy_lwpr_vrss_prpr_rate: str | None = None  # 연중 최저가 대비 현재가 비율
    dryy_lwpr_date: str | None = None  # 연중 최저가 일자
    w52_hgpr: str | None = None  # 52주일 최고가
    w52_hgpr_vrss_prpr_ctrt: str | None = None  # 52주일 최고가 대비 현재가 대비
    w52_hgpr_date: str | None = None  # 52주일 최고가 일자
    w52_lwpr: str | None = None  # 52주일 최저가
    w52_lwpr_vrss_prpr_ctrt: str | None = None  # 52주일 최저가 대비 현재가 대비
    w52_lwpr_date: str | None = None  # 52주일 최저가 일자
    whol_loan_rmnd_rate: str | None = None  # 전체 융자 잔고 비율
    ssts_yn: str | None = None  # 공매도가능여부
    stck_shrn_iscd: str | None = None  # 주식 단축 종목코드
    fcam_cnnm: str | None = None  # 액면가 통화명
    cpfn_cnnm: str | None = None  # 자본금 통화명
    apprch_rate: str | None = None  # 접근도
    frgn_hldn_qty: str | None = None  # 외국인 보유 수량
    vi_cls_code: str | None = None  # VI적용구분코드
    ovtm_vi_cls_code: str | None = None  # 시간외단일가VI적용구분코드
    last_ssts_cntg_qty: str | None = None  # 최종 공매도 체결 수량
    invt_caful_yn: str | None = None  # 투자유의여부
    mrkt_warn_cls_code: str | None = None  # 시장경고코드
    short_over_yn: str | None = None  # 단기과열여부
    sltr_yn: str | None = None  # 정리매매여부
    mang_issu_cls_code: str | None = None  # 관리종목여부

class InquirePriceResponse(KisCommonResponse):
    """응답 본문."""

    output: InquirePriceResponse_OutputItem | None = None  # 응답상세

class InquirePriceExecutor(ApiExecutor[InquirePriceRequest, InquirePriceResponse]):
    """주식현재가 시세[v1_국내주식-008]."""

    # 주식 현재가 시세 API입니다. 실시간 시세를 원하신다면 웹소켓 API를 활용하세요. ※ 종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다. https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePriceResponse
    TR_ID = "FHKST01010100"
