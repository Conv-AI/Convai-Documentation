# Linter rules

Every rule `tools/check_page.py` enforces, in the same order it reports them. Read this when you
cannot run the linter yourself — walking this list by hand produces the same result.

`ERROR` blocks publication. `WARN` is advisory and does not fail the run unless `--strict` is passed.

## Frontmatter

| Level | Rule |
|---|---|
| ERROR | YAML frontmatter (`--- … ---`) is present |
| ERROR | `title` is present |
| ERROR | `description` is present |
| ERROR | `description` is at most 200 characters |
| WARN | `title` is at most 60 characters |
| WARN | `description` is 120–160 characters |
| WARN | `description` does not start with "This page covers", "Learn about", or "Overview of" |
| WARN | `description` contains no banned word (see below) |
| WARN | `description` contains no cloud phrasing (see below) |
| WARN | `description` contains no backtick identifiers |
| WARN | `description` contains no technical token — `method()`, a dotted namespace, a `file.ext` path, or a CamelCase identifier that is not a known product name |

The description is what a reader sees in search results and what an AI assistant quotes. It is plain
English about the outcome, not a summary of the page's API surface.

## Body structure

| Level | Rule |
|---|---|
| ERROR | The body starts with a lead paragraph, not a heading |
| ERROR | The body contains no `# ` H1 — the GitBook page title is the only H1 |
| ERROR | No `## Overview` or `## Introduction` heading at any level from `##` down |
| WARN | No `Step 1` / `Step 2` style headings — use an action title |
| WARN | No `####` headings on task or concept pages — restructure or split |
| WARN | No vague heading: "more information", "miscellaneous", "basics", "conclusion", "summary", "tips", "notes" |

## GitBook blocks and syntax

| Level | Rule |
|---|---|
| ERROR | Every `{% hint %}`, `{% code %}`, `{% tabs %}`, `{% tab %}`, `{% stepper %}`, `{% step %}`, `{% columns %}`, `{% column %}`, and `{% expand %}` has a matching `{% end… %}`, correctly nested |
| ERROR | No `{{ … }}` variable syntax — GitBook does not render it, so it appears as literal text. Use `<code class="expression">space.vars.name</code>` |
| WARN | Every fenced code block declares a language |
| WARN | At most two hints on a task or concept page |
| WARN | Every image has non-empty alt text |

## Publish blockers

| Level | Rule |
|---|---|
| ERROR | The page contains no `TODO-*.png` (or `.jpg`, `.jpeg`, `.gif`, `.svg`) image path |
| ERROR | The page contains no "Screenshot required before publishing" marker |

These exist so an unfinished page cannot reach `main` by accident. Resolve the placeholder or remove
the image before publishing.

## Prose

Checked against the reader-facing text only. Inline code spans, link targets, and bare URLs are
stripped first, so a field named `simple_mode` or a URL containing "just" is not flagged.

| Level | Rule |
|---|---|
| WARN | No banned word: `simply`, `just`, `easy`, `powerful`, `seamless`, `robust`, `cutting-edge`, `cloud-powered` |
| WARN | No cloud phrasing: "convai cloud", "cloud backend", "cloud pipeline", "convai's servers", "convai's cloud" — refer to the backend as **Convai** |
| WARN | No hedging: "you may want to", "you could try", "you might want to", "you might try", "you can optionally" — give a direct instruction instead |
| WARN | No filler opener: "in this guide, we will", "we will explore", "this page will show you", and similar — state the outcome directly |
| WARN | No `[click here]` link text — link text describes the destination |

## Navigation

Only checked when `--summary SUMMARY.md` is passed.

| Level | Rule |
|---|---|
| WARN | The page is referenced in `SUMMARY.md` (skipped for `README.md` section index pages) |
| WARN | The `SUMMARY.md` sidebar label matches the page `title` frontmatter exactly |

## What the linter does not check

These are judgement calls or need source access, so they belong to the other two gates:

- Technical accuracy of any claim — `/verify-doc` (`docs-verifier`)
- Whether the page holds to one Diataxis mode — `/review-doc` (`docs-reviewer`)
- Whether a block choice is the right one for the content — `docs-reviewer`
- Whether prose is clear, correctly ordered, and complete — `docs-reviewer`
- Whether links resolve to real pages — human review in the GitBook Staging Space

## Running it

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/convai-docs/tools/check_page.py" "<page.md>" --summary SUMMARY.md
```

`--json` emits machine-readable findings for CI. `--strict` also fails the run on `WARN`.
