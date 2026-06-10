---
title: Convai utility functions
description: Find cross-cutting Blueprint helper nodes for look-at queries, component lookup, audio utilities, settings, diagnostics, and command-line flags.
last_reviewed: "4.0.0-beta.21"
---

`UConvaiUtils` is a `UBlueprintFunctionLibrary` that exposes miscellaneous helper nodes to Blueprint. It does not need to be attached to an `Actor`; all nodes are callable from any Blueprint graph. Nodes are grouped in the **Convai** category tree in the Blueprint node search palette.

This page documents cross-cutting utility libraries only. Feature-specific Blueprint libraries are documented in their feature reference pages:

| Library / surface | Documented in |
|---|---|
| `UConvaiActions` (action parameter accessors) | [Actions Blueprint reference](../features/character-actions/actions-blueprint-reference.md) |
| Dynamic context transport helpers | [Dynamic context Blueprint reference](../features/dynamic-context/dynamic-context-blueprint-reference.md) |
| Emotion helpers beyond `UConvaiChatbotComponent` | [Emotion Blueprint reference](../features/emotion/emotion-blueprint-reference.md) |
| LTM speaker and identity helpers | [LTM Blueprint reference](../features/long-term-memory/ltm-blueprint-reference.md) |
| Gaze highlight widgets and actors | [Gaze attention reference](../features/gaze-attention/gaze-attention-reference.md) |

## Look-at helpers

These nodes evaluate registered Convai components near the player controller's camera and return a candidate inside the configured radius and camera forward-angle threshold.

### `ConvaiGetLookedAtCharacter`

Category: `Convai|Utilities`

Returns the `UConvaiChatbotComponent` on the character the player is currently looking at.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `WorldContextObject` | Input | `UObject*` | World context (auto-wired in Blueprint). |
| `PlayerController` | Input | `APlayerController*` | The controller whose camera orientation is used for the look direction. |
| `Radius` | Input | `float` | Search radius in world units from the camera location. |
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
| `bOnlyConnected` | Input | `bool` | When `true`, only returns players whose session state is `Connected`. |
| `ConvaiPlayerComponents` | Output | `TArray<UConvaiPlayerComponent*>` | All matching player components. |
| `OutOwners` | Output | `TArray<AActor*>` | Owning actors in the same order as `ConvaiPlayerComponents`. |

### `GetFirstConvaiPlayerComponent`

Category: `Convai|Utilities`

Returns the first `UConvaiPlayerComponent` found in the world.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `WorldContextObject` | Input | `UObject*` | World context (auto-wired in Blueprint). |
| `bOnlyConnected` | Input | `bool` | When `true`, only considers players whose session state is `Connected`. |
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
| `GetClientVersion` | `Convai\|Settings` | `BlueprintPure` | Returns the `ClientVersion` value resolved via the `CustomPrams` / command-line resolve chain. Return: `FString`. |
| `GetVADSettings` | `Convai\|Settings` | `BlueprintPure` | Returns a snapshot of the current `FConvaiVADSettings` from project settings. |
| `SetVADSettings` | `Convai\|Settings` | `BlueprintCallable` | Overwrites the VAD settings on the active `UConvaiSettings` instance. Persisted to `.ini` on save. Input: `InSettings (FConvaiVADSettings)`. |
| `IsAlwaysAllowVisionEnabled` | `Convai\|Settings` | `BlueprintPure` | Returns `true` when the Always Allow Vision setting is enabled. |

`FConvaiVADSettings` field descriptions (`bUseServerDefault`, `Confidence`, `StartSecs`, `StopSecs`, `MinVolume`) are in [Data types and enums](data-types-and-enums.md).

## Audio helpers

### `StereoToMono`

Category: `Convai|Utilities`

Converts stereo WAV bytes and writes the converted mono WAV bytes to the output pin.

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

`FConvaiBlendshapeParameters` field descriptions are in [Data types and enums](data-types-and-enums.md).

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


## Skeletal mesh helpers

### `GetBodyAndFaceSkeletalMeshComponents`

Type: `BlueprintCallable` (has exec pins)\
Category: `Convai|Utilities`

Splits an actor's skeletal mesh components into a body mesh and a face mesh using bone-name heuristics. Useful for MetaHuman-style rigs where the face mesh is separate.

Detection rules:

- 0 skeletal mesh components: both outputs are `nullptr`.
- Exactly 1: that mesh becomes the body; face is `nullptr`.
- 2 or more: each candidate is scored against body tokens (`"pelvis"`, `"hand"`, `"neck"`, …) and face tokens (`"eye"`, `"jaw"`, `"brow"`, …). The highest-scoring mesh wins each slot. If no mesh scores for body, the shallowest skeletal mesh wins; `SkelMeshes[0]` is used only if no candidate is ranked. If no mesh scores for face, `FaceComponent` is `nullptr`.

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

`EC_LipSyncMode` values are documented in [Data types and enums](data-types-and-enums.md).


## Command-line utilities

`UCommandLineUtils` is a second Blueprint function library in the same module. Its nodes appear in the **CommandLine** category. Use these nodes to read command-line argument values at runtime for debug overrides and test automation without recompiling.

| Node | Type | Returns | Description |
|---|---|---|---|
| `GetCommandLineFlagValueAsInt` | `BlueprintCallable` | `int32` | Returns the integer value of `Flag` from the command line. Returns `DefaultValue` (default `0`) when the flag is absent. |
| `GetCommandLineFlagValueAsString` | `BlueprintCallable` | `FString` | Returns the string value of `Flag`. Returns `DefaultValue` (default `""`) when the flag is absent. |
| `GetCommandLineFlagValueAsStringNoDefault` | `BlueprintCallable`, `BlueprintPure` | `FString` | Returns the string value of `Flag` with no default parameter. |
| `GetCommandLineFlagValueAsDouble` | `BlueprintCallable`, `BlueprintPure` | `double` | Returns the double value of `Flag`. Returns `DefaultValue` (default `0.0`) when the flag is absent. |


## Connection management

`UConvaiConnectionLibrary` exposes the `PrepareCharacterConnection` Blueprint node in the `Convai|Connection` category. It pre-warms a character connection for later reuse by `StartSession`; see [Session lifecycle](../core-concepts/session-lifecycle.md) for the connection workflow, and [Data types and enums](data-types-and-enums.md) for `EC_PrepResult` values.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `WorldContextObject` | Input | `UObject*` | World context (auto-wired in Blueprint). |
| `CharacterID` | Input | `FString` | Character ID to pre-warm. |
| `PrepTTLOverrideSeconds` | Input | `float` | Optional warm-window duration. Default `0.0` uses the project setting; positive values are clamped to `1`–`600` seconds. |
| `Return value` | Output | `EC_PrepResult` | Result of the pre-warm request. |

## Related reference

The chatbot component is the primary consumer of the blendshape and look-at utility nodes; the player component uses the component-lookup and microphone helpers.

{% content-ref url="convai-chatbot-component.md" %}
[Convai Chatbot Component](convai-chatbot-component.md)
{% endcontent-ref %}

{% content-ref url="convai-player-component.md" %}
[Convai Player Component](convai-player-component.md)
{% endcontent-ref %}

