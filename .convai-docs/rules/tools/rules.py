#!/usr/bin/env python3
"""The CV rule registry: the one place that knows which rule IDs exist.

Every enforceable Convai documentation rule has a permanent id, `CV-<n>`. The rule text
lives in exactly one file, `gitbook/styleguide.md`, because GitBook's agent reads that page
and only that page. Everything else — this linter, the reviewer agent, the reference files,
a flag left on a change request — refers to a rule by its id rather than restating it.

That only works if ids are stable. An id that gets renumbered or reused silently rewrites
history: a flag recorded last month, or a line in the style guide's decision log, starts
pointing at a different rule. So the ids are pinned in `gitbook/rules.json`, and
`check_rules.py` fails the build when a pinned id changes meaning or disappears.

This module is the shared extractor. It has no dependencies beyond the standard library so
it runs anywhere the linter runs.
"""

import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
STYLEGUIDE = os.path.join(SKILL_ROOT, "gitbook", "styleguide.md")
REGISTRY = os.path.join(SKILL_ROOT, "gitbook", "rules.json")

# A rule is *defined* in one of three shapes on the style guide page. Anything else that
# mentions `CV-n` is a cross-reference, not a definition.
DEFINITION_PATTERNS = [
    # * **CV-1:** No marketing language...
    re.compile(r"(?m)^\* \*\*CV-(\d+):\*\*[ \t]*(.+)$"),
    # | CV-14 | Serial comma | ... |
    re.compile(r"(?m)^\| CV-(\d+) \|[ \t]*([^|]+)"),
    # | The backend | **Convai** | ... | **CV-10.** Write "streams audio to Convai" |
    re.compile(r"\*\*CV-(\d+)\.\*\*[ \t]*([^|]+)"),
]
ANY_REFERENCE = re.compile(r"CV-(\d+)")


def _read(path):
    with io.open(path, encoding="utf-8-sig") as f:
        return f.read()


def summarize(text, limit=90):
    """A short, stable fingerprint of a rule, used to notice an id changing meaning.

    Markdown emphasis and inline code are stripped so that reformatting a rule — adding
    backticks around a banned word, say — does not read as a different rule."""
    text = re.sub(r"[`*_]", "", text)
    text = re.sub(r"\s+", " ", text).strip().rstrip(".")
    return text[:limit]


def extract_rules(styleguide_path=STYLEGUIDE):
    """Return {id_number: {"summary": str, "line": int}} for every rule defined."""
    text = _read(styleguide_path)
    line_of = {}
    offset = 0
    for i, line in enumerate(text.split("\n"), start=1):
        line_of[offset] = i
        offset += len(line) + 1

    def lineno(pos):
        starts = [p for p in line_of if p <= pos]
        return line_of[max(starts)] if starts else 1

    rules = {}
    duplicates = []
    for pattern in DEFINITION_PATTERNS:
        for m in pattern.finditer(text):
            num = int(m.group(1))
            if num in rules:
                duplicates.append(num)
                continue
            rules[num] = {"summary": summarize(m.group(2)), "line": lineno(m.start())}
    return rules, sorted(set(duplicates))


def cross_references(paths):
    """Return {id_number: [file, ...]} for every `CV-n` mentioned in the given files."""
    refs = {}
    for path in paths:
        try:
            text = _read(path)
        except (OSError, UnicodeDecodeError):
            continue
        for m in ANY_REFERENCE.finditer(text):
            refs.setdefault(int(m.group(1)), []).append(path)
    return refs


def load_registry(path=REGISTRY):
    if not os.path.exists(path):
        return {}
    with io.open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def save_registry(rules, path=REGISTRY, stamped_on=None):
    """Write the registry. `stamped_on` is passed in rather than read from the clock so a
    regeneration is reproducible and reviewable in a diff."""
    existing = load_registry(path)
    out = {}
    for num in sorted(rules):
        key = "CV-%d" % num
        prior = existing.get(key, {})
        out[key] = {
            "summary": rules[num]["summary"],
            "first_seen": prior.get("first_seen", stamped_on or "unknown"),
        }
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=2, ensure_ascii=False, sort_keys=False)
        f.write("\n")
    return out
