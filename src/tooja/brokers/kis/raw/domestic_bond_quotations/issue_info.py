"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class IssueInfoRequest(KisBaseModel):
    """요청."""

    PDNO: str  # 사용자권한정보 — 채권 종목번호(ex. KR6449111CB8)
    PRDT_TYPE_CD: str  # 거래소코드 — Unique key(302)

class IssueInfoResponse_OutputItem(KisBaseModel):
    """nested item."""

    pdno: str | None = None  # 상품번호
    prdt_type_cd: str | None = None  # 상품유형코드
    prdt_name: str | None = None  # 상품명
    prdt_eng_name: str | None = None  # 상품영문명
    ivst_heed_prdt_yn: str | None = None  # 투자유의상품여부
    exts_yn: str | None = None  # 연장여부
    bond_clsf_cd: str | None = None  # 채권분류코드
    bond_clsf_kor_name: str | None = None  # 채권분류한글명
    papr: str | None = None  # 액면가
    int_mned_dvsn_cd: str | None = None  # 이자월말구분코드
    rvnu_shap_cd: str | None = None  # 매출형태코드
    issu_amt: str | None = None  # 발행금액
    lstg_rmnd: str | None = None  # 상장잔액
    int_dfrm_mcnt: str | None = None  # 이자지급개월수
    bond_int_dfrm_mthd_cd: str | None = None  # 채권이자지급방법코드
    splt_rdpt_rcnt: str | None = None  # 분할상환횟수
    prca_dfmt_term_mcnt: str | None = None  # 원금거치기간개월수
    int_anap_dvsn_cd: str | None = None  # 이자선후급구분코드
    bond_rght_dvsn_cd: str | None = None  # 채권권리구분코드
    prdt_pclc_text: str | None = None  # 상품특성내용
    prdt_abrv_name: str | None = None  # 상품약어명
    prdt_eng_abrv_name: str | None = None  # 상품영문약어명
    sprx_psbl_yn: str | None = None  # 분리과세가능여부
    pbff_pplc_ofrg_mthd_cd: str | None = None  # 공모사모모집방법코드
    cmco_cd: str | None = None  # 주간사코드
    issu_istt_cd: str | None = None  # 발행기관코드
    issu_istt_name: str | None = None  # 발행기관명
    pnia_dfrm_agcy_istt_cd: str | None = None  # 원리금지급대행기관코드
    dsct_ec_rt: str | None = None  # 할인할증율
    srfc_inrt: str | None = None  # 표면이율
    expd_rdpt_rt: str | None = None  # 만기상환율
    expd_asrc_erng_rt: str | None = None  # 만기보장수익율
    bond_grte_istt_name: str | None = None  # 채권보증기관명
    int_dfrm_day_type_cd: str | None = None  # 이자지급일유형코드
    ksd_int_calc_unit_cd: str | None = None  # 증권예탁결제원이자계산단위코드
    int_wunt_uder_prcs_dvsn_cd: str | None = None  # 이자원화단위미만처리구분코드
    rvnu_dt: str | None = None  # 매출일자
    issu_dt: str | None = None  # 발행일자
    lstg_dt: str | None = None  # 상장일자
    expd_dt: str | None = None  # 만기일자
    rdpt_dt: str | None = None  # 상환일자
    sbst_pric: str | None = None  # 대용가격
    rgbf_int_dfrm_dt: str | None = None  # 직전이자지급일자
    nxtm_int_dfrm_dt: str | None = None  # 차기이자지급일자
    frst_int_dfrm_dt: str | None = None  # 최초이자지급일자
    ecis_pric: str | None = None  # 행사가격
    rght_stck_std_pdno: str | None = None  # 권리주식표준상품번호
    ecis_opng_dt: str | None = None  # 행사개시일자
    ecis_end_dt: str | None = None  # 행사종료일자
    bond_rvnu_mthd_cd: str | None = None  # 채권매출방법코드
    oprt_stfno: str | None = None  # 조작직원번호
    oprt_stff_name: str | None = None  # 조작직원명
    rgbf_int_dfrm_wday: str | None = None  # 직전이자지급요일
    nxtm_int_dfrm_wday: str | None = None  # 차기이자지급요일
    kis_crdt_grad_text: str | None = None  # 한국신용평가신용등급내용
    kbp_crdt_grad_text: str | None = None  # 한국채권평가신용등급내용
    nice_crdt_grad_text: str | None = None  # 한국신용정보신용등급내용
    fnp_crdt_grad_text: str | None = None  # 에프앤자산평가신용등급내용
    dpsi_psbl_yn: str | None = None  # 예탁가능여부
    pnia_int_calc_unpr: str | None = None  # 원리금이자계산단가
    prcm_idx_bond_yn: str | None = None  # 물가지수채권여부
    expd_exts_srdp_rcnt: str | None = None  # 만기연장분할상환횟수
    expd_exts_srdp_rt: str | None = None  # 만기연장분할상환율
    loan_psbl_yn: str | None = None  # 대출가능여부
    grte_dvsn_cd: str | None = None  # 보증구분코드
    fnrr_rank_dvsn_cd: str | None = None  # 선후순위구분코드
    krx_lstg_abol_dvsn_cd: str | None = None  # 한국거래소상장폐지구분코드
    asst_rqdi_dvsn_cd: str | None = None  # 자산유동화구분코드
    opcb_dvsn_cd: str | None = None  # 옵션부사채구분코드
    crfd_item_yn: str | None = None  # 크라우드펀딩종목여부
    crfd_item_rstc_cclc_dt: str | None = None  # 크라우드펀딩종목제한해지일자
    bond_nmpr_unit_pric: str | None = None  # 채권호가단위가격
    ivst_heed_bond_dvsn_name: str | None = None  # 투자유의채권구분명
    add_erng_rt: str | None = None  # 추가수익율
    add_erng_rt_aply_dt: str | None = None  # 추가수익율적용일자
    bond_tr_stop_dvsn_cd: str | None = None  # 채권거래정지구분코드
    ivst_heed_bond_dvsn_cd: str | None = None  # 투자유의채권구분코드
    pclr_cndt_text: str | None = None  # 특이조건내용
    hbbd_yn: str | None = None  # 하이브리드채권여부
    cdtl_cptl_scty_type_cd: str | None = None  # 조건부자본증권유형코드
    elec_scty_yn: str | None = None  # 전자증권여부
    sq1_clop_ecis_opng_dt: str | None = None  # 1차콜옵션행사개시일자
    frst_erlm_stfno: str | None = None  # 최초등록직원번호
    frst_erlm_dt: str | None = None  # 최초등록일자
    frst_erlm_tmd: str | None = None  # 최초등록시각
    tlg_rcvg_dtl_dtime: str | None = None  # 전문수신상세일시

class IssueInfoResponse(KisCommonResponse):
    """응답 본문."""

    output: IssueInfoResponse_OutputItem | None = None  # 응답상세

class IssueInfoExecutor(ApiExecutor[IssueInfoRequest, IssueInfoResponse]):
    """장내채권 발행정보[국내주식-156]."""

    # 장내채권 발행정보 API입니다. 한국투자 HTS(eFriend Plus) &gt; [7216] 채권 발행정보 화면의 상단 채권정보 데이터를 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-bond/v1/quotations/issue-info"
    METHOD = "GET"
    RESPONSE_TYPE = IssueInfoResponse
    TR_ID = "CTPF1101R"
