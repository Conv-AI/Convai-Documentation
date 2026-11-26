#!/usr/bin/env python3
"""The space model: which directory of a documentation repository is which GitBook space.

GitBook can sync several spaces from one repository and branch. The mapping lives in
`gitbook-docs.yaml` at the repository root, and each mapped directory is a space of its own,
with its own `.gitbook.yaml`, `SUMMARY.md`, `README.md`, `.gitbook/vars.yaml` and
`.gitbook/assets/`. Nothing is shared between those directories when GitBook publishes them,
so three things a single-root checker takes for granted stop being true:

    a relative link into another space's directory does not resolve on the published site;
      a link between spaces has to be the target's absolute site URL
    an image in another space's assets folder is not served with this space
    a title only has to be unique inside its own space, because the space is what a reader
      sees as one product

This module reads the mapping and answers the questions the tools ask about it. The tools
call it; none of them parses `gitbook-docs.yaml` itself.

What GitBook documents, and so what this relies on: the mapping file and its `site.structure`
of `space` and `section` entries, `content.directory` per space (`null` for a space not
synced from Git), the `root` and `structure` of each space's `.gitbook.yaml`, that mapped
directories share no content or assets, and that a link to another space is its absolute
URL (https://gitbook.com/docs/docs-as-code/git-sync/monorepos,
https://gitbook.com/docs/docs-as-code/git-sync/content-configuration).

A repository without `gitbook-docs.yaml` is single-root, and every function here then
behaves so that the tools produce exactly what they produced before spaces existed. In
particular a single-root repository's own `.gitbook.yaml` is not read: honouring its `root`
would move every page path in the index, and single-root results must not change.

The file is YAML. The tools stay standard-library Python, so this reads the subset GitBook
writes (block mappings, block lists, plain and quoted scalars, block scalars, comments) and
refuses anything else by line number rather than guessing.

Usage:
    python spaces.py <docs-root>        print the spaces the tools will see
"""

import io
import os
import posixpath
import re
import sys

CONFIG_FILE = "gitbook-docs.yaml"
SPACE_CONFIG = ".gitbook.yaml"


class SpacesError(ValueError):
    """`gitbook-docs.yaml` or a space's `.gitbook.yaml` cannot be read as a space mapping.

    The tools stop on this rather than fall back to single-root, because checking a
    multi-space repository as one root reports every link between spaces as fine."""


# --- a YAML subset ------------------------------------------------------------------

_KEY = re.compile(r"^([^\s#'\"][^:#]*?|'[^']*'|\"[^\"]*\")\s*:(?:\s+(.*))?$")


def _strip_comment(text):
    """Drop a trailing `# comment` that is not inside quotes."""
    quote = None
    for i, ch in enumerate(text):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif ch == "#" and (i == 0 or text[i - 1] in " \t"):
            return text[:i].rstrip()
    return text.rstrip()


def _scalar(raw, lineno, name):
    raw = raw.strip()
    if raw[:1] in "'\"":
        if len(raw) < 2 or raw[-1] != raw[0]:
            raise SpacesError("%s line %d: unterminated quoted value" % (name, lineno))
        body = raw[1:-1]
        return body.replace("''", "'") if raw[0] == "'" else body
    if raw in ("", "~", "null", "Null", "NULL"):
        return None
    if raw in ("true", "True", "TRUE"):
        return True
    if raw in ("false", "False", "FALSE"):
        return False
    if raw in ("[]", "{}"):
        return [] if raw == "[]" else {}
    if raw[:1] in "[{&*!|>":
        raise SpacesError("%s line %d: unsupported YAML value %r; write it as a block"
                          % (name, lineno, raw))
    if re.match(r"^-?\d+$", raw):
        return int(raw)
    return raw


def parse_yaml(text, name="yaml"):
    """Parse the block-style YAML subset GitBook writes. Raises SpacesError otherwise."""
    lines = []
    raw_lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    i = 0
    while i < len(raw_lines):
        raw = raw_lines[i]
        lineno = i + 1
        i += 1
        if "\t" in raw[:len(raw) - len(raw.lstrip())]:
            raise SpacesError("%s line %d: indentation must be spaces" % (name, lineno))
        stripped = _strip_comment(raw)
        if not stripped.strip() or stripped.strip() in ("---", "..."):
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        content = stripped.strip()
        # A block scalar (`key: |` or `key: >`) swallows the more-indented lines after it.
        m = re.match(r"^(.*?:)\s*([|>])[-+]?$", content)
        if m:
            block = []
            while i < len(raw_lines):
                nxt = raw_lines[i]
                if nxt.strip() and len(nxt) - len(nxt.lstrip(" ")) <= indent:
                    break
                block.append(nxt.strip())
                i += 1
            joined = (" " if m.group(2) == ">" else "\n").join(x for x in block if x)
            lines.append((indent, m.group(1), lineno, joined))
            continue
        lines.append((indent, content, lineno, None))

    pos = [0]

    def parse_block(indent):
        if pos[0] >= len(lines):
            return None
        first_indent, first, _, _ = lines[pos[0]]
        if first_indent != indent:
            return None
        if first == "-" or first.startswith("- "):
            return parse_list(indent)
        return parse_map(indent)

    def parse_value(rest, lineno, block_text, indent, allow_same_indent_list):
        if block_text is not None:
            return block_text
        if rest is not None and rest.strip():
            return _scalar(rest, lineno, name)
        if pos[0] < len(lines):
            nxt_indent, nxt, _, _ = lines[pos[0]]
            if nxt_indent > indent:
                return parse_block(nxt_indent)
            if (allow_same_indent_list and nxt_indent == indent
                    and (nxt == "-" or nxt.startswith("- "))):
                return parse_list(indent)
        return None

    def parse_map(indent):
        out = {}
        while pos[0] < len(lines):
            line_indent, content, lineno, block_text = lines[pos[0]]
            if line_indent < indent:
                break
            if line_indent > indent:
                raise SpacesError("%s line %d: unexpected indentation" % (name, lineno))
            if content == "-" or content.startswith("- "):
                break
            m = _KEY.match(content)
            if not m:
                raise SpacesError("%s line %d: expected `key: value`" % (name, lineno))
            key = m.group(1).strip()
            if key[:1] in "'\"":
                key = key[1:-1]
            if key in out:
                raise SpacesError("%s line %d: key %r appears twice" % (name, lineno, key))
            pos[0] += 1
            out[key] = parse_value(m.group(2), lineno, block_text, indent, True)
        return out

    def parse_list(indent):
        out = []
        while pos[0] < len(lines):
            line_indent, content, lineno, block_text = lines[pos[0]]
            if line_indent < indent:
                break
            if line_indent > indent:
                raise SpacesError("%s line %d: unexpected indentation" % (name, lineno))
            if not (content == "-" or content.startswith("- ")):
                break
            rest = content[1:].strip()
            if not rest:
                pos[0] += 1
                out.append(parse_value(None, lineno, None, indent, False))
                continue
            item_indent = indent + (len(content) - len(rest))
            if _KEY.match(rest) or (block_text is not None):
                # `- key: value` opens a mapping whose further keys sit under `key`.
                lines[pos[0]] = (item_indent, rest, lineno, block_text)
                out.append(parse_map(item_indent))
            else:
                pos[0] += 1
                out.append(_scalar(rest, lineno, name))
        return out

    if not lines:
        return {}
    result = parse_block(lines[0][0])
    if pos[0] < len(lines):
        raise SpacesError("%s line %d: unexpected content" % (name, lines[pos[0]][2]))
    return result


def _read_yaml(path, name):
    try:
        with io.open(path, encoding="utf-8-sig") as f:
            return parse_yaml(f.read(), name)
    except (OSError, UnicodeDecodeError) as e:
        raise SpacesError("cannot read %s: %s" % (name, e))


# --- the model ----------------------------------------------------------------------

class Space(object):
    """One space: where it lives in the repository and where its own files are.

    Every path is relative to the documentation root, with forward slashes, and "" for the
    root itself. `content_root` is the directory GitBook reads pages from: the mapped
    directory, moved by the `root` of that directory's `.gitbook.yaml` when it sets one.

    `vars_file` is the space's `.gitbook/vars.yaml` as found on disk, or None. GitBook's
    documentation does not say whether that file sits under `root` or beside
    `.gitbook.yaml` when the two differ, so both places are looked in rather than one assumed."""

    def __init__(self, key, title, path, directory, content_root, summary_file, readme,
                 vars_file=None):
        self.key = key
        self.title = title
        self.path = path
        self.directory = directory
        self.content_root = content_root
        self.summary_file = summary_file
        self.readme = readme
        self.vars_file = vars_file

    def contains(self, rel_path):
        """True when a repository-relative path lies inside this space's directory."""
        return _under(rel_path, self.directory)

    def as_dict(self):
        return {"key": self.key, "title": self.title, "path": self.path,
                "directory": self.directory, "content_root": self.content_root,
                "summary_file": self.summary_file, "readme": self.readme,
                "vars_file": self.vars_file}


def _join(base, rel):
    return posixpath.normpath(posixpath.join(base, rel)) if base else posixpath.normpath(rel)


def _under(rel_path, directory):
    if not directory:
        return not (rel_path == ".." or rel_path.startswith("../"))
    return rel_path == directory or rel_path.startswith(directory + "/")


def _repo_root(start):
    """The nearest folder at or above `start` that holds `.git`, else `start` itself."""
    here = os.path.abspath(start)
    while True:
        if os.path.exists(os.path.join(here, ".git")):
            return here
        parent = os.path.dirname(here)
        if parent == here:
            return os.path.abspath(start)
        here = parent


def _directory(root, raw, key):
    """Resolve a `content.directory` the way GitBook does, relative to the docs root.

    `./docs` and `docs` are inside the project directory (where gitbook-docs.yaml is);
    `/docs` is from the repository root."""
    if not isinstance(raw, str) or not raw.strip():
        raise SpacesError("space %r: content.directory must be a path or null" % key)
    raw = raw.strip().replace("\\", "/")
    if raw.startswith("/"):
        repo = _repo_root(root)
        absolute = os.path.normpath(os.path.join(repo, raw.lstrip("/")))
        rel = os.path.relpath(absolute, os.path.abspath(root)).replace("\\", "/")
    else:
        rel = posixpath.normpath(raw)
    if rel == ".":
        rel = ""
    if rel == ".." or rel.startswith("../"):
        raise SpacesError("space %r maps to %r, outside %s; run the tools on the directory "
                          "that holds %s" % (key, raw, root, CONFIG_FILE))
    return rel


def _space_settings(root, directory, key):
    """Read `root` and `structure` from a space's own `.gitbook.yaml`, if it has one."""
    path = os.path.join(root, *([directory] if directory else []) + [SPACE_CONFIG])
    if not os.path.exists(path):
        return "", "SUMMARY.md", "README.md"
    name = _join(directory, SPACE_CONFIG)
    data = _read_yaml(path, name) or {}
    if not isinstance(data, dict):
        raise SpacesError("%s: expected a mapping" % name)
    content = data.get("root") or "./"
    structure = data.get("structure") or {}
    if not isinstance(content, str) or not isinstance(structure, dict):
        raise SpacesError("%s: `root` must be a path and `structure` a mapping" % name)
    content = posixpath.normpath(content.replace("\\", "/").strip())
    if content == ".":
        content = ""
    if content == ".." or content.startswith("../") or content.startswith("/"):
        raise SpacesError("%s: root %r leaves the space's directory" % (name, data.get("root")))
    return (content, structure.get("summary") or "SUMMARY.md",
            structure.get("readme") or "README.md")


def _walk_structure(items, root, out, where):
    if items is None:
        return
    if not isinstance(items, list):
        raise SpacesError("%s: `structure` must be a list" % where)
    for item in items:
        if not isinstance(item, dict):
            raise SpacesError("%s: every structure entry must be a mapping" % where)
        kind = item.get("type")
        key = item.get("key")
        if kind == "section":
            _walk_structure(item.get("children"), root, out, "section %r" % key)
            continue
        if kind != "space":
            raise SpacesError("%s: entry %r has type %r; expected space or section"
                              % (where, key, kind))
        if not isinstance(key, str) or not key:
            raise SpacesError("%s: a space has no key" % where)
        content = item.get("content") or {}
        if not isinstance(content, dict):
            raise SpacesError("space %r: `content` must be a mapping" % key)
        if content.get("directory") is None:
            # A space that is not synced from this repository: nothing here to check.
            continue
        directory = _directory(root, content.get("directory"), key)
        content_rel, summary, readme = _space_settings(root, directory, key)
        content_root = _join(directory, content_rel) if (directory or content_rel) else ""
        if content_root == ".":
            content_root = ""
        vars_file = None
        for base in (content_root, directory):
            candidate = _join(base, ".gitbook/vars.yaml")
            if os.path.isfile(os.path.join(root, *candidate.split("/"))):
                vars_file = candidate
                break
        out.append(Space(key=key, title=item.get("title") or key, path=item.get("path") or "",
                         directory=directory, content_root=content_root,
                         summary_file=_join(content_root, summary),
                         readme=_join(content_root, readme), vars_file=vars_file))


def load(root):
    """Return the spaces `gitbook-docs.yaml` maps, or [] for a single-root repository."""
    path = os.path.join(root, CONFIG_FILE)
    if not os.path.exists(path):
        return []
    data = _read_yaml(path, CONFIG_FILE)
    if not isinstance(data, dict) or not isinstance(data.get("site"), dict):
        raise SpacesError("%s: expected a `site:` mapping" % CONFIG_FILE)
    out = []
    _walk_structure(data["site"].get("structure"), root, out, CONFIG_FILE)
    if not out:
        raise SpacesError("%s maps no space to a directory of this repository" % CONFIG_FILE)
    seen_keys, seen_dirs = {}, {}
    for space in out:
        if space.key in seen_keys:
            raise SpacesError("%s: space key %r is used twice" % (CONFIG_FILE, space.key))
        if space.directory in seen_dirs:
            raise SpacesError("%s: spaces %r and %r map the same directory %r"
                              % (CONFIG_FILE, seen_dirs[space.directory], space.key,
                                 space.directory or "./"))
        seen_keys[space.key] = True
        seen_dirs[space.directory] = space.key
    return out


def space_of(space_list, rel_path):
    """The space whose directory holds `rel_path` (the deepest one, if they nest)."""
    best = None
    for space in space_list:
        if space.contains(rel_path) and (best is None or len(space.directory) > len(best.directory)):
            best = space
    return best


# --- answers the tools ask, read from an index -----------------------------------------
#
# The index carries the spaces under `index["spaces"]` and each page's key under
# `page["space"]`, and only for a multi-space repository. Everything below returns the
# single-root answer when those keys are absent, so a single-root index needs no change.

def of_index(index):
    """The spaces an index was built with, as {key: dict}; {} when single-root."""
    return index.get("spaces") or {}


def page_space(index, rel_path):
    """The space dict a page belongs to, or None for a single-root index."""
    spaces = of_index(index)
    if not spaces:
        return None
    page = index.get("pages", {}).get(rel_path)
    key = page.get("space") if page else None
    if key in spaces:
        return spaces[key]
    best = None
    for data in spaces.values():
        if _under(rel_path, data["directory"]) and (
                best is None or len(data["directory"]) > len(best["directory"])):
            best = data
    return best


def leaves_space(index, from_page, resolved):
    """The key of the space a relative link from `from_page` to `resolved` leaves, or None.

    `resolved` is repository-relative. Always None for a single-root index."""
    space = page_space(index, from_page)
    if space is None:
        return None
    if _under(resolved, space["directory"]):
        return None
    return space["key"]


def title_scope(index, rel_path):
    """What a title has to be unique within: the page's space, or None for single-root."""
    space = page_space(index, rel_path)
    return "space:" + space["key"] if space else None


def summaries(index):
    """Yield (summary_file, {target: label} or None, space dict or None) per navigation tree.

    A single-root index yields its one root SUMMARY.md, exactly as before."""
    spaces = of_index(index)
    if not spaces:
        yield "SUMMARY.md", index.get("summary"), None
        return
    for key in sorted(spaces):
        data = spaces[key]
        yield data["summary_file"], data.get("summary"), data


def section_prefix(index, key):
    """The page-path prefix of the space `key`, for tools that scope by path."""
    spaces = of_index(index)
    if key not in spaces:
        raise SpacesError("no space %r in this index; spaces: %s"
                          % (key, ", ".join(sorted(spaces)) or "none (single-root)"))
    root = spaces[key]["content_root"]
    return root + "/" if root else ""


def vars_files(index, pages):
    """The vars.yaml files that hold the variables the given pages read.

    For a single-root index this is the one `.gitbook/vars.yaml`. A space with no vars.yaml
    on disk is named as such, because a page there reads a variable nothing defines."""
    spaces = of_index(index)
    if not spaces:
        return [".gitbook/vars.yaml"]
    out = set()
    for rel in pages:
        space = page_space(index, rel)
        if space:
            out.add(space["vars_file"] or "(no vars.yaml in space %r)" % space["key"])
    return sorted(out)


# --- .gitbook.yaml redirects -------------------------------------------------------------

def _norm_path(path):
    path = path.strip().replace("\\", "/")
    if path.startswith("<") and path.endswith(">"):
        path = path[1:-1].strip()
    path = path.split("#")[0].strip()
    while path.startswith("./"):
        path = path[2:]
    return posixpath.normpath(path) if path else ""


def read_gitbook_yaml(root, rel_file=SPACE_CONFIG):
    """The parts of a `.gitbook.yaml` the redirect checks need: the content root and the
    redirects, each with its line. None when the file does not exist.

    Reads the flat shape GitBook documents (`root:` and a `redirects:` block of
    `old/path: new/page.md` lines) line by line, because a redirect finding names its line.
    `root` is returned as written, relative to the file's own directory."""
    path = os.path.join(root, *rel_file.split("/"))
    try:
        with io.open(path, encoding="utf-8-sig") as f:
            text = f.read()
    except (OSError, UnicodeDecodeError):
        return None
    content_root = "."
    redirects = []
    block = None
    for lineno, raw in enumerate(text.split("\n"), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        m = re.match(r"^(\s*)(['\"]?)(.+?)\2\s*:\s*(.*?)\s*$", raw)
        if not m:
            continue
        indent, key, value = m.group(1), m.group(3).strip(), m.group(4)
        if value and value[0] in "'\"":
            value = value[1:].split(value[0])[0]
        else:
            value = value.split(" #")[0].strip()
        if not indent:
            block = key
            if key == "root" and value:
                content_root = _norm_path(value) or "."
        elif block == "redirects" and value:
            redirects.append((key, value, lineno))
    return {"root": content_root, "redirects": redirects}


def redirect_scopes(index, root):
    """One entry per `.gitbook.yaml` whose redirects apply: {"key", "file", "content_root",
    "redirects"}. `content_root` is repository-relative ("." for the repository root) and is
    what redirect targets and served URLs are relative to.

    Single-root: the root `.gitbook.yaml`, read as the redirect checks always read it, with
    its own `root`. Multi-space: each space's `.gitbook.yaml`, relative to that space's
    content root, because GitBook applies a space's redirects inside that space only."""
    spaces = of_index(index)
    if not spaces:
        config = read_gitbook_yaml(root)
        return [{"key": None, "file": SPACE_CONFIG,
                 "content_root": config["root"] if config else ".",
                 "redirects": config["redirects"] if config else []}]
    out = []
    for key in sorted(spaces):
        data = spaces[key]
        rel_file = _join(data["directory"], SPACE_CONFIG)
        config = read_gitbook_yaml(root, rel_file)
        out.append({"key": key, "file": rel_file, "content_root": data["content_root"] or ".",
                    "redirects": config["redirects"] if config else []})
    return out


def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        print("usage: python spaces.py <docs-root>", file=sys.stderr)
        return 2
    try:
        space_list = load(sys.argv[1])
    except SpacesError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    if not space_list:
        print("single-root: no %s, so the whole repository is one space" % CONFIG_FILE)
        return 0
    for space in space_list:
        print("%-16s %-24s directory %s" % (space.key, space.title, space.directory or "./"))
        print("%-16s %-24s summary   %s" % ("", "", space.summary_file))
    return 0


if __name__ == "__main__":
    sys.exit(main())
