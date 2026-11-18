---
title: Audio API
description: Control microphone capture, mute and remote track subscriptions, inspect audio availability, and unlock browser playback from Unity scripts.
last_reviewed: "5.0.0-pre.1"
---

Access the `ConvaiAudio` facade through `ConvaiManager.Audio` after `manager.IsInitialized` becomes true. Use it for microphone capture, permission to capture within a session, track subscription, local mute, and browser audio playback.

## Microphone

| Member | Behavior |
| --- | --- |
| `IsMicMuted`, `SetMicMuted(bool)`, `ToggleMicMuted()`, `OnMicMuteChanged` | Microphone mute state, controls, and notification |
| `StartListeningAsync(CancellationToken)`, `StopListeningAsync(CancellationToken)` | Start or stop capture |
| `IsMicrophoneAllowed`, `SetMicrophoneAllowed(bool)`, `OnMicrophoneAllowedChanged` | Whether the session may open the microphone |
| `MicrophoneLevel`, `IsMicrophoneLevelAvailable` | Local level from `0` to `1` and whether measurement is available |
| `HoldPlayerSpeech()`, `IsPlayerSpeechHeld`, `OnPlayerSpeechHeldChanged` | A disposable hold on player speech, its state, and notification |

Select a preferred device by ID through [Runtime settings API](../ui-and-presentation/settings-panel/runtime-settings-api.md). Starting capture uses the preferred device. Microphone start in a text-only session returns the error `audio.mic_not_allowed`.

## Character audio

| Member | Behavior |
| --- | --- |
| `SetCharacterMuted(characterId, muted)`, `IsCharacterMuted(characterId)` | Silence or restore local playback while audio continues arriving |
| `SetRemoteAudioEnabled(characterId, enabled)`, `IsRemoteAudioEnabled(characterId)` | Control or read the remote track subscription |
| `OnRemoteAudioEnabledChanged` | Character ID and subscription state |
| `ConvaiCharacter.SetRemoteAudioEnabled(bool)` | Set the subscription state from the character component |

**Play Voice On Start** controls the initial subscription. `ConvaiAudioOutput` owns volume and spatial audio settings and exposes `VoiceLevel` and `IsVoiceLevelAvailable` for visual meters. See [Show connection and audio levels](../ui-and-presentation/show-connection-and-audio-levels.md).

## Browser playback

`RequiresUserGesture`, `IsAudioPlaybackActive`, and `CanEnableAudioPlayback` describe playback. Call `EnableAudioPlayback()` from a user gesture when required. `EnableAudioAndStartListening()` also attempts to start capture when the session allows it. These methods require a separate connection.

The manager's default WebGL scene-click handling attempts playback unlock on eligible non-UI clicks after connection. A later gesture can recover blocked playback. Browser microphone permission and autoplay have separate controls.

## Push-to-talk and reply completion

Use the [push-to-talk controller](push-to-talk-api.md) to keep capture and target ownership together. Native `Events.OnCharacterTurnPlaybackCompleted` reports a logically complete reply whose audio finished playing. This event requires a reply that played audio and is unavailable on WebGL.

## Related pages

- [Configure microphone](../getting-started/configure-microphone.md)
- [Audio and microphone issues](../troubleshooting/audio-and-microphone-issues.md)
