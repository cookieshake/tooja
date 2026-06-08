"""Shared enums used by every broker adapter."""

from __future__ import annotations

from enum import Enum


class Exchange(str, Enum):
    KRX = "KRX"
    NXT = "NXT"
    NASD = "NASD"
    NYSE = "NYSE"
    AMEX = "AMEX"
    SEHK = "SEHK"
    SHAA = "SHAA"
    SZAA = "SZAA"
    TKSE = "TKSE"
    HASE = "HASE"
    VNSE = "VNSE"


class AssetClass(str, Enum):
    STOCK = "stock"
    FUTURES_OPTIONS = "futop"
    BOND = "bond"
    ELW = "elw"


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class RebalanceDirection(str, Enum):
    BOTH = "both"
    BUY_ONLY = "buy_only"
    SELL_ONLY = "sell_only"


class OrderStatus(str, Enum):
    PENDING = "pending"
    OPEN = "open"
    PARTIALLY_FILLED = "partial"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class TimeInForce(str, Enum):
    DAY = "DAY"
    IOC = "IOC"
    FOK = "FOK"
    GTC = "GTC"


class Currency(str, Enum):
    KRW = "KRW"
    USD = "USD"
    HKD = "HKD"
    CNY = "CNY"
    JPY = "JPY"
    VND = "VND"


class FinancialPeriod(str, Enum):
    QUARTERLY = "Q"
    ANNUAL = "Y"


class RankingType(str, Enum):
    VOLUME = "volume"
    TURNOVER = "turnover"
    PRICE_CHANGE_UP = "up"
    PRICE_CHANGE_DOWN = "down"
    MARKET_CAP = "market_cap"
    FOREIGN_NET_BUY = "foreign_buy"
    FOREIGN_NET_SELL = "foreign_sell"
    INSTITUTIONAL_NET_BUY = "inst_buy"
    INSTITUTIONAL_NET_SELL = "inst_sell"
    SHORT_SELLING_VOLUME = "short_vol"
    SHORT_SELLING_VALUE = "short_val"
    MARGIN_BALANCE = "margin"
    BID_QTY = "bid_qty"
    ASK_QTY = "ask_qty"
    NEW_HIGH = "new_high"
    NEW_LOW = "new_low"
