#!/usr/bin/env python3
"""Check that the pages the packs hold up as the quality bar still meet it.

Every pack points writers at gold-standard example pages and tells them to match that bar.
Those pages live in the documentation repository, not in this plugin, and nothing has ever
verified them. So the benchmark can quietly rot in three ways, each of which lowers the bar
for every page written afterwards:

    declared-borrow  the pack knows it has no exemplar of its own and says so, with a date
    missing   the page was renamed or deleted, and the pack sends writers to a dead path
    failing   the exemplar itself no longer passes the linter
    thin      the page shrank to the point where it is no longer worth imitating
    borrowed  the pack points at another subject's pages, so its writers are told to match a
              benchmark written for a different product

`thin` is the reason this is not just a link check. A gold standard is not a page that
exists; it is a page worth copying. When one degrades, nothing complains, and every writer
after that copies the degraded version.

`borrowed` is the one that was actually true when this was written: five of six packs pointed
their gold standards at Unity SDK pages, because they were scaffolded from the Unity pack and
never given exemplars of their own. An Unreal writer following that pack is told to match a
page about a different engine.

Usage:
    python check_gold_standards.py --packs <packs-dir> --docs <docs-repo-root> [--json]
"""

import argparse
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_page  # noqa: E402

# A path inside a table cell or a bullet in the pack's gold-standard section. The slash is
# required: a pack's prose says things like "default to `installation.md`", and treating a
# bare filename as a path reported exemplars that were never claimed to be paths.
PAGE_PATH = re.compile(r"`([\w./-]+/[\w.-]+\.md)`")
SECTION_HEADING = re.compile(r"^#{2,3}\s*Gold-standard example pages", re.IGNORECASE)

# Below this a page is too slight to be worth holding up as an example. Not a quality
# judgement in itself - a short page can be excellent - but an exemplar is chosen to be
# copied, and there is nothing to copy from a page of four hundred words.
#
# Word count only. Counting `##` sections looked like a better signal until it reported the
# canonical install page as having one: it carries its structure in a stepper and tabs, which
# is exactly what makes it the exemplar.
MIN_WORDS = 250


def read(path):
    with io.open(path, encoding="utf-8-sig") as f:
        return f.read()


def gold_standard_paths(pack_text):
    """Page paths named in the pack's gold-standard section."""
    lines = pack_text.split("\n")
    start = None
    for i, line in enumerate(lines):
        if SECTION_HEADING.match(line.strip()):
            start = i
            break
    if start is None:
        return []
    out = []
    for line in lines[start + 1:]:
        stripped = line.strip()
        if stripped.startswith("#") and not SECTION_HEADING.match(stripped):
            break
        out.extend(PAGE_PATH.findall(line))
    # A pack legitimately names the same exemplar for two modes.
    seen, unique = set(), []
    for path in out:
        if path not in seen:
            seen.add(path)
            unique.append(path)
    return unique


def pack_section(packs_dir, pack):
    """Where this pack's pages live, from its contract."""
    path = os.path.join(packs_dir, "contracts", "%s.json" % pack)
    if not os.path.exists(path):
        return None
    try:
        with io.open(path, encoding="utf-8-sig") as f:
            return json.load(f).get("section")
    except (OSError, ValueError):
        return None


def owns(pack, page_path, section=None):
    """Does this exemplar belong to the subject the pack is about?

    The contract says where a subject's pages live, because guessing from the pack name is
    right most of the time and wrong for `core-service`, whose pages are under `api-reference`.
    A guess that is right most of the time is the worst kind in a checker: the cases it gets
    wrong look exactly like real findings. The name check remains as a fallback for a pack
    with no contract."""
    if section:
        return page_path.startswith(section)
    return pack.replace("-", "") in page_path.replace("-", "").lower()


def declared_borrow(packs_dir, pack):
    """What the pack's contract says about borrowing, if anything.

    A borrow that has been thought about, written on the page and dated is a state. A borrow
    nobody has noticed is a defect. The difference is worth keeping, because reporting the
    first one every run is how people learn to skip the second."""
    path = os.path.join(packs_dir, "contracts", "%s.json" % pack)
    if not os.path.exists(path):
        return None
    try:
        with io.open(path, encoding="utf-8-sig") as f:
            declared = json.load(f).get("gold_standards")
    except (OSError, ValueError):
        return None
    return declared if declared and declared.get("status") == "borrowed" else None


def check(packs_dir, docs_root):
    findings = []
    seen_pages = set()
    checked = 0

    for fn in sorted(os.listdir(packs_dir)):
        if not fn.endswith(".md") or fn.startswith("_"):
            continue
        pack = fn[:-3]
        pack_text = read(os.path.join(packs_dir, fn))
        borrow = declared_borrow(packs_dir, pack)
        section = pack_section(packs_dir, pack)
        if borrow:
            findings.append({
                "level": "INFO", "kind": "declared-borrow", "pack": pack, "page": "-",
                "detail": "borrows its shape from `%s`; %s pages passed the structure gate when "
                          "this was measured on %s"
                          % (borrow.get("borrowed_from", "another subject"),
                             borrow.get("clean_pages", "too few"), borrow.get("measured_on", "?")),
                "fix": borrow.get("reason", "")})
        for rel in gold_standard_paths(pack_text):
            checked += 1

            if not owns(pack, rel, section) and not borrow:
                findings.append({
                    "level": "WARN", "kind": "borrowed", "pack": pack, "page": rel,
                    "detail": "the %s pack holds up a page from another subject as its benchmark"
                              % pack,
                    "fix": "Choose an exemplar from this subject's own pages. A writer told to "
                           "match a page about a different product copies its structure and its "
                           "assumptions along with its quality."})

            # The same exemplar is named by several packs; check the page itself once.
            if rel in seen_pages:
                continue
            seen_pages.add(rel)
            full = os.path.join(docs_root, rel.replace("/", os.sep))
            if not os.path.exists(full):
                findings.append({
                    "level": "ERROR", "kind": "missing", "pack": pack, "page": rel,
                    "detail": "the pack points writers at a page that does not exist",
                    "fix": "Correct the path in the pack, or choose a new exemplar. Until then "
                           "every writer told to match this benchmark has nothing to open."})
                continue

            errors = [f for f in check_page.check_page(full) if f.level == "ERROR"]
            if errors:
                findings.append({
                    "level": "ERROR", "kind": "failing", "pack": pack, "page": rel,
                    "detail": "the exemplar fails the linter: %s"
                              % "; ".join("%s %s" % (f.rule or "-", f.msg) for f in errors[:3]),
                    "fix": "Fix the page. A benchmark that breaks the rules teaches everyone "
                           "who copies it to break them too."})

            words = len(read(full).split())
            if words < MIN_WORDS:
                findings.append({
                    "level": "WARN", "kind": "thin", "pack": pack, "page": rel,
                    "detail": "%d words - thin for an exemplar" % words,
                    "fix": "Either the page was cut down, or it was never the right choice. "
                           "Pick an exemplar with enough in it to be worth copying."})

    return findings, checked


def main():
    ap = argparse.ArgumentParser(description="Verify the packs' gold-standard example pages.")
    ap.add_argument("--packs", required=True, help="Directory holding the pack markdown files")
    ap.add_argument("--docs", required=True, help="Documentation repository root")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="Also fail on WARN findings")
    args = ap.parse_args()

    findings, checked = check(args.packs, args.docs)
    errors = [f for f in findings if f["level"] == "ERROR"]
    warns = [f for f in findings if f["level"] == "WARN"]
    notes = [f for f in findings if f["level"] == "INFO"]

    if args.json:
        json.dump({"checked": checked, "errors": len(errors), "warnings": len(warns),
                   "findings": findings}, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print("%d gold-standard reference(s) across the packs" % checked)
        for f in findings:
            print("\n%-5s %-8s %s" % (f["level"], f["kind"], f["page"]))
            print("      %s" % f["detail"])
            print("      -> %s" % f["fix"])
        if not findings:
            print("Every exemplar exists, passes the linter, and is substantial enough to copy.")
        print("\n%d error(s), %d warning(s), %d declared borrow(s)."
              % (len(errors), len(warns), len(notes)))

    if errors:
        return 1
    return 1 if (args.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
