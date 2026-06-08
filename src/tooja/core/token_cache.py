"""Secure, broker-agnostic cache for short-lived OAuth tokens.

Tokens are bearer credentials. They are stored OUTSIDE the repo, in the
per-user OS cache directory (platformdirs), with restrictive permissions
(dir 0700, files 0600), or kept in-process only when mode="memory".

Each broker adapter creates its own TokenStore(namespace=...) and addresses
entries by an opaque key. Callers embed a per-credential scope (scope_tag)
in the key so two accounts never share a slot.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Literal

import platformdirs

logger = logging.getLogger(__name__)

CacheMode = Literal["disk", "memory"]


def scope_tag(secret: str) -> str:
    """Stable, non-reversible 8-hex scope for a credential (multi-account safe)."""
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()[:8]


class TokenStore:
    """`key -> JSON dict` persistence with secure on-disk storage or memory mode."""

    def __init__(self, *, namespace: str, mode: CacheMode = "disk"):
        self.namespace = namespace
        self.mode: CacheMode = mode
        self._mem: dict[str, dict] = {}
        self._dir = Path(platformdirs.user_cache_dir("tooja")) / "tokens" / namespace

    def _path(self, key: str) -> Path:
        return self._dir / f"{key}.json"

    def load(self, key: str) -> dict | None:
        if self.mode == "memory":
            return self._mem.get(key)
        path = self._path(key)
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            logger.warning("token cache read failed %s: %s", path, e)
            return None

    def save(self, key: str, data: dict) -> None:
        if self.mode == "memory":
            self._mem[key] = dict(data)
            return
        try:
            self._dir.mkdir(parents=True, exist_ok=True)
            os.chmod(self._dir, 0o700)
        except OSError as e:
            logger.warning("token cache dir prep failed %s: %s", self._dir, e)
            return
        path = self._path(key)
        tmp = path.with_suffix(".tmp")
        try:
            fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp, path)
            os.chmod(path, 0o600)
        except OSError as e:
            logger.warning("token cache write failed %s: %s", path, e)
            try:
                tmp.unlink(missing_ok=True)
            except OSError:
                pass

    def delete(self, key: str) -> None:
        if self.mode == "memory":
            self._mem.pop(key, None)
            return
        try:
            self._path(key).unlink(missing_ok=True)
        except OSError as e:
            logger.warning("token cache delete failed %s: %s", self._path(key), e)
