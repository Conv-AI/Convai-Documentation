# AAA page-writing prompt

The complete structured prompt every docs-writer must follow when creating or revising a
Convai GitBook documentation page. This is extracted directly from the writing template and
applies to every SDK. SDK-specific naming, terminology, and variables come from the SDK pack.

---

## Context to establish before writing

**Audience** (from SDK pack):
- Primary: developers integrating the SDK. Getting Started pages assume limited experience;
  advanced and reference pages may assume domain and language fluency.

**Required source of truth:**
- SDK source code, existing docs, provided technical notes, and the current documentation plan.
- Do not invent API names, component fields, behavior, requirements, limits, or console messages.
- If required technical context is missing, stop and ask before drafting.

**Publishing model:**
- The GitBook page title is the rendered page H1. Never duplicate it with a Markdown `#` heading.
- Body starts with a headingless lead paragraph. Sections start at `##`. Subsections at `###`.
- Do not use `####` on task or concept pages. If a page reaches four heading levels, split it.
  Reserve `####` only for dense reference pages where a third sub-level is the only alternative.

---

## The 10-point AAA structure

### Point 1 — YAML frontmatter

- `title`: specific, unique, sentence case, ≤ 60 characters, keyword-first, suitable as the
  GitBook page title.
- `description`: one sentence, target 120–160 characters (hard max 200), outcome-focused,
  keyword-bearing. Must not start with "This page covers", "Learn about", or "Overview of".
  Must not contain class names, method names, or backtick identifiers — those belong in the
  body. Must not promise ease or speed ("up and running in minutes").

### Point 2 — Lead paragraph

- Headingless. 1-3 short sentences.
- State what the reader will accomplish or understand.
- Include the main topic naturally.
- Do not use `## Introduction`, `## Overview`, or filler like "In this guide…".
- Answer three questions without a heading: What is this page about? Who or when is it for?
  What is the outcome?

### Point 3 — Body structure

- Use 4-7 useful `##` sections for normal task pages; fewer for short reference pages.
- Headings must be sentence case, specific, and scannable.
- Task headings start with a base verb: `Configure the API key`, `Verify the setup`.
- Concept/reference headings use noun phrases: `Conversation lifecycle`, `Events`.
- Do not use vague headings: `Overview`, `Basics`, `Advanced`, `More information`,
  `Miscellaneous`, `Conclusion`, `Summary`.
- The page outline (headings only) must be self-explanatory when scanned alone.

### Point 4 — Page-type requirements (Diataxis)

One primary mode per page. Recommend a split if modes mix.

**Tutorial:**
- Use "We will…" collaborative framing, not "You will learn…".
- Include a clear destination up front.
- Each step must produce a visible, meaningful result the learner can observe.
- Ruthlessly minimize explanation — link to reference or concept pages instead of adding prose.
- Keep to one path; ignore options and alternatives.

**How-to guide:**
- Assume the reader is already competent in the general domain.
- Include: outcome, prerequisites, focused steps, verification, troubleshooting, next steps.
- Prioritize practical usability over exhaustive completeness.
- Do not cover every edge case.

**Reference:**
- Be austere. Include exact names, types, syntax/signature, fields, parameters, defaults,
  return values, events, errors, and constraints.
- Mirror the SDK's structure. No narrative teaching, no marketing, no opinion.

**Explanation:**
- Take a wide perspective. Cover background, rationale, design decisions, alternatives,
  tradeoffs, and relationships between systems.
- Use reasoning statements: "The reason X works this way is…".
- Do not include steps, procedures, or close-up reference detail.

**Troubleshooting:**
- Organize by symptom.
- Each item: symptom, cause, fix, and verification.
- Quote exact console messages.

**Hub/index page:**
- Short section introduction plus cards for the main child pages.
- No long procedures or full reference tables.

### Point 5 — GitBook block usage

Use GitBook-native blocks when the content intent matches. Never flatten structured content
into plain paragraphs, generic bullets, or ad hoc HTML when a block communicates the
structure better.

| Content need | Block to use |
|---|---|
| Important note, prerequisite, non-critical constraint | `{% hint style="info" %}` |
| Expected success state | `{% hint style="success" %}` |
| Common mistake, silent failure, compatibility issue | `{% hint style="warning" %}` |
| Security risk, data loss, destructive action, broken production | `{% hint style="danger" %}` |
| Short linear procedure | `{% stepper %}` with `{% step %}` |
| Equivalent alternatives (OS, version, Inspector vs C#) | `{% tabs %}` |
| Hub/index navigation | Cards (`<table data-view="cards">`) |
| Important related page or next step | `{% content-ref %}` |
| REST API endpoint reference | OpenAPI block |
| Code with syntax highlighting | ` ```language ` (always specify language) |
| Code tied to a file path | `{% code title="path/to/file.cs" %}` |
| External URL with rich preview (video, repo, tool) | Embed block |
| Content identical on multiple pages | Reusable content / Snippet |
| Small within-page variation by version/platform/role | Conditional content block |
| Downloadable asset | File block |
| Changelog / release notes | Updates block (only on changelog pages) |
| Attributed third-party quote | Quote block (rarely; not a hint substitute) |
| Architecture, lifecycle, state machine, data flow | Mermaid diagram + explanatory text |
| Tabular data: fields, matrix, troubleshooting | Table with clear headers |
| Optional detail that interrupts the main flow | Expandable section (never hide prerequisites or warnings) |

**Block rules:**
- Max two hints on task and concept pages. More than two hints signals a structural problem.
- Keep block titles and labels specific: `Inspector`, `C#`, `Windows` — not `Option 1`, `Tab 2`.
- Do not hide required prerequisites, warnings, or setup steps in tabs or expandable sections.
- Use wide layout only for tables, cards, OpenAPI, or dense code.
- GitBook variables: `<code class="expression">space.vars.variable_name</code>` — never `{{ }}`.

### Point 6 — Writing standards

- Direct, factual, developer-focused language.
- Second person for procedures: "Add your API key."
- First-person plural in tutorials: "We will add the component."
- Active voice and present tense.
- Short sentences. One claim per sentence.
- American English spelling.
- Format all class names, methods, fields, enums, file paths, asset paths, package names,
  console messages, and literal values as `inline code` — in prose, table cells, list items,
  step bodies, everywhere.
- Product name and backend naming from the SDK pack.
- Backend: "Convai" — never "Convai cloud", "cloud backend", "Convai's servers", "cloud-powered".

**Avoid:**
- Marketing language: "powerful", "seamless", "robust", "cutting-edge"
- Setup promises: "up and running in minutes", "just one API key"
- Filler: "In this guide, we will explore…"
- Hedging: "you may want to", "you could try"
- Dismissive: "simply", "just", "easy"
- Vague labels: "Overview", "More information", "Miscellaneous"
- Non-descriptive links: "Click here"

### Point 7 — Examples and validation

- Include runnable or clearly scoped examples when the page is not purely conceptual.
- Code blocks must specify the language (`csharp`, `cpp`, `yaml`, `json`, `bash`).
- Examples must use realistic SDK/engine names and paths — not generic placeholders.
- Include expected results after setup or code — state what the reader should observe.
- Include verification steps so the reader knows the task worked.
- Add screenshot placeholders only at points where a visual is required to prevent ambiguity
  or verify a visual result.

### Point 8 — SEO and accessibility

- Title, description, lead, headings, and links must match the reader's search intent.
- Use descriptive link text: "See [Configure the API key](…)" — never "Click here".
- Keep heading order semantic; do not skip levels.
- Add meaningful alt text to images — describe purpose and relevant state.
- Do not use screenshots as the only source of essential instructions.
- Do not add screenshots for decorative, obvious, or text-only content.
- Use tables only for tabular data, not visual layout.
- Make warnings and prerequisites visible as text (not only in images).
- Put the direct answer to the most likely reader question in the **first sentence** of the
  relevant section — not buried in the third paragraph (AI readability).
- Use specific `##` headings that match how a reader would phrase a question.
- Avoid ambiguous pronoun references ("it", "this") across paragraphs.
- Quote exact console messages, field names, and component names in inline code.
- Keep one claim per sentence.

### Point 9 — Cross-linking and orphan prevention

- Every page must be reachable from the sidebar, a hub page, or a related-page link.
- If adding a sidebar page, update `SUMMARY.md` with the smallest necessary change.
  The sidebar label must equal the `title` frontmatter exactly.
- End task pages with 2-5 useful next-step links using `{% content-ref %}`.
- Link to source-of-truth pages instead of repeating large sections.

### Point 10 — Final self-review

Before handing off, confirm every item:

- [ ] No duplicate Markdown `#` H1 in body.
- [ ] Description is 120–160 characters (hard max 200).
- [ ] No `## Overview` or `## Introduction`.
- [ ] Page has one primary Diataxis mode.
- [ ] All technical claims are sourced from code, existing docs, or provided context.
- [ ] Page is not orphaned (reachable from sidebar, hub, or a related-page link).
- [ ] `####` headings do not appear on task or concept pages.
- [ ] Hints do not exceed two on task and concept pages.
- [ ] Deprecated APIs or components have a `warning` hint at the top naming the replacement and version.
- [ ] Version-sensitive pages have `last_reviewed` in frontmatter, set to the current SDK version.
- [ ] Changed files and any assumptions are listed at the end.
- [ ] No git action taken. Stops for human review.
