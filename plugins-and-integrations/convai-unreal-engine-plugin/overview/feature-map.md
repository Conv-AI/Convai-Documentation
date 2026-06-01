---
title: Feature map
description: One-screen overview of every major feature in the Convai Unreal Engine plugin, with links to each feature's documentation.
last_reviewed: "4.0.0-beta.21"
---

The table below lists every major feature in the Convai Unreal Engine plugin, the primary component or module it lives in, and a link to its feature documentation. Use this page to find the right starting point before diving into guides or reference material.

## Feature index

| Feature | Primary component | Description |
|---|---|---|
| [Lip sync](#lip-sync) | `UConvaiFaceSyncComponent` | Drives mouth and facial blendshapes from the character's response audio in real time. |
| [Emotions](#emotions) | `UConvaiChatbotComponent` | Convai infers emotion state from the conversation and drives blendshape expressions on the character. |
| [Actions](#actions) | `UConvaiChatbotComponent` | The character issues typed action commands (Move To, Follow, custom) that Blueprint handlers execute. |
| [Scene objects](#scene-objects) | `UConvaiObjectComponent` | Tags level actors so the character is aware of them and can reference or act on them. |
| [Gaze attention](#gaze-attention) | `UConvaiPlayerComponent` | Tracks which object the player is looking at and routes that context to the active chatbot. |
| [Dynamic context](#dynamic-context) | `UConvaiChatbotComponent` | Pushes live world state (key/value pairs, freeform events) to the character's context window at runtime. |
| [Narrative design](#narrative-design) | `UConvaiChatbotComponent` | Triggers scripted conversation branches and Behavior Tree sections by name, with optional template keys. |
| [Long-term memory](#long-term-memory) | `UConvaiChatbotComponent` | Persists conversation history across sessions using an end-user ID so the character remembers past interactions. |
| [Vision](#vision) | `ConvaiVisionBase` module | Streams camera frames to Convai so the character can describe or react to what the player sees. |
| [Multiplayer](#multiplayer) | `UConvaiSubsystem` | Replicates conversation events, voice, and animation across networked clients. |

## Lip sync

`UConvaiFaceSyncComponent` receives precomputed `FAnimationSequence` data from the chatbot component, interpolates blendshape frames against the character's skeletal mesh, and exposes the result to an Animation Blueprint through the `ConvaiAnimGraph` node. ARKit blendshape naming is supported for MetaHuman and compatible CC5 rigs.

{% content-ref url="../features/lip-sync.md" %}
[Lip sync](../features/lip-sync.md)
{% endcontent-ref %}

## Emotions

When a character responds, Convai infers an emotion state and returns blendshape weights alongside the audio. `UConvaiChatbotComponent` stores the current `FConvaiEmotionState` and fires `OnEmotionStateChangedEvent` when it changes. Blueprint can also call `ForceSetEmotion` to drive expressions programmatically, and `GetEmotionScore` to read per-emotion weights.

{% content-ref url="../features/emotions.md" %}
[Emotions](../features/emotions.md)
{% endcontent-ref %}

## Actions

`UConvaiChatbotComponent` carries an `EnvironmentData` (`FConvaiEnvironmentData`) struct that defines the set of actions the character can issue, the objects it can act on, and the characters in the scene. When the character decides to act, Convai returns a typed action sequence. The component routes each action to the matching Blueprint function on the owning Actor by name, queues remaining actions, and expects the handler to call `HandleActionCompletion` when done.

Default actions (Move To, Follow, Stop Moving, Wait For) are seeded automatically. Custom actions with typed parameters — `string`, `number`, `bool`, `enum`, or object reference — are declared as `FConvaiAction` entries on the component.

{% content-ref url="../features/actions.md" %}
[Actions](../features/actions.md)
{% endcontent-ref %}

## Scene objects

`UConvaiObjectComponent` tags an Actor as a named scene object. The subsystem polls tracked properties on a shared clock and coalesces changes into batched `update-scene-metadata` messages sent to the active chatbot. A chatbot's `EnvironmentData.Objects` list determines which objects are part of the action contract at connect time.

{% content-ref url="../features/scene-objects.md" %}
[Scene objects](../features/scene-objects.md)
{% endcontent-ref %}

## Gaze attention

`UConvaiPlayerComponent` continuously evaluates which `UConvaiObjectComponent` actor the player's camera is aimed at. When the gaze dwells past a configurable threshold, it calls `TrySetObjectInAttentionFromGaze` on the active chatbot, which folds the attention object into the next context update. A silhouette highlight and on-screen cursor provide visual feedback.

{% content-ref url="../features/gaze-attention.md" %}
[Gaze attention](../features/gaze-attention.md)
{% endcontent-ref %}

## Dynamic context

`UConvaiChatbotComponent` exposes a structured dynamic context API: `SetContextState` and `SetContextStates` manage key/value world-state pairs; `AddContextEvent` appends freeform chronological events. Changes are batched within a debounce window (default 0.5 s, capped at 3 s) before being flushed to Convai as a single `context-update` message. `DynamicEnvironmentInfo` is a simpler string property for less structured use cases.

{% content-ref url="../features/dynamic-context.md" %}
[Dynamic context](../features/dynamic-context.md)
{% endcontent-ref %}

## Narrative design

`InvokeNarrativeDesignTrigger` fires a named narrative section defined in the Convai dashboard, optionally generating actions at the same time. `NarrativeTemplateKeys` (a `TMap<FString, FString>` on the chatbot component) substitutes variables into the narrative section text at runtime. `OnNarrativeSectionReceivedEvent` fires when a section completes.

{% content-ref url="../features/narrative-design.md" %}
[Narrative design](../features/narrative-design.md)
{% endcontent-ref %}

## Long-term memory

Set `EndUserID` on `UConvaiChatbotComponent` to a stable identifier for the human player. Convai uses this ID to retrieve and store conversation history across sessions, so the character can reference past interactions. `EndUserMetadata` accepts a JSON string for additional player context.

{% content-ref url="../features/long-term-memory.md" %}
[Long-term memory](../features/long-term-memory.md)
{% endcontent-ref %}

## Vision

The `ConvaiVisionBase` module captures frames from the player's camera and streams them to Convai over the WebRTC session. The character can describe the scene, identify objects, or react to what is visible. Vision is enabled per-chatbot by setting the appropriate flag on `UConvaiChatbotComponent`.

{% content-ref url="../features/vision.md" %}
[Vision](../features/vision.md)
{% endcontent-ref %}

## Multiplayer

The plugin supports networked multiplayer through Unreal's replication system. `UConvaiChatbotComponent` replicates `CharacterID`, `CharacterName`, `EmotionState`, `LookAtTarget`, `PointAtTarget`, and environment data. Voice and animation events broadcast over `NetMulticast`. `UConvaiSubsystem` maintains per-session state so multiple clients can hold simultaneous conversations with different characters.

{% content-ref url="../features/multiplayer.md" %}
[Multiplayer](../features/multiplayer.md)
{% endcontent-ref %}
