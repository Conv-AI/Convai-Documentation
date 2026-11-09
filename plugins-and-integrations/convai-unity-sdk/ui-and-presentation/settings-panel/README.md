---
title: Settings panel
last_reviewed: "5.0.0-preview"
description: >-
  Add a runtime settings panel so users can adjust microphone, transcript
  visibility, and notification preferences, or access the same settings
  programmatically.
---

The settings panel is an optional scene-level UI that lets users adjust key conversation preferences at runtime. To read current settings, apply patches, or subscribe to changes from code, see [Runtime settings API](runtime-settings-api.md).

## Controllable settings

| Setting                 | Description                                                                              |
| ----------------------- | ---------------------------------------------------------------------------------------- |
| **Player Display Name** | The editable player name preference; the panel can display an effective name supplied by the player identity                                      |
| **Transcript**          | Enable or disable the transcript UI entirely                                             |
| **Notifications**       | Enable or disable in-scene notification popups                                           |
| **Microphone**          | Select the active input device from available options                                    |
| **Conversation Mode**   | Switch between Hands Free and Push to Talk (shown when a room connection service is available) |

Changes apply when the user clicks **Save**. The panel closes automatically on save. Clicking **Close** discards unsaved changes.

The **Player Display Name** field initializes from the project-wide `ConvaiSettings.DefaultPlayerDisplayName` setting, configured in the **Runtime Defaults** section of **Convai → Settings**. Saved runtime overrides take precedence over this default. The built-in panel also reads the effective `ConvaiManager.Player.PlayerName`, so an identity provider can affect the name it displays.

## Add the settings panel to your scene

{% stepper %}
{% step %}
### Add the prefab to your scene

Drag `SettingsPanel_Landscape.prefab` into your scene. Find it at `Prefabs/SettingsPanel/SettingsPanel_Landscape.prefab` in the <code class="expression">space.vars.sdk_package_id</code> package. The prefab includes its own `Canvas` — do not nest it inside an existing Canvas.

`SettingsPanel` resolves services from `ConvaiManager`. Ensure the manager is initialized and the scene has an `EventSystem` with the input module appropriate to your project. The prefab does not include an `EventSystem`.
{% endstep %}

{% step %}
### Connect a trigger to open the panel

The panel starts hidden. Wire a button, keyboard shortcut, or pause menu to open it:

```csharp
using Convai.Runtime.Components;
using UnityEngine;
using UnityEngine.UI;

[RequireComponent(typeof(Button))]
public class SettingsButton : MonoBehaviour
{
    private Button button;
    private void Awake() => button = GetComponent<Button>();
    private void OnEnable() => button.onClick.AddListener(OpenSettings);
    private void OnDisable() => button.onClick.RemoveListener(OpenSettings);

    private void OpenSettings()
    {
        var manager = ConvaiManager.ActiveManager;
        if (manager != null && manager.TryGetSettingsPanelController(out var controller))
            controller.Open();
    }
}
```
{% endstep %}

{% step %}
### Run your scene

Click the trigger. The shipped prefab shows and hides instantly because it has no `CanvasFader`. If you add a `CanvasFader`, `fadeDuration` controls its transition, with a script default of `0.5` seconds. Adjust a toggle and click **Save**; reopen the panel to confirm the saved value. The conversation-mode dropdown depends on the room service being available, not on an active connection.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
When the panel opens correctly, the microphone dropdown is populated, the player name field shows the current display name, and the transcript and notification toggles reflect their current state.
{% endhint %}

## `SettingsPanel` inspector reference

| Field                       | Description                                                                                  |
| --------------------------- | -------------------------------------------------------------------------------------------- |
| `fadeDuration`              | Seconds for transitions when a `CanvasFader` is present (default `0.5`)                                            |
| `voiceInputDropdown`        | `TMP_Dropdown` listing available microphone devices                                          |
| `conversationModeDropdown`  | `TMP_Dropdown` for Hands Free / Push to Talk                                                 |
| `playerNameInputField`      | `TMP_InputField` for the player's display name                                               |
| `transcriptToggle`          | `Toggle` enabling or disabling transcript presentation                                       |
| `notificationToggle`        | `Toggle` enabling or disabling notifications                                                 |
| `saveButton`                | `Button` applying all changes and closing the panel                                          |
| `closeButton`               | `Button` closing without saving                                                              |
| `microphoneDropContainer`   | `GameObject` wrapping the microphone dropdown — hidden when no devices found                 |
| `conversationModeContainer` | `GameObject` wrapping the conversation mode dropdown — hidden when no room service available |
| `transcriptModeContainer`   | `GameObject` field, unused — `SettingsPanel` always deactivates it on `Awake` and nothing else reads it. Safe to ignore if you see it in the Inspector. |

## `IConvaiSettingsPanelController` — visibility API

Access the panel controller through `ConvaiManager`:

```csharp
ConvaiManager.ActiveManager.TryGetSettingsPanelController(out var controller);
```

| Member                                 | Description                                                               |
| -------------------------------------- | ------------------------------------------------------------------------- |
| `bool IsOpen`                          | `true` when the panel is currently visible                                |
| `void Open()`                          | Request that the panel is visible                                        |
| `void Close()`                         | Request that the panel is hidden                                        |
| `void Toggle()`                        | Open if closed, close if open                                             |
| `event Action<bool> VisibilityChanged` | Fires when visibility changes. `bool` parameter is the new `IsOpen` value |

## Open the panel from the sample UI

Both shipped chat prefabs include `ConvaiSettingsClickArea`. Clicking that graphic calls `IConvaiSettingsPanelController.Open()`. Keep the settings panel in the scene so that request has a view to display.

`OpenSettingsKey` defaults to `F10`, but a setting does not poll input by itself. The sample's `ConvaiSampleInteractionController` handles that shortcut. A custom scene must include the sample controller or supply its own input binding.

## Test the selected microphone

The panel includes `MicrophoneTestController`. Press **Record**, speak, and press **Stop** to play the recorded audio. It also draws a waveform. The test supports a recording of up to 10 seconds.

In a WebGL player it reports `Microphone test not supported on WebGL`. A session with microphone access disabled reports `Microphone Is Off In This Session` and does not request permission. Browser microphone troubleshooting is separate from this local test.

## Defaults and saved overrides

Project runtime defaults enable transcript presentation and disable notifications. The microphone selection starts with the system default. Character audio volume is a project setting, not one of the four fields in the runtime settings snapshot or panel patch.

The service stores changed preferences as overrides in `PlayerPrefs` under `convai.runtime.settings.v1.*`. `ResetToDefaults()` clears those overrides and reads project defaults again. See [Runtime settings API](runtime-settings-api.md) for the four supported fields and change events.

## Troubleshooting

| Symptom                           | Likely cause                                        | Fix                                                                                                                                     |
| --------------------------------- | --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Panel does not fade in            | `CanvasFader` missing from the prefab               | `SettingsPanel.Awake()` calls `EnsureFadeComponents()`, which adds a missing `CanvasGroup` automatically but only looks up an existing `CanvasFader` — it does not add one. If `CanvasFader` is missing, the panel falls back to an instant, non-animated show/hide; add the component to a project-owned prefab if an animated transition is required. |
| Microphone dropdown is empty      | No microphone devices detected or permission denied | Verify device is connected; check Player Settings for microphone permissions on mobile platforms                                        |
| Conversation mode dropdown hidden | No room service available                           | Expected — the dropdown only appears while `IConvaiRoomConnectionService` is available                                                  |
| Settings not persisted after save | Settings service unavailable at save time           | Ensure `ConvaiManager` is initialized before the panel opens; check `ConvaiManager.IsBootstrapped`                                      |

## Next steps

With the settings panel in place, your users can adjust their session preferences at runtime. For customizing the visual style of the panel itself, see Customizing UI Components. The panel only shows or hides transcript presentation — for adding and configuring the chat and subtitle transcript UIs themselves, see Chat and Subtitle Modes.

{% content-ref url="../customizing-ui-components.md" %}
[Customizing UI components](../customizing-ui-components.md)
{% endcontent-ref %}

{% content-ref url="runtime-settings-api.md" %}
[Runtime settings API](runtime-settings-api.md)
{% endcontent-ref %}

{% content-ref url="../transcript-ui/chat-and-subtitle-modes.md" %}
[Chat and subtitle modes](../transcript-ui/chat-and-subtitle-modes.md)
{% endcontent-ref %}
