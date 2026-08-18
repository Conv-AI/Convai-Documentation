# Unity SDK pack

SDK-specific facts for Convai Unity SDK documentation. Read this before drafting or revising any Unity
page. Generic doctrine lives in `references/`; this pack only supplies Unity specifics.

## Product naming

- Use **"Convai Unity SDK"** or **"Convai SDK for Unity"**.
- Do **not** call it a "plugin". (Note: the repo also has legacy `unity-plugin/` docs — that is the
  older product surface; new SDK docs live under `convai-unity-sdk/` and use "SDK".)
- Refer to the backend as "Convai" — for example "streams audio to Convai", "Convai responds", "sent
  to Convai". Never "Convai cloud", "cloud backend", "Convai's servers", or "cloud-powered".

## Audience and prerequisites baseline

- Primary audience: Unity developers integrating the Convai Unity SDK. Getting Started pages assume
  limited Unity experience; advanced and reference pages may assume Unity, C#, package management, and
  runtime debugging knowledge.
- Common prerequisites: Unity `<code class="expression">space.vars.unity_min_version</code>` (recommend
  Unity 6), a Convai account, a project API key, and Unity Package Manager access.

## Terminology and concepts

- Use Unity-native terms with correct casing: `Package Manager`, `Inspector`, `GameObject`, `prefab`,
  `scene`, `Play mode`, `Project Settings`, `Build Settings`.
- Format component and class names as inline code: `ConvaiNPC`, `ConvaiSettings`, `ConvaiLipSync`,
  `ConvaiAudioManager` (verify exact names against SDK source before use).
- Use "in-scene" rather than "game-world". Primary domain framing: training simulations, then
  interactive experiences, then games.

## Install and package model

- Installed through Unity Package Manager. Package identifier:
  `<code class="expression">space.vars.sdk_package_id</code>`.
- The canonical install/setup pages live under `plugins-and-integrations/convai-unity-sdk/getting-started/`.

## GitBook variables

`.gitbook/vars.yaml` in the documentation repository is the only authority for these values. This pack
lists which variables exist and where they belong, never their current values — a value copied here goes
stale the next release and becomes a wrong fact in the docs. Read `vars.yaml` when you need an actual
value.

| Variable | Holds | Used in |
|---|---|---|
| `unity_sdk_version` | Current SDK release version | Install steps, code examples, release references |
| `unity_min_version` | Minimum supported Unity editor version | Prerequisites sections |
| `unity_recommended_version` | Recommended Unity editor version | Prerequisites, compatibility |
| `sdk_package_id` | Package Manager package identifier | Package Manager install steps |
| `dep_newtonsoft_json_version` | Newtonsoft JSON dependency version | Dependency and compatibility tables |
| `dep_ugui_version` | uGUI dependency version | Dependency and compatibility tables |
| `dep_inputsystem_version` | Input System dependency version | Dependency and compatibility tables |
| `dashboard_url` | Convai dashboard URL | API key setup, character ID steps |
| `live_server_url` | Realtime server URL | Connection and networking references |

Reference inline with `<code class="expression">space.vars.unity_sdk_version</code>`. Do not hard-code
the version, package id, or URLs in page body text.

If a value you need has no variable yet, add it to `.gitbook/vars.yaml` in the same change rather than
writing the literal into the page.

## Gold-standard example pages — READ BEFORE DRAFTING

**Before drafting any Unity page, read the example page whose Diataxis mode matches your task.**
Use it as the quality benchmark for lead paragraph style, section count, block selection, and prose
tone. This is a required step, not an optional check.

| Page type | Example page to open |
|---|---|
| Hub / section index | `plugins-and-integrations/convai-unity-sdk/getting-started/README.md` |
| How-to with steppers + tabs | `plugins-and-integrations/convai-unity-sdk/getting-started/installation.md` |
| How-to simple (focused task) | `plugins-and-integrations/convai-unity-sdk/getting-started/configure-api-key.md` |
| How-to multiplatform / subsections | `plugins-and-integrations/convai-unity-sdk/getting-started/configure-microphone.md` |
| Explanation with Mermaid + tables | `plugins-and-integrations/convai-unity-sdk/core-concepts/session-lifecycle.md` |

When in doubt, default to `installation.md` (tabs + steppers) for task pages or `session-lifecycle.md`
for explanation pages. Additional reference pages live under `getting-started/`, `core-concepts/`,
`features/`, `scripting-reference/`, and `troubleshooting/` — open whichever matches most closely.

## Section layout

New Unity SDK pages live under `plugins-and-integrations/convai-unity-sdk/` in these sections:
`overview`, `getting-started`, `compatibility-and-requirements`, `core-concepts`, `features`,
`ui-and-presentation`, `scripting-reference`, `platform-guides`, `advanced-topics`, `utilities`,
`troubleshooting`. Mirror the GitBook navigation; update `SUMMARY.md` when adding a sidebar page.

## Platform and version notes

- Version-sensitive pages (install, compatibility, scripting reference) require `last_reviewed` in
  frontmatter, set to the SDK version verified against.
- Platform guides cover the supported build targets; confirm the current list against
  `compatibility-and-requirements/` before stating platform support.

## SDK source of truth

- Verify Unity component names, fields, events, and runtime behavior against the Convai Unity SDK
  source (the `convai-unity-core-sdk` repository) and the existing pages under `convai-unity-sdk/`.
- Do not fabricate component fields, console messages, or API signatures. If a fact is not in the
  source or existing docs, stop and ask.
