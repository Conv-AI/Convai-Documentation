---
title: Settings panel
last_reviewed: 4.2.0
description: >-
  Add a runtime settings panel so users can adjust microphone, transcript mode,
  and notification preferences, or access the same settings programmatically.
---

# Settings panel

The settings panel is an optional scene-level UI that lets users adjust key conversation preferences at runtime. To read current settings, apply patches, or subscribe to changes from code, see [Runtime settings API](runtime-settings-api.md).

### Controllable settings

| Setting                 | Description                                                                              |
| ----------------------- | ---------------------------------------------------------------------------------------- |
| **Player Display Name** | The name shown in transcript bubbles for the player                                      |
| **Transcript**          | Enable or disable the transcript UI entirely                                             |
| **Notifications**       | Enable or disable in-scene notification popups                                           |
| **Microphone**          | Select the active input device from available options                                    |
| **Conversation Mode**   | Switch between Hands Free and Push to Talk (shown only when a room connection is active) |

Changes apply when the user clicks **Save**. The panel closes automatically on save. Clicking **Close** discards unsaved changes.

### Add the settings panel to your scene

{% stepper %}
{% step %}
#### Add the prefab to your Canvas

Drag `SettingsPanel_Landscape.prefab` into your scene. Find it at `Prefabs/SettingsPanel/SettingsPanel_Landscape.prefab` in the <code class="expression">space.vars.sdk_package_id</code> package. The prefab includes its own `Canvas` — do not nest it inside an existing Canvas.

`SettingsPanel` auto-resolves all required services from `ConvaiManager` on `OnEnable`. No additional Inspector wiring is required for the basic setup.

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Unity scene hierarchy with the `SettingsPanel_Landscape` GameObject visible at the scene root (not nested inside another Canvas).
{% endhint %}
{% endstep %}

{% step %}
#### Connect a trigger to open the panel

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
#### Run your scene

Click the trigger. The panel fades in (default 0.5s). Adjust settings and click **Save** — the panel fades out and changes apply immediately. The microphone dropdown populates from available system devices; the conversation mode dropdown appears only while a room connection is active.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
When the panel opens correctly, the microphone dropdown is populated, the player name field shows the current display name, and the transcript and notification toggles reflect their current state.
{% endhint %}

### `SettingsPanel` inspector reference

| Field                       | Description                                                                                  |
| --------------------------- | -------------------------------------------------------------------------------------------- |
| `fadeDuration`              | Seconds for fade in/out animation (default `0.5`)                                            |
| `transcriptStyleDropdown`   | `TMP_Dropdown` for the transcript display mode                                               |
| `voiceInputDropdown`        | `TMP_Dropdown` listing available microphone devices                                          |
| `conversationModeDropdown`  | `TMP_Dropdown` for Hands Free / Push to Talk                                                 |
| `playerNameInputField`      | `TMP_InputField` for the player's display name                                               |
| `transcriptToggle`          | `Toggle` enabling or disabling the transcript UI                                             |
| `notificationToggle`        | `Toggle` enabling or disabling notifications                                                 |
| `saveButton`                | `Button` applying all changes and closing the panel                                          |
| `closeButton`               | `Button` closing without saving                                                              |
| `microphoneDropContainer`   | `GameObject` wrapping the microphone dropdown — hidden when no devices found                 |
| `transcriptModeContainer`   | `GameObject` wrapping the transcript style dropdown                                          |
| `conversationModeContainer` | `GameObject` wrapping the conversation mode dropdown — hidden when no room service available |

### `IConvaiSettingsPanelController` — visibility API

Access the panel controller through `ConvaiManager`:

```csharp
ConvaiManager.ActiveManager.TryGetSettingsPanelController(out var controller);
```

| Member                                 | Description                                                               |
| -------------------------------------- | ------------------------------------------------------------------------- |
| `bool IsOpen`                          | `true` when the panel is currently visible                                |
| `void Open()`                          | Show the panel with fade animation                                        |
| `void Close()`                         | Hide the panel with fade animation                                        |
| `void Toggle()`                        | Open if closed, close if open                                             |
| `event Action<bool> VisibilityChanged` | Fires when visibility changes. `bool` parameter is the new `IsOpen` value |

### Usage examples

#### Safety training — pause menu integration

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

#### Corporate onboarding — pre-populate settings from authentication

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

### Troubleshooting

| Symptom                           | Likely cause                                        | Fix                                                                                                                                     |
| --------------------------------- | --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Panel does not fade in            | `CanvasGroup` or `CanvasFader` missing              | `SettingsPanel.Awake()` calls `EnsureFadeComponents()` which adds them automatically — verify the prefab is intact and Awake is running |
| Microphone dropdown is empty      | No microphone devices detected or permission denied | Verify device is connected; check Player Settings for microphone permissions on mobile platforms                                        |
| Conversation mode dropdown hidden | No room connection active                           | Expected — the dropdown only appears while `IConvaiRoomConnectionService` is available                                                  |
| Settings not persisted after save | Settings service unavailable at save time           | Ensure `ConvaiManager` is initialized before the panel opens; check `ConvaiManager.IsBootstrapped`                                      |

### Next steps

With the settings panel in place, your users can adjust their session preferences at runtime. For customizing the visual style of the panel itself, see Customizing UI Components. For controlling transcript display that the panel manages, see Chat and Subtitle Modes.

{% content-ref url="../customizing-ui-components.md" %}
[customizing-ui-components.md](../customizing-ui-components.md)
{% endcontent-ref %}

{% content-ref url="runtime-settings-api.md" %}
[runtime-settings-api.md](runtime-settings-api.md)
{% endcontent-ref %}

{% content-ref url="../transcript-ui/chat-and-subtitle-modes.md" %}
[chat-and-subtitle-modes.md](../transcript-ui/chat-and-subtitle-modes.md)
{% endcontent-ref %}
