---
title: Release notes
description: >-
  Release notes for the Convai Unity SDK — current version highlights,
  previous release notes, bug fixes, and migration guidance for each release.
---

Track changes to the Convai Unity SDK across releases, including new features, bug fixes, and configuration changes.

{% updates format="full" %}
{% update date="2026-06-10" tags="v4.2.0,Current" %}
## June 2026 SDK updates

**Session resume**

`ConvaiCharacter` now exposes `CharacterSessionId`, `SetCharacterSessionId()`, and `ClearCharacterSessionId()` so projects can explicitly control the next `character_session_id` used when **Session Resume** is enabled.

**Scene Metadata and Dynamic Context**

World objects can now define tracked properties on `ConvaiObjectMetadata`. The SDK seeds those values into `ConvaiCharacter.DynamicContext` and pushes runtime changes with state keys such as `Door.Status`.

**WebGL lip sync**

WebGL audio playback timing and lip-sync timing were improved. Intermittent drift can still occur in browser builds, so validate lip sync in the target browser before shipping.

**Samples**

The Basic Sample includes `Basic Sample 1.unity` as an alternate scene using refreshed robot materials. The LipSync Sample includes `DynamicContextDebugPanel` for manual Dynamic Context testing.

**Chat UI**

`ChatTranscriptUI` now focuses the typed input field when the player presses **Enter** while chat is active.
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
