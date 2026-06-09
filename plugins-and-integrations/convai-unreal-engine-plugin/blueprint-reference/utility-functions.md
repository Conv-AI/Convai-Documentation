---
title: Convai utility functions
description: Reference for UConvaiUtils and UCommandLineUtils Blueprint libraries — look-at helpers, component lookups, blendshapes, audio, settings, and diagnostic nodes.
last_reviewed: "2026-06-05"
---

`UConvaiUtils` is a `UBlueprintFunctionLibrary` that exposes miscellaneous helper nodes to Blueprint. It does not need to be attached to an `Actor`; all nodes are callable from any Blueprint graph. Nodes are grouped in the **Convai** category tree in the Blueprint node search palette.

## Look-at helpers

These nodes cast a world-space ray from the player controller's camera and find the nearest Convai component within a given radius.

### `ConvaiGetLookedAtCharacter`

Category: `Convai|Utilities`

Returns the `UConvaiChatbotComponent` on the character the player is currently looking at.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `WorldContextObject` | Input | `UObject*` | World context (auto-wired in Blueprint). |
| `PlayerController` | Input | `APlayerController*` | The controller whose camera orientation is used for the look direction. |
| `Radius` | Input | `float` | Search radius in world units around the look direction ray. |
| `PlaneView` | Input | `bool` | When `true`, only the horizontal plane angle is used (ignores vertical pitch). |
| `IncludedCharacters` | Input | `TArray<UObject*>` | Optional allowlist — only these objects are considered. Pass an empty array to consider all. |
| `ExcludedCharacters` | Input | `TArray<UObject*>` | Optional denylist — these objects are always skipped. |
| `ConvaiCharacter` | Output | `UConvaiChatbotComponent*` | The chatbot component found, or `nullptr` when `Found` is `false`. |
| `Found` | Output | `bool` | `true` when a character was found within `Radius`. |

{% hint style="info" %}
`IncludedCharacters` and `ExcludedCharacters` auto-create their reference terms, so you can leave both empty in Blueprint and the node will search all registered chatbot components.
{% endhint %}

### `ConvaiGetLookedAtObjectOrCharacter`

Category: `Convai|Utilities`

Returns the `FConvaiObjectEntry` (an object or character) from a provided list that the player is currently looking at. Use this when you need to detect gaze attention across a mixed set of objects and characters.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `WorldContextObject` | Input | `UObject*` | World context (auto-wired in Blueprint). |
| `PlayerController` | Input | `APlayerController*` | The controller whose camera orientation is used. |
| `Radius` | Input | `float` | Search radius in world units. |
| `PlaneView` | Input | `bool` | When `true`, only the horizontal plane angle is used. |
| `ListToSearchIn` | Input | `TArray<FConvaiObjectEntry>` | The list of objects and characters to search. |
| `FoundObjectOrCharacter` | Output | `FConvaiObjectEntry` | The matched entry, or an empty entry when `Found` is `false`. |
| `Found` | Output | `bool` | `true` when a match was found within `Radius`. |


## Component lookups

These nodes query the world for registered Convai components without requiring a direct object reference.

### `ConvaiGetAllChatbotComponents`

Category: `Convai|Utilities`

Returns all `UConvaiChatbotComponent` instances currently registered in the world.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `WorldContextObject` | Input | `UObject*` | World context (auto-wired in Blueprint). |
| `bOnlyConnected` | Input | `bool` | When `true`, only chatbots whose session is in the `Connected` state are returned. |
| `ConvaiChatbotComponents` | Output | `TArray<UConvaiChatbotComponent*>` | All matching chatbot components. |
| `OutOwners` | Output | `TArray<AActor*>` | Owning actors in the same order as `ConvaiChatbotComponents`. |

### `GetFirstConvaiChatbotComponent`

Category: `Convai|Utilities`

Returns the first `UConvaiChatbotComponent` found in the world — a convenience shortcut when only one character is present.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `WorldContextObject` | Input | `UObject*` | World context (auto-wired in Blueprint). |
| `bOnlyConnected` | Input | `bool` | When `true`, only considers chatbots in the `Connected` state. |
| `Return value` | Output | `UConvaiChatbotComponent*` | The first matching component, or `nullptr` when none exist. |
| `OutOwner` | Output | `AActor*` | The owning actor of the returned component. |

### `ConvaiGetAllPlayerComponents`

Category: `Convai|Utilities`

Returns all `UConvaiPlayerComponent` instances currently registered in the world.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `WorldContextObject` | Input | `UObject*` | World context (auto-wired in Blueprint). |
| `bOnlyConnected` | Input | `bool` | When `true`, only returns components that have a started or active session. |
| `ConvaiPlayerComponents` | Output | `TArray<UConvaiPlayerComponent*>` | All matching player components. |
| `OutOwners` | Output | `TArray<AActor*>` | Owning actors in the same order as `ConvaiPlayerComponents`. |

### `GetFirstConvaiPlayerComponent`

Category: `Convai|Utilities`

Returns the first `UConvaiPlayerComponent` found in the world.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `WorldContextObject` | Input | `UObject*` | World context (auto-wired in Blueprint). |
| `bOnlyConnected` | Input | `bool` | When `true`, only considers components with an active session. |
| `Return value` | Output | `UConvaiPlayerComponent*` | The first matching component, or `nullptr` when none exist. |
| `OutOwner` | Output | `AActor*` | The owning actor of the returned component. |

### `ConvaiGetAllObjectComponents`

Category: `Convai|Utilities`

Returns all `UConvaiObjectComponent` instances currently registered in the world.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `WorldContextObject` | Input | `UObject*` | World context (auto-wired in Blueprint). |
| `ConvaiObjectComponents` | Output | `TArray<UConvaiObjectComponent*>` | All registered object components. |
| `OutOwners` | Output | `TArray<AActor*>` | Owning actors in the same order as `ConvaiObjectComponents`. |

### `GetFirstConvaiObjectComponent`

Category: `Convai|Utilities`

Returns the first `UConvaiObjectComponent` found in the world.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `WorldContextObject` | Input | `UObject*` | World context (auto-wired in Blueprint). |
| `Return value` | Output | `UConvaiObjectComponent*` | The first matching component, or `nullptr` when none exist. |
| `OutOwner` | Output | `AActor*` | The owning actor of the returned component. |


## Settings accessors

These nodes read and write runtime settings on the active `UConvaiSettings` instance. Changes made with `Set*` nodes take effect immediately; the value is not persisted to `.ini` unless you save project settings separately.

| Node | Category | Type | Description |
|---|---|---|---|
| `SetAPI_Key` | `Convai\|Settings` | `BlueprintCallable` | Overwrites the API key used for authentication. Input: `API_Key (FString)`. |
| `GetAPI_Key` | `Convai\|Settings` | `BlueprintPure` | Returns the current API key as `FString`. |
| `SetAuthToken` | `Convai\|Settings` | `BlueprintCallable` | Overwrites the auth token. Input: `AuthToken (FString)`. |
| `GetAuthToken` | `Convai\|Settings` | `BlueprintPure` | Returns the current auth token as `FString`. |
| `GetTestCharacterID` | `Convai\|Settings` | `BlueprintPure` | Returns the test character ID configured in settings. |
| `SetCustomParam` | `Convai\|Settings` | `BlueprintCallable` | Writes a key-value pair into the `CustomPrams` settings map. The value is resolved by `GetCustomParam` using the chain: built-in defaults → `CustomPrams` → command-line overrides. Inputs: `Key (FString)`, `Value (FString)`. |
| `GetCustomParam` | `Convai\|Settings` | `BlueprintPure` | Returns the resolved value for `Key` using the full resolve chain. Returns `DefaultValue` when the chain yields an empty string. Inputs: `Key (FString)`, `DefaultValue (FString)`. Return: `FString`. |
| `GetClientVersion` | `Convai\|Settings` | `BlueprintPure` | Returns the `client_version` resolved via the `CustomPrams` / command-line resolve chain. Return: `FString`. |
| `GetVADSettings` | `Convai\|Settings` | `BlueprintPure` | Returns a snapshot of the current `FConvaiVADSettings` from project settings. |
| `SetVADSettings` | `Convai\|Settings` | `BlueprintCallable` | Overwrites the VAD settings on the active `UConvaiSettings` instance. Persisted to `.ini` on save. Input: `InSettings (FConvaiVADSettings)`. |
| `IsAlwaysAllowVisionEnabled` | `Convai\|Settings` | `BlueprintPure` | Returns `true` when the Always Allow Vision setting is enabled. |

`FConvaiVADSettings` field descriptions (`bUseServerDefault`, `Confidence`, `StartSecs`, `StopSecs`, `MinVolume`) are in [Data types and enums](data-types-and-enums.md).

## Audio helpers

### `StereoToMono`

Category: `Convai|Utilities`

Converts stereo WAV bytes to mono WAV bytes in-place.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `stereoWavBytes` | Input | `TArray<uint8>` | Raw stereo WAV byte array. |
| `monoWavBytes` | Output | `TArray<uint8>` | Resulting mono WAV byte array. |

### `WriteSoundWaveToWavFile`

Category: `Convai|Utilities`

Writes a `USoundWave` to a `.wav` file on disk.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `SoundWave` | Input | `USoundWave*` | The sound wave asset to write. |
| `FilePath` | Input | `FString` | Absolute file path for the output file. |
| `Return value` | Output | `bool` | `true` on success. |

### `ReadWavFileAsSoundWave`

Category: `Convai|Utilities` — `BlueprintPure`

Reads a `.wav` file from disk and returns it as a `USoundWave`.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `FilePath` | Input | `FString` | Absolute path to a `.wav` file on disk. |
| `Return value` | Output | `USoundWave*` | The loaded sound wave, or `nullptr` on failure. |


## File I/O

| Node | Returns | Description |
|---|---|---|
| `ReadFileAsByteArray` | `bool`, `Bytes (TArray<uint8>)` | Reads a file at `FilePath` into a byte array. Returns `false` on failure. |
| `SaveByteArrayAsFile` | `bool` | Writes `Bytes` to the file at `FilePath`. Returns `false` on failure. |
| `ByteArrayToString` | `FString` | Converts `Bytes` to a UTF-8 `FString`. |
| `WriteStringToFile` | `bool` | Writes `StringToWrite` to the file at `FilePath`. Returns `false` on failure. |
| `ReadStringFromFile` | `bool`, `OutString (FString)` | Reads the file at `FilePath` into `OutString`. Returns `false` on failure. |


## Blendshape utilities

These nodes manipulate `TMap<FName, float>` blendshape maps and are used primarily with the lip sync and face animation pipeline. See [Convai Chatbot Component](convai-chatbot-component.md) for the nodes that send blendshape data to a character.

### `MapBlendshapes`

Category: `Convai|Blendshapes` — `BlueprintPure`

Maps and transforms blendshapes from one naming convention or rig to another. Supports per-blendshape multipliers, offsets, clamping, and override values.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `InputBlendshapes` | Input | `TMap<FName, float>` | Source blendshape map (for example ARKit output). |
| `BlendshapeMap` | Input | `TMap<FName, FConvaiBlendshapeParameters>` | Per-blendshape transform configuration. Each entry maps a source key to one or more target names, a multiplier, offset, and optional clamp and override values. |
| `GlobalMultiplier` | Input | `float` | Applied to all blendshapes except those with `IgnoreGlobalModifiers` set. |
| `GlobalOffset` | Input | `float` | Added to all blendshapes except those with `IgnoreGlobalModifiers` set. |
| `Return value` | Output | `TMap<FName, float>` | Transformed blendshape map ready for the target rig. |

`FConvaiBlendshapeParameters` fields:

| Field | Type | Default | Description |
|---|---|---|---|
| `TargetNames` | `TArray<FName>` | — | Output key names to write the transformed value to. |
| `Multiplyer` | `float` | `1.0` | Per-blendshape multiplier applied before global modifiers. |
| `Offset` | `float` | `0.0` | Per-blendshape offset applied after multiplication. |
| `UseOverrideValue` | `bool` | `false` | When `true`, writes `OverrideValue` directly, ignoring input and modifiers. |
| `IgnoreGlobalModifiers` | `bool` | `false` | When `true`, `GlobalMultiplier` and `GlobalOffset` are not applied to this entry. |
| `OverrideValue` | `float` | `0.0` | Fixed value written when `UseOverrideValue` is `true`. |
| `ClampMinValue` | `float` | `0.0` | Output is clamped to this minimum. |
| `ClampMaxValue` | `float` | `1.0` | Output is clamped to this maximum. |

### `SplitBlendshapeMapByKeys`

Category: `Convai|Blendshapes` — `BlueprintCallable` (display name **Split Blendshape Map by Keys**)

Splits a blendshape map in two: keys listed in `SplitKeys` are removed from `InOutOriginalMap` and placed into `OutSplitMap`. Useful for separating facial regions that need different blend modes.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `InOutOriginalMap` | Input/Output (ref) | `TMap<FName, float>` | Modified in place — matched keys are removed. |
| `SplitKeys` | Input | `TArray<FName>` | Keys to extract. |
| `OutSplitMap` | Output | `TMap<FName, float>` | Contains only the extracted key-value pairs. |

### `MergeBlendshapeMaps`

Category: `Convai|Blendshapes` — `BlueprintPure` (display name **Merge Blendshape Maps**)

Merges two blendshape maps. When the same key exists in both maps, the value from `OverrideMap` takes precedence.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `BaseMap` | Input | `TMap<FName, float>` | Base blendshape values. |
| `OverrideMap` | Input | `TMap<FName, float>` | Values that override `BaseMap` on key collision. |
| `Return value` | Output | `TMap<FName, float>` | Combined map. |


## Lip sync helpers

### `FixCC5LipsyncPostProcessBlendshapes`

Category: `Convai|LipSync`

Fixes a conflict between post-process facial animation and lip sync on Character Creator 5 characters. The function locates the `ExpBoneData` array property (of type `RLExpStruct`) on the skeletal mesh's post-process anim instance and removes the word `"jaw"` from each `ExpName` and `BoneName` field.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `AnimInstance` | Input | `UAnimInstance*` | The animation instance whose owning skeletal mesh component is inspected. |
| `Return value` | Output | `bool` | `true` when the fix was applied successfully. |


## Skeletal mesh helpers

### `GetBodyAndFaceSkeletalMeshComponents`

Type: `BlueprintCallable` (has exec pins)\
Category: `Convai|Utilities`

Splits an actor's skeletal mesh components into a body mesh and a face mesh using bone-name heuristics. Useful for MetaHuman-style rigs where the face mesh is separate.

Detection rules:

- 0 skeletal mesh components: both outputs are `nullptr`.
- Exactly 1: that mesh becomes the body; face is `nullptr`.
- 2 or more: each candidate is scored against body tokens (`"pelvis"`, `"hand"`, `"neck"`, …) and face tokens (`"eye"`, `"jaw"`, `"brow"`, …). The highest-scoring mesh wins each slot. If no mesh scores for body, the first component is used. If no mesh scores for face, `FaceComponent` is `nullptr`.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `Actor` | Input | `AActor*` | The actor to inspect. |
| `BodyComponent` | Output | `USkeletalMeshComponent*` | The identified body mesh, or `nullptr`. |
| `FaceComponent` | Output | `USkeletalMeshComponent*` | The identified face mesh, or `nullptr`. |


## Diagnostic and platform nodes

| Node | Category | Type | Returns | Description |
|---|---|---|---|---|
| `GetPluginInfo` | `Convai\|Utilities` | `BlueprintPure` | `Found (bool)`, `VersionName`, `EngineVersion`, `FriendlyName` (`FString` each) | Returns metadata for the named plugin. Input: `PluginName (FString)`. |
| `GetPlatformInfo` | `Convai\|Utilities` | `BlueprintPure` | `EngineVersion (FString)`, `PlatformName (FString)` | Returns the running engine version string and platform name. |
| `GetDeviceUniqueIdentifier` | `Convai\|Utilities` | `BlueprintPure` | `FString` | Returns a platform-level unique device identifier. |
| `GetStreamURL` | `Convai\|Utilities` | `BlueprintPure` | `FString` | Returns the resolved stream URL from settings. |
| `GetLLMProvider` | `Convai\|Utilities` | `BlueprintPure` | `FString` | Returns the configured LLM provider identifier. |
| `GetConnectionType` | `Convai\|Utilities` | `BlueprintPure` | `FString` | Returns the configured connection type string. |
| `GetEmotionsProvider` | `Convai\|Utilities` | `BlueprintPure` | `FString` | Returns the configured emotions provider identifier. |
| `IsAECEnabled` | `Convai\|Utilities` | `BlueprintPure` | `bool` | `true` when acoustic echo cancellation is enabled in settings. |
| `GetAECType` | `Convai\|Utilities` | `BlueprintPure` | `FString` | Returns the AEC type string from settings. |
| `IsVADEnabled` | `Convai\|Utilities` | `BlueprintPure` | `bool` | `true` when voice activity detection is enabled in settings. |
| `GetVADMode` | `Convai\|Utilities` | `BlueprintPure` | `int32` | Returns the VAD aggressiveness mode (0–3). |
| `IsNoiseSuppressionEnabled` | `Convai\|Utilities` | `BlueprintPure` | `bool` | `true` when noise suppression is enabled in settings. |
| `IsGainControlEnabled` | `Convai\|Utilities` | `BlueprintPure` | `bool` | `true` when automatic gain control is enabled in settings. |
| `IsHighPassFilterEnabled` | `Convai\|Utilities` | `BlueprintPure` | `bool` | `true` when the high-pass audio filter is enabled in settings. |
| `IsFaceSyncSimulateFreeze` | `Convai\|Utilities` | `BlueprintPure` | `bool` | `true` when the FaceSync freeze-simulation debug mode is enabled. |
| `GetLipSyncMode` | `Convai\|Utilities` | `BlueprintPure` | `EC_LipSyncMode` | Returns the configured lip sync mode. |
| `GetLipSyncTimeOffset` | `Convai\|Utilities` | `BlueprintPure` | `double` | Returns the lip sync time offset in seconds. |
| `GetLipSyncAnimParamOverride` | `Convai\|Utilities` | `BlueprintPure` | `FString` | Returns the lip sync anim param override string for the given `Key`. |
| `GetLipSyncStarvationFallback` | `Convai\|Utilities` | `BlueprintPure` | `float` | Returns the starvation fallback duration in seconds for the lip sync pipeline. |
| `GetConnectionProxyTTL` | `Convai\|Utilities` | `BlueprintPure` | `float` | Returns the connection proxy time-to-live in seconds. |
| `GetPrepConnectionTTL` | `Convai\|Utilities` | `BlueprintPure` | `float` | Returns the pre-prepared connection time-to-live in seconds. |
| `GetObjectPollIntervalSeconds` | `Convai\|Utilities` | `BlueprintPure` | `float` | Returns the interval in seconds between object component poll ticks. |
| `GetClientReadyRetrySecs` | `Convai\|Utilities` | `BlueprintPure` | `float` | Returns the retry interval in seconds used while waiting for the client-ready signal. |
| `GetClientReadyTimeoutSecs` | `Convai\|Utilities` | `BlueprintPure` | `float` | Returns the timeout in seconds for the client-ready handshake. |
| `GetContextDebounceWindowDefault` | `Convai\|Utilities` | `BlueprintPure` | `float` | Returns the default debounce window duration in seconds for context updates. |
| `GetContextMaxDebounceWindowDefault` | `Convai\|Utilities` | `BlueprintPure` | `float` | Returns the maximum debounce window duration in seconds for context updates. |

`EC_LipSyncMode` values:

| Enum value | Display name |
|---|---|
| `Off` | Off |
| `Auto` | Auto |
| `VisemeBased` | Viseme Based |
| `BS_MHA` | MetaHuman Blendshapes |
| `BS_ARKit` | ARKit Blendshapes |
| `BS_CC4_Extended` | CC4 Extended Blendshapes |


## Command-line utilities

`UCommandLineUtils` is a second Blueprint function library in the same module. Its nodes appear in the **CommandLine** category. Use these nodes to read command-line argument values at runtime for debug overrides and test automation without recompiling.

| Node | Type | Returns | Description |
|---|---|---|---|
| `GetCommandLineFlagValueAsInt` | `BlueprintCallable` | `int32` | Returns the integer value of `Flag` from the command line. Returns `DefaultValue` (default `0`) when the flag is absent. |
| `GetCommandLineFlagValueAsString` | `BlueprintCallable` | `FString` | Returns the string value of `Flag`. Returns `DefaultValue` (default `""`) when the flag is absent. |
| `GetCommandLineFlagValueAsStringNoDefault` | `BlueprintCallable`, `BlueprintPure` | `FString` | Returns the string value of `Flag` with no default parameter. |
| `GetCommandLineFlagValueAsDouble` | `BlueprintCallable`, `BlueprintPure` | `double` | Returns the double value of `Flag`. Returns `DefaultValue` (default `0.0`) when the flag is absent. |


## Connection management

`UConvaiConnectionLibrary` is a Blueprint function library that exposes connection pre-warming. Its node appears in the **Convai|Connection** category and does not need to be attached to an Actor.

### `PrepareCharacterConnection`

Category: `Convai|Connection` — `BlueprintCallable`

Starts a warm Convai session for `CharacterID` with no owner. A later `StartSession` call for the same character reuses this pre-warmed connection without a fresh handshake, reducing first-connect latency.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `WorldContextObject` | Input | `UObject*` | World context (auto-wired in Blueprint). |
| `CharacterID` | Input | `FString` | The character ID to pre-warm. |
| `PrepTTLOverrideSeconds` | Input | `float` | Duration of the warm window in seconds. Pass `0` or a negative value to use the project default (`GetPrepConnectionTTL`). Positive values are clamped to [1, 600]. |
| `Return value` | Output | `EC_PrepResult` | Outcome of the prep request — `Accepted`, `AlreadyWarm`, `Rejected`, `InvalidInput`, `Disabled`, or `InternalError`. See [Data types and enums](data-types-and-enums.md) for value descriptions. |

## Blueprint usage patterns

### Pre-warming a character connection on level load

In your level Blueprint's **BeginPlay** event, call `PrepareCharacterConnection` with the target character's ID. Leave `PrepTTLOverrideSeconds` at `0` to use the project default. Connect a **Switch on EC_PrepResult** node to log or discard the result. The warm session persists until its TTL expires; when the player triggers conversation and the chatbot calls `StartSession`, the handshake completes in one round-trip instead of two.

### Remapping blendshapes with `MapBlendshapes`

Call `MapBlendshapes` with the raw blendshape map from `ConvaiGetFaceBlendshapes` on the chatbot component reference and a `BlendshapeMap` data-table asset that defines per-blendshape multipliers, offsets, and target rig names. Feed the return value into **Apply Morph Target** or your mesh driver. Adjust `GlobalMultiplier` to scale all blendshapes at once during runtime tuning without rebuilding the mapping asset.

## Troubleshooting

### `GetBodyAndFaceSkeletalMeshComponents` returns `nullptr` for body or face

**Cause:** The scoring heuristic matches against standard bone-name tokens (`"pelvis"`, `"hand"`, `"neck"`, `"eye"`, `"jaw"`, `"brow"`, …). Custom skeletons with non-standard names — for example `"Root_Spine"` instead of `"pelvis"` — score zero and the fallback rule applies: body defaults to the first skeletal mesh component, face returns `nullptr`.

**Fix:** After calling `GetBodyAndFaceSkeletalMeshComponents`, null-check both outputs. When face is missing, retrieve skeletal mesh components directly with **Get Components by Class** and assign them manually.

**Verify:** In PIE, call `GetBodyAndFaceSkeletalMeshComponents` and print both output display names — the printed names confirm which mesh won each scoring slot.

## Related reference

The chatbot component is the primary consumer of the blendshape and look-at utility nodes; the player component uses the component-lookup and microphone helpers.

{% content-ref url="convai-chatbot-component.md" %}
[Convai Chatbot Component](convai-chatbot-component.md)
{% endcontent-ref %}

{% content-ref url="convai-player-component.md" %}
[Convai Player Component](convai-player-component.md)
{% endcontent-ref %}

