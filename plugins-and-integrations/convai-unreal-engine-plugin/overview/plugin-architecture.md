---
title: Plugin architecture
description: Understand the Convai Unreal Engine plugin's four modules and five runtime components, and how they interact during a conversation.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin is structured as four modules and five primary runtime components. Each module has a defined scope and loading phase; each component has a single responsibility and communicates with the others through Unreal's component and subsystem model.

## Modules

The plugin declares four modules in `ConvAI.uplugin`.

| Module | Type | Platforms | Purpose |
|---|---|---|---|
| `Convai` | Runtime | Win64, Android | Core conversation pipeline: WebRTC session management, audio streaming, chatbot and player components, subsystem, dynamic context, environment, actions, vision. |
| `ConvaiEditor` | Editor | All (editor build only) | In-editor configuration window, API key setup, character dashboard browser, Blueprint graph utilities (e.g. "Create Convai Action Handler" right-click entry). Disabled on UE 5.1 and earlier. |
| `ConvaiAnimGraph` | UncookedOnly | All | Animation graph nodes that drive blendshapes from the live facial animation stream. Available in the Animation Blueprint editor for MetaHuman and other rigs. |
| `ConvaiVisionBase` | Runtime | Win64, Android | Base layer for the vision feature: frame capture, encoding, and delivery to the WebRTC session. |

The `Convai` module loads at `PreDefault` phase so it is available before gameplay systems initialize. `ConvaiEditor` loads at `PostEngineInit` so it can access the fully initialized editor environment.

## System diagram

The diagram below shows the runtime flow for a single player–character conversation turn.

```mermaid
graph TD
    Player["UConvaiPlayerComponent\n(audio capture, gaze)"]
    Chatbot["UConvaiChatbotComponent\n(session, environment, actions)"]
    Subsystem["UConvaiSubsystem\n(WebRTC client, registry)"]
    FaceSync["UConvaiFaceSyncComponent\n(blendshapes)"]
    AnimGraph["ConvaiAnimGraph node\n(AnimBP)"]
    Object["UConvaiObjectComponent\n(scene object)"]
    Convai["Convai\n(LLM, voice, narrative)"]

    Player -->|"audio frames"| Subsystem
    Subsystem -->|"WebRTC stream"| Convai
    Convai -->|"audio + face data\naction sequence\nemotion state"| Subsystem
    Subsystem -->|"dispatch to session"| Chatbot
    Chatbot -->|"FAnimationSequence"| FaceSync
    FaceSync -->|"blendshape map"| AnimGraph
    Object -->|"property changes"| Subsystem
    Subsystem -->|"batched context update"| Chatbot
    Chatbot -->|"context flush"| Convai
```

`UConvaiSubsystem` is the single shared connection point. Components register themselves with it at `BeginPlay` and unregister at `EndPlay`. The subsystem's shared object-poll clock fires on every registered `UConvaiObjectComponent` in the same tick so property changes from multiple objects coalesce into one batched update per debounce window.

## Runtime components

Five components form the Blueprint-facing surface of the plugin's runtime. They attach to Actors like any native Unreal component.

{% hint style="info" %}
Each component's **display name** is the label shown in the **Add Component** panel inside the Unreal Editor. Use the display name to find each component when adding it to a Blueprint Actor.
{% endhint %}

### `UConvaiChatbotComponent` (display name: Convai Chatbot)

The central component for an AI character. It holds the character ID, session state, environment contract (actions, objects, scene characters), dynamic context, emotion state, and the action queue. One instance per AI character Actor.

`UConvaiChatbotComponent` owns the WebRTC session for its character. When a session starts it sends the action configuration to Convai, receives audio and facial animation data, drives the audio streamer, and dispatches action sequences to Blueprint handlers.

### `UConvaiPlayerComponent` (display name: Convai Player)

Represents the human player in the conversation. It captures microphone audio through `UConvaiAudioCaptureComponent`, streams it to the active chatbot session, and drives the gaze-attention system that tracks which `UConvaiObjectComponent` actors are under the player's crosshair.

### `UConvaiObjectComponent`

Tags an Actor as a scene object that a chatbot can reference in its environment contract. When the component registers with `UConvaiSubsystem`, the subsystem polls its tracked properties on a shared clock and coalesces changes into batched dynamic-context updates. Multiple chatbots can share the same object component.

### `UConvaiFaceSyncComponent` (display name: Convai Face Sync)

A scene component that applies precomputed facial animation sequences to a skeletal mesh. It consumes `FAnimationSequence` data delivered by `UConvaiChatbotComponent`, interpolates blendshape frames, and exposes the resulting `TMap<FName, float>` to an Animation Blueprint through an AnimGraph node in the `ConvaiAnimGraph` module. It supports ARKit blendshape naming for MetaHuman rigs and compatible CC5 rigs.

### `UConvaiSubsystem` (display name: Convai Subsystem)

A `UGameInstanceSubsystem` that acts as the shared connection manager and component registry. It maintains the WebRTC client, routes audio and data packets to the correct session proxies, and provides registry access to all active `UConvaiChatbotComponent`, `UConvaiPlayerComponent`, and `UConvaiObjectComponent` instances via `GetAllChatbotComponents`, `GetAllPlayerComponents`, and `GetAllObjectComponents`.

## Plugin dependencies

The plugin declares the following engine plugin dependencies in `ConvAI.uplugin`:

| Plugin | Enabled | Role |
|---|---|---|
| `AudioCapture` | Yes | Microphone input pipeline |
| `AndroidPermission` | Yes | Runtime microphone permission request on Android |
| `EditorScriptingUtilities` | Yes | Editor automation helpers used by `ConvaiEditor` (editor only) |
| `PropertyAccessEditor` | Yes | Property-binding editor feature used by `ConvaiEditor` (editor only) |

## Next steps

{% content-ref url="../getting-started/" %}
[Getting started](../getting-started/)
{% endcontent-ref %}

{% content-ref url="feature-map.md" %}
[Feature map](feature-map.md)
{% endcontent-ref %}

{% content-ref url="what-is-the-convai-unreal-plugin.md" %}
[What is the Convai Unreal Engine plugin](what-is-the-convai-unreal-plugin.md)
{% endcontent-ref %}
