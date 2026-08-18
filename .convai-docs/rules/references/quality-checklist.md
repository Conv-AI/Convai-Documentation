# Quality checklist

Run this checklist before delivering or publishing any page. The `docs-reviewer` subagent runs it as a
pass/fail audit.

**Some items apply only to certain kinds of page.** Items marked **(SDK)** apply to pages backed by an
SDK pack; items marked **(product)** apply to pages backed by a topic pack, such as the Convai
Playground or a no-code product. Everything unmarked applies to every page.

Skip the items that do not apply and say you skipped them. Reporting "required SDK version is not
listed" on a dashboard page is a false failure, and a report full of false failures teaches the writer
to stop reading it.

## Metadata

- [ ] `title` is unique, specific, sentence case, keyword-first, ≤ 60 characters, and matches the GitBook page title **(CV-33, CV-17)**
- [ ] `description` is one sentence and states the page outcome **(CV-34)**
- [ ] `description` is 120–160 characters (hard max 200) **(CV-34)**
- [ ] Description does not start with "This page covers...", "Learn about", or "Overview of."
- [ ] URL/file slug is lowercase, hyphenated, readable, and stable **(CV-33)**
- [ ] Canonical or alternate metadata is set when the page is duplicated, versioned, or localized.
- [ ] `last_reviewed` frontmatter field is set for version-sensitive pages **(CV-35)**

## Structure

- [ ] Markdown body does not contain a duplicate `#` H1 **(CV-25)**
- [ ] Body starts with a headingless lead paragraph **(CV-26)**
- [ ] No `## Overview` or `## Introduction` **(CV-27)**
- [ ] Main sections use `##`; subsections use `###` **(CV-26)**
- [ ] Heading levels are not skipped **(CV-31)**
- [ ] Headings use sentence case **(CV-17)**
- [ ] The GitBook page outline is useful when scanned by itself.
- [ ] Page has a useful ending: verification, next steps, or reference completion **(CV-32)**

## Information architecture

- [ ] Page has one primary Diataxis mode: tutorial, how-to, reference, or explanation **(CV-36)**
- [ ] Page is reachable from sidebar, hub, or another page (no orphan pages) **(CV-37)**
- [ ] `SUMMARY.md` is updated when a new sidebar page is added **(CV-37)**
- [ ] `SUMMARY.md` sidebar label matches the `title` frontmatter of each linked page exactly (same wording, same case) **(CV-38)**
- [ ] Existing sidebar order is preserved unless the task explicitly changes navigation.
- [ ] Nav nesting does not exceed 2 levels for non-reference sections, 3 for reference.
- [ ] Page is not mixing unrelated reader intents.
- [ ] Related pages are linked with descriptive link text **(CV-20)**
- [ ] Parent pages with multiple child pages use cards **(CV-32)**
- [ ] Deprecated content has a `warning` hint at the top with the replacement and version **(CV-46)**

## Writing mechanics

These are sentence-level rules. The linter cannot check them, and they are the difference between a
page that reads like Convai and a page that reads like whoever happened to write it.

- [ ] No exclamation points in body text **(CV-4)**
- [ ] The reader is addressed as "you", never as "the user" **(CV-5)**
- [ ] Present tense throughout, except for genuinely future events **(CV-6)**
- [ ] Active voice, except where the actor is unknown or irrelevant **(CV-7)**
- [ ] One claim per sentence, so a quoted half-sentence is still true **(CV-8)**
- [ ] No time-anchored words that go stale: "currently", "new", "now available" **(CV-9)**
- [ ] Serial comma used **(CV-14)**
- [ ] One through nine spelled out; numerals for 10 and above, and always for versions and technical values **(CV-15)**
- [ ] Em dashes take no surrounding spaces **(CV-16)**
- [ ] UI labels are bold and spelled exactly as the product spells them **(CV-19)**
- [ ] Lists, tables, and code blocks inside prose have a colon-ended lead-in; one directly under its own heading does not need one **(CV-21)**

## Writing

- [ ] Tone is direct and factual, pitched at the audience the pack names — a developer for an SDK or API page, a creator or operator for a product page.
- [ ] No filler, marketing language, setup promises, or hedging **(CV-1, CV-2, CV-3)**
- [ ] No "simply", "just", or "easy." **(CV-1)**
- [ ] Product name and capitalization match the pack exactly (do not call an SDK a "plugin" unless the pack says so; match UI labels character for character) **(CV-11, CV-12)**
- [ ] Convai backend is referred to as "Convai" (no "cloud", "servers", "cloud-powered") **(CV-10)**
- [ ] Technical terms are explained or linked on first use **(CV-13)**
- [ ] Classes, methods, fields, file paths, asset paths, and literal values use `inline code` **(CV-18)**

## Examples and technical accuracy

- [ ] Code samples compile or are clearly marked as pseudocode **(CV-23)**
- [ ] Examples use realistic names, paths, and values.
- [ ] Expected output or verification steps are included **(CV-32)**
- [ ] **(SDK)** Required SDK version, engine version, permissions, or prerequisites are listed **(CV-56)**
- [ ] **(SDK)** Public APIs, fields, enums, and behaviors were verified against SDK source **(CV-53)**
- [ ] **(product)** Required plan tier, entitlement, or permission is listed, and a beta surface is labelled as beta in the lead paragraph **(CV-56)**
- [ ] **(product)** Every UI label matches the pack's terminology table exactly.
- [ ] **(product)** Every claim about a screen, default, limit, or supported format is backed by a current screenshot or by written confirmation from the pack's named owner. Anything else is listed as an open question, not stated as fact.
- [ ] **(product)** No fact was carried over from a sibling product that merely shares a folder.
- [ ] A repository's own README, docs folder, or changelog was treated as a lead and every fact taken from it was confirmed in code **(CV-54)**
- [ ] No changelog or release-notes entry was written that does not trace to real source history **(CV-55)**
- [ ] No behavior was fabricated. A claim nobody could verify is raised as a question, never written as a statement **(CV-52)**

## GitBook components

- [ ] A block-fit pass was completed: structured content uses the appropriate GitBook-native block **(CV-39)**
- [ ] Native GitBook blocks were used instead of plain Markdown or ad hoc HTML where they improve structure.
- [ ] Hints are used only for meaningful notes, warnings, success states, or risks. No more than two hints on task and concept pages **(CV-39)**
- [ ] No `####` headings on task or concept pages **(CV-30)**
- [ ] Steppers are used only for short linear procedures **(CV-66)**
- [ ] Tabs contain equivalent alternatives, not unrelated topics **(CV-40)**
- [ ] Cards are used for hubs and section index pages.
- [ ] Content references are used for important next steps or strongly related pages **(CV-32)**
- [ ] Reusable content (Snippets) are used for blocks that repeat identically across pages **(CV-32)**
- [ ] Conditional content blocks are used for small within-page variations; full-page differences use Content Variants.
- [ ] GitBook variables are used for version numbers, package URLs, dashboard URLs, and other synchronized values — not hard-coded text **(CV-24)**
- [ ] Embedded URLs point at a resource that renders for a logged-out reader, and prose says what the embed shows **(CV-68)**
- [ ] No drawing blocks; diagrams are Mermaid **(CV-69)**
- [ ] Math blocks carry their meaning in prose as well **(CV-70)**
- [ ] Prompt blocks appear only where the reader's next action is genuinely an AI task **(CV-71)**
- [ ] Columns hold genuinely parallel content, not a compressed page **(CV-72)**
- [ ] File blocks are used for downloadable assets (not inline links to external hosts) **(CV-67)**
- [ ] Updates blocks appear only on changelog or release notes pages **(CV-42)**
- [ ] Quote blocks are not used as substitutes for hints **(CV-43)**
- [ ] OpenAPI blocks are used for REST endpoint reference pages when an OpenAPI source is available **(CV-73)**
- [ ] Code blocks specify the language and use GitBook code block options when file title, line numbers, or wrapping matter **(CV-22)**
- [ ] Images have useful alt text **(CV-48)**
- [ ] **(SDK)** Required screenshots are added where UI state, Inspector setup, scene hierarchy, or visual output would otherwise be ambiguous. A screenshot here is a last resort, not a default.
- [ ] **(product)** Every panel the reader must find, every easily confused control, and every state that confirms a step worked is shown. On a product page the default is inverted: the reader is following along on screen, so showing it is usually the clearest instruction available.
- [ ] **(product)** Screenshots use a test account with test content — never a real customer's character, another user's conversation, or billing information.
- [ ] **(SDK)** A screenshot is used as a last resort, only where Inspector state, scene hierarchy, or visual output would otherwise be ambiguous **(CV-51)**
- [ ] Screenshot placeholders are used only where an image is genuinely required before publishing.
- [ ] Every screenshot placeholder states exactly what to capture, includes draft alt text, and uses a `TODO-` image filename.
- [ ] No page is published with `TODO-` image paths or "Screenshot required before publishing" hints **(CV-50)**
- [ ] Screenshots are not used for code, logs, terminal output, or configuration text that should be selectable **(CV-47)**
- [ ] Screenshots do not expose API keys, tokens, private project names, local usernames, internal paths, or emails **(CV-49)**
- [ ] Mermaid diagrams have surrounding explanatory text **(CV-45)**
- [ ] Tables are used for tabular information, not visual layout **(CV-44)**
- [ ] Expandable sections hide only optional detail, never required setup, prerequisites, or warnings **(CV-41)**
- [ ] Wide layout is used only when tables, cards, or code blocks need it **(CV-74)**
- [ ] Hidden page, page link title, next/previous links, and search indexing settings are intentional **(CV-75)**

## Troubleshooting

- [ ] Known failure modes are documented **(CV-57)**
- [ ] Each troubleshooting item includes symptom, cause, fix, and verification.
- [ ] Exact console messages are quoted when relevant **(CV-57)**
- [ ] General issues are linked to the top-level Troubleshooting section.

### Troubleshooting entry format

```md
## Troubleshooting

### Package URL cannot be resolved

**Symptom:** Unity shows `Unable to add package`.

**Cause:** The package URL is incorrect, unavailable, or blocked by the network.

**Fix:** Confirm that the URL matches the SDK version you want to install.

**Verify:** Reopen Package Manager and confirm that the SDK appears in the package list.
```

For compact pages, a symptom/cause/fix/verify table is acceptable.

## SEO and accessibility

- [ ] Link text is descriptive; no "click here." **(CV-20)**
- [ ] Meaning is never carried by colour, position, or direction alone; elements are named rather than pointed at **(CV-58)**
- [ ] Images and screenshots are not the only source of essential information **(CV-59)**
- [ ] Tables have clear headers and are not used for layout.
- [ ] Warnings and prerequisites are visible as text **(CV-59)**
- [ ] Search terms appear naturally in title, lead, headings, and examples.
- [ ] Gender-neutral language; singular "they" where gender is unknown **(CV-60)**
- [ ] No ableist or violent idioms **(CV-61)**

## Safe publishing and review

- [ ] Changes were made on the `staging` branch, not directly on `main` **(CV-62)**
- [ ] If using GitBook's native editor: a Change Request was opened and a reviewer was assigned.
- [ ] AI-generated pages include a description listing the source of truth and any assumptions **(CV-63)**
- [ ] No commit, push, pull request, or merge was created without explicit human approval **(CV-64)**
- [ ] A moved or renamed page has a redirect and an updated sidebar label in the same change **(CV-65)**
- [ ] Existing pages, folders, assets, and GitBook configuration were not deleted unless explicitly approved.
- [ ] Unrelated pages were not rewritten.
- [ ] Existing frontmatter, GitBook blocks, links, and page metadata were preserved unless the task required a targeted change.
- [ ] The final change summary lists every changed, added, moved, or deleted file.

## Editorial quality loop (post-publish)

GitBook AI Insights (Pro and Enterprise) tracks every question readers ask the Assistant and flags the
ones that returned poor answers — a direct signal of documentation gaps. Access it in
**Site settings → Insights → AI insights**.

| Signal | What it means | Action |
|---|---|---|
| High-frequency question with a low-confidence answer | The page exists but does not answer the question directly enough | Rewrite so the key answer appears in the first paragraph or a clear heading |
| High-frequency question with no matched page | The topic is undocumented | Create a how-to or reference page for it |
| Question that returns a hallucinated answer | The docs are ambiguous or contradictory | Clarify the source-of-truth page; remove or consolidate conflicting content |
| Low traffic on a page that should be high-traffic | Orphan page or poor SEO title | Check inbound links, revise the title and lead paragraph |

Review AI Insights at least once per release cycle for the subject this page belongs to. Prioritize questions asked more than 10 times
with a low-confidence answer, any question containing an error message (missing troubleshooting entry),
and questions about recently changed APIs (stale page).

- [ ] AI Insights reviewed since the last release: high-frequency unanswered questions added to backlog.
- [ ] Any question returning a hallucinated answer has a source-of-truth page updated.
- [ ] Error messages surfaced in AI Insights have a corresponding troubleshooting entry.
- [ ] Content Variants are up to date: version variants point canonical to `/latest`; language variants are not stale.
