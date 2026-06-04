"""Generic rate-limit primitives — broker-agnostic.

`RateLimitConfig` is what user code constructs to override per-broker defaults.
`TokenBucket` is the async sliding-window throttle the adapter wraps each
request in.

Both are independent of any specific broker; they only assume requests-per-
second + retries-on-rate-limit semantics, which every adapter we've seen so
far follows.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class RateLimitConfig:
    """Tunable rate-limit knobs.

    Fields:
      per_sec      : TokenBucket capacity (max requests per 1.0s window)
      max_retries  : How many times to retry when the broker reports rate-limit
      base_backoff : Initial sleep on retry; doubles each attempt
                     (total sleep <= base * (2^max_retries - 1))
    """

    per_sec: int
    max_retries: int = 5
    base_backoff: float = 0.1

    def __post_init__(self) -> None:
        if self.per_sec < 1:
            raise ValueError(f"per_sec must be >= 1 (got {self.per_sec})")
        if self.max_retries < 0:
            raise ValueError(f"max_retries must be >= 0 (got {self.max_retries})")
        if self.base_backoff < 0:
            raise ValueError(f"base_backoff must be >= 0 (got {self.base_backoff})")


class TokenBucket:
    """Sliding 1-second window with `capacity` permits.

    On each acquire, drop timestamps older than 1.0s; if the window still has
    `capacity` entries, sleep until the oldest expires.
    """

    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError(f"capacity must be >= 1 (got {capacity})")
        self._capacity = capacity
        self._window: list[float] = []
        self._lock = asyncio.Lock()

    @property
    def capacity(self) -> int:
        return self._capacity

    async def acquire(self) -> None:
        while True:
            async with self._lock:
                now = time.monotonic()
                cutoff = now - 1.0
                i = 0
                for ts in self._window:
                    if ts > cutoff:
                        break
                    i += 1
                if i:
                    del self._window[:i]
                if len(self._window) < self._capacity:
                    self._window.append(now)
                    return
                wait = self._window[0] + 1.0 - now
            await asyncio.sleep(max(wait, 0.001))

    async def __aenter__(self) -> "TokenBucket":
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None
