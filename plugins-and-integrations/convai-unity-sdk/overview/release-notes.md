---
title: Release notes
description: >-
  Release notes for the Convai Unity SDK — current version highlights,
  previous release notes, bug fixes, and migration guidance for each release.
last_reviewed: "4.4.0"
---

Track changes to the Convai Unity SDK across releases, including new features, bug fixes, and configuration changes.

{% updates format="full" %}
{% update date="2026-07-21" tags="v4.4.0,Current" %}
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
