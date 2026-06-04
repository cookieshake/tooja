"""Async token bucket for KIS REST rate limiting.

KIS limits: 20 RPS (real), 2 RPS (demo).
The bucket refills `capacity` tokens every 1.0s wall-clock. acquire() takes
exactly one token; if empty, waits until the next refill window.

Usage:
    limiter = TokenBucket(capacity=20)
    async with limiter:
        ... call KIS ...
"""

from __future__ import annotations

import asyncio
import time


class TokenBucket:
    """Sliding 1-second window with `capacity` permits.

    Implementation: we track timestamps of the last `capacity` acquires. On
    each acquire, drop timestamps older than 1.0s; if the window still has
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
                # Drop expired entries (older than 1.0s).
                cutoff = now - 1.0
                # Trim from the front (oldest first).
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
                # Oldest entry expires at self._window[0] + 1.0.
                wait = self._window[0] + 1.0 - now
            await asyncio.sleep(max(wait, 0.001))

    async def __aenter__(self) -> "TokenBucket":
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None
