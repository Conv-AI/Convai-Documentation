# Page structure, metadata, and headings

SDK-agnostic rules for how a GitBook page is shaped: the publishing model, frontmatter, headings, the
single-page skeleton, and file naming. SDK-specific product names and values come from the SDK pack.

## Core publishing model

| Item | Standard |
|---|---|
| Source format | Markdown files in the docs repository, with YAML frontmatter. |
| Publishing target | GitBook. Default workflow is Git Sync from the `staging` branch. Treat `staging` as the sync source and follow the branch workflow in `safe-publishing.md`. |
| GitBook page title | Set in GitBook UI or mapped from frontmatter during import. This is the page H1. Must be ≤ 60 characters. Lead with the primary keyword. |
| Markdown body | Must not duplicate the GitBook page title with a `#` heading. Start with a lead paragraph, then use `##` sections. |
| Page description | Stored in frontmatter and copied into GitBook page description. Target 120–160 characters. Hard maximum 200 characters. |
| Heading style | Sentence case, not title case. |
| Audience | Whoever the pack names. For SDK and API sections that is developers building an integration; for the Playground and no-code sections it is a creator or operator using the product UI. Getting Started pages assume limited experience; advanced and reference pages may assume domain fluency. |

## Required single-page structure

```md
---
title: Install the Unity SDK
description: Install the Convai Unity SDK package, add required project settings, and verify that the SDK loads in Unity.
---

Install the Convai Unity SDK into an existing Unity project and confirm that the runtime components are available in the editor.

## Prerequisites

...

## Install the package

...

## Verify the installation

...

## Troubleshooting

...

## Next steps

...
```

### Metadata and headings

| Element | Rule |
|---|---|
| `title` frontmatter | Same as the GitBook page title unless the import process sets it manually. Specific, unique, sentence case. |
| `description` frontmatter | One sentence. Target 120–160 characters; hard max 200. State the outcome, not "This page covers..." |
| GitBook page title | The platform H1. Do not duplicate it in Markdown body. |
| Lead paragraph | Headingless. One to three short sentences that confirm scope, audience, and outcome. |
| `##` headings | Main body sections. These should form the useful page outline. |
| `###` headings | Subsections under a `##`. Use only when they improve scanning. |
| `####` headings | Avoid. Use only in dense reference pages where a third sub-level is the only alternative. If you reach `####` in a task or concept page, split the page instead. |

### Frontmatter keys

Only `title` and `description` are set on a normal new page. The rest are deliberate exceptions — do
not add one unless the row below says the page needs it.

| Key | When to set it |
|---|---|
| `description` | Always. Every page has one. |
| `title` | Always on a new page. Must match the `SUMMARY.md` sidebar label exactly. |
| `last_reviewed` | Any page whose accuracy depends on a specific SDK, plugin, or engine version — install pages, scripting reference, compatibility tables, version-specific how-tos. Set it to the version you verified against. |
| `icon` | Only when the section already uses icons consistently. Do not introduce icons into a section that has none. |
| `hidden` | A page that must exist but stay out of the sidebar. Needs a stated reason in the change summary. |
| `noIndex` | A page that must not appear in search engines. Rare; confirm with a human first. |
| `cover`, `layout` | Landing and hub pages only, and only where the surrounding section already uses them. |

### Where the title lives

A page carries its title in one of two places, and which one depends on who last edited it.

| Last edited in | Shape |
|---|---|
| GitBook's web editor | A leading `# Title` heading; no `title` key in the frontmatter |
| The repository, through this tooling | `title:` in the frontmatter; no body heading |

Both render correctly, and the linter accepts both. What it rejects is a page with neither, a page with both, or a second `#` heading further down: in each of those cases two strings claim to be the title, and the sidebar, the search result and the page itself can disagree.

Do not convert a page from one shape to the other as a drive-by change. Editing it in GitBook converts it back, and the diff is noise that hides the real change.

### Do not use a second body `#` heading

Because GitBook already has a page title, Markdown pages intended for manual import should not start
with `#`. The first body content is a headingless lead paragraph; the first heading is `##`.

### Intro and ending sections

| Section | Rule |
|---|---|
| Intro | No heading. Do not use `## Introduction` or `## Overview`. |
| Summary | Avoid unless the page genuinely needs a recap. |
| Next steps | Use when there is a clear next page, setup continuation, or related task. |
| Troubleshooting | Add when the feature has known failure modes. Split into a separate page if it becomes large. |

## Page metadata decision table

| Field | Required standard | Good | Bad |
|---|---|---|---|
| GitBook page title / `title` | Unique, specific, sentence case, one user intent, ≤ 60 characters, keyword-first | `Install the Unity SDK` | `Installation`, `Getting started with the Convai Unity SDK for Unity Developers` |
| Description | One sentence, target 120–160 chars (hard max 200), outcome-focused | `Add the Convai Unity SDK to a Unity project and verify that the package loads correctly.` | `This page covers SDK installation.` |
| Lead paragraph | Headingless, 1-3 short sentences, confirms scope and outcome | `Install the Convai Unity SDK into an existing Unity project and confirm that Unity loads the package without errors.` | `## Overview` followed by filler |
| First body heading | Starts at `##`; usually prerequisites, setup, or core concept | `## Prerequisites` | `# Install the Unity SDK` |
| Sidebar label | Short but still meaningful | `Unity SDK install` | `Setup` |
| Slug/file name | Lowercase, hyphenated, readable | `install-the-unity-sdk.md` | `install.md` |

## Description formula

| Page type | Formula | Example |
|---|---|---|
| Tutorial | `Build [result] by [main method/context].` | `Build your first Convai character in Unity and verify that it responds in Play mode.` |
| How-to | `[Action] [object] so [outcome].` | `Configure microphone input so a Unity character can receive player speech.` |
| Reference | `Reference for [API/component], including [key facts].` | `Reference for ConvaiCharacter, including required fields, events, and runtime behavior.` |
| Explanation | `Understand [system/concept], including [scope].` | `Understand the conversation lifecycle between Unity, the SDK, and Convai.` |
| Troubleshooting | `Fix [specific failure] in [context].` | `Fix common Unity Package Manager errors when installing the Convai Unity SDK.` |
| Hub | `Find guides for [section purpose].` | `Find setup, configuration, and verification guides for the Convai Unity SDK.` |

Descriptions must not exceed 200 characters (target 120–160), start with "This page covers", "Learn
about", or "Overview of", promise ease or speed, contain unsupported marketing claims, or repeat the
title without adding outcome or scope.

## Lead paragraph formula

The lead paragraph should answer three questions without a heading:

| Question | Example answer |
|---|---|
| What is this page about? | `Install the Convai Unity SDK into an existing Unity project.` |
| Who or when is it for? | `Use this page when setting up the SDK for the first time or validating a clean project.` |
| What is the outcome? | `At the end, Unity should load the package without errors.` |

## Heading decision table

| Content intent | Heading pattern | Good | Bad |
|---|---|---|---|
| Procedure | Base verb + object | `Configure the API key` | `API key configuration` |
| Verification | Base verb + result | `Verify the installation` | `Testing` |
| Concept | Noun phrase | `Audio input pipeline` | `Understanding audio input` |
| Reference | Object or factual category | `Events` | `Using events` |
| Troubleshooting | Symptom or task | `Package URL cannot be resolved` | `Issue 1` |
| Next action | Standard section name | `Next steps` | `Conclusion` |

Heading rules:

- Use one H1 only: the GitBook page title.
- Start body sections at `##`. Do not skip heading levels.
- Do not put links inside headings.
- Do not use numbered headings like `Step 1`.
- Do not use one-word headings unless the word is a precise reference object.
- Do not put two headings back-to-back without explanatory text, unless the second heading opens a
  compact reference entry in a reference page.
- Keep headings stable once published. Heading text becomes the anchor in the page URL, and other teams
  and external sites link to those anchors. Rewording a heading silently breaks them.

A reader should be able to scan only the outline and understand the page flow. Good outline:
`Prerequisites → Install the package → Configure the API key → Verify the installation →
Troubleshooting → Next steps`. Bad outline: `Overview → Setup → Usage → Advanced → More information →
Conclusion`.

## File naming and location

| Item | Standard |
|---|---|
| Page file | One `.md` file per page. |
| File name | Kebab-case English based on the page title, such as `configure-api-key.md`. Lowercase only. |
| Section index | `README.md` inside the section folder. Every folder that holds pages has one. |
| Folder structure | Mirrors the GitBook navigation tree exactly. `SUMMARY.md` indentation equals folder depth. |
| Images | All assets live in the shared, flat `.gitbook/assets/` pool, referenced by relative path. There are no per-folder image directories. |
| Variables | Defined in `.gitbook/vars.yaml`. See `writing-standards.md`. |
| Root structure | Do not change it as part of a page-writing task. |

### Where a page belongs

The documentation repository has four top-level content sections. Pick the one that matches what the
page is about, not which team wrote it.

| Section | Holds | Example page path |
|---|---|---|
| `convai-playground/` | The Convai web dashboard and character builder UI | `convai-playground/character-customization/knowledge-bank.md` |
| `no-code-experiences/` | Products used without writing code — Avatar Studio, Convai Sim, XR capture | `no-code-experiences/avatar-studio-experiences/customizing-your-avatar/face-filter.md` |
| `plugins-and-integrations/` | Engine SDKs and plugins, one folder per integration | `plugins-and-integrations/convai-unity-sdk/getting-started/install-the-unity-sdk.md` |
| `api-reference/` | REST and realtime API contract documentation | `api-reference/core-api-reference/live-apis-beta/connect-api.md` |

`README.md` at the repository root is the Welcome landing page. `SUMMARY.md` groups the sidebar under
one `##` heading per section, in the order above.

If a page does not fit any of the four, stop and ask where it belongs. Do not create a fifth top-level
section as part of a page-writing task.

### Renaming and moving pages

There is no `.gitbook.yaml` in the repository, so **no redirect map exists**. Renaming a file or folder
changes the published URL and breaks every external link, bookmark, and search result pointing at it.

- Do not rename or move an existing page unless the task is explicitly a restructuring task.
- When a move is genuinely required, list every inbound link you found and flag the URL change in the
  change summary so a human can decide whether a redirect needs to be configured in GitBook first.
- Getting the slug right on the first publish matters more than it looks. Choose the file name from the
  page title, not from the folder it happens to sit in.
