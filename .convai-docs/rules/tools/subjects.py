#!/usr/bin/env python3
"""Load and validate subject files, the one place a subject's decisions live.

A subject replaces a 2.x pack. A pack was hand-written prose plus a contract, and the prose
went stale three times in three months. A subject holds only what code cannot answer and
where to look for the rest: `subjects/<name>.json`, one per subject, documented once in
`references/subjects.md`. Everything the source can say is read from the source, by the
recipes in `extract`, whenever the subject is used.

Every tool that used to read `packs/contracts/<subject>.json` reads a subject through
`contract()`, which gives the shape those tools already expect (`subject`, `source_repo`,
`package_root`, `extract`, `must_not_exist` and the rest). The subject file is the only
thing on disk; the contract is a view of it.

Usage:
    python subjects.py validate [<name-or-path> ...]   validate every subject, or those named
    python subjects.py list                            one line per subject
    python subjects.py contract <name-or-path>         print the contract view as JSON
"""

import argparse
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SUBJECTS_DIR = os.path.normpath(os.path.join(HERE, "..", "subjects"))
# An explicit directory of subject files, for tests and for a subject created on this run
# that is not yet in the plugin (see new_subject.py).
SUBJECTS_ENV = "CONVAI_DOCS_SUBJECTS"
# Where new_subject.py writes a subject created on this run. A name found nowhere else is
# looked up here, so the new subject works by name before its pull request merges.
SUBJECT_CACHE = os.path.join(os.path.expanduser("~"), ".convai-docs", "cache", "subjects")

KINDS = ("sdk", "product", "customer")
NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VAR_RE = re.compile(r"^[a-z][a-z0-9_]*$")
CAPTURE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CAPTURE_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")

TOP_KEYS = ("name", "kind", "product_name", "short_name", "audience", "docs_paths", "sources",
            "extract", "terminology", "must_exist", "must_not_exist", "decisions", "evidence",
            "capture")
REQUIRED_KEYS = ("name", "kind", "product_name", "short_name", "audience", "docs_paths",
                 "sources", "extract", "terminology", "must_exist", "must_not_exist",
                 "decisions")
SOURCE_KEYS = ("owner", "repo", "ref", "root", "why")
EXTRACT_KEYS = ("version", "recipes", "symbol_prefixes", "documented_sets", "coverage_sets",
                "coverage_ignore_prefixes", "historical_pages", "interface_map")
RECIPE_KEYS = ("glob", "file", "capture", "why", "name_pattern", "field", "key", "attribute",
               "methods", "require", "fields", "parent_key")
CAPTURES = ("csharp_type", "attributed_type", "cpp_type", "ts_export", "python_class",
            "http_route", "key_value_string", "json_field", "dir_name", "file_name",
            "attribute", "ts_object")
# What each capture cannot run without.
CAPTURE_NEEDS = {"key_value_string": ("key",), "attributed_type": ("attribute",),
                 "attribute": ("attribute",), "json_field": ("field",),
                 "ts_object": ("require",)}
TERM_KEYS = ("use", "reject", "why")
DECISION_KEYS = ("decision", "date", "by", "about")
EVIDENCE_KEYS = ("owner", "proof", "source_does_not_settle", "open_questions")
# Keys that may be null, and only when the subject says why: a decision `about` the key, or
# an `evidence.open_questions` entry that starts with "<key>:". An unknown fact stays a
# listed question instead of becoming a guess.
NULLABLE = ("product_name", "short_name", "audience")


class SubjectError(ValueError):
    """A subject file is missing, unreadable, or does not match the schema."""


def subjects_dir():
    return os.environ.get(SUBJECTS_ENV) or SUBJECTS_DIR


def read_json(path):
    with io.open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def _known(data, allowed, where, errors):
    """Report keys outside `allowed`. A `<key>_why` beside a known key is a comment."""
    for key in data:
        if key in allowed:
            continue
        if key.endswith("_why") and key[:-4] in allowed:
            continue
        errors.append("%s: unknown key %r" % (where, key))


def _strings(value, where, errors, allow_empty=True):
    if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
        errors.append("%s must be a list of non-empty strings" % where)
        return False
    if not allow_empty and not value:
        errors.append("%s must not be empty" % where)
        return False
    return True


def _recipe(name, spec, where, errors):
    if not isinstance(spec, dict):
        errors.append("%s: recipe %r must be an object" % (where, name))
        return
    _known(spec, RECIPE_KEYS, "%s.%s" % (where, name), errors)
    if ("glob" in spec) == ("file" in spec):
        errors.append("%s.%s: give exactly one of `glob` or `file`" % (where, name))
    capture = spec.get("capture")
    if capture not in CAPTURES:
        errors.append("%s.%s: capture %r is not one of %s"
                      % (where, name, capture, ", ".join(CAPTURES)))
    for need in CAPTURE_NEEDS.get(capture, ()):
        if need not in spec:
            errors.append("%s.%s: capture %s needs `%s`" % (where, name, capture, need))
    if not isinstance(spec.get("why"), str) or not spec.get("why", "").strip():
        errors.append("%s.%s: `why` must say which claim this recipe settles" % (where, name))
    pattern = spec.get("name_pattern")
    if pattern is not None:
        try:
            re.compile(pattern)
        except re.error as exc:
            errors.append("%s.%s: name_pattern does not compile: %s" % (where, name, exc))


def _extract(data, has_sources, errors):
    where = "extract"
    if not isinstance(data, dict):
        errors.append("extract must be an object")
        return
    _known(data, EXTRACT_KEYS, where, errors)
    recipes = data.get("recipes", {})
    if not isinstance(recipes, dict):
        errors.append("extract.recipes must be an object")
        recipes = {}
    if has_sources and not recipes:
        errors.append("extract.recipes is empty, but the subject names a source: a source "
                      "nothing reads is a claim nothing checks")
    if not has_sources and recipes:
        errors.append("extract.recipes needs a source to run against; `sources` is empty")
    for name, spec in sorted(recipes.items()):
        _recipe(name, spec, "extract.recipes", errors)
    version = data.get("version")
    if version is not None:
        if (not isinstance(version, dict) or not {"file", "field"} <= set(version)
                or set(version) - {"file", "field", "docs_var"}):
            errors.append("extract.version must be {\"file\": ..., \"field\": ...}, with an "
                          "optional \"docs_var\"")
        elif "docs_var" in version and not (isinstance(version["docs_var"], str)
                                            and VAR_RE.match(version["docs_var"])):
            errors.append("extract.version.docs_var must be a variable name from vars.yaml")
    for key in ("symbol_prefixes", "coverage_ignore_prefixes", "historical_pages"):
        if key in data:
            _strings(data[key], "extract." + key, errors)
    for key in ("documented_sets", "coverage_sets"):
        if key in data and _strings(data[key], "extract." + key, errors):
            for set_name in data[key]:
                if set_name not in recipes:
                    errors.append("extract.%s names %r, which is not a recipe"
                                  % (key, set_name))
    imap = data.get("interface_map")
    if imap is not None:
        if not isinstance(imap, dict) or imap.get("tabs") not in recipes:
            errors.append("extract.interface_map.tabs must name a recipe")
        elif not isinstance(imap.get("explicit_pages", {}), dict):
            errors.append("extract.interface_map.explicit_pages must be an object")


def validate(data, name=None):
    """Every way `data` breaks the schema, as a list of messages. Empty means valid.

    `name` is the file's stem; the subject's own `name` must match it, because tools find a
    subject by file name and report it by the name inside."""
    errors = []
    if not isinstance(data, dict):
        return ["a subject file must hold one JSON object"]
    _known(data, TOP_KEYS, "subject", errors)
    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append("missing required key %r" % key)
    if errors and any(e.startswith("missing") for e in errors):
        return errors

    if not isinstance(data["name"], str) or not NAME_RE.match(data["name"]):
        errors.append("name must be lowercase letters, digits and hyphens")
    elif name is not None and data["name"] != name:
        errors.append("name %r does not match the file name %r" % (data["name"], name))
    if data["kind"] not in KINDS:
        errors.append("kind must be one of %s" % ", ".join(KINDS))
    for key in ("product_name", "short_name"):
        value = data[key]
        if value is not None and (not isinstance(value, str) or not value.strip()):
            errors.append("%s must be a non-empty string or null" % key)
    if data["audience"] is not None and (
            not isinstance(data["audience"], str) or not data["audience"].strip()):
        errors.append("audience must be one non-empty sentence, or null")
    _strings(data["docs_paths"], "docs_paths", errors)

    sources = data["sources"]
    if not isinstance(sources, list):
        errors.append("sources must be a list")
        sources = []
    for i, src in enumerate(sources):
        where = "sources[%d]" % i
        if not isinstance(src, dict):
            errors.append("%s must be an object" % where)
            continue
        _known(src, SOURCE_KEYS, where, errors)
        for key in ("owner", "repo"):
            if not isinstance(src.get(key), str) or not src.get(key, "").strip():
                errors.append("%s.%s is required" % (where, key))
        for key in ("ref", "root"):
            if src.get(key) is not None and not isinstance(src.get(key), str):
                errors.append("%s.%s must be a string" % (where, key))

    _extract(data["extract"], bool(sources), errors)

    terms = data["terminology"]
    if not isinstance(terms, list):
        errors.append("terminology must be a list")
        terms = []
    for i, term in enumerate(terms):
        where = "terminology[%d]" % i
        if not isinstance(term, dict):
            errors.append("%s must be an object" % where)
            continue
        _known(term, TERM_KEYS, where, errors)
        if not isinstance(term.get("use"), str) or not term.get("use", "").strip():
            errors.append("%s.use is required" % where)
        if "reject" in term:
            _strings(term["reject"], where + ".reject", errors, allow_empty=False)

    _strings(data["must_exist"], "must_exist", errors)
    _strings(data["must_not_exist"], "must_not_exist", errors)
    if data["must_exist"] and not sources:
        errors.append("must_exist needs a source to check the names against")
    overlap = set(data["must_exist"] or []) & set(data["must_not_exist"] or [])
    if overlap:
        errors.append("must_exist and must_not_exist both name %s" % ", ".join(sorted(overlap)))

    decisions = data["decisions"]
    if not isinstance(decisions, list):
        errors.append("decisions must be a list")
        decisions = []
    for i, dec in enumerate(decisions):
        where = "decisions[%d]" % i
        if not isinstance(dec, dict):
            errors.append("%s must be an object" % where)
            continue
        _known(dec, DECISION_KEYS, where, errors)
        if not isinstance(dec.get("decision"), str) or not dec.get("decision", "").strip():
            errors.append("%s.decision is required" % where)
        if not isinstance(dec.get("date"), str) or not DATE_RE.match(dec.get("date", "")):
            errors.append("%s.date must be YYYY-MM-DD" % where)
        if not isinstance(dec.get("by"), str) or not dec.get("by", "").strip():
            errors.append("%s.by must say who decided, or that it was not recorded" % where)
        if dec.get("about") is not None and dec.get("about") not in NULLABLE:
            errors.append("%s.about must be one of %s" % (where, ", ".join(NULLABLE)))
    evidence = data.get("evidence")
    questions = evidence.get("open_questions", []) if isinstance(evidence, dict) else []
    for key in ("product_name", "audience"):
        if data[key] is not None:
            continue
        decided = any(isinstance(d, dict) and d.get("about") == key for d in decisions)
        asked = any(isinstance(q, str) and q.startswith(key + ":") for q in questions)
        if not (decided or asked):
            errors.append("%s is null, so a decision with \"about\": \"%s\" or an "
                          "evidence.open_questions entry starting \"%s:\" must say why"
                          % (key, key, key))

    if evidence is not None:
        if not isinstance(evidence, dict):
            errors.append("evidence must be an object")
        else:
            _known(evidence, EVIDENCE_KEYS, "evidence", errors)
            if "owner" not in evidence:
                errors.append("evidence.owner is required (null when nobody is named yet)")
            elif evidence["owner"] is not None and (
                    not isinstance(evidence["owner"], str) or not evidence["owner"].strip()):
                errors.append("evidence.owner must be a name or null")
            for key in ("proof", "source_does_not_settle", "open_questions"):
                if key in evidence:
                    _strings(evidence[key], "evidence." + key, errors)
    if not sources:
        if not isinstance(evidence, dict) or not evidence.get("proof"):
            errors.append("a subject with no source needs evidence.proof: what counts as "
                          "proof when no code can settle a claim")

    if "capture" in data:
        # Screenshot capture settings (WP7); references/capture.md describes them.
        errors.extend(capture_errors(data["capture"]))
        if not sources and isinstance(data["capture"], dict) and data["capture"].get("surfaces"):
            errors.append("capture.surfaces needs a source: its globs decide when a shot is stale")
    return errors


def capture_errors(cap, where="capture"):
    """Every problem with a subject's `capture` object; [] when it is usable. Lives here,
    not in shots.py, so the public bundle (which ships this file) never needs the tools that
    read private source; every capture run applies the same rules through shots.py."""
    if not isinstance(cap, dict):
        return ["%s must be an object" % where]
    errors = []

    def strings(value, name, allow_empty=False):
        if not isinstance(value, list) or (not value and not allow_empty) or not all(
                isinstance(s, str) and s.strip() for s in value):
            errors.append("%s.%s must be a list of non-empty strings" % (where, name))

    base = cap.get("base_url")
    if not isinstance(base, str) or not re.match(r"^https://[^/\s]+|^http://(127\.0\.0\.1|localhost)(:\d+)?", base or ""):
        errors.append("%s.base_url must be an https URL (or http on localhost, for a fixture)" % where)
    fixture = cap.get("fixture")
    if not isinstance(fixture, dict):
        errors.append("%s.fixture is missing" % where)
    else:
        for key in ("character", "lookup_route"):
            if not isinstance(fixture.get(key), str) or not fixture[key].strip():
                errors.append("%s.fixture.%s must be a non-empty string" % (where, key))
        if "workspace" in fixture and not (isinstance(fixture["workspace"], str) and fixture["workspace"]):
            errors.append("%s.fixture.workspace, when given, must be a non-empty string" % where)
        # Each list the fixture rule reads: a GET endpoint of the product and the keys it uses.
        for part, keys, optional in (("workspaces", ("endpoint", "list", "name"), ()),
                                     ("characters", ("endpoint", "list", "name", "id"), ("total",)),
                                     ("account", ("endpoint",), ())):
            spec = fixture.get(part)
            if not isinstance(spec, dict):
                errors.append("%s.fixture.%s is missing" % (where, part))
                continue
            for key in keys + tuple(k for k in optional if k in spec):
                if not isinstance(spec.get(key), str) or not spec[key].strip():
                    errors.append("%s.fixture.%s.%s must be a non-empty string" % (where, part, key))
            if isinstance(spec.get("endpoint"), str) and not spec["endpoint"].startswith("/"):
                errors.append("%s.fixture.%s.endpoint must be a path that starts with /" % (where, part))
        account = fixture.get("account")
        if isinstance(account, dict):
            strings(account.get("names"), "fixture.account.names")
    identity = cap.get("identity")
    if not isinstance(identity, dict):
        errors.append("%s.identity is missing" % where)
    else:
        strings(identity.get("account"), "identity.account")
        strings(identity.get("workspace", []), "identity.workspace", allow_empty=True)
        strings(identity.get("workspace_items", []), "identity.workspace_items", allow_empty=True)
    strings(cap.get("masks", []), "masks", allow_empty=True)
    storage = cap.get("local_storage", {})
    if not isinstance(storage, dict) or not all(
            isinstance(k, str) and k and isinstance(v, str) for k, v in storage.items()):
        errors.append("%s.local_storage must map names to string values" % where)
    if not CAPTURE_COLOR_RE.match(str(cap.get("mask_color", ""))):
        errors.append("%s.mask_color must be a #rrggbb colour" % where)
    allow = cap.get("allow_post", [])
    if not isinstance(allow, list) or not all(
            isinstance(a, dict) and isinstance(a.get("url"), str) and a["url"].strip()
            and isinstance(a.get("why"), str) and a["why"].strip() for a in allow):
        errors.append("%s.allow_post must be a list of {url, why}" % where)
    surfaces = cap.get("surfaces")
    if not isinstance(surfaces, dict) or not surfaces:
        errors.append("%s.surfaces must name at least one surface" % where)
    else:
        for name, spec in sorted(surfaces.items()):
            if not CAPTURE_ID_RE.match(name):
                errors.append("%s.surfaces: %r is not a kebab-case id" % (where, name))
            if not isinstance(spec, dict):
                errors.append("%s.surfaces.%s must be an object" % (where, name))
                continue
            strings(spec.get("sources"), "surfaces.%s.sources" % name)
    return errors

def capture_covers(rel, directory=None, subject=None):
    """The subject whose screenshot capture covers a page, or None.

    A page is covered when its subject has a `capture` object: `subject` when one is given,
    otherwise the subject one of whose `docs_paths` holds the page. A subject that cannot be
    read covers nothing here; `subjects.py validate` is where it fails."""
    for name in ([subject] if subject else names(directory)):
        path = os.path.join(directory, name + ".json") if directory else name
        try:
            data = load(path)
        except SubjectError:
            continue
        if "capture" not in data:
            continue
        paths = [str(p).strip("/") for p in data.get("docs_paths", [])]
        if subject or any(p and (rel == p or rel.startswith(p + "/")) for p in paths):
            return name
    return None


def path_for(name_or_path):
    """A subject name or a path to a subject file -> the file's path."""
    if name_or_path.endswith(".json") or os.sep in name_or_path or "/" in name_or_path:
        return os.path.abspath(name_or_path)
    shipped = os.path.join(subjects_dir(), name_or_path + ".json")
    created = os.path.join(SUBJECT_CACHE, name_or_path + ".json")
    if not os.path.isfile(shipped) and os.path.isfile(created):
        return created
    return shipped


def load(name_or_path):
    """The validated subject. Raises SubjectError naming every problem at once."""
    path = path_for(name_or_path)
    if not os.path.isfile(path):
        raise SubjectError("no subject file at %s. Create one with new_subject.py; a "
                           "subject is never written by hand from memory." % path)
    try:
        data = read_json(path)
    except ValueError as exc:
        raise SubjectError("%s is not valid JSON: %s" % (path, exc))
    stem = os.path.splitext(os.path.basename(path))[0]
    errors = validate(data, stem)
    if errors:
        raise SubjectError("%s:\n  %s" % (path, "\n  ".join(errors)))
    data["_path"] = path
    return data


def names(directory=None):
    directory = directory or subjects_dir()
    if not os.path.isdir(directory):
        return []
    return sorted(fn[:-5] for fn in os.listdir(directory)
                  if fn.endswith(".json") and not fn.startswith("_"))


def all_subjects(directory=None):
    """{name: subject} for every subject file. A broken file raises: a subject that cannot
    be read must not quietly drop out of every check."""
    directory = directory or subjects_dir()
    return {n: load(os.path.join(directory, n + ".json")) for n in names(directory)}


def contract(subject):
    """The contract-shaped view the extraction and checking tools read.

    `sources[0]` is the repository the recipes run against; any further source is one a
    person verifies by hand and that the source finder can still fetch."""
    if isinstance(subject, str):
        subject = load(subject)
    ex = subject["extract"]
    sources = subject["sources"]
    primary = sources[0] if sources else {}
    out = {
        "subject": subject["name"],
        "kind": subject["kind"],
        "package_root": primary.get("root") or "",
        "extract": ex.get("recipes", {}),
        "must_exist": list(subject["must_exist"]),
        "must_not_exist": list(subject["must_not_exist"]),
        "section": subject["docs_paths"][0] if subject["docs_paths"] else "",
        "docs_paths": list(subject["docs_paths"]),
    }
    if primary:
        out["source_repo"] = primary["repo"]
        out["source_owner"] = primary["owner"]
        if primary.get("ref"):
            out["source_branch"] = primary["ref"]
        related = [{"repo": s["repo"], "owner": s["owner"], "branch": s.get("ref"),
                    "note": s.get("why", "")} for s in sources[1:]]
        if related:
            out["related_repos"] = related
    else:
        out["extractable"] = False
    if ex.get("version"):
        out["version"] = ex["version"]
    for key in ("symbol_prefixes", "documented_sets", "coverage_sets",
                "coverage_ignore_prefixes", "historical_pages", "interface_map"):
        if key in ex:
            out[key] = ex[key]
    if "capture" in subject:
        out["capture"] = subject["capture"]
    return out


def load_contract(name_or_path):
    return contract(load(name_or_path))


def all_contracts(directory=None):
    return {n: contract(s) for n, s in all_subjects(directory).items()}


def rejected_terms(subject):
    """Every variant the subject's terminology rejects, lower-cased. Defined once, in
    site_rules.py, so the bundle's checks and the plugin's agree."""
    sys.path.insert(0, HERE)
    import site_rules  # noqa: E402
    return site_rules.rejected_terms(subject)


def main():
    ap = argparse.ArgumentParser(description="Validate and read subject files.")
    sub = ap.add_subparsers(dest="cmd")
    v = sub.add_parser("validate")
    v.add_argument("subjects", nargs="*")
    sub.add_parser("list")
    c = sub.add_parser("contract")
    c.add_argument("subject")
    args = ap.parse_args()

    if args.cmd == "contract":
        try:
            json.dump(load_contract(args.subject), sys.stdout, indent=2, ensure_ascii=False)
        except SubjectError as exc:
            print("error: %s" % exc, file=sys.stderr)
            return 1
        sys.stdout.write("\n")
        return 0
    if args.cmd == "list":
        for name, s in sorted(all_subjects().items()):
            src = s["sources"][0]["repo"] if s["sources"] else "no source"
            print("%-12s %-8s %s" % (name, s["kind"], src))
        return 0
    targets = args.subjects if args.cmd == "validate" and args.subjects else names()
    failed = 0
    for target in targets:
        try:
            load(target)
            print("ok     %s" % target)
        except SubjectError as exc:
            failed += 1
            print("error  %s" % exc)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
