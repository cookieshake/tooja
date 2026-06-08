"""Toss-specific rate-limit defaults.

The generic primitives (`RateLimitConfig`, `TokenBucket`) live in
`tooja.core.rate_limit`. This module only pins the default config.

Toss does not publish an exact per-second REST quota. We pick a conservative
5 requests/second (well below any plausible server limit) and reuse KIS's
retry/backoff defaults (`max_retries=5`, `base_backoff=0.1`). Users who know
their real entitlement can override via `TossBroker(rate_limit=...)`.
"""

from __future__ import annotations

from tooja.core.rate_limit import RateLimitConfig, TokenBucket

__all__ = ["RateLimitConfig", "TokenBucket", "DEFAULT"]


# Conservative assumption — Toss publishes no exact REST rate limit.
DEFAULT = RateLimitConfig(per_sec=5)
