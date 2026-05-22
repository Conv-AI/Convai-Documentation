---
title: Audio API
description: Scripting reference for ConvaiAudio — microphone muting, per-character audio control, audio playback unlock, and listening state management.
last_reviewed: "4.2.0"
---

`ConvaiAudio` is the audio facade on `ConvaiManager`, providing scripted control over microphone capture, per-character remote audio output, and audio playback unlock. It separates concerns cleanly: microphone input (what you send to Convai), character audio output (what you hear from characters), and the WebGL audio playback gate.

**Access:** `ConvaiManager.ActiveManager.Audio`

```csharp
var audio = ConvaiManager.ActiveManager?.Audio;
if (audio == null) return; // manager not yet bootstrapped
```

***

## Microphone control

### Properties

| Property                 | Type   | Description                                                                 |
| ------------------------ | ------ | --------------------------------------------------------------------------- |
| `IsMicMuted`             | `bool` | True when the microphone is muted and not sending audio to Convai           |
| `RequiresUserGesture`    | `bool` | True when audio playback is blocked pending a user interaction (WebGL only) |
| `IsAudioPlaybackActive`  | `bool` | True when audio playback is currently active and unlocked                   |
| `CanEnableAudioPlayback` | `bool` | True when `EnableAudioPlayback()` can be called to unlock audio             |

### Methods

| Method                                                                         | Returns                  | Description                                             |
| ------------------------------------------------------------------------------ | ------------------------ | ------------------------------------------------------- |
| `SetMicMuted(bool muted)`                                                      | `void`                   | Sets microphone mute state explicitly                   |
| `ToggleMicMuted()`                                                             | `bool`                   | Toggles microphone mute. Returns the new mute state.    |
| `StartListeningAsync(int microphoneIndex = 0, CancellationToken ct = default)` | `IConvaiOperation<Unit>` | Starts microphone capture on the specified device index |
| `StopListeningAsync(CancellationToken ct = default)`                           | `IConvaiOperation<Unit>` | Stops microphone capture                                |

{% hint style="info" %}
The `microphoneIndex` parameter in `StartListeningAsync` corresponds to an index into the list returned by `IMicrophoneDeviceService.GetAvailableDevices()`. Use `ConvaiManager.ActiveManager.TryGetMicrophoneDeviceService(out var svc)` to enumerate devices by name before selecting an index. Index `0` uses the system default microphone.
{% endhint %}

### Events

| Event              | Signature      | Fires When                                                               |
| ------------------ | -------------- | ------------------------------------------------------------------------ |
| `OnMicMuteChanged` | `Action<bool>` | Microphone mute state changes. Parameter: new mute state (true = muted). |

```csharp
using Convai.Runtime.Facades;
using UnityEngine;

public class MicMuteIndicator : MonoBehaviour
{
    [SerializeField] private GameObject _muteIcon;

    private void OnEnable()
    {
        var audio = ConvaiManager.ActiveManager?.Audio;
        if (audio == null) return;
        audio.OnMicMuteChanged += OnMuteChanged;
        _muteIcon.SetActive(audio.IsMicMuted);
    }

    private void OnDisable()
    {
        var audio = ConvaiManager.ActiveManager?.Audio;
        if (audio != null)
            audio.OnMicMuteChanged -= OnMuteChanged;
    }

    private void OnMuteChanged(bool isMuted) => _muteIcon.SetActive(isMuted);
}
```

***

## Per-character audio control

These methods control whether a specific character's audio output plays locally. Use character IDs from `ConvaiCharacter.CharacterId` or `ConvaiManager.ActiveManager.Characters`.

| Method                                                    | Returns | Description                                                                         |
| --------------------------------------------------------- | ------- | ----------------------------------------------------------------------------------- |
| `SetCharacterMuted(string characterId, bool muted)`       | `bool`  | Sets mute state for a specific character. Returns `true` if the change was applied. |
| `MuteCharacter(string characterId)`                       | `bool`  | Mutes a specific character's audio output. Returns `true` if applied.               |
| `UnmuteCharacter(string characterId)`                     | `bool`  | Unmutes a specific character's audio output. Returns `true` if applied.             |
| `IsCharacterMuted(string characterId)`                    | `bool`  | Returns `true` if the character's audio output is currently muted.                  |
| `SetRemoteAudioEnabled(string characterId, bool enabled)` | `bool`  | Enables or disables remote audio output for a character. Returns `true` if applied. |
| `IsRemoteAudioEnabled(string characterId)`                | `bool`  | Returns `true` if this character's remote audio output is enabled.                  |

{% hint style="info" %}
**Mute vs. remote audio enabled:** These are separate controls. Remote audio enabled/disabled controls whether the SDK streams audio output for the character at all. Muting controls whether the locally received audio plays through your audio output device. Disabling remote audio saves bandwidth; muting is a local-only volume control.
{% endhint %}

### Events

| Event                         | Signature              | Fires When                                                                            |
| ----------------------------- | ---------------------- | ------------------------------------------------------------------------------------- |
| `OnRemoteAudioEnabledChanged` | `Action<string, bool>` | A character's remote audio enabled state changes. Parameters: characterId, isEnabled. |

***

## Audio playback — WebGL

On WebGL, browsers block audio playback until the user has interacted with the page. The SDK gates audio output behind this requirement.

| Member                   | Type   | Description                                                                                         |
| ------------------------ | ------ | --------------------------------------------------------------------------------------------------- |
| `RequiresUserGesture`    | `bool` | True when audio is blocked pending user interaction                                                 |
| `CanEnableAudioPlayback` | `bool` | True when `EnableAudioPlayback()` can be called                                                     |
| `IsAudioPlaybackActive`  | `bool` | True when audio playback is unlocked and active                                                     |
| `EnableAudioPlayback()`  | `void` | Unlocks audio playback. **Must be called from inside a user gesture handler** (button click, etc.). |

{% hint style="danger" %}
On WebGL, calling `EnableAudioPlayback()` outside of a user gesture handler (e.g., in `Start()` or `OnEnable()`) has no effect — the browser will block the unlock. Wire it to a UI button's `onClick` event or call it inside `OnPointerClick`.
{% endhint %}

```csharp
using Convai.Runtime.Facades;
using UnityEngine;
using UnityEngine.UI;

public class WebGLStartButton : MonoBehaviour
{
    [SerializeField] private Button     _startButton;
    [SerializeField] private GameObject _startPanel;

    private void OnEnable()  => _startButton.onClick.AddListener(OnStartClicked);
    private void OnDisable() => _startButton.onClick.RemoveListener(OnStartClicked);

    private void OnStartClicked()
    {
        var audio = ConvaiManager.ActiveManager?.Audio;
        if (audio == null) return;

        // Unlock audio inside the user gesture
        if (audio.CanEnableAudioPlayback)
            audio.EnableAudioPlayback();

        // Connect and start listening
        ConvaiManager.ActiveManager.EnableAudioAndStartListening();

        _startPanel.SetActive(false);
    }
}
```

***

## Usage examples

### Example 1 — Mute button in a training simulation HUD

A military training simulation provides a push-button microphone mute in the HUD so trainees can mute themselves before speaking to the observer, without disconnecting.

```csharp
using Convai.Runtime.Facades;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class MuteButton : MonoBehaviour
{
    [SerializeField] private Button   _button;
    [SerializeField] private TMP_Text _label;

    private void OnEnable()
    {
        _button.onClick.AddListener(OnClicked);
        var audio = ConvaiManager.ActiveManager?.Audio;
        if (audio != null)
        {
            audio.OnMicMuteChanged += RefreshLabel;
            RefreshLabel(audio.IsMicMuted);
        }
    }

    private void OnDisable()
    {
        _button.onClick.RemoveListener(OnClicked);
        var audio = ConvaiManager.ActiveManager?.Audio;
        if (audio != null)
            audio.OnMicMuteChanged -= RefreshLabel;
    }

    private void OnClicked() => ConvaiManager.ActiveManager?.Audio?.ToggleMicMuted();

    private void RefreshLabel(bool isMuted) =>
        _label.text = isMuted ? "Unmute" : "Mute";
}
```

### Example 2 — Per-character audio toggle in a multi-NPC assessment scene

A corporate onboarding simulation has two AI instructors. An assessment manager script mutes the secondary instructor during the primary instructor's evaluation segment, then restores both.

```csharp
using Convai.Runtime.Components;
using Convai.Runtime.Facades;
using System.Collections;
using UnityEngine;

public class AssessmentAudioManager : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _primaryInstructor;
    [SerializeField] private ConvaiCharacter _secondaryInstructor;

    public void BeginPrimaryEvaluation()
    {
        var audio = ConvaiManager.ActiveManager?.Audio;
        if (audio == null) return;

        // Mute secondary so only primary is heard
        audio.MuteCharacter(_secondaryInstructor.CharacterId);
        audio.UnmuteCharacter(_primaryInstructor.CharacterId);
    }

    public void RestoreBothInstructors()
    {
        var audio = ConvaiManager.ActiveManager?.Audio;
        if (audio == null) return;

        audio.UnmuteCharacter(_primaryInstructor.CharacterId);
        audio.UnmuteCharacter(_secondaryInstructor.CharacterId);
    }
}
```

### Example 3 — Microphone device selection before connect

An interactive experience lets users pick their preferred microphone from a dropdown before the session starts, then starts listening on the selected device.

```csharp
using Convai.Runtime.Facades;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class MicrophoneSelector : MonoBehaviour
{
    [SerializeField] private TMP_Dropdown _dropdown;

    private List<string> _deviceNames = new();

    private void Start()
    {
        var manager = ConvaiManager.ActiveManager;
        if (manager == null || !manager.TryGetMicrophoneDeviceService(out var svc)) return;

        _deviceNames.Clear();
        _dropdown.ClearOptions();

        foreach (var device in svc.GetAvailableDevices())
        {
            _deviceNames.Add(device.Name);
            _dropdown.options.Add(new TMP_Dropdown.OptionData(device.Name));
        }

        _dropdown.RefreshShownValue();
    }

    public async void OnConfirmDevice()
    {
        int index = _dropdown.value;
        var audio = ConvaiManager.ActiveManager?.Audio;
        if (audio == null) return;

        await audio.StartListeningAsync(index, destroyCancellationToken);
        Debug.Log($"Listening on: {_deviceNames[index]}");
    }
}
```

***

## Troubleshooting

| Symptom                                                            | Likely Cause                                                                                         | Fix                                                                                                                                      |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| No audio output on WebGL                                           | `EnableAudioPlayback()` not called inside a user gesture                                             | Wire `EnableAudioPlayback()` to a button's `onClick`; do not call in `Start()` or `Awake()`                                              |
| `ToggleMicMuted()` returns `true` but character still hears player | `IsMicMuted` controls SDK mute — verify character session is connected and audio pipeline is running | Check `IsSessionConnected` on the active character; mute only takes effect mid-session                                                   |
| `MuteCharacter()` returns `false`                                  | Character ID not recognized — character may not be registered                                        | Verify the ID matches `ConvaiCharacter.CharacterId`; the character must be in `ConvaiManager.Characters`                                 |
| `StartListeningAsync` fails on mobile                              | Platform microphone permission not granted                                                           | Use `TryGetPermissionService` to request microphone permission before calling `StartListeningAsync`                                      |
| `IsRemoteAudioEnabled` returns `false` after connect               | `EnableRemoteAudioOnStart` on the character is `false`                                               | Set `ConvaiCharacter.EnableRemoteAudioOnStart = true` in the Inspector, or call `character.EnableRemoteAudio()` after the session starts |

***

## Next steps

For per-character audio events and session control, see [Character & Player API](character-and-player-api.md). For WebGL-specific audio requirements and limitations, see the [WebGL Platform Guide](../platform-guides/webgl.md). For connection and session control, see [ConvaiManager API](convaimanager-api.md).
