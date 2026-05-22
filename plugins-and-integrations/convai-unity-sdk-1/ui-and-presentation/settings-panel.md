---
title: Settings panel
description: >-
  Add a runtime settings panel so users can adjust microphone, transcript mode,
  and notification preferences, or access the same settings programmatically.
last_reviewed: "4.2.0"
---

The settings panel is an optional scene-level UI that lets users adjust key conversation preferences at runtime. The underlying settings service, `IConvaiRuntimeSettingsService`, is also a standalone scripting API — you can read current settings, apply patches, and subscribe to changes from code without the panel being present.

## Controllable settings

| Setting | Description |
| --- | --- |
| **Player Display Name** | The name shown in transcript bubbles for the player |
| **Transcript** | Enable or disable the transcript UI entirely |
| **Notifications** | Enable or disable in-scene notification popups |
| **Microphone** | Select the active input device from available options |
| **Conversation Mode** | Switch between Hands Free and Push to Talk (shown only when a room connection is active) |

Changes apply when the user clicks **Save**. The panel closes automatically on save. Clicking **Close** discards unsaved changes.

## Add the settings panel to your scene

{% stepper %}
{% step %}
### Add the prefab to your Canvas

Drag `SettingsPanel_Landscape.prefab` into your scene's Canvas hierarchy. Find it at `Prefabs/SettingsPanel/SettingsPanel_Landscape.prefab` in the <code class="expression">space.vars.sdk_package_id</code> package.

`SettingsPanel` auto-resolves all required services from `ConvaiManager` on `OnEnable`. No additional Inspector wiring is required for the basic setup.

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Unity scene hierarchy with the Canvas GameObject expanded. The image must show `SettingsPanel_Landscape` as a child of the Canvas.
{% endhint %}

<figure><img src="../../../.gitbook/assets/TODO-settings-panel-hierarchy.png" alt="Unity scene hierarchy showing SettingsPanel_Landscape as a child of a Canvas GameObject"><figcaption><p>TODO: Replace with screenshot showing SettingsPanel_Landscape inside the scene Canvas hierarchy.</p></figcaption></figure>
{% endstep %}

{% step %}
### Connect a trigger to open the panel

The panel starts hidden. Wire a button, keyboard shortcut, or pause menu to open it:

```csharp
using Convai.Runtime.Components;
using UnityEngine;
using UnityEngine.UI;

public class SettingsButton : MonoBehaviour
{
    private void Start()
    {
        GetComponent<Button>().onClick.AddListener(() =>
        {
            if (ConvaiManager.ActiveManager.TryGetSettingsPanelController(out var c))
                c.Open();
        });
    }
}
```
{% endstep %}

{% step %}
### Run your scene

Click the trigger. The panel fades in (default 0.5s). Adjust settings and click **Save** — the panel fades out and changes apply immediately. The microphone dropdown populates from available system devices; the conversation mode dropdown appears only while a room connection is active.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
When the panel opens correctly, the microphone dropdown is populated, the player name field shows the current display name, and the transcript and notification toggles reflect their current state.
{% endhint %}

## `SettingsPanel` inspector reference

| Field | Description |
| --- | --- |
| `fadeDuration` | Seconds for fade in/out animation (default `0.5`) |
| `transcriptStyleDropdown` | `TMP_Dropdown` for the transcript display mode |
| `voiceInputDropdown` | `TMP_Dropdown` listing available microphone devices |
| `conversationModeDropdown` | `TMP_Dropdown` for Hands Free / Push to Talk |
| `playerNameInputField` | `TMP_InputField` for the player's display name |
| `transcriptToggle` | `Toggle` enabling or disabling the transcript UI |
| `notificationToggle` | `Toggle` enabling or disabling notifications |
| `saveButton` | `Button` applying all changes and closing the panel |
| `closeButton` | `Button` closing without saving |
| `microphoneDropContainer` | `GameObject` wrapping the microphone dropdown — hidden when no devices found |
| `transcriptModeContainer` | `GameObject` wrapping the transcript style dropdown |
| `conversationModeContainer` | `GameObject` wrapping the conversation mode dropdown — hidden when no room service available |

## `IConvaiSettingsPanelController` — visibility API

Access the panel controller through `ConvaiManager`:

```csharp
ConvaiManager.ActiveManager.TryGetSettingsPanelController(out var controller);
```

| Member | Description |
| --- | --- |
| `bool IsOpen` | `true` when the panel is currently visible |
| `void Open()` | Show the panel with fade animation |
| `void Close()` | Hide the panel with fade animation |
| `void Toggle()` | Open if closed, close if open |
| `event Action<bool> VisibilityChanged` | Fires when visibility changes. `bool` parameter is the new `IsOpen` value |

## Runtime settings API — `IConvaiRuntimeSettingsService`

The settings panel is a UI view over the runtime settings service. You can access the same API directly from any script — reading current values, applying changes, and reacting to changes without opening the panel.

### Read current settings

`IConvaiRuntimeSettingsService.Current` returns a `ConvaiRuntimeSettingsSnapshot` — an immutable struct with all current values.

```csharp
if (ConvaiManager.ActiveManager.TryGetRuntimeSettingsService(out var settings))
{
    ConvaiRuntimeSettingsSnapshot current = settings.Current;
    Debug.Log($"Player name: {current.PlayerDisplayName}");
    Debug.Log($"Transcript on: {current.TranscriptEnabled}");
    Debug.Log($"Mode: {current.TranscriptMode}");
}
```

**`ConvaiRuntimeSettingsSnapshot` fields:**

| Field | Type | Description |
| --- | --- | --- |
| `PlayerDisplayName` | `string` | Current player display name |
| `TranscriptEnabled` | `bool` | Whether transcript UI is enabled |
| `NotificationsEnabled` | `bool` | Whether notifications are enabled |
| `PreferredMicrophoneDeviceId` | `string` | ID of the preferred microphone device |
| `TranscriptMode` | `ConvaiTranscriptMode` | Current transcript display mode |

### Apply changes

`Apply(ConvaiRuntimeSettingsPatch)` applies changes atomically. Any field left `null` in the patch remains unchanged.

```csharp
var result = settings.Apply(new ConvaiRuntimeSettingsPatch
{
    PlayerDisplayName = "Dr. Kaan",
    TranscriptEnabled = true,
    TranscriptMode = ConvaiTranscriptMode.Subtitle
});

if (!result.Success)
    Debug.LogWarning($"Settings apply failed: {result.ValidationMessage}");
```

**`ConvaiRuntimeSettingsApplyResult` fields:**

| Field | Type | Description |
| --- | --- | --- |
| `Success` | `bool` | Whether the apply operation succeeded |
| `Snapshot` | `ConvaiRuntimeSettingsSnapshot` | Resulting settings state after apply |
| `AppliedMask` | `ConvaiRuntimeSettingsChangeMask` | Bitmask of which settings actually changed |
| `ValidationMessage` | `string` | Reason for failure when `Success == false`. Empty on success |

**`ResetToDefaults()`** resets all settings to project defaults:

```csharp
settings.ResetToDefaults();
```

### React to settings changes

Subscribe to `Changed` to react when any setting changes. Use `ConvaiRuntimeSettingsChangeMask` to check which specific setting changed before doing work.

```csharp
using Convai.Runtime.Components;
using Convai.Shared.Abstractions;
using Convai.Shared.Types;
using UnityEngine;

public class SettingsChangeReactor : MonoBehaviour
{
    private IConvaiRuntimeSettingsService _settings;

    private void OnEnable()
    {
        if (ConvaiManager.ActiveManager.TryGetRuntimeSettingsService(out _settings))
            _settings.Changed += OnSettingsChanged;
    }

    private void OnDisable()
    {
        if (_settings != null)
            _settings.Changed -= OnSettingsChanged;
    }

    private void OnSettingsChanged(ConvaiRuntimeSettingsChanged changed)
    {
        if ((changed.Mask & ConvaiRuntimeSettingsChangeMask.PreferredMicrophoneDeviceId) != 0)
        {
            Debug.Log($"Microphone changed to: {changed.Current.PreferredMicrophoneDeviceId}");
            ApplyMicrophoneChange(changed.Current.PreferredMicrophoneDeviceId);
        }

        if ((changed.Mask & ConvaiRuntimeSettingsChangeMask.PlayerDisplayName) != 0)
        {
            UpdatePlayerNameDisplay(changed.Current.PlayerDisplayName);
        }
    }
}
```

**`ConvaiRuntimeSettingsChanged` fields:**

| Field | Type | Description |
| --- | --- | --- |
| `Previous` | `ConvaiRuntimeSettingsSnapshot` | Settings before the change |
| `Current` | `ConvaiRuntimeSettingsSnapshot` | Settings after the change |
| `Mask` | `ConvaiRuntimeSettingsChangeMask` | Bitmask indicating which fields changed |

**`ConvaiRuntimeSettingsChangeMask` values:**

| Value | Description |
| --- | --- |
| `None` | No fields changed |
| `PlayerDisplayName` | Player display name changed |
| `TranscriptEnabled` | Transcript enabled state changed |
| `NotificationsEnabled` | Notifications enabled state changed |
| `PreferredMicrophoneDeviceId` | Microphone selection changed |
| `TranscriptMode` | Transcript mode changed |
| `All` | All fields |

### Transcript mode limitation in the panel

The **Transcript Style** dropdown in the settings panel exposes **only Chat mode** at runtime. This is by design — `SettingsPanelPresenter.ExposedTranscriptModes` is hardcoded to `{ ConvaiTranscriptMode.Chat }`.

To switch to Subtitle mode, use `Apply()` directly:

```csharp
settings.Apply(new ConvaiRuntimeSettingsPatch
{
    TranscriptMode = ConvaiTranscriptMode.Subtitle
});
```

See [Chat and Subtitle Modes](chat-and-subtitle-modes.md) for full mode-switching details.

## Usage examples

### Safety training — pause menu integration

A safety training simulation exposes the settings panel through a pause menu and re-shows the menu when the panel closes:

```csharp
using Convai.Runtime.Components;
using Convai.Shared.Abstractions;
using UnityEngine;

public class PauseMenu : MonoBehaviour
{
    [SerializeField] private GameObject _pauseMenuRoot;
    private IConvaiSettingsPanelController _settingsController;

    private void Start()
    {
        ConvaiManager.ActiveManager.TryGetSettingsPanelController(out _settingsController);
    }

    private void OnEnable()
    {
        if (_settingsController != null)
            _settingsController.VisibilityChanged += OnPanelVisibilityChanged;
    }

    private void OnDisable()
    {
        if (_settingsController != null)
            _settingsController.VisibilityChanged -= OnPanelVisibilityChanged;
    }

    public void OpenSettings()
    {
        _pauseMenuRoot.SetActive(false);
        _settingsController?.Open();
    }

    private void OnPanelVisibilityChanged(bool isOpen)
    {
        if (!isOpen)
            _pauseMenuRoot.SetActive(true);
    }
}
```

At runtime, opening settings hides the pause menu. When the trainee saves and the panel closes, the pause menu reappears automatically.

### Corporate onboarding — pre-populate settings from authentication

A corporate onboarding experience pre-fills the player name from the authenticated user's profile and enables transcript before the first session:

```csharp
public void ApplyAuthenticatedProfile(string userName, bool showTranscripts)
{
    if (ConvaiManager.ActiveManager.TryGetRuntimeSettingsService(out var settings))
    {
        settings.Apply(new ConvaiRuntimeSettingsPatch
        {
            PlayerDisplayName = userName,
            TranscriptEnabled = showTranscripts
        });
    }
}
```

At runtime, the trainee's real name appears in transcript bubbles immediately, and transcript display is pre-configured to match the organization's preference.

### Analytics — track settings changes

A training platform logs when trainees change their microphone device for session quality analysis:

```csharp
private void OnSettingsChanged(ConvaiRuntimeSettingsChanged changed)
{
    if ((changed.Mask & ConvaiRuntimeSettingsChangeMask.PreferredMicrophoneDeviceId) != 0)
    {
        AnalyticsTracker.LogEvent("microphone_changed", new Dictionary<string, object>
        {
            { "previous", changed.Previous.PreferredMicrophoneDeviceId },
            { "current", changed.Current.PreferredMicrophoneDeviceId }
        });
    }
}
```

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Panel does not fade in | `CanvasGroup` or `CanvasFader` missing | `SettingsPanel.Awake()` calls `EnsureFadeComponents()` which adds them automatically — verify the prefab is intact and Awake is running |
| Microphone dropdown is empty | No microphone devices detected or permission denied | Verify device is connected; check Player Settings for microphone permissions on mobile platforms |
| Conversation mode dropdown hidden | No room connection active | Expected — the dropdown only appears while `IConvaiRoomConnectionService` is available |
| Settings not persisted after save | Settings service unavailable at save time | Ensure `ConvaiManager` is initialized before the panel opens; check `ConvaiManager.IsBootstrapped` |
| `Apply()` returns `Success == false` | Validation failure | Check `result.ValidationMessage` for the reason |
| `Changed` event not firing | Not subscribed or subscribed after settings changed | Subscribe in `OnEnable` before the session starts |

## Next steps

With the settings panel in place, your users can adjust their session preferences at runtime. For customizing the visual style of the panel itself, see Customizing UI Components. For controlling transcript display that the panel manages, see Chat and Subtitle Modes.

{% content-ref url="customizing-ui-components.md" %}
[Customizing UI Components](customizing-ui-components.md)
{% endcontent-ref %}

{% content-ref url="chat-and-subtitle-modes.md" %}
[Chat and Subtitle Modes](chat-and-subtitle-modes.md)
{% endcontent-ref %}
