---
title: Customizing UI components
description: >-
  Extend or replace the built-in transcript, notification, and settings UI
  using ITranscriptListener, ITranscriptUI, character visibility filters, or
  prefab swapping.
last_reviewed: "4.2.0"
---

The Convai Unity SDK's UI layer is designed for replacement. Four extension paths let you customize to any depth — from lightweight transcript callbacks to fully bespoke UI implementations.

1. **`ITranscriptListener`** — Lightweight callbacks for transcript delivery without building new visual UI
2. **`ITranscriptUI`** — Full custom transcript display replacing the built-in chat or subtitle panel
3. **Character Visibility Filtering** — Control which characters' transcripts route to the active UI
4. **Visual Customization** — Restyle existing components by swapping prefabs

## `ITranscriptListener` — simple custom integration

Use `ITranscriptListener` when you need transcript data routed to your code without building new visual UI. Examples: a compliance scoring system, a conversation logger, a custom text component fed by transcript data.

**Interface members:**

| Member | Description |
| --- | --- |
| `string FilterCharacterId { get; }` | Optional character filter — set to a character ID to receive only that character's transcripts. Return `null` for no filtering |
| `void OnCharacterTranscript(string characterId, string characterName, string text, bool isFinal)` | Called for each character transcript update |
| `void OnPlayerTranscript(string text, bool isFinal)` | Called for each player transcript update |

The `isFinal` boolean is `false` during streaming and `true` on turn completion. Auto-discovery registers all `ITranscriptListener` implementations in the scene automatically.

**Multi-user variant:** Implement `IMultiUserTranscriptListener` to receive per-player attribution via `OnPlayerTranscriptWithSpeaker()`, which includes `speakerId`, `speakerName`, `participantId`, and session context.

**Example — compliance scoring in safety training:**

```csharp
using Convai.Runtime.Presentation.Services;
using UnityEngine;

public class ComplianceScorer : MonoBehaviour, ITranscriptListener
{
    [SerializeField] private string _instructorCharacterId;

    public string FilterCharacterId => _instructorCharacterId;

    public void OnCharacterTranscript(string characterId, string characterName, string text, bool isFinal) { }

    public void OnPlayerTranscript(string text, bool isFinal)
    {
        if (!isFinal) return;
        bool passed = text.Contains("hazard identified", System.StringComparison.OrdinalIgnoreCase);
        Debug.Log($"Response evaluated. Passed: {passed}");
    }
}
```

Place on any `GameObject` in the scene. `ConvaiManager` discovers and registers it automatically.

## `ITranscriptUI` — full custom transcript UI

Use `ITranscriptUI` to replace the entire transcript display — for world-space 3D panels, custom WebGL overlays, or specialized layouts the built-in prefabs cannot provide.

**Key differences from `ITranscriptListener`:**

* Full control over prefab and component layout
* Partial transcripts managed via `DisplayMessage()` / `CompleteMessage()`
* Activates only when its `Identifier` matches the current `ConvaiTranscriptMode`
* More complex (5 methods + 2 properties)

**Interface contract:**

```csharp
public interface ITranscriptUI
{
    string Identifier { get; }  // "Chat" or "Subtitle"
    bool IsActive { get; }
    void DisplayMessage(TranscriptViewModel viewModel);
    void CompleteMessage(string messageId);
    void CompletePlayerTurn();
    void ClearAll();
    void SetActive(bool active);
}
```

**Implementation steps:**

{% stepper %}
{% step %}
### Create a MonoBehaviour implementing `ITranscriptUI`

Set `Identifier` to `"Chat"` to replace the chat UI or `"Subtitle"` to replace the subtitle UI. Implement `DisplayMessage` to handle both partial (`viewModel.IsFinal == false`) and final (`viewModel.IsFinal == true`) transcripts.
{% endstep %}

{% step %}
### Add it to your scene

`ConvaiManager` discovers it automatically on startup. For manual control, use `ConvaiManager.ActiveManager.RegisterTranscriptUI(myUI)`.
{% endstep %}

{% step %}
### Activate via transcript mode

Switch to your custom UI by setting the matching `ConvaiTranscriptMode` through `IConvaiRuntimeSettingsService.Apply()`.
{% endstep %}

{% step %}
### Remove conflicting built-in prefabs

If both your custom UI and the built-in UI share the same `Identifier`, both activate simultaneously. Remove the built-in prefab from your scene for exclusive control.
{% endstep %}
{% endstepper %}

{% hint style="danger" %}
If both your custom UI and a built-in UI share the same `Identifier`, both activate simultaneously when that mode is set. Remove the built-in prefab (`TranscriptUI_Chat.prefab` or `SubtitleTranscriptUI`) from your scene if you want exclusive control.
{% endhint %}

## Character visibility filtering

Controls which characters' transcripts the `TranscriptUIController` routes to active UI — essential for multi-character scenes where simultaneous transcripts create confusion.

**Base class:** `TranscriptFilterBase` (SDK-provided, at `SDK/Runtime/Presentation/Services/Utilities/`)

* Automatically adds a `SphereCollider` (radius `5f`, trigger mode) if none is present on the `GameObject`
* Maintains `CharactersInsideColliderList` via `OnTriggerEnter` / `OnTriggerExit` callbacks
* Integrates with `IVisibleCharacterService` — auto-resolved from `ConvaiManager` on startup
* Place on the player `GameObject` or a child

**Two ready-to-use implementations** (located in `SamplesShared/Scripts/UI/Utilities/` — copy before modifying):

### `SingleCharacterFilter`

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

### `ProximityCharacterFilter`

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

## Visual customization

### Chat message bubbles

`ChatTranscriptUI` instantiates character and player message prefabs from its Inspector fields. To restyle:

1. Duplicate the default bubble from `Prefabs/TranscriptUI/` in the <code class="expression">space.vars.sdk_package_id</code> package
2. Restyle the duplicate (colors, fonts, backgrounds, layout)
3. Assign to `characterMessagePrefab` or `playerMessagePrefab` on `ChatTranscriptUI`

Your replacement prefab must contain a `ChatMessageBubble` component with these fields wired:

| Field | Type | Description |
| --- | --- | --- |
| `senderUI` | `TextMeshProUGUI` | Displays the speaker's name |
| `messageUI` | `TextMeshProUGUI` | Displays the transcript text |

Available styling methods on `ChatMessageBubble`:

| Method | Description |
| --- | --- |
| `SetSender(string sender)` | Set the sender display name |
| `SetSenderColor(Color color)` | Override the automatically-assigned sender name color |
| `SetMessage(string message)` | Set the full message text |
| `AppendMessage(string message)` | Append text to the current message (used during streaming) |

### Notification prefabs

`UINotificationController` instantiates `UINotification` prefabs from its `uiNotificationPrefab` field. To restyle:

1. Duplicate `Notification.prefab` from `Prefabs/Notifications/` in the <code class="expression">space.vars.sdk_package_id</code> package
2. Restyle the duplicate
3. Assign to `uiNotificationPrefab` on `UINotificationController`

Required `UINotification` references:

| Field | Type | Description |
| --- | --- | --- |
| `notificationRectTransform` | `RectTransform` | Used for slide positioning |
| `notificationIcon` | `Image` | Sprite display |
| `notificationTitleText` | `TextMeshProUGUI` | Title |
| `notificationMessageText` | `TextMeshProUGUI` | Body |

### Settings panel view

Implement `ISettingsPanelView` and wire to `SettingsPanelPresenter` for a fully custom settings UI. The presenter handles all business logic — your view only handles rendering and input events.

```csharp
// Bind your custom view to the existing presenter
settingsPanelPresenter.Bind(myCustomView);

// Unbind when your view is destroyed
settingsPanelPresenter.Unbind();
```

## Usage examples

### Clinical notes — custom `ITranscriptUI`

A medical simulation renders character speech as timestamped clinical notes in a scrollable side panel rather than chat bubbles. Implement `ITranscriptUI` with `Identifier = "Chat"`, remove the built-in `TranscriptUI_Chat.prefab` from the scene, and in `DisplayMessage()` instantiate a note entry prefab with the turn's `DisplayName`, `Text`, and `Timestamp`. At runtime, each AI patient response appears as a dated note entry, matching the clinical context of the simulation.

### Multi-character subtitle focus

A medical simulation with multiple AI characters (doctor, nurse, patient) uses `SingleCharacterFilter` on the trainee so subtitle display automatically switches to the AI character they face. Add the component to the player `GameObject`, verify a `Rigidbody` is present, and leave the default 90° vision cone. At runtime, as the trainee turns between characters, the active subtitle switches to the character in front of them without manual intervention.

### Custom notification skin

A military training simulation replaces the default notification prefab with a HUD-style alert that matches the simulation's UI language. Duplicate the default notification prefab, restyle it as a top-right status indicator, and assign it to `UINotificationController.uiNotificationPrefab`. At runtime, all system and session error alerts appear in the project's visual style without changing any notification logic.

### Multi-user drill attribution

A fire safety drill with four trainees uses `IMultiUserTranscriptListener` to log each participant's speech with a stable `speakerId` for the post-drill compliance report. Implement the interface, register it as a `MonoBehaviour` in the scene, and in `OnPlayerTranscriptWithSpeaker()` append each final turn to a keyed log. At runtime, every trainee response is attributed by name and session participant ID, producing an auditable per-trainee transcript.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Custom `ITranscriptUI` activates alongside built-in UI | Both have the same `Identifier` | Remove the built-in prefab (`TranscriptUI_Chat.prefab` or `SubtitleTranscriptUI`) from the scene |
| `TranscriptFilterBase` not tracking characters | No `Rigidbody` on player or characters | Add a `Rigidbody` to at least one side of each character–player pair |
| `SingleCharacterFilter` tracks wrong character | Player `GameObject` not found via `GetComponentInParent<ConvaiPlayer>()` | Place the filter on the player `GameObject` or inject the `IPlayerInputService` via `Inject()` |
| Custom `ISettingsPanelView` not receiving save callbacks | View not bound to the presenter | Call `settingsPanelPresenter.Bind(myCustomView)` after the presenter is available |
| Replacement bubble prefab shows no text | `senderUI` or `messageUI` not assigned on `ChatMessageBubble` | Wire both `TextMeshProUGUI` references in the prefab Inspector |
| Custom notification prefab not appearing | `uiNotificationPrefab` on `UINotificationController` still points to default | Assign your restyled prefab to the `uiNotificationPrefab` field |

## Next steps

You have covered all four extension paths for customizing the SDK's UI layer. For the underlying scripting APIs driving these components, see the Scripting Reference. For display mode configuration, see Chat and Subtitle Modes.

{% content-ref url="chat-and-subtitle-modes.md" %}
[Chat and Subtitle Modes](chat-and-subtitle-modes.md)
{% endcontent-ref %}

{% content-ref url="transcript-ui.md" %}
[Transcript UI](transcript-ui.md)
{% endcontent-ref %}
