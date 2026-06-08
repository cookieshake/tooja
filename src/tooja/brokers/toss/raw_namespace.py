"""`broker.raw.<category>` entry point for the Toss raw layer.

Mirrors ``tooja.brokers.kis.raw_namespace``: each category attribute lazily
imports the underlying ``tooja.brokers.toss.raw.<category>`` package on first
access and delegates attribute lookups to it. Endpoint executors live in
submodules (e.g. ``raw.market_data.get_prices.GetPricesExecutor``); attribute
access on the category also resolves the executor/request classes exported by
those submodules so ``broker.raw.market_data.GetPricesExecutor`` works.
"""

from __future__ import annotations

import importlib
import pkgutil
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tooja.brokers.toss.broker import TossBroker


# Categories under raw/ (the generated Toss domains).
_CATEGORIES: frozenset[str] = frozenset({
    "account",
    "asset",
    "auth",
    "market_data",
    "market_info",
    "order",
    "order_history",
    "order_info",
    "stock_info",
})


class _Category:
    """Category placeholder — imports the underlying raw package on first access.

    Attribute lookups first try the package module itself, then fall back to
    scanning the package's submodules for the named attribute (executor / request
    classes live one level down, in per-endpoint modules).
    """

    def __init__(self, broker: "TossBroker", module_name: str):
        self._resolved: dict[str, object] = {}
        self._broker = broker
        self._module_name = module_name
        self._module = importlib.import_module(
            f"tooja.brokers.toss.raw.{module_name}"
        )

    def __getattr__(self, name: str):
        # Cached resolutions skip the submodule scan on repeat access.
        # (_resolved is set first in __init__, so this lookup never recurses.)
        resolved = self._resolved
        if name in resolved:
            return resolved[name]
        # 1) Attribute exported directly by the category package.
        try:
            value = getattr(self._module, name)
        except AttributeError:
            value = self._resolve_from_submodules(name)
        resolved[name] = value
        return value

    def _resolve_from_submodules(self, name: str):
        # Search per-endpoint submodules for the named attribute (executor /
        # request classes live one level down, in per-endpoint modules).
        path = self._module.__path__  # type: ignore[attr-defined]
        for info in pkgutil.iter_modules(path):
            sub = importlib.import_module(
                f"tooja.brokers.toss.raw.{self._module_name}.{info.name}"
            )
            if hasattr(sub, name):
                return getattr(sub, name)
        raise AttributeError(
            f"category {self._module_name!r} has no attribute {name!r}"
        )


class TossRawNamespace:
    """`broker.raw.*` entry point. Categories are imported and cached on first access."""

    def __init__(self, broker: "TossBroker"):
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
