#!/usr/bin/env python3
"""Which rules actually fail, and where.

A quality system that cannot count itself improves only as fast as one person's intuition
about what keeps going wrong. That is the part of this tooling that depends on a maintainer
being around, and it is the part worth removing.

Every gate already emits machine-readable findings that name a CV rule: `check_page.py --json`,
`check_site.py --json`, `check_pack.py --json`, and the `docs-reviewer`, which ends its report
with a JSON block. Dropping those into `.convai-docs/findings/` and rolling them up answers
questions nobody can answer today:

    Which rule fails most often?      That rule is a candidate for the linter, a template
                                      change, or a clearer explanation - the fix depends on
                                      whether people are getting it wrong or not knowing it.
    Which rule never fails?           Either everyone has internalised it, or nothing checks
                                      it and the number is a lie. Both are worth knowing.
    Is quality moving?                Findings per page, over time, from the same gates.

Read the output as a question, not a verdict. A rule failing often may be a badly written
rule rather than a badly written page - and CONTRIBUTING says a rule that makes pages worse
should be changed, not worked around. This is the evidence for that conversation.

Usage:
    python collect_findings.py <findings-dir> [--rules rules.json] [--since YYYY-MM-DD] [--json]
"""

import argparse
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rules as rulelib  # noqa: E402


def read_json(path):
    with io.open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def iter_findings(payload, source):
    """Normalise the shapes the different gates emit into one record type.

    Each tool grew its own output before there was a reason to compare them, so this is the
    one place that knows the difference. Adding a new gate means teaching this function its
    shape, not changing the gate."""
    # check_page.py: {"pages": [{"page": ..., "findings": [{"rule", "level", "message"}]}]}
    # Guarded by type rather than by key: another gate once used `pages` for a count, and a
    # crash here would take down the only tool that measures whether any of this works.
    page_results = payload.get("pages")
    for page in page_results if isinstance(page_results, list) else []:
        if not isinstance(page, dict):
            continue
        for f in page.get("findings", []):
            yield {"rule": f.get("rule"), "level": f.get("level"), "page": page.get("page"),
                   "detail": f.get("message"), "gate": "lint", "source": source}

    # check_site.py: {"new": [{"kind", "level", "rule", "page", "detail"}]}
    entries = payload.get("new")
    for f in entries if isinstance(entries, list) else []:
        if not isinstance(f, dict):
            continue
        yield {"rule": f.get("rule"), "level": f.get("level"), "page": f.get("page"),
               "detail": f.get("detail"), "gate": "site", "source": source}

    # check_pack.py: {"findings": [{"kind", "level", "subject", "detail"}]}
    # docs-reviewer:  {"findings": [{"rule", "level", "location", "summary"}]}
    entries = payload.get("findings")
    for f in entries if isinstance(entries, list) else []:
        if not isinstance(f, dict):
            continue
        level = f.get("level")
        gate = "review" if "location" in f or "summary" in f else "pack"
        if gate == "review":
            level = {"blocking": "ERROR", "suggestion": "WARN"}.get(level, level)
        yield {"rule": f.get("rule"), "level": level,
               "page": f.get("page") or f.get("location") or f.get("subject"),
               "detail": f.get("summary") or f.get("detail"), "gate": gate, "source": source}


def collect(directory, since=None):
    records = []
    unreadable = []
    for dirpath, dirnames, filenames in os.walk(directory):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for fn in sorted(filenames):
            if not fn.endswith(".json"):
                continue
            # Findings are filed as <date>-<whatever>.json, so a date filter is a name filter.
            if since and fn[:10] < since:
                continue
            path = os.path.join(dirpath, fn)
            try:
                payload = read_json(path)
            except (OSError, ValueError) as e:
                unreadable.append({"file": path, "error": str(e)})
                continue
            records.extend(iter_findings(payload, os.path.relpath(path, directory)))
    return records, unreadable


def roll_up(records, known_rules=None):
    by_rule, by_gate, by_page = {}, {}, {}
    untagged = 0

    for r in records:
        rule = r.get("rule")
        if not rule:
            untagged += 1
        else:
            entry = by_rule.setdefault(rule, {"total": 0, "errors": 0, "pages": set()})
            entry["total"] += 1
            if r.get("level") == "ERROR":
                entry["errors"] += 1
            if r.get("page"):
                entry["pages"].add(str(r["page"]).split(":")[0])
        by_gate[r.get("gate", "?")] = by_gate.get(r.get("gate", "?"), 0) + 1
        page = str(r.get("page") or "").split(":")[0]
        if page:
            by_page[page] = by_page.get(page, 0) + 1

    ranked = sorted(
        ({"rule": rule, "total": d["total"], "errors": d["errors"], "pages": len(d["pages"])}
         for rule, d in by_rule.items()),
        key=lambda x: (-x["total"], x["rule"]))

    never_failed = []
    if known_rules:
        seen = set(by_rule)
        never_failed = sorted(("CV-%d" % n for n in known_rules if "CV-%d" % n not in seen),
                              key=lambda s: int(s.split("-")[1]))

    return {
        "records": len(records),
        "untagged": untagged,
        "by_gate": dict(sorted(by_gate.items())),
        "ranked": ranked,
        "never_failed": never_failed,
        "worst_pages": sorted(({"page": p, "findings": n} for p, n in by_page.items()),
                              key=lambda x: (-x["findings"], x["page"]))[:15],
    }


def print_summary(s, unreadable):
    print("%d finding(s) across %s" % (s["records"], ", ".join(
        "%s=%d" % (g, n) for g, n in s["by_gate"].items()) or "no gates"))
    if s["untagged"]:
        print("%d carried no rule id and cannot be compared across gates." % s["untagged"])

    print("\nMost frequent rules")
    if not s["ranked"]:
        print("  nothing recorded yet")
    for row in s["ranked"][:15]:
        print("  %-8s %4d finding(s) on %3d page(s)   %d blocking"
              % (row["rule"], row["total"], row["pages"], row["errors"]))

    if s["worst_pages"]:
        print("\nPages with the most findings")
        for row in s["worst_pages"][:8]:
            print("  %4d  %s" % (row["findings"], row["page"]))

    if s["never_failed"]:
        print("\n%d rule(s) have never been flagged: %s%s"
              % (len(s["never_failed"]), ", ".join(s["never_failed"][:14]),
                 ", ..." if len(s["never_failed"]) > 14 else ""))
        print("Either everyone has internalised them, or nothing checks them. Worth knowing which.")

    for u in unreadable:
        print("\nUNREADABLE %s: %s" % (u["file"], u["error"]))

    print("\nA rule at the top of this list is a question, not a verdict. People may be getting")
    print("it wrong, they may not know it exists, or the rule itself may be making pages worse.")
    print("Those three have different fixes: a linter check, a clearer template, or a rule change.")


def main():
    ap = argparse.ArgumentParser(description="Roll up recorded findings by rule.")
    ap.add_argument("directory", help="Directory of finding JSON files")
    ap.add_argument("--rules", help="rules.json, to list rules that have never been flagged")
    ap.add_argument("--since", metavar="YYYY-MM-DD", help="Ignore files named before this date")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(args.directory):
        print("not a directory: %s" % args.directory, file=sys.stderr)
        return 2

    records, unreadable = collect(args.directory, since=args.since)

    known = None
    if args.rules:
        known = sorted(int(k.split("-")[1]) for k in rulelib.load_registry(args.rules))
    summary = roll_up(records, known_rules=known)

    if args.json:
        json.dump(summary, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print_summary(summary, unreadable)
    return 0


if __name__ == "__main__":
    sys.exit(main())
