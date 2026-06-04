"""KIS response -> shared exception mapping.

`classify_kis_error(rt_cd, msg_cd, msg)`:
  - rt_cd == "0" or msg_cd == "MCA00000": success -> None
  - msg_cd present in the mapping table: that class
  - msg matches a pattern: that class
  - otherwise: BrokerAPIError
"""

from __future__ import annotations

import re

from tooja.core.errors import (
    AuthError,
    BrokerAPIError,
    BrokerError,
    InsufficientFunds,
    MarketClosed,
    NetworkError,
    OrderNotFound,
    OrderRejected,
    PermissionDenied,
    RateLimitError,
    SymbolNotFound,
)


_KIS_ERROR_MAP: dict[str, type[BrokerError]] = {
    # Auth
    "EGW00121": AuthError,
    "EGW00123": AuthError,
    # Permission / not enrolled
    "APAC0134": PermissionDenied,
    "SKFT2101": PermissionDenied,
    "EGW00550": PermissionDenied,
    # Call constraints
    "EGW00201": RateLimitError,
    "EGW00203": NetworkError,
    # Orders
    "APBK1227": OrderRejected,
    "APBK1631": SymbolNotFound,
}


# Patterns match the Korean error text that KIS actually returns — do not translate.
_KIS_MSG_PATTERNS: list[tuple[re.Pattern, type[BrokerError]]] = [
    (re.compile(r"잔고\s*부족|예수금\s*부족"), InsufficientFunds),
    (re.compile(r"장\s*마감|개장\s*전"), MarketClosed),
    (re.compile(r"주문번호.*없"), OrderNotFound),
]


def classify_kis_error(rt_cd: str, msg_cd: str, msg: str | None) -> type[BrokerError] | None:
    """Return None on success; otherwise return the exception class to raise."""
    if rt_cd == "0" or msg_cd == "MCA00000":
        return None
    cls = _KIS_ERROR_MAP.get(msg_cd)
    if cls is not None:
        return cls
    for pat, err_cls in _KIS_MSG_PATTERNS:
        if pat.search(msg or ""):
            return err_cls
    return BrokerAPIError
