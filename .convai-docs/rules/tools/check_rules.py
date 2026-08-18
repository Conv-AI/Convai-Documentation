#!/usr/bin/env python3
"""Validate the CV rule registry against the style guide.

Run this whenever the style guide changes. It answers four questions the eye cannot answer
reliably on a page of 75 numbered rules:

    Is any id defined twice?          Two rules under one id means a flag is ambiguous.
    Is any id missing from the run?   A gap usually means a rule was deleted by accident.
    Did a pinned id change meaning?   The most damaging case: past flags now point elsewhere.
    Does anything reference an id     A dangling `CV-91` in an agent prompt or a reference
    that does not exist?              file sends a writer looking for a rule that is not there.

Usage:
    python check_rules.py                 validate; exit 1 on any error
    python check_rules.py --update DATE   re-pin the registry, stamping new ids with DATE
    python check_rules.py --json          machine-readable output for CI

A deliberate rule change is expected to fail this check once. Re-run with `--update` and
commit the registry diff — that diff is the audit trail of what the rule used to say.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rules as rulelib  # noqa: E402

SKILL_ROOT = rulelib.SKILL_ROOT

# Places that are allowed to refer to a rule by id. Every id they mention must exist.
REFERENCE_DIRS = ["references", "templates", "packs", "plans"]
REFERENCE_SIBLINGS = [
    os.path.join(os.path.dirname(SKILL_ROOT), "..", "agents"),
    os.path.join(os.path.dirname(SKILL_ROOT), "..", "commands"),
]


def referencing_files():
    out = []
    for d in REFERENCE_DIRS:
        root = os.path.join(SKILL_ROOT, d)
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [x for x in dirnames if x != "__pycache__"]
            out += [os.path.join(dirpath, f) for f in filenames if f.endswith(".md")]
    for d in REFERENCE_SIBLINGS:
        root = os.path.normpath(d)
        if not os.path.isdir(root):
            continue
        out += [os.path.join(root, f) for f in os.listdir(root) if f.endswith(".md")]
    return sorted(out)


def validate(update=None):
    errors = []
    warnings = []

    found, duplicates = rulelib.extract_rules()
    if not found:
        return ["no CV rules found in the style guide; is the file empty or renamed?"], [], {}

    for num in duplicates:
        errors.append("CV-%d is defined more than once; one id must mean one rule" % num)

    highest = max(found)
    gaps = [n for n in range(1, highest + 1) if n not in found]
    for n in gaps:
        errors.append(
            "CV-%d is missing while CV-%d exists; retire a rule by marking it retired, "
            "never by deleting the id" % (n, highest))

    registry = rulelib.load_registry()
    for key, pinned in registry.items():
        num = int(key.split("-")[1])
        if num not in found:
            errors.append("%s is pinned in the registry but no longer defined; a past flag "
                          "referring to it now points at nothing" % key)
        elif pinned.get("summary") and pinned["summary"] != found[num]["summary"]:
            errors.append(
                "%s changed meaning.\n      was: %s\n      now: %s\n"
                "      If this is deliberate, re-run with --update and record it in the "
                "style guide decision log." % (key, pinned["summary"], found[num]["summary"]))

    refs = rulelib.cross_references(referencing_files())
    for num in sorted(refs):
        if num not in found:
            where = sorted(set(os.path.relpath(p, SKILL_ROOT) for p in refs[num]))
            errors.append("CV-%d is referenced by %s but is not defined in the style guide"
                          % (num, ", ".join(where)))

    unreferenced = sorted(n for n in found if n not in refs)
    if unreferenced:
        warnings.append(
            "%d rule(s) are defined but referenced nowhere outside the style guide: %s. "
            "That is fine for a rule only a human applies, but a rule the linter or an "
            "agent should enforce needs a pointer to it."
            % (len(unreferenced), ", ".join("CV-%d" % n for n in unreferenced[:12])
               + (", ..." if len(unreferenced) > 12 else "")))

    if update:
        rulelib.save_registry(found, stamped_on=update)

    return errors, warnings, found


def main():
    ap = argparse.ArgumentParser(description="Validate the CV rule registry.")
    ap.add_argument("--update", metavar="YYYY-MM-DD",
                    help="re-pin the registry, stamping newly added ids with this date")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    errors, warnings, found = validate(update=args.update)

    if args.json:
        json.dump({"rules": len(found), "errors": errors, "warnings": warnings},
                  sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        if args.update:
            print("registry re-pinned: %d rules" % len(found))
        for e in errors:
            print("ERROR  %s" % e)
        for w in warnings:
            print("WARN   %s" % w)
        if not errors:
            print("\nOK  %d rules, ids CV-1 through CV-%d, no gaps and no reuse."
                  % (len(found), max(found) if found else 0))

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
