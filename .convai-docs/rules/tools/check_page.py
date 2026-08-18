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

Usage:
    python check_page.py <page.md> [more.md ...] [--summary SUMMARY.md] [--json] [--strict]

Exit code 0 if no ERROR-level findings, 1 otherwise. WARN findings fail the run only
with --strict.
"""

import argparse
import json
import os
import re
import sys

BANNED_WORDS = [
    "simply", "just", "easy", "powerful", "seamless", "robust", "cutting-edge",
    "cloud-powered",
]
CLOUD_PHRASES = ["convai cloud", "cloud backend", "cloud pipeline", "convai's servers", "convai's cloud"]
DESC_BAD_OPENERS = ["this page covers", "learn about", "overview of"]

# Hedging phrases — passive, non-directive voice that weakens instructions
HEDGING_PHRASES = [
    "you may want to",
    "you could try",
    "you might want to",
    "you might try",
    "you can optionally",
]

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

# Vague heading text — exact lowercase match after stripping hashes and whitespace
VAGUE_HEADINGS = [
    "more information",
    "miscellaneous",
    "basics",
    "conclusion",
    "summary",
    "tips",
    "notes",
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


class Finding:
    """One linter result.

    `rule` carries the CV id from the style guide, so a linter finding, a reviewer
    finding, and a flag left by GitBook's agent all name the same rule. A finding with
    no id is a mechanical failure with no editorial rule behind it, such as a file that
    cannot be read."""

    def __init__(self, level, line, msg, rule=None):
        self.level = level
        self.line = line
        self.msg = msg
        self.rule = rule


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


def check_page(path, summary_text=None, summary_titles=None):
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
    if not title:
        findings.append(Finding("ERROR", 1, "frontmatter is missing `title`", "CV-33"))
    elif len(title) > 60:
        findings.append(Finding("WARN", 1, f"title is {len(title)} chars (keep <= 60)", "CV-33"))
    if not desc:
        findings.append(Finding("ERROR", 1, "frontmatter is missing `description`", "CV-34"))
    else:
        if len(desc) > 200:
            findings.append(Finding("ERROR", 1, f"description is {len(desc)} chars (hard max 200)", "CV-34"))
        elif len(desc) < 120 or len(desc) > 160:
            findings.append(Finding("WARN", 1, f"description is {len(desc)} chars (target 120-160)", "CV-34"))
        low = desc.lower()
        for bad in DESC_BAD_OPENERS:
            if low.startswith(bad):
                findings.append(Finding("WARN", 1, f'description starts with "{bad}" (forbidden opener)', "CV-34"))
        for w in BANNED_WORDS:
            if re.search(r"\b" + re.escape(w) + r"\b", low):
                findings.append(Finding("WARN", 1, f'description contains banned word "{w}"', "CV-1"))
        for ph in CLOUD_PHRASES:
            if ph in low:
                findings.append(Finding("WARN", 1, f'description contains cloud phrasing "{ph}" (refer to the backend as "Convai")', "CV-10"))
        # The description is plain English for search results and AI answers; identifiers
        # belong in the lead paragraph or body instead.
        if "`" in desc:
            findings.append(Finding("WARN", 1, "description contains backtick identifiers (use plain English)", "CV-34"))
        else:
            tokens = [m.group(0) for m in TECH_TOKEN_RE.finditer(desc)]
            tokens += [m.group(0) for m in CAMEL_CASE_RE.finditer(desc)
                       if m.group(0) not in ALLOWED_CAMEL]
            if tokens:
                findings.append(Finding(
                    "WARN", 1,
                    f'description contains technical token(s) {", ".join(sorted(set(tokens)))}; '
                    "use plain English and move identifiers into the body", "CV-34"))

    # --- Body scan ---
    first_content_seen = False
    hint_count = 0
    saw_publish_blocker = False
    open_blocks = []
    for lineno, raw, kind in iter_body_lines(body, body_start):
        stripped = raw.strip()
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

        # first non-blank prose/heading line = lead check
        if not first_content_seen and stripped:
            if stripped.startswith("#"):
                findings.append(Finding("ERROR", lineno, "body must start with a headingless lead paragraph, not a heading", "CV-26"))
            first_content_seen = True

        # headings
        if re.match(r"#\s+\S", stripped):
            findings.append(Finding("ERROR", lineno, "body uses an H1 `# ` heading; GitBook page title is the only H1", "CV-25"))
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
            for vh in VAGUE_HEADINGS:
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
        low = strip_code_and_urls(raw).lower()

        # banned words / cloud phrases (prose only)
        for w in BANNED_WORDS:
            if re.search(r"\b" + re.escape(w) + r"\b", low):
                findings.append(Finding("WARN", lineno, f'banned word "{w}"', "CV-1"))
        for ph in CLOUD_PHRASES:
            if ph in low:
                findings.append(Finding("WARN", lineno, f'cloud phrasing "{ph}" (refer to the backend as "Convai")', "CV-10"))

        # hedging phrases
        for ph in HEDGING_PHRASES:
            if ph in low:
                findings.append(Finding(
                    "WARN", lineno,
                    f'hedging phrase "{ph}" (use a direct instruction: "Add...", "Configure...")',
                    "CV-2"))

        # filler openers
        for ph in FILLER_PHRASES:
            if ph in low:
                findings.append(Finding("WARN", lineno, f'filler phrase "{ph}" (state the outcome directly)', "CV-3"))

        # "click here" link text
        if re.search(r"\[click here\b", low):
            findings.append(Finding(
                "WARN", lineno,
                '"click here" link text; link text describes the destination, '
                'as in "See [Configure the API key](...)"',
                "CV-20"))

    for name, lineno in open_blocks:
        findings.append(Finding("ERROR", lineno, f"`{{% {name} %}}` is never closed by `{{% end{name} %}}`", "CV-76"))
    if hint_count > 2:
        findings.append(Finding("WARN", 0, f"{hint_count} hints on the page (max 2 on task/concept pages)", "CV-39"))
    if saw_publish_blocker:
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
    args = ap.parse_args()

    summary_text, summary_titles = (None, set())
    if args.summary:
        summary_text, summary_titles = load_summary(args.summary)

    total_errors = 0
    total_warns = 0
    report = []
    for page in args.pages:
        findings = check_page(page, summary_text, summary_titles)
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
            "findings": [{"level": f.level, "rule": f.rule, "line": f.line,
                          "message": f.msg}
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
