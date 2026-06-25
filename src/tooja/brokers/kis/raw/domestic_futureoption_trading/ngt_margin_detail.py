"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class NgtMarginDetailRequest(KisBaseModel):
    """요청."""

    CANO: str  # 종합계좌번호
    ACNT_PRDT_CD: str  # 계좌상품코드
    MGNA_DVSN_CD: str  # 증거금 구분코드 — 위탁(01), 유지(02)

class NgtMarginDetailResponse_Output1Item(KisBaseModel):
    """nested item."""

    cash_amt: str | None = None  # 현금금액
    tot_amt: str | None = None  # 총금액
    futr_new_mgn_amt: str | None = None  # 선물신규증거금액 — 신 TR 사용 필드
    futr_sprd_ord_mgna: str | None = None  # 선물스프레드주문증거금 — 신 TR 사용 필드
    opt_sll_new_mgn_amt: str | None = None  # 옵션매도신규증거금액 — 신 TR 사용 필드
    opt_buy_new_mgn_amt: str | None = None  # 옵션매수신규증거금액 — 신 TR 사용 필드
    new_mgn_amt: str | None = None  # 신규증거금액 — 신 TR 사용 필드
    opt_pric_mgna: str | None = None  # 옵션가격증거금 — 신 TR 사용 필드
    fuop_pric_altr_mgna: str | None = None  # 선물옵션가격변동증거금 — 신 TR 사용 필드
    futr_sprd_mgna: str | None = None  # 선물스프레드증거금 — 신 TR 사용 필드
    uwdl_mgna: str | None = None  # 인수도증거금 — 신 TR 사용 필드
    ctrt_per_min_mgna: str | None = None  # 계약당최소증거금 — 신 TR 사용 필드
    tot_risk_mgna: str | None = None  # 총위험증거금 — 신 TR 사용 필드
    netrisk_brkg_mgna: str | None = None  # 순위험위탁증거금 — 신 TR 사용 필드
    opt_sll_chgs: str | None = None  # 옵션매도대금 — 신 TR 사용 필드
    opt_buy_chgs: str | None = None  # 옵션매수대금 — 신 TR 사용 필드
    futr_loss_amt: str | None = None  # 선물손실금액 — 신 TR 사용 필드
    futr_prft_amt: str | None = None  # 선물이익금액 — 신 TR 사용 필드
    thdt_ccld_net_loss_amt: str | None = None  # 당일체결순손실금액 — 신 TR 사용 필드
    brkg_mgna: str | None = None  # 위탁증거금 — 신 TR 사용 필드

class NgtMarginDetailResponse_Output2Item(KisBaseModel):
    """nested item."""

    cash_amt: str | None = None  # 현금금액
    sbst_amt: str | None = None  # 대용금액
    tot_amt: str | None = None  # 총금액
    futr_new_mgn_amt: str | None = None  # 선물신규증거금액 — 신 TR 사용 필드
    futr_sprd_ord_mgna: str | None = None  # 선물스프레드주문증거금 — 신 TR 사용 필드
    opt_sll_new_mgn_amt: str | None = None  # 옵션매도신규증거금액 — 신 TR 사용 필드
    opt_buy_new_mgn_amt: str | None = None  # 옵션매수신규증거금액 — 신 TR 사용 필드
    new_mgn_amt: str | None = None  # 신규증거금액 — 신 TR 사용 필드
    opt_pric_mgna: str | None = None  # 옵션가격증거금 — 신 TR 사용 필드
    fuop_pric_altr_mgna: str | None = None  # 선물옵션가격변동증거금 — 신 TR 사용 필드
    futr_sprd_mgna: str | None = None  # 선물스프레드증거금 — 신 TR 사용 필드
    uwdl_mgna: str | None = None  # 인수도증거금 — 신 TR 사용 필드
    ctrt_per_min_mgna: str | None = None  # 계약당최소증거금 — 신 TR 사용 필드
    tot_risk_mgna: str | None = None  # 총위험증거금 — 신 TR 사용 필드
    netrisk_brkg_mgna: str | None = None  # 순위험위탁증거금 — 신 TR 사용 필드
    opt_sll_chgs: str | None = None  # 옵션매도대금 — 신 TR 사용 필드
    opt_buy_chgs: str | None = None  # 옵션매수대금 — 신 TR 사용 필드
    futr_loss_amt: str | None = None  # 선물손실금액 — 신 TR 사용 필드
    futr_prft_amt: str | None = None  # 선물이익금액 — 신 TR 사용 필드
    thdt_ccld_net_loss_amt: str | None = None  # 당일체결순손실금액 — 신 TR 사용 필드
    brkg_mgna: str | None = None  # 위탁증거금 — 신 TR 사용 필드

class NgtMarginDetailResponse_Output3Item(KisBaseModel):
    """nested item."""

    base_dpsa_gdat_grad_cd: str | None = None  # 기본예탁금차등등급코드
    bfdy_sbst_sll_ccld_amt: str | None = None  # 전일대용매도체결금액
    bfdy_sbst_sll_sbst_amt: str | None = None  # 전일대용매도대용금액
    excc_dfpa: str | None = None  # 정산차금
    fee_amt: str | None = None  # 수수료금액
    nxdy_dncl_amt: str | None = None  # 익일예수금액
    opt_base_dpsa_gdat_grad_cd: str | None = None  # 옵션기본예탁금차등등급코드
    opt_buy_exus_acnt_yn: str | None = None  # 옵션매수전용계좌여부
    opt_dfpa: str | None = None  # 옵션차금
    prsm_dpast_amt: str | None = None  # 추정예탁자산금액
    thdt_sbst_sll_ccld_amt: str | None = None  # 당일대용매도체결금액
    thdt_sbst_sll_sbst_amt: str | None = None  # 당일대용매도대용금액
    dnca_cash: str | None = None  # 예수금현금 — 신 TR 사용 필드
    dnca_sbst: str | None = None  # 예수금대용 — 신 TR 사용 필드
    dnca_tota: str | None = None  # 예수금총액 — 신 TR 사용 필드
    wdrw_psbl_cash_amt: str | None = None  # 인출가능현금금액 — 신 TR 사용 필드
    wdrw_psbl_sbsa: str | None = None  # 인출가능대용금액 — 신 TR 사용 필드
    wdrw_psbl_tot_amt: str | None = None  # 인출가능총금액 — 신 TR 사용 필드
    ord_psbl_cash_amt: str | None = None  # 주문가능현금금액 — 신 TR 사용 필드
    ord_psbl_sbsa: str | None = None  # 주문가능대용금액 — 신 TR 사용 필드
    ord_psbl_tot_amt: str | None = None  # 주문가능총금액 — 신 TR 사용 필드
    brkg_mgna_cash_amt: str | None = None  # 위탁증거금현금금액 — 신 TR 사용 필드
    brkg_mgna_sbst: str | None = None  # 위탁증거금대용 — 신 TR 사용 필드
    brkg_mgna_tot_amt: str | None = None  # 위탁증거금총금액 — 신 TR 사용 필드
    add_mgna_cash_amt: str | None = None  # 추가증거금현금금액 — 신 TR 사용 필드
    add_mgna_sbsa: str | None = None  # 추가증거금대용금액 — 신 TR 사용 필드
    add_mgna_tot_amt: str | None = None  # 추가증거금총금액 — 신 TR 사용 필드

class NgtMarginDetailResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[NgtMarginDetailResponse_Output1Item] = []  # 응답상세 — array 아래 18가지 항목이 순서대로 출력됨 (1) A. 신규증거금 - 선물 - 1.개별종목 (2) A. 신규증거금 - 선물 - 2.스프레드 (3) A. 신규증거금 - 3. ﻿﻿﻿옵션매수증거금 ﻿﻿(4) A. 신규증거금 - 4. 옵션매
    output2: list[NgtMarginDetailResponse_Output2Item] = []  # 응답상세 — array 아래 5가지 항목이 순서대로 출력됨 (1) 예수금 (2) 인출가능금액 (3) 주문가능금액 ﻿﻿(4) 위탁증거금액 ﻿﻿(5) 추가증거금액 ※ 인출가능금액은 정산 후 인출가능 예정 금액입니다. 현재 시점 실제 인출 가능금액은 정규장
    output3: NgtMarginDetailResponse_Output3Item | None = None  # 응답상세

class NgtMarginDetailExecutor(ApiExecutor[NgtMarginDetailRequest, NgtMarginDetailResponse]):
    """(야간)선물옵션 증거금 상세 [국내선물-024]."""

    # (야간)선물옵션 증거금상세 API입니다. 한국투자 HTS(eFriend Plus) &gt; [2537] 야간선물옵션 증거금상세 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-futureoption/v1/trading/ngt-margin-detail"
    METHOD = "GET"
    RESPONSE_TYPE = NgtMarginDetailResponse
    TR_ID = "JTCE6003R"
