"""Generate tooja.brokers.toss.raw.* from the vendored OpenAPI 3.1 document.

Run: uv run python specs/toss/generate.py [--dry-run]
Input:   specs/toss/openapi.json (OpenAPI 3.1.0)
Outputs: src/tooja/brokers/toss/raw/models.py
         src/tooja/brokers/toss/raw/<tag_slug>/<operation>.py  (+ __init__.py per tag)

Design (mirrors specs/kis/generate.py style: helpers, render-to-string, file writing):

- One pydantic model per components/schemas entry in models.py. Field names are
  snake_case Python identifiers; every property carries an explicit
  ``Field(alias="<exact wire name>")`` so OAuth snake_case keys (grant_type, ...)
  and camelCase keys both round-trip. No blanket alias_generator (TossBaseModel
  has populate_by_name=True + extra=ignore).

- Type mapping:
    string + format:decimal -> TDecimal (default None)
    integer                 -> int | None (or int if required)
    boolean                 -> bool | None
    string (date/date-time/enum/plain) -> str | None (or str if required)
    $ref to object schema   -> "<Name> | None" (forward-ref string)
    array                   -> list[<item>] = []
    nullable (type:[X,null] / oneOf:[{$ref},{type:null}]) -> optional, default None
    enums (named $ref or inline) -> str (raw value kept; forward-compat, no Enum/Literal)
    allOf:[{$ref X}] single-ref wrapper -> treated as $ref X

- The only real oneOf (OrderCreateRequest) -> ONE model merging all variant
  properties, every field optional (documented in its docstring).

- One executor per operation. RESPONSE_TYPE = the unwrapped ``result`` model.
  result is array-of-$ref X -> a generated ``<Op>Result(TossBaseModel)`` with a
  single plain field ``root: list[X] = []`` (matches base _coerce {"root": payload}).
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SPEC_FILE = HERE / "openapi.json"
OUT_ROOT = ROOT / "src" / "tooja" / "brokers" / "toss" / "raw"

PYTHON_KEYWORDS = {
    "False", "None", "True", "and", "as", "assert", "async", "await", "break",
    "class", "continue", "def", "del", "elif", "else", "except", "finally", "for",
    "from", "global", "if", "import", "in", "is", "lambda", "nonlocal", "not", "or",
    "pass", "raise", "return", "try", "while", "with", "yield",
}


# ---------- string helpers ----------

def pascal(name: str) -> str:
    return "".join(p[:1].upper() + p[1:] for p in re.split(r"[^A-Za-z0-9]+", name) if p)


def snake(name: str) -> str:
    """camelCase / PascalCase / spaced -> snake_case."""
    s = re.sub(r"[^A-Za-z0-9]+", "_", name)
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s.lower()


def tag_slug(tag: str) -> str:
    return re.sub(r"\s+", "_", tag.strip()).lower()


def safe_field(wire_name: str) -> str:
    """Snake_case python identifier for a wire property name."""
    n = snake(wire_name)
    if not n:
        n = "field"
    if n[0].isdigit():
        n = "_" + n
    if n in PYTHON_KEYWORDS:
        n = n + "_"
    return n


def short_desc(text: str | None) -> str:
    if not text:
        return ""
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned


# ---------- schema type analysis ----------

def ref_name(ref: str) -> str:
    return ref.rsplit("/", 1)[-1]


def is_nullable(schema: dict[str, Any]) -> bool:
    """OpenAPI 3.1 nullable: type:[X,null] OR oneOf/anyOf containing {type:null}."""
    t = schema.get("type")
    if isinstance(t, list) and "null" in t:
        return True
    for key in ("oneOf", "anyOf"):
        variants = schema.get(key)
        if variants and any(v.get("type") == "null" for v in variants):
            return True
    return False


def unwrap_single_ref(schema: dict[str, Any]) -> str | None:
    """allOf:[{$ref X}] (optionally with sibling description) -> 'X'.
    oneOf:[{$ref X}, {type:null}] -> 'X'. Direct $ref -> 'X'. Else None."""
    if "$ref" in schema:
        return ref_name(schema["$ref"])
    for key in ("allOf", "oneOf", "anyOf"):
        variants = schema.get(key)
        if not variants:
            continue
        refs = [v["$ref"] for v in variants if "$ref" in v]
        if len(refs) == 1:
            return ref_name(refs[0])
    return None


def field_type_and_default(
    schema: dict[str, Any], required: bool, all_schemas: dict[str, Any]
) -> tuple[str, str]:
    """Return (python_type, default_suffix) for a property schema."""
    nullable = is_nullable(schema)
    optional = nullable or not required

    # array
    t = schema.get("type")
    types = t if isinstance(t, list) else ([t] if t else [])
    non_null = [x for x in types if x != "null"]

    if "array" in non_null or schema.get("type") == "array":
        items = schema.get("items", {})
        item_ref = unwrap_single_ref(items)
        if item_ref is not None:
            ref_schema = all_schemas.get(item_ref, {})
            if "enum" in ref_schema:  # array of enum -> list[str]
                inner = "str"
            else:
                inner = item_ref
        elif items.get("format") == "decimal":
            inner = "Decimal"
        elif items.get("type") == "integer":
            inner = "int"
        elif items.get("type") == "boolean":
            inner = "bool"
        else:
            inner = "str"
        return f"list[{inner}]", " = []"

    # $ref / allOf-single-ref / oneOf-with-ref
    ref = unwrap_single_ref(schema)
    if ref is not None:
        ref_schema = all_schemas.get(ref, {})
        if "enum" in ref_schema:
            # named enum -> str (forward-compat)
            return ("str" if not optional else "str | None"), (" = None" if optional else "")
        # object ref -> forward-ref string, always optional-friendly
        if optional:
            return f"{ref} | None", " = None"
        return ref, ""

    # decimal string
    fmt = schema.get("format")
    if "string" in non_null and fmt == "decimal":
        return "TDecimal", " = None"  # TDecimal is already Decimal | None

    # integer
    if "integer" in non_null:
        return ("int" if not optional else "int | None"), (" = None" if optional else "")

    # number (float) — none in this spec, but be permissive
    if "number" in non_null:
        return ("float" if not optional else "float | None"), (" = None" if optional else "")

    # boolean
    if "boolean" in non_null:
        return ("bool" if not optional else "bool | None"), (" = None" if optional else "")

    # string (incl. enum, date, date-time, plain) -> str (forward-compat)
    if "string" in non_null or "enum" in schema:
        return ("str" if not optional else "str | None"), (" = None" if optional else "")

    # object without properties / unknown -> permissive Any
    if "object" in non_null:
        return ("dict | None"), " = None"

    # fallback
    return "str | None", " = None"


def uses_decimal_field(schema: dict[str, Any]) -> bool:
    if schema.get("type") == "array":
        return schema.get("items", {}).get("format") == "decimal"
    t = schema.get("type")
    types = t if isinstance(t, list) else [t]
    return "string" in types and schema.get("format") == "decimal"


# ---------- model rendering ----------

def collect_object_properties(schema: dict[str, Any]) -> tuple[dict[str, Any], set[str]]:
    """Resolve an object (incl. oneOf merge) into (properties, required_set)."""
    if "oneOf" in schema and any("properties" in v for v in schema["oneOf"]):
        # Real oneOf with object variants (OrderCreateRequest): merge all props,
        # everything optional.
        merged: dict[str, Any] = {}
        for variant in schema["oneOf"]:
            for pn, pv in (variant.get("properties") or {}).items():
                merged.setdefault(pn, pv)
        return merged, set()  # all optional
    props = dict(schema.get("properties") or {})
    required = set(schema.get("required") or [])
    return props, required


def render_model(name: str, schema: dict[str, Any], all_schemas: dict[str, Any]) -> tuple[str, bool]:
    """Render one model class. Returns (source, uses_decimal)."""
    # Pure enum schema -> still emit a model? No: enums map to str, no class needed.
    # But to keep "one model per schema" referencable, we skip enum-only schemas
    # (they are never used as a model type, only as str). Caller filters these out.
    is_merged_oneof = "oneOf" in schema and any("properties" in v for v in schema["oneOf"])
    props, required = collect_object_properties(schema)

    use_decimal = False
    lines: list[str] = []
    for wire_name, pv in props.items():
        py_name = safe_field(wire_name)
        req = wire_name in required and not is_merged_oneof
        ty, default = field_type_and_default(pv, req, all_schemas)
        if ty == "TDecimal" or "Decimal" in ty:
            use_decimal = True
        # Build the Field(...) — always alias; default if any.
        field_args = [f'alias="{wire_name}"']
        if default:
            default_val = default[len(" = "):]
            field_args.insert(0, f"default={default_val}")
        field_call = "Field(" + ", ".join(field_args) + ")"
        comment = short_desc(pv.get("description"))
        line = f"    {py_name}: {ty} = {field_call}"
        if comment:
            line += f"  # {comment[:120]}"
        lines.append(line)

    body = "\n".join(lines) or "    pass"

    if is_merged_oneof:
        doc = (
            "Merged ``oneOf`` request model. The OpenAPI spec defines this as a "
            "oneOf of variants;\n    all variants' properties are merged here and "
            "made optional so the adapter can\n    populate whichever variant "
            "applies."
        )
    else:
        doc = short_desc(schema.get("description")) or f"{name} schema."
        doc = doc[:200]

    src = f'class {name}(TossBaseModel):\n    """{doc}"""\n\n{body}\n'
    return src, use_decimal


def render_models_module(spec: dict[str, Any]) -> str:
    schemas: dict[str, Any] = spec["components"]["schemas"]

    # Enum-only schemas map to str; they are not emitted as classes.
    enum_only = {n for n, s in schemas.items() if "enum" in s and "properties" not in s}

    any_decimal = False
    model_srcs: list[str] = []
    model_names: list[str] = []
    for name, schema in schemas.items():
        if name in enum_only:
            continue
        src, dec = render_model(name, schema, schemas)
        any_decimal = any_decimal or dec
        model_srcs.append(src)
        model_names.append(name)

    header_imports = ["from pydantic import Field"]
    base_import = "from tooja.brokers.toss.raw.base import TossBaseModel"
    if any_decimal:
        base_import = "from tooja.brokers.toss.raw.base import TDecimal, TossBaseModel"

    parts: list[str] = [
        '"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""',
        "",
        "from __future__ import annotations",
        "",
    ]
    if any_decimal:
        parts += ["from decimal import Decimal", ""]
    parts += [
        header_imports[0],
        "",
        base_import,
        "",
        "",
    ]
    parts.append("\n\n".join(model_srcs))
    # Resolve cross-model forward references.
    parts.append("")
    parts.append("")
    for n in model_names:
        parts.append(f"{n}.model_rebuild()")
    parts.append("")
    return "\n".join(parts)


# ---------- executor rendering ----------

def resolve_param(p: dict[str, Any], components_params: dict[str, Any]) -> dict[str, Any]:
    if "$ref" in p:
        return components_params[ref_name(p["$ref"])]
    return p


def result_info(op: dict[str, Any]) -> tuple[str, str | None]:
    """Return (kind, model_name) for the 200 result.
    kind in {'ref', 'array', 'bare'}; 'bare' = response schema is a direct $ref
    (the OAuth token endpoint, not enveloped)."""
    resp = op.get("responses", {}).get("200", {})
    sch = resp.get("content", {}).get("application/json", {}).get("schema", {})
    if "$ref" in sch:
        return "bare", ref_name(sch["$ref"])
    if "allOf" in sch:
        for part in sch["allOf"]:
            props = part.get("properties")
            if props and "result" in props:
                r = props["result"]
                if "$ref" in r:
                    return "ref", ref_name(r["$ref"])
                if r.get("type") == "array":
                    item = r.get("items", {})
                    if "$ref" in item:
                        return "array", ref_name(item["$ref"])
    raise ValueError("cannot resolve result schema")


def render_executor(
    path: str,
    method: str,
    op: dict[str, Any],
    components_params: dict[str, Any],
) -> tuple[str, str]:
    """Return (filename, source)."""
    oid = op["operationId"]
    op_pascal = pascal(oid)
    executor_cls = f"{op_pascal}Executor"
    filename = snake(oid) + ".py"

    # classify parameters
    path_params: list[str] = []
    query_params: list[str] = []
    header_params: list[str] = []
    for p in op.get("parameters", []):
        rp = resolve_param(p, components_params)
        loc = rp.get("in")
        wire = rp.get("name")
        if loc == "path":
            path_params.append(wire)
        elif loc == "query":
            query_params.append(wire)
        elif loc == "header":
            header_params.append(wire)

    # body content — derived from requestBody.content keys, not a hardcoded whitelist
    rb = op.get("requestBody")
    rb_content = rb.get("content", {}) if rb else {}
    if "application/x-www-form-urlencoded" in rb_content:
        body_content = "form"
    elif "application/json" in rb_content:
        body_content = "json"
    else:
        body_content = "none"

    enveloped = not (method.upper() == "POST" and path == "/oauth2/token")

    kind, model = result_info(op)

    imports_from_models: list[str] = []
    extra_class_src = ""
    if kind == "array":
        result_cls = f"{op_pascal}Result"
        imports_from_models.append(model)
        extra_class_src = (
            f"class {result_cls}(TossBaseModel):\n"
            f'    """Wrapper for the array ``result`` payload of {oid}."""\n\n'
            f"    root: list[{model}] = []\n\n\n"
        )
        response_type = result_cls
    else:
        imports_from_models.append(model)
        response_type = model

    base_import = "from tooja.brokers.toss.raw.base import TossApiExecutor"
    if kind == "array":
        base_import = "from tooja.brokers.toss.raw.base import TossApiExecutor, TossBaseModel"
    models_import = (
        "from tooja.brokers.toss.raw.models import "
        + ", ".join(sorted(set(imports_from_models)))
    )

    summary = short_desc(op.get("summary"))[:160]

    def tup(items: list[str]) -> str:
        if not items:
            return "()"
        if len(items) == 1:
            return f'("{items[0]}",)'
        return "(" + ", ".join(f'"{i}"' for i in items) + ")"

    parts: list[str] = [
        '"""Auto-generated from specs/toss/openapi.json — do not edit by hand."""',
        "",
        "from __future__ import annotations",
        "",
        base_import,
        models_import,
        "",
        "",
    ]
    if extra_class_src:
        parts.append(extra_class_src.rstrip("\n"))
        parts.append("")
        parts.append("")
    parts.append(f"class {executor_cls}(TossApiExecutor[{response_type}]):")
    doc = summary or f"{oid}."
    parts.append(f'    """{doc}"""')
    parts.append("")
    parts.append(f'    PATH = "{path}"')
    parts.append(f'    METHOD = "{method.upper()}"')
    parts.append(f"    RESPONSE_TYPE = {response_type}")
    if path_params:
        parts.append(f"    PATH_PARAMS = {tup(path_params)}")
    if query_params:
        parts.append(f"    QUERY_PARAMS = {tup(query_params)}")
    if header_params:
        parts.append(f"    HEADER_PARAMS = {tup(header_params)}")
    parts.append(f'    BODY_CONTENT = "{body_content}"')
    if not enveloped:
        parts.append("    ENVELOPED = False")
    parts.append("")
    return filename, "\n".join(parts)


# ---------- driver ----------

def generate(dry_run: bool = False) -> None:
    spec = json.loads(SPEC_FILE.read_text())
    components_params = spec["components"].get("parameters", {})

    # Wipe + recreate tag dirs (keep base.py, __init__.py, models.py at raw root).
    if not dry_run:
        OUT_ROOT.mkdir(parents=True, exist_ok=True)
        for entry in OUT_ROOT.iterdir():
            if entry.is_dir() and entry.name != "__pycache__":
                shutil.rmtree(entry)

    # models.py
    models_src = render_models_module(spec)
    n_models = models_src.count("(TossBaseModel):")
    if not dry_run:
        (OUT_ROOT / "models.py").write_text(models_src)

    # executors per tag
    op_count = 0
    tag_dirs: dict[str, list[tuple[str, str]]] = {}
    for path, item in spec["paths"].items():
        for method, op in item.items():
            if method not in ("get", "post", "put", "delete", "patch"):
                continue
            tags = op.get("tags") or ["default"]
            slug = tag_slug(tags[0])
            filename, src = render_executor(path, method, op, components_params)
            tag_dirs.setdefault(slug, []).append((filename, src))
            op_count += 1

    for slug, files in sorted(tag_dirs.items()):
        out_dir = OUT_ROOT / slug
        if not dry_run:
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "__init__.py").write_text("")
            for filename, src in sorted(files):
                (out_dir / filename).write_text(src)

    print(f"Generated models.py ({n_models} models)")
    print(f"Generated {op_count} executors across {len(tag_dirs)} tag dirs:")
    for slug in sorted(tag_dirs):
        print(f"  + {slug}: {len(tag_dirs[slug])} op(s)")
    if dry_run:
        print("(dry run — no files written)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    generate(dry_run=args.dry_run)
