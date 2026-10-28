---
title: Turn-taking modes
description: Configure hands-free and push-to-talk conversation modes, including turn detection, release timing, and barge-in interruption behavior.
last_reviewed: "5.0.0-preview"
---

Turn-taking settings choose whether speech is hands-free or controlled by a push-to-talk input. They belong to the room and are shared by all its character memberships. Configure **Convai Room Manager** or its profile, then inspect the active policy when diagnosing a conversation.

## Modes and end-of-turn detection

| Setting | Default | Meaning |
| --- | --- | --- |
| `TurnTakingOptions.Mode` | `HandsFree` | `HandsFree` uses automatic speech processing; `PushToTalk` uses explicit press/release |
| `TurnDetection` | `UseDefault` | Use service defaults, disable automatic turn detection, or send `Custom` settings |
| `CustomTurnDetection.StopSecs` | `3` | Requested silence duration |
| `CustomTurnDetection.PreSpeechMs` | `0` | Requested pre-speech audio duration |
| `CustomTurnDetection.MaxDurationSecs` | `8` | Requested maximum turn duration |
| `InitialServerStt` | `UseDefault` | SDK resolves STT enabled for hands-free and disabled for push-to-talk |

Custom turn-detection values are sent to the service; they are not a guarantee of an exact response delay. [Voice activity detection](voice-activity-detection.md) controls a separate connect-time VAD request.

## Push-to-talk policy

| `PushToTalkPolicy` field | Default | Meaning |
| --- | --- | --- |
| `ReleaseMode` | `Auto` | Use correlated release when supported; `Legacy` forces compatibility release |
| `ReleaseTailMs` | `1000` | Legacy finalization window, clamped to 0–5000 ms |
| `EnableServerSttToggle` | `true` | Toggle server speech recognition around a press |
| `InterruptBotOnPress` | `true` | Request interruption when a press is accepted |
| `RequireTurnCompletionBeforeNextPress` | `true` | Gate the next press while awaiting the reply |
| `TurnCompletionTimeoutMs` | `5000` | Inaudible wait budget; zero disables this timeout |
| `AllowSpeechStoppedFallbackAfterSpeechStart` | `false` | Allow speech-stopped fallback after speech began |

`Auto` needs server STT toggling and a capture-drain-capable transport. Native capture can provide this; the active format/provider must support it. WebGL uses the Legacy path. `CompatibilityReason` on the push-to-talk controller explains a fallback. See [Push-to-talk lifecycle](push-to-talk-lifecycle.md) before tuning release timing.

In the Inspector, the relevant sections are **Advanced Room Control**, **Listening**, **Interruptions**, **Vision**, and **Reconnect**. Push-to-talk labels include **Interrupt On Press**, **Wait For Reply To Finish**, **Wait Timeout (ms)**, **Start Muted**, and **Prepare Microphone**. Developer settings expose release mode and the legacy tail controls.

## Local microphone policy

| `LocalAudioPolicy` field | Default | Meaning |
| --- | --- | --- |
| `AllowMicrophone` | `true` | Whether this session may open microphone capture |
| `StartMutedInPushToTalk` | `true` | Start push-to-talk muted |
| `PushToTalkStartupMode` | `PrewarmMuted` | Prepare capture before the first press; `OpenOnFirstPress` waits until it is needed |
| `EnableAcousticEchoCancellation` | `false` | Request native echo cancellation |
| `EnableNoiseSuppression` | `true` | Request native noise suppression |
| `EnableAutomaticGainControl` | `false` | Request native automatic gain control |

Audio-processing settings apply when connecting. WebGL uses browser capture processing. Disabling `AllowMicrophone` makes the session text-only: microphone start fails with `audio.mic_not_allowed`. A per-connect option cannot override a room-level prohibition to enable capture. Use `ConvaiRoomManager.SetMicrophoneAllowed` for the runtime policy surface.

## Interruption

`BargeIn.SmoothInterruption` defaults to true; `FadeOutSeconds` defaults to `0.12` and is clamped to `0.04`–`0.25`. `ClientDetection` defaults to `Disabled`. Native `Silero` detection uses the existing microphone stream; it requires the SDK's Unity Inference integration and is excluded from WebGL. The assembly supports Inference versions `[2.2.1, 3.0.0)`.

Local detection and server confirmation are different. A local candidate can duck playback; automatic client interruption has additional echo-processing and capture-readiness guards. Do not infer that selecting Silero or AEC alone guarantees a working interruption path. WebGL relies on server detection.

## Runtime mode changes

Await `ConvaiManager.SetConversationInputModeAsync(ConversationInputMode.PushToTalk)` or `HandsFree` to change a regular room's mode. Read `ActiveConversationInputMode` afterward. A group voice conversation requires supported native correlated push-to-talk: WebGL, hands-free, and Legacy release are refused by that flow.

## Related pages

- [Configure conversation input mode](../getting-started/configure-conversation-input-mode.md)
- [Push-to-talk scripting reference](../scripting-reference/push-to-talk-api.md)
- [Group conversation](../features/group-conversation/README.md)
