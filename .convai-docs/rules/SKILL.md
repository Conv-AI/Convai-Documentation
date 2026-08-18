---
name: convai-docs
description: Write, revise, or review Convai's public GitBook documentation for any SDK or plugin (Unity, Unreal Engine, Web, and others). Use whenever the task involves creating a new docs page, updating an existing page, building a hub/index, or auditing a page for quality in the Convai-Documentation repository. Enforces Diataxis structure, GitBook block usage, the Convai writing standards, and the staging-first publishing workflow.
---

# Convai documentation authoring

This skill governs how Convai documentation pages are written, structured, and reviewed for GitBook.
It applies to every SDK and plugin documented in this repository. Generic doctrine lives in
`references/`; SDK-specific facts live in `packs/`; copy-paste skeletons live in `templates/`.

If required technical context is missing, stop and ask for it before writing. Never invent API names,
component fields, behavior, requirements, limits, or console messages.

## Choose your workflow

| Scenario | Path |
|---|---|
| **You just want a page written and you do not write documentation for a living** | Run **`/doc`**. It asks what it needs in plain language, picks the page type and location for you, writes it, and runs all three checks. This is the default. |
| Write or revise a single page, and you already know the page type and pack | `/write-doc <topic> [pack]`, then the single-page workflow below. |
| Add one feature/section that has several pages | Plan just that scope (`/plan-docs <pack> --scope <area>`), approve, then `/build-docs` the resulting unit(s). |
| Document a whole area from scratch — an SDK, a product surface, or a customer's set | **Plan first, then build by unit.** Run `/plan-docs <sdk>` → human approves the plan → `/build-docs <sdk>` writes one work unit at a time, with review between units. See "Scaffold a whole SDK" below. |

### Scaffold a whole area

Never write an entire area in one pass — quality degrades. This works for any pack kind: an SDK, a
product surface such as the Playground, or a customer's documentation set. The flow is:

1. `/plan-docs <pack>` runs the `docs-planner`, which inspects whatever that pack kind allows — the SDK
   source, the product and its owner, or the customer's agreed facts — and writes a plan to
   `.convai-docs/plans/<pack>.md` in the documentation repo: every page grouped into review-sized
   **work units** (one section, or one feature and its sub-pages, per unit). The planner stops for
   human approval.

   For a topic or customer plan, expect rows marked `[?]` whose source of truth is the owner. Those are
   the plan's questions, and they are the point: `/build-docs` leaves them unwritten until answered
   rather than guessing.
2. The human reviews and approves the plan and resolves its open questions.
3. `/build-docs <pack>` writes exactly **one work unit** with the `docs-writer`, marks those pages
   drafted in the plan, and stops for review. Repeat per unit. A large `features` section is built one
   feature at a time, not all at once.

The plan format and work-unit sizing rules are in `plans/_plan-template.md`.

## Single-page workflow

Follow these steps in order for any single write or revise task.

1. **Identify the pack.** Determine what the page is about and read that pack first — it carries the
   product naming, terminology, verification rules, GitBook variables, and gold-standard example pages
   for that subject. There are three kinds, and they differ in how a claim gets proven:

   | The page is about | Pack | How a claim is verified |
   |---|---|---|
   | An SDK or plugin — Unity, Unreal, Web | `packs/<sdk>.md` | Read the SDK source |
   | A Convai product surface or concept area — the Playground, Avatar Studio and the other no-code products, an API surface, a general topic | `packs/<topic>.md` | Look at the product, or ask its named owner |
   | One named customer's deployment | `packs/customers/<customer>.md` | Check what was agreed with that customer |

   List `packs/` to see what exists. Do not assume a pack is complete because it exists: read it, and
   if it declares itself a stub in its title or still carries a `TODO:` covering a fact this page
   needs, stop and ask the pack's owner. An unfilled field means nobody has confirmed that fact yet,
   which is precisely when guessing does the most damage.

   If no pack exists for the subject, ask whether to scaffold one with `/new-pack` before drafting.

   After reading the plugin pack, check whether `.convai-docs/packs/<name>.md` exists in the
   documentation repo root. If it does, read it — project-level overlays take precedence for any rule
   they override and document known violation history.
2. **Choose one Diataxis mode.** Decide whether the page is a tutorial, how-to guide, reference, or
   explanation. A page has exactly one primary mode. If the request mixes modes, recommend a split.
   See `references/diataxis.md`.
3. **Load the references.** Always read the following four files for every task — they apply to every
   page regardless of scope:
   - `references/writing-standards.md` — voice, tone, terminology, variable syntax, version tracking
   - `references/structure.md` — frontmatter, headings, page skeleton, file naming
   - `references/gitbook-blocks.md` — block selection, syntax, and rules for every block type
   - `references/diataxis.md` — page-type requirements (tutorial/how-to/reference/explanation) and IA

   Then use the routing table below to pull in any additional references the task requires.
4. **Start from a template.** Pick the skeleton that matches the page. A page still has exactly one
   Diataxis mode — the specialised templates are shapes within a mode, not extra modes.

   | The page is | Template | Mode |
   |---|---|---|
   | Teaching a beginner end to end | `tutorial.md` | tutorial |
   | One specific task for someone already competent | `how-to.md` | how-to |
   | Moving a project between versions | `migration.md` | how-to |
   | Fixing errors the reader is hitting right now | `troubleshooting.md` | how-to |
   | Facts about a class, component, or setting | `reference.md` | reference |
   | One REST or realtime endpoint | `api-endpoint.md` | reference |
   | What changed in each release | `release-notes.md` | reference |
   | Why something works the way it does | `explanation.md` | explanation |
   | Defining the vocabulary | `glossary.md` | explanation |
   | Routing readers to child pages | `hub.md` | — |
   | Genuine one-off questions with no home elsewhere | `faq.md` | — |

   Reach for `faq.md` last. Anything a reader would search for by task name belongs on a real page
   where the sidebar and search can find it, not buried in a question list.

   Before filling the template, read the closest gold-standard example page
   from the SDK pack's "Gold-standard example pages" section — choose the page whose Diataxis mode
   matches the task. Match its quality bar: lead paragraph style, section count, block selection, and
   prose tone. This is mandatory. Then copy the matching skeleton from `templates/` and fill it.
5. **Verify before you write.** Before writing any technical claim — class name, component name,
   method, field, Blueprint node display name, console message, version number, default value — locate
   the exact definition in the SDK source files and note the file path and line. If the source cannot be
   found, do **not** infer or invent: stop and flag the missing context to the human. This applies to
   changelogs and release notes as well — only record changes that appear in the SDK source history;
   never fabricate entries.
6. **Draft the page** following the structure, writing, block, and image rules in the references and
   the SDK pack.
7. **Systematic self-review.** Run every section of `references/quality-checklist.md` as a binary
   pass/fail before handing off. Do not summarize — go through each checklist item one by one. Fix every
   failure before stopping. A vague impression that the page "looks good" does not satisfy this step.
8. **Stop for human review.** Prepare file changes only. List every changed, added, moved, or deleted
   file and any assumptions. Do not commit, push, open a pull request, or merge without explicit human
   approval. See `references/safe-publishing.md`.

## Where the rules live

Each reference file owns its rules outright. There is no combined archive: a second copy of the same
rules drifts from the first, and the writer then has two answers to the same question. If a rule is
missing, add it to the one file that owns that area.

- `references/aaa-prompt.md` — The complete 10-point AAA page-writing prompt. Read this when starting
  a new page to follow every requirement in the correct order.
- `references/gold-standard-example.md` — An annotated wrong/right page skeleton. Read this when
  reviewing a draft or when unsure whether a structural choice is correct.
- `references/linter-rules.md` — Every rule `tools/check_page.py` enforces, in readable form.

## Reference routing

Four files are always loaded for every page. Additional files are loaded when the task touches them.

| When the task involves | Read |
|---|---|
| **Every page** (always load — all four) | `references/writing-standards.md`, `references/structure.md`, `references/gitbook-blocks.md`, `references/diataxis.md` |
| Starting any new page (full structured guide) | `references/aaa-prompt.md` |
| Screenshots, image placeholders, alt text | `references/images.md` |
| Titles, slugs, canonical URLs, accessibility | `references/seo-accessibility.md` |
| Final pre-publish verification, AI Insights loop | `references/quality-checklist.md` |
| Checking a page against the deterministic linter without running it | `references/linter-rules.md` |
| Branch workflow, Change Requests, agent permissions | `references/safe-publishing.md` |
| Reviewing a draft or comparing structural choices | `references/gold-standard-example.md` |

## Non-negotiables

These are the highest-frequency failure points. Always enforce them on every page.

### Structure and metadata
- The GitBook page title is the page H1. **Never** add a body `#` heading. Body starts with a
  headingless lead paragraph; sections start at `##`.
- No `## Overview` or `## Introduction`. No `Step 1`/`Step 2` headings. Sentence case headings.
- `description` frontmatter: one outcome-focused **plain English** sentence, 120–160 characters (hard
  max 200). Must not start with "This page covers", "Learn about", or "Overview of". Must not contain
  class names, method names, backtick identifiers, or other technical tokens — those belong in the lead
  paragraph or body, not in the description.
- One Diataxis mode per page.
- Every page must be reachable (sidebar, hub, or related-page link). Update `SUMMARY.md` with the
  smallest change when adding a sidebar page; the label must equal the page `title` frontmatter exactly.
- Set `last_reviewed` frontmatter for any page whose accuracy depends on a specific SDK or engine
  version.

### Voice, terminology, and inline code
- No marketing language, filler, hedging, or "simply"/"just"/"easy".
- Product naming and backend naming come from the SDK pack. Never call an SDK a "plugin" unless the
  pack says so.
- Refer to Convai's backend as **"Convai"** — not "Convai backend", "Convai cloud", "Convai's
  servers", "cloud backend", or "cloud-powered". Write "streams audio to Convai", "Convai responds" —
  not "streams audio to the Convai backend".
- **Format class names, methods, fields, enums, file paths, asset paths, package names, console
  messages, and literal values as `inline code` everywhere they appear — in prose, in table cells, in
  list items, in step bodies.** This is not optional in table cells.
- **No "click here" links.** Link text must describe the destination: "See [Configure the API key](…)",
  not "click here" or "this page".

### Code blocks and screenshots
- **Every code block must specify the language** (`csharp`, `cpp`, `yaml`, `json`, `bash`, etc.).
  A fenced block with no language tag is a checklist failure.
- Use a titled code block (`{% code title="..." %}`) when the file path is relevant to the reader.
- Code examples must compile and run, or be explicitly marked `// pseudocode` in a comment. Do not
  silently include non-compilable snippets.
- **Never use a screenshot for code, terminal output, log messages, or configuration text.** These
  must be selectable text in a code block.
- Do not use `####` headings on task or concept pages. If a third heading level is needed,
  restructure or split the page instead.

### GitBook variables
- **Never hard-code version numbers, package URLs, or other synchronized values as plain text.** Always
  use the GitBook expression syntax: `<code class="expression">space.vars.variable_name</code>`.
  Writing `{{ variable_name }}` or `{{ space.vars.variable_name }}` is wrong — that syntax is not
  rendered by GitBook and will appear as literal text on the published page.

### Technical accuracy and changelogs
- Verify every technical claim against SDK source, existing docs, or provided context before writing it.
  Note the source file path for each claim.
- **Never fabricate changelog or release notes entries.** Every entry in an Updates block or release
  notes page must be traceable to the SDK source history (commit messages, `.uplugin` / `package.json`
  version bumps, or maintainer-provided notes). If the source history is unavailable, write a
  placeholder and flag it for the human to fill in.
- If the SDK version stated in the pack or plan does not match what the source files show, stop and
  report the mismatch instead of guessing.

### GitBook blocks
- Use GitBook-native blocks when the content intent matches a block. Max two hints on task/concept pages.
- Run a block-fit pass before handing off: identify structured content (procedures, alternatives,
  important notes, hub navigation, code) and upgrade it to the matching native block.

## Quality gate

Every page passes three independent checks before a human accepts it. Run them after drafting:

1. **Structure lint (deterministic).** `python "${CLAUDE_PLUGIN_ROOT}/skills/convai-docs/tools/check_page.py" "<page>" --summary SUMMARY.md` —
   frontmatter, description length, body H1, forbidden headings, lead paragraph, hint count, code-fence
   languages, publish-blocking TODO placeholders, banned words, SUMMARY reachability. ERROR fails; WARN advises.
2. **Technical accuracy (`/verify-doc`).** The `docs-verifier` checks every code identifier, console
   message, version, and menu path against the actual SDK source. Catches wrong or invented facts.
3. **Quality review (`/review-doc`).** The `docs-reviewer` runs `references/quality-checklist.md` for
   the judgement-based standards the linter cannot check.

The `docs-writer` runs the lint itself and fixes ERRORs; accuracy and quality review are independent
gates a human triggers before accepting the page.

## Commands and subagents

- `/doc [what you want to document]` is the front door: it interviews the user, picks the page type,
  pack, and file location, runs the `docs-writer`, then runs the lint, `docs-verifier`, and
  `docs-reviewer` without being asked. Use this unless a narrower command is clearly wanted.
- `/plan-docs <pack> [source-path] [--scope <area>]` runs the `docs-planner` to inspect a subject and
  produce a documentation plan in `.convai-docs/plans/<pack>.md`. Stops for approval.
- `/build-docs <pack> [unit]` runs the `docs-writer` to write one approved work unit, then stops.
- `/write-doc <topic> [pack]` runs the `docs-writer` to draft or revise a single page.
- `/verify-doc <path> [source-path]` runs the `docs-verifier` to check technical accuracy against SDK source.
- `/review-doc <path>` runs the lint plus the `docs-reviewer` to audit quality against the checklist.
- `/new-pack <name> [sdk|topic|customer]` scaffolds a new pack from the matching template.

Directory map (bundled in the plugin, read-only): `references/` (generic doctrine),
`packs/` (per-SDK facts), `templates/` (page skeletons),
`plans/_plan-template.md` (the plan format), `tools/` (the linter). Generated per-SDK plans are written
to `.convai-docs/plans/<sdk>.md` in the documentation repo (a gitignored working artifact, never published).
