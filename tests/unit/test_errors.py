import pytest

from tooja.core.errors import (
    AuthError,
    BrokerAPIError,
    BrokerError,
    ConfigError,
    InsufficientFunds,
    MarketClosed,
    NetworkError,
    OrderError,
    OrderNotFound,
    OrderRejected,
    PermissionDenied,
    RateLimitError,
    SubscriptionLimitExceeded,
    SymbolNotFound,
    TimeoutError as BrokerTimeoutError,
    UnsupportedOperation,
)


def test_root_constructor_preserves_raw():
    err = BrokerError(
        "boom",
        broker="kis",
        raw_code="EGW00203",
        raw_message="OPS routing error",
        endpoint="/uapi/...",
    )
    assert str(err) == "boom"
    assert err.broker == "kis"
    assert err.raw_code == "EGW00203"
    assert err.raw_message == "OPS routing error"
    assert err.endpoint == "/uapi/..."


def test_hierarchy_subclasses_all_inherit_from_broker_error():
    for cls in (
        AuthError, PermissionDenied, RateLimitError, UnsupportedOperation,
        MarketClosed, SymbolNotFound, OrderError, OrderRejected,
        InsufficientFunds, OrderNotFound, NetworkError, BrokerTimeoutError,
        SubscriptionLimitExceeded, ConfigError, BrokerAPIError,
    ):
        assert issubclass(cls, BrokerError)


def test_order_subclasses_inherit_from_order_error():
    assert issubclass(OrderRejected, OrderError)
    assert issubclass(InsufficientFunds, OrderError)
    assert issubclass(OrderNotFound, OrderError)


def test_timeout_inherits_from_network():
    assert issubclass(BrokerTimeoutError, NetworkError)


def test_timeout_inherits_from_builtin_timeout_error():
    """External code doing `except TimeoutError:` for the builtin must also catch ours."""
    import builtins

    assert issubclass(BrokerTimeoutError, builtins.TimeoutError)
    with pytest.raises(builtins.TimeoutError):
        raise BrokerTimeoutError("response delayed", broker="kis")


def test_rate_limit_carries_retry_after():
    err = RateLimitError("per-second limit exceeded", broker="kis", raw_code="EGW00201", retry_after=1.5)
    assert err.retry_after == 1.5


def test_can_catch_specific_or_root():
    with pytest.raises(BrokerError):
        raise AuthError("nope", broker="kis")
    with pytest.raises(AuthError):
        raise AuthError("nope", broker="kis")
