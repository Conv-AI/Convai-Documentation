---
title: Convai documentation style guide
description: The writing standards every Convai documentation page follows, so that any writer produces the same clear, accurate, consistent result.
---

Everything on this page exists to answer one question: **what does a good Convai documentation page look like?**

You do not need to be a technical writer to use it. You do not need to read it end to end. If you are about to write or review a page, read "Start here" below — that is the whole job most of the time. Everything after it is the detail, organised so you can look up exactly the part you need.

{% hint style="info" %}
**Never written documentation before?** That is fine, and this guide is built for you. Follow "Start here", copy the shape of an existing page you like, and let the review catch the rest. Nobody is expected to hold 76 rules in their head.
{% endhint %}

## Why we care this much

Convai's documentation exists so that someone who has never heard of Convai can integrate it, ship it, and debug it without asking us a question a page should have answered.

That sets a bar higher than "correct". A page can be entirely true and still fail, because it assumed knowledge the reader did not have, buried the one sentence they needed, or made them guess which of two names is the real one. The rules here are the accumulated fixes for those failures — each one is here because a page without it confused a real reader.

The second reason is consistency. Convai's documentation is written by engineers across the company and by AI agents, not by one writing team. Without a shared standard, every page reads like whoever happened to write it, and readers stop trusting the set. A reader who learns how one Convai page works should already know how the next one works.

## Start here

If you read only one section, read this one. These nine habits produce most of the quality; the rest of the page is detail.

1. **Write the lead paragraph for someone who arrived from Google and knows nothing.** No heading above it. Say what this page lets them do and who it is for, in two or three sentences.
2. **One page, one job.** Teaching a beginner, doing one task, listing facts, or explaining why — pick one. If a page is doing two, it should be two pages.
3. **Never state a fact you have not checked.** Not from memory, not from a README, not from an older page. Check the source. If you cannot check it, leave it out and flag it — an open question is always better than a confident wrong answer.
4. **Put the answer first.** In the page, in the section, in the sentence. Readers scan, and AI assistants quote the first sentence of a section.
5. **Anything you would type or click goes in `code` or bold.** Class names, fields, file paths, console messages in `code`; UI labels the reader clicks in **bold**, spelled exactly as the product spells them.
6. **Cut the words that promise instead of inform.** No `simply`, `just`, `easy`, `powerful`, `seamless`. If a step is genuinely short, the reader will notice without being told.
7. **Use the real GitBook blocks.** Steps go in a stepper, alternatives go in tabs, warnings go in a hint, child pages go in cards. Plain paragraphs where a block belongs is the most common thing reviews catch.
8. **End with proof.** How does the reader know it worked? A verification step, an expected output, or a clear next page.
9. **Show it to a person before it ships.** Everything here is a floor, not a ceiling.

## How this page is used

**By people:** as the reference you check when you are unsure, and the standard a reviewer holds a page to.

**By AI:** GitBook's AI editor and agent read this page — and only this page — when writing, editing, and reviewing our documentation. They do not read any other page in this space, and they apply no outside style rules. Every rule we want enforced has to appear here, written down.

**About the rule IDs:** Numbered rules (`CV-1`, `CV-2`, …) are the enforceable tier — the agent flags violations and cites the ID, so any flag traces back to an exact rule. Unnumbered guidance, like the voice description, is judgement territory: the agent writes with it and may suggest it, but never flags it. Never renumber or reuse an ID; past flags and the decision log refer to them. To add a rule, give it the next number after the current highest, wherever on the page it belongs.

**Where the rules actually live:** this page is generated from the `convai-docs` tooling repository (`Conv-AI/convai-docs-tools`, `skills/convai-docs/gitbook/styleguide.md`). To change a rule, change it there and re-run `/convai-docs:styleguide-sync`. Edits made directly on this page are lost at the next sync.

## Audience and scope

**Who reads our documentation:** developers integrating Convai into a game or simulation, and creators and operators using Convai's no-code products. We assume general technical competence and **no** familiarity with Convai. We explain our concepts fully and do not explain theirs — a Unity developer knows what a prefab is; they do not know what a Narrative Design section is.

Getting Started pages assume the least: someone who has just heard of Convai must be able to follow them end to end. Advanced, scripting-reference, and platform pages may assume more.

**Who writes our documentation:** every engineer at Convai, not only technical writers. That is why these rules are mechanical wherever they can be — a rule that needs taste to apply is a rule that produces inconsistent pages.

**What this guide covers:** every page on Convai's documentation sites, in every SDK, product, and API section. It covers this page too: the guide holds itself to its own rules.

## Voice and tone

Direct and factual. Write like an engineer explaining something to a competent colleague who has not seen this system before: state what is true, state what to do, and stop. No warmth performance, no hype, no apology.

These pairs show where the line falls:

| Guidance | Do | Don't |
|---|---|---|
| Direct, not stiff | ✅ "If the connection drops, the character stops speaking and the session ends." | ❌ "In the event that a connection interruption should occur, the character's speech will be terminated." |
| Factual, not promotional | ✅ "Gaze articulates across torso, head, eyes, and eyelids." | ❌ "Our `powerful` gaze system delivers stunningly lifelike eye contact." |
| Confident, not hedged | ✅ "Add `ConvaiAudioOutput` to the same GameObject." | ❌ "You `may want to` consider adding `ConvaiAudioOutput`, which could help." |
| Complete, not clever | ✅ "This requires Unity's Input System package. Install it before continuing." | ❌ "Assuming your input setup is in order, continue." |

The enforceable rules of voice:

* **CV-1:** No marketing language. Banned outright: `simply`, `just` (as a minimizer), `easy`, `easily`, `powerful`, `seamless`, `robust`, `cutting-edge`, `blazing`, `effortless`. _Exception: `just` meaning "only" is fine — "returns just the first match"._
* **CV-2:** No hedging in instructions. Banned: `you may want to`, `you could try`, `you might want to`, `you might try`, `you can optionally`. Give the instruction, then state when it does not apply.
* **CV-3:** No filler openers. Banned: `In this guide, we will`, `In this section, we will`, `We will explore`, `This page will show you`, `This tutorial will walk you through`. State the outcome directly.
* **CV-4:** No exclamation points in body text.
* **CV-5:** Address the reader as "you". Never "the user" for the reader. _Exception: "the user" is correct when the reader is a developer and the sentence is about **their** end user: "Your app asks the user for microphone permission."_
* **CV-6:** Present tense. ✅ "The component streams audio to Convai." ❌ "The component will stream audio to Convai." _Exception: genuinely future events ("Support for the legacy plugin ends in the 5.0 release")._
* **CV-7:** Active voice. ✅ "`ConvaiRoomManager` opens the connection." ❌ "The connection is opened by `ConvaiRoomManager`." _Exception: when the actor is unknown or irrelevant ("The API key is stored in the settings asset")._
* **CV-8:** One claim per sentence. Split compound claims — an AI assistant quoting half a sentence must still quote something true.
* **CV-9:** No time-anchored words that go stale: "currently", "at present", "new", "now available", "recently". State the fact without the anchor.

## Word list

| Term | Use | Don't use | Notes |
|---|---|---|---|
| The backend | **Convai** | `Convai backend`, `Convai cloud`, `cloud backend`, `Convai's servers`, `cloud-powered`, `cloud pipeline` | **CV-10.** Write "streams audio to Convai", "Convai responds" |
| Unity product | **Convai Unity SDK** | `Convai Unity plugin` | **CV-11.** Legacy plugin sections are a separate, older surface |
| Unreal product | the name in the Unreal pack | anything else | **CV-11** applies per product; the pack is authoritative |
| The thing a reader adds Convai to | **character** | `NPC`, `bot`, `agent` (in SDK docs) | |
| Scene placement | **in-scene** | `game-world`, `in-game` | Primary framing is training simulations, then interactive experiences, then games |
| Convai Playground | **Convai Playground** | "dashboard", "portal", "console" | Match the product's own label |

### Convai product names

Getting a product's name wrong is the fastest way to look like we do not know our own product. These are the canonical names:

| Product | Write it as | Never |
|---|---|---|
| The company and the backend | **Convai** | `the Convai backend`, `Convai cloud` |
| Unity integration | **Convai Unity SDK**, or **Convai SDK for Unity** | `Convai Unity plugin` |
| Web dashboard and character builder | **Convai Playground**, then **the Playground** | `dashboard`, `portal`, `console`, `Legacy Playground` |
| Browser avatar tool | **Avatar Studio** | `Convai Avatar Creator` |
| No-code simulation product | **Convai Sim** | `Convai Simulator` |
| Quest capture app | **Convai XR Animation Capture App** | `XR app` |
| Narrative feature | **Narrative Design** | `narrative designer`, `story mode` |
| Memory feature | **Long-Term Memory** | `LTM` on first use |

A product's own interface always wins over this table for a label the reader clicks — if the button says something else, quote the button and tell the owner the label drifted.

* **CV-12:** Product names, UI labels, and menu paths match the product character for character, including casing. `Package Manager`, `Inspector`, `GameObject`, `Play mode`, `Project Settings`. When a class name and its menu label differ, use the menu label for clicking and the class name for code.
* **CV-13:** Explain or link a technical term the first time it appears on a page.

## Grammar and mechanics

| ID | Rule | Do | Don't | Exception |
|---|---|---|---|---|
| CV-14 | Serial comma | ✅ "torso, head, and eyes" | ❌ "torso, head and eyes" | |
| CV-15 | Spell out one through nine; numerals for 10 and above | ✅ "six dependencies", "24 pages" | ❌ "6 dependencies" | Numerals always for versions, step numbers, units, and technical values |
| CV-16 | Em dashes take no surrounding spaces | ✅ "The module—optional—ships separately." | ❌ "The module — optional — ships separately." | |
| CV-17 | Sentence case everywhere: titles, headings, table headers, card labels | ✅ "Configure the API key" | ❌ "Configure The API Key" | Product names and proper nouns keep their casing |

## Formatting

| ID | Element | Rule |
|---|---|---|
| CV-18 | Inline code | Format class names, methods, fields, enums, file paths, asset paths, package names, console messages, and literal values as `inline code` **everywhere** — in prose, in table cells, in list items, in step bodies. Table cells are not an exception. |
| CV-19 | UI elements | Bold the UI label exactly as the reader sees it: click **Convai > SDK Settings**. |
| CV-20 | Link text | Link text describes the destination. Never `click here`, `this page`, `read more`, or a bare URL as link text. |
| CV-21 | Lead-ins | Introduce a list, table, or code block that appears inside prose with a sentence ending in a colon. A list or table that directly follows its own section heading is introduced by that heading and needs no lead-in — adding one there produces the filler CV-3 bans. |
| CV-22 | Code fences | Every code block declares its language (`csharp`, `cpp`, `js`, `ts`, `python`, `yaml`, `json`, `bash`). A fence with no language is a failure. |
| CV-23 | Code correctness | Code examples compile and run, or carry an explicit `// pseudocode` comment. Never ship a snippet that silently does not compile. |
| CV-24 | Synchronized values | Never hard-code a version number, package identifier, dashboard URL, or server URL as plain text. Use the GitBook expression `<code class="expression">space.vars.name</code>`. The `{{ … }}` syntax is **wrong** and renders as literal text. _Exception: a historical version in a migration page ("retired in 4.2.0") is a deliberate frozen fact._ |

## Page structure

* **CV-25:** A page has exactly one title and therefore one H1. GitBook's editor writes it as a leading `#` heading and leaves `title` out of the frontmatter; pages written through the tooling put it in the frontmatter and have no body heading. Both are correct — what is never correct is two of them, or a second `#` further down the page.
* **CV-26:** The lead paragraph comes first and carries no heading of its own. On a page whose title is a leading `#` heading, it is the first thing after that heading. Sections start at `##`. A page that opens with a section heading has skipped the one paragraph that tells a reader whether they are in the right place.
* **CV-27:** No `## Overview`, `## Introduction`, `## Conclusion`, or `## Summary` heading at any level. The lead paragraph is the introduction; the ending is verification or next steps.
* **CV-28:** No vague headings: `More information`, `Miscellaneous`, `Basics`, `Tips`, `Notes`.
* **CV-29:** No `Step 1` / `Step 2` headings. Use an action title that names the outcome.
* **CV-30:** Do not use `####` on task or concept pages. If a fourth level is needed, restructure or split the page.
* **CV-31:** Do not skip heading levels.
* **CV-32:** Every page has a useful ending: a verification step, next steps, or a complete reference table.
* **CV-33:** The title is specific, keyword-first, and at most 60 characters — wherever it lives, frontmatter or leading heading.
* **CV-34:** `description` is one plain-English sentence stating the page outcome, 120–160 characters, hard maximum 200. It must not start with `This page covers`, `Learn about`, or `Overview of`, and must not contain class names, method names, file paths, or backtick identifiers — those belong in the body.
* **CV-35:** Set `last_reviewed` on any page whose accuracy depends on a specific SDK, engine, or API version.

## Content types

Every page has exactly one primary mode, and a page that mixes modes gets split. The four modes are:

| Mode | Use it for | The test |
|---|---|---|
| Tutorial | Teaching a beginner end to end | The reader learns by doing; success is guaranteed if they follow along |
| How-to | One specific task for someone already competent | The reader has a goal and needs the shortest correct path |
| Reference | Facts about a class, component, setting, or endpoint | The reader knows what they are looking for and needs it to be complete |
| Explanation | Why something works the way it does | The reader is trying to build a mental model, not do a task |

* **CV-36:** One primary mode per page. A how-to page does not become a reference page by growing a table of every field.
* **CV-37:** Every page is reachable — from the sidebar, a hub page, or a related-page link. No orphan pages.
* **CV-38:** A sidebar label matches that page's `title` exactly, in the same wording and case.

## GitBook blocks

GitBook gives you a fixed set of block types, and the table below covers every one of them. Plain Markdown where a block exists is the single most common thing a review catches, so before you hand off a page, do a **block-fit pass**: read the page once looking only for content whose shape matches a block, and upgrade it.

You never have to wonder whether a block exists for what you are writing — if it is not in this table, GitBook does not have it. Every block, and what we use it for:

| Block | Use it for | Our rule |
|---|---|---|
| **Paragraph** | Prose | The default. Every other block has to earn its place |
| **Heading** | Section structure | Second and third level only — see the page structure rules |
| **Unordered list** | Items with no order | Keep items parallel in grammar and length |
| **Ordered list** | Items with a real order that is not a procedure | For a procedure the reader performs, use a stepper |
| **Task list** | A checklist the reader ticks off | Prerequisites and pre-flight checks only. **CV-66** |
| **Hint** | A note, warning, danger, or success the reader must not miss | At most two per task or concept page. **CV-39** |
| **Quote** | Quoting an external source or a person | Never as a substitute for a hint. **CV-43** |
| **Code block** | Code, commands, configuration, log output | Always declares a language. **CV-22**, **CV-23** |
| **File** | A downloadable asset | Preferred over a link to an external host. **CV-67** |
| **Image** | A screenshot or a diagram | Always has alt text, and never carries information found nowhere else. **CV-47**–**CV-51** |
| **Embedded URL** | An external video, demo, or interactive tool | Only for a resource that renders for a logged-out reader. **CV-68** |
| **Table** | Tabular information | Real headers, never layout. **CV-44** |
| **Cards** | Routing readers to child pages | The default body of a hub or section index page |
| **Tabs** | Equivalent alternatives — platforms, install channels, languages | Equivalent, never unrelated. **CV-40** |
| **Expandable** | Optional detail a reader can skip | Never hides prerequisites, warnings, or required setup. **CV-41** |
| **Stepper** | A short linear procedure the reader performs | The default shape for a how-to page's main body |
| **Updates** | What changed in a release | Changelog and release-notes pages only. **CV-42** |
| **Drawing** | A freehand sketch | Do not use — use Mermaid. **CV-69** |
| **Mermaid** | Architecture, sequence, and state diagrams | Always has explanatory text around it. **CV-45** |
| **Math and TeX** | A formula prose cannot express cleanly | Rare here; also state what it means in words. **CV-70** |
| **Page link** | A strongly related page the reader should go to next | Preferred over an inline link for a genuine next step |
| **Prompt** | A reusable AI prompt the reader copies or opens in an AI tool | Only where the reader's next action really is an AI task. **CV-71** |
| **Columns** | Two genuinely parallel pieces of content | Never to compress a long page. **CV-72** |
| **Conditional content** | A small variation within one page | Full-page differences use content variants instead |
| **Reusable content** | A block that repeats identically across pages | Shared prerequisites and warnings. Edit once, changes everywhere |
| **OpenAPI** | REST and webhook reference | Generated from the specification, never hand-written. **CV-73** |

The enforceable rules:

* **CV-39:** At most two hints on a task or concept page. A page of hints has no emphasis left.
* **CV-40:** Tabs contain equivalent alternatives, never unrelated topics.
* **CV-41:** Expandable sections hide optional detail only — never prerequisites, warnings, or required setup.
* **CV-42:** Updates blocks appear only on changelog and release-notes pages.
* **CV-43:** Quote blocks are not a substitute for hints.
* **CV-44:** Tables carry tabular information, with real headers. Never use a table for visual layout.
* **CV-45:** A Mermaid diagram always has explanatory text around it. A diagram nobody explains is decoration.
* **CV-46:** Deprecated content carries a warning hint at the top naming the replacement and the version it changed in.
* **CV-66:** Task lists are for prerequisites and pre-flight checks the reader ticks off. Never use one for a procedure — a procedure is a stepper, because a stepper carries order and a checklist does not.
* **CV-67:** A downloadable asset uses a file block, not a link to an external host. An external host can go away; a file block cannot.
* **CV-68:** Embed a URL only when the resource renders for a reader who is not logged in to anything. Never embed something behind a login, and always say in prose what the embed shows — an embed that fails to load must not take the information with it.
* **CV-69:** Do not use drawings. A Mermaid diagram is text: it diffs in a pull request, it is searchable, an AI assistant can read it, and the next person can edit it. A drawing is none of those.
* **CV-70:** Use Math and TeX only where a formula is genuinely the clearest expression, and state what it means in prose as well. A reader using a screen reader gets nothing from the formula alone.
* **CV-71:** Use a prompt block only where the reader's next real action is an AI task — a troubleshooting prompt, an integration scaffold, a migration analysis. Write the prompt the way you want it used: state the task, define the output format, and name the constraints. Never use one as a novelty.
* **CV-72:** Use columns only for two genuinely parallel pieces of content, such as an explanation beside the image it describes. Never use columns to make a long page look shorter — side-by-side text is harder to read and reflows unpredictably on a phone.
* **CV-73:** An API reference page is generated from the OpenAPI specification, never hand-written. Use the operation block for one endpoint, the schemas block for shared models, and the webhook block for webhooks. When a fact on such a page is wrong, fix the specification, not the page.
* **CV-76:** Every paired GitBook block is closed. An unclosed hint, tabs, stepper, columns, or expandable block swallows the rest of the page on the published site, so an unbalanced block blocks publication rather than merely warning.

## Page options

Every page carries options beyond its content, and they are part of the page, so they are part of the review:

| Option | Our rule |
|---|---|
| Icon | Set one on hub and section index pages so cards and the sidebar read at a glance. Optional elsewhere, but consistent within a section |
| Cover image | Only on a section landing page, and only when the image says something. A decorative cover pushes the lead paragraph below the fold |
| Wide layout | Only when a table, a card grid, or a code block genuinely needs the width. **CV-74** |
| Hidden page | A page deliberately kept out of the sidebar. **CV-75** |
| Search indexing | Turn indexing off only for a page that must not appear in search results at all |
| Tags | Apply the section's existing tags; do not invent a new vocabulary per page |
| Sidebar label | Matches the page title exactly. **CV-38** |

* **CV-74:** Wide layout is a deliberate choice for content that needs the width, not a page default. Wide prose is harder to read than narrow prose.
* **CV-75:** A hidden page is still a real page: it has a title, a description, and an owner. If nothing links to it and nobody owns it, delete it rather than hiding it.

## Screenshots and images

* **CV-47:** Never use a screenshot for code, terminal output, log messages, console messages, or configuration text. Those are selectable text in a code block.
* **CV-48:** Every image has alt text that describes what the image shows, not what it is called.
* **CV-49:** A screenshot must not expose an API key, token, private project name, local username, internal path, email address, or another customer's content. Use a test account with test content.
* **CV-50:** A page does not publish with a placeholder image path or an unresolved screenshot marker.
* **CV-51:** On SDK pages a screenshot is a last resort, used where Inspector state, scene hierarchy, or visual output would otherwise be ambiguous. On product pages the default inverts: the reader is following along on screen, so show the panel they must find and the state that confirms the step worked.

## Technical accuracy

This is the section that matters most. A page that reads beautifully and states a class name that does not exist has done more damage than no page at all.

* **CV-52:** Never invent an API name, component, field, default value, limit, behavior, requirement, or console message. If a fact is missing, the page does not state it — raise it as an open question instead.
* **CV-53:** Every technical claim is verified against the product's source of truth before it is written: SDK source code for SDK pages, the running product or its named owner for product pages, the agreed facts for a customer's pages.
* **CV-54:** A repository's own `README.md`, `docs/`, or `CHANGELOG.md` is a lead, not proof. Find the definition in the code and cite that. If code and prose disagree, the code wins.
* **CV-55:** Never fabricate a changelog or release-notes entry. Every entry traces to real source history — a commit, a version bump, or maintainer-provided notes.
* **CV-56:** State the prerequisites a page depends on: required SDK version, engine version, plan tier, entitlement, or permission.
* **CV-57:** Document the known failure modes. Each troubleshooting entry gives symptom, cause, fix, and verification, and quotes the exact console message where one exists.

## Accessible and inclusive writing

* **CV-58:** Do not convey meaning by colour, position, or direction alone. Name the element instead of "the green button" or "the panel on the right"; prefer "earlier" and "later" over "above" and "below".
* **CV-59:** Essential information is never available only inside an image.
* **CV-60:** Gender-neutral language. Singular "they" when gender is unknown or irrelevant — never "he or she".
* **CV-61:** Replace ableist and violent idioms: "confirmation check" not "sanity check"; "stop the process" not "kill the process" (the literal `kill` command keeps its name).

## Publishing

* **CV-62:** Documentation changes are prepared on the `staging` branch and reviewed in the Staging space before a pull request to `main`. Nothing AI-generated goes straight to `main`.
* **CV-63:** A change request description names the source of truth used for technical claims and any assumption made.
* **CV-64:** A human, not an agent, gives the final approval on any change request.
* **CV-65:** When a page moves or is renamed, add a redirect in the same change, and update its `SUMMARY.md` label in the same change.

## Ownership and updates

* **Owner:** Kaan Eray Akay (kaan@convai.com)
* **Review cadence:** once per SDK release cycle, and quarterly for anything not otherwise touched
* **How to propose a change:** open a pull request against `Conv-AI/convai-docs-tools`, editing `skills/convai-docs/gitbook/styleguide.md`, then re-pin the registry with `tools/check_rules.py --update <date>`. Say in the commit message which page the rule was going to make worse — that is the evidence a reviewer needs.
* **When settled decisions can be revisited:** when a rule demonstrably makes a real page worse. Record the outcome in the decision log below.

## Decision log

| Date | Decision | Rationale |
|---|---|---|
| 2026-08-18 | The backend is called "Convai", never `Convai cloud` or `the Convai backend` (CV-10) | Readers were treating "the backend" as a separate product they had to configure. Naming one thing one way removed the question. |
| 2026-08-18 | Synchronized values use GitBook variables, never literals (CV-24) | A pack that printed the SDK version as `4.2.0` while the repository said `4.5.0` was a source of wrong facts for months. |
| 2026-08-18 | A repository's own docs are a lead, not proof (CV-54) | Every wrong fact this system has shipped entered through prose that nothing recompiles when the code changes. |
| 2026-08-18 | Drawings are banned in favour of Mermaid (CV-69) | A drawing cannot be diffed, searched, or read by an AI assistant, so it goes stale invisibly. |
| 2026-08-18 | The guide holds itself to its own rules, starting with its own description (CV-34) | The first review of this page flagged that it violated CV-34. A standard its own author exempts is not a standard. |
| 2026-08-18 | Banned terms are quoted as inline code wherever the guide names them (CV-18) | A rulebook has to contain the words it bans. Marking them as code keeps a checker from reading a definition as a violation. |
| 2026-08-18 | CV-21 applies to lists and tables inside prose, not to one that directly follows its own heading | A review flagged every reference table on this page. Demanding "Use these patterns:" under a heading that already says it produces the filler CV-3 bans, so the rule was narrowed rather than the pages padded. |
| 2026-08-18 | A page may carry its title in the frontmatter or as a leading `#` heading, but never both (CV-25, CV-26, CV-33) | The rule demanded frontmatter and no body heading. Measured against the repository it failed 89 pages across three whole sections, because GitBook's editor writes the other shape when it round-trips a page. A rule that fails every page authored on the platform it serves is a broken rule; what it was protecting — one title, machine-findable, never two — is unchanged. |
| 2026-08-18 | An unbalanced GitBook block blocks publication rather than warning (CV-76) | An unclosed hint or tabs block swallows the rest of the page on the published site, so the reader loses everything after it with nothing to indicate why. |
