"""Shared broker exception hierarchy.

Unmapped broker errors are surfaced as BrokerAPIError with raw_code/raw_message preserved.
"""

from __future__ import annotations

import builtins


class BrokerError(Exception):
    """Root of every broker-originated error."""

    def __init__(
        self,
        message: str,
        *,
        broker: str,
        raw_code: str | None = None,
        raw_message: str | None = None,
        endpoint: str | None = None,
    ):
        super().__init__(message)
        self.broker = broker
        self.raw_code = raw_code
        self.raw_message = raw_message
        self.endpoint = endpoint

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.args[0]!r}, broker={self.broker!r}, "
            f"raw_code={self.raw_code!r}, endpoint={self.endpoint!r})"
        )


# Auth / permissions
class AuthError(BrokerError):
    """Expired token, invalid key, signing failure."""


class PermissionDenied(BrokerError):
    """Account not enrolled or feature not authorized."""


# Call constraints
class RateLimitError(BrokerError):
    """Per-second call quota exceeded."""

    def __init__(self, message: str, *, retry_after: float | None = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class UnsupportedOperation(BrokerError):
    """Method not supported by this broker."""


# Market state
class MarketClosed(BrokerError):
    """Market closed / holiday."""


class SymbolNotFound(BrokerError):
    """Unknown ticker or delisted symbol."""


# Orders
class OrderError(BrokerError):
    """Base for order-related errors."""


class OrderRejected(OrderError):
    """Order rejected (quantity / price / limit)."""


class InsufficientFunds(OrderError):
    """Deposit / buying power insufficient."""


class OrderNotFound(OrderError):
    """Cancel/replace target order not found."""


# Network
class NetworkError(BrokerError):
    """Connection refused, DNS, TLS, etc."""


class TimeoutError(NetworkError, builtins.TimeoutError):  # noqa: A001 — intentional builtin shadow (import as `brokers.errors.TimeoutError`).
    """Response wait exceeded.

    Also inherits `builtins.TimeoutError` so that external code doing
    `except TimeoutError:` (the builtin) still catches our exception.
    """


# WS
class SubscriptionLimitExceeded(BrokerError):
    """WS concurrent subscription limit exceeded."""


# Config
class ConfigError(BrokerError):
    """Missing required credentials, etc."""


# Unclassified
class BrokerAPIError(BrokerError):
    """Unmapped broker error — passed through with raw_code/raw_message preserved."""
