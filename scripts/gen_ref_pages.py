"""Generate the home page, API reference pages, and navigation at build time.

The mkdocs-gen-files plugin runs this script during `mkdocs build`.
- `index.md`             : reuses README.md as the home page
- `reference/**.md`      : mkdocstrings stubs for every public module under src/tooja
- `reference/SUMMARY.md` : the literate-nav navigation file

No page is authored by hand; the reference tracks the source automatically.
"""

from pathlib import Path

import mkdocs_gen_files

root = Path(__file__).parent.parent
src = root / "src"

# --- Home page: reuse README verbatim ------------------------------------
readme = (root / "README.md").read_text(encoding="utf-8")
with mkdocs_gen_files.open("index.md", "w") as fd:
    fd.write(readme)
mkdocs_gen_files.set_edit_path("index.md", "README.md")

# --- API reference: walk src/tooja ---------------------------------------
nav = mkdocs_gen_files.Nav()

for path in sorted(src.rglob("*.py")):
    module_path = path.relative_to(src).with_suffix("")
    doc_path = path.relative_to(src).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    if not parts:
        continue

    # Skip internal-only modules AND packages: any path segment starting with a
    # single underscore (e.g. _call.py, or a module inside _internal/). Dunder
    # modules (__init__, __main__) are already handled above.
    if any(part.startswith("_") for part in parts):
        continue

    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root))

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
