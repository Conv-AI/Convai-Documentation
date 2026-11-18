---
title: MCP tools reference
description: Look up the Convai commands exposed to coding agents, including their inputs, preview and runtime requirements, and the results to check.
last_reviewed: "5.0.0-pre.1"
---

The Convai Unity SDK exposes 52 commands through Unity CLI MCP. An MCP client calls `Convai_GetProjectStatus`. From a terminal, run `unity command Convai GetProjectStatus`. Keep the Unity Editor open to the project for either route.

## Tool behavior

All commands return a JSON result with `success`, `message`, and `data`. An MCP error from Convai carries that result in the error text. An argument that Pipeline rejects before the command runs produces a plain-text error. `Convai_ValidateSetup` returns a normal MCP result when it detects a blocking issue, with `success=false` and the findings in `data`.

Use the instance IDs returned by `Convai_InspectScene` and pass them back as strings. Scene-authoring commands preview by default where `dryRun` is supported. Applying the edit uses Unity Undo and leaves the scene open for you to save. Live-room changes require Play Mode and explicit `dryRun=false`. If a command times out, check the scene or room state before retrying a mutation.

For setup instructions, see [AI coding assistant quick start](quick-start.md). Inspect the client schema or run `unity command --query Convai` to see the open project's registered commands.

## Feature authoring results

The character feature configuration commands, `Convai_MarkGazeTarget`, and the two personality commands return a shared `data` shape. `dryRun` reports whether the operation was a preview. Read `complete` with `blockers` and `requiredInputs` to see whether the request applied or could apply in a preview. `readiness` reports the feature's present state, including during a preview.

`changes` describes the operations. `affectedInstanceIds` lists the distinct affected objects, components, or assets, and `characterInstanceId` identifies the character's GameObject. `details` carries feature-specific information. `sceneDirty` reports unsaved changes in the active scene, and `sceneSaved` is always `false`. For a failure, read `data.code`, `data.details`, and `data.nextSteps`.

## Reading the input tables

An omitted argument uses the value under **Default**. A `null` value typically preserves the authored setting. In an argument path, `[]` denotes an array item. Required flags on nested inputs apply when you supply the containing object. `timeout`, where present, controls the client wait separately from the command's `timeoutSeconds`.

## Guidance

### `Convai_GetGuidance`

Names the Convai skill reference, tools and documentation for a topic. Call before configuring a Convai feature; do not use for generic Unity operations.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `topic` | `string` | `Overview` | no | `Overview`, `Setup`, `Actions`, `DynamicContext`, `Vision`, `Narrative`, `Embodiment`, `Events`, `Runtime`, `Gaze`, `BodyAnimation`, `BodyLanguage`, `Emotion`, `MultiCharacter`, `SceneTagging` | — |

## Foundation

### `Convai_GetProjectStatus`

Reads Convai SDK and Unity Pipeline versions and non-secret project configuration status. Never returns the Convai API key.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `(none)` | `-` | `-` | - | — | — |

### `Convai_InspectScene`

Inspects open scenes for Convai managers, rooms, players, and characters. Use returned instance IDs for later mutations.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `includeInactive` | `boolean` | `true` | no | — | — |

### `Convai_ValidateSetup`

Validates Convai project and scene readiness without changing assets or scenes. Call before and after Convai authoring operations.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `scope` | `string` | `All` | no | `All`, `Project`, `Scene` | — |

## Scene and conversation setup

### `Convai_ConfigureRoom`

Previews or configures a Convai room on an explicit GameObject. Omitted inline settings keep their current values, and microphone processing, push-to-talk policy and interruption options are never changed. Uses Undo, never saves, and never changes credentials.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `connectOnStart` | `boolean` | `null` | no | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `inputMode` | `string` | `null` | no | `HandsFree`, `PushToTalk` | — |
| `pushToTalkKey` | `string` | `null` | no | — | — |
| `serverEndpoint` | `string` | `null` | no | `Connect`, `RoomSession`, `DemoConnect` | — |
| `targetInstanceId` | `string` | `0` | yes | — | — |
| `visionMode` | `string` | `null` | no | `Off`, `On` | — |

### `Convai_ConfigurePlayer`

Previews or adds and configures ConvaiPlayer on an explicit GameObject, then binds one unambiguous manager. Never modifies Main Camera.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `dryRun` | `boolean` | `true` | no | — | — |
| `managerInstanceId` | `string` | `0` | no | — | — |
| `playerId` | `string` | `""` | no | — | — |
| `playerName` | `string` | `"Player"` | no | — | — |
| `targetInstanceId` | `string` | `0` | yes | — | — |

### `Convai_ConfigureCharacter`

Previews or adds and configures ConvaiCharacter with recommended audio output on an explicit GameObject. Missing Character ID remains an explicit readiness blocker.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `addAudioOutput` | `boolean` | `true` | no | — | — |
| `characterId` | `string` | `""` | no | — | — |
| `characterName` | `string` | `""` | no | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `managerInstanceId` | `string` | `0` | no | — | — |
| `targetInstanceId` | `string` | `0` | yes | — | — |

### `Convai_SetupConversationScene`

Previews or performs end-to-end Audio conversation setup in the active scene using safe placeholders and recommended defaults. Never saves, enters Play Mode, or sets credentials.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterId` | `string` | `""` | no | — | — |
| `characterInstanceId` | `string` | `0` | no | — | — |
| `characterName` | `string` | `"Convai Character"` | no | — | — |
| `connectOnStart` | `boolean` | `true` | no | — | — |
| `createPlaceholders` | `boolean` | `true` | no | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `inputMode` | `string` | `HandsFree` | no | `HandsFree`, `PushToTalk` | — |
| `managerInstanceId` | `string` | `0` | no | — | — |
| `playerId` | `string` | `""` | no | — | — |
| `playerInstanceId` | `string` | `0` | no | — | — |
| `playerName` | `string` | `"Player"` | no | — | — |

### `Convai_DiagnoseConversation`

Diagnoses active-scene Convai conversation readiness and runtime state with ranked evidence and suggested fixes. Never mutates the project or returns API keys.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterInstanceId` | `string` | `0` | no | — | — |
| `includeInactive` | `boolean` | `true` | no | — | — |
| `includeRecentMultiCharacterEvents` | `boolean` | `false` | no | — | — |

### `Convai_SendTextMessage`

Previews or submits a typed message through the active player's real runtime path. Requires Play Mode and a ready character. Never returns message or reply text.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `dryRun` | `boolean` | `true` | no | — | — |
| `playerInstanceId` | `string` | `0` | no | — | — |
| `text` | `string` | `""` | yes | — | — |

## Group conversation

### `Convai_ConfigureGroupConversation`

Previews or adds and configures the Convai Group Conversation component: scene brief, topics, member aliases, anchor, spatial and timing overrides, and head-turns. Every field is optional and omitting one leaves it unchanged. Edit Mode only; uses Undo, never saves, and never changes credentials.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `anchorInstanceId` | `string` | `null` | no | — | — |
| `clearAnchor` | `boolean` | `null` | no | — | — |
| `driveGaze` | `boolean` | `null` | no | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `members` | `object[]` | `null` | no | — | — |
| `members[].aliases` | `string[]` | `[]` | no | — | — |
| `members[].characterInstanceId` | `string` | `0` | yes | — | — |
| `overrides` | `object[]` | `null` | no | — | — |
| `overrides[].key` | `string` | `""` | yes | `hearing_range_m`, `pause_hysteresis_m`, `address_radius_m`, `group_radius_m`, `gaze_dwell_threshold`, `lull_seconds`, `player_reply_wait_seconds`, `reply_to_question_window_seconds`, `empty_transcript_timeout_seconds`, `greeting_reentry_seconds`, `line_timeout_seconds` | — |
| `overrides[].useServerDefault` | `boolean` | `false` | no | — | — |
| `overrides[].value` | `number` | `null` | no | — | — |
| `playerDisplayName` | `string` | `null` | no | — | — |
| `sceneBrief` | `string` | `null` | no | — | — |
| `targetInstanceId` | `string` | `0` | no | — | — |
| `topics` | `object[]` | `null` | no | — | — |
| `topics[].id` | `string` | `""` | no | — | — |
| `topics[].starterCharacterInstanceId` | `string` | `0` | no | — | — |
| `topics[].starterCharacterName` | `string` | `""` | no | — | — |
| `topics[].text` | `string` | `""` | yes | — | — |

## Character memory settings

### `Convai_GetCharacterMemorySettings`

Reads whether a Convai character has long-term memory on and whether a connect must send an end-user ID. Read-only; contacts the Convai service with the project's API key. Never returns memories or end-user IDs.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterId` | `string` | `null` | no | — | — |
| `characterInstanceId` | `string` | `0` | no | — | — |

### `Convai_SetCharacterMemorySettings`

Previews or changes a Convai character's long-term memory on/off and whether a connect must send an end-user ID. Use only when the user asked to change memory: the change is made on the Convai service and applies to every app that uses the character. Previews by default; dryRun=false applies. Never returns memories or end-user IDs.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterId` | `string` | `null` | no | — | — |
| `characterInstanceId` | `string` | `0` | no | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `enabled` | `boolean` | `null` | no | — | — |
| `endUserIdRequirement` | `string` | `null` | no | `required`, `optional` | — |

## Conversation targeting

### `Convai_ConfigureConversationTargeting`

Previews or configures which characters join the next Convai room and how the SDK decides which of them the player is talking to. Every field is optional and omitting one leaves it unchanged. Uses Undo, never saves, and never changes credentials.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `clearInitialCharacter` | `boolean` | `null` | no | — | — |
| `clearViewCamera` | `boolean` | `null` | no | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `includeAllCharacters` | `boolean` | `null` | no | — | — |
| `includedCharacterInstanceIds` | `string[]` | `null` | no | — | — |
| `initialCharacterInstanceId` | `string` | `null` | no | — | — |
| `managerInstanceId` | `string` | `0` | no | — | — |
| `maxAngle` | `number` | `null` | no | — | — |
| `maxDistance` | `number` | `null` | no | — | — |
| `proximityMargin` | `number` | `null` | no | — | — |
| `switchDelaySeconds` | `number` | `null` | no | — | — |
| `switchMargin` | `number` | `null` | no | — | — |
| `targetingMode` | `string` | `null` | no | `LookAt`, `Proximity`, `Manual` | — |
| `viewCameraInstanceId` | `string` | `null` | no | — | — |

### `Convai_SimulateConversationTargeting`

Explains the geometric proposal and any live recovery fallback produced by configured LookAt or Proximity targeting. Read-only in Edit and Play Mode; never contacts the backend or claims to apply temporal switch gates.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `includeInactive` | `boolean` | `true` | no | — | — |
| `managerInstanceId` | `string` | `0` | no | — | — |
| `viewCameraInstanceId` | `string` | `0` | no | — | — |

### `Convai_SetupMultiCharacterRoster`

Previews or configures the exact roster of at least two characters for the next room and optionally chooses who speaks first. Validates local identity before applying through Unity Undo.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterInstanceIds` | `string[]` | `null` | yes | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `initialCharacterInstanceId` | `string` | `0` | no | — | — |
| `managerInstanceId` | `string` | `0` | no | — | — |

## Multi-character

### `Convai_SetConversationTarget`

Previews or changes which character the player is addressing in an active multi-character room. Execution requires Play Mode and an explicit dryRun=false; it never changes Play Mode.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterInstanceId` | `string` | `0` | yes | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `managerInstanceId` | `string` | `0` | no | — | — |
| `timeout` | `number` | `75` | no | — | — |
| `timeoutSeconds` | `number` | `10` | no | — | min `0.1`, max `60` |

### `Convai_UpdateCharacterRoster`

Previews or adds/removes one character in an active multi-character room and returns the authoritative roster and routing epochs. Execution requires Play Mode and dryRun=false; it never changes Play Mode.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterInstanceId` | `string` | `0` | yes | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `operation` | `string` | `Add` | no | `Add`, `Remove` | — |
| `replacementTargetCharacterInstanceId` | `string` | `0` | no | — | — |
| `roomManagerInstanceId` | `string` | `0` | no | — | — |
| `timeoutSeconds` | `number` | `15` | no | — | min `0.1`, max `15` |

### `Convai_WaitForCharacterReady`

Waits for one character already in the active multi-character room to become Ready. The wait never cancels character startup and never changes Play Mode.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterInstanceId` | `string` | `0` | yes | — | — |
| `roomManagerInstanceId` | `string` | `0` | no | — | — |
| `timeout` | `number` | `75` | no | — | — |
| `timeoutSeconds` | `number` | `30` | no | — | min `0.1`, max `60` |

### `Convai_WaitForMultiCharacterState`

Waits for authoritative target, roster epoch, route epoch, roster size, readiness, or conversation availability conditions in the active multi-character room. With no conditions, returns a current snapshot. Read-only and never changes Play Mode.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `expectedActiveCharacterInstanceId` | `string` | `0` | no | — | — |
| `expectedRosterSize` | `integer` | `-1` | no | — | min `-1` |
| `managerInstanceId` | `string` | `0` | no | — | — |
| `minimumRosterEpoch` | `integer` | `-1` | no | — | min `-1` |
| `minimumRouteEpoch` | `integer` | `-1` | no | — | min `-1` |
| `requireAllCharactersReady` | `boolean` | `false` | no | — | — |
| `requireConversationAvailable` | `boolean` | `false` | no | — | — |
| `timeout` | `number` | `75` | no | — | — |
| `timeoutSeconds` | `number` | `30` | no | — | min `0.1`, max `60` |

## Character actions

### `Convai_ConfigureActions`

Previews or safely upserts typed actions and explicit targets on a Convai character. Uses Undo and never saves.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterInstanceId` | `string` | `0` | yes | — | — |
| `characters` | `object[]` | `[]` | no | — | — |
| `characters[].description` | `string` | `""` | no | — | — |
| `characters[].gameObjectInstanceId` | `string` | `0` | yes | — | — |
| `characters[].name` | `string` | `""` | yes | — | — |
| `definitions` | `object[]` | `[]` | no | — | — |
| `definitions[].answerDelivery` | `string` | `null` | no | `UseCharacterSetting`, `RememberOnly`, `MentionIfRelevant`, `TellThePlayer` | — |
| `definitions[].category` | `string` | `null` | no | — | — |
| `definitions[].delayAfterBotSpeechSeconds` | `number` | `0` | no | — | min `0` |
| `definitions[].description` | `string` | `""` | no | — | — |
| `definitions[].enabled` | `boolean` | `null` | no | — | — |
| `definitions[].executorInstanceId` | `string` | `0` | no | — | — |
| `definitions[].failurePolicy` | `string` | `null` | no | `UseDispatcherDefault`, `StopBatch`, `ContinueBatch` | — |
| `definitions[].name` | `string` | `""` | yes | — | — |
| `definitions[].parameters` | `object[]` | `null` | no | — | — |
| `definitions[].parameters[].choices` | `string[]` | `null` | no | — | — |
| `definitions[].parameters[].connector` | `string` | `null` | no | — | — |
| `definitions[].parameters[].description` | `string` | `""` | no | — | — |
| `definitions[].parameters[].name` | `string` | `""` | yes | — | — |
| `definitions[].parameters[].type` | `string` | `Auto` | no | `Auto`, `Reference`, `String`, `Number`, `Bool`, `Choice` | — |
| `definitions[].targetRequirement` | `string` | `None` | no | `None`, `Object`, `Character`, `Either` | — |
| `definitions[].timeoutSeconds` | `number` | `0` | no | — | min `0` |
| `definitions[].waitForBotSpeech` | `boolean` | `false` | no | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `initialAttentionObject` | `string` | `""` | no | — | — |
| `objects` | `object[]` | `[]` | no | — | — |
| `objects[].description` | `string` | `""` | no | — | — |
| `objects[].gameObjectInstanceId` | `string` | `0` | yes | — | — |
| `objects[].name` | `string` | `""` | yes | — | — |

### `Convai_DiagnoseActions`

Diagnoses action definitions, executors, targets, attention, dispatcher presence, and runtime availability without mutation.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterInstanceId` | `string` | `0` | no | — | — |
| `includeInactive` | `boolean` | `true` | no | — | — |

### `Convai_SimulateAction`

Validates an action in Edit Mode or dispatches it through the real runtime dispatcher in Play Mode. Never changes Play Mode.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `actionName` | `string` | `""` | yes | — | — |
| `characterInstanceId` | `string` | `0` | yes | — | — |
| `parameters` | `object` | `{}` | no | — | — |
| `target` | `string` | `""` | no | — | — |
| `timeout` | `number` | `75` | no | — | — |
| `timeoutSeconds` | `number` | `10` | no | — | min `0.1`, max `60` |

## Scene Auto Tagger

Candidate discovery stays in Unity. Drafting a scene description and tagging objects upload captured images to Convai Vision. Review the results before applying them. See [Scene Auto Tagger](../features/scene-metadata/scene-auto-tagger.md).

### `Convai_FindSceneTagCandidates`

Lists the active scene's objects that the Scene Auto Tagger would name and describe, ranked by relevance, with any World Object text they already have. Read-only; uploads nothing. Pass the instance IDs to Convai.TagSceneObjects.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `excludePlainShapes` | `boolean` | `true` | no | — | — |
| `includeTagged` | `boolean` | `false` | no | — | — |
| `limit` | `integer` | `100` | no | — | min `1`, max `300` |
| `minimumRelevance` | `number` | `null` | no | — | — |
| `objectInstanceIds` | `string[]` | `null` | no | — | — |

### `Convai_DescribeSceneView`

Drafts a short name and a description of the environment a camera or the last active Scene view shows, for Convai.TagSceneObjects' sceneDescription. Changes nothing in the scene. Uploads captured images and the guidance text to Convai Vision; call only when the user asked to tag or describe the scene. Waits up to waitSeconds; if the result says Running, call Convai.GetSceneTagRun with its runId.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `cameraInstanceId` | `string` | `0` | no | — | — |
| `characterId` | `string` | `null` | no | — | — |
| `characterInstanceId` | `string` | `0` | no | — | — |
| `waitSeconds` | `number` | `40` | no | — | min `0`, max `50` |

### `Convai_TagSceneObjects`

Starts a Scene Auto Tagger run: captures each object and asks Convai Vision for a name and description shaped by the character. Changes nothing in the scene. Uploads captured images and the guidance text to Convai Vision; call only when the user asked to tag or describe the scene. Waits up to waitSeconds; if the result says Running, call Convai.GetSceneTagRun with its runId. Apply with Convai.ApplySceneTags.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterId` | `string` | `null` | no | — | — |
| `characterInstanceId` | `string` | `0` | no | — | — |
| `focus` | `string` | `null` | no | — | — |
| `includeLowInformation` | `boolean` | `false` | no | — | — |
| `quality` | `string` | `Fast` | no | `Fast`, `Accurate` | — |
| `sceneDescription` | `string` | `null` | no | — | — |
| `targets` | `object[]` | `null` | yes | — | — |
| `targets[].instanceId` | `string` | `0` | yes | — | — |
| `targets[].note` | `string` | `null` | no | — | — |
| `waitSeconds` | `number` | `40` | no | — | min `0`, max `50` |

### `Convai_GetSceneTagRun`

Waits for, reads, or cancels a run started by Convai.TagSceneObjects or Convai.DescribeSceneView. Returns the results when the run has finished. Changes nothing in the scene.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `cancel` | `boolean` | `false` | no | — | — |
| `runId` | `string` | `null` | yes | — | — |
| `waitSeconds` | `number` | `40` | no | — | min `0`, max `50` |

### `Convai_ApplySceneTags`

Previews or writes a finished tagging run's names and descriptions as World Objects (ConvaiWorldObject), with optional action and gaze targets, in one Undo step. Hand-authored metadata is kept, and objects that changed since capture are refused. Previews by default; dryRun=false applies. Never saves the scene.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `createActionTargets` | `boolean` | `true` | no | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `enableGaze` | `boolean` | `true` | no | — | — |
| `includeSpatialContext` | `boolean` | `true` | no | — | — |
| `objects` | `object[]` | `null` | no | — | — |
| `objects[].description` | `string` | `null` | no | — | — |
| `objects[].instanceId` | `string` | `0` | yes | — | — |
| `objects[].name` | `string` | `null` | no | — | — |
| `runId` | `string` | `null` | yes | — | — |

## Lip sync

### `Convai_ConfigureLipSync`

Previews or configures Convai lip sync using existing meshes, shipped profiles, and optional existing maps. Never creates or mutates assets.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterInstanceId` | `string` | `0` | yes | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `latencyMode` | `string` | `Balanced` | no | `Balanced`, `UltraLowLatency`, `NetworkSafe`, `Custom` | — |
| `mappingAssetPath` | `string` | `""` | no | — | — |
| `meshInstanceIds` | `string[]` | `[]` | no | — | — |
| `profile` | `string` | `"Auto"` | no | — | — |

### `Convai_DiagnoseLipSync`

Diagnoses Convai lip-sync component, meshes, blendshape compatibility, mapping, profile, and sanitized runtime buffer state.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterInstanceId` | `string` | `0` | no | — | — |
| `includeRuntimeMetrics` | `boolean` | `true` | no | — | — |

## Transcripts

### `Convai_ConfigureTranscripts`

Previews or configures the canonical transcript facade, event relay, or shipped chat UI. Never changes ConvaiSettings or exposes text.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterIdFilter` | `string` | `""` | no | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `hostInstanceId` | `string` | `0` | no | — | — |
| `managerInstanceId` | `string` | `0` | no | — | — |
| `mode` | `string` | `EventRelay` | no | `EventRelay`, `ChatUI`, `WorldSpaceChatUI` | — |
| `speakerFilter` | `string` | `Any` | no | `Any`, `Player`, `Character` | — |

### `Convai_DiagnoseTranscripts`

Diagnoses transcript enablement, facade readiness, relays, UIs, and sanitized runtime timeline metadata.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `includeText` | `boolean` | `false` | no | — | — |
| `managerInstanceId` | `string` | `0` | no | — | — |

## Narrative

### `Convai_ConfigureNarrative`

Previews or configures Unity-side Convai narrative section mappings, template keys, and triggers. Preserves unrelated entries and UnityEvents; never contacts the backend.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterInstanceId` | `string` | `0` | yes | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `managerHostInstanceId` | `string` | `0` | no | — | — |
| `sections` | `object[]` | `[]` | no | — | — |
| `sections[].sectionId` | `string` | `""` | yes | — | — |
| `sections[].sectionName` | `string` | `""` | no | — | — |
| `templateKeys` | `object[]` | `[]` | no | — | — |
| `templateKeys[].key` | `string` | `""` | yes | — | — |
| `templateKeys[].value` | `string` | `""` | no | — | — |
| `triggers` | `object[]` | `[]` | no | — | — |
| `triggers[].activationMode` | `string` | `Collision` | no | `Collision`, `Proximity`, `Manual`, `TimeBased` | — |
| `triggers[].hostInstanceId` | `string` | `0` | no | — | — |
| `triggers[].playerLayerMask` | `integer` | `-1` | no | — | — |
| `triggers[].playerTag` | `string` | `"Player"` | no | — | — |
| `triggers[].proximityRadius` | `number` | `3` | no | — | — |
| `triggers[].timeDelay` | `number` | `0` | no | — | — |
| `triggers[].triggerId` | `string` | `""` | yes | — | — |
| `triggers[].triggerName` | `string` | `""` | no | — | — |
| `triggers[].triggerOnce` | `boolean` | `true` | no | — | — |

### `Convai_DiagnoseNarrative`

Diagnoses Unity-side Convai narrative character bindings, duplicate/orphaned sections, template keys, triggers, player filters, cached sync errors, and runtime trigger state. Content stays hidden by default.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterInstanceId` | `string` | `0` | no | — | — |
| `includeContent` | `boolean` | `false` | no | — | — |
| `includeInactive` | `boolean` | `true` | no | — | — |

## Runtime diagnostics

### `Convai_TraceRuntimeEvents`

Starts, reads, clears, or stops a bounded editor-only Convai runtime event trace. Transcript capture is off by default.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `captureTranscripts` | `boolean` | `false` | no | — | — |
| `characterInstanceId` | `string` | `0` | no | — | — |
| `eventFilters` | `string[]` | `[]` | no | — | — |
| `limit` | `integer` | `100` | no | — | min `1`, max `256` |
| `managerInstanceId` | `string` | `0` | no | — | — |
| `operation` | `string` | `Read` | no | `Start`, `Read`, `Clear`, `Stop` | — |

## Embodiment



### `Convai_ConfigureEmbodiment`

Sets a Convai character up so it can come alive: works out its rig now instead of at runtime, adds the expressive features you name — whichever of Gaze, Emotion, Body Animation, Body Language and Conversation Flow this project has installed — and assigns an Embodiment Preset the project already has. Previews by default. Never creates or edits an asset, and never tunes a feature; each feature has its own Configure tool for that.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `capabilities` | `string[]` | `[]` | no | — | — |
| `characterInstanceId` | `string` | `0` | yes | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `presetAssetPath` | `string` | `""` | no | — | — |
| `setUpRig` | `boolean` | `true` | no | — | — |

### `Convai_DiagnoseEmbodiment`

Surveys one Convai character end to end: whether its rig is understood, which expressive features it has, which of them will actually do something and which are blocked or inert and why, which settings assets they run on, its Embodiment Preset, and — in Play Mode — what it is doing right now. Call this before any other Convai embodiment tool; it names the per-feature tool to call next. Read-only.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterInstanceId` | `string` | `0` | no | — | — |
| `includeCapabilities` | `boolean` | `true` | no | — | — |
| `includeRuntimeState` | `boolean` | `true` | no | — | — |

### `Convai_InspectEmbodimentPresets`

Lists the Embodiment Presets this project has and whether each one is valid, so a preset can be assigned to a character without guessing which assets exist. Also lists every expressive feature a preset can carry and the menu path that creates its settings asset. Read-only, and never creates or edits an asset.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `folderPaths` | `string[]` | `[]` | no | — | — |

## Gaze



### `Convai_ConfigureGaze`

Adds Convai Gaze to a character and tunes how it makes eye contact — who it treats as the player, how strongly it commits, how it turns its body, and which optional extras it has. Previews by default. Assigns an existing Gaze Profile if the project has one; never creates or edits an asset. Omitted settings are left unchanged.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `allowScriptedOverrides` | `boolean` | `null` | no | — | — |
| `autoCreatePlayerAnchor` | `boolean` | `null` | no | — | — |
| `bodyTurnStyle` | `string` | `null` | no | `SteppingTurn`, `SmoothRotation` | — |
| `capabilities` | `string[]` | `null` | no | `PlayerAttention`, `AttentionGrounding`, `ReferentialGlances`, `JointAttention`, `CharacterGaze`, `PupilResponse` | — |
| `characterInstanceId` | `string` | `0` | yes | — | — |
| `clearPlayerAnchorOverride` | `boolean` | `null` | no | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `eyeContactMode` | `string` | `null` | no | `Natural`, `ConversationLock`, `AlwaysLock`, `SpeakingFocus` | — |
| `focusFidelity` | `string` | `null` | no | `Social`, `Exact` | — |
| `lockBlocksGlances` | `boolean` | `null` | no | — | — |
| `playerAnchorAimMode` | `string` | `null` | no | `Auto`, `ExactTransform`, `LocalOffset` | — |
| `playerAnchorAimOffset` | `object` | `null` | no | — | — |
| `playerAnchorAimOffset.x` | `number` | `0` | no | — | — |
| `playerAnchorAimOffset.y` | `number` | `0` | no | — | — |
| `playerAnchorAimOffset.z` | `number` | `0` | no | — | — |
| `playerAnchorInstanceId` | `string` | `null` | no | — | — |
| `profileAssetPath` | `string` | `null` | no | — | — |

### `Convai_DiagnoseGaze`

Explains why a character is or is not looking at the player: which head and eye bones resolved, whether the rig faces the right way, what it treats as the player and which setting decided that, which personality is in use, which optional extras it has, and live gaze state in Play Mode. Read-only.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterInstanceId` | `string` | `0` | no | — | — |
| `includeRuntimeState` | `boolean` | `true` | no | — | — |

### `Convai_MarkGazeTarget`

Marks scene objects as worth looking at, so Convai characters glance at them — a painting, a screen, a prop. Previews by default. Adds a component to the objects named; never creates an asset.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `aimOffset` | `object` | `null` | no | — | — |
| `aimOffset.x` | `number` | `0` | no | — | — |
| `aimOffset.y` | `number` | `0` | no | — | — |
| `aimOffset.z` | `number` | `0` | no | — | — |
| `baseRelevance` | `number` | `null` | no | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `fullRelevanceDistance` | `number` | `null` | no | — | — |
| `gameObjectInstanceIds` | `string[]` | `[]` | yes | — | — |
| `maxDistance` | `number` | `null` | no | — | — |
| `priority` | `integer` | `null` | no | — | — |
| `remove` | `boolean` | `false` | no | — | — |

## Body animation



### `Convai_ConfigureBodyAnimation`

Adds Convai Body Animation to a character and sets it up — the shipped animation content, whether the character can walk, and how it moves. Previews by default. Assigns existing content assets; never creates, edits or measures an asset, and never touches an Animator Controller. Omitted settings are left unchanged.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `accelerationMetersPerSecondSquared` | `number` | `null` | no | — | — |
| `animationSetAssetPath` | `string` | `null` | no | — | — |
| `autoJogDistanceMeters` | `number` | `null` | no | — | — |
| `characterInstanceId` | `string` | `0` | yes | — | — |
| `configAssetPath` | `string` | `null` | no | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `includeMovement` | `boolean` | `true` | no | — | — |
| `minJogDistanceMeters` | `number` | `null` | no | — | — |
| `profileAssetPath` | `string` | `null` | no | — | — |
| `rotationDegreesPerSecond` | `number` | `null` | no | — | — |
| `speedProfile` | `string` | `null` | no | `Walk`, `Jog`, `Auto` | — |

### `Convai_DiagnoseBodyAnimation`

Explains what a character's body animation is actually doing: whether it is set up at all, whether the rig can drive it, which animation content it resolved, which behaviours work and which are inert because this character has no clips for them, how the rig's scale is calibrated, and live state in Play Mode. Read-only.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterInstanceId` | `string` | `0` | no | — | — |
| `includeRuntimeState` | `boolean` | `true` | no | — | — |

### `Convai_InspectBodyAnimationContent`

Lists what a character's Animation Set can actually perform — the idle, talk, listen and think pools, every action and gesture with the names you can play it by, walking coverage, and pointing directions. Read-only. Call this before writing code that uses PlayAction.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `animationSetAssetPath` | `string` | `null` | no | — | — |
| `characterInstanceId` | `string` | `0` | no | — | — |

### `Convai_TuneBodyAnimationPersonality`

Tunes how expressive and how calm a character is, and whether it keeps busy when alone. Because one Body Animation Config can be shared by many characters, this makes a private copy for the named character before changing anything, so tuning one character never changes another. Previews by default and needs explicit consent before copying.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `archetype` | `string` | `null` | no | `Composed`, `Warm`, `Energetic`, `Reserved` | — |
| `characterInstanceId` | `string` | `0` | yes | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `howCalm` | `number` | `null` | no | — | — |
| `howExpressive` | `number` | `null` | no | — | — |
| `howOftenSeconds` | `number` | `null` | no | — | — |
| `keepsBusyWhenAlone` | `boolean` | `null` | no | — | — |
| `makeConfigUnique` | `boolean` | `false` | no | — | — |

## Body language



### `Convai_ConfigureBodyLanguage`

Adds Convai Body Language to a character so it breathes, shifts its weight, sways and gestures as it talks, and gives it a personality by assigning a Body Language Profile the project already has. Previews by default. Never creates or edits an asset, and refuses a character whose rig cannot drive the module rather than adding something inert.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `assignDefaultPersonality` | `boolean` | `false` | no | — | — |
| `characterInstanceId` | `string` | `0` | yes | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `personalityAssetPath` | `string` | `null` | no | — | — |

### `Convai_DiagnoseBodyLanguage`

Explains what a character's body is doing and why: what its rig offers, which personality tunes it and which behaviours that personality switches off, which other Convai modules share its body and what each one changes, and — in Play Mode — its live posture, breathing, weight shifts and gesture suppression. Answers \

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterInstanceId` | `string` | `0` | no | — | — |
| `includeRuntimeState` | `boolean` | `true` | no | — | — |

### `Convai_InspectBodyLanguagePersonalities`

Lists the Body Language Profiles in this project — what each one's expressiveness is, which behaviours it switches off, and which characters in the open scenes already use it. Read this before giving a character a personality, since these tools assign a personality but never author one. Read-only.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `folderPaths` | `string[]` | `[]` | no | — | — |

## Emotion



### `Convai_ConfigureEmotion`

Adds Convai Emotions to a character so its face reacts to what is said, gives it a personality the project already has, and sets how it detects feelings and what it rests at. Previews by default. Only ever writes fields on the character itself — it never creates or edits a personality asset, so it can never restyle other characters by accident.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterInstanceId` | `string` | `0` | yes | — | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `emotionDetection` | `string` | `null` | no | `Off`, `Accurate`, `Responsive` | — |
| `personalityAssetPath` | `string` | `""` | no | — | — |
| `restingMood` | `string` | `""` | no | — | — |
| `restingMoodStrength` | `number` | `null` | no | — | — |

### `Convai_DiagnoseEmotion`

Explains what a Convai character's face will actually do and why: whether it can show emotions at all, how it detects them, which personality tunes it, what it rests at and which setting decided that, and which of its behaviours are switched off or quietly gated by another setting. Answers \

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterInstanceId` | `string` | `0` | no | — | — |
| `includeRuntimeState` | `boolean` | `true` | no | — | — |

### `Convai_InspectEmotionPersonalities`

Lists the Convai emotion personalities in this project — which character type each one is, what it rests at, which of its behaviours are on, whether it ships with the SDK, and which characters already use it. Read this before giving a character a personality, since these tools assign one but never author one from nothing. Read-only.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `folderPaths` | `string[]` | `[]` | no | — | — |

### `Convai_TuneEmotionPersonality`

Changes how a Convai character feels — its character type, what it rests at, how strongly and quickly it shows things, and its feel switches. These live on a personality asset that other characters may share, so this previews first and, on explicit consent, gives the character its own copy and writes only that. It never edits a shared or SDK-shipped personality in place.

| Argument | Type | Default | Required | Choices | Limits |
| --- | --- | --- | --- | --- | --- |
| `characterInstanceId` | `string` | `0` | yes | — | — |
| `characterType` | `string` | `null` | no | `Composed`, `Warm`, `Energetic`, `Reserved` | — |
| `dryRun` | `boolean` | `true` | no | — | — |
| `howQuicklyItReacts` | `number` | `null` | no | — | — |
| `howStronglyItShows` | `number` | `null` | no | — | — |
| `makePersonalityUnique` | `boolean` | `false` | no | — | — |
| `moodFollowsConversation` | `boolean` | `null` | no | — | — |
| `neverSitsPerfectlyStill` | `boolean` | `null` | no | — | — |
| `picksUpOtherCharactersMoods` | `boolean` | `null` | no | — | — |
| `restingMood` | `string` | `""` | no | — | — |
| `restingMoodStrength` | `number` | `null` | no | — | — |
| `showsMoreThanOneEmotion` | `boolean` | `null` | no | — | — |

## Related pages

{% content-ref url="quick-start.md" %}
[AI coding assistant quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot AI coding assistant setup](troubleshooting.md)
{% endcontent-ref %}
