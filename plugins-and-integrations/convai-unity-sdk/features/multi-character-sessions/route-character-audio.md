---
title: Route audio for each character
description: Control the shared room microphone, bind and mute each character's audio by identity, and measure character playback in Unity.
last_reviewed: "4.6.0"
---

Control microphone capture, bind an `AudioSource` per participant, mute or disable a character's playback, and read a character's playback position in a multi-character session with `IConvaiRoomAudioService`. Use this page once your room is connected and its memberships have started reporting participant identities.

## Prerequisites

- A connected multi-character session. See [Build your first multi-character session](quick-start.md).
- `IConvaiRoomAudioService`, retrieved with `ConvaiManager.TryGetRoomAudioService(out IConvaiRoomAudioService audioService)`, for `BindParticipantAudioOutput`, `SetParticipantAudioEnabled`, and `TryGetCharacterAudioPlayhead`. The mute, remote-audio, and WebGL playback members below are also available through the `ConvaiManager.Audio` convenience facade.
- One `AudioSource` per character you want to hear independently.

## Control the room microphone

The microphone is room-scoped: one capture device feeds the whole room, and it is not bound to any single character. `IsMicMuted` reports whether it is currently muted, and `SetMicMuted(bool muted)` mutes or unmutes it. Subscribe to `MicMuteChanged` (`Action<bool>`) to react whenever the state changes, whether your own code changed it or something else did. The facade prefixes its events with `On`, so the same event is `ConvaiManager.Audio.OnMicMuteChanged`.

Muting the microphone does not decide which character the player is addressing. That routing is a separate decision made by the interaction target — see [Switch the interaction target](switch-the-interaction-target.md) to change who receives the player's speech once the microphone is unmuted.

```csharp
ConvaiManager manager = ConvaiManager.ActiveManager;
manager.Audio.SetMicMuted(true);
```

## Bind an AudioSource to each character

Call `BindParticipantAudioOutput(string participantIdentity, AudioSource audioSource)` once per character, using the `ParticipantIdentity` from that character's `CharacterRoomMembership`. It returns `false` when `participantIdentity` is empty, so check the return value rather than assuming the bind succeeded.

{% code title="Assets/Scripts/MultiCharacterAudioBinder.cs" %}
```csharp
using Convai.Runtime.Room;
using UnityEngine;

public class MultiCharacterAudioBinder : MonoBehaviour
{
    [SerializeField] private AudioSource[] _characterAudioSources;

    public void BindRoomAudio(MultiCharacterRoomSession session, IConvaiRoomAudioService audioService)
    {
        for (int i = 0; i < session.Characters.Count && i < _characterAudioSources.Length; i++)
        {
            CharacterRoomMembership membership = session.Characters[i];
            if (string.IsNullOrEmpty(membership.ParticipantIdentity))
            {
                Debug.LogWarning($"[MultiCharacter] {membership.CharacterId} has no participant identity yet.");
                continue;
            }

            audioService.BindParticipantAudioOutput(membership.ParticipantIdentity, _characterAudioSources[i]);
        }
    }
}
```
{% endcode %}

{% hint style="warning" %}
While a multi-character session is active, an incoming audio track is matched to a membership through the membership index only. A track that resolves to no membership is not attached to any `AudioSource` — there is no fallback to matching by `CharacterId`. Bind by `ParticipantIdentity`, never by `CharacterId`.
{% endhint %}

Call `SetParticipantAudioEnabled(string participantIdentity, bool enabled)` to mute or unmute a bound participant without unbinding its `AudioSource`. It returns `false` when no `AudioSource` has been bound for that identity yet — bind it first.

```csharp
// Silence a secondary character without unbinding it
audioService.SetParticipantAudioEnabled(secondaryMembership.ParticipantIdentity, false);
```

## Route audio for other humans in the room

`BindParticipantAudioOutput` and `SetParticipantAudioEnabled` also cover other humans present in the room, such as a second participant who joined with [Join an existing multi-character session](join-an-existing-session.md). Human participant identities use the backend form `human:{speaker_id}`, so a scene that renders another learner's voice through a spatial `AudioSource` binds it exactly the way it binds a character.

```csharp
audioService.BindParticipantAudioOutput("human:learner-43", _otherLearnerAudioSource);
```

## Mute or disable one character's playback

`SetCharacterMuted(string characterId, bool muted)` and `IsCharacterMuted(string characterId)` control local playback volume without changing what arrives over the network — the character's audio track keeps streaming, and only local output is silenced. `SetRemoteAudioEnabled(string characterId, bool enabled)` and `IsRemoteAudioEnabled(string characterId)` go further: disabling unsubscribes the character's track entirely, so no audio packets are received for it at all. Muting is a volume decision; disabling is a bandwidth decision. Subscribe to `RemoteAudioEnabledChanged` (`Action<string, bool>`, character ID then the new enabled state) to react whenever either your own code or something else changes it. On the facade the same event is `ConvaiManager.Audio.OnRemoteAudioEnabledChanged`.

```csharp
// Silence a character locally, but keep receiving its track
manager.Audio.SetCharacterMuted(characterId, true);

// Stop receiving a character's track entirely
manager.Audio.SetRemoteAudioEnabled(characterId, false);
```

{% hint style="warning" %}
`SetCharacterMuted`, `IsCharacterMuted`, `SetRemoteAudioEnabled`, `IsRemoteAudioEnabled`, and `TryGetCharacterAudioPlayhead` are all keyed by `characterId`, which is not unique in a room containing two memberships that share a `CharacterId` — see [Why a character ID is not an address](character-identity.md#why-a-character-id-is-not-an-address). Each resolves to the first membership carrying that character ID, so none of them can target one instance once a clone is present in the room. Use `BindParticipantAudioOutput` and `SetParticipantAudioEnabled`, keyed by `ParticipantIdentity`, whenever the room may contain clones — they are the only participant-level controls precise enough for that case.
{% endhint %}

## Enable playback on platforms that require a user gesture

Some platforms, including WebGL, require a user gesture before audio playback can start. Check whether the current platform needs that gesture — the property is `RequiresUserGestureForAudio` on `IConvaiRoomAudioService` and `RequiresUserGesture` on the `ConvaiManager.Audio` facade — and `IsAudioPlaybackActive` to know whether playback is already running. Call `EnableAudioPlayback()` after the required gesture, typically from a UI event handler tied to a click or tap. `CanEnableAudioPlayback` reports whether the conditions for a successful call are currently met, so a button can disable itself until they are.

```csharp
public void OnEnableAudioButtonClicked()
{
    if (manager.Audio.CanEnableAudioPlayback)
        manager.Audio.EnableAudioPlayback();
}
```

## Measure a character's playback position

`TryGetCharacterAudioPlayhead(string characterId, out double playedSeconds)` reads how many seconds of a character's audio have actually been rendered to the output device since its current playback signal started. Like the mute controls above, it is keyed by `characterId` and resolves to the first matching membership, so it cannot measure one clone separately from another. The playhead freezes during an underrun and accounts for any drift-correction skips, so it reflects what the player actually heard rather than a wall-clock estimate. The method returns `false` when the current platform's audio stream does not expose a playhead — fall back to a wall-clock timer in that case rather than treating `playedSeconds` as valid.

```csharp
if (audioService.TryGetCharacterAudioPlayhead(characterId, out double playedSeconds))
    Debug.Log($"[MultiCharacter] {characterId} has played {playedSeconds:F2}s.");
```

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `BindParticipantAudioOutput` returns `false` | `participantIdentity` was empty when the call ran. | Wait for the membership's `CharacterStatusChanged` or `CharacterAdded` event before binding, then read `ParticipantIdentity` again. |
| `SetParticipantAudioEnabled` returns `false` | No `AudioSource` is bound for that participant identity. | Call `BindParticipantAudioOutput` for that identity first. |
| A secondary character produces no audio even after binding | The bound identity does not match the membership's actual `ParticipantIdentity`, often from binding by `CharacterId` instead. | Re-read `CharacterRoomMembership.ParticipantIdentity` from `session.Characters` and rebind. |
| `SetCharacterMuted` or `SetRemoteAudioEnabled` appears to affect the wrong instance | The room holds two memberships sharing one `CharacterId`, and the character-ID-keyed call cannot distinguish them. | Switch to `SetParticipantAudioEnabled`, keyed by `ParticipantIdentity`, for that character. |
| `EnableAudioPlayback` has no effect | `CanEnableAudioPlayback` was `false` when the call ran. | Check `CanEnableAudioPlayback` before calling, and trigger `EnableAudioPlayback` from a UI click or tap handler on platforms where `RequiresUserGestureForAudio` is `true`. |
| `TryGetCharacterAudioPlayhead` returns `false` | The current platform's audio stream does not expose a playhead. | Track elapsed time with a wall-clock timer instead. |

## Next steps

{% content-ref url="character-identity.md" %}
[Character identity and addressing](character-identity.md)
{% endcontent-ref %}

{% content-ref url="handle-roster-events.md" %}
[React to roster and target changes](handle-roster-events.md)
{% endcontent-ref %}

{% content-ref url="switch-the-interaction-target.md" %}
[Switch the interaction target](switch-the-interaction-target.md)
{% endcontent-ref %}
