"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class SearchInfoRequest(KisBaseModel):
    """요청."""

    PRDT_TYPE_CD: str  # 상품유형코드 — 512 미국 나스닥 / 513 미국 뉴욕 / 529 미국 아멕스 515 일본 501 홍콩 / 543 홍콩CNY / 558 홍콩USD 507 베트남 하노이 / 508 베트남 호치민 551 중국 상해A / 552 중국 심천A
    PDNO: str  # 상품번호 — 예) AAPL (애플)

class SearchInfoResponse_OutputItem(KisBaseModel):
    """nested item."""

    std_pdno: str | None = None  # 표준상품번호
    prdt_eng_name: str | None = None  # 상품영문명
    natn_cd: str | None = None  # 국가코드
    natn_name: str | None = None  # 국가명
    tr_mket_cd: str | None = None  # 거래시장코드
    tr_mket_name: str | None = None  # 거래시장명
    ovrs_excg_cd: str | None = None  # 해외거래소코드
    ovrs_excg_name: str | None = None  # 해외거래소명
    tr_crcy_cd: str | None = None  # 거래통화코드
    ovrs_papr: str | None = None  # 해외액면가
    crcy_name: str | None = None  # 통화명
    ovrs_stck_dvsn_cd: str | None = None  # 해외주식구분코드 — 01.주식 02.WARRANT 03.ETF 04.우선주
    prdt_clsf_cd: str | None = None  # 상품분류코드
    prdt_clsf_name: str | None = None  # 상품분류명
    sll_unit_qty: str | None = None  # 매도단위수량
    buy_unit_qty: str | None = None  # 매수단위수량
    tr_unit_amt: str | None = None  # 거래단위금액
    lstg_stck_num: str | None = None  # 상장주식수
    lstg_dt: str | None = None  # 상장일자
    ovrs_stck_tr_stop_dvsn_cd: str | None = None  # 해외주식거래정지구분코드 — ※ 해당 값 지연 반영될 수 있는 점 유의 부탁드립니다. 01.정상 02.거래정지(ALL) 03.거래중단 04.매도정지 05.거래정지(위탁) 06.매수정지
    lstg_abol_item_yn: str | None = None  # 상장폐지종목여부
    ovrs_stck_prdt_grp_no: str | None = None  # 해외주식상품그룹번호
    lstg_yn: str | None = None  # 상장여부
    tax_levy_yn: str | None = None  # 세금징수여부
    ovrs_stck_erlm_rosn_cd: str | None = None  # 해외주식등록사유코드
    ovrs_stck_hist_rght_dvsn_cd: str | None = None  # 해외주식이력권리구분코드
    chng_bf_pdno: str | None = None  # 변경전상품번호
    prdt_type_cd_2: str | None = None  # 상품유형코드2
    ovrs_item_name: str | None = None  # 해외종목명
    sedol_no: str | None = None  # SEDOL번호
    blbg_tckr_text: str | None = None  # 블름버그티커내용
    ovrs_stck_etf_risk_drtp_cd: str | None = None  # 해외주식ETF위험지표코드 — 001.ETF 002.ETN 003.ETC(Exchage Traded Commodity) 004.Others(REIT's, Mutual Fund) 005.VIX Underlying ETF 006.VIX Underlying 
    etp_chas_erng_rt_dbnb: str | None = None  # ETP추적수익율배수
    istt_usge_isin_cd: str | None = None  # 기관용도ISIN코드
    mint_svc_yn: str | None = None  # MINT서비스여부
    mint_svc_yn_chng_dt: str | None = None  # MINT서비스여부변경일자
    prdt_name: str | None = None  # 상품명
    lei_cd: str | None = None  # LEI코드
    ovrs_stck_stop_rson_cd: str | None = None  # 해외주식정지사유코드 — 01.권리발생 02.ISIN상이 03.기타 04.급등락종목 05.상장폐지(예정) 06.종목코드,거래소변경 07.PTP종목
    lstg_abol_dt: str | None = None  # 상장폐지일자
    mini_stk_tr_stat_dvsn_cd: str | None = None  # 미니스탁거래상태구분코드 — 01.정상 02.매매 불가 03.매수 불가 04.매도 불가
    mint_frst_svc_erlm_dt: str | None = None  # MINT최초서비스등록일자
    mint_dcpt_trad_psbl_yn: str | None = None  # MINT소수점매매가능여부
    mint_fnum_trad_psbl_yn: str | None = None  # MINT정수매매가능여부
    mint_cblc_cvsn_ipsb_yn: str | None = None  # MINT잔고전환불가여부
    ptp_item_yn: str | None = None  # PTP종목여부
    ptp_item_trfx_exmt_yn: str | None = None  # PTP종목양도세면제여부
    ptp_item_trfx_exmt_strt_dt: str | None = None  # PTP종목양도세면제시작일자
    ptp_item_trfx_exmt_end_dt: str | None = None  # PTP종목양도세면제종료일자
    dtm_tr_psbl_yn: str | None = None  # 주간거래가능여부
    sdrf_stop_ecls_yn: str | None = None  # 급등락정지제외여부
    sdrf_stop_ecls_erlm_dt: str | None = None  # 급등락정지제외등록일자
    memo_text1: str | None = None  # 메모내용1
    ovrs_now_pric1: str | None = None  # 해외현재가격1 — 23.5
    last_rcvg_dtime: str | None = None  # 최종수신일시
    sgle_item_lvrg_etp_yn: str | None = None  # 단일종목레버리지ETP여부

class SearchInfoResponse(KisCommonResponse):
    """응답 본문."""

    output: SearchInfoResponse_OutputItem | None = None  # 응답상세1

class SearchInfoExecutor(ApiExecutor[SearchInfoRequest, SearchInfoResponse]):
    """해외주식 상품기본정보[v1_해외주식-034]."""

    # 해외주식 상품기본정보 API입니다. 시세제공기관(연합)에서 제공하는 해외주식 상품기본정보 데이터를 확인하실 수 있습니다. ※ 해당자료는 시세제공기관(연합)의 자료를 제공하고 있으며, 오류와 지연이 발생할 수 있습니다. ※ 위 정보에 의한 투자판단의 최종책임은 정보이용자에게 있으며, 당사와 시세제공기관(연합)는 어떠한 법적인 책임도 지지 않사오니 투자에 참고로만 이용하시기 바랍니다.

    PATH = "/uapi/overseas-price/v1/quotations/search-info"
    METHOD = "GET"
    RESPONSE_TYPE = SearchInfoResponse
    TR_ID = "CTPF1702R"
