#!/usr/bin/env python3
"""The public part of each subject: what the documentation repository's checks may know.

A subject file describes private source (repositories, paths, recipes, decisions), so it is
never copied into the public documentation repository. The checks that run there still need
a few of its facts: the names a page must never use, the terms it rejects, and which pages
are historical and may name a retired symbol. `scripts/sync_agent_rules.py` writes those
facts, and nothing else, into `site-rules.json` beside `tools/` in the bundle.

Every tool reads them through `entries()`:

- In the plugin, the subject files are there, and `entries()` reads them directly.
- In the documentation repository, they are not, and `entries()` reads `site-rules.json`.

So the same tool gives the same answer in both places, and there is no second list anybody
has to keep in step with the subjects.

Usage:
    python site_rules.py            print the site-rules.json the subjects produce
"""

import io
import json
import os
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
SUBJECTS_DIR = os.path.normpath(os.path.join(TOOLS_DIR, "..", "subjects"))
SITE_RULES_FILE = os.path.normpath(os.path.join(TOOLS_DIR, "..", "site-rules.json"))

# The subject keys that are public, copied as they are.
PUBLIC_FIELDS = ("product_name", "short_name", "docs_paths", "must_not_exist")
# Each terminology entry keeps only these keys. Its `why` can describe the source.
TERM_FIELDS = ("use", "reject")
# `extract.historical_pages` holds globs over documentation pages, not over source. It is the
# one part of `extract` that is public; without it a migration page that names a retired
# symbol would fail the never-use check it is meant to be exempt from.
HISTORICAL = "historical_pages"


def _read_json(path):
    with io.open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def public_part(subject):
    """The fields of one subject that may be published, in a fixed shape."""
    out = {key: subject.get(key) for key in PUBLIC_FIELDS}
    out["terminology"] = [{k: term[k] for k in TERM_FIELDS if k in term}
                          for term in subject.get("terminology", [])]
    extract = subject.get("extract")
    out[HISTORICAL] = list(extract.get(HISTORICAL, [])) if isinstance(extract, dict) else []
    return out


def _subject_files(directory):
    if not os.path.isdir(directory):
        return {}
    out = {}
    for fn in sorted(os.listdir(directory)):
        if not fn.endswith(".json") or fn.startswith("_"):
            continue
        data = _read_json(os.path.join(directory, fn))
        if isinstance(data, dict):
            out[fn[:-len(".json")]] = public_part(data)
    return out


def build(directory=SUBJECTS_DIR, publish=None):
    """The content of `site-rules.json`, from the subject files in `directory`, and the
    plugin's `publish` settings (`base_branch`, `enabled`), which AGENTS.md and the Cursor
    rule tell Codex and Cursor to read here instead of naming a branch themselves."""
    out = {
        "generated_by": "convai-docs scripts/sync_agent_rules.py",
        "note": ("The public part of each subject, and the publishing settings. Generated; do "
                 "not edit. The checks in tools/ read it when the subject files are not present."),
        "subjects": _subject_files(directory),
    }
    if publish is not None:
        out["publish"] = {"base_branch": publish["base_branch"],
                          "enabled": bool(publish.get("enabled"))}
    return out


def render(directory=SUBJECTS_DIR, publish=None):
    """`build()` as the bytes the bundle carries."""
    return (json.dumps(build(directory, publish), indent=2, sort_keys=True, ensure_ascii=False)
            + "\n").encode("utf-8")


def entries(directory=None):
    """{subject name: public part}.

    With `directory`, the subject files in it. Without, the subject files shipped with the
    plugin when they are present, else `site-rules.json` beside `tools/`, else nothing."""
    if directory is not None:
        return _subject_files(directory)
    if os.path.isdir(SUBJECTS_DIR):
        return _subject_files(SUBJECTS_DIR)
    if os.path.isfile(SITE_RULES_FILE):
        data = _read_json(SITE_RULES_FILE)
        subjects = data.get("subjects") if isinstance(data, dict) else None
        if not isinstance(subjects, dict):
            raise ValueError("%s has no `subjects` object" % SITE_RULES_FILE)
        return subjects
    return {}


def entry(name):
    """The public part of one subject. An unknown name is an error, because a check that
    silently extends nothing looks exactly like one that worked."""
    found = entries()
    if name not in found:
        raise ValueError("no subject named %r in %s (known: %s)"
                         % (name, SUBJECTS_DIR if os.path.isdir(SUBJECTS_DIR) else SITE_RULES_FILE,
                            ", ".join(sorted(found)) or "none"))
    return found[name]


def rejected_terms(subject):
    """Every variant the subject's terminology rejects, lower-cased."""
    out = []
    for term in subject.get("terminology", []):
        for variant in term.get("reject", []):
            if variant.lower() not in out:
                out.append(variant.lower())
    return out


def main():
    sys.stdout.write(render().decode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
