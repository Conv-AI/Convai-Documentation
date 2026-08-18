# Unreal Engine pack

SDK-specific facts for Convai Unreal Engine documentation. Read this before drafting or revising any
Unreal page. Generic doctrine lives in `references/`; this pack only supplies Unreal specifics.

Verified against the Convai Unreal plugin source (`ConvAI.uplugin`, `Source/Convai/`,
`Source/ConvaiEditor/`, `Source/ConvaiToolset/`, `Source/Convai/Public/ConvaiDefinitions.h`,
`Source/Convai/Convai.h`, plugin `Content/` folder, `CHANGELOG.md`, `.github/workflows/main.yml`).
Last audited: 2026-08-18 against 1f06778d.

## Product naming

- The Unreal integration **is** an Unreal Engine plugin — call it the **"Convai Unreal Engine plugin"**
  or **"Convai plugin for Unreal Engine"**. (This differs from Unity, where the product is the "Convai
  Unity SDK" and must not be called a plugin.) The `.uplugin` `FriendlyName` is `Convai`.
- Refer to the backend as "Convai" — never "Convai cloud", "Convai's servers", or "cloud-powered".

## Audience and prerequisites baseline

- Primary audience: Unreal Engine developers. The plugin is **Blueprint-first** (it "adds new Blueprint
  functions and components to integrate Convai"); C++ usage is possible but secondary.
- Common prerequisites: a supported Unreal Engine version (see "Platform and version notes" for how
  the range is derived — do not hardcode it), a Convai account, an API key, and the `AudioCapture`
  engine plugin (bundled as an enabled dependency).
- Supported platforms: **Win64**, **Mac**, and **Android** (from the runtime modules'
  `PlatformAllowList` in `ConvAI.uplugin`; the editor-side modules allow Win64 and Mac).

## Terminology and concepts

- Use Unreal-native terms with correct casing: `Actor`, `Component`, `Blueprint`, `Details` panel,
  `Content Browser`, `Subsystem`, `.uasset`, `Edit > Plugins`.
- Format Convai class names as inline code (verify each against source before use):
  - `UConvaiChatbotComponent` — the main conversation component (Blueprint display name **"Convai
    Chatbot"**), derives from `UConvaiConversationComponent`. Added to the NPC Actor. Holds a
    `UConvaiConnectionSessionProxy` for its character — it does **not** own the WebRTC client
    directly. The actual WebRTC client (`ConvaiClient`) lives in `UConvaiSubsystem`. Write:
    "the chatbot holds a session proxy; `UConvaiSubsystem` manages the WebRTC client."
  - `UConvaiPlayerComponent` — the player interaction component (Blueprint display name **"Convai
    Player"**), derives from `UConvaiConversationComponent`. Added to the player Pawn. Manages
    microphone capture, push-to-talk, hands-free VAD, text input, and session initiation.
  - `UConvaiObjectComponent` — the scene object component (Blueprint display name **"Convai Object
    Component"** — derived from class name; no explicit `DisplayName` in UCLASS meta, re-verified
    this audit). Drop on any Actor to register it with all chatbots in the level. Provides object
    name, description, object scoping and movement targeting (`EConvaiObjectReference` plus the
    Movement Points system on `FConvaiObjectEntry`), movement awareness
    (`FConvaiObjectMovementSettings` / `EConvaiMovementSensitivity`), and live property tracking
    (`FConvaiTrackedProperty`).
  - `UConvaiFaceSyncComponent` — face/lip sync component (Blueprint display name **"Convai Face Sync"**),
    derives from `USceneComponent`.
  - `UConvaiAudioCaptureComponent` — microphone capture component (Blueprint display name **"Convai
    Audio Capture"**). BlueprintSpawnable; added alongside `UConvaiPlayerComponent` when explicit
    capture control is needed.
  - `UConvaiSubsystem` — engine subsystem (display name **"Convai Subsystem"**). **Do not create a
    standalone reference page for this.** Embed it as a section inside core-concepts → session-lifecycle.
    The user-facing Blueprint surface is: nodes `GetServerConnectionState`, `ResetIdleTimer`,
    `InvalidateOrphanedConnection`; events `OnServerConnectionStateChangedEvent`, `OnUserIdleWarning`.
  - `UConvaiActions` — Blueprint function library for character actions.
  - `UConvaiSettings` — settings object holding the API key and project-wide defaults (see Install and
    package model). Lives in `Source/Convai/Convai.h`.
  - `UConvaiConversationComponent` — abstract base class for both `UConvaiChatbotComponent` and
    `UConvaiPlayerComponent`. Referenced by name when a parameter type accepts either component (e.g.
    `SendText()` accepts `UConvaiConversationComponent`).
- Use Convai feature ownership as the primary documentation boundary. Document shipped Convai features
  and their user-facing Blueprint workflows, including new features added in future plugin releases after
  source verification. A Blueprint node's REST/HTTP implementation detail does not make it documentable
  on its own.
- Document only the Unreal REST/HTTP surfaces that belong to a shipped Convai feature workflow:
  - **Long-term memory** nodes under **`Convai|LTM`**: speaker ID management and character LTM status.
  - **Narrative design** fetch nodes under **`Convai|REST API`**: `Convai Fetch Narrative Sections`
    and `Convai Fetch Narrative Triggers`.
- Do **not** document the rest of the plugin's REST/HTTP surface as user-facing Unreal docs:
  - character management nodes under **`Convai|REST API`** (`Convai Create Character`,
    `Convai Update Character`, `Convai Get Character Details`, `Convai Get All Characters IDs`,
    `Convai Download Image`, `Convai Download Image using RPM Link`, `Convai Get Available Voices`,
    and related helpers).
  - types that exist only to support those character-management or voice-list helpers: `EVoiceType`,
    `ELanguageType`, `EGenderType`, `FAvailableVoices`, `FVoiceLanguageStruct`, and related structs
    or enums.
  - deprecated fields on `UConvaiChatbotComponent` that those nodes populate: `VoiceType`,
    `Backstory`, `LanguageCode`, `ReadyPlayerMeLink`, `AvatarImageLink`. These exist in source
    as `BlueprintReadOnly` replicated properties but are no longer in active use.
  - speech-to-text and text-to-speech nodes under **`Convai|Http`**.
  - deprecated chatbot `getResponse` nodes under **`Convai|DEPRECATED`**.
  - editor-only HTTP implementation details from `ConvaiEditor`.
  - raw `EConvaiEndpoint` / `UConvaiURL` endpoint inventory or URL-construction internals.
  - `blueprint-reference/character-management.md` is a **known violation** of this rule. Do not
    link to it from any hub, feature map, index, or guide. Flag it for deprecation or removal.
- Voice for a character is configured on the character in the **Convai dashboard** — there is no
  user-facing in-plugin voice selection enum. Do not reference any voice-type enum; it is deprecated.
- Use "in-scene" / "in-level" framing. Choose the example domain (training simulation, interactive
  experience, game) that best explains the feature being documented. Do not force any particular domain.

## Lip sync modes

Configured on `UConvaiFaceSyncComponent`. Source enum: `EC_LipSyncMode` (in `ConvaiDefinitions.h`).
Available modes (verified in `ConvaiDefinitions.h`):

| Mode | Display name | Source enum value | When to use |
|---|---|---|---|
| Disabled | `Off` | `Off` | No lip sync |
| Automatic | `Auto` | `Auto` | Plugin selects mode based on rig |
| Viseme-based | `Viseme Based` | `VisemeBased` | General phoneme-driven rigs |
| MetaHuman blendshapes | `MetaHuman Blendshapes` | `BS_MHA` | MetaHuman and CC5 characters |
| ARKit blendshapes | `ARKit Blendshapes` | `BS_ARKit` | CC4 characters |
| CC4 extended blendshapes | `CC4 Extended Blendshapes` | `BS_CC4_Extended` | CC4 characters (extended set) |

**Rig guidance:** MetaHuman and CC5 → **MetaHuman Blendshapes**; CC4 → **ARKit Blendshapes** (or
CC4 Extended Blendshapes for the extended set).

## Key enums

Document these enums by their display names. Always verify a display name against source before
writing it. **Do not document any enum that belongs to or supports the `Convai|REST API` surface**
— this includes `ETTS_Voice_Type`, `EVoiceType`, `ELanguageType`, `EGenderType`, and any other
type that only appears in REST API node signatures. These are off-limits across all pages.

| Enum class | Source location | Values (display names) | Used in |
|---|---|---|---|
| `EC_LipSyncMode` | `ConvaiDefinitions.h` | Off, Auto, Viseme Based, MetaHuman Blendshapes, ARKit Blendshapes, CC4 Extended Blendshapes | `UConvaiFaceSyncComponent` |
| `EBasicEmotions` | `ConvaiDefinitions.h` | Happy, Calm, Afraid, Surprise, Sad, Bored, Angry | Emotion system, animation |
| `EEmotionIntensity` | `ConvaiDefinitions.h` | Basic, Less Intense, More Intense | Emotion system |
| `EC_ConnectionState` | `ConvaiDefinitions.h` | Disconnected, Connecting, Connected, Reconnecting | `UConvaiSubsystem`, session lifecycle |
| `EC_ContextUpdateMode` | `ConvaiDefinitions.h` | Append, Replace, Reset | Dynamic context feature |
| `EC_RunLLMOption` | `ConvaiDefinitions.h` | Auto, Always, Never | Object component, dynamic context, tracked properties |
| `EConvaiActionParamType` | `ConvaiDefinitions.h` | Auto, Actor Reference, String, Number, Bool, Enum | Parameterized actions |
| `EConvaiObjectReference` | `ConvaiDefinitions.h` | Whole Actor, Specific Component | `FConvaiObjectEntry` (shown as **Object Is**) — gaze/attention scope and movement fallback |
| `EConvaiMovementPointAttachment` | `ConvaiDefinitions.h` | Relative To Object, Keep World Position | `FConvaiMovementPoint.Attachment` |
| `EConvaiContextDelivery` | `ConvaiDefinitions.h` | Send Normally, Wait Until Conversation Is Idle | Dynamic context delivery, `FConvaiTrackedProperty.Delivery`, spatial preferences |
| `EConvaiMovementSensitivity` | `ConvaiDefinitions.h` | Very Low, Low, Medium, High, Very High | `FConvaiObjectMovementSettings` (object movement awareness) |
| `EConvaiObjectNameSuffixStyle` | `ConvaiDefinitions.h` | Numeric (2, 3, 4), Alphabetical (A, B, C) | Duplicate object-name disambiguation; project setting on `UConvaiSettings` |
| `EConvaiAttentionSource` | `ConvaiDefinitions.h` | None, Explicit (Blueprint/C++), Gaze | Gaze attention system |

`EConvaiMoveTarget` no longer exists in source (removed with the Movement Points rework). Do not
reference it; existing docs that mention it are stating a dead type.

## Key structs

Document these structs at the page level where they appear. Verify every field name and type against
source before writing it.

| Struct | Source location | Key fields | Used in |
|---|---|---|---|
| `FConvaiAction` | `ConvaiDefinitions.h` | `bEnabled`, `Name`, `Description`, `Parameters` (array of `FConvaiActionParam`), `bWaitForBotSpeech`, `DelayAfterBotSpeechSec` | Chatbot component action config |
| `FConvaiActionParam` | `ConvaiDefinitions.h` | `Name`, `Description`, `Type` (`EConvaiActionParamType`), `Connector`, `Choices`, `EnumType` | Inside `FConvaiAction.Parameters` |
| `FConvaiResultAction` | `ConvaiDefinitions.h` | `Action`, `ActionString`, `Parameters` (map of `FConvaiResultParam`), `bWaitForBotSpeech`, `DelayAfterBotSpeechSec` (deprecated mirrors: `RelatedObjectOrCharacter`, `ConvaiExtraParams`) | Action received events |
| `FConvaiObjectEntry` | `ConvaiDefinitions.h` | `Ref` (Actor), `OptionalPositionVector` (deprecated auto-written snapshot — point readers at Resolve Goal Location's `Out Goal Location` output), `Name`, `Description`, `ObjectReference` (`EConvaiObjectReference`, shown as **Object Is**), `ComponentName`, `SocketOrBoneName`, `AcceptanceRadius`, `MovementPoints` (array of `FConvaiMovementPoint`), `bFallbackToObjectWhenPointsUnreachable` | Environment, action results, object targeting |
| `FConvaiMovementPoint` | `ConvaiDefinitions.h` | `Transform`, `Attachment` (`EConvaiMovementPointAttachment`), `bEnabled`, `bCreatesSeparateDestination` (shown as **Create Separate Destination**), `Name` (shown as **Destination Name**) | Movement Points list on `FConvaiObjectEntry`; edited via the viewport visualizer on Convai Object components |
| `FConvaiTrackedProperty` | `ConvaiDefinitions.h` | `PropertyPath`, `Alias`, `Description`, `StateValueDescriptions` (array of `FConvaiTrackedPropertyStateValueDesc`), `ShouldRespond` (`EC_RunLLMOption`), `Delivery` (`EConvaiContextDelivery`), `bFlushImmediately` | `UConvaiObjectComponent` live state tracking |
| `FConvaiVADSettings` | `ConvaiDefinitions.h` | `bUseServerDefault`, `Confidence`, `StartSecs`, `StopSecs`, `MinVolume` | `UConvaiPlayerComponent`, project VAD defaults |
| `FConvaiSpeakerInfo` | `ConvaiDefinitions.h` | `SpeakerID`, `Name`, `DeviceID` | Long-term memory, speaker identity |
| `FNarrativeSection` | `ConvaiDefinitions.h` | `section_id`, `section_name`, `objective`, `decisions`, `updated_character_data` | Narrative design |
| `FNarrativeTrigger` | `ConvaiDefinitions.h` | `trigger_id`, `trigger_name`, `trigger_message`, `destination_section` | Narrative design |

## Character rigs

### MetaHuman

Works out of the box — no extra assets or animation Blueprint required.
Reference video: https://youtu.be/4fMCKkrfyaA

### Reallusion / Character Creator (CC)

Requires a separate Convai Reallusion animation Blueprint:

1. Download the animation Blueprint from:
   https://drive.google.com/drive/folders/1k3072DH3zJXk2xTg-CJ_najnm0pyvZJS
2. Copy it into the project `Content/` folder.
3. Set up the animation graph as shown in the reference video.
4. In the character's **Skeletal Mesh Component**, set the **Animation Class** to
   **"Convai Reallusion Animation Blueprint"**.

Reference video: https://www.youtube.com/watch?v=nyPNP-S92QI

## Vision

Vision is a **stable** feature in the current plugin version. It is not experimental. Document it
as any other production-ready feature.

## Gaze attention

The gaze attention system allows `UConvaiPlayerComponent` to track which scene object the player
is looking at and expose it to chatbots as the "attention object". Key concepts:

- `EConvaiAttentionSource` enum controls how the chatbot's current attention object was set: `None`,
  `Explicit (Blueprint/C++)` (set programmatically), or `Gaze` (set by the gaze system).
- Gaze attention raises highlight events via `UConvaiObjectComponent` and `UConvaiPlayerComponent`
  gaze delegates.
- The `M_ConvaiGazeOverlay` material (in `Content/Highlights/`) provides the visual highlight effect.
  (The `Content/Tools/` generator script that previously produced it is no longer in the plugin;
  do not reference it.)
- Document in `features/gaze-attention/` section. Reference `EConvaiAttentionSource` and the gaze
  event delegates on both the player and object components.

## Install and package model

The plugin is distributed through two channels. Document both; note the tradeoff.

### Method 1 — Fab (Epic Games Marketplace)

Listing: https://www.fab.com/listings/ba3145af-d2ef-434a-8bc3-f3fa1dfe7d5c

1. Add the plugin to your Epic Games account from Fab.
2. Open the Epic Games Launcher → Library → find **Convai**.
3. Click **Install to Engine** or **Add to project**.
4. Enable under **Edit > Plugins** → search "Convai" → enable → restart the editor.

Fab updates less frequently; newer features appear on GitHub Releases first.

### Method 2 — GitHub Releases (latest features)

Releases page: https://github.com/Conv-AI/Convai-UnrealEngine-SDK-V4/releases

1. Choose the release matching your target plugin version **and** target UE version.
2. Download the `.zip` file.
3. Extract the archive. The extracted folder should be named `Convai` and contain `ConvAI.uplugin`
   at its root.
4. In the project root, create a `Plugins/` folder if one does not exist.
5. Move the extracted Convai plugin folder into `Plugins/`.
6. Enable under **Edit > Plugins** → search "Convai" → enable → restart the editor.

GitHub Releases update more frequently and carry new features before they reach Fab.

Quick-setup video (covers both methods): https://youtu.be/n-UG3nmMeZQ

### Modules

- `Convai` (Runtime) — Win64, Mac, and Android (`PlatformAllowList`)
- `ConvaiEditor` (Editor) — Win64 and Mac
- `ConvaiAnimGraph` (UncookedOnly) — Win64 and Mac
- `ConvaiVisionBase` (Runtime) — Win64, Mac, and Android
- `ConvaiToolset` (Editor) — Win64 and Mac. Registers the Convai AI toolset — AI-callable editor
  setup actions exposed as MCP tools — with the engine `ToolsetRegistry` plugin. Editor-only; on
  engine versions without `ToolsetRegistry` it compiles as an empty module (gated in
  `Source/ConvaiToolset/ConvaiToolset.Build.cs`).

### Enabled plugin dependencies

| Plugin | Enabled | Notes |
|---|---|---|
| `ToolsetRegistry` | Yes (Optional) | Backs the Convai AI toolset / MCP editor tooling used by `ConvaiToolset`. Marked `Optional` in the source `.uplugin`; the CI packaging step (`.github/workflows/main.yml`) rewrites it to required on engine versions where the engine plugin exists and keeps it optional below that |
| `AudioCapture` | Yes | Microphone capture; required on all platforms |
| `AndroidPermission` | Yes | Microphone permission handling on Android; document platform-specific steps |
| `EditorScriptingUtilities` | Yes | Editor tooling dependency; no user configuration required |
| `PropertyAccessEditor` | Yes | Powers the **Bind** picker on `FConvaiTrackedProperty.PropertyPath`; no user configuration required |
| `AndroidFileServer` | No | Disabled; do not document |

### API key and the Convai Editor window

The API key is configured through the **Convai Editor window** (the in-editor panel, accessible from
the Unreal toolbar or the **Convai** menu). Enter the API key in the provided field and save. The key
is stored on `UConvaiSettings` (`API_Key`, a `Config` property — managed automatically by the editor
UI; read-only in Project Settings).

Project-wide defaults also live on `UConvaiSettings` in **Edit > Project Settings > Plugins > Convai**:
- **Audio Settings | VAD** — `FConvaiVADSettings` for project-wide voice activity detection defaults.
- **Lip Sync Mode** — default `EC_LipSyncMode` applied to all characters unless overridden per-component.
- Further categories exist on `UConvaiSettings` in source: **Spatial Awareness**, **Objects**
  (including the `EConvaiObjectNameSuffixStyle` suffix style), **Debug Overlay**, and **Long Term
  Memory**. Verify field names and display names in `Source/Convai/Convai.h` before documenting
  any of them.

Document the Convai Editor window only from the user's perspective: how to open it, what fields it
exposes, and what actions it enables. Do not document its internal implementation or code-level calls
(`SetAPIKey()`, `SaveSettings()`, etc.).

## GitBook variables

`.gitbook/vars.yaml` in the Convai-Documentation repo is the only authority for these values. This pack
records which variables exist and where each value is derived from, never the value itself — a value
frozen here goes stale at the next release and becomes a wrong fact in the docs.

| Variable | Holds | Derive from | Used in |
|---|---|---|---|
| `unreal_plugin_version` | Current plugin release version | `VersionName` in the `.uplugin` file | Install steps, release references |
| `unreal_min_version` | Minimum supported Unreal Engine version | Not derivable from `ConvAI.uplugin` — it has **no `EngineVersion` field**. Read the "Kept compatibility with Unreal Engine ..." line in the latest `CHANGELOG.md` release entry; see "Platform and version notes" for why the CI matrix says something different | Prerequisites |
| `dashboard_url` | Convai dashboard URL | Stable product URL | API key and character setup |

If a variable is missing from `vars.yaml`, add it there in the same change instead of writing the
literal value into a page.

## Gold-standard example pages

No Unreal gold-standard page exists yet. **Once the first Unreal work unit is reviewed and accepted
by the human, add those Unreal page paths here and update this note.** Subsequent pages must match
their structure, tone, and depth.

Until Unreal gold-standard pages are established, use the **Unity** docs as the cross-SDK structural
reference — matching their depth, page count per section, and quality bar, but not their
Unity-specific layout or content. Unreal pages must reflect Blueprint-first workflows and
Unreal-native terminology. Before drafting, open the closest Unity example for the Diataxis mode
you are writing:

| Page type | Unity example to open |
|---|---|
| Hub / section index | `plugins-and-integrations/convai-unity-sdk/getting-started/README.md` |
| How-to with steppers + tabs | `plugins-and-integrations/convai-unity-sdk/getting-started/installation.md` |
| How-to simple (focused task) | `plugins-and-integrations/convai-unity-sdk/getting-started/configure-api-key.md` |
| How-to multiplatform / subsections | `plugins-and-integrations/convai-unity-sdk/getting-started/configure-microphone.md` |
| Explanation with Mermaid + tables | `plugins-and-integrations/convai-unity-sdk/core-concepts/session-lifecycle.md` |

Reading the Unity example is mandatory — it calibrates structure and quality, not content.

## Section layout

- New pages go under `plugins-and-integrations/convai-unreal-engine-plugin/` in the Convai-Documentation
  repo. This is the active, structured section with full hierarchy (overview, compatibility-and-requirements,
  getting-started, core-concepts, features, blueprint-reference, editor-window, troubleshooting).
- The `plugins-and-integrations/unreal-engine/` folder is **legacy**. Do not add new pages there.
- Mirror Unity's section types where they fit the Unreal plugin. Every section must reach
  Unity-comparable depth (see the depth baseline in `plans/_plan-template.md`).
- Add the proposed `SUMMARY.md` subtree when planning.

## Platform and version notes

- The current release is a **beta**. The version string lives in `VersionName` in `ConvAI.uplugin`;
  the docs value is the `unreal_plugin_version` variable in `.gitbook/vars.yaml`. Never write the
  literal version into a page — or into this pack. Mark all version-sensitive pages with
  `last_reviewed`.
- Supported UE versions: `ConvAI.uplugin` has **no `EngineVersion` field**, so the range is not
  derivable from the manifest. Two sources look contradictory and are not — they measure different
  things, and a page that confuses them will turn readers away:
  - **`CHANGELOG.md` is the support range.** Every recent release entry ends with a
    "Kept compatibility with Unreal Engine ..." line. Read the latest one. It is the plugin's own
    statement of what it supports, and it names an upper bound as well as a lower one, so "all UE
    5.x, no upper bound" is not a safe claim.
  - **`.github/workflows/main.yml` is the prebuilt-package range**, which starts higher. It is which
    engine versions CI produces binaries for, not which versions the plugin supports. Since the
    plugin descriptor no longer carries the precompiled "Installed" flag, Fab compiles from source
    per engine version, so a reader below the CI floor can still use the plugin — they build it.
    `Docs/InternalChangelog.md` records manually verified builds below that floor.

  So the support floor comes from `CHANGELOG.md`, and the CI matrix is only worth mentioning on a
  page if the distinction between a prebuilt package and building from source matters to the reader.
  Both values move: re-read them rather than trusting this pack's audit date.
- Platforms: Win64, Mac, and Android (runtime modules; editor modules are Win64 and Mac). Android
  requires the `AndroidPermission` plugin (bundled dependency) and microphone permission handling —
  document platform-specific steps where relevant. Mac is newly allowed relative to earlier
  releases (the beta.23-hotfix changelog entry declared Win64/Android only); no Mac-specific setup
  steps exist in source, so confirm any Mac install guidance with the plugin owner before writing it.

## SDK source of truth

- Plugin manifest: `ConvAI.uplugin`
- Runtime gameplay surface: `Source/Convai/Public/` (components, proxies, audio, vision, gaze,
  dynamic context, environment) and `Source/Convai/Convai.h` (`UConvaiSettings`)
- Enum values and display names: `Source/Convai/Public/ConvaiDefinitions.h`
- Editor UI / configuration: `Source/ConvaiEditor/`

Verify every class, component, Blueprint node display name, setting, and console message against
this source before stating it. Do not fabricate Blueprint node names or component fields.

### What the code settles

| Claim | Where to verify |
|---|---|
| Plugin version string | `VersionName` in `ConvAI.uplugin` |
| Modules, module types, platform allow lists | `Modules` in `ConvAI.uplugin` |
| Bundled plugin dependencies and whether each is enabled or optional | `Plugins` in `ConvAI.uplugin` |
| Class names, Blueprint display names, component properties | `UCLASS` / `UPROPERTY` declarations in `Source/Convai/Public/` |
| Enum values and their exact display names | `UMETA(DisplayName = ...)` in `Source/Convai/Public/ConvaiDefinitions.h` |
| Struct fields, defaults, and deprecations | `USTRUCT` declarations in `ConvaiDefinitions.h` (deprecations carry `DeprecatedProperty` meta with a message) |
| Blueprint node names and categories | `UFUNCTION` meta (`DisplayName`, `Category`) in the component and proxy headers |
| Project settings surface | `UConvaiSettings` in `Source/Convai/Convai.h` |
| Bundled assets and folder layout | the plugin `Content/` folder |
| Per-engine-version packaging differences (what ships where) | `.github/workflows/main.yml` |

### What the code cannot settle

These need the plugin owner, or a look at the released product. Do not infer them:

- **Whether the changelog's stated range is still current on the day you write.** It is the best
  source available and it is maintained per release, but it is prose in a file, not a build
  constraint — nothing fails if it goes stale. Confirm with the plugin owner before publishing a
  version claim on a prerequisites page.
- **Fab listing state and release cadence.** The source says nothing about what is currently
  published on Fab or GitHub Releases, or how far Fab lags behind.
- **Server-side behavior.** VAD server defaults (`bUseServerDefault`), when `EC_RunLLMOption::Auto`
  produces a response, and anything else the Convai backend decides. The local defaults in source
  are fallbacks, not the served values.
- **Dashboard behavior.** Character configuration, voices, and everything else done on the Convai
  dashboard lives outside this repo.

## Tutorials & external sources

Official tutorial videos produced by Convai:

| Topic | Video URL | Transcript |
|---|---|---|
| Quick plugin setup | https://youtu.be/n-UG3nmMeZQ | `.convai-docs/sources/unreal/plugin-quick-setup-transcript.md` |
| MetaHuman character setup | https://youtu.be/4fMCKkrfyaA | `.convai-docs/sources/unreal/metahuman-setup-transcript.md` |
| Reallusion / CC character setup | https://www.youtube.com/watch?v=nyPNP-S92QI | `.convai-docs/sources/unreal/reallusion-setup-transcript.md` |

**Transcript convention:** transcripts live under `.convai-docs/sources/<sdk>/` in the documentation
repo. They are auto-generated captions and contain OCR/transcription errors. Apply these corrections
whenever quoting from a transcript:

| Auto-caption (wrong) | Correct |
|---|---|
| Convey | Convai |
| Realusion | Reallusion |
| Neurosync | NeuroSync |
| quicks bridge / quixel bridge (any variant) | Quixel Bridge |
| forum.convey.com | forum.convai.com |

When a video covers a feature being documented, use the transcript (with corrections applied) as a
planning and writing source alongside the SDK source. The transcript captures the intended user
workflow; the source code provides authoritative API names and behavior. If a transcript and source
conflict, the source wins.

## Bundled sample/demo assets

The plugin ships a set of reusable Blueprint, animation, and widget assets inside the plugin's own
`Content/` folder. They are available in any project with the plugin enabled — no separate project
import is needed. **There is no bundled demo level/map** — no `.umap` exists anywhere in `Content/`,
and there is no `Convai_Demo`, `Companion`, or `ConvaiDemoGM` asset. Downloadable sample content is
offered through the Convai editor window **Samples** page (a content feed), not as a shipped level.

For local source verification in the current Unreal plugin development checkout, use
`C:\Users\Kaan\Documents\UnrealProjects\Convai-UnrealEngine-SDK-Dev\Content` as the plugin content
root. MetaHuman animation assets and animation Blueprint references are under
`C:\Users\Kaan\Documents\UnrealProjects\Convai-UnrealEngine-SDK-Dev\Content\MetaHumans\Animations`.
Published documentation should still use plugin-relative paths such as `MetaHumans/Animations/`.

| Asset name | Path | Type | Purpose |
|---|---|---|---|
| `BP_ConvaiChatbotComponent` | `ConvaiConveniencePack/ConvaiBPComponent/` | Blueprint component | Preconfigured chatbot component example |
| `BP_ConvaiPlayerComponent` | `ConvaiConveniencePack/ConvaiBPComponent/` | Blueprint component | Player interaction component example |
| `BP_ConvaiSamplePlayer` | `ConvaiConveniencePack/Sample/` | Player Blueprint | Sample player character for interacting with Convai NPCs |
| `BP_SampleGameMode` | `ConvaiConveniencePack/Sample/` | Game Mode Blueprint | Sample game mode for demo scenes |
| `BP_Convai3DWidgetComponent` | `ConvaiConveniencePack/3DWidget/` | Blueprint component | In-world 3D chat widget component |
| `WBP_3DChatWidget` | `ConvaiConveniencePack/3DWidget/` | Widget Blueprint | In-world 3D chat widget UI |
| `ConvaiBaseCharacter` | `Core/` | Character Blueprint | Base character class for Convai NPCs |
| `ConvaiBasePlayer` | `Core/` | Pawn Blueprint | Base player class |
| `ConvaiPlayerWithVoiceActivation` | `Core/` | Pawn Blueprint | Base player with voice-activation capture |
| `Convai_MetaHuman_BodyAnim` | `MetaHumans/Animations/` | Animation Blueprint | MetaHuman body animation for Convai characters |
| `Convai_MetaHuman_FaceAnim` | `MetaHumans/Animations/` | Animation Blueprint | MetaHuman face/lip sync animation |
| `Full_Emotion_spectrum` | `MetaHumans/Animations/Motion/Face/Emotion/` | Animation | Full emotion blendshape spectrum (note: lowercase `spectrum`) |
| `Full_Emotion_NoMouth_spectrum` | `MetaHumans/Animations/Motion/Face/Emotion/` | Animation | Emotion spectrum excluding mouth shapes |
| `M_ConvaiGazeOverlay` | `Highlights/` | Material | Gaze-attention highlight overlay |
| `BPI_Convai_Animation` | `Interfaces/` | Blueprint Interface | Animation interface for Convai characters |
| `AudioInput` / `MuteMic` | `Submixes/` | Sound Submix | Microphone capture / mute submixes |
| `EUW_LTM` | `Editor/` | Editor Utility Widget | Long-term-memory editor utility |
| `Chat_WB` | `Widgets/` | Widget Blueprint | Main chat UI |
| `ChatItem_WB` | `Widgets/` | Widget Blueprint | Individual chat message item |
| `MicSettings_WB` | `Widgets/` | Widget Blueprint | Microphone settings UI |

The plugin also bundles:

- A large MetaHuman animation library under `MetaHumans/Animations/Motion/` — body (`Anim_*`),
  face (`MHF_*`, split into `Face/Emotion`, `Face/Eyes`, `Face/Lips`), head-look/point (`Pose_*`)
  — with supporting animation Blueprints under `MetaHumans/Animations/AnimBP/` (`A1D_MH_BEye`,
  `A2D_MH_EyeLook`, `B1D_F/M_Movement`, `B2D_F/M_HeadLook`, `B2D_F/M_Pointing`).
- Instrument enums and functions under `MetaHumans/Instruments/` — enums in `Enm/` (`E_Emotions`,
  `E_InConversation`, `E_Lips`, `E_Movement`, `E_TurnDirection`), functions in `Functions/`
  (`F_AIUtilities`).
- Agent skill assets under `Skills/` — 17 `.uasset` skill documents (`ConvaiQuickStart`,
  `ConvaiProjectSetup`, `ConvaiActions`, `ConvaiCustomActions`, `ConvaiSimpleAnimationActions`,
  `ConvaiCharacterReference`, `ConvaiConversation`, `ConvaiDynamicContext`, `ConvaiExpressiveness`,
  `ConvaiFaceAndAnimation`, `ConvaiGazeAttention`, `ConvaiMetahumanSetup`, `ConvaiNarrativeDesign`,
  `ConvaiPlayerAndInput`, `ConvaiRestAndAudioUtilities`, `ConvaiSceneObjects`, `ConvaiVision`).
  This is the in-editor knowledge base an AI coding agent reads through the Convai Toolset / MCP
  integration. The CI packaging workflow ships `Content/Skills/` only in packages for engine
  versions that support the toolset (`.github/workflows/main.yml`); packages for older engines
  do not contain it — do not document it as universally present.
- Localization font assets under `Widgets/Fonts/` — Arabic (`KFGQPC_Uthman_Taha_Naskh_Regular`),
  CJK (`SourceHanSans`), Hindi (`Mangal_Regular`), default (`ConvaiFont`). These support the
  multilingual chat widget (`Chat_WB`).

When documenting features or tutorials that reference these assets, use the exact names listed here.
Do not invent asset names; verify against the plugin `Content/` folder.
