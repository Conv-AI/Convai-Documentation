#!/usr/bin/env python3
"""What the SDK ships that the documentation never mentions.

Documentation gaps are normally discovered by a reader hitting one, which is the most
expensive way to find out. Both halves of the answer already exist: `surfaces/<pack>.json`
knows what the SDK exposes, and `index.json` knows what every page says. Intersecting them
turns "what have we not documented" from a discussion into a query.

Two things this deliberately does not claim. Not every public type should be documented —
plenty are internal in everything but the access modifier — so an undocumented symbol is a
question for the owner, not a defect. And a symbol named on a page is not proof that the page
explains it; coverage is a floor, not a measure of quality.

Usage:
    python check_coverage.py --surface surfaces/unity.json --index .convai-docs/index.json
                             [--contract contracts/unity.json] [--section PREFIX] [--json]
"""

import argparse
import io
import json
import sys

# Sets worth asking about. Internal helper types are excluded by asking the contract which
# sets it considers documented surface, and falling back to the user-facing ones.
DEFAULT_SETS = ["modules", "inspector_components", "samples"]

# Sets whose members a page names as ordinary words rather than as identifiers in code font.
PROSE_SETS = {"modules", "samples"}

# A dotted name is a namespace or a tool id - `Convai.ConfigureGaze` is an MCP tool, not a
# C# type - so it will never be in a surface of type names. Reporting 254 of those buried the
# handful of real ones.
DEFAULT_IGNORE_PREFIXES = ()


def read_json(path):
    with io.open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def build_report(surface, index, sets=None, section=None, ignore_prefixes=()):
    sets = sets or DEFAULT_SETS
    symbols = index.get("symbols", {})
    pages = index.get("pages", {})

    def pages_for(symbol):
        hits = symbols.get(symbol, [])
        if section:
            hits = [h for h in hits if h.startswith(section)]
        return hits

    def mentioned_anywhere(name):
        """A feature module is a folder name - `Gaze`, `Emotion` - and a page writes it as an
        ordinary word, not as an identifier in code font. The symbol index only records
        identifiers, so asking it about a module reported four of ten documented when every
        one of them has pages. Look at page paths and headings too."""
        if pages_for(name):
            return True
        needle = name.lower()
        for path, data in pages.items():
            if section and not path.startswith(section):
                continue
            if needle in path.lower():
                return True
            for heading in data.get("headings", []):
                if needle in heading.get("text", "").lower():
                    return True
        return False

    report = {"subject": surface.get("subject"), "version": surface.get("version"),
              "section": section, "sets": {}}

    for set_name in sets:
        members = surface.get("sets", {}).get(set_name, [])
        if not members:
            continue
        # Folder-shaped sets are prose words; identifier-shaped sets are code font.
        looks_up = mentioned_anywhere if set_name in PROSE_SETS else pages_for
        documented, undocumented = [], []
        for symbol in members:
            (documented if looks_up(symbol) else undocumented).append(symbol)
        report["sets"][set_name] = {
            "total": len(members),
            "documented": len(documented),
            "undocumented": sorted(undocumented),
        }

    # A page that names a Convai-looking symbol the surface has never heard of is the other
    # direction of the same question, and it is the more urgent one: it is either a typo, a
    # name that was removed, or a claim about something that does not exist.
    known = set()
    for values in surface.get("sets", {}).values():
        known.update(values)
    prefixes = tuple(surface.get("symbol_prefixes") or ["Convai"])
    unknown = {}
    for symbol, hits in symbols.items():
        if not symbol.startswith(prefixes) or symbol in known:
            continue
        if "." in symbol or "(" in symbol or "::" in symbol:
            # A namespace, a tool id, or a method call. None of those are types, and the
            # surface only holds types.
            continue
        if ignore_prefixes and symbol.startswith(tuple(ignore_prefixes)):
            continue
        if section:
            hits = [h for h in hits if h.startswith(section)]
        if hits:
            unknown[symbol] = hits
    report["named_but_unknown"] = dict(sorted(unknown.items()))

    return report


def print_report(r):
    print("%s %s   coverage of the documentation against the shipped surface"
          % (r["subject"], r["version"] or ""))
    if r["section"]:
        print("scoped to pages under %s" % r["section"])

    for set_name, data in sorted(r["sets"].items()):
        pct = (100.0 * data["documented"] / data["total"]) if data["total"] else 0.0
        print("\n%s: %d of %d named on a page (%.0f%%)"
              % (set_name.replace("_", " "), data["documented"], data["total"], pct))
        for symbol in data["undocumented"][:25]:
            print("    %s" % symbol)
        if len(data["undocumented"]) > 25:
            print("    ... and %d more" % (len(data["undocumented"]) - 25))

    unknown = r["named_but_unknown"]
    print("\nNamed on a page but not in the surface  (%d)" % len(unknown))
    if not unknown:
        print("    none")
    for symbol, hits in list(unknown.items())[:25]:
        print("    %-42s %s" % (symbol, hits[0]))
    if len(unknown) > 25:
        print("    ... and %d more" % (len(unknown) - 25))

    print("\nAn undocumented symbol is a question for the owner, not a defect: plenty of")
    print("public types are internal in everything but the access modifier. A symbol named")
    print("on a page but absent from the surface is the urgent direction - it is a typo, a")
    print("removed name, or a claim about something that does not exist.")


def main():
    ap = argparse.ArgumentParser(description="Documentation coverage against a shipped surface.")
    ap.add_argument("--surface", required=True)
    ap.add_argument("--index", required=True)
    ap.add_argument("--contract", help="Read which sets count as documented surface")
    ap.add_argument("--section", help="Only consider pages under this path prefix")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    surface = read_json(args.surface)
    index = read_json(args.index)
    sets = None
    ignore_prefixes = DEFAULT_IGNORE_PREFIXES
    if args.contract:
        contract = read_json(args.contract)
        sets = (contract.get("documented_sets", []) + contract.get("coverage_sets", [])) or None
        surface.setdefault("symbol_prefixes", contract.get("symbol_prefixes"))
        ignore_prefixes = contract.get("coverage_ignore_prefixes", DEFAULT_IGNORE_PREFIXES)

    report = build_report(surface, index, sets=sets, section=args.section,
                          ignore_prefixes=ignore_prefixes)

    if args.json:
        json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print_report(report)

    # Reporting a gap is not a failure: this is a planning tool, not a gate.
    return 0


if __name__ == "__main__":
    sys.exit(main())
