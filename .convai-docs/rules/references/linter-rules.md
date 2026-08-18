# Linter rules

Every rule `tools/check_page.py` enforces, in the same order it reports them. Read this when you
cannot run the linter yourself — walking this list by hand produces the same result.

`ERROR` blocks publication. `WARN` is advisory and does not fail the run unless `--strict` is passed.

Each row names the CV rule it enforces. That id is the same one the style guide defines, the
`docs-reviewer` cites, and GitBook's agent quotes when it flags a change request, so a finding can be
traced to one rule text no matter which of the three raised it. The rule text itself lives in
`gitbook/styleguide.md` and nowhere else; this file says only which of those rules a machine can check.

## Frontmatter

| Level | Rule | Enforces |
|---|---|---|
| ERROR | YAML frontmatter (`--- … ---`) is present | CV-33 |
| ERROR | The page has a title: either `title` in the frontmatter or a single leading `# ` heading | CV-33 |
| ERROR | The page does not have both — two titles mean the sidebar, the search result and the page can disagree | CV-33 |
| ERROR | `description` is present | CV-34 |
| ERROR | `description` is at most 200 characters | CV-34 |
| WARN | The title is at most 60 characters, wherever it lives | CV-33 |
| WARN | `description` is 120–160 characters | CV-34 |
| WARN | `description` does not start with "This page covers", "Learn about", or "Overview of" | CV-34 |
| WARN | `description` contains no banned word | CV-1 |
| WARN | `description` contains no cloud phrasing | CV-10 |
| WARN | `description` contains no backtick identifiers | CV-34 |
| WARN | `description` contains no technical token — `method()`, a dotted namespace, a `file.ext` path, or a CamelCase identifier that is not a known product name | CV-34 |

The description is what a reader sees in search results and what an AI assistant quotes. It is plain
English about the outcome, not a summary of the page's API surface.

## Body structure

| Level | Rule | Enforces |
|---|---|---|
| ERROR | The lead paragraph comes first, with no heading of its own (after the title heading, on a page that has one) | CV-26 |
| ERROR | No second `# ` H1. A leading one is the page title in GitBook's own shape and is allowed | CV-25 |
| ERROR | No `## Overview` or `## Introduction` heading at any level from `##` down | CV-27 |
| WARN | No `Step 1` / `Step 2` style headings — use an action title | CV-29 |
| WARN | No `####` headings on task or concept pages — restructure or split | CV-30 |
| WARN | No vague heading: "more information", "miscellaneous", "basics", "conclusion", "summary", "tips", "notes" | CV-28 |

## GitBook blocks and syntax

| Level | Rule | Enforces |
|---|---|---|
| ERROR | Every `{% hint %}`, `{% code %}`, `{% tabs %}`, `{% tab %}`, `{% stepper %}`, `{% step %}`, `{% columns %}`, `{% column %}`, and `{% expand %}` has a matching `{% end… %}`, correctly nested | CV-76 |
| ERROR | No `{{ … }}` variable syntax — GitBook does not render it, so it appears as literal text. Use `<code class="expression">space.vars.name</code>` | CV-24 |
| WARN | Every fenced code block declares a language | CV-22 |
| WARN | At most two hints on a task or concept page | CV-39 |
| WARN | Every image has non-empty alt text | CV-48 |

## Publish blockers

| Level | Rule | Enforces |
|---|---|---|
| ERROR | The page contains no `TODO-*.png` (or `.jpg`, `.jpeg`, `.gif`, `.svg`) image path | CV-50 |
| ERROR | The page contains no unresolved screenshot marker | CV-50 |

These exist so an unfinished page cannot reach `main` by accident. Resolve the placeholder or remove
the image before publishing.

## Prose

Checked against the reader-facing text only. Inline code spans, link targets, and bare URLs are
stripped first, so a field named `simple_mode` or a URL containing "just" is not flagged.

| Level | Rule | Enforces |
|---|---|---|
| WARN | No banned word: `simply`, `just`, `easy`, `powerful`, `seamless`, `robust`, `cutting-edge`, `cloud-powered` | CV-1 |
| WARN | No cloud phrasing: "convai cloud", "cloud backend", "cloud pipeline", "convai's servers", "convai's cloud" — refer to the backend as **Convai** | CV-10 |
| WARN | No hedging: "you may want to", "you could try", "you might want to", "you might try", "you can optionally" | CV-2 |
| WARN | No filler opener: "in this guide, we will", "we will explore", "this page will show you", and similar | CV-3 |
| WARN | No `[click here]` link text — link text describes the destination | CV-20 |

`just` is the one banned word with a legitimate sense the checker cannot separate: as a minimizer
("just run the installer") it is banned, but meaning "only" or "recently" ("returns just the first match",
"someone who has just heard of Convai") it is correct English and CV-1 permits it. Read a `just` warning
before acting on it rather than rewriting the sentence reflexively.

## Navigation

Only checked when `--summary SUMMARY.md` is passed.

| Level | Rule | Enforces |
|---|---|---|
| WARN | The page is referenced in `SUMMARY.md` (skipped for `README.md` section index pages) | CV-37 |
| WARN | The `SUMMARY.md` sidebar label matches the page `title` frontmatter exactly | CV-38 |

## What the linter does not check

These are judgement calls or need source access, so they belong to the other two gates:

- Technical accuracy of any claim — `/verify-doc` (`docs-verifier`), covering CV-52 through CV-57
- Whether the page holds to one Diataxis mode — `/review-doc` (`docs-reviewer`), covering CV-36
- Whether a block choice is the right one for the content — `docs-reviewer`, covering CV-40 through CV-46 and CV-66 through CV-73
- Whether prose is clear, correctly ordered, and complete — `docs-reviewer`
- Whether a page's options are set deliberately — `docs-reviewer`, covering CV-74 and CV-75

Cross-page checks — broken relative links, orphan pages, duplicate titles — belong to `check_site.py`,
which sees the whole repository rather than one page at a time.

## Running it

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/convai-docs/tools/check_page.py" "<page.md>" --summary SUMMARY.md
```

`--json` emits machine-readable findings for CI, each carrying its `rule` id. `--strict` also fails the
run on `WARN`.

## Keeping the ids honest

`tools/check_rules.py` validates the rule ids themselves: that none is defined twice, that none has
disappeared, that no pinned id has quietly changed meaning, and that nothing in this repository refers
to an id the style guide does not define.

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/convai-docs/tools/check_rules.py"
```

A deliberate rule change fails this check once, by design. Re-run it with `--update <date>` and commit
the resulting `gitbook/rules.json` diff — that diff is the record of what the rule used to say, and the
style guide's decision log is where you explain why it changed.
