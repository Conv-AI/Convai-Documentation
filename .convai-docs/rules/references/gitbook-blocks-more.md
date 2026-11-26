# GitBook blocks for particular pages

The blocks most pages never need. `page-types.md` says which page types read this file.

| Content need | Block |
|---|---|
| A relationship prose cannot express cleanly | Math and TeX |
| Prerequisite or pre-flight checklist the reader ticks off | Task list |
| Content identical on several pages | Reusable content (snippet) |
| Small variation by version, platform, or role within a page | Conditional content |
| Downloadable file: sample project, config template, script | File block |
| Attributed third-party quote | Quote block |
| External URL with a rich preview: video, repository, tool | Embed |
| A reusable AI prompt the reader runs | Prompt block |

## Math and TeX

Use a math block only where a formula is genuinely the clearest expression of a relationship — a
sample-rate conversion, a blend weight, a coordinate transform. It is rare in this documentation.

Always state what the formula means in prose as well. A reader using a screen reader, and an AI
assistant answering a question, get nothing from the rendered formula alone.

## Task lists

Use a task list for a checklist the reader ticks off as they work — prerequisites before a setup page,
or a pre-flight check before a build. It is not a procedure. A procedure carries order and a checklist
does not, so anything the reader performs in sequence belongs in a stepper instead.

```md
* [ ] Unity project set to the Android build target
* [ ] Convai API key configured in `ConvaiSettings`
* [ ] Microphone permission granted in Player Settings
```

Never use a task list as a substitute for real prose about what each item means. If an item needs
explaining, it needs a section, not a checkbox.

## Reusable content (Snippets)

Use reusable content for blocks that appear identically on multiple pages: shared prerequisites,
standard environment requirements, repeated API key warnings, or boilerplate setup steps. Create a
snippet once, then insert it by reference. Editing the source updates every page that uses it, instead
of copy-pasting the same content by hand.

Rules: use snippets for content that must stay byte-for-byte identical across pages; do not
snapshot-copy snippet content into pages; name snippets descriptively (`prerequisite-unity-2022-3`,
`warning-api-key-commit`); treat snippets as a shared codebase — review impact before editing a
widely-used snippet. In this repo, snippets live under `.gitbook/includes/`.

## Conditional content

Use conditional content blocks to show or hide sections based on visitor context — without duplicating
the page or writing separate pages for differences that affect a few blocks. Supported conditions: URL
parameter, cookie, feature flag, visitor token.

Rules: use when the variation is small (a few blocks) — if entire page sections differ, use Content
Variants; never hide required safety warnings or prerequisites behind a condition; every conditional
block must have a sensible default; document active conditions in space settings; do not use
conditional content as a substitute for a well-split page.

## File blocks

Use file blocks to attach downloadable assets directly to a page: sample projects, migration scripts,
configuration templates, or exported settings files, never a link to an external host that may go
offline. Store files in `.gitbook/assets/`. Name files descriptively. Do not use file blocks for content
that should be selectable text — use code blocks.

## Quote block

Use the Quote block for attributed third-party quotes or pull quotes that require typographic
distinction. Do not use quote blocks for ordinary emphasis or as an alternative to hint blocks. SDK
documentation rarely needs quote blocks.

## Embed blocks

Use embed blocks for external URLs where a rich link preview adds context — demo videos, repositories,
interactive tools.

```md
{% embed url="https://www.youtube.com/watch?v=EXAMPLE" %}
```

Use embed blocks for content the reader needs to watch or interact with, not for general references.
Plain inline links are better for URLs that require no preview. Do not embed URLs that add no context,
are likely to change, go offline, or require authentication.

## Prompt blocks

A prompt block holds a reusable AI prompt. The reader copies it in one click or opens it directly in a
supported AI tool.

Use one only where the reader's next real action is an AI task: a troubleshooting prompt that collects
the right diagnostic information, an integration scaffold, a migration analysis over their own project.
Do not add one as a novelty, and do not use one where a code block or a procedure is what the reader
actually needs.

Write the prompt the way you want it used: state the task, define the output format, and name the
constraints, exactly as the writing standards require of any instruction.
