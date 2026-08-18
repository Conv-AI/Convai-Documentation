# Convai Playground pack

Topic pack for the Convai Playground: the web application where a creator builds, configures, tests,
and publishes a character without writing code. Generic doctrine lives in `references/`.

This is a **topic pack**, not an SDK pack. There is no package to install and no source repository to
read, so every claim about the interface has to be verified against the interface itself. Read
"Source of truth and verification" before writing anything.

---

## What this pack covers

Pages under `convai-playground/` in the documentation repository:

- `get-started/` — dashboard orientation, creating a character, testing it, versioning, voice mode
- `character-customization/` — every configuration surface of a character: description, avatar,
  language and speech, Knowledge Bank, Personality Traits, Core AI Settings, Guardrails, State of Mind,
  Memory, Mindview, Narrative Design, External API, MCP Servers, publishing

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
  label exactly, such as the **Create Character** button.
- Do not call it an "agent", a "bot", an "NPC", or an "assistant" in Playground pages. The SDK packs use
  their own engine-side terms; this pack does not inherit them.
- Do not write "Legacy Playground" for the current product. That name refers to the older interface and
  means something specific to readers.
- Refer to Convai's backend as **Convai**. Never "Convai cloud", "Convai's servers", or "the backend".

## Audience

Creators, designers, writers, and product people configuring a character through the interface. Assume
no programming knowledge and no engine knowledge. A reader who has never opened a code editor must be
able to complete every procedure on these pages.

Two exceptions where technical knowledge is fair to assume, and only on those pages: **External API**
and **MCP Servers**.

Baseline before starting: a Convai account and access to the Playground. State any additional plan tier
or permission requirement on the page itself.

## Terminology

Match the interface character for character. The reader is looking at the screen while reading, so a
near-miss label costs them more than a missing sentence.

| Term | Notes |
|---|---|
| Convai Playground | The product. "The Playground" after first mention. |
| Dashboard | The landing surface after signing in. |
| character | Lowercase in prose. Capitalized only inside a quoted UI label. |
| Knowledge Bank | Two words, both capitalized. Not "knowledge base". |
| Core AI Settings | All three words capitalized. |
| Personality Traits | Both words capitalized. |
| State of Mind | Lowercase "of". |
| Guardrails | One word. |
| Mindview | One word, no space, no capital V. |
| Narrative Design | Both words capitalized. |
| Chatbox | One word. |
| My Characters, My Experiences | Dashboard section labels, capitalized as shown. |
| Avatar Studio | A separate product. Link, do not document. |

Before using any label not in this table, confirm its exact spelling against the current interface.

## Source of truth and verification

There is no source code to check a claim against. Everything here is verified against the running
product or a person.

- **Owner:** the Convai Playground product owner. Named per page in the plan; confirm who it is before
  starting a work unit.
- **Proof that counts:** a current screenshot or screen recording of the interface; written
  confirmation from the product owner; or an existing page that was itself verified against one of
  those and is listed as a gold standard below.
- **Proof that does not count:** a memory of the interface, a screenshot of unknown age, a marketing
  page, a support thread, or an existing page from the "Known violations" list below.

If a fact cannot be proven, the writer stops and asks. Never describe a screen you have not seen, name
a field you have not read, or state a default, limit, or behavior you have not been shown. A plausible
guess about a UI is indistinguishable from a fact to the reader, and it is what sends them to support.

## Screenshot policy

The SDK default is inverted here: a Playground reader is following along on screen, so showing the
screen is usually the clearest instruction available. Existing pages in this section carry roughly four
to seven figures each, and that density is appropriate.

Required:

- Any panel the reader must find, the first time the page sends them there
- Any control that is easy to confuse with a neighbouring one
- Any state the reader must recognise to know a step worked

Not a screenshot, ever — these stay selectable text in a code block: JSON, API payloads, error
messages, log output, configuration text, and anything the reader might copy.

Every screenshot must use a test account with test content. Never capture a real customer's character,
a real end user's conversation, an API key, billing information, or another account's data.

Use the GitBook figure syntax already used throughout this section, with real alt text:

```md
<figure><img src="../../.gitbook/assets/knowledge-bank-upload.png" alt="The Knowledge Bank panel with one uploaded document listed"><figcaption><p>Uploaded documents appear in the Knowledge Bank list.</p></figcaption></figure>
```

## Feature and rollout state

Some Playground surfaces are gated by plan tier or are still rolling out. A reader who follows a guide
and cannot find the control has been handed a wrong fact.

- State the requirement in the page's prerequisites when a feature needs a specific plan tier.
- Label a beta surface as beta in the lead paragraph, not only in a hint at the bottom.
- Confirm the current gating with the owner before writing it. Gating changes more often than the
  interface does, and a stale tier requirement is a support ticket.

## GitBook variables

`.gitbook/vars.yaml` in the documentation repository is the only authority for values.

| Variable | Holds | Derive from | Used in |
|---|---|---|---|
| `dashboard_url` | Convai dashboard URL | Stable product URL | Sign-in steps, links out to the Playground |

If a Playground page needs a synchronized value that has no variable yet, add it to `.gitbook/vars.yaml`
in the same change rather than writing the literal into the page.

## Gold-standard example pages

**No page in `convai-playground/` currently meets the quality bar.** Every page sampled in this section
carries a body `#` H1, most open with `## Introduction`, none set `title` frontmatter, and several close
with `## Conclusion`. All four are doctrine violations. Do not model a new page on them.

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
page; do not silently rewrite pages the task did not ask for.

| Pattern | What is wrong | What to do instead |
|---|---|---|
| Body `# Title` H1 on every page | Duplicates the GitBook page title, which is already the only H1 | Delete it. Start with a headingless lead paragraph. |
| `## Introduction` opening section | Forbidden heading; delays the content | Delete the heading and fold its content into the lead paragraph. |
| Missing `title` frontmatter | Sidebar label cannot be matched to the page title | Add `title`, identical to the `SUMMARY.md` label. |
| `## Conclusion` closing section | Vague heading; usually restates the page | Replace with `## Next steps` and content refs, or delete it. |
| Plain "Continue to: _Page_" lists on hub pages | Not a GitBook navigation block | Use `{% content-ref %}` or cards. |
| Hardcoded values in prose | Goes stale silently | Use a `space.vars` expression. |
| Broken link in `character-customization/README.md` — the Personality Traits entry points at `knowledge-bank.md` | Sends the reader to the wrong page | Point it at `personality-traits.md`. |

## What must never be documented

- Internal admin or moderation tooling
- Unreleased features, including anything visible only behind an internal flag
- Pricing or plan limits not already published on Convai's public pricing page
- Another customer's characters, content, or configuration
- Internal service names, repository names, or ticket links
