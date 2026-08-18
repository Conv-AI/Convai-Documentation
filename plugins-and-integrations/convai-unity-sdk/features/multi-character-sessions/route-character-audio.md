---
title: Route audio for each character
description: Bind one audio source per participant identity in a shared Unity room, then enable or silence each character or human independently.
last_reviewed: "4.6.0"
---

Bind a Unity `AudioSource` to each character's audio in a multi-character session with `BindParticipantAudioOutput`, keyed by participant identity rather than character ID. Use this page once your room is connected and its memberships have started reporting participant identities.

## Prerequisites

- A connected multi-character session. See [Build your first multi-character session](quick-start.md).
- `IConvaiRoomAudioService`, retrieved with `ConvaiManager.TryGetRoomAudioService`.
- One `AudioSource` per character you want to hear independently.

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

## Enable or silence one participant

Call `SetParticipantAudioEnabled(string participantIdentity, bool enabled)` to mute or unmute a bound participant without unbinding its `AudioSource`. It returns `false` when no `AudioSource` has been bound for that identity yet — bind it first.

```csharp
// Silence a secondary character without unbinding it
audioService.SetParticipantAudioEnabled(secondaryMembership.ParticipantIdentity, false);
```

## Route audio for other humans in the room

The same two methods cover other humans present in the room, such as a second participant who joined with [Join an existing multi-character session](join-an-existing-session.md). Human participant identities use the backend form `human:{speaker_id}`, so a scene that renders another learner's voice through a spatial `AudioSource` binds it exactly the way it binds a character.

```csharp
audioService.BindParticipantAudioOutput("human:learner-43", _otherLearnerAudioSource);
```

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `BindParticipantAudioOutput` returns `false` | `participantIdentity` was empty when the call ran. | Wait for the membership's `CharacterStatusChanged` or `CharacterAdded` event before binding, then read `ParticipantIdentity` again. |
| `SetParticipantAudioEnabled` returns `false` | No `AudioSource` is bound for that participant identity. | Call `BindParticipantAudioOutput` for that identity first. |
| A secondary character produces no audio even after binding | The bound identity does not match the membership's actual `ParticipantIdentity`, often from binding by `CharacterId` instead. | Re-read `CharacterRoomMembership.ParticipantIdentity` from `session.Characters` and rebind. |

## Next steps

{% content-ref url="character-identity.md" %}
[Character identity and addressing](character-identity.md)
{% endcontent-ref %}

{% content-ref url="handle-roster-events.md" %}
[React to roster and target changes](handle-roster-events.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[Build your first multi-character session](quick-start.md)
{% endcontent-ref %}
