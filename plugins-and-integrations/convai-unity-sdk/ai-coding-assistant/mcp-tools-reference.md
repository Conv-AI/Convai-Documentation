---
title: MCP tools reference
description: Reference for every Convai MCP tool exposed to a coding agent, including default enablement and scene-mutation behavior.
last_reviewed: "4.5.0"
---

Unity's official MCP server exposes 37 Convai-specific tools under the `Convai.*` namespace, at tool contract version 4, so a connected coding agent can inspect, configure, or diagnose Convai components instead of you wiring them by hand in the Unity Editor. Unity AI Assistant calls a tool by its dot-separated name (for example `Convai.GetGuidance`); external MCP clients receive the same tool under an underscore-normalized name (`Convai_GetGuidance`). Most of the growth since `4.4.0` is the embodiment module wave — Gaze, Body Animation, Body Language, and Emotion each shipped with its own Configure, Diagnose, and content-inspection tools, tied together by three Embodiment-core tools. This page documents every tool's purpose, parameters, default enabled state, and scene or project mutation behavior, using the dot-separated name throughout.

## All 37 tools

| Tool | Area | Enabled by default | Mutates |
|---|---|---|---|
| `Convai.GetGuidance` | Guidance | Yes | No |
| `Convai.GetProjectStatus` | Foundation | Yes | No |
| `Convai.InspectScene` | Foundation | Yes | No |
| `Convai.ValidateSetup` | Foundation | Yes | No |
| `Convai.BootstrapScene` | Scene and conversation setup | No | Yes — Edit Mode only; `dryRun` defaults differently by caller (see below) |
| `Convai.ConfigureRoom` | Scene and conversation setup | Yes | Yes — Edit Mode only; `dryRun` defaults to `true` |
| `Convai.ConfigurePlayer` | Scene and conversation setup | Yes | Yes — Edit Mode only; `dryRun` defaults to `true` |
| `Convai.ConfigureCharacter` | Scene and conversation setup | Yes | Yes — Edit Mode only; `dryRun` defaults to `true` |
| `Convai.SetupConversationScene` | Scene and conversation setup | Yes | Yes — Edit Mode only; `dryRun` defaults to `true` |
| `Convai.DiagnoseConversation` | Scene and conversation setup | Yes | No |
| `Convai.ConfigureActions` | Character actions | Yes | Yes — Edit Mode only |
| `Convai.DiagnoseActions` | Character actions | Yes | No |
| `Convai.SimulateAction` | Character actions | Yes | Play Mode only, through the dispatcher |
| `Convai.ConfigureLipSync` | Lip sync | Yes | Yes — Edit Mode only; `dryRun` defaults to `true` |
| `Convai.DiagnoseLipSync` | Lip sync | Yes | No |
| `Convai.ConfigureTranscripts` | Transcripts | Yes | Yes — Edit Mode only; `dryRun` defaults to `true` |
| `Convai.DiagnoseTranscripts` | Transcripts | Yes | No |
| `Convai.ConfigureNarrative` | Narrative | Yes | Yes — Edit Mode only; `dryRun` defaults to `true` |
| `Convai.DiagnoseNarrative` | Narrative | Yes | No |
| `Convai.TraceRuntimeEvents` | Runtime diagnostics | Yes | No — manages an editor-only trace buffer only |
| `Convai.ConfigureEmbodiment` | Embodiment | Yes | Yes — Edit Mode only; `dryRun` defaults to `true` |
| `Convai.DiagnoseEmbodiment` | Embodiment | Yes | No |
| `Convai.InspectEmbodimentPresets` | Embodiment | Yes | No |
| `Convai.ConfigureGaze` | Gaze | Yes | Yes — Edit Mode only; `dryRun` defaults to `true` |
| `Convai.DiagnoseGaze` | Gaze | Yes | No |
| `Convai.MarkGazeTarget` | Gaze | Yes | Yes — Edit Mode only; `dryRun` defaults to `true` |
| `Convai.ConfigureBodyAnimation` | Body animation | Yes | Yes — Edit Mode only; `dryRun` defaults to `true` |
| `Convai.DiagnoseBodyAnimation` | Body animation | Yes | No |
| `Convai.InspectBodyAnimationContent` | Body animation | Yes | No |
| `Convai.TuneBodyAnimationPersonality` | Body animation | Yes | Yes — Edit Mode only; also duplicates a shared config asset, gated behind `makeConfigUnique` |
| `Convai.ConfigureBodyLanguage` | Body language | Yes | Yes — Edit Mode only; `dryRun` defaults to `true` |
| `Convai.DiagnoseBodyLanguage` | Body language | Yes | No |
| `Convai.InspectBodyLanguagePersonalities` | Body language | Yes | No |
| `Convai.ConfigureEmotion` | Emotion | Yes | Yes — Edit Mode only; `dryRun` defaults to `true` |
| `Convai.DiagnoseEmotion` | Emotion | Yes | No |
| `Convai.InspectEmotionPersonalities` | Emotion | Yes | No |
| `Convai.TuneEmotionPersonality` | Emotion | Yes | Yes — Edit Mode only; also duplicates a shared personality asset, gated behind `makePersonalityUnique` |

Toggle any tool under **Edit > Project Settings > AI > Unity MCP Server**.

## Guidance

### `Convai.GetGuidance`

**Area:** Guidance · **Enabled by default:** Yes · **Mutates:** No

Loads concise Convai SDK workflow guidance for one topic. Call it before configuring or debugging a Convai feature; it is not for generic Unity operations. The response includes a summary, prerequisites, an ordered workflow, the relevant Convai and Unity tools, and documentation paths.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `topic` | `enum ConvaiGuidanceTopic` | `Overview` | Workflow topic to load. |

`ConvaiGuidanceTopic` values and what each returns:

| Topic | Summary returned |
|---|---|
| `Overview` (default) | Use Convai tools only for SDK-aware operations; compose official Unity MCP tools for generic project changes. |
| `Setup` | Complete runnable Convai scene setup proactively; an explicit setup request authorizes safe, reversible defaults. |
| `Actions` | Author explicit action affordances and bind local executors; never infer affordances from scene metadata. |
| `DynamicContext` | Send state, events, and attention-object changes through the character dynamic-context facade. |
| `Vision` | Configure a vision publisher and one frame source under the room hierarchy before enabling video mode. |
| `Narrative` | Use the Narrative module for section state and named or inline trigger workflows. |
| `Embodiment` | Configure each embodiment module through its own branded Configure/Diagnose pair, starting from `Convai.DiagnoseEmbodiment`; every feature degrades gracefully when a peer is absent. |
| `Gaze` | Add the Gaze component and see eye contact working; the Player Anchor and the watches block explain what a character treats as the player. |
| `BodyAnimation` | Body animation is content-gated — several behaviours stay inert until the character's animation set carries clips for them, which is a content gap, not a setup fault. |
| `BodyLanguage` | Body Language layers ambient nonverbal motion on top of Body Animation and Gaze, ducking itself automatically when either module is present. |
| `Emotion` | Give a character a face that reacts to what is said, and tune its temperament without restyling every other character sharing its personality. |
| `Events` | Prefer `ConvaiManager.Events` for typed code and relay components for Inspector-driven `UnityEvent`s. |
| `Runtime` | Use `ConvaiManager` for session ownership, Audio for room audio, and Transcripts for canonical history. |

## Foundation

### `Convai.GetProjectStatus`

**Area:** Foundation · **Enabled by default:** Yes · **Mutates:** No

Reads Convai SDK, Unity AI Assistant, and non-secret project configuration status. Never returns the Convai API key.

No input parameters.

Returns `sdkVersion`, `unityVersion`, `assistantVersion`, `toolContractVersion`, `credentialsConfigured`, `serverUrl`, `transcriptSystemEnabled`, `notificationSystemEnabled`, `backgroundPolicy`, `defaultMicrophoneDeviceId`, `connectionTimeoutSeconds`, `isPlaying`, `isCompiling`, and `packageRoot`.

### `Convai.InspectScene`

**Area:** Foundation · **Enabled by default:** Yes · **Mutates:** No

Inspects open scenes for `ConvaiManager`, `ConvaiRoomManager`, `ConvaiPlayer`, and `ConvaiCharacter` components and returns exact instance IDs for later mutations.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `includeInactive` | `bool` | `true` | Include disabled `GameObject`s and components in the inspection. |

### `Convai.ValidateSetup`

**Area:** Foundation · **Enabled by default:** Yes · **Mutates:** No

Validates Convai project and scene readiness without changing assets or scenes. Call before and after Convai authoring operations. Returns `errors`, `warnings`, and `nextSteps`, folding in every embodiment module's own findings for every `ConvaiCharacter` in the active scene.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `scope` | `enum ConvaiValidationScope` | `All` | Validation scope: `All`, `Project`, or `Scene`. |

## Scene and conversation setup

### `Convai.BootstrapScene`

**Area:** Scene and conversation setup · **Enabled by default:** No · **Mutates:** Yes

Idempotently adds the required `ConvaiManager` and `ConvaiRoomManager` to the active scene. Does not add players, characters, save the scene, or set credentials. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `dryRun` | `bool` | `true` via Unity AI Assistant; `false` via the external MCP tool contract | Preview required changes without modifying the scene. |

{% hint style="warning" %}
`Convai.BootstrapScene` is the only one of the 37 tools disabled by default. Its `dryRun` default also depends on how the agent calls it: Unity AI Assistant's dot-named wrapper defaults `dryRun` to `true` like every other mutating tool, but the underlying MCP tool contract used by external MCP clients (the underscore-named `Convai_BootstrapScene`) defaults `dryRun` to `false` — those clients apply the change immediately unless they pass `dryRun: true` explicitly. Prefer `Convai.SetupConversationScene` for end-to-end setup; use `Convai.BootstrapScene` only for manager/room-only work.
{% endhint %}

### `Convai.ConfigureRoom`

**Area:** Scene and conversation setup · **Enabled by default:** Yes · **Mutates:** Yes

Previews or configures a Convai room — `ConvaiManager` and `ConvaiRoomManager` — on an explicit target `GameObject`, using inline settings or an existing `ConvaiRoomManagerProfile`. Uses Unity's Undo system, never saves the scene, and never changes credentials. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `targetInstanceId` | `long` | — (required) | GameObject instance ID that owns or will own `ConvaiManager` and `ConvaiRoomManager`. |
| `configurationMode` | `enum ConvaiToolConfigurationMode` | `Inline` | `Inline` or `ExistingProfile`. |
| `profileAssetPath` | `string` | `""` | Existing `ConvaiRoomManagerProfile` asset path. Required in `ExistingProfile` mode. |
| `connectionType` | `enum ConvaiConnectionType` | `Audio` | Inline connection type. |
| `inputMode` | `enum ConversationInputMode` | `HandsFree` | Inline conversation input mode. |
| `connectOnStart` | `bool` | `true` | Connect automatically when the scene starts. |
| `serverEndpoint` | `enum ConvaiServerEndpoint` | `Connect` | Core-service endpoint. |
| `visionMode` | `enum ConvaiVisionContextMode` | `Auto` | Dynamic vision policy. |
| `pushToTalkKey` | `string` | `"T"` | Unity `KeyCode` name used by push-to-talk. |
| `dryRun` | `bool` | `true` | Preview changes without modifying the scene. |

### `Convai.ConfigurePlayer`

**Area:** Scene and conversation setup · **Enabled by default:** Yes · **Mutates:** Yes

Previews or adds and configures `ConvaiPlayer` on an explicit target `GameObject`, then binds one unambiguous manager. Never modifies `Main Camera`. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `targetInstanceId` | `long` | — (required) | Target player GameObject instance ID. |
| `managerInstanceId` | `long` | `0` | Optional manager GameObject instance ID. Zero auto-resolves one manager in the target scene. |
| `playerName` | `string` | `"Player"` | Player display name. |
| `playerId` | `string` | `""` | Optional local transcript attribution ID. Defaults to the player name. |
| `dryRun` | `bool` | `true` | Preview changes without modifying the scene. |

### `Convai.ConfigureCharacter`

**Area:** Scene and conversation setup · **Enabled by default:** Yes · **Mutates:** Yes

Previews or adds and configures `ConvaiCharacter` with recommended audio output — `AudioSource` and `ConvaiAudioOutput` — on an explicit target `GameObject`. A missing Character ID stays an explicit readiness blocker: the tool returns `complete=false` and `requiredInputs=["characterId"]` instead of guessing one. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `targetInstanceId` | `long` | — (required) | Target character GameObject instance ID. |
| `managerInstanceId` | `long` | `0` | Optional manager GameObject instance ID. Zero auto-resolves one manager in the target scene. |
| `configurationMode` | `enum ConvaiToolConfigurationMode` | `Inline` | `Inline` or `ExistingProfile`. |
| `profileAssetPath` | `string` | `""` | Existing `ConvaiCharacterProfile` asset path. Required in `ExistingProfile` mode. |
| `characterId` | `string` | `""` | Convai dashboard Character ID. May be omitted while authoring an incomplete placeholder. |
| `characterName` | `string` | `""` | Character display name. Defaults to the target GameObject name. |
| `addAudioOutput` | `bool` | `true` | Ensure `AudioSource` and `ConvaiAudioOutput` companions. |
| `dryRun` | `bool` | `true` | Preview changes without modifying the scene. |

### `Convai.SetupConversationScene`

**Area:** Scene and conversation setup · **Enabled by default:** Yes · **Mutates:** Yes

Previews or performs end-to-end Audio conversation setup in the active scene, using safe placeholders and recommended defaults. Selection order is an explicit instance ID, then one unambiguous existing component, then a safe placeholder — a standalone `Convai Player` and a visible Capsule `Convai Character` — when none exists. Never saves the scene, enters Play Mode, or sets credentials. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `managerInstanceId` | `long` | `0` | Optional manager target instance ID. |
| `playerInstanceId` | `long` | `0` | Optional player target instance ID. |
| `characterInstanceId` | `long` | `0` | Optional character target instance ID. |
| `roomProfileAssetPath` | `string` | `""` | Optional existing `ConvaiRoomManagerProfile` path. |
| `characterProfileAssetPath` | `string` | `""` | Optional existing `ConvaiCharacterProfile` path. |
| `characterId` | `string` | `""` | Convai dashboard Character ID. May be omitted until all independent setup is complete. |
| `characterName` | `string` | `"Convai Character"` | Character display name. |
| `playerName` | `string` | `"Player"` | Player display name. |
| `playerId` | `string` | `""` | Optional local transcript attribution ID. |
| `inputMode` | `enum ConversationInputMode` | `HandsFree` | Recommended room input mode. |
| `connectOnStart` | `bool` | `true` | Connect automatically when the scene starts. |
| `createPlaceholders` | `bool` | `true` | Create standalone player and Capsule character placeholders when none exist. |
| `dryRun` | `bool` | `true` | Preview changes without modifying the scene. |

### `Convai.DiagnoseConversation`

**Area:** Scene and conversation setup · **Enabled by default:** Yes · **Mutates:** No

Diagnoses active-scene Convai conversation readiness and runtime state with ranked evidence and suggested fixes. Works in both Edit Mode and Play Mode. Never mutates the project or returns API keys.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | `0` | Optional focused character GameObject instance ID. |
| `includeInactive` | `bool` | `true` | Include inactive scene objects. |

Returns `readyToRun`, configuration and runtime snapshots, and an `issues` array with stable codes, evidence, `autoFixable`, and `suggestedTool`/`suggestedArguments` for each issue.

## Character actions

### `Convai.ConfigureActions`

**Area:** Character actions · **Enabled by default:** Yes · **Mutates:** Yes

Previews or safely upserts typed action definitions and explicit object or character targets on a Convai character. Uses Undo and never saves. A definition with no bound executor receives an unwired `UnityEvent` placeholder and stays incomplete until wired. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | — (required) | Character GameObject or component instance ID. |
| `definitions` | `array` | `[]` | Typed action definitions to upsert by name. See [Character actions scripting reference](../features/character-actions/actions-scripting-reference.md) for the full field set. |
| `objects` | `array` | `[]` | Explicit actionable GameObjects to upsert by name. |
| `characters` | `array` | `[]` | Explicit actionable characters to upsert by name. |
| `initialAttentionObject` | `string` | `""` | Optional authored object name used as initial attention. |
| `dryRun` | `bool` | `true` | Preview changes without modifying the scene. |

### `Convai.DiagnoseActions`

**Area:** Character actions · **Enabled by default:** Yes · **Mutates:** No

Diagnoses action definitions, executors, targets, attention, dispatcher presence, and runtime availability without mutation.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | `0` | Optional character instance ID. |
| `includeInactive` | `bool` | `true` | Include inactive objects. |

### `Convai.SimulateAction`

**Area:** Character actions · **Enabled by default:** Yes · **Mutates:** Play Mode only

Validates an action payload in Edit Mode, or dispatches it through the real runtime `ConvaiActionDispatcher` in Play Mode. Never changes Play Mode itself.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | — (required) | Character instance ID. |
| `actionName` | `string` | — (required) | Configured action name. |
| `target` | `string` | `""` | Optional target name. |
| `parameters` | `dictionary<string, string>` | `{}` | Optional action parameter values keyed by authored parameter name. |
| `timeoutSeconds` | `float` | `10` | Completion timeout, clamped between `0.1` and `60` seconds. |

In Edit Mode the tool returns `executed=false` and `requiresPlayMode=true` after validating the payload. In Play Mode it enqueues the command on the character's dispatcher and waits for a `ConvaiActionStepReport`, returning `SIMULATION_TIMEOUT` if the step does not complete within `timeoutSeconds`.

## Lip sync

### `Convai.ConfigureLipSync`

**Area:** Lip sync · **Enabled by default:** Yes · **Mutates:** Yes

Previews or configures Convai lip sync using existing meshes, shipped profiles, and an optional existing lip sync map asset. Never creates or mutates assets. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | — (required) | Character GameObject instance ID. |
| `meshInstanceIds` | `long[]` | `[]` | Target mesh instance IDs. Empty resolves every `SkinnedMeshRenderer` under the character. |
| `profile` | `string` | `"Auto"` | `Auto`, `arkit`, `cc4_extended`, or `metahuman`. `Auto` requires a unique blendshape-name match across the target meshes. |
| `mappingAssetPath` | `string` | `""` | Existing `ConvaiLipSyncMapAsset` path. |
| `latencyMode` | `enum LipSyncLatencyMode` | `Balanced` | `Balanced`, `UltraLowLatency`, `NetworkSafe`, or `Custom`. |
| `dryRun` | `bool` | `true` | Preview changes without modifying the scene. |

See [Add lip sync](../getting-started/add-lip-sync/README.md) for the Inspector workflow this tool automates.

### `Convai.DiagnoseLipSync`

**Area:** Lip sync · **Enabled by default:** Yes · **Mutates:** No

Diagnoses the `ConvaiLipSyncComponent`, target meshes, blendshape compatibility, mapping, profile, and sanitized runtime buffer state.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | `0` | Character GameObject instance ID. |
| `includeRuntimeMetrics` | `bool` | `true` | Include `isPlaying`, `isTalking`, `isFadingOut`, `engineState`, buffered and stream duration, and headroom. |

## Transcripts

### `Convai.ConfigureTranscripts`

**Area:** Transcripts · **Enabled by default:** Yes · **Mutates:** Yes

Previews or configures the canonical transcript facade, event relay, or shipped chat UI. Never changes `ConvaiSettings` or exposes transcript text. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `managerInstanceId` | `long` | `0` | Optional manager instance ID. |
| `hostInstanceId` | `long` | `0` | Optional host GameObject instance ID. |
| `mode` | `enum ConvaiTranscriptToolMode` | `EventRelay` | `EventRelay`, `ChatUI`, or `WorldSpaceChatUI`. |
| `finalOnly` | `bool` | `false` | Forward final updates only. |
| `ignoreInterim` | `bool` | `true` | Ignore interim updates. |
| `characterIdFilter` | `string` | `""` | Optional character ID filter. |
| `dryRun` | `bool` | `true` | Preview changes without modifying the scene. |

See [Transcript API](../scripting-reference/transcript-api.md) for the runtime facade this tool wires up.

### `Convai.DiagnoseTranscripts`

**Area:** Transcripts · **Enabled by default:** Yes · **Mutates:** No

Diagnoses transcript enablement, facade readiness, relays, UIs, and sanitized runtime timeline metadata.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `managerInstanceId` | `long` | `0` | Optional manager instance ID. |
| `includeText` | `bool` | `false` | Include transcript text only when explicitly requested. |

## Narrative

### `Convai.ConfigureNarrative`

**Area:** Narrative · **Enabled by default:** Yes · **Mutates:** Yes

Previews or configures Unity-side narrative section mappings, template keys, and triggers — `ConvaiNarrativeDesignManager` and `ConvaiNarrativeDesignTrigger`. Preserves unrelated entries and `UnityEvent`s and never contacts Convai. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | — (required) | Character GameObject instance ID. |
| `managerHostInstanceId` | `long` | `0` | Optional host GameObject instance ID for the narrative manager. |
| `sections` | `array` | `[]` | Narrative sections to upsert, each `{ sectionId, sectionName }`. |
| `templateKeys` | `array` | `[]` | Template keys to upsert, each `{ key, value }`. |
| `triggers` | `array` | `[]` | Triggers to upsert. See [Narrative design scripting reference](../features/narrative-design/scripting-narrative-design.md) for the full trigger field set. |
| `dryRun` | `bool` | `true` | Preview changes without modifying the scene. |

### `Convai.DiagnoseNarrative`

**Area:** Narrative · **Enabled by default:** Yes · **Mutates:** No

Diagnoses Unity-side narrative character bindings, duplicate or orphaned sections, template keys, triggers, player filters, cached sync errors, and runtime trigger state.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | `0` | Character GameObject instance ID. |
| `includeInactive` | `bool` | `true` | Include inactive objects. |
| `includeContent` | `bool` | `false` | Include template values and trigger names. Content stays hidden by default. |

## Runtime diagnostics

### `Convai.TraceRuntimeEvents`

**Area:** Runtime diagnostics · **Enabled by default:** Yes · **Mutates:** No (manages an editor-only trace buffer only)

Starts, reads, clears, or stops a bounded editor-only Convai runtime event trace of up to 256 entries. The trace clears on Play Mode exit and domain reload. Transcript capture is off by default.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `operation` | `enum ConvaiRuntimeTraceOperation` | `Read` | `Start`, `Read`, `Clear`, or `Stop`. |
| `managerInstanceId` | `long` | `0` | Optional active-scene manager instance ID. |
| `characterInstanceId` | `long` | `0` | Optional active-scene character instance ID filter. |
| `eventFilters` | `string[]` | `[]` | Optional event type or category filters. |
| `limit` | `int` | `100` | Entries to return, clamped between `1` and `256`. |
| `captureTranscripts` | `bool` | `false` | Capture transcript events and text. Off by default. |

## Embodiment

The Embodiment tools set up the composition root every expressive module plugs into — `EmbodimentContext` and `StandardRigBinding` — and hand off to the per-module tools below. `Convai.DiagnoseEmbodiment` is the tool to call first on any character: it reports the rig, every module the character has, which will actually do something, and names the per-module tool to call next.

### `Convai.ConfigureEmbodiment`

**Area:** Embodiment · **Enabled by default:** Yes · **Mutates:** Yes

Sets a Convai character up: works out its rig now instead of at runtime, adds the expressive modules named — whichever of Gaze, Emotion, Body Animation, Body Language, and Conversation Flow this project has installed — and assigns an Embodiment Preset the project already has. Never creates or edits an asset, and never tunes an individual module; each module has its own Configure tool for that. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | — (required) | The Convai Character to set up. `0` uses the only one in the active scene. |
| `setUpRig` | `bool` | `true` | Add the Character Rig component and work out the character's bones and face meshes now. |
| `capabilities` | `string[]` | `[]` | Which expressive modules to add, by display name or module ID. Modules already on the character are left alone. |
| `presetAssetPath` | `string` | `""` | Project path of an existing Embodiment Preset to assign. Never creates one. |
| `dryRun` | `bool` | `true` | Preview the changes without touching the scene. |

### `Convai.DiagnoseEmbodiment`

**Area:** Embodiment · **Enabled by default:** Yes · **Mutates:** No

Surveys one Convai character end to end: whether its rig is understood, which expressive modules it has, which will actually do something and which are blocked or inert and why, which settings assets they run on, its Embodiment Preset, and — in Play Mode — what it is doing right now.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | `0` | The Convai Character to diagnose. `0` uses the only one in the active scene. |
| `includeCapabilities` | `bool` | `true` | Include the per-module breakdown. |
| `includeRuntimeState` | `bool` | `true` | Include live conversation and emotion state. Play Mode only. |

### `Convai.InspectEmbodimentPresets`

**Area:** Embodiment · **Enabled by default:** Yes · **Mutates:** No

Lists the Embodiment Presets in the project and whether each is valid, plus every expressive module a preset can carry and the menu path that creates its settings asset. Never creates or edits an asset.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `folderPaths` | `string[]` | `[]` | Project folders to search. Omit to search the whole project. |

## Gaze

### `Convai.ConfigureGaze`

**Area:** Gaze · **Enabled by default:** Yes · **Mutates:** Yes

Adds `ConvaiGazeController` to a character and tunes how it makes eye contact — who it treats as the player, how strongly it commits, how it turns its body, and which optional extras it has. Assigns an existing Gaze Profile if the project has one; never creates or edits an asset. Omitted tuning fields are left unchanged. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | — (required) | The Convai Character to configure. `0` uses the only one in the active scene. |
| `eyeContactMode` | `enum GazeEyeContactMode` | omit = unchanged | `Natural`, `SpeakingFocus`, `ConversationLock`, or `AlwaysLock`. |
| `focusFidelity` | `enum GazeFocusFidelity` | omit = unchanged | `Social` or `Exact`. |
| `playerAnchorInstanceId` | `long` | omit = unchanged | The transform this character should treat as the player. |
| `clearPlayerAnchorOverride` | `bool` | omit = unchanged | Clear the override so the character watches the main camera again. |
| `playerAnchorAimMode` | `enum GazeAnchorAimMode` | omit = unchanged | `Auto`, `ExactTransform`, or `LocalOffset`. |
| `bodyTurnStyle` | `enum GazeBodyTurnStyle` | omit = unchanged | `SteppingTurn` or `SmoothRotation`. |
| `profileAssetPath` | `string` | `""` | Existing Gaze Profile to assign. Never creates one. |
| `capabilities` | `string[]` | omit = unchanged | The exact set of optional Gaze extras this character should end up with. |
| `dryRun` | `bool` | `true` | Preview the changes without touching the scene. |

### `Convai.DiagnoseGaze`

**Area:** Gaze · **Enabled by default:** Yes · **Mutates:** No

Explains why a character is or is not looking at the player: which head and eye bones resolved, whether the rig faces the right way, what it treats as the player and which setting decided that, which Gaze Profile is in use, which optional extras it has, and live gaze state in Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | `0` | The Convai Character to diagnose. `0` uses the only one in the active scene. |
| `includeRuntimeState` | `bool` | `true` | Include what the character is looking at right now. Play Mode only. |

### `Convai.MarkGazeTarget`

**Area:** Gaze · **Enabled by default:** Yes · **Mutates:** Yes

Marks scene objects as worth looking at, so Convai characters glance at them — a painting, a screen, a prop. Adds `ConvaiGazeTarget` to the objects named; never creates an asset. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `gameObjectInstanceIds` | `long[]` | — (required) | The GameObjects to mark as worth looking at. |
| `priority` | `int` | omit = default `5` | How important the object is. The player counts as priority `10`; above that a character looks here instead of the player. |
| `baseRelevance` | `float` | omit = unchanged | How interesting the object is up close, from `0` to `1`. |
| `maxDistance` | `float` | omit = unchanged | Metres beyond which characters stop noticing the object. |
| `fullRelevanceDistance` | `float` | omit = unchanged | Metres within which the object is at its most interesting. |
| `remove` | `bool` | `false` | Unmark these objects instead. |
| `dryRun` | `bool` | `true` | Preview the changes without touching the scene. |

## Body animation

### `Convai.ConfigureBodyAnimation`

**Area:** Body animation · **Enabled by default:** Yes · **Mutates:** Yes

Adds `ConvaiBodyAnimationController` to a character and sets it up — the shipped animation content, whether the character can walk, and how it moves. Assigns existing content assets; never creates, edits, or measures an asset, and never touches an Animator Controller. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | — (required) | The Convai Character to configure. `0` uses the only one in the active scene. |
| `includeMovement` | `bool` | `true` | Add `ConvaiNavMeshLocomotion` so the character can walk, jog, turn, and stop. |
| `profileAssetPath` | `string` | `""` | Existing Body Animation Profile, which bundles an Animation Set and a Config. Never creates one. |
| `animationSetAssetPath` | `string` | `""` | Existing Animation Set, for a character not using a profile. |
| `configAssetPath` | `string` | `""` | Existing Body Animation Config, for a character not using a profile. |
| `speedProfile` | `enum LocomotionSpeedProfile` | omit = unchanged | Whether a move walks or jogs. |
| `accelerationMetersPerSecondSquared` | `float` | omit = unchanged | How fast the character reaches its target speed. |
| `dryRun` | `bool` | `true` | Preview the changes without touching the scene. |

### `Convai.DiagnoseBodyAnimation`

**Area:** Body animation · **Enabled by default:** Yes · **Mutates:** No

Explains what a character's body animation is actually doing: whether it is set up, whether the rig can drive it, which animation content it resolved, which behaviours work and which are inert because the character has no clips for them, how the rig's scale is calibrated, and live state in Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | `0` | The Convai Character to diagnose. `0` uses the only one in the active scene. |
| `includeRuntimeState` | `bool` | `true` | Include what the character is animating right now. Play Mode only. |

### `Convai.InspectBodyAnimationContent`

**Area:** Body animation · **Enabled by default:** Yes · **Mutates:** No

Lists what a character's Animation Set can actually perform — the idle, talk, listen, and think pools, every action and gesture with the names `PlayAction` accepts, walking coverage, and pointing directions. Call this before writing code that uses `PlayAction`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | `0` | The Convai Character whose animation content to list. Ignored when `animationSetAssetPath` is given. |
| `animationSetAssetPath` | `string` | `""` | An Animation Set to inspect directly, with no character involved. |

### `Convai.TuneBodyAnimationPersonality`

**Area:** Body animation · **Enabled by default:** Yes · **Mutates:** Yes

Tunes how expressive and how calm a character is, and whether it keeps busy when alone. A Body Animation Config can be shared by many characters, so this tool makes a private copy for the named character before changing anything — the same **Give This Character Its Own Settings** command the Inspector offers — rather than editing a config that other characters or the SDK's shipped defaults still rely on. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | — (required) | The Convai Character to tune. `0` uses the only one in the active scene. |
| `archetype` | `enum BodyAnimationArchetype` | omit = unchanged | A named personality preset: `Composed`, `Warm`, `Energetic`, or `Reserved`. |
| `howExpressive` | `float` | omit = unchanged | How large and frequent talking gestures are, from `0` to `2`. |
| `howCalm` | `float` | omit = unchanged | How long the character holds a pose and how gently it settles, from `0` to `2`. |
| `keepsBusyWhenAlone` | `bool` | omit = unchanged | Whether the character performs small activities on its own during silence. |
| `makeConfigUnique` | `bool` | `false` | Consent to copying the config when it is shared by more than one character or ships with the SDK. Required before applying; a preview always reports whether it will be needed. |
| `dryRun` | `bool` | `true` | Preview the change, and whether a copy is needed, without writing anything. |

{% hint style="info" %}
`Convai.TuneBodyAnimationPersonality` and `Convai.TuneEmotionPersonality` are the only two tools in this catalog that write to disk. Both duplicate a shared or SDK-shipped settings asset for one character rather than editing it in place, and both refuse to apply without explicit `makeConfigUnique`/`makePersonalityUnique` consent once a preview shows a copy is required.
{% endhint %}

## Body language

### `Convai.ConfigureBodyLanguage`

**Area:** Body language · **Enabled by default:** Yes · **Mutates:** Yes

Adds `ConvaiBodyLanguageController` to a character so it breathes, shifts its weight, sways, and gestures as it talks, and gives it a personality by assigning a Body Language Profile the project already has. Never creates or edits an asset, and refuses a character whose rig cannot drive the module rather than adding something inert. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | — (required) | The Convai Character to configure. `0` uses the only one in the active scene. |
| `personalityAssetPath` | `string` | `""` | Existing Body Language Profile to assign. Never creates one. Omit to leave the personality unchanged. |
| `assignDefaultPersonality` | `bool` | `false` | Give a character with no personality the shipped one, or the first the project has. Leaves an existing personality alone. |
| `dryRun` | `bool` | `true` | Preview the changes without touching the scene. |

### `Convai.DiagnoseBodyLanguage`

**Area:** Body language · **Enabled by default:** Yes · **Mutates:** No

Explains what a character's body is doing and why: what its rig offers, which personality tunes it and which behaviours that personality switches off, which other Convai modules share its body and what each one changes, and — in Play Mode — its live posture, breathing, weight shifts, and gesture suppression.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | `0` | The Convai Character to diagnose. `0` uses the only one in the active scene. |
| `includeRuntimeState` | `bool` | `true` | Include live posture and gesture state. Play Mode only. |

### `Convai.InspectBodyLanguagePersonalities`

**Area:** Body language · **Enabled by default:** Yes · **Mutates:** No

Lists the Body Language Profiles in the project — each one's expressiveness, which behaviours it switches off, and which characters in the open scenes already use it.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `folderPaths` | `string[]` | `[]` | Project folders to search. Omit to search the whole project. |

## Emotion

### `Convai.ConfigureEmotion`

**Area:** Emotion · **Enabled by default:** Yes · **Mutates:** Yes

Adds `ConvaiEmotionController` to a character so its face reacts to what is said, gives it a personality the project already has, and sets how it detects feelings and what it rests at. Only ever writes fields on the character itself — it never creates or edits a personality asset, so it can never restyle other characters by accident. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | — (required) | The Convai Character to configure. `0` uses the only one in the active scene. |
| `personalityAssetPath` | `string` | `""` | Existing `ConvaiEmotionProfile` to assign. Never creates one. |
| `emotionDetection` | `string` | `""` (unchanged) | The character's own emotion-detection setting. |
| `restingMood` | `string` | `""` (unchanged) | This character's own resting-mood override. |
| `restingMoodStrength` | `float` | omit = unchanged | Strength of the resting-mood override. |
| `dryRun` | `bool` | `true` | Preview the changes without touching the scene. |

### `Convai.DiagnoseEmotion`

**Area:** Emotion · **Enabled by default:** Yes · **Mutates:** No

Explains what a Convai character's face will actually do and why: whether it can show emotions at all, how it detects them, which personality tunes it, what it rests at and which setting decided that, and which of its behaviours are switched off or quietly gated by another setting.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | `0` | The Convai Character to diagnose. `0` uses the only one in the active scene. |
| `includeRuntimeState` | `bool` | `true` | Include the live dominant emotion and mood. Play Mode only. |

### `Convai.InspectEmotionPersonalities`

**Area:** Emotion · **Enabled by default:** Yes · **Mutates:** No

Lists the Convai emotion personalities in the project — which character type each one is, what it rests at, which behaviours are on, whether it ships with the SDK, and which characters already use it.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `folderPaths` | `string[]` | `[]` | Project folders to search. Omit to search the whole project. |

### `Convai.TuneEmotionPersonality`

**Area:** Emotion · **Enabled by default:** Yes · **Mutates:** Yes

Changes how a character feels — its character type, what it rests at, how strongly and quickly it shows things, and its feel switches. These live on a personality asset other characters may share, so this tool previews first and, on explicit consent, gives the character its own copy and writes only that. It never edits a shared or SDK-shipped personality in place. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | — (required) | The Convai Character to tune. `0` uses the only one in the active scene. |
| `characterType` | `string` | `""` (unchanged) | A named personality preset for the character type. |
| `restingMood` | `string` | `""` (unchanged) | The personality's own resting mood. |
| `howStronglyItShows` | `float` | omit = unchanged | How strongly emotions show on the face. |
| `howQuicklyItReacts` | `float` | omit = unchanged | How quickly the face reacts to a change in feeling. |
| `neverSitsPerfectlyStill` | `bool` | omit = unchanged | Whether conversation-beat micro-reactions play. |
| `picksUpOtherCharactersMoods` | `bool` | omit = unchanged | Whether this character's mood is influenced by other characters' moods. Has no visible effect in a scene with one character. |
| `makePersonalityUnique` | `bool` | `false` | Consent to copying the personality when it is shared by more than one character or ships with the SDK. Required before applying. |
| `dryRun` | `bool` | `true` | Preview the change, and whether a copy is needed, without writing anything. |

## Next steps

{% content-ref url="README.md" %}
[AI coding assistant](README.md)
{% endcontent-ref %}

{% content-ref url="supported-coding-agents.md" %}
[Supported coding agents](supported-coding-agents.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot the AI coding assistant](troubleshooting.md)
{% endcontent-ref %}
