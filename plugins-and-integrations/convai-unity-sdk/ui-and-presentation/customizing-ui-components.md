---
title: Customizing UI components
last_reviewed: "4.6.0"
description: >-
  Restyle or replace the built-in transcript, notification, and settings UI
  using the room transcript facade, speaker filters, or prefab swapping.
---

Two extension paths let you customize the SDK's scene-level UI without replacing its data pipeline. Transcript subscriptions control which room turns reach your display. Visual customization swaps the prefabs that render those turns, notifications, and settings controls.

For a custom transcript display, obtain `ConvaiTranscripts` with `ConvaiManager.TryGetTranscripts(...)`. The facade exposes the canonical room timeline, committed-turn and live-update subscriptions, captions, and export. The `ITranscriptListener`, `ITranscriptUI`, `TranscriptUIController`, and `TranscriptFilterBase` names referenced by earlier documentation were removed in SDK 4.4 and are not part of the current <code class="expression">space.vars.unity_sdk_version</code> presentation API.

## Filter room transcripts

Incoming transcript turns are room-wide. They can include the player and any character in the roster, whether or not that character is the current interaction target. Filter a custom display with `TranscriptSubscriptionOptions`:

| Option | Use |
| --- | --- |
| `SpeakerType` | Include only character or player turns. |
| `SpeakerId` | Match `TranscriptTurn.Speaker.Id`; use a known local Character ID for one character. |
| `ParticipantId` | Match the room participant ID when transport identity is the stable key you have. |
| `ReplayExisting` | Replay matching turns already present in the room timeline. |
| `IncludeActive` | Include turns that are still streaming. |
| `IncludeTerminal` | Include committed, interrupted, or corrected turns. |

Use `SubscribeCommitted(...)` for logs or chat history that should not redraw partial text. Use `Subscribe(...)` when subtitles need streaming updates. Dispose the returned subscription before changing filters or destroying the view.

**Unity SDK <code class="expression">space.vars.unity_sdk_preview_version</code> preview:** The transcript APIs in this example are available in <code class="expression">space.vars.unity_sdk_version</code>, but `SetInteractionTargetAsync(...)` and shared-room target routing are staged preview APIs that are not in the current Asset Store release.

```csharp
using System;
using Convai.Domain.Models;
using Convai.Runtime.Components;
using Convai.Runtime.Facades;
using Convai.Runtime.Room;
using TMPro;
using UnityEngine;

public sealed class FocusedCharacterSubtitle : MonoBehaviour
{
    [SerializeField] private ConvaiManager _manager;
    [SerializeField] private TMP_Text _label;

    private ConvaiTranscripts _transcripts;
    private IConvaiRoomConnectionService _room;
    private IDisposable _subscription;

    private void OnEnable() => TryBindServices();

    private bool TryBindServices()
    {
        if (_manager == null)
            _manager = ConvaiManager.ActiveManager;

        if (_manager == null || !_manager.IsInitialized)
            return false;

        return _manager.TryGetTranscripts(out _transcripts)
               && _manager.TryGetRoomConnectionService(out _room);
    }

    public async void Focus(ConvaiCharacter character)
    {
        if (character == null || !TryBindServices())
            return;

        try
        {
            // Completes after Convai acknowledges the new interaction target.
            await _room.SetInteractionTargetAsync(character);

            _subscription?.Dispose();
            _subscription = _transcripts.Subscribe(
                change => _label.text = change.Turn?.DisplayText ?? string.Empty,
                new TranscriptSubscriptionOptions
                {
                    ReplayExisting = false,
                    SpeakerType = TranscriptSpeakerType.Character,
                    SpeakerId = character.CharacterId
                });
        }
        catch (Exception exception)
        {
            Debug.LogError($"Could not change the interaction target: {exception.Message}");
        }
    }

    private void OnDisable()
    {
        _subscription?.Dispose();
        _subscription = null;
    }
}
```

`Focus(...)` can be called by a raycast, a proximity trigger, a UI button, or any application-specific selector. Target routing and transcript filtering are separate responsibilities: `SetInteractionTargetAsync(...)` controls where subsequent player input goes, while `TranscriptSubscriptionOptions` controls what this local view renders.

{% hint style="warning" %}
Do not update target-dependent UI only because a raycast or button selected a character. Await `SetInteractionTargetAsync(...)` first. A failed, cancelled, stale, or timed-out route command must leave the UI aligned with the last server-acknowledged target. After a timeout, stop routing new input until you reread `CurrentMultiCharacterSession` or reconnect because the outcome is unknown.
{% endhint %}

## Visual customization

### Chat message bubbles

`ChatTranscriptUI` instantiates character and player message prefabs from its Inspector fields. To restyle:

1. Duplicate the default bubble from `Prefabs/TranscriptUI/` in the <code class="expression">space.vars.sdk_package_id</code> package
2. Restyle the duplicate (colors, fonts, backgrounds, layout)
3. Assign to `characterMessagePrefab` or `playerMessagePrefab` on `ChatTranscriptUI`

Your replacement prefab must contain a `ChatMessageBubble` component with these fields wired:

| Field       | Type              | Description                  |
| ----------- | ----------------- | ---------------------------- |
| `senderUI`  | `TextMeshProUGUI` | Displays the speaker's name  |
| `messageUI` | `TextMeshProUGUI` | Displays the transcript text |

Available styling methods on `ChatMessageBubble`:

| Method                          | Description                                                |
| ------------------------------- | ---------------------------------------------------------- |
| `SetSender(string sender)`      | Set the sender display name                                |
| `SetSenderColor(Color color)`   | Override the automatically-assigned sender name color      |
| `SetMessage(string message)`    | Set the full message text                                  |
| `AppendMessage(string message)` | Append text to the current message (used during streaming) |

### Notification prefabs

`UINotificationController` instantiates `UINotification` prefabs from its `uiNotificationPrefab` field. To restyle:

1. Duplicate `Notification.prefab` from `Prefabs/Notifications/` in the <code class="expression">space.vars.sdk_package_id</code> package
2. Restyle the duplicate
3. Assign to `uiNotificationPrefab` on `UINotificationController`

Required `UINotification` references:

| Field                       | Type              | Description                |
| --------------------------- | ----------------- | -------------------------- |
| `notificationRectTransform` | `RectTransform`   | Used for slide positioning |
| `notificationIcon`          | `Image`           | Sprite display             |
| `notificationTitleText`     | `TextMeshProUGUI` | Title                      |
| `notificationMessageText`   | `TextMeshProUGUI` | Body                       |

### Settings panel view

Implement `ISettingsPanelView` and wire to `SettingsPanelPresenter` for a fully custom settings UI. The presenter handles all business logic — your view only handles rendering and input events.

```csharp
// Bind your custom view to the existing presenter
settingsPanelPresenter.Bind(myCustomView);

// Unbind when your view is destroyed
settingsPanelPresenter.Unbind();
```

## Usage examples

### Multi-character subtitle focus

A medical simulation with doctor, nurse, and patient characters casts from the trainee's camera. When the hit character changes, it awaits `SetInteractionTargetAsync(character)` and then replaces the subtitle subscription with a `SpeakerId` filter for that Character ID. The selector is application code; the SDK does not automatically infer focus from the camera or collider state.

### Custom notification skin

A military training simulation replaces the default notification prefab with a HUD-style alert that matches the simulation's UI language. Duplicate the default notification prefab, restyle it as a top-right status indicator, and assign it to `UINotificationController.uiNotificationPrefab`. At runtime, all system and session error alerts appear in the project's visual style without changing any notification logic.

## Troubleshooting

| Symptom                                                  | Likely cause                                                                 | Fix                                                                                            |
| -------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Focused subtitle shows other characters                  | Subscription has no `SpeakerId` or `ParticipantId` filter                    | Dispose the old subscription and create a filtered `TranscriptSubscriptionOptions` subscription |
| Target highlight changes but player input reaches the previous character | UI changed before the route command was acknowledged | Await `SetInteractionTargetAsync(...)`; update the highlight only after it completes |
| Custom `ISettingsPanelView` not receiving save callbacks | View not bound to the presenter                                              | Call `settingsPanelPresenter.Bind(myCustomView)` after the presenter is available              |
| Replacement bubble prefab shows no text                  | `senderUI` or `messageUI` not assigned on `ChatMessageBubble`                | Wire both `TextMeshProUGUI` references in the prefab Inspector                                 |
| Custom notification prefab not appearing                 | `uiNotificationPrefab` on `UINotificationController` still points to default | Assign your restyled prefab to the `uiNotificationPrefab` field                                |

## Next steps

{% content-ref url="transcript-ui/" %}
[transcript-ui](transcript-ui/)
{% endcontent-ref %}

{% content-ref url="transcript-ui/chat-and-subtitle-modes.md" %}
[chat-and-subtitle-modes.md](transcript-ui/chat-and-subtitle-modes.md)
{% endcontent-ref %}
