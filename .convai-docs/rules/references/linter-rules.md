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

A task or concept page is one whose template's mode in `page-types.md` is how-to, tutorial or
explanation. The linter reads the template from the page's shape, the headings and blocks that
template requires (`tools/page_types.py`); pages carry no type key. Reference, hub and FAQ pages are
exempt from CV-30 and CV-39, and a page whose shape matches no template is held to both.

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

The lines of a paragraph are joined before these checks run, so a phrase wrapped across two lines
is caught, and the finding names the line the phrase starts on. A paragraph ends at a blank line or a
code fence; a heading, a list item, a quote, a table row, a GitBook block tag or an HTML line starts a
new one.

| Level | Rule | Enforces |
|---|---|---|
| WARN | No banned word: `simply`, `just`, `easy`, `powerful`, `seamless`, `robust`, `cutting-edge`, `cloud-powered` | CV-1 |
| WARN | No cloud phrasing: "convai cloud", "cloud backend", "cloud pipeline", "convai's servers", "convai's cloud" — refer to the backend as **Convai** | CV-10 |
| WARN | No hedging: "you may want to", "you could try", "you might want to", "you might try", "you can optionally" | CV-2 |
| WARN | No filler opener: "in this guide, we will", "we will explore", "this page will show you", and similar | CV-3 |
| WARN | No `[click here]` link text — link text describes the destination | CV-20 |

The banned words, hedging phrases and vague headings (CV-28, under "Body structure") are read from
`tools/prose_rules.json`, so this table and that file name the same terms. With
`check_page.py --subject <subject>`, every variant the subject's `terminology` rejects is a banned word
on that page too (see `references/subjects.md`); a subject can add terms, never remove one.

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

- Technical accuracy of any claim — `/convai-docs:check <path> --only accuracy` (`docs-verifier`), covering CV-52 through CV-57
- Whether the page holds to one Diataxis mode — `/convai-docs:check <path> --only quality` (`docs-reviewer`), covering CV-36
- Whether a block choice is the right one for the content — `docs-reviewer`, covering CV-40 through CV-46 and CV-66 through CV-73
- Whether prose is clear, correctly ordered, and complete — `docs-reviewer`
- Whether a page's options are set deliberately — `docs-reviewer`, covering CV-74 and CV-75

Cross-page checks — broken relative links, orphan pages, duplicate titles — belong to `check_site.py`,
which sees the whole repository rather than one page at a time.

## Site checks

`tools/check_site.py` checks what no single page can see. The rows below are its link, page-option,
image, retired-section and redirect checks; every one is an `ERROR`. Findings already present when a check was
adopted live in `.convai-docs/site-baseline.json` and do not fail a run, so only new ones do.

| Level | Rule | Enforces |
|---|---|---|
| ERROR | Every relative link resolves to a file in the repository (`broken-link`) | CV-85 |
| ERROR | Every image is a file in the repository, inside the page's own space (`missing-image`) | CV-86 |
| ERROR | No relative link leads into another space's directory; use the page's absolute site URL (`cross-space-link`) | CV-87 |
| ERROR | No `noIndex: true` on a `README.md` or on a page with child pages in `SUMMARY.md` | CV-77 |
| ERROR | `noIndex: true` on any other page has a `path: reason` line in `.convai-docs/noindex-allowlist.txt` | CV-77 |
| INFO | Every `hidden: true` page is listed on every run, baselined or not, and in the `hidden` key of `--json` | CV-78 |
| ERROR | Every page at the first level of `SUMMARY.md`, and every page with child pages, has an `icon` (hidden pages excepted) | CV-81 |
| ERROR | That icon is in the space's list in `.convai-docs/icons.json` (`{"<space directory>": ["icon", …]}`, `"."` for a single-root repository). Without the file, only presence is checked | CV-81 |
| ERROR | No file exists under a prefix listed in `.convai-docs/retired-sections.txt` | CV-82 |
| ERROR | Every `redirects:` target in `.gitbook.yaml` exists, resolved against its `root:` | CV-83 |

Three more run only with `--base <ref>`, because they are about a change rather than the site. The
change is everything between the merge base with `<ref>` and the working tree, untracked files
included, so the same command answers for a pull request in CI and for uncommitted work locally.

| Level | Rule | Enforces |
|---|---|---|
| ERROR | No image on a changed page has empty or missing alt text, in Markdown or `<img>` form | CV-79 |
| ERROR | No added image has a tool's default name: `image`, `image (19)`, `Screenshot …`, `Screen Shot …`, `untitled`, `unknown`, `capture`, `clipboard`, `download`, `pasted image`, `IMG_1234`, or digits only | CV-80 |
| ERROR | Every removed or moved page has a `.gitbook.yaml` redirect for its old URL, unless a page is still served there. Not parked by the retiring list | CV-84 |

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/convai-docs/tools/check_site.py" . \
  --baseline .convai-docs/site-baseline.json --base origin/main
```

`--write-baseline` refuses `--base`: a baseline records the site's standing backlog, and a
change-only finding recorded there would excuse the next change that repeats it.

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
