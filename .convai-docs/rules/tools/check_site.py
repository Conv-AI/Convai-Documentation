#!/usr/bin/env python3
"""Whole-repository checks: the failures a single page cannot see.

`check_page.py` reads one page at a time, so there is a class of real defect it is
structurally blind to. A link is only broken relative to a repository. A page is only an
orphan relative to a navigation tree. Two titles only collide relative to each other. These
are the failures readers hit most and reviewers catch least, because catching them by hand
means holding 692 pages in your head.

Everything here is deterministic. Nothing here judges writing.

    broken-link        a relative link whose target file does not exist
    missing-image      an image whose file is not in the repository
    orphan             a page nothing links to and the sidebar does not list
    summary-dangling   a sidebar entry whose page does not exist
    summary-label      a sidebar label that does not match the page title
    duplicate-title    two pages in the same section claiming the same title
    duplicate-desc     two pages claiming the same description
    forbidden-symbol   a name a pack says must never appear
    stale-review       a version-sensitive page whose last_reviewed is behind

## Adopting this on a repository that predates it

A checker that reports 400 findings on its first run gets ignored, and then it is worse than
no checker, because it looks like a gate. So the first run writes a baseline: everything it
found is recorded as known. After that only *new* findings are reported, and the baseline
shrinks as the backlog is worked through. Nothing is silently forgiven — `--show-baseline`
prints the whole backlog whenever someone wants to see the real number.

Usage:
    python check_site.py <docs-root> [--index index.json] [--baseline FILE]
                         [--write-baseline] [--show-baseline] [--json] [--strict]
                         [--forbidden NAME ...]

Exit code 0 when there are no new ERROR findings, 1 otherwise. WARN findings fail the run
only with --strict.
"""

import argparse
import io
import json
import os
import posixpath
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_index  # noqa: E402

# Findings that break the published site are errors; the rest advise.
ERROR_KINDS = {"broken-link", "summary-dangling", "missing-image", "forbidden-symbol"}

RULE_OF_KIND = {
    "broken-link": "CV-20",
    "missing-image": "CV-48",
    "orphan": "CV-37",
    "summary-dangling": "CV-37",
    "summary-label": "CV-38",
    "duplicate-title": "CV-33",
    "duplicate-desc": "CV-34",
    "forbidden-symbol": "CV-12",
    "stale-review": "CV-35",
}


DEFAULT_CONTRACTS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "..", "packs", "contracts")


def forbidden_from_contracts(directory):
    """Collect every `must_not_exist` name the pack contracts declare.

    The never-use list belongs to the pack that knows why the name is wrong, not to a
    command-line flag someone has to remember. `ConvaiNPC` reached two published pages while
    the only thing guarding it was a sentence in a Markdown file."""
    names = set()
    directory = os.path.normpath(directory)
    if not os.path.isdir(directory):
        return names
    for fn in sorted(os.listdir(directory)):
        if not fn.endswith(".json"):
            continue
        try:
            with io.open(os.path.join(directory, fn), encoding="utf-8-sig") as f:
                names.update(json.load(f).get("must_not_exist", []))
        except (OSError, ValueError):
            continue
    return names


class Finding(object):
    def __init__(self, kind, page, detail, line=0):
        self.kind = kind
        self.page = page
        self.detail = detail
        self.line = line
        self.level = "ERROR" if kind in ERROR_KINDS else "WARN"
        self.rule = RULE_OF_KIND.get(kind)

    def key(self):
        """A stable identity for baselining. The line number is deliberately excluded: a
        finding should not reappear as new just because a paragraph moved."""
        return "%s|%s|%s" % (self.kind, self.page, self.detail)

    def as_dict(self):
        return {"kind": self.kind, "level": self.level, "rule": self.rule,
                "page": self.page, "line": self.line, "detail": self.detail}


RETIRING_FILE = ".convai-docs/retiring-sections.txt"


def top_section(page_path):
    """The part of a path a reader experiences as the product they are in."""
    parts = page_path.split("/")
    return "/".join(parts[:2]) if len(parts) > 2 else (parts[0] if parts else "")


def retiring_prefixes(root):
    """Path prefixes for content awaiting deletion, from a committed list in the repo.

    Findings there are counted separately rather than dropped. A section that is deleted
    next month should not generate a backlog nobody will ever work - but a section that
    was *supposed* to be deleted and still exists in a year should not have quietly
    stopped being checked either."""
    path = os.path.join(root, RETIRING_FILE.replace("/", os.sep))
    if not os.path.exists(path):
        return []
    out = []
    with io.open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.split("#")[0].strip()
            if line:
                out.append(line.rstrip("/"))
    return out


def resolve(from_page, target):
    """Resolve a relative link the way a static site does, from the linking page's folder."""
    target = target.split("#")[0].strip()
    if not target:
        return None
    base = posixpath.dirname(from_page)
    return posixpath.normpath(posixpath.join(base, target)) if base else posixpath.normpath(target)


# Directories with no linkable content. Deliberately *not* build_index.SKIP_DIRS: that set
# governs which folders hold pages, and `.gitbook/` holds no pages but does hold every image
# the pages point at. Skipping it here reported the whole asset library as missing.
NON_CONTENT_DIRS = {".git", "node_modules", "__pycache__", ".pytest_cache"}


def existing_files(root):
    out = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in NON_CONTENT_DIRS]
        for fn in filenames:
            rel = os.path.relpath(os.path.join(dirpath, fn), root).replace("\\", "/")
            out.add(rel)
    return out


def check(index, root, forbidden=(), retiring=()):
    findings = []
    pages = index["pages"]
    files = existing_files(root)
    page_names = set(pages)

    # A target may be written with or without the .md suffix, and a folder link means that
    # folder's README. Accept every form a GitBook site actually resolves.
    def target_exists(resolved):
        if resolved in files or resolved in page_names:
            return True
        for candidate in (resolved + ".md", posixpath.join(resolved, "README.md")):
            if candidate in files or candidate in page_names:
                return True
        return False

    for rel, page in sorted(pages.items()):
        for link in page["links"]:
            resolved = resolve(rel, link["target"])
            if resolved is None or resolved.startswith(".."):
                continue
            if not target_exists(resolved):
                findings.append(Finding("broken-link", rel, link["target"], link["line"]))

        for img in page["images"]:
            src = img["src"]
            if src.startswith(("http://", "https://", "data:")):
                continue
            resolved = resolve(rel, src)
            if resolved and not resolved.startswith("..") and resolved not in files:
                findings.append(Finding("missing-image", rel, src, img["line"]))

        for name in forbidden:
            if name in page["symbols"]:
                findings.append(Finding("forbidden-symbol", rel, name, page["symbols"][name]))

    summary = index.get("summary")
    if summary is not None:
        linked = set()
        for rel, page in pages.items():
            for link in page["links"]:
                resolved = resolve(rel, link["target"])
                if resolved:
                    linked.add(resolved)
                    linked.add(resolved + ".md")

        summary_targets = set()
        for target, label in sorted(summary.items()):
            normalised = posixpath.normpath(target)
            summary_targets.add(normalised)
            if normalised in pages:
                title = pages[normalised]["title"]
                if title and title != label:
                    findings.append(Finding(
                        "summary-label", normalised,
                        "sidebar says %r, page title is %r" % (label, title)))
            elif not target_exists(normalised):
                findings.append(Finding("summary-dangling", "SUMMARY.md",
                                        "%s (label %r)" % (target, label)))

        for rel in sorted(pages):
            if rel in summary_targets or rel in linked:
                continue
            if os.path.basename(rel) == "README.md":
                # A folder index is reached through its folder, not by its own filename.
                continue
            findings.append(Finding("orphan", rel, "not in SUMMARY.md and nothing links to it"))

    # A title is a name within its context, and the context a reader sees first is the
    # sidebar parent. `Event system` under Unity and `Event system` under Unreal is not
    # ambiguous to anyone reading; the two SDK sections mirror each other deliberately.
    # Two pages with the same title *inside one section* is still a real problem.
    for title, where in sorted(index["titles"].items()):
        if len(where) < 2:
            continue
        by_section = {}
        for page in where:
            by_section.setdefault(top_section(page), []).append(page)
        # Not `pages`: that name already holds index["pages"], and shadowing it here broke
        # the duplicate-description loop below in a way the type error pointed at the wrong line.
        for section, in_section in sorted(by_section.items()):
            if len(in_section) > 1:
                findings.append(Finding(
                    "duplicate-title", in_section[0],
                    "%r also used by %s, in the same section"
                    % (title, ", ".join(in_section[1:]))))

    by_description = {}
    for rel, page in sorted(pages.items()):
        desc = (page.get("description") or "").strip()
        if desc:
            by_description.setdefault(desc, []).append(rel)
    for desc, where in sorted(by_description.items()):
        if len(where) > 1:
            findings.append(Finding("duplicate-desc", where[0],
                                    "same description as %s" % ", ".join(where[1:])))

    if retiring:
        for f in findings:
            if any(f.page.startswith(prefix) for prefix in retiring):
                f.kind = "retiring:" + f.kind
                f.level = "INFO"

    return findings


def load_baseline(path):
    if not path or not os.path.exists(path):
        return set()
    with io.open(path, encoding="utf-8-sig") as f:
        return set(json.load(f).get("known", []))


def save_baseline(path, findings):
    payload = {
        "note": ("Findings already present when this check was adopted. They are real and "
                 "still need fixing; they are recorded here so that new problems stand out. "
                 "Remove entries as you fix them - never regenerate this file to make a run "
                 "green."),
        "count": len(findings),
        "known": sorted(f.key() for f in findings),
    }
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    ap = argparse.ArgumentParser(description="Whole-repository documentation checks.")
    ap.add_argument("root", help="Documentation repository root")
    ap.add_argument("--index", help="Reuse an index.json instead of rebuilding it")
    ap.add_argument("--baseline", help="Baseline file of already-known findings")
    ap.add_argument("--write-baseline", action="store_true",
                    help="Record every current finding as known, then exit 0")
    ap.add_argument("--show-baseline", action="store_true",
                    help="Report baselined findings too, so the real backlog is visible")
    ap.add_argument("--forbidden", nargs="*", default=[],
                    help="Extra symbol names that must never appear on any page")
    ap.add_argument("--contracts", default=DEFAULT_CONTRACTS,
                    help="Directory of pack contracts to read never-use lists from "
                         "(default: the contracts shipped with the plugin)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="Also fail on WARN findings")
    args = ap.parse_args()

    if not os.path.isdir(args.root):
        print("not a directory: %s" % args.root, file=sys.stderr)
        return 2

    if args.index:
        with io.open(args.index, encoding="utf-8-sig") as f:
            index = json.load(f)
    else:
        index = build_index.build(args.root, quiet=True)

    forbidden = sorted(set(args.forbidden) | forbidden_from_contracts(args.contracts))
    retiring = retiring_prefixes(args.root)
    findings = check(index, os.path.abspath(args.root), forbidden=forbidden, retiring=retiring)

    if args.write_baseline:
        if not args.baseline:
            print("--write-baseline needs --baseline FILE", file=sys.stderr)
            return 2
        save_baseline(args.baseline, findings)
        print("baseline written: %d known finding(s) in %s" % (len(findings), args.baseline))
        print("These are real. Work them down; do not regenerate this file to go green.")
        return 0

    known = load_baseline(args.baseline)
    new = [f for f in findings if f.key() not in known]
    baselined = [f for f in findings if f.key() in known]
    shown = findings if args.show_baseline else new

    errors = [f for f in shown if f.level == "ERROR"]
    warns = [f for f in shown if f.level == "WARN"]
    retiring_findings = [f for f in findings if f.level == "INFO"]

    if args.json:
        json.dump({
            # Named `pages_checked`, not `pages`: check_page.py uses `pages` for a list of
            # per-page results, and one key meaning two things breaks anything reading both.
            "pages_checked": index["page_count"],
            "new": [f.as_dict() for f in new],
            "baselined": len(baselined),
            "errors": len(errors),
            "warnings": len(warns),
        }, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        by_kind = {}
        for f in shown:
            by_kind.setdefault(f.kind, []).append(f)
        for kind in sorted(by_kind):
            group = by_kind[kind]
            print("\n%s  (%d)" % (kind, len(group)))
            for f in group[:40]:
                loc = "%s:%d" % (f.page, f.line) if f.line else f.page
                print("  %-5s %-6s %s  %s" % (f.level, f.rule or "", loc, f.detail))
            if len(group) > 40:
                print("  ... and %d more" % (len(group) - 40))
        print("\n%d page(s) checked. %d new finding(s): %d error(s), %d warning(s)."
              % (index["page_count"], len(new), len(errors), len(warns)))
        if retiring_findings:
            print("%d finding(s) in sections awaiting deletion, not counted. If those sections "
                  "are still here in six months, they are not being retired and this number is "
                  "real work." % len(retiring_findings))
        if baselined and not args.show_baseline:
            print("%d known finding(s) held in the baseline. Run --show-baseline to see them."
                  % len(baselined))

    if errors:
        return 1
    return 1 if (args.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
