# No-code experiences pack

Topic pack for the Convai products a creator uses without writing code, outside the Playground:
**Avatar Studio**, **Convai Sim**, and the **Convai XR Animation Capture App**. Generic doctrine lives
in `references/`.

This is a **topic pack**, not an SDK pack. There is no package to install and no source repository to
read, so every claim about an interface is verified against that interface. Read "Source of truth and
verification" before writing anything.

---

## What this pack covers

Pages under `no-code-experiences/`:

| Product | Folder | What it is |
|---|---|---|
| Avatar Studio | `avatar-studio-experiences/` | Browser tool for creating and customizing an avatar, including MetaHuman and Reallusion avatars, face filters, environment, and lighting |
| Convai Sim | `convai-sim-experiences/` | Interactive 3D simulation experiences built without code |
| Convai XR Animation Capture App | `convai-xr-animation-capture-app/` | Meta Quest application for capturing animation for AI avatars |

Out of scope, with the pack that owns each:

| Subject | Pack |
|---|---|
| Character configuration in the web dashboard | `playground.md` |
| Engine SDK and plugin integration | `unity.md`, `unreal.md`, `web.md` |
| REST and realtime API contracts | `core-service.md` |

These three products share a folder and an audience, not a codebase. Do not carry a fact from one into
another; verify each separately.

## Product naming

- **Avatar Studio**, **Convai Sim**, **Convai XR Animation Capture App** — full names on first mention
  on a page, exactly as written here.
- After first mention: "Avatar Studio", "Convai Sim", and "the capture app" are acceptable.
- **MetaHuman** and **Reallusion** are third-party names. Spell them as their owners do. Do not
  pluralize a product name into "MetaHumans" when referring to the format.
- An **avatar** is the visual character; a **character** is the Convai character it is attached to.
  These are different things — do not use one word for both.
- Refer to Convai's backend as **Convai**.

## Audience

Creators and designers working visually. Assume no programming knowledge and no engine knowledge.

For the XR Animation Capture App, assume the reader has a Meta Quest headset and knows how to install
and launch an application on it, but not how to develop for it. State the headset and OS requirements
on the page rather than assuming them.

## Terminology

| Term | Notes |
|---|---|
| Avatar Studio | Both words capitalized. |
| avatar | Lowercase in prose. The visual model. |
| character | Lowercase in prose. The Convai character an avatar is attached to. |
| MetaHuman | One word, capital H. Third-party name. |
| Reallusion | Third-party name. |
| Face Filter | Capitalized when naming the feature. |
| Convai Sim | Two words. |
| Convai XR Animation Capture App | Full name on first mention. |

Confirm any label not in this table against the current interface before using it.

## Source of truth and verification

- **Owner:** the product owner for the specific product being documented. Avatar Studio, Convai Sim, and
  the capture app may have different owners. Confirm which one before starting a work unit; do not
  assume one person covers all three.
- **Proof that counts:** a current screenshot or recording of that product's interface, written
  confirmation from its owner, or an existing page verified against one of those and listed as a gold
  standard.
- **Proof that does not count:** a memory of the interface, an undated screenshot, a marketing page, or
  a fact carried over from one of the sibling products.

If a fact cannot be proven, stop and ask. Never describe a screen you have not seen or state a
supported format, file size limit, device requirement, or export option you have not been shown.
Format and limit claims are the highest-risk facts in this section: they are easy to assume, the reader
acts on them immediately, and a wrong one wastes their upload and their time.

## Screenshot policy

The SDK default is inverted here. These are visual products and the reader is working on screen.

Required:

- Any panel or control the reader must find, the first time the page sends them there
- Any visual result the reader needs to recognise to know a step worked
- Any before/after comparison where the difference is the point

For the XR capture app, prefer a short recording over a still where the motion is the subject.

Not a screenshot, ever: file paths, error messages, JSON, configuration text, and anything the reader
might copy. Those are code blocks.

Use test content and a test account. Never capture a real customer's avatar, another user's content,
account identifiers, or billing information.

Use the GitBook figure syntax with real alt text:

```md
<figure><img src="../../.gitbook/assets/avatar-studio-face-filter.png" alt="The Face Filter panel with a filter applied to the avatar preview"><figcaption><p>The preview updates as the filter is adjusted.</p></figcaption></figure>
```

## Feature and rollout state

- State plan tier or entitlement requirements in the page prerequisites.
- Label a beta product or feature as beta in the lead paragraph.
- For the capture app, state the supported headset models and app version the page was verified
  against, and set `last_reviewed` to that version.

## GitBook variables

`.gitbook/vars.yaml` in the documentation repository is the only authority for values.

| Variable | Holds | Derive from | Used in |
|---|---|---|---|
| `dashboard_url` | Convai dashboard URL | Stable product URL | Sign-in and entry-point steps |

Add a variable to `.gitbook/vars.yaml` rather than writing a synchronized literal into a page.

## Gold-standard example pages

**No page in `no-code-experiences/` currently meets the quality bar.** Pages in this section carry a
body `#` H1, open with `## Introduction`, and do not set `title` frontmatter. Do not model a new page on
them.

Until a page in this section is written to standard and accepted, model structure on the Unity SDK
section and adapt the audience:

| Mode | Model page |
|---|---|
| How-to | `plugins-and-integrations/convai-unity-sdk/getting-started/installation.md` |
| Hub | `plugins-and-integrations/convai-unity-sdk/README.md` |

Take the structure, frontmatter, block usage, and heading discipline. Do not take the developer voice.

**When the first page here is written to standard and accepted, replace this section with its path.**

## Section layout

```
no-code-experiences/
├── README.md                          section hub
├── avatar-studio-experiences/
│   ├── README.md                      product hub
│   └── customizing-your-avatar/...    nested by task
├── convai-sim-experiences/
│   ├── README.md                      product hub
│   └── <task>.md
└── convai-xr-animation-capture-app/
    ├── README.md                      product hub
    └── <task>.md
```

Avatar Studio pages nest several levels deep. Deep nesting is acceptable where each level is a real
reader decision; it is not acceptable as a substitute for a hub page. If a folder has one child, it
should not be a folder.

## Known violations in existing pages

| Pattern | What is wrong | What to do instead |
|---|---|---|
| Body `# Title` H1 | Duplicates the GitBook page title | Delete it; start with a headingless lead paragraph. |
| `## Introduction` opening section | Forbidden heading | Delete it; fold the content into the lead paragraph. |
| Missing `title` frontmatter | Sidebar label cannot be matched to the page title | Add `title`, identical to the `SUMMARY.md` label. |
| Plain link lists on hub pages | Not a GitBook navigation block | Use `{% content-ref %}` or cards. |

Fix these only on pages the task covers.

## What must never be documented

- Internal admin or moderation tooling
- Unreleased products or features, including anything behind an internal flag
- Third-party licensing terms for MetaHuman or Reallusion assets — link to the owner's terms instead of
  restating them
- Another customer's avatars, experiences, or content
- Internal service names, repository names, or ticket links
