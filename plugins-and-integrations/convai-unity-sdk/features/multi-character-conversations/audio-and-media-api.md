---
title: Multi-character audio and media API
description: Reference microphone, character, participant, playback, and audio playhead controls for multi-character rooms in the Unity SDK.
last_reviewed: "4.6.0"
---

`IConvaiRoomAudioService` controls microphone input, character audio subscription and mute state, participant output routing, platform playback, and rendered audio playheads for the current room.

## Access the audio surfaces

Use `ConvaiManager.Audio` for common microphone and character controls. Resolve `IConvaiRoomAudioService` when an integration needs participant output binding or audio playhead access.

```csharp
using Convai.Runtime.Components;
using Convai.Runtime.Room;
using UnityEngine;

public sealed class MultiCharacterAudioStatus : MonoBehaviour
{
    public void LogMicrophoneStatus()
    {
        ConvaiManager manager = ConvaiManager.ActiveManager;
        if (manager != null &&
            manager.TryGetRoomAudioService(out IConvaiRoomAudioService audioService))
            Debug.Log($"Microphone muted: {audioService.IsMicMuted}");
    }
}
```

| Surface | Includes |
| --- | --- |
| `ConvaiManager.Audio` | Microphone methods, character mute and subscription methods, playback properties, playback enablement, and convenience toggle methods |
| `IConvaiRoomAudioService` | All facade capabilities plus `BindParticipantAudioOutput`, `SetParticipantAudioEnabled`, and `TryGetCharacterAudioPlayhead` |

## Microphone properties and events

| Member | Type | Description |
| --- | --- | --- |
| `IsMicMuted` | `bool` | Whether the local microphone is muted |
| `RequiresUserGestureForAudio` | `bool` | Whether the platform requires a user gesture before playback starts |
| `IsAudioPlaybackActive` | `bool` | Whether audio playback is active |
| `CanEnableAudioPlayback` | `bool` | Whether `EnableAudioPlayback` can currently enable playback |
| `MicMuteChanged` | `Action<bool>` | Raised when local microphone mute state changes |
| `RemoteAudioEnabledChanged` | `Action<string, bool>` | Raised when remote audio enablement changes for a character ID |

The high-level facade names the corresponding events `OnMicMuteChanged` and `OnRemoteAudioEnabledChanged`. It names `RequiresUserGestureForAudio` as `RequiresUserGesture`.

## Microphone methods

```csharp
IConvaiOperation<Unit> StartListeningAsync(
    int microphoneIndex = 0,
    CancellationToken cancellationToken = default);

IConvaiOperation<Unit> StopListeningAsync(
    CancellationToken cancellationToken = default);

void SetMicMuted(bool muted);
```

`StartListeningAsync` starts capture on the zero-based microphone device index and publishes the local audio track. `StopListeningAsync` stops capture and unpublishes the track. Microphone state belongs to the local room participant, not to an individual character.

## Character audio methods

```csharp
bool SetCharacterMuted(string characterId, bool muted);
bool IsCharacterMuted(string characterId);
bool SetRemoteAudioEnabled(string characterId, bool enabled);
bool IsRemoteAudioEnabled(string characterId);
```

Muting controls local playback for the character's resolved output. Remote audio enablement controls track subscription: disabling it stops receiving that character's remote audio packets, while enabling it subscribes and routes the track to the character output.

All four methods are keyed by character ID. They return `false` when the ID is empty or the SDK cannot resolve the required character or audio state.

{% hint style="warning" %}
Use distinct character IDs when independent audio control is required. Character-ID-keyed methods cannot promise independent control for repeated character IDs.
{% endhint %}

## Participant output methods

```csharp
bool BindParticipantAudioOutput(
    string participantIdentity,
    AudioSource audioSource);

bool SetParticipantAudioEnabled(
    string participantIdentity,
    bool enabled);
```

`BindParticipantAudioOutput` associates an exact LiveKit participant identity with an application-owned `AudioSource`. Pass `null` as `audioSource` to remove an existing binding. The method returns `false` for an empty identity. Create the binding before that participant's remote audio track is subscribed; an existing stream is not rerouted by a later binding.

For a character, use `CharacterRoomMembership.ParticipantIdentity`. Human participant identities use the form `human:{speaker_id}`. Human participant routing is a multiplayer integration boundary and is not required for a multi-NPC room owned by one local player.

`SetParticipantAudioEnabled` sets the bound `AudioSource.mute` state. It returns `false` if the identity is empty or no non-null output is bound. It does not change the character-ID remote subscription preference.

## Audio playback on WebGL

```csharp
void EnableAudioPlayback();
```

On WebGL, call `EnableAudioPlayback` from a user gesture handler, such as a Unity UI button callback. Check `RequiresUserGestureForAudio` and `CanEnableAudioPlayback` before presenting the unlock control. `IsAudioPlaybackActive` reports whether playback is active after the gate is released.

{% hint style="danger" %}
Calling `EnableAudioPlayback` from `Start` or another non-gesture callback does not satisfy browser autoplay policy. Keep the call inside the user's click or tap handler.
{% endhint %}

## Character audio playhead

```csharp
bool TryGetCharacterAudioPlayhead(
    string characterId,
    out double playedSeconds);
```

`playedSeconds` measures source audio rendered to the output device since the current playback signal began. The value freezes during an underrun and accounts for drift-correction skips.

The method returns `false` when the character ID is empty, no audio manager is available, or the platform stream does not expose a playhead. Fall back to a wall clock when it returns `false`.

## Routing and lifecycle constraints

- Character output normally routes through the local character instance and its assigned `AudioSource`.
- Participant output binding takes precedence for a track whose exact participant identity has a binding.
- `SetCharacterMuted` is local mute state. `SetRemoteAudioEnabled` changes remote track subscription.
- `SetParticipantAudioEnabled` changes only the bound output's mute state.
- Clearing the interaction target does not stop audio already playing.
- Reacquire membership identities after reconnect. Rebind an output when its participant identity changed for the new connection.

## Related reference

See the general audio facade reference for convenience methods and microphone-device selection.

{% content-ref url="../../scripting-reference/audio-api.md" %}
[Audio API](../../scripting-reference/audio-api.md)
{% endcontent-ref %}

Review the platform setup and browser playback gate before building for WebGL.

{% content-ref url="../../platform-guides/webgl.md" %}
[WebGL](../../platform-guides/webgl.md)
{% endcontent-ref %}
