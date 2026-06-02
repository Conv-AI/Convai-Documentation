---
title: Scene components
description: Reference for the Convai Chatbot, Convai Player, Convai Object, and Convai Face Sync components and how they relate to each other.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin adds four components to Unreal Engine. Each has a distinct role. Understanding their responsibilities before building a scene prevents the most common wiring mistakes.

## Component roles

| Component | Class | Display name | Attach to |
|---|---|---|---|
| Convai Chatbot | `UConvaiChatbotComponent` | "Convai Chatbot" | NPC character Blueprint |
| Convai Player | `UConvaiPlayerComponent` | "Convai Player" | Player pawn Blueprint |
| Convai Object | `UConvaiObjectComponent` | (no display name override) | Any in-scene Actor the AI should know about |
| Convai Face Sync | `UConvaiFaceSyncComponent` | "Convai Face Sync" | NPC character Blueprint |

## Convai Chatbot component

`UConvaiChatbotComponent` is the AI brain for a non-player character. It holds the `CharacterID` that links the component to a character you created on the Convai dashboard. At runtime it:

- Connects to Convai when `bAutoInitializeSession` is `true` (default) or when `StartSession()` is called.
- Receives player speech or text from a `UConvaiPlayerComponent` and streams the response back.
- Exposes conversation state through Blueprint-callable functions: `IsListening()`, `IsProcessing()` ("Is Thinking"), `GetIsTalking()` ("Is Talking"), and `IsInConversation()`.
- Fires Blueprint events: **On Actions Received**, **On Emotion State Changed**, **On Character Data Loaded**, **On Narrative Section Received**, **On Interaction ID Received**, **On Interrupted**, and **On Failure**.

The `CharacterID` property is the only required field. All other properties have usable defaults.

## Convai Player component

`UConvaiPlayerComponent` represents the human participant in the conversation. It:

- Captures microphone audio from the system's default capture device using `UConvaiAudioCaptureComponent`.
- Streams audio to the active `UConvaiChatbotComponent` during a conversation.
- Provides `StartRecording()` / `FinishRecording()` for manual audio capture, and `UnmuteStreamingAudio()` / `MuteStreamingAudio()` for streaming control.
- Exposes `SendText()` for text-only conversations without a microphone.
- Supports push-to-talk and hands-free (voice activity detection) modes through the `bMute` property and `UpdateVadBP()`.
- Enumerates and selects capture devices: `GetAvailableCaptureDeviceNames()`, `SetCaptureDeviceByIndex()`, `SetCaptureDeviceByName()`.

One `UConvaiPlayerComponent` on the player pawn can talk to any `UConvaiChatbotComponent` in the level.

## Convai Object component

`UConvaiObjectComponent` marks an in-scene Actor so every Convai chatbot in the level can reference it by name. Attach it to doors, switches, items, rooms, or any object that your AI characters should be able to name, describe, or interact with.

The component gives each object:

- **Identity** — a name and description that appear in the character's context.
- **Live state** — `TrackedProperties` entries that monitor UPROPERTY values on the Actor and push updates to chatbots when they change.

## Convai Face Sync component

`UConvaiFaceSyncComponent` drives blendshape-based lip sync and facial animation on an NPC. It receives pre-computed face animation data from the `UConvaiChatbotComponent` and applies it frame by frame in sync with the character's speech audio.

The key property is `LipSyncMode`, which selects the blendshape target:

| Display name | Enum value | Use with |
|---|---|---|
| Off | `EC_LipSyncMode::Off` | Disables face sync |
| Auto | `EC_LipSyncMode::Auto` | Let the plugin decide |
| Viseme Based | `EC_LipSyncMode::VisemeBased` | Custom rigs using OVR visemes (15 shapes) |
| MetaHuman Blendshapes | `EC_LipSyncMode::BS_MHA` | MetaHuman and Reallusion CC5 characters |
| ARKit Blendshapes | `EC_LipSyncMode::BS_ARKit` | Reallusion CC4 characters |
| CC4 Extended Blendshapes | `EC_LipSyncMode::BS_CC4_Extended` | CC4 characters with extended blendshapes |

The default value is `BS_MHA` (MetaHuman Blendshapes).

## How the components connect

```
Player pawn
└── UConvaiPlayerComponent   ← captures microphone audio
         │
         ▼  (streams audio and receives responses)
NPC character Blueprint
├── UConvaiChatbotComponent  ← connects to Convai, manages conversation
└── UConvaiFaceSyncComponent ← applies face animation data from the chatbot

Any scene Actor
└── UConvaiObjectComponent   ← makes the actor visible to all chatbots
```

The `UConvaiPlayerComponent` and `UConvaiChatbotComponent` connect through the session managed by `UConvaiSubsystem` (the engine subsystem that the plugin registers automatically). You do not need to reference the subsystem directly in most Blueprint setups.

## Convenience Blueprint wrappers

The plugin ships pre-configured Blueprint wrappers in its `Content/` folder. These are ready to drop into a scene:

| Asset | Wraps |
|---|---|
| `BP_ConvaiChatbotComponent` | `UConvaiChatbotComponent` with sensible defaults |
| `BP_ConvaiPlayerComponent` | `UConvaiPlayerComponent` with defaults |
| `BP_ConvaiSamplePlayer` | A full player pawn with `UConvaiPlayerComponent` attached |
| `BP_SampleGameMode` | A game mode that pairs with `BP_ConvaiSamplePlayer` |
| `BP_Convai3DWidgetComponent` / `WBP_3DChatWidget` | In-world chat UI |

## Base classes

For custom character Blueprints, the plugin provides base classes you can derive from:

| Class | Purpose |
|---|---|
| `ConvaiBaseCharacter` | NPC base — includes `UConvaiChatbotComponent` and `UConvaiFaceSyncComponent` pre-attached |
| `ConvaiBasePlayer` | Player base — includes `UConvaiPlayerComponent` pre-attached |
| `ConvaiPlayerWithVoiceActivation` | Player base with voice activity detection (hands-free) pre-configured |

## Next steps

- [Add your first Convai character](add-your-first-character.md) — step-by-step tutorial.
- [Set up a MetaHuman character](set-up-a-metahuman-character.md) — rig-specific setup for MetaHuman.
- [Set up a Reallusion (CC) character](set-up-a-reallusion-character.md) — rig-specific setup for Reallusion CC characters.
