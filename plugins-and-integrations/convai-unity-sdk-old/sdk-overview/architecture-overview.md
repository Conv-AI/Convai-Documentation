---
description: >-
  The four-tier Convai Unity SDK architecture — Runtime, Room, Agent, and Module
  — and the responsibilities of each layer.
---

# Architecture Overview

## How the SDK Layers Fit Together

The SDK is organized into four tiers: Runtime, Room, Agent, and Module. Each tier has a clear owner and a defined set of responsibilities. As a developer, you interact primarily with the Agent tier (character and player components) and the Module layer (opt-in feature modules). The Runtime and Room tiers handle connection and service bootstrapping with minimal configuration required.

***

## System Diagram

```mermaid
graph TD
    subgraph RT["Runtime Tier"]
        CM["ConvaiManager\n(composition root, service hub)"]
        CS["ConvaiSDK\n(version metadata)"]
    end

    subgraph RM_TIER["Room Tier"]
        RM["ConvaiRoomManager\n(connection · audio · turn-taking)"]
    end

    subgraph AG["Agent Tier"]
        CC["ConvaiCharacter × N\n(session · transcripts · events)"]
        CP["ConvaiPlayer × 1\n(identity · text input)"]
    end

    subgraph ML["Module Layer (opt-in per character)"]
        direction LR
        LS[LipSync]
        EM[Emotion]
        VI[Vision]
        NA[Narrative]
        DA[DialogueAnimation]
        FA[FacialAnimation]
        GA[Gaze]
        AT[Attention]
        CF[ConversationFlow]
        EB[Embodiment]
    end

    CM --> RM
    RM --> CC
    RM --> CP
    CC -.->|modules attach to| ML
```

The dashed line from `ConvaiCharacter` to the Module Layer means modules are optional components you add to the same GameObject as the character — not required for basic conversation.

***

## Runtime Tier

The Runtime tier boots when your scene loads and provides services to everything below it.

`ConvaiSDK` is a static class that exposes the SDK version (`ConvaiSDK.Version`). You rarely reference it directly.

`ConvaiManager` is the composition root. It is a singleton (`ConvaiManager.ActiveManager`) marked with `[DefaultExecutionOrder(-1100)]` so it initializes before other scene objects. It owns:

* **Service accessors** — `TryGet` methods for every internal service (microphone, audio, agent registry, notification, settings panel, etc.)
* **High-level facades** — `ConvaiManager.Audio`, `ConvaiManager.Transcripts`, `ConvaiManager.Events` for the most common scripting tasks
* **Connection control** — `ConnectAsync()`, `DisconnectAsync()`, `SetConversationInputModeAsync()`
* **Agent references** — `Characters`, `Player`, `ActiveConversationCharacter`

{% hint style="info" %}
Most integration code only needs `ConvaiManager.ActiveManager` and the character's own events. The `TryGet` service accessors are for advanced use cases where you replace or extend internal services.
{% endhint %}

***

## Room Tier

`ConvaiRoomManager` owns the live connection to Convai. One `ConvaiRoomManager` per scene, managed by `ConvaiManager`.

It is responsible for:

* **Room connection lifecycle** — connecting, disconnecting, reconnecting with exponential backoff
* **Microphone capture** — starting and stopping audio input, mute control
* **Turn-taking mode** — hands-free (LocalAudio), push-to-talk (PushToTalk), or smart turn detection (SmartTurn)
* **Dynamic context transport** — sending state updates and events to Convai at runtime
* **Audio playback coordination** — enabling remote character audio, WebGL user-gesture handling

`ConvaiRoomManager` exposes coordinators for diagnostics, audio, ownership, and connection management. These are accessible via `ConvaiManager.ActiveManager.TryGetRoomConnectionService()` for advanced scripting.

***

## Agent Tier

The Agent tier contains the components you place on scene GameObjects.

### ConvaiCharacter

Add `ConvaiCharacter` to each NPC or agent GameObject. One component per character. It owns:

* Character ID — the unique ID from your Convai dashboard
* Session state — `Connected`, `Disconnecting`, `Reconnecting`, etc.
* Conversation lifecycle — `StartConversationAsync()`, `StopConversationAsync()`, `ToggleSpeech()`
* Transcript and event callbacks — `OnTranscriptReceived`, `OnEmotionChanged`, `OnActionsReceived`, `OnSpeechStarted`, `OnSpeechStopped`, `OnCharacterReady`
* Action configuration — via `ConvaiActionConfigSource` component

`ConvaiCharacter` can be configured inline in the Inspector or via a reusable `ConvaiCharacterProfile` ScriptableObject asset.

### ConvaiPlayer

Add `ConvaiPlayer` to your player GameObject. Exactly one `ConvaiPlayer` per scene. It owns:

* Player display name and name tag color for transcript attribution
* Text message sending — `SendTextMessage(string message)`
* Runtime identity override — `SetRuntimeDisplayName(string displayName)`

{% hint style="warning" %}
`ConvaiPlayer.PlayerId` is a local display identifier for transcript UI attribution. It is not the server-generated speaker ID used for Long-Term Memory tracking.
{% endhint %}

***

## Module Layer

Modules are optional Unity components you add to the same GameObject as `ConvaiCharacter` (or `ConvaiRoomManager` for Vision). Each module is independent — add only what your project needs.

| Module              | What it does                                                                                                     |
| ------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `LipSync`           | Real-time blend shape mouth animation driven by audio playback; supports ARKit, MetaHuman, and CC4 Extended maps |
| `Emotion`           | Receives Convai emotion signals, smooths them, and dispatches to blend shape or Animator parameter bindings      |
| `Vision`            | Publishes camera, webcam, or Meta Quest passthrough frames to Convai for multimodal awareness                    |
| `Narrative`         | Manages story section progression through trigger-based events tied to conversation flow                         |
| `DialogueAnimation` | Drives a four-layer animator stack (base idle, masked overlays, body talk, head talk) during dialogue            |
| `FacialAnimation`   | Plays facial animation clips at runtime, composited against lip sync and emotion outputs                         |
| `Gaze`              | Blends eye and head actuators toward conversation partners and attention targets                                 |
| `Attention`         | Resolves weighted focus targets, providing gaze direction to the Gaze module                                     |
| `ConversationFlow`  | Bridges the conversation event stream to per-frame dialogue state (Idle, Speaking, Reacting, etc.)               |
| `Embodiment`        | Foundational behavior profile and lifecycle management for physical presence and behavioral modules              |

`ConversationFlow` and `Embodiment` are automatically added when you use the scene setup menu. `LipSync`, `Emotion`, `Vision`, `Narrative`, `DialogueAnimation`, `Gaze`, and `Attention` are opt-in.

***

## Configuration Model

Every major component supports two configuration modes, selectable in the Inspector.

{% tabs %}
{% tab title="Inline" %}
Values are set directly on the component in the Inspector. This is the default mode and is suitable for most scenes — no additional assets required.
{% endtab %}

{% tab title="Asset" %}
Values come from a reusable `ConvaiCharacterProfile` or `ConvaiRoomManagerProfile` ScriptableObject. Use this when you want shared defaults across multiple scenes or prefab variants, or when you need to swap character behavior without modifying individual prefabs.
{% endtab %}
{% endtabs %}

***

## Next Steps

{% content-ref url="/broken/pages/cf8f17d258329a4e0e89aa6d7460fecf2a80f3fd" %}
[Broken link](/broken/pages/cf8f17d258329a4e0e89aa6d7460fecf2a80f3fd)
{% endcontent-ref %}

{% content-ref url="/broken/pages/63e79c1ce45c5fae027b5b1e1b756bbfd5e332d0" %}
[Broken link](/broken/pages/63e79c1ce45c5fae027b5b1e1b756bbfd5e332d0)
{% endcontent-ref %}
