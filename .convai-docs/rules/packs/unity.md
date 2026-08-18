# Unity SDK pack

SDK-specific facts for Convai Unity SDK documentation. Read this before drafting or revising any Unity
page. Generic doctrine lives in `references/`; this pack only supplies Unity specifics.

Last audited: 2026-08-18 against efbb61bf5.

The SDK has a source repository, so most of what a page needs to state is verifiable in code rather
than guessed from memory. Read "Source of truth and verification" before writing anything — it says
exactly which file settles which kind of claim, and which claims code cannot settle.

---

## Product naming

- Use **"Convai Unity SDK"** or **"Convai SDK for Unity"** (the latter is the package `displayName` in
  `package.json`).
- Do **not** call it a "plugin". The docs repo also carries legacy plugin sections
  (`plugins-and-integrations/unity-plugin/` and `unity-plugin-beta-overview/`) — that is the older
  product surface; SDK docs live under `plugins-and-integrations/convai-unity-sdk/` and use "SDK".
- Refer to the backend as "Convai" — "streams audio to Convai", "Convai responds". Never "Convai
  cloud", "cloud backend", "Convai's servers", or "cloud-powered".

## Audience and prerequisites baseline

- Primary audience: Unity developers integrating the Convai Unity SDK. Getting Started pages assume
  limited Unity experience; advanced and reference pages may assume Unity, C#, package management, and
  runtime debugging knowledge.
- Common prerequisites: Unity `<code class="expression">space.vars.unity_min_version</code>`, a Convai
  account, a project API key, and Unity Package Manager access.

## Terminology and concepts

- Use Unity-native terms with correct casing: `Package Manager`, `Inspector`, `GameObject`, `prefab`,
  `scene`, `Play mode`, `Project Settings`, `Build Settings`.
- The thing a reader adds Convai to is a **character**. Format component and class names as inline
  code, exactly as they appear in source: `ConvaiCharacter`, `ConvaiManager`, `ConvaiRoomManager`,
  `ConvaiPlayer`, `ConvaiSceneInstaller`, `ConvaiAudioOutput`, `ConvaiSettings`,
  `ConvaiLipSyncComponent`.
- Names that do **not** exist and must never appear: `ConvaiNPC` (the component is `ConvaiCharacter`),
  `ConvaiAudioManager` (audio output is `ConvaiAudioOutput`; room audio belongs to
  `ConvaiRoomManager`), and bare `ConvaiLipSync` as a class name (the class is
  `ConvaiLipSyncComponent`; `ConvaiLipSyncProfile` and `ConvaiLipSyncMapAsset` are its assets).
- A class name and its Add Component menu label can differ. `StandardRigBinding` appears in the menu
  as **Convai > Embodiment > Character Rig**; `ConvaiLipSyncComponent` as **Convai > Lip Sync > Convai
  Lip Sync**. Use the `[AddComponentMenu]` label when telling a reader where to click, and the class
  name in code and scripting reference.
- Use "in-scene" rather than "game-world". Primary domain framing: training simulations, then
  interactive experiences, then games.

## Architecture orientation

The runtime is a small set of core scene components plus optional feature modules. A writer who only
knows the core components is blind to half the documented surface — read this section before touching
any feature or embodiment page.

### Core components

All paths are relative to the package root, `Packages/com.convai.convai-sdk-for-unity/`. All of these
live in `SDK/Runtime/Components/` except where noted.

| Component | Responsibility |
|---|---|
| `ConvaiManager` | Main Unity entrypoint for the active Convai runtime. One per scene; owns lifecycle and runtime construction (`ConvaiManager.Lifecycle.cs`, `ConvaiManager.RuntimeBuilder.cs`, `ConvaiManager.WebGL.cs`). Its conversation mode enum offers `UseRoomDefaults`, `HandsFree`, `PushToTalk`. |
| `ConvaiRoomManager` | Room connection and room audio, managed by `ConvaiManager`. Lives in `SDK/Runtime/Adapters/Networking/`, split across partials (`.Connection`, `.Audio`, `.Composition`, and others). Microphone input is its job, not the player component's. |
| `ConvaiCharacter` | Per-character component: conversation control, transcript callbacks, character-scoped runtime state. Added to each character connected to Convai. Configured inline or from a `ConvaiCharacterProfile` asset (`SDK/Runtime/Configuration/ConvaiCharacterProfile.cs`). Feature surfaces are partials: `.Actions`, `.Audio`, `.Configuration`, `.Conversation`, `.DynamicContext`, `.Environment`, `.Events`, `.NarrativeDesign`. |
| `ConvaiPlayer` | Player-side equivalent of `ConvaiCharacter`: player identity (name, id, colour) and text messaging. Its `PlayerId` is a local display identifier, **not** the server-generated speaker id used for Long-Term Memory — the source file spells out this distinction; do not conflate them in docs. |
| `ConvaiSceneInstaller` | Explicit scene configuration: registers characters and players with the agent registry on scene load. Preferred over scene discovery for IL2CPP compatibility. |
| `ConvaiAudioOutput` | Optional companion on the same GameObject as `ConvaiCharacter` (enforced by `RequireComponent`); AudioSource configuration and playback for that character's speech. |
| `ConvaiPushToTalkController`, `ConvaiPushToTalkInputReader` | Push-to-talk input handling. |
| `ConvaiSettings` | Project-wide settings `ScriptableObject` (`SDK/Runtime/Configuration/ConvaiSettings.cs`), auto-created at `Assets/Resources/ConvaiSettings.asset`, created manually via **Convai > SDK Settings**. Holds the API environment; the default realtime server URL constant lives here. |

### Feature modules

Each module lives under `SDK/Modules/<folder>/` with its own asmdef (`Convai.Modules.<Name>`), so a
module's presence, assembly name, and public surface are all checkable in that one folder. Most
embodiment modules are driven by a profile asset and surface as one controller component.

| Module | Folder | Main entry point | What it does |
|---|---|---|---|
| Embodiment | `SDK/Modules/Embodiment/` | `ConvaiEmbodimentPresetBinding` (**Convai > Embodiment > Preset**) | Applies a `ConvaiEmbodimentPreset` across the embodiment modules on a character. |
| Gaze | `SDK/Modules/Gaze/` | `ConvaiGazeController` (**Convai > Embodiment > Gaze**) | Decides what the character looks at and articulates it across torso, head, eyes, and eyelids, including full-body turns. Authored through a `ConvaiGazeProfile` asset. Target providers sit under **Convai > Gaze**. |
| Body Animation | `SDK/Modules/BodyAnimation/` | `ConvaiBodyAnimationController` (**Convai > Embodiment > Body Animation**) | Code-driven layered PlayableGraph: idle/talk variants, NavMesh-synced locomotion (`ConvaiNavMeshLocomotion`), backend-triggered actions and gestures, pointing. No Animator Controller asset. Action executors (walk to, follow, gesture, point) register under **Convai > Actions**. |
| Body Language | `SDK/Modules/BodyLanguage/` | `ConvaiBodyLanguageController` (**Convai > Embodiment > Body Language**) | Conversational nonverbal direction — when to gesture, posture, breathing, listening behaviour. Authored through a `ConvaiBodyLanguageProfile` asset. |
| Emotion | `SDK/Modules/Emotion/` | `ConvaiEmotionController` (**Convai > Embodiment > Emotion**) | Consumes server emotion events, smooths scores, and drives the face and authored output bindings via a `ConvaiEmotionProfile`. |
| Conversation Flow | `SDK/Modules/ConversationFlow/` | `ConvaiConversationFlowController` (**Convai > Embodiment > Conversation Flow**) | Tracks whether the character is idle, listening, thinking, or talking. |
| Vision | `SDK/Modules/Vision/` | `ConvaiVisionPublisher` | Publishes a video track to the active room so characters receive visual context from the scene. |
| Narrative | `SDK/Modules/Narrative/` | `ConvaiNarrativeDesignManager`, `ConvaiNarrativeDesignTrigger` | Unity components for Narrative Design: backend sections, triggers, and template-key updates. |
| Lip Sync | `SDK/Modules/LipSync/` | `ConvaiLipSyncComponent` (**Convai > Lip Sync > Convai Lip Sync**) | Maps Convai lip-sync transport data to blendshape playback through `ConvaiLipSyncProfile` and `ConvaiLipSyncMapAsset` assets. |
| Client Voice Activity | `SDK/Modules/ClientVoiceActivity/Sentis/` | `SentisClientVoiceActivityDetector` | Client-side voice activity detection running on Unity Sentis. |

## Install and package model

- Installed through Unity Package Manager or the Asset Store — the two channels documented in
  `getting-started/installation.md`, which is the canonical install page. Package identifier:
  `<code class="expression">space.vars.sdk_package_id</code>`.
- The package declares six dependencies in `package.json`: `com.unity.nuget.newtonsoft-json`,
  `com.unity.ugui`, `com.unity.inputsystem`, `com.unity.ai.navigation`, `com.unity.collections`, and
  `com.unity.modules.xr`. Their versions live in the GitBook variables below — never print them.

## GitBook variables

`.gitbook/vars.yaml` in the documentation repository is the only authority for these values. This pack
lists which variables exist and where they belong, never their current values — a value copied here goes
stale the next release and becomes a wrong fact in the docs. Read `vars.yaml` when you need an actual
value.

| Variable | Holds | Used in |
|---|---|---|
| `unity_sdk_version` | Current SDK release version | Install steps, `last_reviewed`, release references |
| `unity_min_version` | Minimum supported Unity editor version | Prerequisites sections |
| `unity_recommended_version` | Recommended Unity editor version | Prerequisites, compatibility |
| `sdk_package_id` | Package Manager package identifier | Package Manager install steps |
| `dep_newtonsoft_json_version` | Newtonsoft JSON dependency version | Dependency and compatibility tables |
| `dep_ugui_version` | uGUI dependency version | Dependency and compatibility tables |
| `dep_inputsystem_version` | Input System dependency version | Dependency and compatibility tables |
| `dep_ai_navigation_version` | AI Navigation dependency version | Dependency and compatibility tables |
| `dep_collections_version` | Collections dependency version | Dependency and compatibility tables |
| `dep_modules_xr_version` | XR module dependency version | Dependency and compatibility tables |
| `dashboard_url` | Convai dashboard URL | API key setup, character ID steps |
| `live_server_url` | Realtime server URL | Connection and networking references |

Reference inline with `<code class="expression">space.vars.unity_sdk_version</code>`. Do not hard-code
the version, package id, or URLs in page body text. If a value you need has no variable yet, add it to
`.gitbook/vars.yaml` in the same change rather than writing the literal into the page.

## Source of truth and verification

**Repository:** `convai-unity-core-sdk` — a Unity project whose actual package is
`Packages/com.convai.convai-sdk-for-unity/`. The repository path is per-machine — ask for it, never
guess it. All paths below are relative to that package root.

### What the code settles

| Claim | Where to verify |
|---|---|
| Package name, display name, dependency list, minimum Unity version, bundled samples | `package.json` (state the values through `space.vars`, not literals) |
| A core component's existence, serialized fields, defaults, and Inspector help text | its `.cs` file in `SDK/Runtime/Components/` — `[Tooltip]` attributes are the Inspector text |
| The exact Add Component menu path for any component | that class's `[AddComponentMenu]` attribute — search the attribute string, since class name and menu label can differ |
| `ConvaiCharacter` / `ConvaiManager` API surface for a feature area | the matching partial file, e.g. `ConvaiCharacter.NarrativeDesign.cs`, `ConvaiManager.WebGL.cs` |
| Room, connection, and microphone behaviour | `SDK/Runtime/Adapters/Networking/ConvaiRoomManager*.cs` |
| Which feature modules exist and their assembly names | `SDK/Modules/<module>/*.asmdef` |
| A module's components, profile assets, and executors | that module's `Components/`, `Profiles/`, `Executors/` folders |
| Settings asset location, creation menu, defaults | `SDK/Runtime/Configuration/ConvaiSettings.cs` |
| Editor windows and Project Settings surface | `SDK/Editor/` (`ConvaiSettingsProvider.cs`, `ConfigurationWindow/`, `Inspectors/`) |
| Sample names, descriptions, and paths | the `samples` array in `package.json`; content under `Samples/` |

### What the code cannot settle

These need the product owner, the backend team, or the running product. Do not infer them:

- **Backend behaviour.** The SDK shows the client contract — what is sent and what is handled — not
  what Convai does with it, which models run, or any server-side limit. A field existing on a request
  does not prove the backend honours it.
- **Plan and pricing gating.** Nothing in the SDK maps features to subscription tiers.
- **Asset Store channel state.** Which version is live on the Asset Store, and its listing content,
  are not in this repository.
- **Rendered Editor appearance.** Inspector layout and screenshots come from running the Editor, not
  from reading attributes.
- **Current variable values.** `.gitbook/vars.yaml` in the docs repo is the authority for every value
  a page prints; `package.json` is where the release process reads from, but pages reference the
  variable, never either literal.

### What does not count as proof

The package ships an in-repo `Documentation~/` directory (`EMBODIMENT.md`, `GAZE.md`, `ACTIONS.md`,
`PLATFORMS.md`, and more). It is genuinely useful for orientation — read it to find where a feature
lives, then verify every fact you take from it against the code. It is prose that nothing recompiles
when a class changes. The same applies to `README.md` files inside modules, `CHANGELOG.md`, existing
published pages, and memory of the API. See "In-repo documentation is a lead, not a source of truth"
in `references/safe-publishing.md`.

If a fact cannot be proven from code and nobody has confirmed it, the page does not state it.

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
for explanation pages.

## Section layout

Unity SDK pages live under `plugins-and-integrations/convai-unity-sdk/` in these sections:

```
convai-unity-sdk/
├── overview/
├── getting-started/
├── compatibility-and-requirements/
├── authentication/
├── core-concepts/
├── embodiment/              per-module subfolders: body-animation, body-language,
│                            conversation-flow, emotion, gaze
├── features/
├── ui-and-presentation/
├── scripting-reference/
├── platform-guides/
├── advanced-topics/
├── ai-coding-assistant/
└── troubleshooting/
```

There is no `utilities/` section. `embodiment/` mirrors the module architecture above — a page about
Gaze, Emotion, Body Animation, Body Language, or Conversation Flow belongs there, not in `features/`.
Mirror the GitBook navigation; update `SUMMARY.md` when adding a sidebar page.

## Platform and version notes

- Version-sensitive pages (install, compatibility, scripting reference) require `last_reviewed` in
  frontmatter, set to the SDK version verified against.
- State platform support from the pages under `compatibility-and-requirements/`, cross-checked against
  `Documentation~/PLATFORMS.md` in the package. Do not infer support from file names alone — the
  package contains WebGL-specific code (`ConvaiManager.WebGL.cs`) and depends on
  `com.unity.modules.xr`, but what those imply about supported build targets is a claim for the
  compatibility pages and the owner, not for a grep.
- Historical version references in migration pages ("retired in <release>", "changed in SDK
  <release>") are deliberate frozen facts about a specific past release and are the one legitimate
  use of a literal version number in body text.

## Bundled samples

Declared in the `samples` array of `package.json`; refer to them by their exact display names.

| Sample | Path | Purpose |
|---|---|---|
| Basic Sample | `Samples~/BasicSample` | Core SDK setup and interaction flow with a non-humanoid character |
| LipSync Sample | `Samples~/LipSyncSample` | High-quality character with real-time lip sync |

No official tutorial video transcripts are catalogued for this SDK yet; if a task supplies one, verify
its claims against source like any other lead before quoting it.
