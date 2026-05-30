from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class Exchange(str, Enum):
    KRX = "KRX"

    NASD = "NASD"
    NYSE = "NYSE"
    AMEX = "AMEX"

    SEHK = "SEHK"
    SHAA = "SHAA"
    SZAA = "SZAA"
    TKSE = "TKSE"
    HASE = "HASE"
    VNSE = "VNSE"


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    LIMIT = "limit"
    MARKET = "market"
    MOO = "moo"
    LOO = "loo"
    MOC = "moc"
    LOC = "loc"


class Currency(str, Enum):
    KRW = "KRW"
    USD = "USD"
    HKD = "HKD"
    CNY = "CNY"
    JPY = "JPY"
    VND = "VND"


class Holding(BaseModel):
    ticker: str
    exchange: Exchange | None = None
    name: str | None = None
    qty: Decimal
    avg_price: Decimal
    current_price: Decimal | None = None
    currency: Currency | None = None
    pnl: Decimal | None = None
    pnl_rate: Decimal | None = None


class Balance(BaseModel):
    total_asset: Decimal | None = None
    cash: dict[Currency, Decimal] = {}
    holdings: list[Holding] = []


class OrderResult(BaseModel):
    order_no: str
    org_no: str | None = None
    time: str | None = None
    message: str | None = None


class Price(BaseModel):
    ticker: str
    exchange: Exchange | None = None
    price: Decimal
    currency: Currency | None = None
    date: str | None = None
    time: str | None = None
    change: Decimal | None = None
    change_rate: Decimal | None = None
    open: Decimal | None = None
    high: Decimal | None = None
    low: Decimal | None = None
    volume: Decimal | None = None
