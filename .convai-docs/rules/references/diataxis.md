# Information architecture and Diataxis

How to choose a page's type and place it in the navigation. Every page has exactly one primary
Diataxis mode. If a draft mixes modes, split it.

## Section types

Organize pages by user intent, not by internal SDK implementation.

| Section type | Purpose | Typical pages |
|---|---|---|
| Start | Fast path from zero to first working result | SDK overview, requirements, installation, quickstart, authentication |
| Tutorials | Guided learning experiences | Build your first character, create a training simulation scene |
| How-to guides | Task-focused procedures | Configure microphone input, stream character responses, handle in-scene actions |
| Concepts | Explanation and mental models | Conversation lifecycle, character state, audio flow |
| Reference | Complete factual documentation | Classes, components, fields, methods, events, configuration options |
| Troubleshooting | Known failure modes and fixes | Package install fails, audio not detected, authentication errors |
| Release notes and migration | Change management | Upgrade guides, breaking changes, compatibility notes |

## Diataxis page types

| Type | Reader question | Page shape | Do | Avoid |
|---|---|---|---|---|
| Tutorial | "Teach me through a safe first experience." | End-to-end lesson | Use a single known-good path. Each step produces a visible, meaningful result. Use "We will…" not "You will learn…". Ruthlessly minimize explanation — defer it to linked reference or concept pages. | Options, branching, deep API reference, and any content that teaches rather than does. |
| How-to guide | "Help me accomplish this specific task." | Goal, prerequisites, steps, verification, troubleshooting | Assume the reader is already competent in the general domain. Prioritize practical usability over exhaustive completeness. Keep steps focused on one goal. | Teaching concepts inline, covering every edge case, or adding material the reader did not come for. |
| Reference | "Tell me exactly what this thing is or does." | Structured factual entry | Be austere and uncompromising. Mirror the product's structure. State facts: names, types, defaults, parameters, return values, errors, constraints. | Narrative explanation, opinion, marketing, or instruction. |
| Explanation | "Help me understand why this works this way." | Conceptual article | Take a wide perspective. Discuss background, rationale, alternatives, tradeoffs, and design decisions. Use reasoning statements: "The reason X works this way is…". | Step-by-step instructions, close-up reference detail, or anything that belongs in a how-to or reference page. |

### Page-type requirements

- **Tutorial:** use "We will…" collaborative framing, not "You will learn…". Include a clear
  destination up front. Each step must produce a visible, meaningful result the learner can observe.
  Ruthlessly minimize explanation — if you need to explain something, link to a reference or concept
  page instead of adding prose. Keep to one path; ignore options and alternatives.
- **How-to guide:** assume the reader is already competent. Include outcome, prerequisites, focused
  steps, verification, troubleshooting, and next steps. Prioritize practical usability over
  completeness — do not cover every edge case.
- **Reference:** be austere. Include exact names, types, syntax/signature, fields, parameters,
  defaults, return values, events, errors, and constraints. Mirror the SDK's structure. No narrative
  teaching, no marketing, no opinion.
- **Explanation:** take a wide perspective. Cover background, rationale, design decisions,
  alternatives, tradeoffs, and relationships between systems. Use reasoning statements. Do not include
  steps, procedures, or close-up reference detail.
- **Troubleshooting:** organize by symptom. Each item must include symptom, cause, fix, and verification.
- **Hub/index page:** use a short section introduction plus cards for the main child pages. Do not
  include long procedures or full reference tables.

## Page nesting and hubs

| Pattern | Use when | Standard |
|---|---|---|
| Single page | The topic has one clear intent. | Keep it flat. |
| Parent hub + child pages | A section has 3 or more related pages. | Parent introduces the section and routes readers with cards. |
| Empty parent page | The parent exists only for navigation. | Let GitBook show child pages, or add a short hub if manual routing is needed. |
| Deep nesting | Reference surfaces are large and stable. | Max 2 levels in the left nav for all non-reference sections. Reference sections may use 3 levels. Beyond 3 levels: flatten or restructure. |

Every major section should have a hub page with: one short paragraph stating the section purpose,
cards for the main child pages, minimal prose, and no long tutorials or reference tables.

## When to split a page

Split a page when:

- It serves more than one Diataxis mode.
- It contains more than two major tasks.
- The page outline has more than seven `##` sections.
- One section needs independent search traffic.
- Troubleshooting dominates the page.
- Beginner and advanced readers need substantially different paths.
- Platform or language variants become too long for tabs.

Do not split only because a page is long. Split when reader intent changes.

One more trigger: when a section that other pages and external sites link to directly keeps growing,
promote it to its own page and link to it. A heavily linked section is already being treated as a page
by readers — leaving it buried makes their link land in the middle of something else.

Merge two pages when both are under approximately 300 words and serve the same reader goal. A page
that exists only to say "see also X" is an orphan stub — merge it into the closest logical parent.

When a topic is split: the parent page becomes a hub, the parent uses cards for child pages, each
child page remains self-contained, and each child page links back to related concepts, reference
pages, or next steps.

## Content Variants

Use Content Variants when an entire documentation set must be maintained in parallel — different SDK
versions, different languages, or different product editions — under the same site URL.

| Variant type | When to use | SEO behavior |
|---|---|---|
| Version variants (`v4`, `v5`, `/latest`) | Breaking API changes between major SDK versions | Set canonical on all version variants pointing to `/latest`; prevents outdated versions outranking current docs |
| Language variants | Full translation of the documentation set | Each language variant gets its own URL; use `hreflang` alternate links |
| Edition variants | SDK features differ between free and enterprise builds | Keep shared content in Snippets; variant only the pages that differ |

Rules:

- Prefer Content Variants over duplicated spaces. Variants share site settings, customization, and analytics.
- Use Snippets for content shared across variants so it stays synchronized.
- Use Conditional content blocks for small within-page differences rather than creating a full variant.
- Set the canonical URL on all non-primary variants to point to the current primary variant.
- Every variant must have the same page slug structure so internal links resolve correctly across variants.

## Cross-linking and orphan prevention

Every page must be reachable through at least one of: sidebar navigation, a parent hub page, a related
page link, or a next steps section.

- Link when reader intent changes from task to concept, task to reference, or concept to how-to.
- Use descriptive link text. Never "click here."
- Link to the source of truth rather than repeating large sections.
- Keep next steps to 2-5 links. Do not create a "Related articles" dump.
- When adding a page that should appear in the sidebar, update `SUMMARY.md` in the same change. The
  sidebar label must match the page `title` frontmatter exactly.
