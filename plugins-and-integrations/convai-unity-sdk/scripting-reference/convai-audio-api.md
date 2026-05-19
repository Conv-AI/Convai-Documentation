# convai audio api

`ConvaiAudio` is the facade for all audio control in the Convai Unity SDK. It manages microphone state, per-character audio muting, and the WebGL audio unlock flow. Access it via `ConvaiManager.ActiveManager.Audio`.

```csharp
var audio = ConvaiManager.ActiveManager.Audio;
```

***

## Microphone Control

### Properties

| Property     | Type   | Description                                 |
| ------------ | ------ | ------------------------------------------- |
| `IsMicMuted` | `bool` | True when the microphone is currently muted |

### Events

| Event              | Signature      | Fires When                                            |
| ------------------ | -------------- | ----------------------------------------------------- |
| `OnMicMuteChanged` | `Action<bool>` | Microphone mute state changes. Parameter: `(isMuted)` |

For C# hub–style access, `ConvaiEvents.OnMicMuteChanged` fires `MicMuteChanged` events. See [MicMuteChanged](convai-audio-api.md#micmutechanged-struct) below.

### Methods

| Method                                                                         | Returns                  | Description                                                                             |
| ------------------------------------------------------------------------------ | ------------------------ | --------------------------------------------------------------------------------------- |
| `SetMicMuted(bool muted)`                                                      | `void`                   | Sets the microphone mute state explicitly                                               |
| `ToggleMicMuted()`                                                             | `bool`                   | Toggles mute. Returns the new mute state (`true` = now muted)                           |
| `StartListeningAsync(int microphoneIndex = 0, CancellationToken ct = default)` | `IConvaiOperation<Unit>` | Starts microphone capture on the given device index. Resolves when listening is active. |
| `StopListeningAsync(CancellationToken ct = default)`                           | `IConvaiOperation<Unit>` | Stops microphone capture. Resolves when listening has stopped.                          |

```csharp
// Push-to-talk: start on button down, stop on button up
private async void OnPushToTalkDown()
{
    await ConvaiManager.ActiveManager.Audio.StartListeningAsync(ct: destroyCancellationToken);
}

private async void OnPushToTalkUp()
{
    await ConvaiManager.ActiveManager.Audio.StopListeningAsync(ct: destroyCancellationToken);
}
```

### `MicMuteChanged` Struct

Fired via `ConvaiEvents.OnMicMuteChanged` when mute state changes for any participant.

| Field                 | Type       | Description                                                  |
| --------------------- | ---------- | ------------------------------------------------------------ |
| `IsMuted`             | `bool`     | True when the participant is muted                           |
| `IsUnmuted`           | `bool`     | True when the participant is unmuted (`!IsMuted`)            |
| `IsLocalPlayer`       | `bool`     | True when this event describes the local player's microphone |
| `IsRemoteParticipant` | `bool`     | True when this event describes a remote participant          |
| `ParticipantId`       | `string`   | Room participant identifier                                  |
| `Timestamp`           | `DateTime` | UTC time of the mute change                                  |

***

## Per-Character Audio

These methods mute or enable individual characters by their `CharacterId`. Multiple characters can be independently muted.

### Methods

| Method                                                    | Returns | Description                                                                               |
| --------------------------------------------------------- | ------- | ----------------------------------------------------------------------------------------- |
| `MuteCharacter(string characterId)`                       | `bool`  | Mutes the character. Returns `true` if the character was found and muted.                 |
| `UnmuteCharacter(string characterId)`                     | `bool`  | Unmutes the character. Returns `true` if the character was found and unmuted.             |
| `SetCharacterMuted(string characterId, bool muted)`       | `bool`  | Sets mute state explicitly. Returns `true` if the character was found.                    |
| `IsCharacterMuted(string characterId)`                    | `bool`  | Returns the current mute state for the character. Returns `false` if character not found. |
| `SetRemoteAudioEnabled(string characterId, bool enabled)` | `bool`  | Enables or disables the character's remote audio stream. Returns `true` if found.         |
| `IsRemoteAudioEnabled(string characterId)`                | `bool`  | Returns whether the character's remote audio stream is enabled.                           |

### Events

| Event                         | Signature              | Fires When                                                                               |
| ----------------------------- | ---------------------- | ---------------------------------------------------------------------------------------- |
| `OnRemoteAudioEnabledChanged` | `Action<string, bool>` | A character's remote audio enabled state changes. Parameters: `(characterId, isEnabled)` |

```csharp
// Mute all characters except the active one
private void MuteAllExcept(string activeCharacterId)
{
    var audio = ConvaiManager.ActiveManager.Audio;
    foreach (var character in ConvaiManager.ActiveManager.Characters)
    {
        bool shouldMute = character.CharacterId != activeCharacterId;
        audio.SetCharacterMuted(character.CharacterId, shouldMute);
    }
}
```

***

## WebGL Audio Unlock

Browsers require a user gesture (click, tap, key press) before allowing audio playback. The SDK detects this requirement and exposes it through the following members.

### Properties

| Property                 | Type   | Description                                                                    |
| ------------------------ | ------ | ------------------------------------------------------------------------------ |
| `RequiresUserGesture`    | `bool` | True when the platform requires a user gesture before audio playback can start |
| `CanEnableAudioPlayback` | `bool` | True when `EnableAudioPlayback()` can be called — gesture has been received    |
| `IsAudioPlaybackActive`  | `bool` | True when audio playback is active and characters can produce audio            |

### Methods

| Method                  | Description                                                                                                            |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `EnableAudioPlayback()` | Unlocks audio playback. Must be called from a user-gesture handler — a button `onClick`, `OnPointerClick`, or similar. |

{% hint style="danger" %}
Calling `EnableAudioPlayback()` outside a user-gesture handler fails silently on most browsers. The audio context will remain suspended and characters will not produce any sound. Always gate this call on `RequiresUserGesture` and call it from within a UI click event.
{% endhint %}

```csharp
// Attach to a "Tap to Start" Button.onClick in the Inspector
public void OnStartButtonClicked()
{
    var audio = ConvaiManager.ActiveManager?.Audio;
    if (audio == null) return;

    if (audio.RequiresUserGesture)
        audio.EnableAudioPlayback();

    // Now safe to connect
    _ = ConvaiManager.ActiveManager.ConnectAsync(destroyCancellationToken);
}
```

***

## Usage Examples

### Example 1 — Push-To-Talk Button Implementation

A military training simulation uses a push-to-talk button that activates the microphone only while held, preventing ambient noise from interrupting the AI instructor.

{% code title="PushToTalkButton.cs" %}
```csharp
using Convai.Runtime.Facades;
using System.Threading;
using UnityEngine;
using UnityEngine.EventSystems;

public class PushToTalkButton : MonoBehaviour, IPointerDownHandler, IPointerUpHandler
{
    private CancellationTokenSource _listenCts;

    public async void OnPointerDown(PointerEventData _)
    {
        _listenCts?.Cancel();
        _listenCts = CancellationTokenSource.CreateLinkedTokenSource(destroyCancellationToken);

        await ConvaiManager.ActiveManager.Audio
            .StartListeningAsync(ct: _listenCts.Token);
    }

    public async void OnPointerUp(PointerEventData _)
    {
        _listenCts?.Cancel();

        await ConvaiManager.ActiveManager.Audio
            .StopListeningAsync(ct: destroyCancellationToken);
    }
}
```
{% endcode %}

### Example 2 — WebGL "Tap To Start" Overlay

An interactive experience on WebGL shows a full-screen overlay that blocks interaction until the user taps it, unlocking audio and connecting the session in a single user gesture.

{% code title="WebGLStartOverlay.cs" %}
```csharp
using Convai.Runtime.Facades;
using UnityEngine;

public class WebGLStartOverlay : MonoBehaviour
{
    [SerializeField] private GameObject _overlayRoot;

    private void Start()
    {
        var audio = ConvaiManager.ActiveManager?.Audio;
        _overlayRoot.SetActive(audio != null && audio.RequiresUserGesture);
    }

    // Assign to the overlay's Button.onClick in the Inspector
    public async void OnOverlayTapped()
    {
        var manager = ConvaiManager.ActiveManager;
        if (manager == null) return;

        manager.Audio.EnableAudioPlayback();
        _overlayRoot.SetActive(false);

        await manager.ConnectAsync(destroyCancellationToken);
    }
}
```
{% endcode %}

### Example 3 — Mute All Characters Except The Active Speaker

An industrial safety drill with multiple AI instructors mutes all characters when a new active speaker is designated, then unmutes only that speaker, ensuring learners always hear one voice at a time.

{% code title="SpeakerFocusController.cs" %}
```csharp
using Convai.Runtime.Components;
using Convai.Runtime.Facades;
using UnityEngine;

public class SpeakerFocusController : MonoBehaviour
{
    public void FocusOn(ConvaiCharacter speaker)
    {
        var manager = ConvaiManager.ActiveManager;
        if (manager == null) return;

        var audio = manager.Audio;

        foreach (var character in manager.Characters)
        {
            bool isSpeaker = character.CharacterId == speaker.CharacterId;
            audio.SetRemoteAudioEnabled(character.CharacterId, isSpeaker);
        }

        manager.SetExplicitConversationTarget(speaker);
    }
}
```
{% endcode %}

***

## Troubleshooting

| Symptom                                                                        | Likely Cause                                                       | Fix                                                                                                   |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| Microphone starts (`StartListeningAsync` resolves) but no audio reaches Convai | Microphone permissions not granted                                 | Call `TryGetPermissionService` and request mic permission before `StartListeningAsync` on Android/iOS |
| `RequiresUserGesture` is `true` on Windows standalone                          | Platform detection returning WebGL incorrectly in Editor Play mode | This is Editor-only behavior; test WebGL builds in a browser to confirm                               |
| `SetCharacterMuted` returns `false`                                            | Character ID not found — character may not yet be registered       | Wait for `ConvaiCharacter.OnCharacterReady` before muting                                             |
| Per-character mute resets after reconnect                                      | Mute state is not persisted across sessions                        | Re-apply mute in the `OnConnected` handler                                                            |
| WebGL: characters produce no audio after `EnableAudioPlayback()`               | Called outside a user-gesture handler                              | Move the call into a `Button.onClick` handler — not `Start()` or `Awake()`                            |

***

## Next Steps

{% content-ref url="/broken/pages/899573c6355c9e81274dd551dab24ec910d8459b" %}
[Broken link](/broken/pages/899573c6355c9e81274dd551dab24ec910d8459b)
{% endcontent-ref %}
