---
title: Runtime settings API
last_reviewed: "4.4.0"
description: >-
  Reference for IConvaiRuntimeSettingsService — read current settings, apply
  patches, react to changes, and reset to defaults from code.
---

`IConvaiRuntimeSettingsService` is the scripting layer beneath the built-in Settings Panel. Any script can read the current settings snapshot, apply patches atomically, and subscribe to change events — without the panel being present in the scene.

Access the service through `ConvaiManager`:

```csharp
ConvaiManager.ActiveManager.TryGetRuntimeSettingsService(out var settings);
```

## `IConvaiRuntimeSettingsService`

| Member                                     | Type                                         | Description                                                |
| ------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------ |
| `Current`                                   | `ConvaiRuntimeSettingsSnapshot`               | Immutable snapshot of all current settings values           |
| `Changed`                                   | `event Action<ConvaiRuntimeSettingsChanged>`  | Fired whenever any setting changes                          |
| `Apply(ConvaiRuntimeSettingsPatch patch)`   | `ConvaiRuntimeSettingsApplyResult`            | Apply one or more settings atomically. Fields left `null` in the patch remain unchanged |
| `ResetToDefaults()`                         | `ConvaiRuntimeSettingsApplyResult`            | Reset all settings to project defaults                      |

## `ConvaiRuntimeSettingsSnapshot`

An immutable struct returned by `Current` and included in apply results and change events. All fields reflect the state at the moment the snapshot was produced.

| Field                         | Type      | Description                                             |
| ------------------------------ | ---------- | ---------------------------------------------------------- |
| `PlayerDisplayName`            | `string`   | Current player display name shown in transcript bubbles |
| `TranscriptEnabled`            | `bool`     | Whether transcript UI is enabled                         |
| `NotificationsEnabled`         | `bool`     | Whether in-scene notification popups are enabled         |
| `PreferredMicrophoneDeviceId`  | `string`   | Device ID of the preferred microphone input               |

## `ConvaiRuntimeSettingsPatch`

Passed to `Apply()`. Any field left `null` remains unchanged after apply.

| Field                         | Type      | Description                                             |
| ------------------------------ | ---------- | ---------------------------------------------------------- |
| `PlayerDisplayName`            | `string`   | Set a new player display name. `null` = no change        |
| `TranscriptEnabled`            | `bool?`    | Enable or disable the transcript UI. `null` = no change  |
| `NotificationsEnabled`         | `bool?`    | Enable or disable notifications. `null` = no change       |
| `PreferredMicrophoneDeviceId`  | `string`   | Set preferred microphone device ID. `null` = no change    |

## `ConvaiRuntimeSettingsApplyResult`

Returned by `Apply()` and `ResetToDefaults()`.

| Field               | Type                              | Description                                                  |
| -------------------- | ----------------------------------- | ---------------------------------------------------------------- |
| `Success`            | `bool`                              | `true` if the apply operation succeeded                     |
| `Snapshot`           | `ConvaiRuntimeSettingsSnapshot`     | Resulting settings state after the apply                    |
| `AppliedMask`        | `ConvaiRuntimeSettingsChangeMask`   | Bitmask of which fields actually changed                    |
| `ValidationMessage`  | `string`                            | Reason for failure when `Success == false`. Empty on success |

## `ConvaiRuntimeSettingsChanged`

The payload delivered to `Changed` subscribers.

| Field      | Type                              | Description                             |
| ----------- | ----------------------------------- | ------------------------------------------ |
| `Previous`  | `ConvaiRuntimeSettingsSnapshot`     | Settings state before the change         |
| `Current`   | `ConvaiRuntimeSettingsSnapshot`     | Settings state after the change          |
| `Mask`      | `ConvaiRuntimeSettingsChangeMask`   | Bitmask indicating which fields changed  |

## `ConvaiRuntimeSettingsChangeMask`

A `[Flags]` enum used in `AppliedMask` and `ConvaiRuntimeSettingsChanged.Mask`. Compare with bitwise AND to detect specific changes.

| Value                         | Description                         |
| ------------------------------ | -------------------------------------- |
| `None`                          | No fields changed                    |
| `PlayerDisplayName`             | Player display name changed          |
| `TranscriptEnabled`             | Transcript enabled state changed     |
| `NotificationsEnabled`          | Notifications enabled state changed  |
| `PreferredMicrophoneDeviceId`   | Microphone selection changed          |
| `All`                            | All fields                            |

## Usage examples

### Read current settings

```csharp
using Convai.Runtime.Components;
using Convai.Shared.Types;
using UnityEngine;

public class SettingsReader : MonoBehaviour
{
    private void Start()
    {
        if (ConvaiManager.ActiveManager.TryGetRuntimeSettingsService(out var settings))
        {
            ConvaiRuntimeSettingsSnapshot current = settings.Current;
            Debug.Log($"Player name: {current.PlayerDisplayName}");
            Debug.Log($"Transcript on: {current.TranscriptEnabled}");
        }
    }
}
```

### Apply a settings patch

```csharp
if (ConvaiManager.ActiveManager.TryGetRuntimeSettingsService(out var settings))
{
    var result = settings.Apply(new ConvaiRuntimeSettingsPatch
    {
        PlayerDisplayName = "Dr. Kaan",
        TranscriptEnabled = true
    });

    if (!result.Success)
        Debug.LogWarning($"Settings apply failed: {result.ValidationMessage}");
}
```

### React to settings changes

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

| Symptom                                | Likely cause                                         | Fix                                                                                                                   |
| ---------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| `Apply()` returns `Success == false`   | Validation failure                                   | Check `result.ValidationMessage` for the reason                                                                       |
| `Changed` event not firing             | Not subscribed, or subscribed after settings changed | Subscribe in `OnEnable` before the session starts                                                                     |
| `ResetToDefaults()` result not checked | Return value ignored                                 | `ResetToDefaults()` returns `ConvaiRuntimeSettingsApplyResult` — check `result.Success` if the reset must be verified |

## Next steps

{% content-ref url="./" %}
[.](./)
{% endcontent-ref %}

{% content-ref url="../transcript-ui/chat-and-subtitle-modes.md" %}
[chat-and-subtitle-modes.md](../transcript-ui/chat-and-subtitle-modes.md)
{% endcontent-ref %}
