---
title: Configure audio
description: >-
  Set the default microphone device and configure ConvaiAudioOutput for
  character voice playback in your scene.
last_reviewed: "4.2.0"
---

The Convai SDK for Unity manages two audio paths: microphone input from the player, and voice output from the character. This page covers how to configure both, and how to handle platform-specific microphone permissions.

## Character audio output

`ConvaiAudioOutput` controls how a character's voice plays back in the scene. Add it to the same GameObject as `ConvaiCharacter`. An `AudioSource` on the same GameObject is required.

**Inspector fields:**

| Field          | Default | Description                               |
| -------------- | ------- | ----------------------------------------- |
| `Volume`       | `1.0`   | Playback volume (0–1)                     |
| `IsMuted`      | `false` | Mute this character's audio output        |
| `_use3DAudio`  | `true`  | Enable Unity spatial audio                |
| `_minDistance` | `1`     | Distance at which audio is at full volume |
| `_maxDistance` | `50`    | Distance at which audio falls to zero     |

Disable `_use3DAudio` for non-positional scenarios — for example, a kiosk interface where the character always sounds "present" regardless of where the player stands.

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

## Microphone device selection

To list available microphone devices and let the player choose one:

```csharp
using Convai.Runtime.Settings;

// Get the microphone device service from the SDK
if (ConvaiManager.ActiveManager.TryGetMicrophoneDeviceService(out IMicrophoneDeviceService micService))
{
    // List all available devices
    IReadOnlyList<ConvaiMicrophoneDevice> devices = micService.GetAvailableDevices();

    foreach (var device in devices)
    {
        Debug.Log($"{device.Name} (ID: {device.Id}, Index: {device.Index})");
    }

    // Start listening with a specific device index
    await ConvaiManager.ActiveManager.Audio.StartListeningAsync(microphoneIndex: device.Index);
}
```

{% hint style="warning" %}
On WebGL, `GetAvailableDevices()` returns an empty list outside the Editor. Microphone access on WebGL goes through the browser's Web Audio API and does not support Unity's native device enumeration.
{% endhint %}

## Platform-specific setup

### Android

The SDK requests microphone permission at runtime automatically when a recording starts. You must declare the permission in your `AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.RECORD_AUDIO" />
```

If your project does not have a custom manifest, create one or enable **Override Default Manifest** in **Player Settings > Publishing Settings**.

When the SDK requests the permission, Android shows its standard permission dialog. If the player grants it, recording starts automatically. If denied, the SDK logs a warning and the microphone remains inactive.

### iOS

Add a microphone usage description to your `Info.plist`. In Unity, set this via **Player Settings > iOS > Other Settings > Microphone Usage Description**:

```
"This app uses the microphone to support voice conversations with AI characters."
```

The SDK requests authorization automatically using Unity's `Application.RequestUserAuthorization`. The app does not need to call any permission API directly.

{% hint style="danger" %}
Submitting to the App Store without a microphone usage description will cause App Store review rejection. Set this value before building for iOS distribution.
{% endhint %}

### WebGL

Browsers block audio playback and microphone access until the user has interacted with the page. The SDK provides two methods depending on your use case:

* **`Audio.EnableAudioPlayback()`** — unlocks browser audio output only. Use this when you want character voice to play but are not yet starting the microphone (for example, during a tutorial before the player speaks).
* **`ConvaiManager.EnableAudioAndStartListening()`** — unlocks browser audio output **and** opens the microphone. Use this when the player is ready to begin a full conversation.

```csharp
// Call from a UI button's onClick event
public void OnStartButtonClicked()
{
    // Option A: unlock audio only (no microphone yet)
    if (ConvaiManager.ActiveManager.Audio.RequiresUserGesture)
    {
        ConvaiManager.ActiveManager.Audio.EnableAudioPlayback();
    }

    // Option B: unlock audio and open microphone in one step
    // ConvaiManager.ActiveManager.EnableAudioAndStartListening();
}
```

If you skip this step on WebGL, the character's voice will not play even though Convai sends audio data. `RequiresUserGesture` returns `true` only on WebGL.

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

With audio configured, add a transcript UI to display conversation text.

{% content-ref url="add-chat-ui.md" %}
[Add chat UI](add-chat-ui.md)
{% endcontent-ref %}
