# SDK pack template

A pack carries everything the generic `references/` must not hard-code: product naming, terminology,
install model, GitBook variables, gold-standard example pages, and platform notes. The `docs-writer`
reads the pack **before** drafting any page.

This is the **SDK pack** template, for an SDK or plugin — something with a package to install and a
source repository whose code can be read to verify a claim. There are two other kinds:

| The subject is | Use |
|---|---|
| An SDK or plugin with a source repository | this file |
| A Convai product surface or concept area with no source repository — the Playground, Avatar Studio, an API surface, a general topic | `_topic-pack-template.md` |
| Documentation for one named customer | `_customer-pack-template.md` |

The kinds differ mainly in how a claim is verified. An SDK pack points at code. A topic pack cannot,
so it names a human owner and states what evidence counts as proof. A customer pack additionally has to
settle where the pages are allowed to be published.

Copy this file to `packs/<sdk>.md` and fill every section. Replace each `TODO:` marker. Do not leave a
`TODO:` in a published pack. Keep facts verifiable against the SDK source or existing docs.

---

## Product naming

- TODO: Canonical product name (for example "Convai Unity SDK" or "Convai SDK for Unity").
- TODO: What never to call it (for example "do not call it a plugin").
- TODO: Backend phrasing. The cross-SDK rule is to call the backend "Convai"; restate any SDK-specific
  phrasing here.

## Audience and prerequisites baseline

- TODO: Who the reader is and what they are assumed to know.
- TODO: Baseline prerequisites that appear on most pages (engine/runtime version, account, API key).

## Terminology and concepts

- TODO: SDK-specific terms and the exact casing/spelling to use (component names, manager classes,
  settings assets, menus).
- TODO: Terms to avoid or common mistakes (for example "in-scene" not "game-world").

## Install and package model

- TODO: How the SDK is installed (package manager, marketplace, npm, git URL) and the package identifier.
- TODO: The canonical install/setup page path in this repo.

## GitBook variables

List the `space.vars` defined for this SDK in `.gitbook/vars.yaml`. Use these instead of hard-coding
values.

| Variable | Example value | Used in |
|---|---|---|
| TODO | TODO | TODO |

## Gold-standard example pages

Point writers to existing pages that already meet the quality bar for this SDK. New pages should match
their structure and tone.

- TODO: path to an exemplary how-to page
- TODO: path to an exemplary reference page
- TODO: path to an exemplary concept/explanation page
- TODO: path to the section hub

## Section layout

- TODO: The folder structure for this SDK under `plugins-and-integrations/<sdk>/` (getting-started,
  core-concepts, features, scripting-reference, troubleshooting, and so on).

## Platform and version notes

- TODO: Supported platforms, version-sensitivity, and where `last_reviewed` is required.

## SDK source of truth

- TODO: Where to verify technical claims (SDK repo name/path, key files, public API surface).

## Tutorials & external sources

Official tutorial videos and their sources. Use these alongside the SDK source when planning and
writing feature pages. Transcripts (if available) live under `.convai-docs/sources/<sdk>/` in the
documentation repo.

| Topic | Video URL | Transcript |
|---|---|---|
| TODO | TODO | TODO |

**Transcript corrections:** auto-generated captions contain errors. List known corrections here so
writers apply them consistently when quoting from transcripts.

| Auto-caption (wrong) | Correct |
|---|---|
| TODO | TODO |

## Bundled sample/demo assets

Assets shipped with the SDK or plugin that writers can reference by name in documentation. List every
map, character Blueprint, player Blueprint, game mode, widget Blueprint, and animation Blueprint by
its actual asset name. Writers use these names in tutorials and how-to pages; do not leave them as
placeholders.

| Asset name | Type | Purpose |
|---|---|---|
| TODO | TODO | TODO |
