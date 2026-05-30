"""Pytest config — load .env and resolve KIS_ENV → KIS_* canonical keys."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

CANONICAL_KEYS = ("APP_KEY", "APP_SECRET", "CANO", "ACNT_PRDT_CD", "HTS_ID")


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip())


def _resolve_env_profile() -> None:
    """KIS_ENV(demo|real)에 따라 KIS_<PROFILE>_*를 KIS_*에 채움.

    이미 KIS_* 직접 설정된 값이 있으면 그대로 둠 (덮어쓰기 X).
    """
    env = os.environ.get("KIS_ENV", "demo").lower()
    profile = "REAL" if env == "real" else "DEMO"
    for key in CANONICAL_KEYS:
        target = f"KIS_{key}"
        source = f"KIS_{profile}_{key}"
        if not os.environ.get(target) and os.environ.get(source):
            os.environ[target] = os.environ[source]


@pytest.fixture(scope="session", autouse=True)
def _load_env() -> None:
    _load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    _resolve_env_profile()
