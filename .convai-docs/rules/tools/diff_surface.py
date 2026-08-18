#!/usr/bin/env python3
"""Turn a release into a work list.

Everything before this exists to make one question answerable: the SDK went from 4.4.0 to
4.5.0 — what has to change in the documentation? Until now that was answered from memory,
which is why an update meant someone recalling which pages mention lip sync, and why pages
naming a renamed component survived two releases.

This intersects what changed in the source with what the pages actually say, and sorts the
result by what it costs to be wrong:

    broken     a page names a symbol the new version removed. The page is wrong right now
    historical a migration guide or release note names it, which is what those pages are for
    renamed    a removal that looks like a rename, with the likely new name
    missing    new public surface no page mentions. A shipped feature nobody documented
    vars       the version moved, so every page pinned to it needs its `last_reviewed` re-set
    retired    a symbol disappeared and no page named it. Nothing to do; recorded for the log

The `historical` split matters more than it looks. The first run of this against a real
release found fifteen removed symbols still named in the documentation, and thirteen of them
were on migration guides and release notes, where naming the old component is the entire
purpose of the page. Reporting those as errors would have taught everyone to scroll past the
report.

`broken` is the only category that is unambiguously an error. `missing` is a judgement call —
some new surface is internal and should stay undocumented — so it is offered as a question,
not an instruction. Nothing here writes a page: it produces the list a human approves before
`/build-docs` touches anything.

Usage:
    python diff_surface.py --before old.json --after new.json [--index index.json] [--json]
"""

import argparse
import difflib
import fnmatch
import io
import json
import sys

# Which extracted sets are worth reporting on. `types` is every internal helper in the
# package; diffing it would bury the ten findings that matter under four hundred that do not.
REPORTED_SETS = ["modules", "inspector_components", "components", "configuration",
                 "menu_paths", "samples", "dependencies", "assemblies"]

# How close two names have to be before a removal plus an addition reads as a rename rather
# than an unrelated pair. Tuned to catch ConvaiLipSync -> ConvaiLipSyncComponent without
# claiming ConvaiGaze -> ConvaiEmotion.
RENAME_SIMILARITY = 0.72

# Pages whose job is to talk about what a release changed. A retired name on one of these is
# correct, not stale. Overridable per subject through the contract's `historical_pages`.
DEFAULT_HISTORICAL_PAGES = [
    "**/release-notes.md",
    "**/changelog.md",
    "**/migrate-*.md",
    "**/migration-*.md",
    "**/migration-guide/**",
    "**/upgrade-*.md",
]


def is_historical(page_path, patterns):
    path = page_path.split(":")[0].replace("\\", "/")
    return any(fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch("/" + path, pattern)
               for pattern in patterns)


def read_json(path):
    with io.open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def guess_rename(removed, added):
    """Pair each removed name with the most similar added name, if any is close enough."""
    pairs = {}
    for name in removed:
        best, score = None, 0.0
        for candidate in added:
            ratio = difflib.SequenceMatcher(None, name, candidate).ratio()
            if ratio > score:
                best, score = candidate, ratio
        if best and score >= RENAME_SIMILARITY:
            pairs[name] = {"to": best, "confidence": round(score, 2)}
    return pairs


def diff_sets(before, after):
    out = {}
    for set_name in REPORTED_SETS:
        old = set(before.get("sets", {}).get(set_name, []))
        new = set(after.get("sets", {}).get(set_name, []))
        if not old and not new:
            continue
        out[set_name] = {"added": sorted(new - old), "removed": sorted(old - new)}
    return out


def pages_naming(index, symbol):
    return index.get("symbols", {}).get(symbol, []) if index else []


def build_report(before, after, index=None, historical_patterns=None):
    patterns = historical_patterns or DEFAULT_HISTORICAL_PAGES
    changes = diff_sets(before, after)

    all_removed, all_added = set(), set()
    for set_name, delta in changes.items():
        if set_name in ("menu_paths", "dependencies"):
            continue  # not symbols; handled separately
        all_removed.update(delta["removed"])
        all_added.update(delta["added"])

    renames = guess_rename(sorted(all_removed), sorted(all_added))

    broken, historical, retired = [], [], []
    for symbol in sorted(all_removed):
        where = pages_naming(index, symbol)
        live = [p for p in where if not is_historical(p, patterns)]
        past = [p for p in where if is_historical(p, patterns)]
        entry = {"symbol": symbol, "pages": live, "historical_pages": past}
        if symbol in renames:
            entry["likely_new_name"] = renames[symbol]["to"]
            entry["confidence"] = renames[symbol]["confidence"]
        if live:
            broken.append(entry)
        elif past:
            historical.append(entry)
        else:
            retired.append(entry)

    missing = []
    for set_name in ("modules", "inspector_components", "samples"):
        for symbol in changes.get(set_name, {}).get("added", []):
            if not pages_naming(index, symbol):
                missing.append({"symbol": symbol, "set": set_name})

    menu_delta = changes.get("menu_paths", {"added": [], "removed": []})
    dependency_delta = changes.get("dependencies", {"added": [], "removed": []})

    version_before = before.get("version")
    version_after = after.get("version")
    var_pages = []
    if index and version_before != version_after:
        seen = set()
        for var, pages in index.get("vars", {}).items():
            if "version" not in var:
                continue
            for page in pages:
                if page not in seen:
                    seen.add(page)
                    var_pages.append(page)

    stale_reviews = []
    if index and version_after:
        for page, data in sorted(index.get("pages", {}).items()):
            reviewed = (data.get("last_reviewed") or "").strip()
            if reviewed and reviewed != version_after:
                stale_reviews.append({"page": page, "last_reviewed": reviewed})

    return {
        "subject": after.get("subject"),
        "version_before": version_before,
        "version_after": version_after,
        "source_before": before.get("generated_against"),
        "source_after": after.get("generated_against"),
        "broken": broken,
        "historical": historical,
        "renamed": renames,
        "missing": missing,
        "retired": retired,
        "menu_paths": menu_delta,
        "dependencies": dependency_delta,
        "version_pinned_pages": sorted(var_pages),
        "stale_reviews": stale_reviews,
        "changes": changes,
        "indexed": bool(index),
    }


def print_report(r):
    print("%s  %s -> %s   (source %s -> %s)"
          % (r["subject"], r["version_before"], r["version_after"],
             r["source_before"], r["source_after"]))
    if not r["indexed"]:
        print("\nNo documentation index was given, so nothing below knows which pages are")
        print("affected. Run build_index.py against the documentation repo and pass --index.")

    print("\nBROKEN  (%d)  a published page names a symbol this release removed" % len(r["broken"]))
    for item in r["broken"]:
        rename = ""
        if item.get("likely_new_name"):
            rename = "  -> likely now `%s` (%.0f%% similar)" % (
                item["likely_new_name"], item["confidence"] * 100)
        print("  `%s`%s" % (item["symbol"], rename))
        for page in item["pages"][:8]:
            print("      %s" % page)
        if len(item["pages"]) > 8:
            print("      ... and %d more" % (len(item["pages"]) - 8))
    if not r["broken"]:
        print("  none")

    print("\nHISTORICAL  (%d)  named only where naming it is the point of the page"
          % len(r["historical"]))
    for item in r["historical"]:
        print("  `%s`  on %d migration or release page(s)"
              % (item["symbol"], len(item["historical_pages"])))
    if not r["historical"]:
        print("  none")

    print("\nMISSING  (%d)  new surface no page mentions" % len(r["missing"]))
    for item in r["missing"]:
        print("  %-22s %s" % (item["set"], item["symbol"]))
    if not r["missing"]:
        print("  none")

    if r["menu_paths"]["added"] or r["menu_paths"]["removed"]:
        print("\nMENU PATHS  a click path a page tells the reader to follow may have moved")
        for path in r["menu_paths"]["removed"]:
            print("  removed  %s" % path)
        for path in r["menu_paths"]["added"]:
            print("  added    %s" % path)

    if r["dependencies"]["added"] or r["dependencies"]["removed"]:
        print("\nDEPENDENCIES  the compatibility page states this list")
        for name in r["dependencies"]["removed"]:
            print("  removed  %s" % name)
        for name in r["dependencies"]["added"]:
            print("  added    %s" % name)

    if r["version_before"] != r["version_after"]:
        print("\nVERSION  %s -> %s" % (r["version_before"], r["version_after"]))
        print("  %d page(s) read a version variable; confirm .gitbook/vars.yaml is bumped"
              % len(r["version_pinned_pages"]))
        print("  %d page(s) carry a last_reviewed that is not %s"
              % (len(r["stale_reviews"]), r["version_after"]))

    if r["retired"]:
        print("\nRETIRED  (%d)  removed from source, named by no page. Nothing to do."
              % len(r["retired"]))

    total = len(r["broken"]) + len(r["missing"])
    print("\n%d finding(s) needing work: %d broken, %d undocumented."
          % (total, len(r["broken"]), len(r["missing"])))
    print("%d retired name(s) left alone on migration and release pages, where they belong."
          % len(r["historical"]))


def main():
    ap = argparse.ArgumentParser(description="Diff two extracted surfaces into a work list.")
    ap.add_argument("--before", required=True, help="The surface.json from the older version")
    ap.add_argument("--after", required=True, help="The surface.json from the new version")
    ap.add_argument("--index", help="index.json from build_index.py, to resolve affected pages")
    ap.add_argument("--contract", help="Pack contract, read for its historical_pages patterns")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    before = read_json(args.before)
    after = read_json(args.after)
    index = read_json(args.index) if args.index else None

    patterns = None
    if args.contract:
        patterns = read_json(args.contract).get("historical_pages")
    report = build_report(before, after, index, historical_patterns=patterns)

    if args.json:
        json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print_report(report)

    # A removed symbol that pages still name is the one unambiguous error here.
    return 1 if report["broken"] else 0


if __name__ == "__main__":
    sys.exit(main())
