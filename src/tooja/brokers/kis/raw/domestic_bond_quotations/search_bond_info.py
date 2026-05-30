"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class SearchBondInfoRequest(KisBaseModel):
    """요청."""

    PDNO: str  # 상품번호
    PRDT_TYPE_CD: str  # 상품유형코드 — Unique key(302)

class SearchBondInfoResponse_OutputItem(KisBaseModel):
    """nested item."""

    pdno: str | None = None  # 상품번호
    prdt_type_cd: str | None = None  # 상품유형코드
    ksd_bond_item_name: str | None = None  # 증권예탁결제원채권종목명
    ksd_bond_item_eng_name: str | None = None  # 증권예탁결제원채권종목영문명
    ksd_bond_lstg_type_cd: str | None = None  # 증권예탁결제원채권상장유형코드
    ksd_ofrg_dvsn_cd: str | None = None  # 증권예탁결제원모집구분코드
    ksd_bond_int_dfrm_dvsn_cd: str | None = None  # 증권예탁결제원채권이자지급구분
    issu_dt: str | None = None  # 발행일자
    rdpt_dt: str | None = None  # 상환일자
    rvnu_dt: str | None = None  # 매출일자
    iso_crcy_cd: str | None = None  # 통화코드
    mdwy_rdpt_dt: str | None = None  # 중도상환일자
    ksd_rcvg_bond_dsct_rt: str | None = None  # 증권예탁결제원수신채권할인율
    ksd_rcvg_bond_srfc_inrt: str | None = None  # 증권예탁결제원수신채권표면이율
    bond_expd_rdpt_rt: str | None = None  # 채권만기상환율
    ksd_prca_rdpt_mthd_cd: str | None = None  # 증권예탁결제원원금상환방법코드
    int_caltm_mcnt: str | None = None  # 이자계산기간개월수
    ksd_int_calc_unit_cd: str | None = None  # 증권예탁결제원이자계산단위코드 — 1.발행금액 2.만원 3.십만원 4.백만원
    uval_cut_dvsn_cd: str | None = None  # 절상절사구분코드
    uval_cut_dcpt_dgit: str | None = None  # 절상절사소수점자릿수
    ksd_dydv_caltm_aply_dvsn_cd: str | None = None  # 증권예탁결제원일할계산기간적용
    dydv_calc_dcnt: str | None = None  # 일할계산일수
    bond_expd_asrc_erng_rt: str | None = None  # 채권만기보장수익율
    padf_plac_hdof_name: str | None = None  # 원리금지급장소본점명
    lstg_dt: str | None = None  # 상장일자
    lstg_abol_dt: str | None = None  # 상장폐지일자
    ksd_bond_issu_mthd_cd: str | None = None  # 증권예탁결제원채권발행방법코드
    laps_indf_yn: str | None = None  # 경과이자지급여부
    ksd_lhdy_pnia_dfrm_mthd_cd: str | None = None  # 증권예탁결제원공휴일원리금지급
    frst_int_dfrm_dt: str | None = None  # 최초이자지급일자
    ksd_prcm_lnkg_gvbd_yn: str | None = None  # 증권예탁결제원물가연동국고채여
    dpsi_end_dt: str | None = None  # 예탁종료일자
    dpsi_strt_dt: str | None = None  # 예탁시작일자
    dpsi_psbl_yn: str | None = None  # 예탁가능여부
    atyp_rdpt_bond_erlm_yn: str | None = None  # 비정형상환채권등록여부
    dshn_occr_yn: str | None = None  # 부도발생여부
    expd_exts_yn: str | None = None  # 만기연장여부
    pclr_ptcr_text: str | None = None  # 특이사항내용
    dpsi_psbl_excp_stat_cd: str | None = None  # 예탁가능예외상태코드
    expd_exts_srdp_rcnt: str | None = None  # 만기연장분할상환횟수
    expd_exts_srdp_rt: str | None = None  # 만기연장분할상환율
    expd_rdpt_rt: str | None = None  # 만기상환율
    expd_asrc_erng_rt: str | None = None  # 만기보장수익율
    bond_int_dfrm_mthd_cd: str | None = None  # 채권이자지급방법코드 — 01.할인채 02.복리채 03.이표채.확정금리 04.이표채.금리연동 05.이표채.변동금리 06.단리채 07.분할채 09.복5단2 19.기타.고정금리 29.기타.변동금리
    int_dfrm_day_type_cd: str | None = None  # 이자지급일유형코드 — 01.발행일 02.만기일 03.특정일
    prca_dfmt_term_mcnt: str | None = None  # 원금거치기간개월수
    splt_rdpt_rcnt: str | None = None  # 분할상환횟수
    rgbf_int_dfrm_dt: str | None = None  # 직전이자지급일자
    nxtm_int_dfrm_dt: str | None = None  # 차기이자지급일자
    sprx_psbl_yn: str | None = None  # 분리과세가능여부
    ictx_rt_dvsn_cd: str | None = None  # 소득세율구분코드
    bond_clsf_cd: str | None = None  # 채권분류코드
    bond_clsf_kor_name: str | None = None  # 채권분류한글명
    int_mned_dvsn_cd: str | None = None  # 이자월말구분코드 — 1.일자기준 2.말일기준
    pnia_int_calc_unpr: str | None = None  # 원리금이자계산단가
    frn_intr: str | None = None  # FRN금리
    aply_day_prcm_idx_lnkg_cefc: str | None = None  # 적용일물가지수연동계수
    ksd_expd_dydv_calc_bass_cd: str | None = None  # 증권예탁결제원만기일할계산기준
    expd_dydv_calc_dcnt: str | None = None  # 만기일할계산일수
    ksd_cbbw_dvsn_cd: str | None = None  # 증권예탁결제원신종사채구분코드
    crfd_item_yn: str | None = None  # 크라우드펀딩종목여부
    pnia_bank_ofdy_dfrm_mthd_cd: str | None = None  # 원리금은행휴무일지급방법코드
    qib_yn: str | None = None  # QIB여부
    qib_cclc_dt: str | None = None  # QIB해지일자
    csbd_yn: str | None = None  # 영구채여부
    csbd_cclc_dt: str | None = None  # 영구채해지일자
    ksd_opcb_yn: str | None = None  # 증권예탁결제원옵션부사채여부
    ksd_sodn_yn: str | None = None  # 증권예탁결제원후순위채권여부
    ksd_rqdi_scty_yn: str | None = None  # 증권예탁결제원유동화증권여부
    elec_scty_yn: str | None = None  # 전자증권여부
    rght_ecis_mbdy_dvsn_cd: str | None = None  # 권리행사주체구분코드
    int_rkng_mthd_dvsn_cd: str | None = None  # 이자산정방법구분코드
    ofrg_dvsn_cd: str | None = None  # 모집구분코드
    ksd_tot_issu_amt: str | None = None  # 증권예탁결제원총발행금액
    next_indf_chk_ecls_yn: str | None = None  # 다음이자지급체크제외여부
    ksd_bond_intr_dvsn_cd: str | None = None  # 증권예탁결제원채권금리구분코드
    ksd_inrt_aply_dvsn_cd: str | None = None  # 증권예탁결제원이율적용구분코드
    krx_issu_istt_cd: str | None = None  # KRX발행기관코드
    ksd_indf_frqc_uder_calc_cd: str | None = None  # 증권예탁결제원이자지급주기미만
    ksd_indf_frqc_uder_calc_dcnt: str | None = None  # 증권예탁결제원이자지급주기미만
    tlg_rcvg_dtl_dtime: str | None = None  # 전문수신상세일시

class SearchBondInfoResponse(KisCommonResponse):
    """응답 본문."""

    output: SearchBondInfoResponse_OutputItem | None = None  # 응답상세

class SearchBondInfoExecutor(ApiExecutor[SearchBondInfoRequest, SearchBondInfoResponse]):
    """장내채권 기본조회 [국내주식-129]."""

    # 장내채권 기본조회 API입니다. 장내채권의 상품정보를 확인 가능합니다.

    PATH = "/uapi/domestic-bond/v1/quotations/search-bond-info"
    METHOD = "GET"
    RESPONSE_TYPE = SearchBondInfoResponse
    TR_ID = "CTPF1114R"
