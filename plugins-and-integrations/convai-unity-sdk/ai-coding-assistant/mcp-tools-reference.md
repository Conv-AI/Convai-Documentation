---
title: MCP tools reference
description: Reference for every Convai MCP tool exposed to a coding agent, including default enablement and scene-mutation behavior.
last_reviewed: "4.4.0"
---

Unity's official MCP server exposes 20 Convai-specific tools under the `Convai.*` namespace, at tool contract version 4, so a connected coding agent can inspect, configure, or diagnose Convai components instead of you wiring them by hand in the Unity Editor. Unity AI Assistant calls a tool by its dot-separated name (for example `Convai.GetGuidance`); external MCP clients receive the same tool under an underscore-normalized name (`Convai_GetGuidance`). This page documents every tool's purpose, parameters, default enabled state, and scene or project mutation behavior, using the dot-separated name throughout.

## All 20 tools

| Tool | Area | Enabled by default | Mutates |
|---|---|---|---|
| `Convai.GetGuidance` | Guidance | Yes | No |
| `Convai.GetProjectStatus` | Foundation | Yes | No |
| `Convai.InspectScene` | Foundation | Yes | No |
| `Convai.ValidateSetup` | Foundation | Yes | No |
| `Convai.BootstrapScene` | Scene and conversation setup | No | Yes — `dryRun` defaults to `false` |
| `Convai.ConfigureRoom` | Scene and conversation setup | Yes | Yes — `dryRun` defaults to `true` |
| `Convai.ConfigurePlayer` | Scene and conversation setup | Yes | Yes — `dryRun` defaults to `true` |
| `Convai.ConfigureCharacter` | Scene and conversation setup | Yes | Yes — `dryRun` defaults to `true` |
| `Convai.SetupConversationScene` | Scene and conversation setup | Yes | Yes — `dryRun` defaults to `true` |
| `Convai.DiagnoseConversation` | Scene and conversation setup | Yes | No |
| `Convai.ConfigureActions` | Character actions | Yes | Yes — `dryRun` defaults to `true` |
| `Convai.DiagnoseActions` | Character actions | Yes | No |
| `Convai.SimulateAction` | Character actions | Yes | Play Mode only, through the dispatcher |
| `Convai.ConfigureLipSync` | Lip sync | Yes | Yes — `dryRun` defaults to `true` |
| `Convai.DiagnoseLipSync` | Lip sync | Yes | No |
| `Convai.ConfigureTranscripts` | Transcripts | Yes | Yes — `dryRun` defaults to `true` |
| `Convai.DiagnoseTranscripts` | Transcripts | Yes | No |
| `Convai.ConfigureNarrative` | Narrative | Yes | Yes — `dryRun` defaults to `true` |
| `Convai.DiagnoseNarrative` | Narrative | Yes | No |
| `Convai.TraceRuntimeEvents` | Runtime diagnostics | Yes | No — manages an editor-only trace buffer only |

Toggle any tool under **Project Settings > AI > Unity MCP Server**.

## `Convai.GetGuidance`

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
| `Embodiment` | Configure each embodiment module through its branded component and profile; missing peers must degrade gracefully. |
| `Events` | Prefer `ConvaiManager.Events` for typed code and relay components for Inspector-driven `UnityEvent`s. |
| `Runtime` | Use `ConvaiManager` for session ownership, Audio for room audio, and Transcripts for canonical history. |

## `Convai.GetProjectStatus`

**Area:** Foundation · **Enabled by default:** Yes · **Mutates:** No

Reads Convai SDK, Unity AI Assistant, and non-secret project configuration status. Never returns the Convai API key.

No input parameters.

Returns `sdkVersion`, `unityVersion`, `assistantVersion`, `toolContractVersion`, `credentialsConfigured`, `serverUrl`, `transcriptSystemEnabled`, `notificationSystemEnabled`, `defaultMicrophoneDeviceId`, `connectionTimeoutSeconds`, `isPlaying`, `isCompiling`, and `packageRoot`.

## `Convai.InspectScene`

**Area:** Foundation · **Enabled by default:** Yes · **Mutates:** No

Inspects open scenes for `ConvaiManager`, `ConvaiRoomManager`, `ConvaiPlayer`, and `ConvaiCharacter` components and returns exact instance IDs for later mutations.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `includeInactive` | `bool` | `true` | Include disabled `GameObject`s and components in the inspection. |

## `Convai.ValidateSetup`

**Area:** Foundation · **Enabled by default:** Yes · **Mutates:** No

Validates Convai project and scene readiness without changing assets or scenes. Call before and after Convai authoring operations. Returns `errors`, `warnings`, and `nextSteps`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `scope` | `enum ConvaiValidationScope` | `All` | Validation scope: `All`, `Project`, or `Scene`. |

## `Convai.BootstrapScene`

**Area:** Scene and conversation setup · **Enabled by default:** No · **Mutates:** Yes

Idempotently adds the required `ConvaiManager` and `ConvaiRoomManager` to the active scene. Does not add players, characters, save the scene, or set credentials. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `dryRun` | `bool` | `false` | Preview required changes without modifying the scene. |

{% hint style="warning" %}
`Convai.BootstrapScene` is the only one of the 20 tools disabled by default, and the only mutating tool whose `dryRun` parameter defaults to `false`. Calling it with no arguments applies the change immediately instead of previewing it. Prefer `Convai.SetupConversationScene` for end-to-end setup; use `Convai.BootstrapScene` only for manager/room-only work.
{% endhint %}

## `Convai.ConfigureRoom`

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

## `Convai.ConfigurePlayer`

**Area:** Scene and conversation setup · **Enabled by default:** Yes · **Mutates:** Yes

Previews or adds and configures `ConvaiPlayer` on an explicit target `GameObject`, then binds one unambiguous manager. Never modifies `Main Camera`. Available only in Edit Mode — returns a `PLAY_MODE_ACTIVE` failure code if called during Play Mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `targetInstanceId` | `long` | — (required) | Target player GameObject instance ID. |
| `managerInstanceId` | `long` | `0` | Optional manager GameObject instance ID. Zero auto-resolves one manager in the target scene. |
| `playerName` | `string` | `"Player"` | Player display name. |
| `playerId` | `string` | `""` | Optional local transcript attribution ID. Defaults to the player name. |
| `dryRun` | `bool` | `true` | Preview changes without modifying the scene. |

## `Convai.ConfigureCharacter`

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

## `Convai.SetupConversationScene`

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

## `Convai.DiagnoseConversation`

**Area:** Scene and conversation setup · **Enabled by default:** Yes · **Mutates:** No

Diagnoses active-scene Convai conversation readiness and runtime state with ranked evidence and suggested fixes. Works in both Edit Mode and Play Mode. Never mutates the project or returns API keys.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | `0` | Optional focused character GameObject instance ID. |
| `includeInactive` | `bool` | `true` | Include inactive scene objects. |

Returns `readyToRun`, configuration and runtime snapshots, and an `issues` array with stable codes, evidence, `autoFixable`, and `suggestedTool`/`suggestedArguments` for each issue.

## `Convai.ConfigureActions`

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

## `Convai.DiagnoseActions`

**Area:** Character actions · **Enabled by default:** Yes · **Mutates:** No

Diagnoses action definitions, executors, targets, attention, dispatcher presence, and runtime availability without mutation.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | `0` | Optional character instance ID. |
| `includeInactive` | `bool` | `true` | Include inactive objects. |

## `Convai.SimulateAction`

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

## `Convai.ConfigureLipSync`

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

## `Convai.DiagnoseLipSync`

**Area:** Lip sync · **Enabled by default:** Yes · **Mutates:** No

Diagnoses the `ConvaiLipSyncComponent`, target meshes, blendshape compatibility, mapping, profile, and sanitized runtime buffer state.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | `0` | Character GameObject instance ID. |
| `includeRuntimeMetrics` | `bool` | `true` | Include `isPlaying`, `isTalking`, `isFadingOut`, `engineState`, buffered and stream duration, and headroom. |

## `Convai.ConfigureTranscripts`

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

## `Convai.DiagnoseTranscripts`

**Area:** Transcripts · **Enabled by default:** Yes · **Mutates:** No

Diagnoses transcript enablement, facade readiness, relays, UIs, and sanitized runtime timeline metadata.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `managerInstanceId` | `long` | `0` | Optional manager instance ID. |
| `includeText` | `bool` | `false` | Include transcript text only when explicitly requested. |

## `Convai.ConfigureNarrative`

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

## `Convai.DiagnoseNarrative`

**Area:** Narrative · **Enabled by default:** Yes · **Mutates:** No

Diagnoses Unity-side narrative character bindings, duplicate or orphaned sections, template keys, triggers, player filters, cached sync errors, and runtime trigger state.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterInstanceId` | `long` | `0` | Character GameObject instance ID. |
| `includeInactive` | `bool` | `true` | Include inactive objects. |
| `includeContent` | `bool` | `false` | Include template values and trigger names. Content stays hidden by default. |

## `Convai.TraceRuntimeEvents`

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
