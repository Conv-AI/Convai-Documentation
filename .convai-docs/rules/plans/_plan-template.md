# Documentation plan format

A documentation plan is the agreed scope for building an area's docs from scratch, or for a scoped part
of one. The `docs-planner` produces one per subject at `.convai-docs/plans/<pack>.md`; the `docs-writer`
(driven by `/build-docs`) consumes it one **work unit** at a time. The plan is a tooling artifact — it
is not a GitBook page and never goes in `SUMMARY.md`.

Copy this shape when generating a plan. Keep it scannable. Every page row must name its source of truth
so writing never invents behavior.

## The plan header states the pack kind

The kind decides what a row's "Source of truth" column is allowed to contain, and everything downstream
reads it. Put it in the header:

| Pack kind | Source-of-truth column holds | Example |
|---|---|---|
| SDK | A code path, class, or sample asset | `Source/ConvaiCore/Public/ConvaiChatbot.h` |
| Topic | A named screen, or the owner when only they can settle it | `Knowledge Bank panel — screenshot 2026-05-08`, or `owner: <name>` |
| Customer | A row in the customer pack's facts table | `facts table: negotiated rate limit` |

A topic or customer plan will have rows whose source is the owner. That is expected and correct — those
rows are questions, and `/build-docs` skips them until the owner has answered. A row that quietly
asserts an unverified fact is the failure mode this column exists to prevent.

For a topic plan, the header names the owner. For a customer plan, it also records the destination,
visibility, and approver from the pack, because those govern where the finished pages may go.

---

## Work units (review batches)

The plan is organized into **work units**. A work unit is one coherent group of pages that is written
together and then reviewed together before the next unit starts. Sizing rules:

- A unit must be small enough that writing it in one pass does **not** degrade quality.
- One section with a handful of pages (for example `getting-started`) can be a single unit.
- A large section is split: **each feature is its own unit**, even if it has 9–10 sub-pages. Never put
  two unrelated features in one unit.
- Reference surfaces are split by class/area, not written as one giant unit.
- Order units by reader journey and dependency: overview/getting-started first, then concepts, then
  features, then reference, then troubleshooting.

`/build-docs <sdk>` writes exactly one unit per run, then stops for human review.

## Depth baseline

**Match the Unity SDK's page count per section and per feature.** The Unity SDK is the quality and
depth floor; the plan must reach it by default. A plan with 2–3 pages per feature, or a
getting-started section with a single page, is too shallow — revise before approval.

### Section-level depth (common sections)

| Section | Minimum expected pages | Notes |
|---|---|---|
| Overview / landing | 1 hub | Introduces the subject, links to child sections |
| Getting started | 4–5 | Install + configure + first character + verify (split by task) |
| Core concepts | 3–5 | One explanation page per major system/lifecycle |
| Features | 6–10 per feature | See canonical feature page set below |
| Scripting reference | 1–3 per component/class | One page per API surface area |
| Troubleshooting | 3–5 | One page per symptom cluster; general + feature-specific |
| Release notes / migration | As needed | One page per major release or breaking change |

For a **topic** subject — a product surface with no code — the depth floor is the same but the sections
differ, because the reader's unit of work is a screen rather than a class:

| Section | Minimum expected pages | Notes |
|---|---|---|
| Overview / landing | 1 hub | What the product is and what the reader can do with it |
| Getting started | 4–5 | Sign in, orient, first result, verify it worked |
| Configuration surfaces | 1 per surface | One page per panel, settings group, or tab the user configures |
| Concepts | 3–5 | One page per idea the reader must hold to use the product well |
| Troubleshooting | 3–5 | One page per symptom cluster |

There is no scripting-reference section for a topic subject. Do not invent one to hit a page count; a
page with nothing real behind it is worse than a missing page.

### Canonical feature page set

A feature work unit defaults to **6–10 pages**. Trim only when the feature genuinely does not need a
page (for example, a trivial feature with no failure modes does not need a troubleshooting page). Do
not trim to save effort. Extend beyond 10 when the feature has multiple distinct sub-tasks or
components.

| Page | Typical file name | Diataxis | Required? |
|---|---|---|---|
| Feature hub / overview | `README.md` | Explanation (hub) | Required — every feature |
| How this feature works | `how-<feature>-works.md` | Explanation | Required unless trivially obvious |
| Quick-start / first use | `quick-start.md` or `configure-<feature>.md` | How-to | Required |
| Feature reference (Blueprint / API) | `<feature>-reference.md` | Reference | Required |
| Usage examples | `usage-examples.md` | How-to | Required unless quick-start is comprehensive |
| Troubleshooting & diagnostics | `troubleshooting.md` | Troubleshooting | Required if known failure modes exist |
| Additional task how-to pages | `<specific-task>.md` | How-to | As needed for distinct sub-tasks |
| Additional component reference pages | `<component>-reference.md` | Reference | As needed per component |

**Six pages is the minimum for a non-trivial feature. Two or three pages is a strong signal that
the plan needs to go deeper before the human approves it.**

---

## Example plan layout

```md
# Unreal Engine documentation plan

Pack: packs/unreal.md  (kind: SDK)
Source of truth: <ABSOLUTE PATH the user provided to the SDK source>  (verified: <date>)
Status legend: [ ] not started  [~] drafted, awaiting review  [x] reviewed & accepted  [?] blocked on owner

## Unit 1 — Overview & getting started   (status: [ ])

Folder: plugins-and-integrations/unreal-engine/getting-started/
Rationale: entry path, small and linear — safe as one unit.

| # | Page title | File | Diataxis | Description (1 line) | Source of truth | Status |
|---|---|---|---|---|---|---|
| 1 | Convai Unreal Engine overview | README.md | explanation | What the plugin does and where it fits | <code dir / docs> | [ ] |
| 2 | Install the Unreal plugin | install-the-unreal-plugin.md | how-to | Install and enable the plugin | <.uplugin / install path> | [ ] |
| 3 | Configure the API key | configure-the-api-key.md | how-to | Authenticate to Convai | <settings class> | [ ] |
| 4 | Build your first Convai character | build-your-first-character.md | tutorial | First working character in a level | <sample / blueprint> | [ ] |

## Unit 2 — Conversation lifecycle (concepts)   (status: [ ])

Folder: plugins-and-integrations/unreal-engine/core-concepts/
Rationale: shared mental model needed before feature pages.

| # | Page title | File | Diataxis | Description | Source of truth | Status |
|---|---|---|---|---|---|---|
| 1 | Conversation lifecycle | conversation-lifecycle.md | explanation | Flow between level, plugin, and Convai | <runtime classes> | [ ] |

## Unit 3 — Feature: Lip sync   (status: [ ])

Folder: plugins-and-integrations/unreal-engine/features/lip-sync/
Rationale: one feature = one unit (its sub-pages are written and reviewed together).
Expected depth: 6–8 pages (canonical feature page set).

| # | Page title | File | Diataxis | Description | Source of truth | Status |
|---|---|---|---|---|---|---|
| 1 | Lip sync overview | README.md | explanation (hub) | What lip sync does, available modes, when to use each | UConvaiFaceSync component | [ ] |
| 2 | How lip sync works | how-lip-sync-works.md | explanation | Audio-to-blendshape pipeline, mode selection logic | ConvaiDefinitions.h, UConvaiFaceSync | [ ] |
| 3 | Enable lip sync on a MetaHuman | enable-lip-sync-metahuman.md | how-to | Configure MetaHuman Blendshapes mode end-to-end | UConvaiFaceSync, demo assets | [ ] |
| 4 | Enable lip sync on a CC character | enable-lip-sync-cc.md | how-to | Configure ARKit/CC4 mode, assign Reallusion anim BP | UConvaiFaceSync, Reallusion anim BP | [ ] |
| 5 | Lip sync reference | lip-sync-reference.md | reference | All fields, enums, events, constraints on UConvaiFaceSync | UConvaiFaceSync source | [ ] |
| 6 | Usage examples | usage-examples.md | how-to | Scene setups for training sim and interactive experience | Demo map assets | [ ] |
| 7 | Troubleshoot lip sync | troubleshooting.md | troubleshooting | No movement, wrong mode, blendshape mismatch | Common failure patterns | [ ] |

## Proposed SUMMARY.md subtree

<The exact nesting to add under the Unreal section, with labels equal to each page title.>

## Open questions / missing context

<Anything the writer will need that the source did not make clear. The human resolves these before build.>
```

### Example: a topic plan header and unit

A topic plan looks the same, but its source-of-truth column names screens and its owner, and it carries
rows that are openly blocked on an answer:

```md
# Convai Playground documentation plan

Pack: packs/playground.md  (kind: topic)
Owner: <name> — answers every "owner:" row below
Source of truth: the running product; see the pack's "Source of truth and verification"
Status legend: [ ] not started  [~] drafted, awaiting review  [x] reviewed & accepted  [?] blocked on owner

## Unit 1 — Get started   (status: [ ])

Folder: convai-playground/get-started/
Rationale: the first-run path, linear and small.

| # | Page title | File | Diataxis | Description (1 line) | Source of truth | Status |
|---|---|---|---|---|---|---|
| 1 | Convai Playground overview | README.md | explanation | What the Playground is and what a creator does in it | Dashboard landing screen | [ ] |
| 2 | Create a character | create-a-character.md | how-to | Make a first character and save it | Create Character flow | [ ] |
| 3 | Test a character | test-a-character.md | how-to | Talk to the character and confirm it responds | Chatbox screen | [ ] |
| 4 | Character version limits | character-versioning.md | reference | How many versions are kept and what happens at the cap | owner: <name> | [?] |
```

Row 4 is the shape that keeps wrong facts out. Nobody on the writing side knows the version cap, so the
plan says so rather than guessing, and `/build-docs` leaves it unwritten until the owner answers.

---

## Plan rules

- **Depth first.** Use the Unity SDK docs (`plugins-and-integrations/convai-unity-sdk/`) as the
  **depth baseline**: every common section (overview, getting-started, core-concepts, troubleshooting)
  must match Unity's page count for that section; every feature unit must reach the canonical feature
  page set (6–10 pages). The goal is Unity-level depth, not Unity's exact page list or layout. SDK-
  specific features, workflows, and terminology determine the actual content.
- **A shallow plan requires a revision.** If a feature unit has fewer than six pages, or if
  getting-started has fewer than four pages, the plan is too shallow. Revise before declaring it ready
  for human approval.
- Every page has exactly one Diataxis mode. If a topic needs both a concept and a how-to, that is two rows.
- Name a concrete source of truth per page. What counts depends on the pack kind: a code file, class or
  sample for an SDK; a named screen or the owner for a topic; a facts-table row for a customer. If none
  exists, add it to "Open questions" — do not plan a page you cannot source.
- Do not invent features. Plan only what the subject actually contains. For a topic subject that means
  what you can see in the product or the pack; a capability you assume exists because similar products
  have it is not a plan row.
- **The depth baseline never justifies a fabricated page.** If reaching the floor would require a page
  with nothing real behind it, the section is genuinely smaller than Unity's — say so in the plan
  instead of padding it.
- The plan is reviewed and approved by a human before any page is written.
