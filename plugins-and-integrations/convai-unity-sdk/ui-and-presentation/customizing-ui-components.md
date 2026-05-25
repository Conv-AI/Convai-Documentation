---
title: Customizing UI components
last_reviewed: 4.2.0
description: >-
  Restyle or replace the built-in transcript, notification, and settings UI
  using character visibility filters or prefab swapping.
---

# Customizing UI components

Two extension paths let you customize the SDK's scene-level UI without replacing its data pipeline. Character visibility filtering controls which characters' transcripts reach the active display. Visual customization swaps the prefabs that render those transcripts, notifications, and settings controls.

For lightweight transcript callbacks without a custom UI, use `ITranscriptListener`. For a complete custom transcript display replacing the built-in chat or subtitle panel, use `ITranscriptUI`. Both interfaces are documented in [Transcript UI](transcript-ui/).

### Character visibility filtering

Controls which characters' transcripts the `TranscriptUIController` routes to active UI — essential for multi-character scenes where simultaneous transcripts create confusion.

**Base class:** `TranscriptFilterBase` (SDK-provided, at `SDK/Runtime/Presentation/Services/Utilities/`)

* Automatically adds a `SphereCollider` (radius `5f`, trigger mode) if none is present on the `GameObject`
* Maintains `CharactersInsideColliderList` via `OnTriggerEnter` / `OnTriggerExit` callbacks
* Integrates with `IVisibleCharacterService` — auto-resolved from `ConvaiManager` on startup
* Place on the player `GameObject` or a child

**Two ready-to-use implementations** (located in `SamplesShared/Scripts/UI/Utilities/` — copy before modifying):

#### `SingleCharacterFilter`

Tracks the **nearest character within the player's vision cone**.

* Best for subtitle mode with multiple characters
* Player sees only the transcript of the character they face
* Default vision cone: 90° total (any character within 45° of forward)
* Override the cone angle by implementing `IVisionConeProvider` on your player agent. The interface is defined in `ProximityCharacterFilter.cs` (namespace `Convai.Sample.UI.Utilities`, SamplesShared layer):

```csharp
// Defined in ProximityCharacterFilter.cs — namespace Convai.Sample.UI.Utilities
public interface IVisionConeProvider
{
    float VisionConeAngle { get; }
}
```

#### `ProximityCharacterFilter`

Tracks **all characters within radius and vision cone**.

* Best for chat mode with group conversations
* Multiple characters' transcripts visible simultaneously
* Same vision cone behavior as `SingleCharacterFilter`

**Scene setup checklist:**

* [ ] Add `SingleCharacterFilter` or `ProximityCharacterFilter` to the player `GameObject`
* [ ] Ensure a `Rigidbody` exists on the player or the characters (required for trigger callbacks)
* [ ] `ConvaiManager` auto-resolves `IVisibleCharacterService` on filter startup
* [ ] Test in Play Mode by walking toward and away from characters

{% hint style="warning" %}
`SingleCharacterFilter` and `ProximityCharacterFilter` are reference implementations in `SamplesShared`. Copy them into your own assembly before modifying — changes to `SamplesShared` scripts are overwritten on SDK updates.
{% endhint %}

### Visual customization

#### Chat message bubbles

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

#### Notification prefabs

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

#### Settings panel view

Implement `ISettingsPanelView` and wire to `SettingsPanelPresenter` for a fully custom settings UI. The presenter handles all business logic — your view only handles rendering and input events.

```csharp
// Bind your custom view to the existing presenter
settingsPanelPresenter.Bind(myCustomView);

// Unbind when your view is destroyed
settingsPanelPresenter.Unbind();
```

### Usage examples

#### Multi-character subtitle focus

A medical simulation with multiple AI characters (doctor, nurse, patient) uses `SingleCharacterFilter` on the trainee so subtitle display automatically switches to the AI character they face. Add the component to the player `GameObject`, verify a `Rigidbody` is present, and leave the default 90° vision cone. At runtime, as the trainee turns between characters, the active subtitle switches to the character in front of them without manual intervention.

#### Custom notification skin

A military training simulation replaces the default notification prefab with a HUD-style alert that matches the simulation's UI language. Duplicate the default notification prefab, restyle it as a top-right status indicator, and assign it to `UINotificationController.uiNotificationPrefab`. At runtime, all system and session error alerts appear in the project's visual style without changing any notification logic.

### Troubleshooting

| Symptom                                                  | Likely cause                                                                 | Fix                                                                                            |
| -------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `TranscriptFilterBase` not tracking characters           | No `Rigidbody` on player or characters                                       | Add a `Rigidbody` to at least one side of each character–player pair                           |
| `SingleCharacterFilter` tracks wrong character           | Player `GameObject` not found via `GetComponentInParent<ConvaiPlayer>()`     | Place the filter on the player `GameObject` or inject the `IPlayerInputService` via `Inject()` |
| Custom `ISettingsPanelView` not receiving save callbacks | View not bound to the presenter                                              | Call `settingsPanelPresenter.Bind(myCustomView)` after the presenter is available              |
| Replacement bubble prefab shows no text                  | `senderUI` or `messageUI` not assigned on `ChatMessageBubble`                | Wire both `TextMeshProUGUI` references in the prefab Inspector                                 |
| Custom notification prefab not appearing                 | `uiNotificationPrefab` on `UINotificationController` still points to default | Assign your restyled prefab to the `uiNotificationPrefab` field                                |

### Next steps

{% content-ref url="transcript-ui/" %}
[transcript-ui](transcript-ui/)
{% endcontent-ref %}

{% content-ref url="transcript-ui/chat-and-subtitle-modes.md" %}
[chat-and-subtitle-modes.md](transcript-ui/chat-and-subtitle-modes.md)
{% endcontent-ref %}
