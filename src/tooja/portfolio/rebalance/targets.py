"""Target allocation helpers: nested weight config flattening & validation."""

from __future__ import annotations

import logging
from decimal import Decimal

from tooja.portfolio.rebalance.models import TargetSpec, TargetWeight

logger = logging.getLogger(__name__)


def flatten_targets(
    specs: list[TargetSpec | dict], parent_pct: Decimal = Decimal("1.0")
) -> list[TargetWeight]:
    """Normalize a tree of TargetSpec (or dicts) into a flat list of TargetWeight.

    Weights are normalized within each sibling group, then scaled by parent_pct.
    Accepts TargetSpec instances or dicts (validated via pydantic) — invalid
    structures raise ValidationError rather than being silently skipped.
    """
    parsed = [TargetSpec.model_validate(s) for s in specs]
    total = sum((s.weight for s in parsed), Decimal("0"))
    if total == 0:
        return []
    out: list[TargetWeight] = []
    for s in parsed:
        abs_pct = (s.weight / total) * parent_pct
        if s.symbol is not None:
            out.append(TargetWeight(symbol=s.symbol, weight=abs_pct))
        else:
            out.extend(flatten_targets(s.children, abs_pct))  # children already TargetSpec
    return out


def validate_targets(targets: list[TargetWeight]) -> None:
    total = sum((t.weight for t in targets), Decimal("0"))
    if not (Decimal("0.99") <= total <= Decimal("1.01")):
        logger.warning("total target allocation is %.2f%%, expected 100%%.", total * 100)
