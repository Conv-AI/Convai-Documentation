#!/usr/bin/env python3
"""Whole-repository checks: the failures a single page cannot see.

`check_page.py` reads one page at a time, so there is a class of real defect it is
structurally blind to. A link is only broken relative to a repository. A page is only an
orphan relative to a navigation tree. Two titles only collide relative to each other. These
are the failures readers hit most and reviewers catch least, because catching them by hand
means holding 692 pages in your head.

Everything here is deterministic. Nothing here judges writing.

    broken-link        a relative link whose target file does not exist
    cross-space-link   a relative link into another space's directory
    missing-image      an image whose file is not in the repository, or not in its space
    orphan             a page nothing links to and the sidebar does not list
    summary-dangling   a sidebar entry whose page does not exist
    summary-label      a sidebar label that does not match the page title
    duplicate-title    two pages in the same section (or space) claiming the same title
    duplicate-desc     two pages claiming the same description
    forbidden-symbol   a name a subject says must never appear
    stale-review       a version-sensitive page whose last_reviewed is behind

    noindex           `noIndex: true` on a hub, or on a page the allow-list does not name
    missing-icon       a top-level or hub page with no `icon`
    icon-not-allowed   an icon outside the space's allowed list
    retired-path       a file under a section that was retired
    redirect-target    a `.gitbook.yaml` redirect pointing at nothing
    hidden pages       not a finding: listed on every run, because agents still read them

  With --base REF, also the checks that only make sense for a change:

    empty-alt          an image with empty alt text on a page this change touches
    generic-image-name an image this change adds under a name like `image (19).png`
    missing-redirect   a page this change removes or moves, with no redirect for its URL

## Repositories with several spaces

When the root holds `gitbook-docs.yaml`, each mapped directory is a GitBook space (see
`spaces.py`). A relative link that leaves its space is reported as `cross-space-link` and an
image outside its space as `missing-image`, because GitBook publishes each space on its own;
links between spaces are absolute site URLs. Each space's own `SUMMARY.md` is checked, and titles are unique per space.
A repository without that file is checked exactly as before.

## Adopting this on a repository that predates it

A checker that reports 400 findings on its first run gets ignored, and then it is worse than
no checker, because it looks like a gate. So the first run writes a baseline: everything it
found is recorded as known. After that only *new* findings are reported, and the baseline
shrinks as the backlog is worked through. Nothing is silently forgiven — `--show-baseline`
prints the whole backlog whenever someone wants to see the real number.

Usage:
    python check_site.py <docs-root> [--index index.json] [--baseline FILE]
                         [--write-baseline] [--show-baseline] [--json] [--strict]
                         [--forbidden NAME ...] [--base REF]

Exit code 0 when there are no new ERROR findings, 1 otherwise. WARN findings fail the run
only with --strict.
"""

import argparse
import fnmatch
import io
import json
import os
import posixpath
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_index  # noqa: E402
import site_rules  # noqa: E402
import spaces  # noqa: E402

# Findings that break the published site are errors; the rest advise.
ERROR_KINDS = {"broken-link", "cross-space-link", "summary-dangling", "missing-image",
               "forbidden-symbol"}

RULE_OF_KIND = {
    "broken-link": "CV-85",
    "cross-space-link": "CV-87",
    "missing-image": "CV-86",
    "orphan": "CV-37",
    "summary-dangling": "CV-37",
    "summary-label": "CV-38",
    "duplicate-title": "CV-91",
    "duplicate-desc": "CV-34",
    "forbidden-symbol": "CV-12",
    "stale-review": "CV-35",
}


def _subject_entries(directory):
    """The public part of each subject (site_rules.py). Without `directory`: the subject files
    shipped with the plugin, or, in the public bundle that carries none because they describe
    private repositories, the `site-rules.json` generated from them."""
    return site_rules.entries(directory).values()


def forbidden_from_subjects(directory=None):
    """Collect every `must_not_exist` name the subjects declare.

    The never-use list belongs to the subject that knows why the name is wrong, not to a
    command-line flag someone has to remember. `ConvaiNPC` reached two published pages while
    the only thing guarding it was a sentence in a Markdown file."""
    names = set()
    for data in _subject_entries(directory):
        names.update(data.get("must_not_exist") or [])
    return names


def historical_from_subjects(directory=None):
    """Collect the `extract.historical_pages` globs the subjects declare.

    A subject can override the defaults - a repository that keeps its migration guides under
    `upgrading/` rather than `migrate-*.md` says so once, in its subject file, instead of
    teaching every tool separately. When no subject declares any, the defaults stand."""
    patterns = set()
    for data in _subject_entries(directory):
        patterns.update(data.get(site_rules.HISTORICAL) or [])
    return sorted(patterns) or list(DEFAULT_HISTORICAL_PAGES)


def is_historical(page_path, patterns):
    """Match the way diff_surface.py matches, including the leading-slash form, so the two
    tools agree on which pages are allowed to name a retired symbol."""
    path = page_path.split(":")[0].replace("\\", "/")
    return any(fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch("/" + path, pattern)
               for pattern in patterns)


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


# Pages whose job is to say what a release changed. A retired name on one of these is the
# point of the page, not drift: a migration table that cannot name the symbol it is telling
# you to replace is useless. `diff_surface.py` has always honoured this; this checker did not,
# so a correct migration guide failed CV-12 with no legitimate way to record the exception.
# Kept identical to diff_surface.py's list so one subject cannot mean two different things.
DEFAULT_HISTORICAL_PAGES = [
    "**/release-notes.md",
    "**/changelog.md",
    "**/migrate-*.md",
    "**/migration-*.md",
    "**/migration-guide/**",
    "**/upgrade-*.md",
]

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


def check(index, root, forbidden=(), retiring=(), historical=(), changes=None):
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
            if resolved is None:
                continue
            left = spaces.leaves_space(index, rel, resolved)
            if left:
                # GitBook publishes each space on its own, so a relative path into another
                # space's directory has nothing to resolve against on the site.
                findings.append(Finding(
                    "cross-space-link", rel, "%s leaves space %r; link to it with its absolute "
                    "site URL" % (link["target"], left), link["line"]))
                continue
            if resolved.startswith(".."):
                continue
            if not target_exists(resolved):
                findings.append(Finding("broken-link", rel, link["target"], link["line"]))

        for img in page["images"]:
            src = img["src"]
            if src.startswith(("http://", "https://", "data:")):
                continue
            resolved = resolve(rel, src)
            left = spaces.leaves_space(index, rel, resolved) if resolved else None
            if left:
                findings.append(Finding(
                    "missing-image", rel, "%s is outside space %r; assets are not shared "
                    "between spaces" % (src, left), img["line"]))
            elif resolved and not resolved.startswith("..") and resolved not in files:
                findings.append(Finding("missing-image", rel, src, img["line"]))

        for name in forbidden:
            if name in page["symbols"]:
                # One finding per page, on the first line: the fix is to the page.
                findings.append(Finding("forbidden-symbol", rel, name, page["symbols"][name][0]))

    # One navigation tree per space; a single-root index has the one root SUMMARY.md.
    trees = [tree for tree in spaces.summaries(index) if tree[1] is not None]
    if trees:
        linked = set()
        for rel, page in pages.items():
            for link in page["links"]:
                resolved = resolve(rel, link["target"])
                if resolved:
                    linked.add(resolved)
                    linked.add(resolved + ".md")

        summary_targets = set()
        for summary_file, summary, space in trees:
            for target, label in sorted(summary.items()):
                normalised = posixpath.normpath(target)
                summary_targets.add(normalised)
                left = space and spaces.leaves_space(index, summary_file, normalised)
                if left:
                    findings.append(Finding("summary-dangling", summary_file,
                                            "%s (label %r) leaves space %r"
                                            % (target, label, left)))
                elif normalised in pages:
                    title = pages[normalised]["title"]
                    if title and title != label:
                        findings.append(Finding(
                            "summary-label", normalised,
                            "sidebar says %r, page title is %r" % (label, title)))
                elif not target_exists(normalised):
                    findings.append(Finding("summary-dangling", summary_file,
                                            "%s (label %r)" % (target, label)))

        for rel in sorted(pages):
            if rel in summary_targets or rel in linked:
                continue
            if os.path.basename(rel) == "README.md":
                # A folder index is reached through its folder, not by its own filename.
                continue
            space = spaces.page_space(index, rel)
            if space is not None and space.get("summary") is None:
                # GitBook builds a space's sidebar from its folders when it has no SUMMARY.md.
                continue
            findings.append(Finding("orphan", rel, "not in SUMMARY.md and nothing links to it"))

    # A title is a name within its context, and the context a reader sees first is the
    # sidebar parent. `Event system` under Unity and `Event system` under Unreal is not
    # ambiguous to anyone reading; the two SDK sections mirror each other deliberately.
    # Two pages with the same title *inside one section* is still a real problem. In a
    # multi-space repository the space is that context, so a title is unique per space.
    for title, where in sorted(index["titles"].items()):
        if len(where) < 2:
            continue
        by_section = {}
        for page in where:
            by_section.setdefault(spaces.title_scope(index, page) or top_section(page),
                                  []).append(page)
        # Not `pages`: that name already holds index["pages"], and shadowing it here broke
        # the duplicate-description loop below in a way the type error pointed at the wrong line.
        for section, in_section in sorted(by_section.items()):
            if len(in_section) > 1:
                findings.append(Finding(
                    "duplicate-title", in_section[0],
                    "%r also used by %s, in the same %s"
                    % (title, ", ".join(in_section[1:]),
                       "space" if section.startswith("space:") else "section")))

    by_description = {}
    for rel, page in sorted(pages.items()):
        desc = (page.get("description") or "").strip()
        if desc:
            by_description.setdefault(desc, []).append(rel)
    for desc, where in sorted(by_description.items()):
        if len(where) > 1:
            findings.append(Finding("duplicate-desc", where[0],
                                    "same description as %s" % ", ".join(where[1:])))

    findings.extend(site_option_findings(index, root, files, changes))

    if retiring:
        for f in findings:
            # Deleting a retiring section is the moment its redirects matter most, so a
            # missing one is never parked with the section's backlog.
            if f.kind == "missing-redirect":
                continue
            if any(f.page.startswith(prefix) for prefix in retiring):
                f.kind = "retiring:" + f.kind
                f.level = "INFO"

    # Only forbidden-symbol is exempt on a historical page. A broken link on a migration
    # guide is still broken; naming the symbol the guide exists to retire is not.
    if historical:
        for f in findings:
            if f.kind == "forbidden-symbol" and is_historical(f.page, historical):
                f.kind = "historical:forbidden-symbol"
                f.level = "INFO"

    return findings


# --- Page options, images, retired sections and redirects (CV-77 to CV-84) ---------------
#
# Kept as one block of functions so it can be read, and merged, on its own. Everything below
# reads the repository's files directly rather than widening the index, so an index.json
# written by an older build_index.py still works with --index.

SITE_OPTION_RULES = {
    "noindex": "CV-77",
    "empty-alt": "CV-79",
    "generic-image-name": "CV-80",
    "missing-icon": "CV-81",
    "icon-not-allowed": "CV-81",
    "retired-path": "CV-82",
    "redirect-target": "CV-83",
    "missing-redirect": "CV-84",
}
HIDDEN_RULE = "CV-78"
# Every one of these breaks something a reader or a search engine sees, so all are errors.
ERROR_KINDS.update(SITE_OPTION_RULES)
RULE_OF_KIND.update(SITE_OPTION_RULES)

NOINDEX_ALLOW_FILE = ".convai-docs/noindex-allowlist.txt"
RETIRED_FILE = ".convai-docs/retired-sections.txt"
ICONS_FILE = ".convai-docs/icons.json"
GITBOOK_YAML = ".gitbook.yaml"

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".avif")

# The names a file gets when nobody named it: GitBook's upload default (`image (19).png`), the
# operating system's screenshot and snipping defaults, a camera roll, a browser download, a
# paste. Matched against the name without its extension, so `image-tracking-panel.png` and
# `screenshot-settings-window.png` are left alone: those were named by a person.
GENERIC_IMAGE_STEMS = [
    re.compile(r"^(?:image|untitled|unknown|capture|clipboard|download|pasted[ _-]?image)"
               r"(?:[ _-]*(?:\(\d+\)|\d+))*$", re.IGNORECASE),
    re.compile(r"^screen[ _-]?shot[\d ._:()-]*(?:at[\d ._:()-]*)?(?:[ap]m)?[\d ._:()-]*$",
               re.IGNORECASE),
    re.compile(r"^img[ _-]?\d+$", re.IGNORECASE),
    re.compile(r"^\d+$"),
]

MD_IMAGE_WITH_ALT = re.compile(r"!\[([^\]]*)\]\(\s*(<[^>]*>|[^)\s]+)")
HTML_IMG_TAG = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
HTML_ALT = re.compile(r'\balt\s*=\s*"([^"]*)"', re.IGNORECASE)
HTML_SRC = re.compile(r'\bsrc\s*=\s*"([^"]+)"', re.IGNORECASE)
SUMMARY_ENTRY = re.compile(r"^(\s*)[*+-]\s+\[[^\]]*\]\(([^)]+)\)")


def _read_text(root, rel):
    try:
        return build_index.read(os.path.join(root, rel.replace("/", os.sep)))
    except (OSError, UnicodeDecodeError):
        return None


def _truthy(value):
    return str(value or "").strip().strip("'\"").lower() == "true"


def _norm(path):
    path = build_index._clean_target(path).split("#")[0].strip().replace("\\", "/")
    while path.startswith("./"):
        path = path[2:]
    return posixpath.normpath(path) if path else ""


def page_options(root, rel):
    """A page's frontmatter, read from the file. GitBook stores the page options a reader never
    sees - `hidden`, `noIndex`, `icon` - only there."""
    text = _read_text(root, rel)
    return build_index.split_frontmatter(text)[0] if text is not None else {}


def summary_levels(root, summary_file="SUMMARY.md", base=""):
    """Return (top_level, hubs) from SUMMARY.md: the pages listed at the sidebar's first level
    under a group, and the pages that have child pages under them. None without a SUMMARY.md.

    A hub is defined by the sidebar, not by being named README.md: a folder index with nothing
    under it is a leaf to the reader, and that is what they experience. `base` is a space's
    content root, which the space's sidebar targets are relative to."""
    text = _read_text(root, summary_file)
    if text is None:
        return None
    entries = []
    for line in text.split("\n"):
        m = SUMMARY_ENTRY.match(line.expandtabs(4))
        if m:
            target = _norm(m.group(2))
            entries.append((len(m.group(1)), _norm(posixpath.join(base, target)) if base
                            else target))
    top = set(t for indent, t in entries if indent == 0)
    hubs = set()
    for (indent, target), (next_indent, _next) in zip(entries, entries[1:]):
        if next_indent > indent:
            hubs.add(target)
    return top, hubs


def _listed_file(root, rel_file):
    """Non-comment lines of a committed list in the documentation repo."""
    text = _read_text(root, rel_file)
    if text is None:
        return []
    return [line.strip() for line in text.split("\n")
            if line.strip() and not line.strip().startswith("#")]


def noindex_allowlist(root):
    """{page: reason} from `.convai-docs/noindex-allowlist.txt`, one `path: reason` per line.

    The reason is part of the entry. A page hidden from search for a reason nobody wrote down is
    exactly how 13 to 19 November happened, so a bare path does not count as allowed."""
    allowed = {}
    for line in _listed_file(root, NOINDEX_ALLOW_FILE):
        path, _sep, reason = line.partition(":")
        allowed[_norm(path)] = reason.strip()
    return allowed


def retired_prefixes(root):
    """Sections that have been removed and must not come back, from a committed list.

    Not the same as the retiring list: that one holds sections still present and awaiting
    deletion. A section moves from that file to this one in the change that deletes it."""
    return [line.split("#")[0].strip().rstrip("/")
            for line in _listed_file(root, RETIRED_FILE) if line.split("#")[0].strip()]


def allowed_icons(root):
    """{space directory: set of icon names} from `.convai-docs/icons.json`, or None when the
    repository has no list yet. The single-root repository is the space ".". Raises ValueError
    on a file that is not a JSON object of lists, so a typo cannot switch the check off."""
    path = os.path.join(root, ICONS_FILE.replace("/", os.sep))
    if not os.path.exists(path):
        return None
    with io.open(path, encoding="utf-8-sig") as f:
        data = json.load(f)
    if not isinstance(data, dict) or not all(isinstance(v, list) for v in data.values()):
        raise ValueError("%s must map each space directory to a list of icon names" % ICONS_FILE)
    return dict((_norm(k) or ".", set(v)) for k, v in data.items())


def _space_of(rel, spaces):
    best = None
    for space in spaces:
        if space == "." or rel == space or rel.startswith(space + "/"):
            if best is None or best == "." or len(space) > len(best):
                best = space
    return best


def url_path(rel):
    """The URL path GitBook serves a page file at, relative to its space: the file path without
    `.md`, and a folder's README at the folder itself."""
    rel = _norm(rel)
    if rel.endswith(".md"):
        rel = rel[:-3]
    if rel == "README":
        return ""
    if rel.endswith("/README"):
        return rel[:-len("/README")]
    return rel


def is_page_path(rel):
    """Whether a repository path is a documentation page, by the same rules build_index walks."""
    parts = rel.split("/")
    if not rel.endswith(".md") or parts[-1] == "SUMMARY.md":
        return False
    if any(p in build_index.SKIP_DIRS or p.startswith(".") for p in parts[:-1]):
        return False
    return not (len(parts) == 1 and parts[0] in build_index.NON_PAGE_FILES)


def empty_alt_images(text):
    """Yield (line, src) for every image on a page whose alt text is empty or absent.

    Both syntaxes, because GitBook writes `<figure><img src alt="">` when an image is uploaded
    and leaves the alt empty unless someone types one."""
    fm_end = build_index.split_frontmatter(text)[1]
    in_code = False
    for offset, raw in enumerate(text.split("\n")[fm_end:]):
        lineno = fm_end + offset + 1
        if build_index.FENCE.match(raw):
            in_code = not in_code
            continue
        if in_code:
            continue
        for m in MD_IMAGE_WITH_ALT.finditer(raw):
            if not m.group(1).strip():
                yield lineno, build_index._clean_target(m.group(2))
        for tag in HTML_IMG_TAG.findall(raw):
            alt = HTML_ALT.search(tag)
            if alt is None or not alt.group(1).strip():
                src = HTML_SRC.search(tag)
                yield lineno, src.group(1) if src else "<img>"


def is_generic_image_name(rel):
    name = posixpath.basename(rel)
    stem, ext = posixpath.splitext(name)
    if ext.lower() not in IMAGE_EXTENSIONS:
        return False
    return any(p.match(stem.strip()) for p in GENERIC_IMAGE_STEMS)


def git_changes(root, base):
    """What this change does relative to `base`, from git: {"pages", "added", "removed"}.

    Compared against the merge base, and against the working tree rather than HEAD, so the same
    call answers for a pull request in CI and for a writer's uncommitted edits on their machine.
    Untracked files count as added. Paths are relative to `root`."""
    def git(*args):
        return subprocess.run(["git", "-C", root] + list(args), check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

    merge_base = git("merge-base", base, "HEAD").decode("utf-8").strip()
    tokens = git("diff", "--name-status", "-z", "-M", "--relative", merge_base).decode("utf-8")
    tokens = tokens.split("\0")
    pages, added, removed = set(), set(), {}
    i = 0
    while i < len(tokens) and tokens[i]:
        status = tokens[i]
        if status[0] in "RC":
            old, new = tokens[i + 1], tokens[i + 2]
            i += 3
            if status[0] == "R":
                removed[old] = new
            added.add(new)
            pages.add(new)
            continue
        path = tokens[i + 1]
        i += 2
        if status[0] == "D":
            removed[path] = None
        else:
            pages.add(path)
            if status[0] == "A":
                added.add(path)
    for path in git("ls-files", "--others", "--exclude-standard", "-z").decode("utf-8").split("\0"):
        if path:
            added.add(path)
            pages.add(path)
    return {"pages": set(p for p in pages if is_page_path(p)), "added": added,
            "removed": dict((k, v) for k, v in removed.items() if is_page_path(k))}


def hidden_pages(index, root):
    """Every page marked `hidden: true`. Hidden takes a page out of the sidebar only: it is still
    served at its URL, still in the space's llms.txt and still read by AI agents, so each run
    lists them and keeping one stays a decision rather than something forgotten (CV-78)."""
    return sorted(rel for rel in index["pages"] if _truthy(page_options(root, rel).get("hidden")))


def site_option_findings(index, root, files, changes=None):
    """CV-77 and CV-79 to CV-84. `changes` is git_changes()'s result, or None for a whole-site
    run, in which case the three checks that are about a change do not run."""
    findings = []
    pages = index["pages"]
    options = dict((rel, page_options(root, rel)) for rel in pages)
    # One sidebar per space; a single-root repository has the one root SUMMARY.md.
    top, hubs = set(), set()
    for summary_file, _entries, space in spaces.summaries(index):
        levels = summary_levels(root, summary_file, space["content_root"] if space else "")
        if levels is not None:
            top |= levels[0]
            hubs |= levels[1]

    allowed = noindex_allowlist(root)
    for rel in sorted(pages):
        if not _truthy(options[rel].get("noIndex")):
            continue
        if posixpath.basename(rel) == "README.md" or rel in hubs:
            findings.append(Finding("noindex", rel, "noIndex on a hub page hides every page "
                                    "reached through it from search; remove it"))
        elif not allowed.get(rel):
            findings.append(Finding("noindex", rel, "noIndex with no reason in %s; add "
                                    "`%s: <reason>` or remove it" % (NOINDEX_ALLOW_FILE, rel)))

    try:
        icons = allowed_icons(root)
    except ValueError as e:
        findings.append(Finding("icon-not-allowed", ICONS_FILE, str(e)))
        icons = None
    for rel in sorted((top | hubs) & set(pages)):
        if _truthy(options[rel].get("hidden")):
            # Out of the sidebar and off every card, so an icon has nowhere to show.
            continue
        icon = (options[rel].get("icon") or "").strip()
        if not icon:
            findings.append(Finding("missing-icon", rel, "top-level and hub pages carry an icon"
                                    if rel in top else "hub page has no icon"))
        elif icons is not None:
            space = _space_of(rel, icons)
            if space is not None and icon not in icons[space]:
                findings.append(Finding("icon-not-allowed", rel, "icon %r is not in the allowed "
                                        "list for space %r in %s" % (icon, space, ICONS_FILE)))

    for prefix in retired_prefixes(root):
        for rel in sorted(files):
            if rel == prefix or rel.startswith(prefix + "/"):
                findings.append(Finding("retired-path", rel,
                                        "under retired section %s/; it must not come back" % prefix))

    # Each space's redirects apply inside that space, relative to its own content root.
    scopes = spaces.redirect_scopes(index, root)
    for scope in scopes:
        content_root = scope["content_root"]
        scope["sources"] = set()
        for source, target, line in scope["redirects"]:
            scope["sources"].add(url_path(source.strip("/")))
            if target.startswith(("http://", "https://")):
                continue
            resolved = _norm(posixpath.join(content_root, target))
            if not any(c in files for c in (resolved, resolved + ".md",
                                            posixpath.join(resolved, "README.md"))):
                findings.append(Finding("redirect-target", scope["file"],
                                        "%s -> %s: no such page" % (source, target), line))

    if changes is not None:
        for rel in sorted(set(changes["pages"]) & set(pages)):
            text = _read_text(root, rel) or ""
            for line, src in empty_alt_images(text):
                findings.append(Finding("empty-alt", rel, "image `%s` has empty alt text" % src,
                                        line))
        for rel in sorted(changes["added"]):
            if is_generic_image_name(rel):
                findings.append(Finding("generic-image-name", rel, "name the file for what it "
                                        "shows, in kebab-case"))

        for scope in scopes:
            content_root = scope["content_root"]

            def space_relative(rel, content_root=content_root, key=scope["key"]):
                if key is not None:
                    owner = spaces.page_space(index, rel)
                    if owner is None or owner["key"] != key:
                        return None
                if content_root in (".", ""):
                    return rel
                return (rel[len(content_root) + 1:] if rel.startswith(content_root + "/")
                        else None)

            served = set(url_path(space_relative(p)) for p in pages
                         if space_relative(p) is not None)
            for old, new in sorted(changes["removed"].items()):
                relative = space_relative(old)
                if relative is None:
                    continue
                path = url_path(relative)
                if path in served or path in scope["sources"]:
                    continue
                findings.append(Finding("missing-redirect", old,
                                        "%s; add a redirect for /%s to %s"
                                        % ("moved to %s" % new if new else "removed", path,
                                           scope["file"])))
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
    ap.add_argument("--subjects",
                    help="Directory of subject files to read never-use lists and historical "
                         "pages from (default: the subjects shipped with the plugin, or "
                         "site-rules.json in the public bundle)")
    ap.add_argument("--base", help="Git ref this change is compared with (a pull request's base "
                                   "branch). Adds the checks that are about a change: alt text "
                                   "on changed pages, names of added images, and redirects for "
                                   "removed or moved pages")
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
        try:
            index = build_index.build(args.root, quiet=True)
        except spaces.SpacesError as e:
            print("error: %s" % e, file=sys.stderr)
            return 2

    forbidden = sorted(set(args.forbidden) | forbidden_from_subjects(args.subjects))
    retiring = retiring_prefixes(args.root)
    historical = historical_from_subjects(args.subjects)
    changes = None
    if args.base:
        if args.write_baseline:
            # A baseline records the site's standing backlog. Change-only findings belong to
            # one pull request and would excuse the next one that repeats them.
            print("--write-baseline records the whole site; run it without --base", file=sys.stderr)
            return 2
        try:
            changes = git_changes(os.path.abspath(args.root), args.base)
        except (OSError, subprocess.CalledProcessError) as e:
            detail = getattr(e, "stderr", b"") or b""
            print("cannot compare with %s: %s %s" % (args.base, e, detail.decode("utf-8", "replace")),
                  file=sys.stderr)
            return 2
    findings = check(index, os.path.abspath(args.root), forbidden=forbidden,
                     retiring=retiring, historical=historical, changes=changes)
    hidden = hidden_pages(index, os.path.abspath(args.root))

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
    retiring_findings = [f for f in findings if f.kind.startswith("retiring:")]
    historical_findings = [f for f in findings if f.kind.startswith("historical:")]

    if args.json:
        json.dump({
            # Named `pages_checked`, not `pages`: check_page.py uses `pages` for a list of
            # per-page results, and one key meaning two things breaks anything reading both.
            "pages_checked": index["page_count"],
            "new": [f.as_dict() for f in new],
            "baselined": len(baselined),
            "errors": len(errors),
            "warnings": len(warns),
            "hidden": hidden,
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
        if hidden:
            print("\nhidden pages  (%d)  %s: out of the sidebar, still served at their URL and "
                  "read by AI agents. Keep each one on purpose, or delete it." % (len(hidden),
                                                                                HIDDEN_RULE))
            for rel in hidden:
                print("  INFO  %-6s %s" % (HIDDEN_RULE, rel))
        print("\n%d page(s) checked. %d new finding(s): %d error(s), %d warning(s)."
              % (index["page_count"], len(new), len(errors), len(warns)))
        if retiring_findings:
            print("%d finding(s) in sections awaiting deletion, not counted. If those sections "
                  "are still here in six months, they are not being retired and this number is "
                  "real work." % len(retiring_findings))
        if historical_findings:
            print("%d retired name(s) left alone on migration and release pages, where naming "
                  "them is the point of the page." % len(historical_findings))
        if not os.path.exists(os.path.join(args.root, ICONS_FILE.replace("/", os.sep))):
            print("No %s yet: top-level and hub pages must carry an icon, but no allowed list "
                  "is checked." % ICONS_FILE)
        if changes is None:
            print("Alt text on changed pages, names of added images and redirects for removed "
                  "pages are checked only with --base.")
        if baselined and not args.show_baseline:
            print("%d known finding(s) held in the baseline. Run --show-baseline to see them."
                  % len(baselined))

    if errors:
        return 1
    return 1 if (args.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
