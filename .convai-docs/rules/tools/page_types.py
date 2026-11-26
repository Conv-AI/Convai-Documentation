#!/usr/bin/env python3
"""A page's type: the template it was written from, read from the page's shape.

Pages carry no type key. A key would be one more fact a person has to keep true, GitBook's
editor does not write it, and none of the published pages has one. The template a page was
written from is visible in the headings and blocks that template requires, so the type is
read from those instead (`page_type`).

Two tools use it. `pick_example.py` picks the example page a writer imitates by type, and
`check_page.py` applies the rules the quality checklist limits to task and concept pages
(CV-30, CV-39) only to pages of those modes.

`MODES` maps each template to its Diataxis mode, as the table in `references/page-types.md`
does; `tests/test_check_page.py` holds the two to the same answer.
"""

import re

TYPES = ("how-to", "tutorial", "reference", "explanation", "hub", "troubleshooting", "faq",
         "glossary", "migration", "release-notes", "api-endpoint", "interface-tour",
         "interface-task", "field-reference")

# The Diataxis mode of each template. A hub and an FAQ route or answer; they have no mode.
MODES = {
    "how-to": "how-to", "interface-task": "how-to", "troubleshooting": "how-to",
    "migration": "how-to", "tutorial": "tutorial",
    "reference": "reference", "field-reference": "reference", "interface-tour": "reference",
    "api-endpoint": "reference", "release-notes": "reference",
    "explanation": "explanation", "glossary": "explanation",
    "hub": None, "faq": None,
}

# The modes the quality checklist calls task and concept pages: "no more than two hints on
# task and concept pages" (CV-39) and "no `####` headings on task or concept pages" (CV-30).
TASK_OR_CONCEPT = ("how-to", "tutorial", "explanation")

H2_RE = re.compile(r"^##\s+(.+?)\s*#*\s*$", re.MULTILINE)
VERSION_HEADING = re.compile(r"^v?\d+\.\d+")
AREA_HEADING = re.compile(r"^the .+ area$")
OPEN_TAB_HEADING = re.compile(r"^open the .+ tab$")
REFERENCE_HEADINGS = {"fields", "methods", "events", "errors and constraints", "related reference"}


def _headings(text):
    """The `##` headings outside code fences, lower-cased."""
    out, fenced = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if not fenced:
            m = H2_RE.match(line)
            if m:
                out.append(m.group(1).strip().lower())
    return out


def page_type(text, name):
    """The template a page was written from, or None. The rules run in this order because
    the earlier shapes are the more specific ones: a troubleshooting page also has steps,
    and a migration guide also has prerequisites."""
    name = name.lower()
    heads = _headings(text)
    hset = set(heads)
    if name in ("release-notes.md", "changelog.md") or any(VERSION_HEADING.match(h) for h in heads):
        return "release-notes"
    if "glossary" in name:
        return "glossary"
    if "faq" in name:
        return "faq"
    if name in ("readme.md", "hub.md") or 'data-view="cards"' in text:
        return "hub"
    if {"endpoint", "request", "response"} <= hset:
        return "api-endpoint"
    if name.startswith("migrat") or {"what changed", "breaking changes"} & hset:
        return "migration"
    if "still blocked" in hset or "troubleshoot" in name:
        return "troubleshooting"
    if "labels that change" in hset or sum(1 for h in heads if AREA_HEADING.match(h)) >= 2:
        return "interface-tour"
    if any(OPEN_TAB_HEADING.match(h) for h in heads):
        return "interface-task"
    if any(h.endswith(" fields") for h in heads):
        return "field-reference"
    if {"what we will build", "run the character"} & hset:
        return "tutorial"
    if REFERENCE_HEADINGS & hset:
        return "reference"
    if "prerequisites" in hset or "{% stepper %}" in text:
        return "how-to"
    if "related concepts" in hset:
        return "explanation"
    if len(heads) >= 2 and sum(1 for h in heads if h.endswith("?")) * 3 >= len(heads) * 2:
        return "faq"
    return None


def task_or_concept(ptype):
    """Whether the checklist's task-and-concept limits apply to a page of type `ptype`. A page
    of no recognised type is held to them, as every page was before types were read."""
    return ptype is None or MODES[ptype] in TASK_OR_CONCEPT
