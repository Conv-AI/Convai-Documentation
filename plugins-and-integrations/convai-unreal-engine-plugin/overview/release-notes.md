---
title: Release notes
description: Version history and notable changes for the Convai Unreal Engine plugin, covering all 4.x beta releases and the full 3.x history.
last_reviewed: "4.0.0-beta.21"
---

Track changes to the Convai Unreal Engine plugin across releases. The current release is <code class="expression">space.vars.unreal_plugin_version</code>, supporting Unreal Engine <code class="expression">space.vars.unreal_min_version</code> and later.

{% hint style="info" %}
This plugin is in beta. Beta releases may include breaking changes between minor versions. The plugin manifest identifies the current package as <code class="expression">space.vars.unreal_plugin_version</code>; the latest traceable source changelog entry is `4.0.0-beta.20`.
{% endhint %}

{% updates format="full" %}
{% update date="2026-05-25" tags="4.0.0-beta.20" %}
## 4.0.0-beta.20

**Animation and gestures**

* Overhauled the bundled MetaHuman animations.
* Added gesture and pointing animations triggered automatically from LLM-issued character actions.
* Added replicated `PointAtTarget` alongside `LookAtTarget` on the chatbot component.

**Object awareness and gaze**

* Added `UConvaiObjectComponent` for tagging actors and exposing their live properties as context to the chatbot.
* Added gaze-driven attention: the actor under the player's gaze becomes the object in attention, with a silhouette highlight and an on-screen cursor.
* Added proximity-driven state: object components report when they are reachable from a chatbot's pawn so the bot can react.

**Actions**

* Added "Create Convai Action Handler" right-click entry in Blueprint graphs for scaffolding typed action handlers.
* Added "Setup Convai Pawn Movement" content-browser action that seeds navigation defaults on any pawn Blueprint.
* Added component and socket targeting plus per-entry movement overrides for actions.
* Improved action completion: handlers can wait for bot speech to finish before the next action, post a dynamic-context event in the same call, and abort an unrecoverable sequence cleanly.
* Added fuzzy matching for enum and choice action parameters so minor LLM spelling drift no longer drops the action.
* Switched the action wire format to `{name}` braces with more reliable response parsing.
* Enabled actions on by default in the chatbot environment.

**Audio and lip sync**

* Added VAD (voice activity detection) parameters in project settings and the connect request.
* Improved tail-of-utterance audio handling to reduce clipping on soft trailing consonants.
* Improved lip-sync stability with a starvation fallback when frames briefly stop arriving.
* Fixed microphone hot-swap so switching device mid-session no longer requires restarting the stream.

**Other improvements**

* Added Convai auth caching so subsequent connects don't re-authenticate from scratch.
* Added `GetBodyAndFaceSkeletalMeshComponents` helper for resolving MetaHuman and CC5 rigs.

**Bug fixes and compatibility**

* Fixed Android crash on app shutdown.
* Fixed several UE 5.0 / 5.4 / 5.5 / 5.7 compilation and compatibility issues so the plugin builds clean across all supported engine versions.
* Disabled the Convai editor UI on UE 5.1 and earlier (the property-binding editor feature it relies on isn't available there).
* Regenerated the gaze-highlight material under UE 5.0 so the asset loads across all supported engine versions.
{% endupdate %}

{% update date="2026-05-01" tags="4.0.0-beta.19" %}
## 4.0.0-beta.19

* Actions integration with WebRTC: chatbot now sends `action_config` at connect when `bEnableActions` is on, and parses structured action-response payloads into typed action sequences.
* Refactored `Environment` from `UConvaiEnvironment` UObject to `FConvaiEnvironmentData` USTRUCT. Granular Add/Remove/Clear methods on the chatbot for Objects, Characters, and Actions; debounced scene-metadata flush; `bFlushImmediately` advanced opt-in for time-critical updates.
* Split legacy `MainCharacter` into `ConversationPartner` (replicated, scene-aware) and `LookAtTarget` (animation-only). New `bAutoFillConversationPartnerFromPlayer` toggle populates the partner from the first registered Convai Player component automatically.
* New `SetObjectInAttention` rides the dynamic-context flush and auto-registers the entry in `Environment.Objects` if missing.
* Added `bEnableActions` chatbot toggle. `Environment.Actions` seeded by default with `Move To`, `Follow`, `Stop Moving`, and `Wait For`.
* Actions V2 — typed action templates: `FConvaiAction` with structured `Parameters` typed via `EConvaiActionParamType`. Optional `Connector` for compound actions, `Choices` for fixed-list constraints, or `EnumType` to draw choices from a `UENUM`.
* Unified action-result shape: `FConvaiResultAction.Parameters` as `TMap<FString, FConvaiResultParam>`. Legacy `RelatedObjectOrCharacter` and `ConvaiExtraParams` kept as deprecated mirrors.
* New Blueprint-pure accessors: `Get First Param`, `Get Param`, `Get Param Type`, `Get Param As String/Number/Bool/Ref/Byte`, `Has Param`.
* `HandleActionCompletion` gains optional `AdditionalNote` and `ShouldRespond`. New `AbortActionSequence` accepts optional `EventText` and clears the queue without retrying.
* Removed the `EnableNewActionSystem` global toggle — the action queue path is now always on.
* Backward compatibility: legacy `UConvaiEnvironment` and `UConvaiActionContext` resurrected as deprecated shims so older Blueprint graphs keep compiling with deprecation warnings.
{% endupdate %}

{% update date="2026-04-24" tags="4.0.0-beta.18" %}
## 4.0.0-beta.18

* Added Android packaging support.
* Added dynamic context batching and logging for chatbot interactions to reduce redundant updates.
* Added starvation blending and playable frame checks for improved lip sync stability.
* Added command-line overrides for lip sync animation parameters and simulation freeze functionality.
* Added custom parameter handling and client version retrieval to `ConvaiUtils`.
* Added reset idle timer and user idle warning support.
* Enhanced component resolution in the FaceSync Animation Node to include the parent actor when searching for `UConvaiChatbotComponent`.
* Renamed `RunLLM` parameter to `ShouldRespond` for improved API clarity in context update methods.
* Updated lip-sync timing behavior for better audio/animation alignment. The current source default for `LipSyncTimeOffset` is `0.02` seconds (20 ms).
* Updated dynamic-context debounce behavior for improved batching consistency. The current source setting is `ContextDebounceWindow`, with a default of `0.5` seconds.
* Refactored narrative trigger handling to streamline context processing.
{% endupdate %}

{% update date="2026-04-13" tags="4.0.0-beta.17" %}
## 4.0.0-beta.17

* Optimized lip sync computational performance in MetaHuman Face Animation Blueprint.
* Improved audio playback time estimation and removed deprecated `FSoundSource` caching.
* Enhanced audio finish detection with tolerance to avoid floating-point rounding edge cases.
* Added performance timing statistics for audio streamer and face sync components in debug mode.
* Added detailed audio playback debug logging.
* Improved audio capture cleanup to ensure safe resource release during component destruction and end play.
* Fixed potential dangling references in async tasks by switching to weak pointers.
* Fixed re-entrant callbacks during Convai client disconnection.
* Fixed crash caused by cross-object delegate cleanup in `BeginDestroy` for chatbot and player components.
* Fixed player transcriptions not being appended properly.
* Added emotions provider plumbing.
* Fixed `ConvaiConnectionConfig` struct layout mismatch with DLLs.
{% endupdate %}

{% update date="2026-04-09" tags="4.0.0-beta.16" %}
## 4.0.0-beta.16

* Added Android support.
{% endupdate %}

{% update date="2026-04-05" tags="4.0.0-beta.15" %}
## 4.0.0-beta.15

* Fixed lip sync slow receival.
{% endupdate %}

{% update date="2026-03-31" tags="4.0.0-beta.14" %}
## 4.0.0-beta.14

* Added Update Context functionality.
* Updated `OutputFPS` to 60 for improved lip sync output.
* Improved lip sync audio handling and cleaned up unused variables.
* Improved audio playback time calculation accuracy and simplified play voice data flow.
{% endupdate %}

{% update date="2026-03-16" tags="4.0.0-beta.13" %}
## 4.0.0-beta.13

* Added connection indicator UI widget.
* Fixed attendee disconnect state notification handling.
* Fixed editor UI to show changelog only for installed plugin version.
* Improved connection manager reliability and state handling.
* Fixed audio not being sent when connection is in orphan state.
* Improved server event dispatching.
* Enhanced logging for better debugging.
{% endupdate %}

{% update date="2026-03-09" tags="4.0.0-beta.12" %}
## 4.0.0-beta.12

* Deprecated old `ConvaiBaseCharacter` and `ConvaiBasePlayer` Blueprint classes.
* Added connection indicator widget to show the connection state.
* Added LLM start/stop events (`OnLLMStarted`, `OnLLMStopped`) to `ConvaiChatbotComponent`.
* Added emotions support.
* Added toggle STT functionality.
* Improved lip sync at the end of response.
* Fixed lip sync desync corner case due to taking frames from previous response.
* Fixed PIE crash when recording audio at the same time as starting a new connection.
* Fixed minimum buffer duration updated to 0.2 seconds.
{% endupdate %}

{% update date="2026-02-19" tags="4.0.0-beta.11" %}
## 4.0.0-beta.11

* Improved compatibility with CC5 Reallusion characters.
{% endupdate %}

{% update date="2026-02-11" tags="4.0.0-beta.10" %}
## 4.0.0-beta.10

* Fixed DLL loading issue.
* Fixed crash in the Convai Dashboard.
* Added support for Blueprint-only projects.
{% endupdate %}

{% update date="2026-02-10" tags="4.0.0-beta.9" %}
## 4.0.0-beta.9

* Improved character interrupt handling.
* Improved lip sync accuracy.
* Added connection state functions to `ConvaiSubsystem` and `ConvaiChatbotComponent`.
{% endupdate %}

{% update date="2026-01-15" tags="4.0.0-beta.7" %}
## 4.0.0-beta.7

* Fixed corruption of some transcription characters.
{% endupdate %}

{% update date="2026-01-05" tags="4.0.0-beta.6" %}
## 4.0.0-beta.6

* Added ARKit blendshapes lip sync support.
* Updated default `LipSyncMode` to `BS_MHA` (MetaHuman) in `ConvaiFaceSyncComponent`.
* Added `RequiresPrecomputedFaceData` method to `ConvaiConnectionInterface`.
* Fixed blendshape selection logic to use ARKit names conditionally.
{% endupdate %}

{% update date="2025-12-20" tags="4.0.0-beta.5" %}
## 4.0.0-beta.5

* Updated `BlendShapesNames` to new naming convention for ARKit.
{% endupdate %}

{% update date="2025-12-05" tags="4.0.0-beta.4" %}
## 4.0.0-beta.4

* Implemented bulk NeuroSync blendshape handling with stats logging.
* Added audio frame tracking and improved voice handling in `ConvaiAudioStreamer` and `ConvaiChatbotComponent`.
* Added end user ID functionality and device unique ID support.
* Fixed voice playback overlap by stopping voice when audio starts.
* Added MetaHuman control names support.
* Fixed editor freezing issues.
* Fixed Linux library linking issues.
* Vision optimization improvements.
{% endupdate %}

{% update date="2025-11-20" tags="4.0.0-beta.3" %}
## 4.0.0-beta.3

* Added UE 5.7 support.
* Added Blueprint-only project support.
{% endupdate %}

{% update date="2025-11-05" tags="4.0.0-beta.2" %}
## 4.0.0-beta.2

* Added editor login screen and dashboard.
* Added better echo and noise cancellation.
* Added initial viseme-based lip sync support using the FaceSync component.
* Added gamma correction to vision.
* Fixed the F10 Settings menu.
{% endupdate %}

{% update date="2025-10-20" tags="4.0.0-beta.1" %}
## 4.0.0-beta.1

* Initial WebRTC integration.
{% endupdate %}
{% endupdates %}

---

## Version 3.x releases

<details>
<summary>3.6.x release history</summary>

**3.6.7-Beta**
- Added `UseSystemCertificates` option for SSL configuration on Windows.
- Fixed Convai logging not showing after packaging.
- Fixed multiplayer crash due to sending text data over non-game thread.

**3.6.6**
- Added `EnableSync` parameter for audio and lip sync synchronization control.

**3.6.5**
- Adjusted `MinBufferDuration` and `AudioLipSyncRatio` defaults to reduce audio stutters.

**3.6.4**
- Improved data validation in `ConvaiAudioStreamer` to prevent crashes from invalid input.
- Fixed `MinBufferDuration` not working as expected when lip sync is active.

**3.6.3**
- Improved memory management in `ConvaiGRPC`.

**3.6.2**
- Potential fix for missing audio for ElevenLabs and some Azure voices.
- Improved performance when receiving AI audio responses.

**3.6.1**
- Fixed headers for Linux build.

**3.6.0**
- UE 5.6 support.
- Optimized internal component registry lookups.
- Added Convai Logger.

</details>

<details>
<summary>3.5.x release history</summary>

**3.5.4-hotfix-1**
- Fixed racing condition when playing audio.
- Updated Android Play Core to 2.0.3.
- Refactored old unused classes and code.

**3.5.4**
- Further improved lip sync accuracy and synchronization.
- Fixed player speech transcription failing after short character responses.
- Improved gRPC connection stability to prevent conversation failures.
- Resolved a rare crash caused by the server sending large volumes of audio in small chunks.

**3.5.3-beta**
- Improved lip sync accuracy and synchronization.
- Fixed voice cutting off for ElevenLabs voices.
- Fixed Pixel Streaming compatibility.

**3.5.2**
- Fixed rare crash when new voice data starts to play while the character is finishing its current sentence.

**3.5.1**
- Added Long Term Memory V0.
- Fixed voice not being sent to clients on multiplayer.
- Added Dynamic Environment Info.

**3.5.0**
- UE 5.5 support.

</details>

<details>
<summary>3.4.x and earlier</summary>

**3.4.2-beta**
- Fixed player time-out warning message when using text.
- Increased gRPC connection robustness by adding small delays and read retries.

**3.4.1-beta**
- Fixed `IsListening()` not properly returning the character state.

**3.4.0-beta**
- Fixed multiple connection issues.
- Can now play custom montages over MetaHuman face animation.

**3.3.2**
- Added intermediate fix for audio being cut off in multiplayer.
- Added `ConvaiGetAvailableVoices` function.

**3.3.1**
- Fixed narrative keys not being set properly.
- Better lip synchronization using timestamps.
- Added `Convai Download Image using RPM link` function.
- Exposed Convai Player component for C++ use.

**3.3.0**
- Added Linux support.
- Fixed issue where an object similar to a character name would be picked up as the related object or character.

**3.2.2-Beta**
- Fixed NPC2NPC crash when interrupting the character early on.

**3.2.1-Beta**
- Fixed body gestures not animating while talking.
- Added Narrative Trigger Keys.
- Improved emotion animations for MetaHumans.

**3.2.0**
- Added UE 5.4 support.

**3.1.4**
- Added Pixel Streaming support and documentation.
- Added x86_64 Android support.
- Added Narrative Design helper functions.
- Added more Blueprint documentation.
- Improved action accuracy with objects and characters.
- Improved MetaHuman facial and body animation logic.
- Improved lip sync.
- Updated Reallusion Animation Blueprint.
- Fixed issue when adding custom MetaHuman animations.
- Fixed crash with UE 5.3 when there is a connection issue.
- Fixed multiplayer crash.
- Fixed rare crash when using Invoke Speech with bad connection.

**3.0.1 Hotfix**
- Fixed audio capture on Android sometimes not capturing properly.
- Fixed lip sync crash on Android and improved performance.
- Fixed rare crash on Android when a large amount of audio is spoken by the character.
- Improved overall audio capture.
- Fixed `Update Character` node not updating language.
- Updated Convai ReadyPlayerMe plugin for improved head tracking.
- Fixed lip sync not working when a player component and a chatbot component are in the same character Blueprint.
- Added documentation guide for Mac microphone permissions issue.
- Fixed startup crash for packaged apps on macOS UE 5.3 due to microphone permissions.

**3.0.0**

Added:
- New lip sync component `FaceSync`, which no longer requires the `ConvaiOVRLipsync` plugin.
- Mac lip sync support.
- Emotions.
- Object in Attention.
- New Convai Chatbot Component functions: `Invoke Speech`, `Invoke Narrative Design Trigger`, `Force Set Emotion`, `Reset Emotion State`, `Get Emotion Score`, `Get Talking Time Elapsed`, `Get Talking Time Remaining`, `Set Lipsync Component`, `Clear Action Queue`.
- New Convai Chatbot Component events: `On Narrative Section Received`, `On Emotion State Changed`.
- `ConvaiGetLookedAtObjectOrCharacter` function.
- Actor loses focus with player after predefined time.
- `Move To` and `Follow` action failures trigger a character response.
- Environment replication for multiplayer use cases.

Improved:
- MetaHuman body animations, facial expressions, and eye look-at.
- Reallusion Animation Blueprint, lip sync, and eye look-at.
- Settings widget UI.
- Actions accuracy.
- Audio capture for low frame rate.

Fixed:
- Packaging issue if Convai Player Component was in the scene prior to packaging.
- Crash when many interactions were happening simultaneously.
- `ConvaiBasePlayerWithVoiceActivation` Beta class was only working for the first interaction.
- Overall plugin stability and warnings.

Deprecated:
- `ConvaiOVRLipsync` plugin and component. Delete the plugin from your project and use the new `FaceSync` component instead.

</details>

## Next steps

{% content-ref url="../getting-started/" %}
[Getting started](../getting-started/)
{% endcontent-ref %}
