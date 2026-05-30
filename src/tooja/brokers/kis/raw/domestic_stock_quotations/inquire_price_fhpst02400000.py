"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePriceFhpst02400000Request(KisBaseModel):
    """요청."""

    fid_input_iscd: str  # FID 입력 종목코드 — 종목코드
    fid_cond_mrkt_div_code: str  # FID 조건 시장 분류 코드 — J

class InquirePriceFhpst02400000Response_OutputItem(KisBaseModel):
    """nested item."""

    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_vrss: str | None = None  # 전일 대비
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    prdy_vol: str | None = None  # 전일 거래량
    stck_mxpr: str | None = None  # 주식 상한가
    stck_llam: str | None = None  # 주식 하한가
    stck_prdy_clpr: str | None = None  # 주식 전일 종가
    stck_oprc: str | None = None  # 주식 시가2
    prdy_clpr_vrss_oprc_rate: str | None = None  # 전일 종가 대비 시가2 비율
    stck_hgpr: str | None = None  # 주식 최고가
    prdy_clpr_vrss_hgpr_rate: str | None = None  # 전일 종가 대비 최고가 비율
    stck_lwpr: str | None = None  # 주식 최저가
    prdy_clpr_vrss_lwpr_rate: str | None = None  # 전일 종가 대비 최저가 비율
    prdy_last_nav: str | None = None  # 전일 최종 NAV
    nav: str | None = None  # NAV
    nav_prdy_vrss: str | None = None  # NAV 전일 대비
    nav_prdy_vrss_sign: str | None = None  # NAV 전일 대비 부호
    nav_prdy_ctrt: str | None = None  # NAV 전일 대비율
    trc_errt: str | None = None  # 추적 오차율
    stck_sdpr: str | None = None  # 주식 기준가
    stck_sspr: str | None = None  # 주식 대용가
    nmix_ctrt: str | None = None  # 지수 대비율
    etf_crcl_stcn: str | None = None  # ETF 유통 주수
    etf_ntas_ttam: str | None = None  # ETF 순자산 총액
    etf_frcr_ntas_ttam: str | None = None  # ETF 외화 순자산 총액
    frgn_limt_rate: str | None = None  # 외국인 한도 비율
    frgn_oder_able_qty: str | None = None  # 외국인 주문 가능 수량
    etf_cu_unit_scrt_cnt: str | None = None  # ETF CU 단위 증권 수
    etf_cnfg_issu_cnt: str | None = None  # ETF 구성 종목 수
    etf_dvdn_cycl: str | None = None  # ETF 배당 주기
    crcd: str | None = None  # 통화 코드
    etf_crcl_ntas_ttam: str | None = None  # ETF 유통 순자산 총액
    etf_frcr_crcl_ntas_ttam: str | None = None  # ETF 외화 유통 순자산 총액
    etf_frcr_last_ntas_wrth_val: str | None = None  # ETF 외화 최종 순자산 가치 값
    lp_oder_able_cls_code: str | None = None  # LP 주문 가능 구분 코드
    stck_dryy_hgpr: str | None = None  # 주식 연중 최고가
    dryy_hgpr_vrss_prpr_rate: str | None = None  # 연중 최고가 대비 현재가 비율
    dryy_hgpr_date: str | None = None  # 연중 최고가 일자
    stck_dryy_lwpr: str | None = None  # 주식 연중 최저가
    dryy_lwpr_vrss_prpr_rate: str | None = None  # 연중 최저가 대비 현재가 비율
    dryy_lwpr_date: str | None = None  # 연중 최저가 일자
    bstp_kor_isnm: str | None = None  # 업종 한글 종목명 — ※ 거래소 정보로 특정 종목은 업종구분이 없어 데이터 미회신
    vi_cls_code: str | None = None  # VI적용구분코드
    lstn_stcn: str | None = None  # 상장 주수
    frgn_hldn_qty: str | None = None  # 외국인 보유 수량
    frgn_hldn_qty_rate: str | None = None  # 외국인 보유 수량 비율
    etf_trc_ert_mltp: str | None = None  # ETF 추적 수익률 배수
    dprt: str | None = None  # 괴리율
    mbcr_name: str | None = None  # 회원사 명
    stck_lstn_date: str | None = None  # 주식 상장 일자
    mtrt_date: str | None = None  # 만기 일자
    shrg_type_code: str | None = None  # 분배금형태코드
    lp_hldn_rate: str | None = None  # LP 보유 비율
    etf_trgt_nmix_bstp_code: str | None = None  # ETF대상지수업종코드
    etf_div_name: str | None = None  # ETF 분류 명
    etf_rprs_bstp_kor_isnm: str | None = None  # ETF 대표 업종 한글 종목명
    lp_hldn_vol: str | None = None  # ETN LP 보유량

class InquirePriceFhpst02400000Response(KisCommonResponse):
    """응답 본문."""

    output: InquirePriceFhpst02400000Response_OutputItem | None = None  # 응답상세

class InquirePriceFhpst02400000Executor(ApiExecutor[InquirePriceFhpst02400000Request, InquirePriceFhpst02400000Response]):
    """ETF/ETN 현재가[v1_국내주식-068]."""

    # ETF/ETN 현재가 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0240] ETF/ETN 현재가 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/etfetn/v1/quotations/inquire-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePriceFhpst02400000Response
    TR_ID = "FHPST02400000"
