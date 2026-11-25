#!/usr/bin/env python3
"""Deterministic structure linter for Convai GitBook documentation pages.

Checks the mechanical, non-judgement rules from the convai-docs writing template:
frontmatter, description length and plain-English wording, body H1, forbidden headings,
lead paragraph, hint count, GitBook block balance, GitBook variable syntax, code-fence
languages, image alt text, publish-blocking TODO placeholders, banned words, hedging
phrases, filler openers, vague headings, "click here" links, and (optionally)
SUMMARY.md reachability + label match.

This is the deterministic half of the quality gate. It does NOT judge writing quality
or technical accuracy — use the docs-reviewer (quality checklist) and docs-verifier
(SDK source accuracy) for those.

The human-readable rule list lives in `references/linter-rules.md`. Keep the two in sync.
The banned-word, hedging and vague-heading lists live in `prose_rules.json` beside this file.

Usage:
    python check_page.py <page.md> [more.md ...] [--summary SUMMARY.md] [--json] [--strict]
                         [--subject <name-or-path>]

Exit code 0 if no ERROR-level findings, 1 otherwise. WARN findings fail the run only
with --strict. Exit code 2 if --subject names no subject file or the file is invalid. In
the public bundle, which carries no subject files, --subject reads the subject's entry in
`site-rules.json` (see site_rules.py).
`--pack` is the 2.6 name of `--subject`, kept until 3.1.
"""

import argparse
import bisect
import json
import os
import re
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
# Banned words (CV-1), hedging phrases (CV-2) and vague headings (CV-28) live in a JSON file,
# so adding a term the team has agreed on is not a code change, and a subject adds the
# variants its terminology rejects. See load_prose_rules.
PROSE_RULES_FILE = os.path.join(TOOLS_DIR, "prose_rules.json")
PROSE_RULE_KEYS = ("banned_words", "hedging_phrases", "vague_headings")

CLOUD_PHRASES = ["convai cloud", "cloud backend", "cloud pipeline", "convai's servers", "convai's cloud"]
DESC_BAD_OPENERS = ["this page covers", "learn about", "overview of"]


def _term_lists(data, where):
    """Return {key: [lowercase terms]} for the PROSE_RULE_KEYS present in `data`."""
    unknown = sorted(set(data) - set(PROSE_RULE_KEYS))
    if unknown:
        raise ValueError("%s: unknown prose rule key(s) %s; expected %s"
                         % (where, ", ".join(unknown), ", ".join(PROSE_RULE_KEYS)))
    out = {}
    for key in PROSE_RULE_KEYS:
        if key not in data:
            continue
        terms = data[key]
        if not isinstance(terms, list) or not all(isinstance(t, str) and t.strip() for t in terms):
            raise ValueError("%s: %s must be a list of non-empty strings" % (where, key))
        out[key] = [t.strip().lower() for t in terms]
    return out


def load_prose_rules(subject=None, defaults_path=PROSE_RULES_FILE):
    """Return the banned words, hedging phrases and vague headings the linter checks.

    The defaults come from prose_rules.json. With `subject` (a name or a path to a subject
    file), every variant the subject's `terminology` rejects is added to the banned words for
    that subject's pages; it can only add, so a subject cannot switch off a rule the whole
    team agreed on. An unknown or invalid subject is an error, because an extension that
    silently extends nothing looks exactly like one that worked."""
    with open(defaults_path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    data = {k: v for k, v in data.items() if not k.startswith("_")}
    rules = _term_lists(data, defaults_path)
    missing = [k for k in PROSE_RULE_KEYS if k not in rules]
    if missing:
        raise ValueError("%s: missing %s" % (defaults_path, ", ".join(missing)))
    if subject:
        sys.path.insert(0, TOOLS_DIR)
        import site_rules  # noqa: E402  (kept local: only --subject needs it)
        is_path = subject.endswith(".json") or "/" in subject or os.sep in subject
        if is_path or os.path.isdir(site_rules.SUBJECTS_DIR):
            # The plugin: validate the subject file itself.
            import subjects  # noqa: E402
            loaded = subjects.load(subject)  # SubjectError is a ValueError
        else:
            # The public bundle carries no subject files, only site-rules.json.
            loaded = site_rules.entry(subject)
        rules["banned_words"] += [t for t in site_rules.rejected_terms(loaded)
                                  if t not in rules["banned_words"] and t not in CLOUD_PHRASES]
    return rules


DEFAULT_PROSE_RULES = load_prose_rules()

# Filler openers — marketing/narrative framing that delays the actual content
FILLER_PHRASES = [
    "in this guide, we will",
    "in this page, we will",
    "in this section, we will",
    "in this tutorial, we will",
    "in this document, we will",
    "we will explore",
    "we will walk you through",
    "will walk you through",
    "this guide will show you",
    "this page will show you",
    "this tutorial will show you",
    "this article will",
]


# GitBook blocks that must be closed by a matching `{% endX %}`. An unbalanced block
# swallows the rest of the page on the published site, so this is publish-blocking.
PAIRED_BLOCKS = ["hint", "code", "tabs", "tab", "stepper", "step", "columns", "column", "expand"]
PAIRED_BLOCK_RE = re.compile(r"\{%\s*(end)?(" + "|".join(PAIRED_BLOCKS) + r")\b")

# Technical tokens that must not appear in a page description: call syntax, dotted
# namespaces, file paths with an extension, and CamelCase identifiers.
TECH_TOKEN_RE = re.compile(
    r"\b[A-Za-z_]\w*\(\)|"                 # method() — any casing, so Initialize() is caught too
    r"\b\w+\.\w+\.\w+\b|"                  # a.b.c namespace
    r"\b[\w/\\-]+\.(?:cs|cpp|h|py|js|ts|json|yaml|yml|uplugin|md)\b"  # file.ext
)
CAMEL_CASE_RE = re.compile(r"\b[A-Z][a-z0-9]+(?:[A-Z]\w*)+\b")

# CamelCase words that are product or platform names, not code identifiers. These are
# normal English in a description; everything else CamelCase is treated as an identifier.
ALLOWED_CAMEL = {
    "GitBook", "GitHub", "JavaScript", "TypeScript", "WebGL", "WebRTC", "WebSocket",
    "WebSockets", "OpenAI", "OpenAPI", "MetaHuman", "MetaHumans", "PlayStation",
    "VisionOS", "VisionPro", "OpenXR", "ARCore", "ARKit", "MacOS", "IOS", "AndroidX",
    "ElevenLabs", "PlayCanvas", "ThreeJS", "NodeJS", "DevOps", "YouTube", "LinkedIn",
}

# GitBook renders images as <figure><img src="..." alt="...">. Almost every page in the
# documentation repo uses this rather than Markdown image syntax, so the alt-text rule has
# to understand it or it never fires where it matters.
HTML_IMG_RE = re.compile(r"<img[\s>][^>]*>", re.IGNORECASE)
HTML_ALT_RE = re.compile(r'\balt\s*=\s*"([^"]*)"', re.IGNORECASE)
HTML_SRC_RE = re.compile(r'\bsrc\s*=\s*"([^"]*)"', re.IGNORECASE)

INLINE_CODE_RE = re.compile(r"`[^`]*`")
LINK_TARGET_RE = re.compile(r"\]\([^)]*\)")
BARE_URL_RE = re.compile(r"https?://\S+")


def strip_code_and_urls(line):
    """Remove inline code spans, link targets, and bare URLs from a prose line.

    Prose rules (banned words, hedging, filler) apply to what the reader reads, not to
    identifiers or URLs. Without this, a field named `simple_mode` or a link to
    `.../just-in-time` would be reported as a banned word."""
    line = INLINE_CODE_RE.sub(" ", line)
    line = LINK_TARGET_RE.sub("]()", line)
    line = BARE_URL_RE.sub(" ", line)
    return line


# Where a reader sees a new block, so prose lines are not joined across it. A list item or a
# quote starts a block its unmarked continuation lines join; a heading, a table row, a GitBook
# block tag or an HTML line is a block of one line.
PROSE_BLOCK_START_RE = re.compile(r"^(?:#{1,6}\s|[-*+]\s|\d+[.)]\s|>|\||\{%|<)")
PROSE_ONE_LINE_BLOCK_RE = re.compile(r"^(?:#{1,6}\s|\||\{%|<)")


def prose_findings(block, rules=DEFAULT_PROSE_RULES):
    """Run the prose rules on one paragraph, given as [(lineno, text)].

    The lines are joined first, because pages wrap at 100 columns and a phrase broken after
    "we" is the normal case. Each finding names the line its match starts on, and a rule
    fires at most once per line, as it did when the checks ran line by line."""
    starts, pos = [], 0
    for _lineno, text in block:
        starts.append(pos)
        pos += len(text) + 1
    joined = " ".join(text for _lineno, text in block)

    out, seen = [], set()

    def scan(pattern, key, msg, rule):
        for m in re.finditer(pattern, joined):
            lineno = block[bisect.bisect_right(starts, m.start()) - 1][0]
            if (key, lineno) not in seen:
                seen.add((key, lineno))
                out.append(Finding("WARN", lineno, msg, rule))

    for w in rules["banned_words"]:
        scan(r"\b" + re.escape(w) + r"\b", ("banned", w), f'banned word "{w}"', "CV-1")
    for ph in CLOUD_PHRASES:
        scan(re.escape(ph), ("cloud", ph),
             f'cloud phrasing "{ph}" (refer to the backend as "Convai")', "CV-10")
    for ph in rules["hedging_phrases"]:
        scan(re.escape(ph), ("hedging", ph),
             f'hedging phrase "{ph}" (use a direct instruction: "Add...", "Configure...")', "CV-2")
    for ph in FILLER_PHRASES:
        scan(re.escape(ph), ("filler", ph), f'filler phrase "{ph}" (state the outcome directly)', "CV-3")
    scan(r"\[click here\b", ("click-here",),
         '"click here" link text; link text describes the destination, '
         'as in "See [Configure the API key](...)"',
         "CV-20")
    return out


class Finding:
    """One linter result.

    `rule` carries the CV id from the style guide, so a linter finding, a reviewer
    finding, and a flag left by GitBook's agent all name the same rule. A finding with
    no id is a mechanical failure with no editorial rule behind it, such as a file that
    cannot be read."""

    def __init__(self, level, line, msg, rule=None, capture=None):
        self.level = level
        self.line = line
        self.msg = msg
        self.rule = rule
        # The subject whose screenshot capture covers the page, on a CV-50 placeholder
        # finding: that placeholder goes back to the writer as a shot, not to a person.
        self.capture = capture


def split_frontmatter(text):
    """Return (frontmatter_dict, body_text, body_start_lineno). Frontmatter is the
    simple `key: value` lines between the first two `---` fences."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text, 1
    # find closing fence
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, text, 1

    fm = {}
    i = 1
    while i < end:
        m = re.match(r"([A-Za-z0-9_]+):\s*(.*)$", lines[i])
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val and val[0] in "|>":
            # YAML block scalar: gather following more-indented lines
            block = []
            i += 1
            while i < end and (lines[i].strip() == "" or lines[i][:1] in (" ", "\t")):
                block.append(lines[i].strip())
                i += 1
            joined = " ".join(s for s in block if s) if val[0] == ">" else "\n".join(block)
            fm[key] = joined.strip()
            continue
        fm[key] = val.strip().strip('"').strip("'")
        i += 1

    body = "\n".join(lines[end + 1:])
    return fm, body, end + 2  # 1-based line where body begins


def frontmatter_line(text, key):
    """The 1-based line of `key`'s value in the frontmatter: the key's own line, or for a
    block scalar (`key: >`) its first value line. 1 when the key is absent. A release unit is
    judged by the lines it changed, so a finding about a value must sit on that value's line."""
    lines = text.splitlines()
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            break
        m = re.match(r"%s:\s*(.*)$" % re.escape(key), lines[i])
        if m:
            value = m.group(1).strip()
            return i + 2 if value[:1] in ("|", ">") and i + 1 < len(lines) else i + 1
    return 1


def iter_body_lines(body, body_start):
    """Yield (lineno, text, in_code) tracking fenced code blocks (``` and ~~~)."""
    in_code = False
    fence = None
    for idx, raw in enumerate(body.splitlines()):
        lineno = body_start + idx
        stripped = raw.lstrip()
        if not in_code and (stripped.startswith("```") or stripped.startswith("~~~")):
            in_code = True
            fence = stripped[:3]
            yield lineno, raw, "fence-open"
            continue
        if in_code and stripped.startswith(fence):
            in_code = False
            fence = None
            yield lineno, raw, "fence-close"
            continue
        yield lineno, raw, ("code" if in_code else "prose")


def leading_h1(body, body_start):
    """Return (title, line) if the body opens with a single `# ` heading, else ("", 0).

    This is the shape GitBook writes when it round-trips a page. Only a heading that is the
    body's first content counts: a `# ` further down is a second H1 and stays an error."""
    for lineno, raw, kind in iter_body_lines(body, body_start):
        if kind in ("code", "fence-close"):
            continue
        stripped = raw.strip()
        if not stripped:
            continue
        m = re.match(r"#\s+(\S.*?)\s*$", stripped)
        return (m.group(1), lineno) if m else ("", 0)
    return ("", 0)


def capture_cover(path, subjects_dir=None, subject=None):
    """(subject, page path relative to its repository) when screenshot capture covers the
    page, else (None, that path). See references/capture.md."""
    sys.path.insert(0, TOOLS_DIR)
    import spaces
    import subjects
    root = spaces._repo_root(os.path.dirname(os.path.abspath(path)))
    rel = os.path.relpath(os.path.abspath(path), root).replace(os.sep, "/")
    return subjects.capture_covers(rel, subjects_dir, subject), rel


def check_page(path, summary_text=None, summary_titles=None, rules=None,
               subjects_dir=None, subject=None):
    """Lint one page. `rules` is what load_prose_rules returns; the default is the shipped
    lists with no subject extension. `subjects_dir` (default: where subjects.py looks) and
    `subject` decide whether screenshot capture covers the page, which changes what a CV-50
    placeholder finding asks for."""
    rules = rules or DEFAULT_PROSE_RULES
    findings = []
    try:
        # utf-8-sig strips a UTF-8 BOM, which Windows editors add and which would
        # otherwise hide the opening `---` and make every page look frontmatter-less.
        with open(path, "r", encoding="utf-8-sig") as f:
            text = f.read()
    except OSError as e:
        return [Finding("ERROR", 0, f"cannot read file: {e}")]
    except UnicodeDecodeError as e:
        # UnicodeDecodeError is a ValueError, not an OSError — without this branch a
        # single non-UTF-8 page crashes the whole run instead of failing just that page.
        return [Finding("ERROR", 0, f"file is not valid UTF-8 ({e.reason}); re-save it as UTF-8")]

    fm, body, body_start = split_frontmatter(text)

    # --- Frontmatter ---
    if fm is None:
        findings.append(Finding("ERROR", 1, "missing YAML frontmatter (--- ... ---) with title and description", "CV-33"))
        fm = {}
    title = fm.get("title", "").strip()
    desc = fm.get("description", "").strip()

    # A page carries its title in one of two places, and which one depends on who last
    # touched it. GitBook's editor writes it as a leading `# ` heading and omits the
    # frontmatter key; the tooling writes the frontmatter key and no body heading. Both
    # render correctly, so both are accepted - what is not accepted is a page with neither,
    # or one with both, because then two strings claim to be the title and the sidebar,
    # the search result and the page can disagree.
    body_title, body_title_line = leading_h1(body, body_start)
    effective_title = title or body_title

    if not effective_title:
        findings.append(Finding(
            "ERROR", 1,
            "the page has no title: add `title` to the frontmatter, or a single `# ` heading "
            "as the first line of the body",
            "CV-33"))
    elif title and body_title:
        findings.append(Finding(
            "ERROR", body_title_line,
            f"two titles: frontmatter says {title!r} and the body heading says {body_title!r}; "
            "keep one",
            "CV-33"))
    elif len(effective_title) > 60:
        findings.append(Finding(
            "WARN", 1, f"title is {len(effective_title)} chars (keep <= 60)", "CV-33"))
    title = effective_title
    desc_line = frontmatter_line(text, "description")
    if not desc:
        findings.append(Finding("ERROR", desc_line, "frontmatter is missing `description`", "CV-34"))
    else:
        if len(desc) > 200:
            findings.append(Finding("ERROR", desc_line, f"description is {len(desc)} chars (hard max 200)", "CV-34"))
        elif len(desc) < 120 or len(desc) > 160:
            findings.append(Finding("WARN", desc_line, f"description is {len(desc)} chars (target 120-160)", "CV-34"))
        low = desc.lower()
        for bad in DESC_BAD_OPENERS:
            if low.startswith(bad):
                findings.append(Finding("WARN", desc_line, f'description starts with "{bad}" (forbidden opener)', "CV-34"))
        for w in rules["banned_words"]:
            if re.search(r"\b" + re.escape(w) + r"\b", low):
                findings.append(Finding("WARN", desc_line, f'description contains banned word "{w}"', "CV-1"))
        for ph in CLOUD_PHRASES:
            if ph in low:
                findings.append(Finding("WARN", desc_line, f'description contains cloud phrasing "{ph}" (refer to the backend as "Convai")', "CV-10"))
        # The description is plain English for search results and AI answers; identifiers
        # belong in the lead paragraph or body instead.
        if "`" in desc:
            findings.append(Finding("WARN", desc_line, "description contains backtick identifiers (use plain English)", "CV-34"))
        else:
            tokens = [m.group(0) for m in TECH_TOKEN_RE.finditer(desc)]
            tokens += [m.group(0) for m in CAMEL_CASE_RE.finditer(desc)
                       if m.group(0) not in ALLOWED_CAMEL]
            if tokens:
                findings.append(Finding(
                    "WARN", desc_line,
                    f'description contains technical token(s) {", ".join(sorted(set(tokens)))}; '
                    "use plain English and move identifiers into the body", "CV-34"))

    # --- Body scan ---
    # With a GitBook-shaped page the title heading is content, so the lead-paragraph check
    # starts after it rather than at it.
    first_content_seen = False
    lead_after = body_title_line
    hint_count = 0
    saw_publish_blocker = False
    open_blocks = []
    prose_block = []  # [(lineno, text)] of the paragraph being read

    def flush_prose():
        findings.extend(prose_findings(prose_block, rules))
        del prose_block[:]

    for lineno, raw, kind in iter_body_lines(body, body_start):
        stripped = raw.strip()
        if kind != "prose":
            flush_prose()
        if kind == "fence-open":
            # code fence must declare a language
            lang = stripped[3:].strip()
            if not lang:
                findings.append(Finding("WARN", lineno, "code fence has no language label", "CV-22"))
            # the fence counts as first content
            first_content_seen = True
            continue
        if kind in ("code", "fence-close"):
            continue

        # First non-blank line. A leading `# ` heading is the page's title in GitBook's own
        # shape and is allowed; any other heading here means the lead paragraph is missing.
        if not first_content_seen and stripped:
            if stripped.startswith("#"):
                if not (lineno == lead_after and body_title):
                    findings.append(Finding(
                        "ERROR", lineno,
                        "body must start with a headingless lead paragraph, not a heading",
                        "CV-26"))
                    first_content_seen = True
                else:
                    # The title heading itself. The lead paragraph is the next line.
                    pass
            else:
                first_content_seen = True

        # A second H1 is always wrong: the page would claim two titles.
        if re.match(r"#\s+\S", stripped) and lineno != lead_after:
            findings.append(Finding(
                "ERROR", lineno,
                "a second H1 `# ` heading; a page has exactly one title", "CV-25"))
        # Matches any level from ## down, so `### Overview` is caught too, not just `## Overview`.
        if re.match(r"#{2,6}\s+(Overview|Introduction)\b", stripped, re.IGNORECASE):
            findings.append(Finding("ERROR", lineno, f"forbidden heading: {stripped}", "CV-27"))
        if re.match(r"#{2,4}\s+Step\s+\d+\b", stripped, re.IGNORECASE):
            findings.append(Finding("WARN", lineno, f'numbered step heading: "{stripped}" (use an action title)', "CV-29"))
        if re.match(r"####\s+\S", stripped):
            findings.append(Finding("WARN", lineno, "`####` heading (avoid on task/concept pages; split instead)", "CV-30"))

        # vague section headings (## level)
        if re.match(r"#{2,3}\s+\S", stripped):
            heading_text = re.sub(r"^#+\s*", "", stripped).lower().rstrip()
            for vh in rules["vague_headings"]:
                if heading_text == vh:
                    findings.append(Finding("WARN", lineno, f'vague heading "{stripped}" (use a specific, scannable heading)', "CV-28"))

        # hints
        if "{% hint" in stripped:
            hint_count += 1

        # GitBook block balance: an unclosed block silently swallows the rest of the page.
        for m in PAIRED_BLOCK_RE.finditer(stripped):
            name = m.group(2)
            if m.group(1):  # {% endX %}
                if open_blocks and open_blocks[-1][0] == name:
                    open_blocks.pop()
                else:
                    findings.append(Finding(
                        "ERROR", lineno,
                        f"`{{% end{name} %}}` does not close the innermost open GitBook block", "CV-76"))
            else:  # {% X %}
                open_blocks.append((name, lineno))

        # Wrong GitBook variable syntax renders as literal text on the published page.
        if re.search(r"\{\{\s*[\w.]+\s*\}\}", raw):
            findings.append(Finding(
                "ERROR", lineno,
                'invalid GitBook variable syntax `{{ ... }}` (use '
                '`<code class="expression">space.vars.name</code>`)', "CV-24"))

        # Images must carry alt text for accessibility and AI readability. Both syntaxes
        # count: GitBook writes <figure><img alt="">, which is what almost every page in
        # the documentation repo actually uses, and Markdown ![alt](src) appears too.
        for m in re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", raw):
            if not m.group(1).strip():
                findings.append(Finding("WARN", lineno, f"image `{m.group(2)}` has empty alt text", "CV-48"))
        for m in HTML_IMG_RE.finditer(raw):
            tag = m.group(0)
            alt = HTML_ALT_RE.search(tag)
            src = HTML_SRC_RE.search(tag)
            label = src.group(1) if src else "image"
            if alt is None:
                findings.append(Finding("WARN", lineno, f"image `{label}` has no alt attribute", "CV-48"))
            elif not alt.group(1).strip():
                findings.append(Finding("WARN", lineno, f"image `{label}` has empty alt text", "CV-48"))

        # publish blockers
        if "Screenshot required before publishing" in raw or re.search(r"\bTODO-[\w\-]+\.(png|jpg|jpeg|gif|svg)", raw):
            saw_publish_blocker = True

        # Prose checks run on text with inline code and link targets removed, so a field
        # literally named `simple_mode` or a URL containing "just" is not a false positive.
        # The line joins the paragraph it belongs to; the rules run when the paragraph ends.
        low = strip_code_and_urls(raw).lower().strip()
        if not stripped:
            flush_prose()
        elif PROSE_BLOCK_START_RE.match(stripped):
            flush_prose()
            prose_block.append((lineno, low))
            if PROSE_ONE_LINE_BLOCK_RE.match(stripped):
                flush_prose()
        else:
            prose_block.append((lineno, low))
    flush_prose()

    for name, lineno in open_blocks:
        findings.append(Finding("ERROR", lineno, f"`{{% {name} %}}` is never closed by `{{% end{name} %}}`", "CV-76"))
    if hint_count > 2:
        findings.append(Finding("WARN", 0, f"{hint_count} hints on the page (max 2 on task/concept pages)", "CV-39"))
    if saw_publish_blocker:
        covered_by, rel = capture_cover(path, subjects_dir, subject)
        if covered_by:
            # Capture covers this page, so a placeholder is no longer a task for a person:
            # the writer describes the shot in the manifest and the capturer takes it.
            findings.append(Finding(
                "ERROR", 0,
                "page has a TODO- image path or 'Screenshot required before publishing', and "
                "screenshot capture covers it (subject %s): describe the shot in "
                ".convai-docs/shots/%s.json and run capture instead (not publishable)"
                % (covered_by, rel[:-3] if rel.endswith(".md") else rel), "CV-50",
                capture=covered_by))
        else:
            findings.append(Finding("ERROR", 0, "page has a TODO- image path or 'Screenshot required before publishing' (not publishable)", "CV-50"))

    # --- SUMMARY.md reachability + label match ---
    if summary_text is not None:
        base = os.path.basename(path)
        if base != "README.md":  # section index pages are reached via folder, skip strict check
            # Match on the deepest path segments that SUMMARY.md could plausibly carry, so
            # a shared basename like `overview.md` in another folder cannot mask an orphan.
            rel = path.replace("\\", "/")
            candidates = ["/".join(rel.split("/")[-n:]) for n in (3, 2, 1)]
            if not any(c in summary_text for c in candidates):
                findings.append(Finding("WARN", 0, f"'{base}' is not referenced in SUMMARY.md (possible orphan)", "CV-37"))
            elif title and title not in (summary_titles or set()):
                findings.append(Finding("WARN", 0, f"SUMMARY.md has no sidebar label exactly matching title '{title}'", "CV-38"))

    return findings


def load_summary(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            text = f.read()
    except (OSError, UnicodeDecodeError):
        return None, set()
    # sidebar labels are the link texts: [Label](path)
    titles = set(m.group(1).strip() for m in re.finditer(r"\[([^\]]+)\]\([^)]+\)", text))
    return text, titles


def main():
    ap = argparse.ArgumentParser(description="Lint Convai GitBook documentation pages.")
    ap.add_argument("pages", nargs="+", help="Markdown page(s) to check")
    ap.add_argument("--summary", help="Path to SUMMARY.md for reachability/label checks")
    ap.add_argument("--json", action="store_true", help="Emit findings as JSON (for CI)")
    ap.add_argument("--strict", action="store_true", help="Also fail the run on WARN findings")
    ap.add_argument("--subject", "--pack", dest="subject",
                    help="Also flag the variants this subject's terminology rejects "
                         "(subjects/<subject>.json, or a path to a subject file). "
                         "--pack is the 2.6 name, kept until 3.1")
    args = ap.parse_args()

    try:
        rules = load_prose_rules(subject=args.subject)
    except (OSError, ValueError) as e:
        print(f"check_page.py: {e}", file=sys.stderr)
        return 2

    summary_text, summary_titles = (None, set())
    if args.summary:
        summary_text, summary_titles = load_summary(args.summary)

    total_errors = 0
    total_warns = 0
    report = []
    for page in args.pages:
        findings = check_page(page, summary_text, summary_titles, rules, subject=args.subject)
        # Report in reading order within each level; end-of-page findings (line 0) last.
        findings.sort(key=lambda f: (f.line == 0, f.line))
        errors = [f for f in findings if f.level == "ERROR"]
        warns = [f for f in findings if f.level == "WARN"]
        total_errors += len(errors)
        total_warns += len(warns)
        status = "FAIL" if errors else ("WARN" if warns else "PASS")
        report.append({
            "page": page,
            "status": status,
            "findings": [dict({"level": f.level, "rule": f.rule, "line": f.line,
                               "message": f.msg}, **({"capture": f.capture} if f.capture else {}))
                         for f in errors + warns],
        })
        if args.json:
            continue
        print(f"\n{status}  {page}")
        for f in errors + warns:
            loc = f"L{f.line}" if f.line else "-"
            rule = f.rule or ""
            print(f"  {f.level:5} {rule:6} {loc:>5}  {f.msg}")
        if status == "PASS":
            print("  no structural issues")

    if args.json:
        json.dump({"pages": report, "errors": total_errors, "warnings": total_warns},
                  sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"\n{total_errors} error(s), {total_warns} warning(s) across {len(args.pages)} page(s).")

    if total_errors:
        return 1
    return 1 if (args.strict and total_warns) else 0


if __name__ == "__main__":
    sys.exit(main())
