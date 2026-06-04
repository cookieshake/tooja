"""KIS credentials.

The caller passes keys explicitly (no environment-variable auto-discovery). Load
keys via dotenv / a secret manager and hand them to KisBroker directly.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KisCredentials:
    app_key: str
    app_secret: str
    cano: str
    acnt_prdt_cd: str
    hts_id: str

    def __repr__(self) -> str:
        # Mask app_key (show last 4) and app_secret (full mask) — never expose secrets in logs.
        app_key_tail = self.app_key[-4:] if len(self.app_key) >= 4 else "*" * len(self.app_key)
        return (
            f"KisCredentials(app_key=***{app_key_tail}, app_secret=***, "
            f"cano={self.cano!r}, acnt_prdt_cd={self.acnt_prdt_cd!r}, "
            f"hts_id={self.hts_id!r})"
        )
