# Page structure, metadata, and headings

How one GitBook page is shaped: frontmatter, title, description, lead paragraph, headings, ending, and
links. Where a page goes is in `structure.md`; the skeleton for each page type is its template.

A page is a Markdown file with YAML frontmatter. Its audience is whoever the subject file names: for
SDK and API sections, developers building an integration; for the Playground and no-code sections, a
creator or operator using the product UI. Getting Started pages assume limited experience; advanced
and reference pages may assume domain fluency.

## Frontmatter keys

A normal new page sets `title` and `description` only. Add another key only when its row applies.

| Key | When to set it |
|---|---|
| `title` | Always on a new page. Matches the `SUMMARY.md` sidebar label exactly. |
| `description` | Always. |
| `last_reviewed` | A page whose accuracy depends on an SDK, plugin, or engine version: install pages, scripting reference, compatibility tables, version-specific how-tos. Set to the version you verified against (CV-35). |
| `icon` | Every top-level page and hub page, from the space's allowed list (CV-81). |
| `hidden` | A page that must exist but stay out of the sidebar, with the reason in the change summary. Every site check lists it (CV-78). |
| `noIndex` | Never on a hub or section index page (CV-77). Elsewhere only for a page that must not appear in search engines: confirm with a person first, and add it with its reason to `.convai-docs/noindex-allowlist.txt`. |
| `cover`, `layout` | Landing and hub pages only, where the section already uses them. |

## Where the title lives

A page edited in GitBook's web editor has a leading `# Title` heading and no `title` key; a page
written through this tooling has `title:` in the frontmatter and no body heading. Both render, and the
linter accepts both. A page with neither, with both, or with a second `#` heading further down has two
strings claiming to be the title, so the sidebar, the search result and the page can disagree (CV-25).
Do not convert a page between the two shapes as a drive-by change: GitBook converts it back, and the
diff hides the real change.

## Title and description

The title names one reader question, the one the page answers (CV-89). It is specific, sentence case,
keyword-first, at most 60 characters (CV-33), and unique within its space (CV-91): `Install the Unity
SDK`, not `Installation` or `Getting started with the Convai Unity SDK for Unity Developers`.

The description is one plain-English sentence stating the outcome, 120 to 160 characters, hard maximum
200 (CV-34). It never starts with "This page covers", "Learn about", or "Overview of"; never contains
class names, method names, file paths, or backtick identifiers; never promises ease or speed; makes no
unsupported marketing claim; and never just repeats the title. Good: `Add the Convai Unity SDK to a
Unity project and verify that the package loads correctly.` Bad: `This page covers SDK installation.`
A page type's description formula, where it has one, is in its template's opening comment.

## Lead paragraph

Headingless, one to three short sentences, with no `## Introduction` or `## Overview` and no filler
such as "In this guide…" (CV-26, CV-27). Its first sentence answers the question the title asks (CV-88)
and uses the page's main topic naturally. It says what the page is about (`Install the Convai Unity SDK
into an existing Unity project.`), who or when it is for (`Use this page when setting up the SDK for
the first time.`), and the outcome (`At the end, Unity loads the package without errors.`).

## Headings

Sections start at `##`; `###` marks a subsection only when it improves scanning. Never `####` on a task
or concept page: split the page (CV-30). A dense reference page may use it when a third sub-level is
the only alternative. A normal task page has four to seven useful `##` sections, a short reference page
fewer; the first is usually prerequisites, setup, or the core concept.

| Content intent | Heading pattern | Good | Bad |
|---|---|---|---|
| Procedure | Base verb + object | `Configure the API key` | `API key configuration` |
| Verification | Base verb + result | `Verify the installation` | `Testing` |
| Concept | Noun phrase | `Audio input pipeline` | `Understanding audio input` |
| Reference | Object or factual category | `Events` | `Using events` |
| Troubleshooting | Symptom or task | `Package URL cannot be resolved` | `Issue 1` |
| Next action | Standard section name | `Next steps` | `Conclusion` |

- Do not skip heading levels (CV-31) or put links inside headings.
- No numbered headings like `Step 1` (CV-29), and no vague ones: `Overview`, `Basics`, `Advanced`,
  `More information`, `Miscellaneous`, `Conclusion`, `Summary` (CV-27, CV-28).
- No one-word heading unless the word is a precise reference object.
- No two headings back-to-back without text between, except a compact entry in a reference page.
- Keep headings stable once published: the heading is the anchor in the URL that other pages and sites
  link to, and rewording it silently breaks them.

The outline alone should show the page's flow: `Prerequisites → Install the package → Configure the API
key → Verify the installation → Troubleshooting → Next steps`, never `Overview → Setup → Usage →
Advanced → More information → Conclusion`.

## Endings

Every page has a useful ending: a verification step, next steps, or a complete reference table (CV-32).
A task page ends with two to five next-step links in `{% content-ref %}` blocks, never a "Related
articles" dump. Add a troubleshooting section when the feature has known failure modes, and split it
into its own page when it grows large. Avoid a summary unless the page genuinely needs a recap.

## Links and reachability

Every page is reachable from the sidebar, a parent hub page, a related-page link, or a next steps
section (CV-37). Link when the reader's intent changes (task to concept, task to reference, concept to
how-to), with link text that names the destination, never "click here" (CV-20), and link to the source
of truth instead of repeating it. A page that belongs in the sidebar gets its `SUMMARY.md` entry in the
same change: the smallest change, in the existing order, with the label equal to the page `title`
(CV-38).
