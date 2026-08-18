# Topic pack template

For documenting something that is **not** an SDK or plugin: a product surface such as the Convai
Playground or Avatar Studio, a cross-cutting concept area, or any Convai subject with no package to
install and no source repository to read.

The difference that matters is verification. An SDK pack points the writer at source code, and every
claim is checkable by reading a file. A topic pack cannot do that, so it must name a **named human
owner** and state exactly what evidence counts as proof. Without that, a writer documenting a UI has
nothing to check against and will guess. Guessing is what this pack exists to prevent.

Copy this file to `packs/<topic>.md` and fill every section. Replace every `TODO:`. A pack with a
`TODO:` left in it is not ready for `docs-writer` to use.

For an SDK or plugin, use `_pack-template.md` instead. For documentation written for one named
customer, use `_customer-pack-template.md`.

---

## What this pack covers

- TODO: The product, surface, or subject area, in one sentence.
- TODO: The repository section its pages live under (`convai-playground/`, `no-code-experiences/`,
  `api-reference/`, or another existing top-level section).
- TODO: What is explicitly **out** of scope and belongs to a different pack. Name the other pack.

## Product naming

- TODO: The canonical product name and its exact capitalization, as the product's own UI spells it.
- TODO: Names that must never be used for it, including internal or legacy names.
- TODO: How to refer to Convai's backend on these pages. The cross-pack rule is plain **"Convai"**.

## Audience

- TODO: Who reads these pages and what they already know. For product-UI areas this is usually a
  creator, designer, or operator — not a developer. Do not assume programming knowledge unless the
  audience genuinely has it.
- TODO: What the reader needs before starting: an account, a plan tier, a permission, a device.

## Terminology

- TODO: Every product term and its exact spelling and capitalization as the UI shows it. UI labels are
  proper nouns: match them character for character, because the reader is looking at the screen while
  reading.
- TODO: Terms that are easy to confuse, and which one to use where.
- TODO: Terms to avoid.

## Source of truth and verification

This is the section that keeps wrong facts out. Fill it carefully.

- **Owner:** TODO: the named person or team who confirms behavior for this area. A pack without a named
  owner is not usable.
- **What counts as proof:** TODO: list the evidence a writer may treat as verified. For a product UI
  this is typically a current screenshot or recording of the screen, written confirmation from the
  owner, or an existing page already verified against one of those.
- **What does not count:** a memory of the UI, an older screenshot, a marketing page, a support thread,
  or another documentation page that was never itself verified.

A writer who cannot verify a claim stops and asks the owner. They do not describe a screen they have
not seen, invent a field name, state a limit or default, or guess what a control does. This is not
negotiable and does not weaken because a deadline is close.

- TODO: Where a writer can obtain proof — which environment or account to look at, who to ask, and
  where existing verified screenshots are kept.

## Screenshot policy

Product-UI documentation inverts the SDK default. In SDK docs a screenshot is a last resort; here, a
reader following along on screen usually needs to see the screen.

- TODO: When a screenshot is required for this area, and when prose alone is enough.
- TODO: What each screenshot must show — which state, which panel, whether test data or a real account.
- TODO: Anything that must never appear in a screenshot: real customer names, real API keys, billing
  details, other users' content, internal tooling.

Screenshots still never replace text for anything selectable — code, JSON, log output, error messages,
or configuration text. Those are code blocks. See `references/images.md`.

## Feature and rollout state

- TODO: Which parts of this area are beta, gated behind a plan tier, gated behind a flag, or still
  rolling out. Say how a page must label each, and where the current state is tracked.

A feature that some readers cannot see must say so on the page. A reader who follows a guide and finds
the button missing has been given a wrong fact.

## GitBook variables

`.gitbook/vars.yaml` in the documentation repository is the only authority for these values. Record
which variables exist and where each value comes from, never the value itself — a value copied into a
pack goes stale and becomes a wrong fact.

| Variable | Holds | Derive from | Used in |
|---|---|---|---|
| TODO | TODO | TODO | TODO |

## Gold-standard example pages

Pages that already meet the quality bar for this area. A new page matches their structure and tone.

- TODO: path to an exemplary how-to page
- TODO: path to an exemplary reference page
- TODO: path to an exemplary concept page
- TODO: path to the section hub

If no page in this area meets the bar yet, say so plainly here and name the closest page from another
section to model instead. **Never point at a page you know violates the doctrine** — the writer will
copy whatever you point at.

## Section layout

- TODO: The folder structure for this area, and what belongs in each folder.

## Known violations in existing pages

Existing pages a writer will encounter that break current doctrine, so they are not copied by accident.
Record what is wrong, not just that something is.

| Page or pattern | What is wrong | What to do instead |
|---|---|---|
| TODO | TODO | TODO |

## What must never be documented

- TODO: Internal tooling, admin surfaces, unreleased features, pricing not published elsewhere,
  anything under NDA, and any other content that must not reach the public site.
