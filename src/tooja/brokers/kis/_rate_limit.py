"""KIS-specific rate-limit defaults.

The generic primitives (`RateLimitConfig`, `TokenBucket`) live in
`tooja.core.rate_limit`. This module only pins the per-env defaults that
match KIS's published limits.
"""

from __future__ import annotations

from tooja.core.rate_limit import RateLimitConfig, TokenBucket

__all__ = ["RateLimitConfig", "TokenBucket", "DEFAULT_REAL", "DEFAULT_DEMO"]


DEFAULT_REAL = RateLimitConfig(per_sec=20)
DEFAULT_DEMO = RateLimitConfig(per_sec=2)
