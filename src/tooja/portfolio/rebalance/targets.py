"""Target allocation helpers: nested weight config flattening & validation."""

from __future__ import annotations

import logging
from decimal import Decimal
from typing import Any

from tooja.core.models import Symbol
from tooja.portfolio.rebalance.models import TargetWeight

logger = logging.getLogger(__name__)


def flatten_targets(config: Any, parent_pct: Decimal = Decimal("1.0")) -> list[TargetWeight]:
    """Parse [weight, ticker] / [weight, [...]] nested config into flat TargetWeight list.

    ticker strings are parsed via Symbol.parse, so "005930" and "NASD:AAPL" both work.
    Weights are normalized within each sibling group, then scaled by parent_pct.
    """
    if not isinstance(config, list):
        raise ValueError(f"config must be a list, got {type(config)}")
    if not config:
        return []

    total_weight = Decimal("0")
    for item in config:
        if not isinstance(item, list) or len(item) < 2:
            logger.warning("skipping invalid item: %s", item)
            continue
        total_weight += Decimal(str(item[0]))
    if total_weight == 0:
        return []

    targets: list[TargetWeight] = []
    for item in config:
        if not isinstance(item, list) or len(item) < 2:
            continue
        weight = Decimal(str(item[0]))
        content = item[1]
        abs_pct = (weight / total_weight) * parent_pct
        if isinstance(content, str):
            targets.append(TargetWeight(symbol=Symbol.parse(content), weight=abs_pct))
        elif isinstance(content, list):
            targets.extend(flatten_targets(content, abs_pct))
        else:
            logger.warning("invalid content type in %s: %s", item, type(content))
    return targets


def validate_targets(targets: list[TargetWeight]) -> None:
    total = sum((t.weight for t in targets), Decimal("0"))
    if not (Decimal("0.99") <= total <= Decimal("1.01")):
        logger.warning("total target allocation is %.2f%%, expected 100%%.", total * 100)
