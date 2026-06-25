"""Two-phase confirm tokens binding an order preview to its execution."""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import time
from collections.abc import Callable
from typing import Any


class ConfirmGate:
    def __init__(
        self,
        *,
        secret: bytes | None = None,
        ttl: float = 300.0,
        now: Callable[[], float] = time.time,
    ) -> None:
        self._secret = secret or secrets.token_bytes(32)
        self._ttl = ttl
        self._now = now

    def _sign(self, account: str, payload: dict[str, Any], exp: int) -> str:
        body = json.dumps(
            {"account": account, "payload": payload, "exp": exp},
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode()
        return hmac.new(self._secret, body, hashlib.sha256).hexdigest()[:32]

    def issue(self, account: str, payload: dict[str, Any]) -> str:
        exp = int(self._now() + self._ttl)
        return f"{exp}.{self._sign(account, payload, exp)}"

    def verify(self, account: str, payload: dict[str, Any], token: str) -> bool:
        exp_str, _, sig = token.partition(".")
        if not sig or not exp_str.isdigit():
            return False
        exp = int(exp_str)
        if self._now() > exp:
            return False
        return hmac.compare_digest(sig, self._sign(account, payload, exp))
