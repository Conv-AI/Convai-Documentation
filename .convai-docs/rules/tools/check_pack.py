#!/usr/bin/env python3
"""Compare a pack's prose against the source it claims to describe.

A pack is the only part of this tooling that describes something outside it, so it is the
only part that can go wrong while nobody touches it. The SDK renames a component, adds a
module, drops an enum; the pack keeps confidently handing the writer the old name, and every
gate downstream trusts it. Every wrong fact this system has shipped entered exactly there.

Until now the only defence was a person remembering to run an audit. This makes the
mechanical half deterministic:

    wrong        the pack names a type the source does not have
    missing      the source has a module the pack never mentions
    coverage     how much of a large surface the pack accounts for, as one finding
    stale-guard  a name the contract says can never exist now exists in source
    absent-guard a name the contract says must exist is gone from source
    frozen       a version literal written into the pack, which goes stale by itself
    unaudited    the pack's audit sha does not match the surface it is being checked against

What it deliberately does not do is judge whether the pack's *advice* is still right. Whether
"prefer the scene installer for IL2CPP" still holds is a question for a person; whether
`ConvaiSceneInstaller` still exists is a question for a machine, and this answers that one so
the person can spend their attention on the other.

Usage:
    python check_pack.py <pack.md> --contract <contract.json> --surface <surface.json>
    python check_pack.py <pack.md> --contract <contract.json> --source <sdk-root>
"""

import argparse
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract_surface  # noqa: E402

INLINE_CODE = re.compile(r"`([^`\n]+)`")
VERSION_LITERAL = re.compile(r"\b\d+\.\d+\.\d+\b")
# `Last audited: <date> against ... <sha>`. The middle is free text on purpose: a subject
# with more than one repository needs to say which one, and the sha is taken as the last
# commit-shaped token on the line rather than the first thing after "against".
AUDIT_LINE = re.compile(r"^Last audited:\s*(\S+)\s+against\s+(.+)$", re.MULTILINE)
SHA_TOKEN = re.compile(r"\b([0-9a-f]{7,40})\b")

SEVERITY = {
    "wrong": "ERROR",
    "stale-guard": "ERROR",
    "absent-guard": "ERROR",
    "missing": "WARN",
    "coverage": "WARN",
    "frozen": "WARN",
    "unaudited": "WARN",
}


class Finding(object):
    def __init__(self, kind, subject, detail, fix=""):
        self.kind = kind
        self.subject = subject
        self.detail = detail
        self.fix = fix
        self.level = SEVERITY[kind]

    def as_dict(self):
        return {"kind": self.kind, "level": self.level, "subject": self.subject,
                "detail": self.detail, "fix": self.fix}


def read(path):
    with io.open(path, encoding="utf-8-sig") as f:
        return f.read()


def pack_symbols(text, prefixes):
    """Every backticked token in the pack that is one of *our* type names.

    The prefix filter matters: a pack legitimately names `GameObject` and `MonoBehaviour`,
    which belong to Unity and will never be in our surface. Reporting those as wrong would
    make the check useless on its first run."""
    out = {}
    for lineno, line in enumerate(text.split("\n"), start=1):
        for m in INLINE_CODE.finditer(line):
            token = m.group(1).strip()
            if any(token.startswith(p) for p in prefixes) and re.match(r"^[A-Za-z_]\w*$", token):
                out.setdefault(token, lineno)
    return out


def check(pack_text, contract, surface):
    findings = []
    prefixes = contract.get("symbol_prefixes", ["Convai"])
    known = set()
    for values in surface["sets"].values():
        known.update(values)

    # Menu labels contain the type's own words but are not type names; a component's label
    # is checked separately by the verifier, not here.
    # A pack is *required* to name the never-use list, so those are not wrong here.
    guarded = set(contract.get("must_not_exist", []))
    for symbol, lineno in sorted(pack_symbols(pack_text, prefixes).items()):
        if symbol not in known and symbol not in guarded:
            findings.append(Finding(
                "wrong", "%s:%d" % (contract["subject"], lineno),
                "pack names `%s`, which is not in the source surface" % symbol,
                "Find the current name in the surface and correct the pack, or delete the claim."))

    # A whole area the pack is silent about is worse than a wrong name: a writer relying on
    # the pack cannot know to ask about it. Two granularities, because they need different
    # answers.
    #
    # `documented_sets` are small and every member matters - a missing feature module is a
    # real hole, and there are ten of them.
    for set_name in contract.get("documented_sets", ["modules"]):
        for value in surface["sets"].get(set_name, []):
            if value not in pack_text:
                findings.append(Finding(
                    "missing", contract["subject"],
                    "source has %s `%s`, which the pack never mentions" % (set_name.rstrip("s"), value),
                    "Add it to the pack, or say explicitly that it is internal and undocumented."))

    # `coverage_sets` are large, and the pack legitimately summarises them at module level
    # rather than listing every member. Reporting sixty-three separate findings there would
    # bury the ten that matter, and a check people scroll past is worse than no check. So
    # this is one finding carrying a ratio.
    for set_name in contract.get("coverage_sets", []):
        members = surface["sets"].get(set_name, [])
        if not members:
            continue
        unmentioned = [m for m in members if m not in pack_text]
        if not unmentioned:
            continue
        shown = ", ".join("`%s`" % m for m in unmentioned[:8])
        if len(unmentioned) > 8:
            shown += ", and %d more" % (len(unmentioned) - 8)
        findings.append(Finding(
            "coverage", contract["subject"],
            "pack names %d of %d %s; unmentioned: %s"
            % (len(members) - len(unmentioned), len(members), set_name.replace("_", " "), shown),
            "Summarising these at module level is fine. Check that each unmentioned one "
            "belongs to a module the pack does describe, and add any that do not."))

    for name in contract.get("must_not_exist", []):
        if name in known:
            findings.append(Finding(
                "stale-guard", contract["subject"],
                "`%s` is on the never-use list but now exists in source" % name,
                "The name became real. Remove it from must_not_exist and decide how to document it."))

    for name in contract.get("must_exist", []):
        if name not in known:
            findings.append(Finding(
                "absent-guard", contract["subject"],
                "`%s` is required by the contract but is not in source" % name,
                "Either the type was renamed and every page naming it is now wrong, or the "
                "contract's extraction recipe stopped matching. Check which before editing."))

    for lineno, line in enumerate(pack_text.split("\n"), start=1):
        if line.startswith("Last audited:"):
            continue
        for m in VERSION_LITERAL.finditer(line):
            findings.append(Finding(
                "frozen", "%s:%d" % (contract["subject"], lineno),
                "version literal %s written into the pack" % m.group(0),
                "A pack records where a value lives, never the value. Point at the GitBook "
                "variable or at package.json instead."))

    audit = AUDIT_LINE.search(pack_text)
    generated = surface.get("generated_against", "unrecorded")
    audited_sha = None
    if audit:
        shas = SHA_TOKEN.findall(audit.group(2))
        audited_sha = shas[-1] if shas else None

    if audit is None:
        findings.append(Finding(
            "unaudited", contract["subject"], "the pack has no `Last audited:` line",
            "Add `Last audited: <date> against <sha>` once you have checked it."))
    elif audited_sha is None:
        findings.append(Finding(
            "unaudited", contract["subject"],
            "the `Last audited:` line names no commit",
            "A date alone cannot be checked against anything. Name the commit the pack was "
            "read against, so a later reader can tell whether the source has moved since."))
    elif generated not in ("unrecorded", None) and not generated.startswith(audited_sha[:7]) \
            and not audited_sha.startswith(generated[:7]):
        findings.append(Finding(
            "unaudited", contract["subject"],
            "pack was audited against %s; this surface is from %s" % (audited_sha, generated),
            "Re-audit and update the line, or regenerate the surface from the audited commit."))

    return findings


def main():
    ap = argparse.ArgumentParser(description="Check a pack against its source surface.")
    ap.add_argument("pack", help="Path to the pack markdown")
    ap.add_argument("--contract", required=True)
    ap.add_argument("--surface", help="A surface.json produced by extract_surface.py")
    ap.add_argument("--source", help="Extract the surface now from this source checkout")
    ap.add_argument("--stamp", help="Commit sha to record when extracting")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="Also fail on WARN findings")
    args = ap.parse_args()

    contract = json.loads(read(args.contract))
    if args.surface:
        surface = json.loads(read(args.surface))
    elif args.source:
        surface = extract_surface.extract(contract, args.source)
        surface["generated_against"] = args.stamp or "unrecorded"
    else:
        print("give either --surface or --source", file=sys.stderr)
        return 2

    findings = check(read(args.pack), contract, surface)
    errors = [f for f in findings if f.level == "ERROR"]
    warns = [f for f in findings if f.level == "WARN"]

    if args.json:
        json.dump({"pack": args.pack, "version": surface.get("version"),
                   "errors": len(errors), "warnings": len(warns),
                   "findings": [f.as_dict() for f in findings]},
                  sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print("pack: %s   source version: %s   surface from: %s"
              % (args.pack, surface.get("version"), surface.get("generated_against")))
        by_kind = {}
        for f in findings:
            by_kind.setdefault(f.kind, []).append(f)
        for kind in sorted(by_kind):
            group = by_kind[kind]
            print("\n%s  (%d)" % (kind, len(group)))
            for f in group[:30]:
                print("  %-5s %s  %s" % (f.level, f.subject, f.detail))
                if f.fix:
                    print("        -> %s" % f.fix)
            if len(group) > 30:
                print("  ... and %d more" % (len(group) - 30))
        print("\n%d error(s), %d warning(s)." % (len(errors), len(warns)))
        if not findings:
            print("The pack matches the source.")

    if errors:
        return 1
    return 1 if (args.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
