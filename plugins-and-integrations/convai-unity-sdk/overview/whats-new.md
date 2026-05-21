# whats new

The current release is **v4.2.0** (2026-05-08). For the full commit-level changelog, see [docs.convai.com/unity/changelog](https://docs.convai.com/unity/changelog).

{% updates %}
{% update date="2026-05-08" tags="v4.2.0,Current" %}
## v4.2.0

### Actions System

The SDK now ships with a complete structured Actions runtime. Characters can execute in-scene commands in response to decisions made by Convai.

* `ConvaiActionDispatcher` — queued dispatch with configurable batch and failure policies
* `IConvaiActionExecutor` — interface for writing custom executors
* Built-in executors for common action types
* `ConvaiActionConfigSource` — Inspector-driven action configuration on each character
* `ConvaiActionDebugProbe` — runtime action monitoring and diagnostics
* Target resolution with attention and reference grounding

See [Actions](/broken/pages/46d20373036c3c1a8d7d4088901c20f1baa78a4c) for setup and usage.

**Meta Quest Passthrough Vision**

`QuestVisionFrameSource` enables the Vision module on Meta Quest devices using the headset's passthrough cameras. No external camera component required.

See [Vision — Frame Sources](/broken/pages/02718710a9ff584e645825102e7340e88310b8de) for setup.

**Runtime Turn-Taking Mode Switching**

You can now switch between hands-free, push-to-talk, and smart turn-taking modes on a live session without disconnecting and reconnecting. Use `ConvaiManager.SetConversationInputModeAsync()` or the Settings Panel at runtime.

See [Turn-Taking Modes](/broken/pages/43d2a627f3db81eba35c332edf2ffbb98a923065) and [Configure Conversation Input Mode](/broken/pages/ca110b3413d787ae6ac298e2b8400531a54d4961).

**Dynamic Context Expansion**

* Tracker APIs for monitoring context state at runtime
* Inspector tooling for authoring context commands in the Editor
* Sample UI commands demonstrating runtime context injection

See [Dynamic Context](/broken/pages/ff229409c9d35525aedff2c5f5d53a1d4a34c251).

**Scene Setup API and Wizard Validation**

* `GameObject > Convai > Setup Required Components` menu item creates and validates all required scene components
* Setup wizard reports missing or misconfigured components before you enter Play mode

See [Custom Scene Setup](/broken/pages/477f3e0fbffc248414da1eaa9b83f8ca3a186c06).

**Settings Panel Input Mode Control**

The runtime Settings Panel now includes hands-free / push-to-talk switching, giving players control over input mode without any additional scripting.

See [Settings Panel](/broken/pages/be2b7d7c1cf1ff14ddde43a3dbfae7851dbbfdb4).
{% endupdate %}

{% update date="2026-04-09" tags="v4.1.0" %}
## v4.1.0

* **Dynamic Context** — initial support for injecting runtime state and events into character knowledge via `ConvaiDynamicContextCommand` components
* **LipSync sample camera** — the showcase camera in the LipSync sample no longer has a hard dependency on the Unity Input System package
* **Vision module** — reliability improvements to the publish flow and source selection UX
* **iOS** — fixed a crash caused by support library shutdown handling
* **Sample scenes** — refined scene hierarchy, refreshed transcript prefab defaults
* **Editor** — improved startup reliability for native plugin errors during import
{% endupdate %}

{% update date="2026-03-12" tags="v4.0.0,Initial Release" %}
## v4.0.0

The first public release of the Convai Unity SDK.

**Core components:**

* `ConvaiManager` — composition root and service hub
* `ConvaiRoomManager` — room connection, audio, and turn-taking
* `ConvaiCharacter` — per-NPC conversation lifecycle and event callbacks
* `ConvaiPlayer` — player identity and text input

**Conversation pipeline:**

* Real-time streaming speech recognition (STT)
* Language understanding and generation (LLM)
* Text-to-speech (TTS) with Unity audio playback

**Modules:**

* LipSync — blend shape lip animation (ARKit maps bundled)
* Emotion — server emotion signal → facial/animator bindings
* Vision — camera and webcam frame publishing
* Narrative Design — trigger-based story progression
* Dialogue Animation — four-layer animator stack
* Gaze & Attention — eye and head gaze toward focus targets

**Platform support:** Windows, macOS, Linux, Android, iOS. WebGL supported with known audio/lip-sync timing limitation in some browsers.

**Editor tooling:** Project Settings API key panel, custom Inspectors, scene setup menu, configurable logging.
{% endupdate %}
{% endupdates %}

***

## Next Steps

{% content-ref url="/broken/pages/63e79c1ce45c5fae027b5b1e1b756bbfd5e332d0" %}
[Broken link](/broken/pages/63e79c1ce45c5fae027b5b1e1b756bbfd5e332d0)
{% endcontent-ref %}
