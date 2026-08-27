#!/usr/bin/env python3
"""Build the documentation index: what every page says, and what it depends on.

Without this, a question like "the SDK renamed `ConvaiGazeController` — which pages have to
change?" has no answer except someone's memory. That is the reason a release currently
depends on a person remembering which pages mention lip sync, and it is the single thing
standing between this tooling and an automatic update.

The index records, per page:

    title, description, last_reviewed      what the page claims about itself
    headings                               its outline
    symbols                                every code identifier it names
    links                                  every relative link it makes
    images                                 every image it shows
    vars                                   every GitBook variable it reads

and inverts the interesting ones, so `symbols["ConvaiGazeController"]` lists every page and
line that names it. `diff_surface.py` intersects that inversion with what actually changed
between two SDK versions, which is how a release turns into a work list instead of a guess.

Two deliberate limits. It indexes what a page *says*, never whether that is true — accuracy
is the verifier's job. And a symbol is recognised by shape, not by looking it up in a source
tree, so the index can be built without the SDK checked out.

Usage:
    python build_index.py <docs-repo-root> [-o index.json] [--quiet]
"""

import argparse
import io
import json
import os
import re
import sys

# A backticked token counts as a code symbol when its shape says "identifier" rather than
# "ordinary word in code font". Being generous here would fill the index with words like
# `staging`, and every one of those becomes a false hit during a release impact pass.
# Written without a repeated group: `(?:[A-Z][A-Za-z0-9]*)+` accepts exactly the same
# tokens but can split a run of capitals in many ways, which CodeQL flags as exponential
# backtracking (py/redos) on input like `AAAA...`.
CAMEL_CASE = re.compile(r"^[A-Za-z][a-z0-9]*[A-Z][A-Za-z0-9]*$")
CALL = re.compile(r"^[A-Za-z_][\w.]*\(\)$")
QUALIFIED = re.compile(r"^[A-Za-z_]\w*(?:::|\.)[\w.:]+$")
FILE_PATH = re.compile(r"^[\w./\\-]+\.(?:cs|cpp|h|hpp|py|js|ts|json|yaml|yml|uplugin|asmdef|md|unity|asset|prefab)$")

INLINE_CODE = re.compile(r"`([^`\n]+)`")
# GitBook wraps a target containing spaces in angle brackets - `![](<../assets/image (1).png>)`.
# Stopping at the first space instead reported most of the asset library as missing, so both
# forms are matched and the brackets stripped by `_clean_target`.
MD_LINK = re.compile(r"\[[^\]]*\]\(\s*(<[^>]*>|[^)\s]+)")
MD_IMAGE = re.compile(r"!\[[^\]]*\]\(\s*(<[^>]*>|[^)\s]+)")
HTML_IMG_SRC = re.compile(r'<img[^>]*\bsrc\s*=\s*"([^"]+)"', re.IGNORECASE)
GITBOOK_VAR = re.compile(r"space\.vars\.([A-Za-z0-9_]+)")
HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")

SKIP_DIRS = {".git", ".github", "node_modules", "__pycache__", ".gitbook", ".convai-docs"}

# Repository housekeeping that lives at the root and is not a documentation page. Indexing
# these reports their template placeholders as broken links, which trains people to ignore
# the checker.
NON_PAGE_FILES = {"CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "LICENSE.md",
                  "AGENTS.md", "CLAUDE.md"}


def read(path):
    with io.open(path, encoding="utf-8-sig") as f:
        return f.read()


def split_frontmatter(text):
    """Return (dict, body_lines_offset). Mirrors check_page.py's simple parser so the two
    tools agree on what a page's frontmatter says."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, 0
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, 0
    fm = {}
    i = 1
    while i < end:
        m = re.match(r"([A-Za-z0-9_]+):\s*(.*)$", lines[i])
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val and val[0] in "|>":
            # YAML block scalar. Without this branch the value reads as the literal ">-"
            # and every page using GitBook's folded form collides with every other one,
            # which turned duplicate-desc into 310 pages of noise on one repository.
            block = []
            i += 1
            while i < end and (lines[i].strip() == "" or lines[i][:1] in (" ", "\t")):
                block.append(lines[i].strip())
                i += 1
            joined = " ".join(x for x in block if x) if val[0] == ">" else "\n".join(block)
            fm[key] = joined.strip()
            continue
        fm[key] = val.strip().strip('"').strip("'")
        i += 1
    return fm, end + 1


def _clean_target(raw):
    """Normalise a link or image target as written in Markdown."""
    raw = raw.strip()
    if raw.startswith("<") and raw.endswith(">"):
        raw = raw[1:-1]
    return raw.strip()


def is_symbol(token):
    token = token.strip()
    if not token or len(token) > 120 or " " in token.strip("()"):
        return False
    return bool(CAMEL_CASE.match(token) or CALL.match(token)
                or QUALIFIED.match(token) or FILE_PATH.match(token))


def index_page(abs_path, rel_path):
    text = read(abs_path)
    fm, body_start = split_frontmatter(text)

    page = {
        "title": fm.get("title", ""),
        "description": fm.get("description", ""),
        "last_reviewed": fm.get("last_reviewed", ""),
        "headings": [],
        "symbols": {},   # symbol -> first line it appears on
        "links": [],
        "images": [],
        "vars": [],
    }

    in_code = False
    for offset, raw in enumerate(text.split("\n")[body_start:]):
        lineno = body_start + offset + 1
        if FENCE.match(raw):
            in_code = not in_code
            continue
        if in_code:
            # A fenced example is not evidence that a page documents a symbol; it is
            # usually illustrative. Links and images inside a fence are not real either.
            continue

        h = HEADING.match(raw)
        if h:
            page["headings"].append({"level": len(h.group(1)), "text": h.group(2), "line": lineno})

        for m in INLINE_CODE.finditer(raw):
            token = m.group(1).strip()
            if is_symbol(token) and token not in page["symbols"]:
                page["symbols"][token] = lineno

        for m in MD_IMAGE.finditer(raw):
            page["images"].append({"src": _clean_target(m.group(1)), "line": lineno})
        for m in HTML_IMG_SRC.finditer(raw):
            page["images"].append({"src": _clean_target(m.group(1)), "line": lineno})

        images_on_line = set(i["src"] for i in page["images"] if i["line"] == lineno)
        for m in MD_LINK.finditer(raw):
            target = _clean_target(m.group(1))
            if target in images_on_line:
                continue
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            page["links"].append({"target": target, "line": lineno})

        for m in GITBOOK_VAR.finditer(raw):
            if m.group(1) not in page["vars"]:
                page["vars"].append(m.group(1))

    return page


def parse_summary(root):
    """Return {normalised target: label} for every entry in SUMMARY.md."""
    path = os.path.join(root, "SUMMARY.md")
    if not os.path.exists(path):
        return None
    entries = {}
    for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", read(path)):
        target = m.group(2).split("#")[0].strip()
        entries[target.replace("\\", "/").lstrip("./")] = m.group(1).strip()
    return entries


def build(root, quiet=False):
    root = os.path.abspath(root)
    pages = {}
    unreadable = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in sorted(dirnames) if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in sorted(filenames):
            if not fn.endswith(".md") or fn == "SUMMARY.md":
                continue
            if dirpath == root and fn in NON_PAGE_FILES:
                continue
            abs_path = os.path.join(dirpath, fn)
            rel = os.path.relpath(abs_path, root).replace("\\", "/")
            try:
                pages[rel] = index_page(abs_path, rel)
            except (OSError, UnicodeDecodeError) as e:
                unreadable.append({"page": rel, "error": str(e)})

    symbols = {}
    variables = {}
    titles = {}
    for rel, page in pages.items():
        for sym, line in page["symbols"].items():
            symbols.setdefault(sym, []).append("%s:%d" % (rel, line))
        for var in page["vars"]:
            variables.setdefault(var, []).append(rel)
        if page["title"]:
            titles.setdefault(page["title"], []).append(rel)

    index = {
        "root": root,
        "page_count": len(pages),
        "pages": pages,
        "symbols": dict(sorted(symbols.items())),
        "vars": dict(sorted(variables.items())),
        "titles": dict(sorted(titles.items())),
        "summary": parse_summary(root),
        "unreadable": unreadable,
    }

    if not quiet:
        print("indexed %d page(s)" % len(pages))
        print("  %d distinct code symbol(s)" % len(symbols))
        print("  %d GitBook variable(s) in use" % len(variables))
        if index["summary"] is None:
            print("  no SUMMARY.md at the root; navigation checks will be skipped")
        else:
            print("  %d SUMMARY.md entr(y/ies)" % len(index["summary"]))
        for u in unreadable:
            print("  UNREADABLE %s: %s" % (u["page"], u["error"]))

    return index


def main():
    ap = argparse.ArgumentParser(description="Index a Convai documentation repository.")
    ap.add_argument("root", help="Path to the documentation repository root")
    ap.add_argument("-o", "--out", help="Write the index here (default: <root>/.convai-docs/index.json)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(args.root):
        print("not a directory: %s" % args.root, file=sys.stderr)
        return 2

    index = build(args.root, quiet=args.quiet)

    out = args.out or os.path.join(args.root, ".convai-docs", "index.json")
    out_dir = os.path.dirname(os.path.abspath(out))
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
        f.write("\n")
    if not args.quiet:
        print("wrote %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
