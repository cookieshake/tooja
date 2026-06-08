"""Toss error code -> shared exception mapping.

`classify_toss_error(code, http_status)` returns the `BrokerError` subclass to
raise for a given Toss error envelope code (the `{error:{code,...}}` shape, or
the OAuth `{error: "..."}` shape). Always returns a class — ``BrokerAPIError``
is the fallback for any unmapped code; the function never returns ``None``.

Toss does not publish a stable numeric code table the way KIS does; codes are
hyphenated string slugs. We map the well-known auth / rate-limit / not-found
families and let everything else fall through to `BrokerAPIError`, which still
preserves `raw_code`/`raw_message` for the caller.
"""

from __future__ import annotations

from tooja.core.errors import (
    AuthError,
    BrokerAPIError,
    BrokerError,
    OrderNotFound,
    RateLimitError,
)

# Exact-code table. Codes are matched case-insensitively (see classify).
_TOSS_ERROR_MAP: dict[str, type[BrokerError]] = {
    # Auth — invalid / expired token, OAuth client failures, edge auth blocks.
    "invalid-token": AuthError,
    "expired-token": AuthError,
    "edge-blocked": AuthError,
    "invalid_client": AuthError,
    "invalid_grant": AuthError,
    "unauthorized_client": AuthError,
    "unauthorized": AuthError,
    # Rate limit — both the API gateway and the edge variants.
    "rate-limit-exceeded": RateLimitError,
    "edge-rate-limit-exceeded": RateLimitError,
    "too-many-requests": RateLimitError,
    # Orders / lookup.
    "order-not-found": OrderNotFound,
}


def classify_toss_error(code: str, http_status: int) -> type[BrokerError]:
    """Return the exception class to raise for a Toss error code.

    Always returns a class — falls back to ``BrokerAPIError`` for any unmapped
    code (generic 4xx/5xx), preserving the raw code/message at the call site.
    Never returns ``None``.
    """
    if not code:
        return BrokerAPIError
    cls = _TOSS_ERROR_MAP.get(code) or _TOSS_ERROR_MAP.get(code.lower())
    if cls is not None:
        return cls
    # HTTP-status fallbacks for codes we don't recognise.
    if http_status == 401 or http_status == 403:
        return AuthError
    if http_status == 429:
        return RateLimitError
    return BrokerAPIError
