"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from tooja.brokers.toss.raw.base import TDecimal, TossBaseModel


class ApiResponse(TossBaseModel):
    """성공 응답 envelope. 200 응답에 사용됩니다. 각 엔드포인트의 성공 응답 스키마는 `allOf` 로 본 스키마를 상속하며 `result` 를 구체 타입으로 specialize 합니다. 실패 응답은 별도의 `ErrorResponse` 스키마를 사용합니다 (4xx/5xx). `result` 와 `error` 는 동시에 나타나지 않습니다."""

    result: str | None = Field(default=None, alias="result")  # 성공 응답의 페이로드. 엔드포인트별 타입이 다르며, 각 엔드포인트 스펙에서 `allOf` 로 구체 타입을 명시합니다.


class ErrorResponse(TossBaseModel):
    """에러 응답 envelope. 4xx/5xx 응답에 사용됩니다. 성공 응답은 별도의 `ApiResponse` 스키마를 사용합니다."""

    error: ApiError = Field(alias="error")


class ApiError(TossBaseModel):
    """에러 객체. 에러 식별에 필요한 최소 정보(`requestId`, `code`, `message`)와 필요 시 해결 힌트(`data`)를 포함합니다."""

    request_id: str = Field(alias="requestId")  # 요청을 식별하는 고유 ID. 응답 헤더 `X-Request-Id` 와 동일한 값입니다. 토스증권 CS 문의 시 첨부를 권장합니다.
    code: str = Field(alias="code")  # 에러 코드. flat string 식별자. 도메인 에러는 이유를 직접 표현하는 단일 식별자 (예: `invalid-request`, `order-not-found`) 를 사용합니다. 클라이언트는 unknown cod
    message: str = Field(alias="message")  # 사용자에게 노출 가능한 에러 메시지. 내부 정책상 노출이 제한되는 경우 빈 문자열로 내려갈 수 있으므로 클라이언트는 `code` 기반으로 메시지를 자체 매핑할 것을 권장합니다.
    data: dict | None = Field(default=None, alias="data")  # 에러 해결 힌트. 에러 코드별로 포함 여부와 키 구조가 다르며, 없는 경우 필드 자체가 생략됩니다. 모든 표준 키가 항상 함께 내려가지 않으며, 각 에러 코드에 해당하는 서브셋만 포함됩니다. ## 표준 키 (came


class OAuth2TokenRequest(TossBaseModel):
    """OAuth2 Client Credentials Grant 토큰 발급 요청. `application/x-www-form-urlencoded` 으로 전송합니다."""

    grant_type: str = Field(alias="grant_type")  # 인증 방식. `client_credentials` 만 지원합니다.
    client_id: str = Field(alias="client_id")  # 발급받은 클라이언트 ID
    client_secret: str = Field(alias="client_secret")  # 발급받은 클라이언트 시크릿. 노출되지 않도록 서버 측에서만 사용합니다.


class OAuth2TokenResponse(TossBaseModel):
    """토큰 발급 성공 응답. BFF 의 공통 `ApiResponse` envelope 을 사용하지 않고 OAuth2 표준 형식으로 응답합니다."""

    access_token: str = Field(alias="access_token")  # JWT 형식의 access token. 모든 API 요청의 `Authorization: Bearer` 헤더에 담습니다.
    token_type: str = Field(alias="token_type")  # 토큰 타입. 항상 `Bearer`.
    expires_in: int = Field(alias="expires_in")  # 토큰 만료까지 남은 초.


class OAuth2ErrorResponse(TossBaseModel):
    """OAuth2 토큰 발급 실패 응답. `/oauth2/token` 엔드포인트는 BFF 공통 `ErrorResponse` envelope 이 아닌 OAuth2 표준 포맷으로 응답합니다. 클라이언트는 `code` 가 아닌 `error` 필드로 에러를 식별해야 합니다."""

    error: str = Field(alias="error")  # 에러 코드.
    error_description: str | None = Field(default=None, alias="error_description")  # 에러 상세 설명 (선택). 메시지에 non-ASCII 문자가 포함되는 경우 생략될 수 있습니다.
    error_uri: str | None = Field(default=None, alias="error_uri")  # 에러 정보가 게시된 페이지 URI (선택).


class OrderbookEntry(TossBaseModel):
    """OrderbookEntry schema."""

    price: TDecimal = Field(default=None, alias="price")  # 호가
    volume: TDecimal = Field(default=None, alias="volume")  # 잔량


class OrderbookResponse(TossBaseModel):
    """OrderbookResponse schema."""

    timestamp: str | None = Field(default=None, alias="timestamp")  # 데이터 시각. 데이터 미제공 시 null
    currency: str = Field(alias="currency")
    asks: list[OrderbookEntry] = Field(default=[], alias="asks")  # 매도호가 목록 (낮은 가격순)
    bids: list[OrderbookEntry] = Field(default=[], alias="bids")  # 매수호가 목록 (높은 가격순)


class PriceResponse(TossBaseModel):
    """PriceResponse schema."""

    symbol: str = Field(alias="symbol")  # 종목 심볼
    timestamp: str | None = Field(default=None, alias="timestamp")  # 데이터 시각. 체결 미발생 등으로 시각이 없을 경우 null
    last_price: TDecimal = Field(default=None, alias="lastPrice")  # 현재가
    currency: str = Field(alias="currency")


class Trade(TossBaseModel):
    """Trade schema."""

    price: TDecimal = Field(default=None, alias="price")  # 체결가
    volume: TDecimal = Field(default=None, alias="volume")  # 체결 수량
    timestamp: str = Field(alias="timestamp")  # 체결 시각
    currency: str = Field(alias="currency")


class PriceLimitResponse(TossBaseModel):
    """PriceLimitResponse schema."""

    timestamp: str = Field(alias="timestamp")  # 데이터 시각
    upper_limit_price: TDecimal = Field(default=None, alias="upperLimitPrice")  # 상한가. 미국 주식 등 가격제한이 없는 시장에서는 null
    lower_limit_price: TDecimal = Field(default=None, alias="lowerLimitPrice")  # 하한가. 미국 주식 등 가격제한이 없는 시장에서는 null
    currency: str = Field(alias="currency")


class CandlePageResponse(TossBaseModel):
    """CandlePageResponse schema."""

    candles: list[Candle] = Field(default=[], alias="candles")  # 캔들 목록
    next_before: str | None = Field(default=None, alias="nextBefore")  # 다음 페이지 조회 시 `before` 쿼리 파라미터에 그대로 전달. 마지막 페이지면 null.


class Candle(TossBaseModel):
    """Candle schema."""

    timestamp: str = Field(alias="timestamp")  # 봉 시작 시각
    open_price: TDecimal = Field(default=None, alias="openPrice")  # 시가
    high_price: TDecimal = Field(default=None, alias="highPrice")  # 고가
    low_price: TDecimal = Field(default=None, alias="lowPrice")  # 저가
    close_price: TDecimal = Field(default=None, alias="closePrice")  # 종가
    volume: TDecimal = Field(default=None, alias="volume")  # 거래량
    currency: str = Field(alias="currency")


class StockInfo(TossBaseModel):
    """StockInfo schema."""

    symbol: str = Field(alias="symbol")  # 종목 심볼.
    name: str = Field(alias="name")  # 종목명 (한글)
    english_name: str = Field(alias="englishName")  # 영문 종목명
    isin_code: str = Field(alias="isinCode")  # 국제증권식별번호 (ISO 6166)
    market: str = Field(alias="market")  # 상장 시장. warnings API의 exchange(거래소 단위)와 달리 시장 세그먼트 단위로 구분
    security_type: str = Field(alias="securityType")  # 종목 유형
    is_common_share: bool = Field(alias="isCommonShare")  # 보통주 여부. 우선주인 경우 false
    status: str = Field(alias="status")  # 상장 상태
    currency: str = Field(alias="currency")
    list_date: str | None = Field(default=None, alias="listDate")  # 상장일 (YYYY-MM-DD, KST 기준). 정보 미제공 시 null
    delist_date: str | None = Field(default=None, alias="delistDate")  # 상장폐지일 (YYYY-MM-DD, KST 기준). 활성 종목은 null
    shares_outstanding: TDecimal = Field(default=None, alias="sharesOutstanding")  # 발행주식수
    leverage_factor: TDecimal = Field(default=None, alias="leverageFactor")  # 레버리지 배수. ETF/ETN에만 적용 (1.0, 2.0, -1.0 등). 일반 주식 등 해당 없는 종목은 null
    korean_market_detail: KrMarketDetail | None = Field(default=None, alias="koreanMarketDetail")  # 국내 시장 상세 정보. 국내 종목(KOSPI, KOSDAQ, KR_ETC)에만 제공되며, 해외 종목은 null


class KrMarketDetail(TossBaseModel):
    """KrMarketDetail schema."""

    liquidation_trading: bool = Field(alias="liquidationTrading")  # 정리매매 여부 (상장폐지 절차 진행 중).
    nxt_supported: bool = Field(alias="nxtSupported")  # NXT 대체거래소 지원 여부
    krx_trading_suspended: bool = Field(alias="krxTradingSuspended")  # KRX 거래정지 여부
    nxt_trading_suspended: bool | None = Field(default=None, alias="nxtTradingSuspended")  # NXT 거래정지 여부. NXT 미지원 종목(nxtSupported=false)은 null


class StockWarning(TossBaseModel):
    """StockWarning schema."""

    warning_type: str = Field(alias="warningType")  # 유의사항 유형. 클라이언트는 unknown code 를 허용하도록 구현해야 합니다. | 값 | 의미 | |------|------| | `LIQUIDATION_TRADING` | 정리매매 (상장폐지 절차 진행 중) 
    exchange: str | None = Field(default=None, alias="exchange")  # 거래소 코드 (KRX, NXT 등 물리적 거래소 단위). stocks API의 market(상장 시장 단위)과 추상화 수준이 다름. 거래소 무관 경고는 null
    start_date: str | None = Field(default=None, alias="startDate")  # 적용 시작일 (inclusive, YYYY-MM-DD, KST 기준). 시작일 미정 시 null
    end_date: str | None = Field(default=None, alias="endDate")  # 적용 종료일 (inclusive, YYYY-MM-DD, KST 기준). 진행 중이거나 미정 시 null


class ExchangeRateResponse(TossBaseModel):
    """ExchangeRateResponse schema."""

    base_currency: str = Field(alias="baseCurrency")  # 기준 통화
    quote_currency: str = Field(alias="quoteCurrency")  # 표시 통화 (quote currency)
    rate: TDecimal = Field(default=None, alias="rate")  # 매수 환율 (1 baseCurrency = ? quoteCurrency)
    mid_rate: TDecimal = Field(default=None, alias="midRate")  # 매매기준율 (은행간 mid rate)
    basis_point: TDecimal = Field(default=None, alias="basisPoint")  # 매매기준율(midRate) 대비 basis points. (rate - midRate) / midRate * 10000
    rate_change_type: str = Field(alias="rateChangeType")  # 등락 구분
    valid_from: str = Field(alias="validFrom")  # 환율 유효 시작 시각
    valid_until: str = Field(alias="validUntil")  # 환율 유효 종료 시각


class KrMarketCalendarResponse(TossBaseModel):
    """KrMarketCalendarResponse schema."""

    today: KrMarketDay = Field(alias="today")
    previous_business_day: KrMarketDay = Field(alias="previousBusinessDay")
    next_business_day: KrMarketDay = Field(alias="nextBusinessDay")


class KrMarketDay(TossBaseModel):
    """KrMarketDay schema."""

    date: str = Field(alias="date")  # 영업일 (KST 기준)
    integrated: IntegratedHour | None = Field(default=None, alias="integrated")  # 거래 가능 시간 (통합 모드 (KRX+NXT) 기준). 둘 다 휴장이면 null


class IntegratedHour(TossBaseModel):
    """거래 가능 시간. 특수장(시간외종가/시간외단일가) 제외, 통합 모드 (KRX+NXT) 기준. 세 세션(`preMarket`, `regularMarket`, `afterMarket`) 각각 nullable. 해당 세션이 휴장이면 null, 세 세션 모두 null 이면 상위 `integrated` 자체가 null."""

    pre_market: PreMarketSession | None = Field(default=None, alias="preMarket")  # 프리마켓 (NXT 접속매매). NXT 프리마켓이 휴장이면 null
    regular_market: RegularMarketSession | None = Field(default=None, alias="regularMarket")  # 정규장. KRX·NXT 정규장의 합집합. 둘 다 휴장이면 null
    after_market: AfterMarketSession | None = Field(default=None, alias="afterMarket")  # 애프터마켓 (NXT). NXT 애프터마켓이 휴장이면 null


class PreMarketSession(TossBaseModel):
    """프리마켓 세션"""

    start_time: str = Field(alias="startTime")  # 프리마켓 시작
    single_price_auction_start_time: str | None = Field(default=None, alias="singlePriceAuctionStartTime")  # 프리마켓 내 시가단일가 구간 시작 (NXT 프리마켓 접속매매 종료). 단일가 정보 결손 시 null
    end_time: str = Field(alias="endTime")  # 프리마켓 종료 (시가단일가 종료)


class RegularMarketSession(TossBaseModel):
    """정규장 세션. KRX·NXT 정규장의 합집합(가장 이른 시작 ~ 가장 늦은 종료). 종가단일가 구간을 포함"""

    start_time: str = Field(alias="startTime")  # 정규장 시작. 가장 이른 KRX/NXT 정규장 시작 시각
    single_price_auction_start_time: str | None = Field(default=None, alias="singlePriceAuctionStartTime")  # 정규장 내 종가단일가 구간 시작 (KRX 기준). KRX 휴장이면 null
    end_time: str = Field(alias="endTime")  # 정규장 종료 (종가단일가 종료)


class AfterMarketSession(TossBaseModel):
    """애프터마켓 세션 (NXT)"""

    start_time: str = Field(alias="startTime")  # 애프터마켓 시작
    single_price_auction_end_time: str | None = Field(default=None, alias="singlePriceAuctionEndTime")  # 애프터마켓 내 시가단일가 구간 종료.
    end_time: str = Field(alias="endTime")  # 애프터마켓 전체 종료


class UsMarketCalendarResponse(TossBaseModel):
    """UsMarketCalendarResponse schema."""

    today: UsMarketDay = Field(alias="today")
    previous_business_day: UsMarketDay = Field(alias="previousBusinessDay")
    next_business_day: UsMarketDay = Field(alias="nextBusinessDay")


class UsMarketDay(TossBaseModel):
    """미국 시장 영업일 정보. 4 세션(`dayMarket`, `preMarket`, `regularMarket`, `afterMarket`) 각각 nullable. 휴장일이면 4 세션 모두 null."""

    date: str = Field(alias="date")  # 영업일 (미국 현지 기준)
    day_market: UsDayMarketSession | None = Field(default=None, alias="dayMarket")  # 데이마켓 세션 (토스증권). 휴장이면 null
    pre_market: UsPreMarketSession | None = Field(default=None, alias="preMarket")  # 프리마켓 세션. 휴장이면 null
    regular_market: UsRegularMarketSession | None = Field(default=None, alias="regularMarket")  # 정규장 세션. 휴장이면 null
    after_market: UsAfterMarketSession | None = Field(default=None, alias="afterMarket")  # 애프터마켓 세션. 휴장이면 null


class UsDayMarketSession(TossBaseModel):
    """데이마켓 세션 (토스증권)"""

    start_time: str = Field(alias="startTime")  # 데이마켓 시작
    end_time: str = Field(alias="endTime")  # 데이마켓 종료


class UsPreMarketSession(TossBaseModel):
    """프리마켓 세션"""

    start_time: str = Field(alias="startTime")  # 프리마켓 시작
    end_time: str = Field(alias="endTime")  # 프리마켓 종료


class UsRegularMarketSession(TossBaseModel):
    """정규장 세션"""

    start_time: str = Field(alias="startTime")  # 정규장 시작
    end_time: str = Field(alias="endTime")  # 정규장 종료


class UsAfterMarketSession(TossBaseModel):
    """애프터마켓 세션"""

    start_time: str = Field(alias="startTime")  # 애프터마켓 시작
    end_time: str = Field(alias="endTime")  # 애프터마켓 종료


class Account(TossBaseModel):
    """Account schema."""

    account_no: str = Field(alias="accountNo")  # 계좌번호
    account_seq: int = Field(alias="accountSeq")  # 계좌 식별 키. 주문 등 API 호출 시 이 값을 사용
    account_type: str = Field(alias="accountType")  # 계좌 유형. 현재는 BROKERAGE 만 지원합니다. - BROKERAGE: 종합매매. 국내·해외 주식 통합 매매 계좌 - OVERSEAS_DERIVATIVES: 해외파생. 해외 파생상품 거래 계좌 - PENSION


class HoldingsOverview(TossBaseModel):
    """HoldingsOverview schema."""

    total_purchase_amount: Price = Field(alias="totalPurchaseAmount")  # 투자원금. 전체 보유 종목의 통화별 합산
    market_value: OverviewMarketValue = Field(alias="marketValue")
    profit_loss: OverviewProfitLoss = Field(alias="profitLoss")
    daily_profit_loss: OverviewDailyProfitLoss = Field(alias="dailyProfitLoss")
    items: list[HoldingsItem] = Field(default=[], alias="items")  # 보유 종목 목록. 보유 종목이 없으면 빈 배열


class HoldingsItem(TossBaseModel):
    """HoldingsItem schema."""

    symbol: str = Field(alias="symbol")  # 종목 심볼. KR: 6자리 숫자, US: 티커
    name: str = Field(alias="name")  # 종목명
    market_country: str = Field(alias="marketCountry")
    currency: str = Field(alias="currency")
    quantity: TDecimal = Field(default=None, alias="quantity")  # 보유 수량
    last_price: TDecimal = Field(default=None, alias="lastPrice")  # 현재가. 거래 통화(currency) 기준
    average_purchase_price: TDecimal = Field(default=None, alias="averagePurchasePrice")  # 매수 평균가. 거래 통화(currency) 기준
    market_value: MarketValue = Field(alias="marketValue")
    profit_loss: ProfitLoss = Field(alias="profitLoss")
    daily_profit_loss: DailyProfitLoss = Field(alias="dailyProfitLoss")
    cost: Cost = Field(alias="cost")


class Price(TossBaseModel):
    """통화별 합산 금액. 각 통화 필드는 해당 통화로 거래된 종목의 합만 포함합니다 (환율 환산을 통한 통화 간 합산 미포함)."""

    krw: TDecimal = Field(default=None, alias="krw")  # KRW로 거래되는 국내 종목의 합산 금액. 국내 종목이 없으면 0
    usd: TDecimal = Field(default=None, alias="usd")  # USD로 거래되는 해외 종목의 합산 금액. 해외 종목이 없으면 null


class OverviewMarketValue(TossBaseModel):
    """시장 평가금액. 전체 보유 종목의 통화별 합산"""

    amount: Price = Field(alias="amount")  # 시장 평가금액
    amount_after_cost: Price = Field(alias="amountAfterCost")  # 세금/수수료 공제 후 평가금액


class OverviewProfitLoss(TossBaseModel):
    """손익. 전체 보유 종목의 통화별 합산"""

    amount: Price = Field(alias="amount")  # 손익금액
    amount_after_cost: Price = Field(alias="amountAfterCost")  # 세금/수수료 공제 후 손익금액
    rate: TDecimal = Field(default=None, alias="rate")  # 손익률 (소수비율). 전체 자산을 현재 환율로 원화 환산한 기준. 0.1516 = 15.16%
    rate_after_cost: TDecimal = Field(default=None, alias="rateAfterCost")  # 세금/수수료 공제 후 손익률 (소수비율). 전체 자산을 현재 환율로 원화 환산한 기준. 0.1406 = 14.06%


class OverviewDailyProfitLoss(TossBaseModel):
    """일간 손익. 전체 보유 종목의 통화별 합산"""

    amount: Price = Field(alias="amount")  # 일간 손익금액
    rate: TDecimal = Field(default=None, alias="rate")  # 일간 손익률 (소수비율). 전체 자산을 현재 환율로 원화 환산한 기준. 0.0185 = 1.85%


class MarketValue(TossBaseModel):
    """시장 평가. 거래 통화(currency) 기준"""

    purchase_amount: TDecimal = Field(default=None, alias="purchaseAmount")  # 매입금액
    amount: TDecimal = Field(default=None, alias="amount")  # 시장 평가금액
    amount_after_cost: TDecimal = Field(default=None, alias="amountAfterCost")  # 세금/수수료 공제 후 평가금액


class ProfitLoss(TossBaseModel):
    """손익. 거래 통화(currency) 기준"""

    amount: TDecimal = Field(default=None, alias="amount")  # 손익금액
    amount_after_cost: TDecimal = Field(default=None, alias="amountAfterCost")  # 세금/수수료 공제 후 손익금액
    rate: TDecimal = Field(default=None, alias="rate")  # 손익률. 소수비율 (0.1077 = 10.77%)
    rate_after_cost: TDecimal = Field(default=None, alias="rateAfterCost")  # 세금/수수료 공제 후 손익률. 소수비율 (0.0846 = 8.46%)


class DailyProfitLoss(TossBaseModel):
    """일간 손익. 거래 통화(currency) 기준"""

    amount: TDecimal = Field(default=None, alias="amount")  # 일간 손익금액
    rate: TDecimal = Field(default=None, alias="rate")  # 일간 손익률. 소수비율 (0.0141 = 1.41%)


class Cost(TossBaseModel):
    """비용. 거래 통화(currency) 기준"""

    commission: TDecimal = Field(default=None, alias="commission")  # 수수료
    tax: TDecimal = Field(default=None, alias="tax")  # 세금. 세금이 없는 경우 null


class OrderCreateRequest(TossBaseModel):
    """Merged ``oneOf`` request model. The OpenAPI spec defines this as a oneOf of variants;
    all variants' properties are merged here and made optional so the adapter can
    populate whichever variant applies."""

    client_order_id: str | None = Field(default=None, alias="clientOrderId")  # 클라이언트 지정 주문 식별자. 멱등성 키로 사용됩니다. - 미전달: 멱등성 미적용. 매 요청을 별개 주문으로 처리합니다. - 전달: 동일 값으로 재요청 시 이전 주문 결과를 그대로 재반환합니다. 서버는 자동 생성하지
    symbol: str | None = Field(default=None, alias="symbol")  # 종목 심볼. KRX: 6자리 숫자, US: 영문 티커
    side: str | None = Field(default=None, alias="side")  # 주문 방향
    order_type: str | None = Field(default=None, alias="orderType")  # 호가 유형. - `LIMIT`: 지정가 - `MARKET`: 시장가
    time_in_force: str | None = Field(default=None, alias="timeInForce")  # 주문 유효 조건 (Time In Force). 미전달 시 `DAY`. `orderType` 과 결합되어 주문 방식이 결정됩니다 (예: `LIMIT` + `CLS` = LOC). - `DAY`: 당일 유효 (Day).
    quantity: TDecimal = Field(default=None, alias="quantity")  # 주문 수량 (주 단위). 지정한 수량만큼 주문합니다. 정수만 가능합니다. (소수점 불가능. 소수점 주문 시 Amount-based variant 의 `orderAmount` 를 사용해야 합니다.)
    price: TDecimal = Field(default=None, alias="price")  # 주문 가격. `orderType`이 `LIMIT` 일 때만 사용합니다. - `LIMIT`: 필수. 미전달 시 `400 invalid-request`. - `MARKET`: 전달 불가. 전달 시 `400 invalid
    confirm_high_value_order: bool | None = Field(default=None, alias="confirmHighValueOrder")  # 착오주문 방지를 위한 주문 확인 플래그. 기본값 `false`. 1억원 이상의 주문 시 `true`가 아니면 `400 confirm-high-value-required` 에러를 반환합니다. 사용자가 해당 주문의 금액
    order_amount: TDecimal = Field(default=None, alias="orderAmount")  # 주문 금액 (달러). 지정한 금액만큼 주문합니다. 체결 수량은 체결 시점의 시장가에 따라 결정됩니다. Quantity-based 와의 차이: quantity 는 수량을 확정하고 비용이 변동하며, orderAmount


class OrderModifyRequest(TossBaseModel):
    """OrderModifyRequest schema."""

    order_type: str = Field(alias="orderType")  # 변경할 호가 유형. - `LIMIT`: 지정가 - `MARKET`: 시장가
    quantity: TDecimal = Field(default=None, alias="quantity")  # 변경할 수량. **KR 주식: 필수.** 양의 정수만 허용합니다 (미전달/0/음수/소수점은 `400 invalid-request`). US 주식: 전달 불가. 제공 시 `400 us-modify-quantity-no
    price: TDecimal = Field(default=None, alias="price")  # 변경할 가격. `orderType`이 `LIMIT` 일 때만 사용합니다. - `LIMIT`: 필수. 미전달 시 `400 invalid-request`. - `MARKET`: 전달 불가. 전달 시 `400 invali
    confirm_high_value_order: bool | None = Field(default=None, alias="confirmHighValueOrder")  # 착오주문 방지를 위한 주문 확인 플래그. 기본값 `false`. 1억원 이상의 주문 시 `true`가 아니면 `400 confirm-high-value-required` 에러를 반환합니다. 사용자가 해당 주문의 금액


class OrderResponse(TossBaseModel):
    """OrderResponse schema."""

    order_id: str = Field(alias="orderId")  # 서버 생성 주문 식별자. 정정/취소 시 사용
    client_order_id: str | None = Field(default=None, alias="clientOrderId")  # 요청 시 전달한 값 그대로 반환. 미전달 시 `null`.


class OrderOperationResponse(TossBaseModel):
    """OrderOperationResponse schema."""

    order_id: str = Field(alias="orderId")  # 정정/취소로 새로 발급된 주문 식별자. 원주문의 orderId 와 다릅니다.


class PaginatedOrderResponse(TossBaseModel):
    """주문 목록 페이징 응답. - `status=OPEN`: 모든 대기 중 주문을 반환합니다. `nextCursor`는 항상 `null`, `hasNext`는 항상 `false`. - `status=CLOSED`: 현재 호출 시 `400 closed-not-supported` 를 반환합니다."""

    orders: list[Order] = Field(default=[], alias="orders")  # 주문 목록
    next_cursor: str | None = Field(default=None, alias="nextCursor")  # 다음 페이지 커서. 다음 페이지가 없으면 null
    has_next: bool = Field(alias="hasNext")  # 다음 페이지 존재 여부


class Order(TossBaseModel):
    """Order schema."""

    order_id: str = Field(alias="orderId")  # 주문 식별자
    symbol: str = Field(alias="symbol")  # 종목 심볼. KRX: 6자리 숫자, US: 영문 티커
    side: str = Field(alias="side")  # 주문 방향
    order_type: str = Field(alias="orderType")  # 호가 유형. - `LIMIT`: 지정가 - `MARKET`: 시장가 클라이언트는 unknown code 를 허용하도록 구현해야 합니다.
    time_in_force: str = Field(alias="timeInForce")  # 주문 유효 조건 (Time In Force). `orderType` 과 결합되어 주문 방식이 결정됩니다 (예: `LIMIT` + `CLS` = LOC). - `DAY`: 당일 유효 (Day) - `CLS`: 장 마감
    status: str = Field(alias="status")
    price: TDecimal = Field(default=None, alias="price")  # 주문 가격 (native currency). MARKET 주문 시 null
    quantity: TDecimal = Field(default=None, alias="quantity")  # 주문 수량
    order_amount: TDecimal = Field(default=None, alias="orderAmount")  # 주문 금액 (USD). 금액 기반 US 시장가 매수 주문에만 해당. 그 외 null
    currency: str = Field(alias="currency")
    ordered_at: str = Field(alias="orderedAt")  # 주문 시간 (ISO 8601, KST)
    canceled_at: str | None = Field(default=None, alias="canceledAt")  # 취소 시간 (ISO 8601, KST). 해당 없으면 null
    execution: OrderExecution = Field(alias="execution")  # 체결 결과. 체결 내역이 없으면 filledQuantity=0


class OrderExecution(TossBaseModel):
    """OrderExecution schema."""

    filled_quantity: TDecimal = Field(default=None, alias="filledQuantity")  # 체결 수량
    average_filled_price: TDecimal = Field(default=None, alias="averageFilledPrice")  # 평균 체결 가격 (native currency). 부분 체결 시 체결된 건의 평균
    filled_amount: TDecimal = Field(default=None, alias="filledAmount")  # 총 체결 금액 (native currency)
    commission: TDecimal = Field(default=None, alias="commission")  # 총 체결 수수료 (native currency)
    tax: TDecimal = Field(default=None, alias="tax")  # 총 체결 세금 (native currency)
    filled_at: str | None = Field(default=None, alias="filledAt")  # 최종 체결 시간 (ISO 8601, KST)
    settlement_date: str | None = Field(default=None, alias="settlementDate")  # 결제 예정일 (YYYY-MM-DD, KST 기준). 미결제 시 null


class BuyingPowerResponse(TossBaseModel):
    """BuyingPowerResponse schema."""

    currency: str = Field(alias="currency")
    cash_buying_power: TDecimal = Field(default=None, alias="cashBuyingPower")  # 현금 기반 매수 가능 금액 (미수 미발생 기준). 순수 현금으로 매수할 수 있는 금액. KRW: 정수 (원 단위). USD: 소수점 포함 (달러 단위).


class SellableQuantityResponse(TossBaseModel):
    """SellableQuantityResponse schema."""

    sellable_quantity: TDecimal = Field(default=None, alias="sellableQuantity")  # 판매 가능 수량. KR: 정수 (주 단위). US: 소수점 포함 가능 (주 단위).


class Commission(TossBaseModel):
    """Commission schema."""

    market_country: str = Field(alias="marketCountry")
    commission_rate: TDecimal = Field(default=None, alias="commissionRate")  # 수수료율 (%). 예: 0.015는 0.015%
    start_date: str | None = Field(default=None, alias="startDate")  # 수수료 적용 시작일 (YYYY-MM-DD, KST 기준). 해외주식은 null
    end_date: str | None = Field(default=None, alias="endDate")  # 수수료 적용 종료일 (YYYY-MM-DD, KST 기준). 무기한 적용 시 null



ApiResponse.model_rebuild()
ErrorResponse.model_rebuild()
ApiError.model_rebuild()
OAuth2TokenRequest.model_rebuild()
OAuth2TokenResponse.model_rebuild()
OAuth2ErrorResponse.model_rebuild()
OrderbookEntry.model_rebuild()
OrderbookResponse.model_rebuild()
PriceResponse.model_rebuild()
Trade.model_rebuild()
PriceLimitResponse.model_rebuild()
CandlePageResponse.model_rebuild()
Candle.model_rebuild()
StockInfo.model_rebuild()
KrMarketDetail.model_rebuild()
StockWarning.model_rebuild()
ExchangeRateResponse.model_rebuild()
KrMarketCalendarResponse.model_rebuild()
KrMarketDay.model_rebuild()
IntegratedHour.model_rebuild()
PreMarketSession.model_rebuild()
RegularMarketSession.model_rebuild()
AfterMarketSession.model_rebuild()
UsMarketCalendarResponse.model_rebuild()
UsMarketDay.model_rebuild()
UsDayMarketSession.model_rebuild()
UsPreMarketSession.model_rebuild()
UsRegularMarketSession.model_rebuild()
UsAfterMarketSession.model_rebuild()
Account.model_rebuild()
HoldingsOverview.model_rebuild()
HoldingsItem.model_rebuild()
Price.model_rebuild()
OverviewMarketValue.model_rebuild()
OverviewProfitLoss.model_rebuild()
OverviewDailyProfitLoss.model_rebuild()
MarketValue.model_rebuild()
ProfitLoss.model_rebuild()
DailyProfitLoss.model_rebuild()
Cost.model_rebuild()
OrderCreateRequest.model_rebuild()
OrderModifyRequest.model_rebuild()
OrderResponse.model_rebuild()
OrderOperationResponse.model_rebuild()
PaginatedOrderResponse.model_rebuild()
Order.model_rebuild()
OrderExecution.model_rebuild()
BuyingPowerResponse.model_rebuild()
SellableQuantityResponse.model_rebuild()
Commission.model_rebuild()
