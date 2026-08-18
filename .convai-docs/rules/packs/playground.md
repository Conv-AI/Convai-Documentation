# Convai Playground pack

Facts for documenting the Convai Playground: the web application where a creator builds, configures,
tests, and publishes a character without writing code. Generic doctrine lives in `references/`.

The Playground has a source repository, so most of what a page needs to state is verifiable in code
rather than guessed from a screenshot. Read "Source of truth and verification" before writing anything —
it says exactly which file settles which kind of claim, and which claims code cannot settle.

Last audited: 2026-08-18 against `Conv-AI/convai-playground` at `3777d67`.

---

## What this pack covers

Pages under `convai-playground/` in the documentation repository:

- `get-started/` — dashboard orientation, creating a character, testing it, versioning, voice mode
- `character-customization/` — one page per surface of the character editor

Out of scope, with the pack that owns each:

| Subject | Pack |
|---|---|
| Avatar Studio, Convai Sim, XR Animation Capture App | `no-code.md` |
| Engine SDK and plugin integration | `unity.md`, `unreal.md`, `web.md` |
| REST and realtime API contracts | `core-service.md` |

Avatar Studio is reachable from the Playground but is a separate product with its own pages. A
Playground page links to it; it does not document it.

## Product naming

- The product is the **Convai Playground**. Shortened to **the Playground** after first mention on a
  page.
- A thing a creator builds is a **character**, lowercase in prose. Capitalize it only when quoting a UI
  label exactly.
- Do not call it an "agent", a "bot", an "NPC", or an "assistant". The SDK packs use their own
  engine-side terms; this pack does not inherit them.
- Do not write "Legacy Playground" for the current product. That name refers to the older interface and
  means something specific to readers — and to the code, which disables several tabs with the tooltip
  "This feature is currently available in legacy playground only".
- Refer to Convai's backend as **Convai**. Never "Convai cloud", "Convai's servers", or "the backend".

## Audience

Creators, designers, writers, and product people configuring a character through the interface. Assume
no programming knowledge and no engine knowledge. A reader who has never opened a code editor must be
able to complete every procedure on these pages.

Two exceptions where technical knowledge is fair to assume, and only on those pages: **MCP and APIs**
and anything covering the external API surface.

Baseline before starting: a Convai account and access to the Playground.

## Source of truth and verification

**Repository:** `Conv-AI/convai-playground`. A Next.js monorepo; the Playground itself is `apps/web`.
The path is per-machine — ask for it, never guess it.

### What the code settles

| Claim | Where to verify |
|---|---|
| Which tabs exist, their exact labels, their order, which are disabled | `apps/web/src/navigation/tab-definitions/character-editor-tabs.ts` |
| A tab's sub-tabs and their labels | the same file's `*_SUB_TABS` constants |
| Field labels, placeholders, helper text, tooltips | `apps/web/src/sections/character/character-edit/<tab>/` |
| Client-enforced limits and defaults | that tab's `constants.ts` |
| Exact toast and warning strings | that tab's `constants.ts` |
| Which capability path gates a tab or section | the `capabilityPath` / `anyOfCapabilityPaths` fields in the tab definitions |
| Routes and deep links | `packages/routes/src/paths.ts` |

There is **no i18n layer**. Every user-facing string is an inline English literal in TSX or a
per-feature `constants.ts`, so a label is found by reading the component, not a translation file.

### What the code cannot settle

These need the product owner, or a look at the running product. Do not infer them:

- **Backend-enforced limits.** Several limits are fetched at runtime and only fall back to a local
  constant. The character word limit is the clear case: the local default is 1000, but the real value
  comes from `projectSettingsService.getCharacterWordLimit()` and is server-controlled. Stating the
  local constant as the limit is stating a fallback as a fact.
- **Plan and tier gating.** There is no plan map in the repo. Tabs are gated by boolean capability
  paths resolved from a feature-flags endpoint at runtime, and a missing flag defaults to enabled. The
  code gives you the capability path name; only the backend knows which plan turns it on.
- **Rendered appearance.** Spacing, colour, and where something sits on screen.

### What does not count as proof

An in-repo `docs/` folder, a `README.md`, a `CLAUDE.md`, an existing published page, a marketing page,
or a memory of the interface. The Playground repo has a genuinely useful `docs/` directory covering
architecture — read it to orient yourself, then verify every fact you take from it against the code.
It is prose that nothing recompiles when a constant changes. See "In-repo documentation is a lead, not
a source of truth" in `references/safe-publishing.md`.

If a fact cannot be proven from code and nobody has confirmed it, the page does not state it. A
plausible guess about a UI is indistinguishable from a fact to the reader, and it is what sends them to
support.

## The character editor

This is the backbone of `character-customization/`, so its structure is worth stating once here.
**Verify the current list against `character-editor-tabs.ts` before writing** — it changes.

At the time of writing, the top-level tabs were: Description, Avatar, Knowledge Bank, Core AI Settings,
MCP and APIs, Guardrails, State Of Mind, Embodied Actions, Narrative Design, Publish, Memory, Mindview.

Three things about that list matter for documentation:

- **A tab's label is not always its documentation page title.** The tab reads "Description"; the
  documentation page for it is "Character Description". Use the tab's exact label when telling a reader
  where to click, and the page title for the page itself.
- **Some tabs are disabled with a legacy-only tooltip.** Embodied Actions and Narrative Design are in
  this state in the code. A page that walks a reader into a disabled tab is a wrong page — check the
  `disabled` flag and the tooltip before documenting a surface.
- **One tab renames itself when a capability is denied**: MCP and APIs appears as "External API" for
  users without it. If a page names that tab, it has to account for both labels or say which one it
  assumes.

Publish, Memory, and the Description tab have sub-tabs. Sub-tabs are usually sections within one page
rather than pages of their own — decide by reader intent, not by mirroring the UI tree.

## How to document one configuration surface

This is the most common page in this section, so the shape is worth stating.

A configuration-surface page is a **how-to** with a reference table, not a tour of the screen. The
reader arrived because they want to achieve something with that panel.

1. **Lead paragraph** — what this surface controls and what changes about the character when you use
   it. Not "this page explains the Description tab".
2. **A screenshot of the panel**, first time you send the reader there.
3. **The task**, as steps. Where to click, using the tab's exact label from the code.
4. **A field table** — every field, what it does, its limit or default, whether it is required. Take
   the labels and limits from the component and its `constants.ts`; mark any limit that is
   backend-controlled as such rather than printing the fallback.
5. **What good input looks like** — one worked example. This is what makes a configuration page useful
   rather than a restatement of the form.
6. **Next steps** — content refs to the surfaces a reader usually configures next.

Do not document a field by restating its label. "Character's Name — the name of the character" tells
the reader nothing they could not see. Say what it affects.

## Screenshot policy

The SDK default is inverted here: a Playground reader is following along on screen, so showing the
screen is usually the clearest instruction available. Existing pages carry roughly four to seven
figures each, and that density is appropriate.

Required:

- Any panel the reader must find, the first time the page sends them there
- Any control that is easy to confuse with a neighbouring one
- Any state the reader must recognise to know a step worked

Not a screenshot, ever — these stay selectable text in a code block: JSON, API payloads, error
messages, log output, configuration text, and anything the reader might copy.

There is **no Storybook** in the repo, and the Playwright end-to-end specs do not cover most surfaces,
so screenshots come from running `apps/web` or from someone with Playground access. Plan for that: a
page needing new screenshots is blocked on a person, and the placeholder should say exactly what to
capture.

Every screenshot must use a test account with test content. Never capture a real customer's character,
a real end user's conversation, an API key, billing information, or another account's data.

Use the GitBook figure syntax already used throughout this section, with real alt text:

```md
<figure><img src="../../.gitbook/assets/knowledge-bank-upload.png" alt="The Knowledge Bank panel with one uploaded document listed"><figcaption><p>Uploaded documents appear in the Knowledge Bank list.</p></figcaption></figure>
```

## Feature and rollout state

A reader who follows a guide and cannot find the control has been handed a wrong fact.

- Check the tab definition for `disabled` and for a capability path before documenting a surface.
- State the requirement in the page's prerequisites when a feature needs a specific plan tier — and get
  that from the owner, because the repo only has the capability path name, not which plan grants it.
- Label a beta surface as beta in the lead paragraph, not only in a hint at the bottom.

## GitBook variables

`.gitbook/vars.yaml` in the documentation repository is the only authority for values.

| Variable | Holds | Derive from | Used in |
|---|---|---|---|
| `dashboard_url` | Convai dashboard URL | Stable product URL | Sign-in steps, links out to the Playground |

If a Playground page needs a synchronized value that has no variable yet, add it to `.gitbook/vars.yaml`
in the same change rather than writing the literal into the page.

## Gold-standard example pages

**No page in `convai-playground/` currently meets the quality bar.** Every page sampled carries a body
`#` H1, most open with `## Introduction`, none set `title` frontmatter, and several close with
`## Conclusion`. All four are doctrine violations. Do not model a new page on them.

Until a Playground page is written to standard and accepted, model structure and tone on the Unity SDK
section, which does meet the bar, and adapt the audience:

| Mode | Model page |
|---|---|
| How-to | `plugins-and-integrations/convai-unity-sdk/getting-started/installation.md` |
| Hub | `plugins-and-integrations/convai-unity-sdk/README.md` |

Take the structure, frontmatter, block usage, and heading discipline from those pages. Do not take
their voice: they are written for a developer, and this audience is not one.

**When the first Playground page is written to standard and accepted, replace this section with that
page's path.**

## Section layout

```
convai-playground/
├── README.md                       section hub
├── get-started/
│   ├── README.md                   subsection hub
│   └── <task>.md                   one page per first-run task
└── character-customization/
    ├── README.md                   subsection hub
    └── <surface>.md                one page per configuration surface
```

One page per configuration surface. A surface that grows past a single reader goal gets split, with the
parent becoming a hub.

## Known violations in existing pages

These are what a writer will find when opening this section. Fix them only when the task covers that
page; do not silently rewrite pages the task did not ask about.

| Pattern | What is wrong | What to do instead |
|---|---|---|
| Body `# Title` H1 on every page | Duplicates the GitBook page title, which is already the only H1 | Delete it. Start with a headingless lead paragraph. |
| `## Introduction` opening section | Forbidden heading; delays the content | Delete the heading and fold its content into the lead paragraph. |
| Missing `title` frontmatter | Sidebar label cannot be matched to the page title | Add `title`, identical to the `SUMMARY.md` label. |
| `## Conclusion` closing section | Vague heading; usually restates the page | Replace with `## Next steps` and content refs, or delete it. |
| Plain "Continue to: _Page_" lists on hub pages | Not a GitBook navigation block | Use `{% content-ref %}` or cards. |
| Hardcoded values in prose | Goes stale silently | Use a `space.vars` expression. |
| Empty `alt=""` on figures | Fails accessibility and gives an AI assistant nothing to read | Write alt text describing what the image shows. |
| Broken link in `character-customization/README.md` — the Personality Traits entry points at `knowledge-bank.md` | Sends the reader to the wrong page | Point it at `personality-traits.md`. |

## What must never be documented

- Internal admin or moderation tooling
- Unreleased features, including anything behind an internal capability flag that is off by default
- Pricing or plan limits not already published on Convai's public pricing page
- Another customer's characters, content, or configuration
- Internal service names, repository names, capability path strings, or ticket links
