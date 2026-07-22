---
title: Configure character audio
description: >-
  Configure per-character and project-wide voice volume, spatial audio, and
  audio feedback, and control playback in script with mute and unmute calls.
last_reviewed: "4.4.0"
---

The `ConvaiAudioOutput` component controls how a character's voice plays back in the scene, while `ConvaiSettings` sets the project-wide default volume and audio feedback behavior. Pair either with the `ConvaiAudio` facade on `ConvaiManager` for scripted runtime control of mute state, per-character volume, and audio events.

## Character audio output

Add `ConvaiAudioOutput` to the same GameObject as `ConvaiCharacter`. An `AudioSource` on the same GameObject is required.

**Inspector fields:**

| Field          | Default | Description                               |
| -------------- | ------- | ----------------------------------------- |
| `Volume`       | `1.0`   | Playback volume (0–1)                     |
| `IsMuted`      | `false` | Mute this character's audio output        |
| `_use3DAudio`  | `true`  | Enable Unity spatial audio                |
| `_minDistance` | `1`     | Distance at which audio is at full volume |
| `_maxDistance` | `50`    | Distance at which audio falls to zero     |

Disable `_use3DAudio` for non-positional scenarios — for example, a kiosk interface where the character always sounds "present" regardless of where the player stands.

## Project-wide audio defaults

`ConvaiSettings` exposes two project-wide defaults that apply until a script overrides them.

| Field                   | Default | Description                                                         |
| ----------------------- | ------- | -------------------------------------------------------------------- |
| `CharacterAudioVolume`  | `1`     | Default master volume for character audio (`0`–`1`)                  |
| `AudioFeedbackEnabled`  | `true`  | Plays feedback sounds, such as the listening indicator, by default   |

Configure both fields in the Convai Editor window's **Runtime Defaults** section (**Convai > Settings > Runtime Defaults**), or the equivalent **Edit > Project Settings > Convai SDK > Runtime Defaults** page — both surface the same fields.

These defaults seed `RuntimePreferences` when `ConvaiManager` builds its runtime. Read or change the effective value while a session is running through `ConvaiManager.ActiveManager.ConvaiRuntime.RuntimePreferences`:

```csharp
// Read the current project-wide defaults
float volume = ConvaiManager.ActiveManager.ConvaiRuntime.RuntimePreferences.CharacterAudioVolume;
bool audioFeedbackOn = ConvaiManager.ActiveManager.ConvaiRuntime.RuntimePreferences.AudioFeedbackEnabled;

// Override at runtime — CharacterAudioVolume clamps to the 0-1 range
ConvaiManager.ActiveManager.ConvaiRuntime.RuntimePreferences.CharacterAudioVolume = 0.5f;
ConvaiManager.ActiveManager.ConvaiRuntime.RuntimePreferences.AudioFeedbackEnabled = false;
```

{% hint style="warning" %}
`CharacterAudioVolume` does not change `ConvaiAudioOutput.Volume` on existing characters automatically. Read `RuntimePreferences.CharacterAudioVolume` in your own volume-control script and apply it to `ConvaiAudioOutput` or an audio mixer.
{% endhint %}

## Audio facade

For scripted audio control, use the `ConvaiAudio` facade accessed through `ConvaiManager.Audio`. This is the recommended API for runtime audio management.

### Microphone control

```csharp
// Mute/unmute the local microphone
ConvaiManager.ActiveManager.Audio.SetMicMuted(true);

// Toggle and get the new state
bool isMuted = ConvaiManager.ActiveManager.Audio.ToggleMicMuted();

// Start microphone capture manually (if ConnectOnStart is false)
await ConvaiManager.ActiveManager.Audio.StartListeningAsync();
```

### Per-character playback control

```csharp
string characterId = character.CharacterId;

// Mute a specific character
ConvaiManager.ActiveManager.Audio.MuteCharacter(characterId);

// Unmute
ConvaiManager.ActiveManager.Audio.UnmuteCharacter(characterId);

// Check mute state
bool muted = ConvaiManager.ActiveManager.Audio.IsCharacterMuted(characterId);

// Disable remote audio entirely for a character
ConvaiManager.ActiveManager.Audio.SetRemoteAudioEnabled(characterId, false);
```

### Audio events

```csharp
void OnEnable()
{
    ConvaiManager.ActiveManager.Audio.OnMicMuteChanged += HandleMicMuteChanged;
}

void OnDisable()
{
    ConvaiManager.ActiveManager.Audio.OnMicMuteChanged -= HandleMicMuteChanged;
}

void HandleMicMuteChanged(bool isMuted)
{
    muteButton.SetIsOnWithoutNotify(isMuted);
}
```

## Usage examples

### Example 1: Mute toggle UI button

**Scenario:** A corporate onboarding simulation includes a mic mute button in the corner of the screen.

```csharp
public class MuteButtonController : MonoBehaviour
{
    [SerializeField] private Toggle _muteToggle;

    void OnEnable()
    {
        _muteToggle.onValueChanged.AddListener(OnMuteToggled);
        ConvaiManager.ActiveManager.Audio.OnMicMuteChanged += OnMicMuteChanged;
    }

    void OnDisable()
    {
        _muteToggle.onValueChanged.RemoveListener(OnMuteToggled);
        ConvaiManager.ActiveManager.Audio.OnMicMuteChanged -= OnMicMuteChanged;
    }

    void OnMuteToggled(bool muted) =>
        ConvaiManager.ActiveManager.Audio.SetMicMuted(muted);

    void OnMicMuteChanged(bool muted) =>
        _muteToggle.SetIsOnWithoutNotify(muted);
}
```

**Expected outcome:** The toggle stays in sync with the actual microphone state. Pressing it mutes or unmutes the mic. External changes (for example, from push-to-talk logic) also update the toggle automatically.

### Example 2: Per-character volume in a multi-instructor scene

**Scenario:** A language learning simulation has two AI instructors — a main teacher and a conversation partner. Players can independently adjust their volumes.

```csharp
public class CharacterVolumeController : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _character;
    [SerializeField] private Slider _volumeSlider;

    void Start()
    {
        var audioOutput = _character.GetComponent<ConvaiAudioOutput>();
        _volumeSlider.value = audioOutput.Volume;
        _volumeSlider.onValueChanged.AddListener(v => audioOutput.Volume = v);
    }
}
```

**Expected outcome:** Each character's volume slider controls only that character's `AudioSource` volume. The two characters can be heard at different levels independently.

## Next steps

Configure the microphone device and platform-specific audio permissions.

{% content-ref url="configure-microphone.md" %}
[Configure microphone](configure-microphone.md)
{% endcontent-ref %}
