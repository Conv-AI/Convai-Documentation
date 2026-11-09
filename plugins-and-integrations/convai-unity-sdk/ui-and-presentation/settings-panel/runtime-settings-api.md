---
title: Runtime settings API
last_reviewed: "5.0.0-preview"
description: Read runtime preferences, apply partial changes, observe changed fields, and reset saved overrides to the defaults set by your project.
---

`IConvaiRuntimeSettingsService` is the scripting layer beneath the built-in Settings Panel. A script with access to the initialized manager can read the current settings snapshot, apply patches atomically, and subscribe to change events — without the panel being present in the scene.

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
| `ResetToDefaults()`                         | `ConvaiRuntimeSettingsApplyResult`            | Clear saved overrides and read normalized project defaults                      |

## `ConvaiRuntimeSettingsSnapshot`

An immutable struct returned by `Current` and included in apply results and change events. All fields reflect the state at the moment the snapshot was produced.

| Field                         | Type      | Description                                             |
| ------------------------------ | ---------- | ---------------------------------------------------------- |
| `PlayerDisplayName`            | `string`   | Saved player name preference; effective identity can supply a different display name |
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

## Normalization and persistence

`Apply(null)` fails with `ValidationMessage` equal to `Patch cannot be null.`. An empty patch or a patch that normalizes to the existing values succeeds with `AppliedMask = None` and does not raise `Changed`.

Player names are trimmed; a blank name falls back to the project default. Microphone selection is normalized against the available device list. Always read the returned `Snapshot` instead of assuming that every requested value was stored verbatim.

The default store saves differences from project defaults in `PlayerPrefs` keys under `convai.runtime.settings.v1.*`. `ResetToDefaults()` deletes those overrides and reconstructs the normalized defaults. The four fields above are the complete snapshot; conversation input mode belongs to the room connection service, and character audio volume remains a separate project setting.

## Read, apply, and observe settings

This component waits for a usable manager, subscribes once, and detaches when disabled. Call `EnableTranscript()` from your application UI after initialization:

```csharp
using Convai.Runtime.Components;
using Convai.Shared.Abstractions;
using Convai.Shared.Types;
using UnityEngine;

public class RuntimePreferences : MonoBehaviour
{
    private IConvaiRuntimeSettingsService settings;

    private void Update()
    {
        if (settings != null) return;
        var manager = ConvaiManager.ActiveManager;
        if (manager == null || !manager.TryGetRuntimeSettingsService(out settings)) return;
        settings.Changed += OnChanged;
        Debug.Log($"Transcript enabled: {settings.Current.TranscriptEnabled}");
    }

    public void EnableTranscript()
    {
        if (settings == null) return;
        var result = settings.Apply(new ConvaiRuntimeSettingsPatch { TranscriptEnabled = true });
        if (!result.Success) Debug.LogWarning(result.ValidationMessage);
    }

    private void OnChanged(ConvaiRuntimeSettingsChanged change)
    {
        if ((change.Mask & ConvaiRuntimeSettingsChangeMask.TranscriptEnabled) != 0)
            Debug.Log($"Transcript enabled: {change.Current.TranscriptEnabled}");
    }

    private void OnDisable()
    {
        if (settings != null) settings.Changed -= OnChanged;
        settings = null;
    }
}
```

This example assumes a single manager for the lifetime of the enabled component. If your application replaces managers without disabling the UI, rebind to the replacement service. For analytics, observe `Previous`, `Current`, and `Mask` in the same change callback and send only the fields your application needs.

## Troubleshooting

| Symptom                                | Likely cause                                         | Fix                                                                                                                   |
| ---------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| `Apply()` returns `Success == false`   | A null patch                                   | Pass a non-null patch; verify the resulting `Snapshot`                                                                       |
| `Changed` event not firing             | Not subscribed, or subscribed after settings changed | Bind after service initialization and confirm the requested value differs from `Current`                                                                     |
| `ResetToDefaults()` result not checked | Return value ignored                                 | `ResetToDefaults()` returns `ConvaiRuntimeSettingsApplyResult` — check `result.Success` if the reset must be verified |

## Next steps

{% content-ref url="./" %}
[.](./)
{% endcontent-ref %}

{% content-ref url="../transcript-ui/chat-and-subtitle-modes.md" %}
[Chat and subtitle modes](../transcript-ui/chat-and-subtitle-modes.md)
{% endcontent-ref %}
