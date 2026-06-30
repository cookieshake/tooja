"""Serialize tooja domain models to JSON-safe structures for MCP tool results."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel


def to_json(obj: BaseModel | Sequence[BaseModel] | None) -> Any:
    if obj is None:
        return None
    if isinstance(obj, BaseModel):
        return obj.model_dump(mode="json")
    return [item.model_dump(mode="json") for item in obj]
