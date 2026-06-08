"""Toss API credentials."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TossCredentials:
    client_id: str
    client_secret: str

    def __repr__(self) -> str:
        tail = self.client_id[-4:] if len(self.client_id) >= 4 else "*" * len(self.client_id)
        return f"TossCredentials(client_id=***{tail}, client_secret=***)"
