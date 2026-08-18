#!/usr/bin/env python3
"""Extract a subject's public surface from its source, as data rather than prose.

This is the fix for the one part of a pack that rots on its own. A pack holds four kinds of
thing at four different speeds: naming policy that changes once a year, verification recipes
that change rarely, section layout that belongs to the documentation site, and the actual
names of components and modules, which change every release. Only the last kind rots, and
because it sat in the same hand-written Markdown as the rest, it dragged the credibility of
the whole file down with it. The Unity pack named three components that no longer existed
and was silent about eight feature modules that did.

So the volatile layer stops being prose. `contract.json` says *where* each kind of fact
lives in the source; this tool reads the source and writes `surface.json`. A release
regenerates the surface instead of someone rewriting paragraphs, and `check_pack.py` compares
the prose against it.

The contract is JSON, not YAML, for the same reason nothing here imports a third-party
package: the linter has to run on any machine on the team with nothing installed.

Contract shape:

    {
      "subject": "unity",
      "kind": "sdk",
      "package_root": "Packages/com.convai.convai-sdk-for-unity/",
      "version": {"file": "package.json", "field": "version"},
      "extract": {
        "components": {"glob": "SDK/Runtime/Components/*.cs", "capture": "csharp_type"},
        "modules":    {"glob": "SDK/Modules/*/",              "capture": "dir_name"},
        "assemblies": {"glob": "SDK/Modules/*/*.asmdef",      "capture": "json_field",
                       "field": "name"},
        "menu_paths": {"glob": "SDK/**/*.cs",                 "capture": "attribute",
                       "attribute": "AddComponentMenu"},
        "samples":    {"file": "package.json", "capture": "json_field",
                       "field": "samples[].displayName"}
      },
      "must_exist":     ["ConvaiCharacter"],
      "must_not_exist": ["ConvaiNPC"]
    }

Usage:
    python extract_surface.py <contract.json> --source <sdk-root> [-o surface.json]
"""

import argparse
import fnmatch
import io
import json
import os
import re
import sys

# `public class Foo`, `internal sealed partial class Bar`, plus structs, enums and interfaces.
CSHARP_TYPE = re.compile(
    r"(?m)(?:^|[{;])\s*(?:\[[^\]]*\]\s*)*"
    r"(?:public|internal|protected|private)?\s*"
    r"(?:static\s+|sealed\s+|abstract\s+|partial\s+|readonly\s+|unsafe\s+)*"
    r"(class|struct|interface|enum)\s+([A-Za-z_]\w*)")

# Unity ignores these; so must we, or every type is reported twice.
IGNORED_SUFFIXES = (".meta",)


def read(path):
    with io.open(path, encoding="utf-8-sig", errors="replace") as f:
        return f.read()


def walk_matching(root, pattern):
    """Resolve a contract glob against a source tree.

    Supports `**` for "any depth" and a trailing slash for "directories, not files". Written
    by hand rather than with `glob` because `glob.glob(recursive=True)` only learned some of
    this in 3.5 and the behaviour differs enough between platforms to be worth pinning."""
    want_dirs = pattern.endswith("/")
    pattern = pattern.rstrip("/")
    out = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in sorted(dirnames)
                       if d not in (".git", "obj", "Library", "Temp", "node_modules")]
        rel_dir = os.path.relpath(dirpath, root).replace("\\", "/")
        rel_dir = "" if rel_dir == "." else rel_dir

        if want_dirs:
            for d in dirnames:
                candidate = ("%s/%s" % (rel_dir, d)).lstrip("/")
                if _match(candidate, pattern, None):
                    out.append((candidate, os.path.join(dirpath, d)))
            continue

        for fn in sorted(filenames):
            if fn.endswith(IGNORED_SUFFIXES):
                continue
            candidate = ("%s/%s" % (rel_dir, fn)).lstrip("/")
            if _match(candidate, pattern, None):
                out.append((candidate, os.path.join(dirpath, fn)))
    return out


def _match(candidate, pattern, recursive):
    """Match a path against a contract glob, one path segment at a time.

    `fnmatch` alone is wrong here: its `*` happily matches a `/`, so `SDK/Modules/*` also
    matched `SDK/Modules/Gaze/Components` and reported 54 feature modules where there are
    ten. A pack built on that number would have sent a writer looking for modules that do
    not exist."""
    cand_parts = [p for p in candidate.split("/") if p]
    pat_parts = [p for p in pattern.split("/") if p]
    return _match_parts(cand_parts, pat_parts)


def _match_parts(cand, pat):
    if not pat:
        return not cand
    head = pat[0]
    if head == "**":
        # `**` spans zero or more segments, so try every split point.
        rest = pat[1:]
        for i in range(len(cand) + 1):
            if _match_parts(cand[i:], rest):
                return True
        return False
    if not cand:
        return False
    if not fnmatch.fnmatch(cand[0], head):
        return False
    return _match_parts(cand[1:], pat[1:])


def _json_field(data, field):
    """Read `a.b`, or `list[].name` to collect one key from every element of a list."""
    cur = data
    for part in field.split("."):
        if part.endswith("[]"):
            key = part[:-2]
            cur = cur.get(key, []) if isinstance(cur, dict) else []
            return cur
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
        if cur is None:
            return None
    return cur


def capture_from(path, rel, spec):
    kind = spec.get("capture", "file_name")

    if kind == "dir_name":
        return [os.path.basename(rel)]

    if kind == "file_name":
        return [os.path.splitext(os.path.basename(rel))[0]]

    if kind == "csharp_type":
        # A partial class spread over several files must be counted once, and the file name
        # is not the type name: `ConvaiCharacter.Actions.cs` declares `ConvaiCharacter`.
        return [m.group(2) for m in CSHARP_TYPE.finditer(read(path))]

    if kind == "attributed_type":
        # The type an attribute decorates. `[AddComponentMenu(...)]` is the only mechanical
        # marker of "a reader can add this in the Inspector", which is what makes a type
        # part of the documented surface rather than an internal helper.
        name = spec["attribute"]
        pattern = re.compile(
            r"\[\s*%s\s*\([^)]*\)\s*\]"
            r"(?:\s*\[[^\]]*\])*"
            r"[\s\S]{0,200}?\bclass\s+([A-Za-z_]\w*)" % re.escape(name))
        return [m.group(1) for m in pattern.finditer(read(path))]

    if kind == "attribute":
        name = spec["attribute"]
        pattern = re.compile(r"\[\s*%s\s*\(\s*\"([^\"]+)\"" % re.escape(name))
        return [m.group(1) for m in pattern.finditer(read(path))]

    if kind == "json_field":
        try:
            data = json.loads(read(path))
        except ValueError:
            return []
        field = spec["field"]
        if "[]" in field:
            list_key, _, leaf = field.partition("[].")
            items = _json_field(data, list_key + "[]") or []
            return [i.get(leaf) for i in items if isinstance(i, dict) and i.get(leaf)]
        value = _json_field(data, field)
        if isinstance(value, dict):
            return sorted(value.keys())
        if isinstance(value, list):
            return [v for v in value if isinstance(v, str)]
        return [value] if value else []

    raise ValueError("unknown capture kind %r" % kind)


def extract(contract, source_root):
    base = os.path.join(source_root, contract.get("package_root", "").replace("/", os.sep))
    base = os.path.normpath(base)
    if not os.path.isdir(base):
        raise SystemExit("package root not found: %s" % base)

    surface = {
        "subject": contract["subject"],
        "kind": contract.get("kind", "sdk"),
        "package_root": contract.get("package_root", ""),
        "version": None,
        "sets": {},
        "evidence": {},
    }

    version_spec = contract.get("version")
    if version_spec:
        vpath = os.path.join(base, version_spec["file"].replace("/", os.sep))
        if os.path.exists(vpath):
            values = capture_from(vpath, version_spec["file"],
                                  {"capture": "json_field", "field": version_spec["field"]})
            surface["version"] = values[0] if values else None

    for set_name, spec in sorted(contract.get("extract", {}).items()):
        values = {}
        if "file" in spec:
            path = os.path.join(base, spec["file"].replace("/", os.sep))
            if os.path.exists(path):
                for value in capture_from(path, spec["file"], spec):
                    values.setdefault(value, spec["file"])
        else:
            for rel, path in walk_matching(base, spec["glob"]):
                for value in capture_from(path, rel, spec):
                    values.setdefault(value, rel)
        surface["sets"][set_name] = sorted(values)
        surface["evidence"][set_name] = dict(sorted(values.items()))

    return surface


def main():
    ap = argparse.ArgumentParser(description="Extract a subject's public surface from source.")
    ap.add_argument("contract", help="Path to the pack contract JSON")
    ap.add_argument("--source", required=True,
                    help="Absolute path to the source checkout on this machine")
    ap.add_argument("-o", "--out", help="Where to write surface.json")
    ap.add_argument("--stamp", help="Value to record as `generated_against` (a commit sha)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    contract = json.loads(read(args.contract))
    surface = extract(contract, args.source)
    surface["generated_against"] = args.stamp or "unrecorded"

    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.contract)),
                                   "..", "surfaces", "%s.json" % contract["subject"])
    out = os.path.normpath(out)
    out_dir = os.path.dirname(out)
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(surface, f, indent=2, ensure_ascii=False)
        f.write("\n")

    if not args.quiet:
        print("subject: %s   version: %s" % (surface["subject"], surface["version"]))
        for name in sorted(surface["sets"]):
            print("  %-14s %d" % (name, len(surface["sets"][name])))
        print("wrote %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
