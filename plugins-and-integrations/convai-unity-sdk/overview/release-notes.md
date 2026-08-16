---
title: Release notes
description: >-
  Release notes for the Convai Unity SDK — current version highlights,
  previous release notes, bug fixes, and migration guidance for each release.
last_reviewed: "4.5.0"
---

Track changes to the Convai Unity SDK across releases, including new features, bug fixes, and configuration changes. The current release is <code class="expression">space.vars.unity_sdk_version</code>.

{% updates format="full" %}
{% update date="2026-08-14" tags="v4.5.0,Current" %}
## v4.5.0

**Character embodiment**

Five behavior modules now share one component family under **Add Component > Convai > Embodiment**, and each module reads the same dialogue state.

* **Convai Gaze** (`ConvaiGazeController`) replaces the previous Gaze implementation and the Attention module. It decides what the character looks at and performs the look in one component: eye-contact styles (`Natural`, `Speaking Focus`, `Conversation Lock`, `Always Lock`), `ConvaiGazeTarget` for scene objects with priority tier and aim offset, `PlayerAttentionSensor` for "is the player looking at me", a whole-body look-sharing ladder from eyes to head to chest to feet, and an XR eye-tracking extension point through `IPlayerGazeRaySource`
* **Convai Body Animation** (`ConvaiBodyAnimationController`) replaces Dialogue Animation. It builds its own layered `PlayableGraph` in code, so there is no Animator Controller asset to author. It covers idle and talk variants, co-speech gestures, target-aimed gestures, and NavMesh-synced walking with directional starts, planted stops, and turns in place. Animation clips and `ConvaiBodyAnimationSet_Female` ship with the module
* **Convai Body Language** (`ConvaiBodyLanguageController`) is new: breathing, weight shifts, sway, posture pulses, speech-timed head beats, listening lean-in, idle fidget, and startle or amused reactions. It layers on top of the Animator without owning a clip and needs no imported content
* **Emotion** gained semantic expression recipes that resolve onto ARKit, Reallusion CC3 and CC4, and MetaHuman rigs with no per-character authoring, plus resting mood, mood drift, a micro-expression idle layer, and shader-property output. `ConvaiEmotionController.SetMood(label, intensity, transitionSeconds)` and `ClearMood(transitionSeconds)` control mood at runtime, and `DominantEmotionChanged` and `MoodChanged` report resolved expression. Four personalities ship: Composed, Warm, Energetic, and Reserved
* **Conversation flow** supplies the dialogue state the other four modules read

**Character Actions**

* The **Actions Editor** window (**Convai > Actions Editor**) adds reusable Action Sets, Scene Knowledge, Character Settings, and a Live mode with batch progress, timeline, target registry, and per-action insights. The **Try It** box previews an action in Edit mode and dispatches it in Play mode
* Four built-in executors are new: Lead Player To Target, Scan Environment, Count Target Group, and Measure Distance
* `ConvaiActionExecutionResult.Answered("…")` lets an action supply a sentence the character can speak, separate from the diagnostic `Message`. **When It Finishes** authors this per action
* `ConvaiActionFailureReason` reports a typed failure cause on `ConvaiActionExecutionResult` and `ConvaiActionStepReport`. `ConvaiActionParameterValue.Presence` distinguishes an unfilled slot from a blank one. `ConvaiActionDispatcher` exposes `IsBusy`, `PendingBatchCount`, and `CurrentActionName`
* `ConvaiActionExecutorBase`, `ConvaiTargetedActionExecutor`, and `ConvaiCharacterActionExecutor<TPeer>` are the base classes for custom behaviors. `ConvaiPlayerBody` is now public, and `ConvaiActionExecutorBase.ResolvePlayer()` is `virtual`, so first-person rigs that move a child capsule resolve to the player's real position
* Wire parsing was corrected across a large set of dropped and garbled command cases, and a scene-placed `ConvaiActionTarget` is now synced to Convai mid-session

**Authentication**

* Authentication is now a project-level choice between API Key mode and Auth Token mode. Auth Token mode resolves a fresh short-lived credential from a configured endpoint or an `IConvaiAuthTokenProvider` before each room connection, works on Native and WebGL transports, sends the credential in the `API-AUTH-TOKEN` header, and strips the saved account API key from player builds while keeping it for Editor tooling
* `ConvaiManager.ConnectWithAuthTokenAsync` is a one-shot connect for projects whose login layer already holds a Convai auth token. It also supplies `end_user_id` and `end_user_metadata.name` without a registered provider or a configured endpoint

**Session lifecycle**

Idle-warning and idle-deadline events, `ResetIdleTimer` and `ExtendIdleTimeout`, and explicit pause, resume, and reconnect controls are available at runtime. Background behavior is set through the `ContinueAudibly`, `PauseTimeline`, and `MuteButCatchUp` policies, with an observable WebGL fallback from `PauseTimeline` to `MuteButCatchUp`.

**Editor tooling**

* **Convai > Troubleshooter** reports every Convai capability per character as set up, blocked, or set up but inert, with one-click fixes and a **Fix All** action. Extend it with `IConvaiSetupHealthProvider` and `ConvaiSetupHealthRegistry.Register`
* The **Convai** menu was reduced from 17 rows to 9 — see Breaking changes and migration below
* Every Convai inspector and window moved to a shared editor design system, and the Character Rig inspector was rewritten to lead with a Ready or Needs Attention verdict and banded detection confidence
* Opening a package-shipped settings asset is read-only and offers **Create A Project Copy**, which lands the copy under `Assets/Convai/`

**Requirements and dependencies**

The minimum Unity version is `6000.0.80f1`. The package adds three dependencies: `com.unity.ai.navigation`, `com.unity.collections`, and `com.unity.modules.xr`.

**LipSync, samples, and platforms**

* The Lip Sync Sample ships Sofia, a Reallusion CC4 character, in place of Camila
* Built-in viseme maps and lip sync profiles moved from `SamplesShared/Resources/` into the LipSync module and are constructed in code. Project registries under `Resources/LipSync/ProfileRegistries/` are still discovered and still win
* `ConvaiLipSyncSpeechEnergyAdapter` never sampled, so every feature reading speech energy read a flat signal. It now joins the character tick and samples each frame
* The package ships `ConvaiSampleFirstPersonController` and `ConvaiSampleFirstPersonInputs`, a renamed copy of Unity's Starter Assets first-person controller
* Meta Quest push-to-talk release now reads the A, B, X, and Y buttons through Unity's XR input API, and a controller read failure or disconnect fails closed so microphone capture cannot stay open
* The Quest Vision Frame Source has a designed inspector with live capture readout. Vision component foldout states reset once on upgrade

**Breaking changes and migration**

* **Unity 6000.0.80f1 is the minimum editor version.** There is no supported configuration below this floor. Upgrade the editor before upgrading the package
* **Three modules were retired, each with a successor.** Attention is replaced by Convai Gaze, Dialogue Animation by Convai Body Animation, and the facial clip system by the Emotion module's micro-expression layer. Their assemblies, profile assets, and preset slots were removed with them
* **Migrating from Attention or the previous Gaze components:** replace `ConvaiAttentionController`, `ConvaiGazeCoordinator`, `ConvaiHeadLookActuator`, and `ConvaiEyeGazeActuator` with a single `ConvaiGazeController` (**Add Component > Convai > Embodiment > Gaze**). Delete your `ConvaiAttentionProfile`, `ConvaiGazeCoordinationProfile`, `ConvaiGazeEyeProfile`, and `ConvaiGazeHeadProfile` assets — those types are gone and the assets will not deserialize. Tuning values do not carry over; re-tune on a `ConvaiGazeProfile`, or assign none and start from the defaults. Replace a custom `IFocusTargetProvider` or `IGazeIntentProvider` with `IGazeTargetProvider` registered through `RegisterTargetProvider`, `ConvaiAttentionDynamicContextBridge` with `GazeDynamicContextBridge`, and `ConvaiWorldObjectFocusProvider` with `ConvaiGazeTarget`. Replace `ConvaiWorldObjectFocusProvider` before you save the affected scenes, because Unity strips the removed component silently on the next save
* **Migrating from Dialogue Animation:** replace `ConvaiDialogueAnimationController` with `ConvaiBodyAnimationController`, move clips from a `DialogueAnimationLibrary` into a `ConvaiBodyAnimationSet`, and move timing and weight tuning into a `ConvaiBodyAnimationConfig`. Delete the `DialogueAnimatorContract` asset, its four Animator layers, the ping-pong states, and the `ConvaiDialogueSlot_*` placeholder clips; an Animator Controller left in place fights the graph for the same bones. Per-clip gender filtering (`CharacterGender`) and per-clip emotion affinity tags (`DialogueEmotionAffinity`) have no field-level migration — author one set per character type instead of filtering a mixed set at runtime. `AnimationRiggingGazeBridge` is gone, and Convai Gaze needs no rigging package
* **Migrating from facial clips:** delete `ConvaiFacialClipPlayer`, `ConvaiFacialClipRuntimePlayer`, and their profile assets, and let the Emotion module's micro-expression layer produce idle facial life — it is on by default and nothing needs porting. A deliberate authored facial performance has no supported replacement in this release; drive the mesh yourself with `SkinnedMeshRenderer.SetBlendShapeWeight` on a mesh no Convai module composes. Bake your clips into your own asset before upgrading, because `ConvaiFacialAnimationProfile` assets will not deserialize once the module is gone
* **The Convai editor menu was restructured.** **Convai > Welcome**, **Convai > Account**, **Convai > Long Term Memory**, **Convai > Updates**, **Convai > Contact Us**, and **Convai > AI Coding Setup** are gone; those sections live one click further in, inside the window that **Convai > Convai Editor** opens. The nine current rows group into three bands: the Convai Editor window and its settings — **Convai > Convai Editor**, **Convai > Settings**, **Convai > Documentation**; the per-feature authoring editors — **Convai > Actions Editor**, **Convai > Body Animation Editor**, **Convai > Emotion Editor**, **Convai > Gaze Editor**, **Convai > Embodiment Editor**; and diagnostics — **Convai > Troubleshooter**. The `ConvaiConfigurationWindowEditor` methods that opened a section directly are still public
* **`UnityEventActionExecutor` was renamed to `ConvaiUnityEventActionExecutor` and carries a new GUID.** Unity does not migrate the component: it is dropped from every scene and prefab that had one, along with the events wired into it, and no upgrade step recovers them. Record what each event called before you upgrade. Afterwards, add `ConvaiUnityEventActionExecutor` (**Add Component > Convai > Actions > Raise Unity Event**) on each affected object, re-wire its event by hand, and re-point any action bound to the old component. The serialized field is still `_onExecute`
* **Three experimental action executors were removed from the public catalog:** Guided Tour, Address The Group, and Perform Gesture At Target. `LookAtTargetActionExecutor` was also removed — add `ConvaiLookAtActionExecutor` (**Add Component > Convai > Actions > Look At Target**) instead and give the character Gaze, since the replacement works through `ConvaiGazeController`. Six sample action behaviors, `ConvaiActionTestSetup`, and `ConvaiActionDebugWindow` were removed; the Actions Editor covers their work
* **Point At Target's `Hold Seconds` means only the mid-gesture pause**, not the length of the whole gesture. Two settings now reach the pointing layer: **Gesture Speed** multiplies the rise and fall, and **Release** set to `Blend` drops the pose when the hold ends. Both default to the previous behavior, so no existing scene changes; a point of about a second is Gesture Speed `1.5` with Release `Blend`
* **Fourteen editor types are now `internal`,** among them `ConvaiVisionBaseEditor`, `ConvaiCharacterEditor`, and `TurnTakingOptionsDrawer`. Subclassing a Convai editor or property drawer is no longer supported and has no replacement extension point — delete the subclass, and add project-specific controls through a separate `MonoBehaviour` of your own. `[CustomEditor]` registration is unaffected, so every Convai inspector draws as before
* **The Emotion module's slot-list facial output path was removed:** `EmotionSlotBinding`, `BlendshapeEmotionBinding`, `AnimatorParameterEmotionBinding`, `RealisticEmotionSlots`, `NeutralAlternator`, and the `SemanticExpressionsEnabled` and `NeutralAlternationEnabled` switches on `ConvaiEmotionProfile`. The runtime discarded this data whenever semantic expressions were on, which was every shipped profile, so nothing needs porting. Shader-property output is unaffected
* **The shared Emotion taxonomy and profile assets changed identity.** `ConvaiSamplesShared_EmotionTaxonomy.asset` was rebuilt and `ConvaiSamplesShared_EmotionProfile.asset` was replaced by the four named personalities. Open each affected character and re-point the taxonomy and the personality; a character with no taxonomy still runs, but every emotion dropdown comes up empty
* **Embodiment types were renamed, with asset GUIDs preserved:** `EmbodimentProfileReceiver<T>` to `ConvaiCharacterModule<T>`, `CharacterEmbodimentPreset` to `ConvaiEmbodimentPreset`, `EmbodimentPresetLibrary` to `ConvaiEmbodimentPresetLibrary`, and `ConvaiCharacterEmbodimentBinding` to `ConvaiEmbodimentPresetBinding`. Only source references need updating. `EmbodimentContext` replaced its per-seam registration members with one `CharacterServiceRegistry` — implement `IEmbodimentTickable` and call `EmbodimentContext.RegisterTickable(this)` from `OnEnable` to join the character tick. `EmbodimentContext.TryResolve` no longer creates a context on a GameObject that is not a Convai character; call `TryResolveFor` for a diagnosable failure
* **`ActionResponsePayload` and the public `UnityObjectCompatibility` class were removed.** Action commands still arrive through `ConvaiCharacter.OnActionsReceived` and `ConvaiManager.Events.OnCharacterActionReceived`. Replace `UnityObjectCompatibility.FindObjectsByType<T>(mode)` with Unity's `Object.FindObjectsByType<T>`, and `UnityObjectCompatibility.GetId(value)` with `value.GetInstanceID()` up to Unity 6000.4 or `value.GetEntityId()` on 6000.2 and newer
* **The Camila sample character was removed.** A scene or prefab referencing her prefab, materials, or textures reports a missing reference. Sofia uses the same blendshape convention, so a Convai setup transfers. Copy any customized Camila assets out of the package before upgrading
{% endupdate %}

{% update date="2026-07-30" tags="v4.4.1" %}
## v4.4.1

**Fixes**

* Added Unity 6.0 through 6.5+ compatibility paths for object IDs and object searches. Unity 6.4 and newer use 64-bit `EntityId` and no-sort search APIs, while Unity 6.0 through 6.3 retain legacy fallbacks
* Fixed Unity 6.0 project resolution by removing unavailable pseudo-module dependencies and pinning `com.unity.collections` to `2.6.8`, avoiding the known Collections `2.6.7` and AI Assistant `xxHash3`/`Unsafe` compiler regression
* Kept the LipSync sample background light isolated on Unity 6.0 and 6.4+ by aligning both URP rendering-layer serialization formats, preventing the light from overexposing the sample character
* Push-to-talk release now keeps the microphone and speech recognition open while waiting for the final transcription result. When the configurable `PushToTalkPolicy.ReleaseTailMs` window expires, the SDK signals the authoritative stop and allows one more bounded window before closing capture
* Fixed WebGL builds crashing from a stale `NativeLib` reference in `livekit-bridge.jslib`, and restored first-turn LipSync by correcting audio-timing registration order, warming the WebGL analyser, and recovering missed `PlaybackStarted` callbacks
{% endupdate %}

{% update date="2026-07-21" tags="v4.4.0" %}
## v4.4.0

**Canonical transcript timeline**

`ConvaiManager.Transcripts` now exposes a room-scoped `TranscriptTimeline` built from immutable `TranscriptTurn` and `TranscriptChange` models, replacing the previous snapshot-based contract. `CurrentTimeline` returns `TranscriptTimeline` instead of a timeline snapshot, `Changed` supplies `TranscriptChangeBatch`, and `Subscribe`/`SubscribeCommitted` callbacks receive `TranscriptChange` values. This is a breaking change for any code that consumed the old snapshot types — see the [Transcript API](../scripting-reference/transcript-api.md) reference for the full migration path.

**Character Actions**

* `ConvaiActionConfigPatch` updates a character's actions, character targets, object targets, and current attention object during an active session, with omitted-versus-empty list semantics and generated update IDs
* `ConvaiActionDefinition.WaitForBotSpeech` (mirrored on `ConvaiActionCommand`) makes the first action of a fresh batch wait for character speech before executing, with an optional `DelayAfterBotSpeechSeconds` pause and a dispatcher-level speech gate timeout so a silent turn never stalls the batch

**AI Coding Assistant integration**

**Convai > AI Coding Setup** opens a new Editor section for configuring Unity MCP-based AI coding assistance, with support for Codex, Claude Code, Cursor, Gemini, and VS Code Copilot. A dedicated documentation section covers this integration in full.

**Dynamic Vision Context**

Rooms can opt into backend frame sampling through a new Dynamic Vision Context section on `ConvaiRoomManager` and `ConvaiRoomManagerProfile`.

**Convai SDK Settings**

The **Convai SDK** Project Settings page (**Edit > Project Settings > Convai SDK**) and the Editor window's new **Convai > Settings** section share one implementation, covering Setup Health, Credentials, Runtime Defaults, Diagnostics, Advanced, and About. Credentials adds API key obfuscation with automatic migration from plaintext, an Environment preset (Production, Beta, or Custom), and a Validate & Save action with a cached validation badge.

**LipSync**

Playback-alignment hardening anchors NeuroSync lipsync to the exact audio frame where speech starts, reducing drift on long or interrupted responses.

**Breaking changes**

* `ConvaiSettings.DefaultMicrophoneIndex` was replaced by `DefaultMicrophoneDeviceId` (string) — the integer index is not migrated; re-pick the microphone in Settings > Runtime Defaults
* `ConvaiSettings.ServerUrl` is now derived from the Environment preset — the serialized URL applies only when the environment is `Custom`
* The **Convai > Logger Settings** menu was removed — logging configuration lives in **Convai > Settings** (Diagnostics)
* `ConvaiRespondMode` unifies the respond-mode vocabulary (`ConvaiContextReactionMode` removed) — only relevant to scenes saved against unreleased beta builds
{% endupdate %}

{% update date="2026-06-23" tags="v4.3.0" %}
## v4.3.0

* **VAD settings:** Configurable connect-time user voice activity detection (VAD) settings for room connections, with room and profile Inspector controls and server-default handling
* **Dynamic context v2:** Consolidated dynamic context flow with tracked state and events, batching, acknowledgement/result events, and the `ConvaiDynamicContextRelay` authoring surface
* **World-object context:** Synced world-object context sends tracked scene metadata and the current focus object through dynamic context
* **Narrative triggers:** Separate trigger modes for saved triggers, inline events, and scripted speech
* **Transcript UI:** World-space chat transcript prefab for spatial UI setups
* **Actions:** Action configuration validation and duplicate-binding preservation, with step diagnostics and action debug probing
* **Chat input:** Enter-to-focus behavior for chat input

**Migration notes**

* Dynamic context now uses the v2 tracked update flow — prefer `ConvaiCharacter.DynamicContext` or `ConvaiDynamicContextRelay` over the removed command-style dynamic context UI
* Narrative trigger requests now carry an explicit mode — use saved triggers, inline events, or scripted speech according to the desired backend behavior
* Custom VAD values are sent only during room connect — use the server-default option when the backend should own VAD defaults
{% endupdate %}

{% update date="2026-05-08" tags="v4.2.0" %}
## v4.2.0

**Actions System**

Characters can execute in-scene commands through a structured runtime. New in this release:

* `ConvaiActionDispatcher` with queued dispatch — actions execute in sequence without race conditions
* `IConvaiActionExecutor` interface for custom executors
* Six built-in executors: move-to (Transform and NavMesh), pick-up, look-at, Animator trigger, and UnityEvent
* Inspector-driven configuration — no scripting required for standard action setups
* Runtime diagnostics for monitoring action queue state

**Meta Quest Passthrough Vision**

`QuestVisionFrameSource` enables the Vision module on Quest 3 and Quest 3S devices without an external camera. Characters see through the device's passthrough camera during mixed reality sessions.

**Runtime Turn-Taking Mode Switching**

Switch between hands-free and push-to-talk modes during live sessions using `ConvaiManager.SetConversationInputModeAsync()` or the runtime Settings Panel — no scene reload required.

**Dynamic Context Expansion**

* Tracker APIs let you monitor current context state from scripts
* Inspector tooling for authoring context commands without code
* `SampleDynamicContextUI` prefab demonstrates runtime injection patterns

**Scene Setup Tooling and Validation**

Menu-driven component creation (**GameObject > Convai > Setup Required Components**) and scene validation (**GameObject > Convai > Validate Scene Setup**) prevent misconfiguration before entering Play mode.

**Settings Panel Input Mode Control**

The runtime Settings Panel now exposes input mode switching — players or developers can change turn-taking mode during a session without scripting.
{% endupdate %}

{% update date="2026-04-09" tags="v4.1.0" %}
## v4.1.0

* **Dynamic Context:** `ConvaiDynamicContextCommand` component enables runtime injection of state and events into character knowledge
* **LipSync sample:** Removed camera dependency from the LipSync sample scene — works with any camera setup
* **Vision module:** Reliability improvements to frame source lifecycle and reconnection handling
* **iOS:** Fixed crash on first microphone access when `NSMicrophoneUsageDescription` was absent from build settings
* **Sample scenes:** Refined setup and scene structure across Basic and LipSync samples
* **Editor:** Startup time improvements for projects with large scene counts
{% endupdate %}

{% update date="2026-03-12" tags="v4.0.0,Initial Release" %}
## v4.0.0

Initial public release of the Convai Unity SDK.

**Core components:** `ConvaiManager`, `ConvaiRoomManager`, `ConvaiCharacter`, `ConvaiPlayer`

**Conversation pipeline:** Speech-to-text, language understanding and generation, text-to-speech — fully streamed in real time

**Modules:** LipSync, Emotion, Vision, Narrative Design, Dynamic Context, Long-Term Memory, Scene Metadata, Dialogue Animation, Gaze and Attention

**Platform support:** Windows, macOS, Linux, Android, iOS, WebGL

**Editor tooling:** Scene setup, validation, Project Settings integration, and the Convai Welcome window
{% endupdate %}
{% endupdates %}

## Next steps

To start using the SDK, follow Getting Started.

{% content-ref url="../getting-started/README.md" %}
[Getting Started](../getting-started/README.md)
{% endcontent-ref %}
