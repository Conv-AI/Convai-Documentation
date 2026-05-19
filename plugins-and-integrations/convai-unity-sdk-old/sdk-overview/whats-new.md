---
description: >-
  Release notes for the Convai Unity SDK — current version highlights, new
  features, and migration notes.
---

# What's New

## Release Notes

{% updates format="full" %}
{% update date="2026-05-08" tags="v4.2.0,Current" %}
## v4.2.0

#### Actions System

Characters can execute in-scene commands through a structured runtime. New in this release:

* `ConvaiActionDispatcher` with queued dispatch — actions execute in sequence without race conditions
* `IConvaiActionExecutor` interface for custom executors
* Six built-in executors: move-to (Transform and NavMesh), pick-up, look-at, Animator trigger, and UnityEvent
* Inspector-driven configuration — no scripting required for standard action setups
* Runtime diagnostics for monitoring action queue state

#### Meta Quest Passthrough Vision

`QuestVisionFrameSource` enables the Vision module on Quest 3 and Quest 3S devices without an external camera. Characters see through the device's passthrough camera during mixed reality sessions.

#### Runtime Turn-Taking Mode Switching

Switch between hands-free, push-to-talk, and smart turn-taking modes during live sessions using `ConvaiManager.SetConversationInputModeAsync()` or the runtime Settings Panel — no scene reload required.

#### Dynamic Context Expansion

* Tracker APIs let you monitor current context state from scripts
* Inspector tooling for authoring context commands without code
* `SampleDynamicContextUI` prefab demonstrates runtime injection patterns

#### Scene Setup Tooling and Validation

Menu-driven component creation (`GameObject > Convai > Setup Required Components`) and scene validation (`GameObject > Convai > Validate Scene Setup`) prevent misconfiguration before entering Play mode.

#### Settings Panel Input Mode Control

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

**Modules:** LipSync, Emotion, Vision, Narrative Design, Dynamic Context, Long-Term Memory, Scene Metadata, Dialogue Animation, Gaze & Attention

**Platform support:** Windows, macOS, Linux, Android, iOS, WebGL

**Editor tooling:** Scene setup, validation, Project Settings integration, and the Convai Welcome window
{% endupdate %}
{% endupdates %}

### Next Steps

For full commit-level details, see the [changelog](https://docs.convai.com/unity/changelog). To start using the SDK, follow [Getting Started](/broken/pages/6df632490c3086c38b9bf965dcef2ede7bd15514).
