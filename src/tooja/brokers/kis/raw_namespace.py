"""Skeleton for exposing client.raw.<category>.<endpoint>(...).

This plan: attach category attributes and reserve the spot for a future Executor
functional wrapper. The Executor call body itself lives in a separate plan.
"""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker


# Categories under raw/ (oauth + 21 domains)
_CATEGORIES: frozenset[str] = frozenset({
    "oauth",
    "domestic_bond_quotations", "domestic_bond_trading", "domestic_bond_ws",
    "domestic_futureoption_quotations", "domestic_futureoption_trading",
    "domestic_futureoption_ws",
    "domestic_stock_elw_quotations", "domestic_stock_industry",
    "domestic_stock_info", "domestic_stock_quotations",
    "domestic_stock_quote_analysis", "domestic_stock_rank_analysis",
    "domestic_stock_trading", "domestic_stock_ws",
    "overseas_futureoption_quotations", "overseas_futureoption_trading",
    "overseas_futureoption_ws",
    "overseas_stock_quotations", "overseas_stock_quote_analysis",
    "overseas_stock_trading", "overseas_stock_ws",
})


class _Category:
    """Category placeholder — imports the underlying raw module on first access and delegates attribute lookups."""

    def __init__(self, broker: "KisBroker", module_name: str):
        self._broker = broker
        self._module = importlib.import_module(f"tooja.brokers.kis.raw.{module_name}")

    def __getattr__(self, name: str):
        return getattr(self._module, name)


class KisRawNamespace:
    """`client.raw.*` entry point. Categories are imported and cached on first access."""

    def __init__(self, broker: "KisBroker"):
        self._broker = broker
        self._cache: dict[str, _Category] = {}

    def __getattr__(self, name: str) -> _Category:
        if name in _CATEGORIES:
            cat = self._cache.get(name)
            if cat is None:
                cat = _Category(self._broker, name)
                self._cache[name] = cat
            return cat
        raise AttributeError(
            f"{type(self).__name__!r} has no category {name!r}"
        )
