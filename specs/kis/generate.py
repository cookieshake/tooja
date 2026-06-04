"""Generate tooja.brokers.kis.raw.* from apiportal api-list JSON.

Run: uv run python specs/kis/generate.py [--dry-run] [--category <slug>]
Inputs:  specs/kis/api-list/<category_slug>.json
Outputs: src/tooja/brokers/kis/raw/<category_slug>/<endpoint_slug>.py

Nested output handling:
- propertyOrder ``006`` (parent, A0005/A0003/A0002) + ``006.001``... (children, A0001 etc.)
- Parent A0005 (Object Array) -> ``list[<Name>Item]`` + separate Item class
- Parent A0003 (Object)       -> ``<Name>Item | None`` + separate Item class
- Parent A0002 (Array)        -> ``list[str] | None`` (treated as scalar array)
- Orphan child (no parent)    -> exposed as a flat field
- Siblings whose propertyOrder differs only in the integer part = top-level scalars
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import OrderedDict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SPEC_DIR = HERE / "api-list"
OUT_ROOT = ROOT / "src" / "tooja" / "brokers" / "kis" / "raw"
CATEGORIES_FILE = HERE / "categories.json"

PYTHON_KEYWORDS = {"False", "None", "True", "and", "as", "assert", "async", "await",
                   "break", "class", "continue", "def", "del", "elif", "else", "except",
                   "finally", "for", "from", "global", "if", "import", "in", "is",
                   "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try",
                   "while", "with", "yield"}


# ---------- string helpers ----------

def slugify_endpoint(access_url: str) -> str:
    last = access_url.rstrip("/").rsplit("/", 1)[-1]
    last = last.lower()
    last = re.sub(r"[^a-z0-9_]+", "_", last)
    last = re.sub(r"_+", "_", last).strip("_")
    if not last or last[0].isdigit():
        last = "_" + last
    return last


def primary_tr_id(raw: str | None) -> str:
    if not raw:
        return ""
    m = re.search(r"[A-Z0-9]+", raw)
    return m.group(0) if m else ""


def pascal(slug: str) -> str:
    return "".join(p.capitalize() for p in re.split(r"[^A-Za-z0-9]+", slug) if p)


def safe_ident(name: str) -> str:
    n = re.sub(r"[^A-Za-z0-9_]", "_", name)
    if n and n[0].isdigit():
        n = "_" + n
    if n in PYTHON_KEYWORDS:
        n = n + "_"
    return n


def short_desc(text: str | None) -> str:
    if not text:
        return ""
    cleaned = re.sub(r"<[^>]+>", " ", text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


# ---------- type mapping ----------

def scalar_type(prop_type: str, required: str) -> str:
    """A0001/A0004 (scalar) -> str/SDecimal. Anything else falls back."""
    is_required = required == "Y"
    if prop_type == "A0004":
        return "SDecimal"  # always nullable (= Decimal | None)
    if prop_type == "A0001":
        return "str" if is_required else "str | None"
    if prop_type == "A0003":
        return "dict" if is_required else "dict | None"
    if prop_type in ("A0002", "A0005"):
        return "list" if is_required else "list | None"
    # Corrupted data (e.g. propertyType='응답상세2') — fall back to str.
    return "str | None"


def default_for(prop_type: str, required: str) -> str:
    if required == "Y":
        if prop_type == "A0004":
            return " = None"  # SDecimal can always default to None
        if prop_type == "A0001":
            return ""
        return ""
    return " = None"


# ---------- grouping ----------

def dedupe(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Dedup by propertyCd+propertyOrder. Same cd with a different order = distinct."""
    seen = OrderedDict()
    for it in items:
        k = (it.get("propertyCd"), it.get("propertyOrder"))
        if k not in seen:
            seen[k] = it
    return list(seen.values())


def order_key(s: str) -> tuple[float, ...]:
    """``006.001`` -> (6.0, 1.0); ``007`` -> (7.0,). For stable sorting."""
    parts = (s or "0").split(".")
    out: list[float] = []
    for p in parts:
        try:
            out.append(float(p))
        except ValueError:
            out.append(0.0)
    return tuple(out)


def group_body(props: list[dict[str, Any]]) -> list[tuple[dict[str, Any] | None, list[dict[str, Any]]]]:
    """Group properties by parent-child propertyOrder relationship.

    Returns: list of (parent, children).
    - parent != None & children == [] -> top-level scalar
    - parent != None & children != [] -> container (A0005/A0003/A0002)
    - parent == None (orphan child)   -> flatten
    """
    props = dedupe(props)
    by_order = {p.get("propertyOrder"): p for p in props}

    top_level = [p for p in props if "." not in (p.get("propertyOrder") or "")]
    top_level.sort(key=lambda p: order_key(p.get("propertyOrder") or "0"))

    consumed: set[str] = set()
    groups: list[tuple[dict[str, Any] | None, list[dict[str, Any]]]] = []
    for parent in top_level:
        parent_order = parent.get("propertyOrder") or ""
        children = sorted(
            (p for p in props if (p.get("propertyOrder") or "").startswith(parent_order + ".")),
            key=lambda p: order_key(p.get("propertyOrder") or "0"),
        )
        consumed.add(parent_order)
        for c in children:
            consumed.add(c.get("propertyOrder") or "")
        groups.append((parent, children))

    # Orphans: propertyOrder contains a dot but no matching parent.
    orphans = [p for p in props if "." in (p.get("propertyOrder") or "") and (p.get("propertyOrder") not in consumed)]
    orphans.sort(key=lambda p: order_key(p.get("propertyOrder") or "0"))
    for o in orphans:
        # Double-check `consumed` (the loop above may have already consumed the parent).
        if o.get("propertyOrder") not in consumed:
            groups.append((None, [o]))

    return groups


# ---------- rendering ----------

def field_line(p: dict[str, Any], explicit_type: str | None = None,
               explicit_default: str | None = None, *, force_nullable: bool = False) -> str:
    name = safe_ident(p["propertyCd"])
    # Response field requireYn often disagrees with actual API behavior — caller uses force_nullable.
    required = "N" if force_nullable else p["requireYn"]
    ty = explicit_type or scalar_type(p["propertyType"], required)
    default = explicit_default if explicit_default is not None else default_for(p["propertyType"], required)
    nm = short_desc(p.get("propertyNm"))
    desc = short_desc(p.get("description"))
    comment = nm + (f" — {desc}" if desc and desc != nm else "")
    line = f"    {name}: {ty}{default}"
    if comment.strip():
        line += f"  # {comment.strip()[:140]}"
    return line


def render_item_class(class_name: str, children: list[dict[str, Any]],
                      *, force_nullable: bool = False) -> tuple[str, bool]:
    use_decimal = False
    lines: list[str] = []
    for c in children:
        required = "N" if force_nullable else c["requireYn"]
        ty = scalar_type(c["propertyType"], required)
        if ty == "SDecimal":
            use_decimal = True
        lines.append(field_line(c, force_nullable=force_nullable))
    body = "\n".join(lines) or "    pass"
    return f'class {class_name}(KisBaseModel):\n    """nested item."""\n\n{body}\n', use_decimal


def render_body_class(class_name: str, base: str,
                      groups: list[tuple[dict[str, Any] | None, list[dict[str, Any]]]],
                      docstring: str,
                      *,
                      skip_common: bool = False,
                      force_nullable: bool = False) -> tuple[str, list[str], bool]:
    """Render the body class (Request or Response) plus any extra Item classes.

    Returns: (main_class_src, [item_class_srcs], use_decimal)
    """
    use_decimal = False
    item_classes: list[str] = []
    field_lines: list[str] = []

    for parent, children in groups:
        if parent is None:
            for c in children:
                required = "N" if force_nullable else c["requireYn"]
                ty = scalar_type(c["propertyType"], required)
                if ty == "SDecimal":
                    use_decimal = True
                field_lines.append(field_line(c, force_nullable=force_nullable))
            continue

        if skip_common and parent["propertyCd"] in ("rt_cd", "msg_cd", "msg1"):
            continue

        if not children:
            required = "N" if force_nullable else parent["requireYn"]
            ty = scalar_type(parent["propertyType"], required)
            if ty == "SDecimal":
                use_decimal = True
            field_lines.append(field_line(parent, force_nullable=force_nullable))
            continue

        # nested container
        item_cls = f"{class_name}_{pascal(parent['propertyCd'])}Item"
        item_src, item_dec = render_item_class(item_cls, children, force_nullable=force_nullable)
        item_classes.append(item_src)
        use_decimal = use_decimal or item_dec

        ptype = parent["propertyType"]
        if ptype == "A0005":
            field_ty = f"list[{item_cls}]"
            default = " = []"
        elif ptype == "A0003":
            field_ty = f"{item_cls} | None"
            default = " = None"
        elif ptype == "A0002":
            field_ty = "list[str]"
            default = " = []"
        else:
            field_ty = "list"
            default = " = []"

        field_lines.append(field_line(parent, explicit_type=field_ty, explicit_default=default))

    body = "\n".join(field_lines) or "    pass"
    main = f'class {class_name}({base}):\n    """{docstring}"""\n\n{body}\n'
    return main, item_classes, use_decimal


def render_rest(ep: dict[str, Any], slug: str) -> str:
    name_pascal = pascal(slug)
    request_cls = f"{name_pascal}Request"
    response_cls = f"{name_pascal}Response"
    executor_cls = f"{name_pascal}Executor"

    props = ep.get("apiPropertys") or []
    req_b = [p for p in props if p["bodyType"] == "req_b"]
    res_b = [p for p in props if p["bodyType"] == "res_b"]

    has_rt_cd = any(p["propertyCd"] == "rt_cd" for p in res_b)

    req_groups = group_body(req_b)
    res_groups = group_body(res_b)

    req_src, req_items, req_dec = render_body_class(
        request_cls, "KisBaseModel", req_groups, docstring="요청."
    )
    base = "KisCommonResponse" if has_rt_cd else "KisBaseModel"
    res_src, res_items, res_dec = render_body_class(
        response_cls, base, res_groups, docstring="응답 본문.",
        skip_common=has_rt_cd,
        force_nullable=True,  # KIS spec required disagrees with actual response — mark all nullable for safety.
    )

    use_decimal = req_dec or res_dec

    tr_id = primary_tr_id(ep.get("realTrId"))
    tr_id_v = primary_tr_id(ep.get("virtualTrId"))
    method = (ep.get("httpMethod") or "GET").upper()
    api_summary = short_desc(ep.get("apiSummary"))[:240]
    name = ep.get("name", "")

    import_line = "from tooja.brokers.kis.raw.base import (\n    ApiExecutor, KisBaseModel, KisCommonResponse,"
    if use_decimal:
        import_line += " SDecimal,"
    import_line += "\n)"

    parts: list[str] = [
        '"""Auto-generated from apiportal spec — do not edit by hand."""',
        "",
        "from __future__ import annotations",
        "",
        import_line,
        "",
        "",
        *req_items,
        req_src,
        *res_items,
        res_src,
        f'class {executor_cls}(ApiExecutor[{request_cls}, {response_cls}]):',
        f'    """{name}."""',
    ]
    if api_summary:
        parts += ["", f'    # {api_summary}']
    parts += [
        "",
        f'    PATH = "{ep["accessUrl"]}"',
        f'    METHOD = "{method}"',
        f"    RESPONSE_TYPE = {response_cls}",
    ]
    if tr_id:
        parts.append(f'    TR_ID = "{tr_id}"')
    if tr_id_v and tr_id_v != tr_id:
        parts.append(f'    TR_ID_VIRTUAL = "{tr_id_v}"')
    parts.append("")
    return "\n".join(parts)


def render_ws(ep: dict[str, Any], slug: str) -> str:
    name_pascal = pascal(slug)
    msg_cls = f"{name_pascal}Message"
    sub_cls = f"{name_pascal}Subscriber"
    props = ep.get("apiPropertys") or []
    res_b = [p for p in props if p["bodyType"] == "res_b"]

    # WS is a ^-delimited stream of single records, so flattening is natural (drop the nested parent cds).
    res_b_dedup = dedupe(res_b)
    flat = [p for p in res_b_dedup
            if p["propertyType"] in ("A0001", "A0004") and "." not in (p.get("propertyOrder") or "")]
    nested_children = [p for p in res_b_dedup if "." in (p.get("propertyOrder") or "")]
    # When nested fields exist (rare), flatten using only children (the parent is a container, not in ^-stream).
    flat_props = nested_children if nested_children else flat
    flat_props = sorted(flat_props, key=lambda p: order_key(p.get("propertyOrder") or "0"))

    use_decimal = any(p["propertyType"] == "A0004" for p in flat_props)
    columns = [safe_ident(p["propertyCd"]) for p in flat_props]

    msg_groups = [(None, [p]) for p in flat_props]
    msg_src, _, _ = render_body_class(msg_cls, "KisBaseModel", msg_groups, docstring="WS 메시지 1건.")

    tr_id = primary_tr_id(ep.get("realTrId"))
    name = ep.get("name", "")
    cols_repr = ", ".join(f'"{c}"' for c in columns)

    import_line = "from tooja.brokers.kis.raw.base import KisBaseModel"
    if use_decimal:
        import_line += ", SDecimal"
    return "\n".join([
        '"""Auto-generated from apiportal spec — do not edit by hand."""',
        "",
        "from __future__ import annotations",
        "",
        import_line,
        "from tooja.brokers.kis.raw.ws_base import WsSubscriber",
        "",
        "",
        msg_src,
        f'class {sub_cls}(WsSubscriber[{msg_cls}]):',
        f'    """{name}."""',
        "",
        f'    TR_ID = "{tr_id}"',
        f"    RESPONSE_TYPE = {msg_cls}",
        f"    COLUMNS = ({cols_repr},)",
        "",
    ])


def is_ws_endpoint(category_slug: str, ep: dict[str, Any]) -> bool:
    if category_slug.endswith("_ws"):
        return True
    return (ep.get("accessUrl") or "").startswith("/tryitout/")


def generate(dry_run: bool = False, only_category: str | None = None) -> None:
    cats = json.loads(CATEGORIES_FILE.read_text())
    if not dry_run and not only_category:
        for entry in OUT_ROOT.iterdir():
            if entry.is_dir():
                shutil.rmtree(entry)
    counts = {"rest": 0, "ws": 0, "skip": 0, "nested_containers": 0}
    name_collisions: list[tuple[str, str]] = []
    for cat in cats:
        slug = cat["slug"]
        if only_category and slug != only_category:
            continue
        spec_path = SPEC_DIR / f"{slug}.json"
        if not spec_path.exists():
            print(f"  ! missing spec: {spec_path}")
            continue
        endpoints = json.loads(spec_path.read_text())
        out_dir = OUT_ROOT / slug
        if not dry_run:
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "__init__.py").write_text("")
        emitted: set[str] = set()
        for ep in endpoints:
            ws = is_ws_endpoint(slug, ep)
            endpoint_slug = slugify_endpoint(ep["accessUrl"])
            if endpoint_slug in emitted:
                tr = primary_tr_id(ep.get("realTrId")).lower() or f"v{len(emitted)}"
                endpoint_slug = f"{endpoint_slug}_{tr}"
                base = endpoint_slug
                n = 2
                while endpoint_slug in emitted:
                    endpoint_slug = f"{base}_{n}"
                    n += 1
                name_collisions.append((slug, endpoint_slug))
            emitted.add(endpoint_slug)
            try:
                src = render_ws(ep, endpoint_slug) if ws else render_rest(ep, endpoint_slug)
            except Exception as e:
                print(f"  ! render failed {slug}/{endpoint_slug}: {e}")
                counts["skip"] += 1
                continue
            counts["ws" if ws else "rest"] += 1
            # Stats: count nested containers.
            for p in ep.get("apiPropertys") or []:
                if "." in (p.get("propertyOrder") or ""):
                    counts["nested_containers"] += 1
                    break  # Count once per endpoint.
            if not dry_run:
                (out_dir / f"{endpoint_slug}.py").write_text(src)
        if not dry_run:
            print(f"  + {slug}: {len(endpoints)} files")
    print(f"\nGenerated REST={counts['rest']} WS={counts['ws']} skipped={counts['skip']}")
    print(f"Endpoints with nested containers: {counts['nested_containers']}")
    if name_collisions:
        print(f"Slug collisions resolved: {len(name_collisions)}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--category", default=None)
    args = p.parse_args()
    generate(dry_run=args.dry_run, only_category=args.category)
