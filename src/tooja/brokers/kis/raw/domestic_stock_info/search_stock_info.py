"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class SearchStockInfoRequest(KisBaseModel):
    """요청."""

    PRDT_TYPE_CD: str  # 상품유형코드 — 300: 주식, ETF, ETN, ELW 301 : 선물옵션 302 : 채권 306 : ELS'
    PDNO: str  # 상품번호 — 종목번호 (6자리) ETN의 경우, Q로 시작 (EX. Q500001)

class SearchStockInfoResponse_OutputItem(KisBaseModel):
    """nested item."""

    pdno: str | None = None  # 상품번호
    prdt_type_cd: str | None = None  # 상품유형코드
    mket_id_cd: str | None = None  # 시장ID코드 — AGR.농축산물파생 BON.채권파생 CMD.일반상품시장 CUR.통화파생 ENG.에너지파생 EQU.주식파생 ETF.ETF파생 IRT.금리파생 KNX.코넥스 KSQ.코스닥 MTL.금속파생 SPI.주가지수파생 STK.유가증권
    scty_grp_id_cd: str | None = None  # 증권그룹ID코드 — BC.수익증권 DR.주식예탁증서 EF.ETF EN.ETN EW.ELW FE.해외ETF FO.선물옵션 FS.외국주권 FU.선물 FX.플렉스 선물 GD.금현물 IC.투자계약증권 IF.사회간접자본투융자회사 KN.코넥스주권 MF.투자회사 
    excg_dvsn_cd: str | None = None  # 거래소구분코드 — 01.한국증권 02.증권거래소 03.코스닥 04.K-OTC 05.선물거래소 06.CME 07.EUREX 21.금현물 50.미국주간 51.홍콩 52.상해B 53.심천 54.홍콩거래소 55.미국 56.일본 57.상해A 58.심천A 59.
    setl_mmdd: str | None = None  # 결산월일
    lstg_stqt: str | None = None  # 상장주수
    lstg_cptl_amt: str | None = None  # 상장자본금액
    cpta: str | None = None  # 자본금
    papr: str | None = None  # 액면가
    issu_pric: str | None = None  # 발행가격
    kospi200_item_yn: str | None = None  # 코스피200종목여부
    scts_mket_lstg_dt: str | None = None  # 유가증권시장상장일자
    scts_mket_lstg_abol_dt: str | None = None  # 유가증권시장상장폐지일자
    kosdaq_mket_lstg_dt: str | None = None  # 코스닥시장상장일자
    kosdaq_mket_lstg_abol_dt: str | None = None  # 코스닥시장상장폐지일자
    frbd_mket_lstg_dt: str | None = None  # 프리보드시장상장일자
    frbd_mket_lstg_abol_dt: str | None = None  # 프리보드시장상장폐지일자
    reits_kind_cd: str | None = None  # 리츠종류코드
    etf_dvsn_cd: str | None = None  # ETF구분코드
    oilf_fund_yn: str | None = None  # 유전펀드여부
    idx_bztp_lcls_cd: str | None = None  # 지수업종대분류코드
    idx_bztp_mcls_cd: str | None = None  # 지수업종중분류코드
    idx_bztp_scls_cd: str | None = None  # 지수업종소분류코드
    stck_kind_cd: str | None = None  # 주식종류코드 — 000.해당사항없음 101.보통주 201.우선주 202.2우선주 203.3우선주 204.4우선주 205.5우선주 206.6우선주 207.7우선주 208.8우선주 209.9우선주 210.10우선주 211.11우선주 212.12우선주 21
    mfnd_opng_dt: str | None = None  # 뮤추얼펀드개시일자
    mfnd_end_dt: str | None = None  # 뮤추얼펀드종료일자
    dpsi_erlm_cncl_dt: str | None = None  # 예탁등록취소일자
    etf_cu_qty: str | None = None  # ETFCU수량
    prdt_name: str | None = None  # 상품명
    prdt_name120: str | None = None  # 상품명120
    prdt_abrv_name: str | None = None  # 상품약어명
    std_pdno: str | None = None  # 표준상품번호
    prdt_eng_name: str | None = None  # 상품영문명
    prdt_eng_name120: str | None = None  # 상품영문명120
    prdt_eng_abrv_name: str | None = None  # 상품영문약어명
    dpsi_aptm_erlm_yn: str | None = None  # 예탁지정등록여부
    etf_txtn_type_cd: str | None = None  # ETF과세유형코드
    etf_type_cd: str | None = None  # ETF유형코드
    lstg_abol_dt: str | None = None  # 상장폐지일자
    nwst_odst_dvsn_cd: str | None = None  # 신주구주구분코드
    sbst_pric: str | None = None  # 대용가격
    thco_sbst_pric: str | None = None  # 당사대용가격
    thco_sbst_pric_chng_dt: str | None = None  # 당사대용가격변경일자
    tr_stop_yn: str | None = None  # 거래정지여부
    admn_item_yn: str | None = None  # 관리종목여부
    thdt_clpr: str | None = None  # 당일종가
    bfdy_clpr: str | None = None  # 전일종가
    clpr_chng_dt: str | None = None  # 종가변경일자
    std_idst_clsf_cd: str | None = None  # 표준산업분류코드
    std_idst_clsf_cd_name: str | None = None  # 표준산업분류코드명 — 표준산업소분류코드 000000 해당사항없음 010101 작물 재배업 010102 축산업 010103 작물재배 및 축산 복합농업 010104 작물재배 및 축산 관련 서비스업 010105 수렵 및 관련 서비스업 010201 임업 01
    idx_bztp_lcls_cd_name: str | None = None  # 지수업종대분류코드명 — 표준산업대분류코드 00 해당사항없음 01 농업, 임업 및 어업 02 광업 03 제조업 04 전기, 가스, 증기 및 수도사업 05 하수-폐기물 처리, 원료재생 및환경복원업 06 건설업 07 도매 및 소매업 08 운수업 09 숙박 
    idx_bztp_mcls_cd_name: str | None = None  # 지수업종중분류코드명 — 표준산업중분류코드 0000 해당사항없음 0101 농업 0102 임업 0103 어업 0205 석탄, 원유 및 천연가스 광업 0206 금속 광업 0207 비금속광물 광업; 연료용 제외 0208 광업 지원 서비스업 0310 식료품 제
    idx_bztp_scls_cd_name: str | None = None  # 지수업종소분류코드명 — 표준산업소분류코드 참조
    ocr_no: str | None = None  # OCR번호
    crfd_item_yn: str | None = None  # 크라우드펀딩종목여부
    elec_scty_yn: str | None = None  # 전자증권여부
    issu_istt_cd: str | None = None  # 발행기관코드
    etf_chas_erng_rt_dbnb: str | None = None  # ETF추적수익율배수
    etf_etn_ivst_heed_item_yn: str | None = None  # ETFETN투자유의종목여부
    stln_int_rt_dvsn_cd: str | None = None  # 대주이자율구분코드
    frnr_psnl_lmt_rt: str | None = None  # 외국인개인한도비율
    lstg_rqsr_issu_istt_cd: str | None = None  # 상장신청인발행기관코드
    lstg_rqsr_item_cd: str | None = None  # 상장신청인종목코드
    trst_istt_issu_istt_cd: str | None = None  # 신탁기관발행기관코드
    cptt_trad_tr_psbl_yn: str | None = None  # NXT 거래종목여부 — NXT 거래가능한 종목은 Y, 그 외 종목은 N
    nxt_tr_stop_yn: str | None = None  # NXT 거래정지여부 — NXT 거래종목 중 거래정지가 된 종목은 Y, 그 외 모든 종목은 N

class SearchStockInfoResponse(KisCommonResponse):
    """응답 본문."""

    output: SearchStockInfoResponse_OutputItem | None = None  # 응답상세1

class SearchStockInfoExecutor(ApiExecutor[SearchStockInfoRequest, SearchStockInfoResponse]):
    """주식기본조회[v1_국내주식-067]."""

    # 주식기본조회 API입니다. 국내주식 종목의 종목상세정보를 확인할 수 있습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/search-stock-info"
    METHOD = "GET"
    RESPONSE_TYPE = SearchStockInfoResponse
    TR_ID = "CTPF1002R"
