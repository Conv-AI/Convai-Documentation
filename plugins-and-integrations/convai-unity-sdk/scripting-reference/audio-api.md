---
title: Audio API
description: Control microphone capture, mute and remote track subscriptions, inspect audio availability, and unlock browser playback from Unity scripts.
last_reviewed: "5.0.0-preview"
---

`ConvaiManager.Audio` returns the `ConvaiAudio` facade after manager initialization. Before that it throws; a null check on the property does not guard startup. Check `manager.IsInitialized` or use `TryGetRoomAudioService`.

## Microphone

| Member | Behavior |
| --- | --- |
| `IsMicMuted` | Current mute state |
| `SetMicMuted(bool)`, `ToggleMicMuted()` | Change mute state |
| `StartListeningAsync(int microphoneIndex = 0, CancellationToken)` | Start capture using the transport's device-list index |
| `StopListeningAsync(CancellationToken)` | Stop capture |
| `OnMicMuteChanged` | Mute-state notification |

Index zero is the first listed transport device, not a system-default lookup. Indices are clamped to the device-list range. Use the microphone device/runtime-settings service for device selection UI.

Text-only sessions refuse microphone start with `audio.mic_not_allowed`. The room exposes `IsMicrophoneAllowed`, `SetMicrophoneAllowed`, and `MicrophoneAllowedChanged`. `MicrophoneLevel` and `IsMicrophoneLevelAvailable` belong to `ConvaiRoomManager`, not this facade.

## Character audio

| Method | Behavior |
| --- | --- |
| `SetCharacterMuted`, `MuteCharacter`, `UnmuteCharacter`, `IsCharacterMuted` | Local character mute control |
| `SetRemoteAudioEnabled`, `IsRemoteAudioEnabled` | Track subscription control |
| `OnRemoteAudioEnabledChanged` | Character ID and enabled state |

Muting and disabling a remote track are different operations. The latter disables the character's remote audio subscription. Native and WebGL adapters both apply the preference to controllable tracks. `ConvaiCharacter.ToggleRemoteAudio` can re-enable a disabled track. Configure startup behavior with **Play Voice On Start**; `EnableRemoteAudioOnStart` is read-only.

`ConvaiAudioOutput` controls volume, spatial blend, distances, and rolloff on its `AudioSource`. Adjust its own fields instead of fields it will overwrite. It exposes `VoiceLevel` and `IsVoiceLevelAvailable` for meters. See [Show connection and audio levels](../ui-and-presentation/show-connection-and-audio-levels.md).

## Browser playback

`RequiresUserGesture`, `IsAudioPlaybackActive`, and `CanEnableAudioPlayback` report playback capability. Call `EnableAudioPlayback()` from a user interaction when required. The manager's `EnableAudioAndStartListening()` combines playback unlock and microphone start; it does not connect the room.

The manager's default WebGL scene-click handling retries playback unlock on eligible non-UI clicks after connection. A later click can recover blocked playback. A browser microphone permission error and an autoplay block are separate conditions.

## Push-to-talk and reply completion

Use [Push-to-talk scripting reference](push-to-talk-api.md) for capture ownership instead of manually sequencing mute calls. A logical character turn can end before buffered audio finishes. Native `OnCharacterTurnPlaybackCompleted` reports a completed reply whose audio has finished; it is absent for replies without audio and on WebGL.

## Related pages

- [Configure microphone](../getting-started/configure-microphone.md)
- [Audio and microphone issues](../troubleshooting/audio-and-microphone-issues.md)
