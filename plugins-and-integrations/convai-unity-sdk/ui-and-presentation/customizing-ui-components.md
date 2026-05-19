# customizing ui components

The Convai Unity SDK's UI layer is designed for replacement. Every visual component has a corresponding interface or prefab reference that you can swap without touching SDK internals. This page covers four extension paths: lightweight transcript callbacks, full custom transcript UI, character visibility filtering, and visual customization of existing components.

***

## `ITranscriptListener` — Simple Custom Integration

Use `ITranscriptListener` when you need transcripts delivered to your code but do not need to build a new visual UI. The interface gives you two callbacks — one for character speech, one for player speech — with an optional filter for a specific character.

### Interface Contract

```csharp
public interface ITranscriptListener
{
    // Optional character filter. Set to a character ID to receive only that character's transcripts.
    // Player transcripts are always received regardless of this value.
    // Return null for no filtering.
    string FilterCharacterId { get; }

    void OnCharacterTranscript(string characterId, string characterName, string text, bool isFinal);
    void OnPlayerTranscript(string text, bool isFinal);
}
```

`isFinal` is `false` on partial transcripts (streaming), `true` on the completed turn. Partial transcripts fire frequently — react only to final ones unless you need real-time text feedback.

### Auto-Discovery

Add `ITranscriptListener` to any `MonoBehaviour` in the scene. `ConvaiManager` discovers and registers all implementations automatically. No manual registration call is needed.

### Multi-User Attribution

For multi-user rooms where you need to know which specific player spoke, implement `IMultiUserTranscriptListener` instead:

```csharp
public interface IMultiUserTranscriptListener : ITranscriptListener
{
    void OnPlayerTranscriptWithSpeaker(
        string speakerId,
        string speakerName,
        string participantId,
        string text,
        bool isFinal);
}
```

`OnPlayerTranscript` is still called for all player speech. `OnPlayerTranscriptWithSpeaker` fires in addition, carrying the stable `speakerId` and the LiveKit `participantId` for per-player attribution within the session.

### Example — Trainee Response Scoring

```csharp
using Convai.Runtime.Presentation.Services;
using UnityEngine;

public class ComplianceScorer : MonoBehaviour, ITranscriptListener
{
    [SerializeField] private string _instructorCharacterId;
    [SerializeField] private ScoreDisplay _scoreDisplay;

    private int _score;

    public string FilterCharacterId => _instructorCharacterId;

    public void OnCharacterTranscript(string characterId, string characterName, string text, bool isFinal)
    {
        // Instructor speech — not scored
    }

    public void OnPlayerTranscript(string text, bool isFinal)
    {
        if (!isFinal) return;

        bool passed = EvaluateResponse(text);
        if (passed) _score++;
        _scoreDisplay.UpdateScore(_score);
    }

    private bool EvaluateResponse(string text)
    {
        return text.Contains("hazard identified", System.StringComparison.OrdinalIgnoreCase);
    }
}
```

***

## `ITranscriptUI` — Full Custom Transcript UI

Use `ITranscriptUI` when you need to build a replacement for the entire transcript display — a world-space 3D panel, a custom HTML overlay for WebGL, or a specialized layout that the built-in prefabs cannot accommodate.

### When to Use vs `ITranscriptListener`

|                         | `ITranscriptListener`     | `ITranscriptUI`                                                            |
| ----------------------- | ------------------------- | -------------------------------------------------------------------------- |
| **Visual output**       | Your code handles display | Full control over prefab and component layout                              |
| **Partial transcripts** | Delivered as callbacks    | Managed via `DisplayMessage` / `CompleteMessage`                           |
| **Mode activation**     | Always active             | Activates when its `Identifier` matches the current `ConvaiTranscriptMode` |
| **Complexity**          | 2–3 methods               | 6 methods + 2 properties                                                   |

### Interface Contract

```csharp
public interface ITranscriptUI
{
    // Must be "Chat" or "Subtitle" to match ConvaiTranscriptMode
    string Identifier { get; }

    bool IsActive { get; }

    // Called for both partial and final transcripts.
    // viewModel.IsFinal == false during streaming; true when the turn completes.
    void DisplayMessage(TranscriptViewModel viewModel);

    // Called when a specific message bubble should finalize.
    void CompleteMessage(string messageId);

    // Called when all active player messages should finalize.
    void CompletePlayerTurn();

    // Called to clear all displayed content.
    void ClearAll();

    // Called by the controller to activate or deactivate this UI.
    void SetActive(bool active);
}
```

### `Identifier` and Mode Activation

Your `Identifier` must exactly match a `ConvaiTranscriptMode` name: `"Chat"` or `"Subtitle"`. `TranscriptUIController` activates your UI when the current mode matches your identifier.

```csharp
public string Identifier => "Subtitle"; // Activated when ConvaiTranscriptMode.Subtitle is set
```

### Step-by-Step: Implementing a Custom Transcript UI

{% stepper %}
{% step %}
**Create Your MonoBehaviour**

Implement `ITranscriptUI` on a `MonoBehaviour`. The class must be in a scene that `ConvaiManager` initializes.

```csharp
using Convai.Runtime.Presentation.Services;
using Convai.Runtime.Presentation.Presenters;
using UnityEngine;

public class ClinicalNoteUI : MonoBehaviour, ITranscriptUI
{
    [SerializeField] private Transform _notesContainer;

    public string Identifier => "Chat";
    public bool IsActive { get; private set; }

    public void SetActive(bool active)
    {
        IsActive = active;
        gameObject.SetActive(active);
    }

    public void DisplayMessage(TranscriptViewModel viewModel)
    {
        if (viewModel.IsEmpty) return;
        AppendOrUpdateNote(viewModel.MessageId, viewModel.DisplayName, viewModel.Text, viewModel.IsFinal);
    }

    public void CompleteMessage(string messageId)
    {
        FinalizeNote(messageId);
    }

    public void CompletePlayerTurn() { }

    public void ClearAll()
    {
        foreach (Transform child in _notesContainer)
            Destroy(child.gameObject);
    }

    // ... your note rendering logic
}
```
{% endstep %}

{% step %}
**Add the Component to Your Scene**

Place the `MonoBehaviour` on any active `GameObject` in the scene. `ConvaiManager` discovers and registers it automatically on startup.

For manual control when auto-discovery is not appropriate:

```csharp
ConvaiManager.ActiveManager.RegisterTranscriptUI(myUI);

// Unregister when done (e.g., OnDestroy)
ConvaiManager.ActiveManager.UnregisterTranscriptUI(myUI);
```
{% endstep %}

{% step %}
**Activate Your UI via Mode**

Switch to your UI's mode using the runtime settings service or the Settings Panel. Your UI's `SetActive(true)` will be called, and the built-in UI with the matching identifier (if present) will be deactivated.

```csharp
if (ConvaiManager.ActiveManager.TryGetRuntimeSettingsService(out var settings))
{
    settings.Apply(new ConvaiRuntimeSettingsPatch
    {
        TranscriptMode = ConvaiTranscriptMode.Chat
    });
}
```
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
If both your custom `ITranscriptUI` and the built-in `ChatTranscriptUI` have `Identifier = "Chat"`, both are registered. The controller activates all registered UIs that match the current mode — both will display simultaneously. Remove or disable the built-in prefab if you want only your custom UI active.
{% endhint %}

***

## Character Visibility Filtering

When multiple `ConvaiCharacter` objects are present in a scene, every character's transcripts flow through the transcript pipeline simultaneously. Character visibility filtering controls which character's transcript the `TranscriptUIController` routes to the active `ITranscriptUI`. This is particularly useful for subtitle-style UIs where showing multiple characters' speech simultaneously is confusing, or for proximity-based scenarios where the player should only see transcripts from characters they are facing.

The SDK provides a public base class — `TranscriptFilterBase` — and two ready-to-use implementations in the `SamplesShared` layer.

{% hint style="warning" %}
`SingleCharacterFilter` and `ProximityCharacterFilter` live in `SamplesShared`. Copy them into your own assembly before modifying. Changes to `SamplesShared` scripts are overwritten on SDK updates.
{% endhint %}

***

### `TranscriptFilterBase`

`TranscriptFilterBase` is the SDK-provided base class for all character visibility filters. It handles proximity detection through a trigger collider and integrates with `IVisibleCharacterService` — the service that `TranscriptUIController` consults to determine which characters' transcripts to display.

**How it works:**

1. On `OnEnable`, if no `SphereCollider` is present on the `GameObject`, it adds one automatically (radius `5f`, isTrigger `true`) and performs an initial `SphereCastAll` to populate any characters already within range.
2. `OnTriggerEnter` / `OnTriggerExit` maintain the `CharactersInsideColliderList` — all characters within the collider radius.
3. Subclasses read `CharactersInsideColliderList` and call `VisibilityService.AddCharacter()` / `VisibilityService.RemoveCharacter()` to declare which characters are currently visible.
4. `TranscriptUIController` routes transcripts only from characters present in `IVisibleCharacterService`.

**Dependency resolution:**

`TranscriptFilterBase` calls `ConvaiManager.TryGetVisibleCharacterService()` automatically on `OnEnable`. You can also inject it manually:

```csharp
transcriptFilter.Inject(visibilityService);
```

**Placement:** Add a `TranscriptFilterBase` subclass to the player `GameObject` or a child. The collider proximity is relative to this transform.

***

### `SingleCharacterFilter`

`SingleCharacterFilter` tracks exactly one character at a time — the nearest character within the player's vision cone. Characters outside the cone or outside the collider radius are excluded. When the player turns to face a different character, the filter switches automatically.

**Best for:** Subtitle mode with multiple characters in the scene. The player sees only the transcript of the character they are looking at.

**Inspector / setup:** No Inspector fields. Place on the player `GameObject` or a child. The component resolves `ConvaiPlayer` automatically by walking up the parent hierarchy; you can also inject it:

```csharp
singleCharacterFilter.Inject(visibilityService, playerInputService);
```

**Vision cone:** Default `90°`. To override, implement `IVisionConeProvider` on `ConvaiPlayer` (or your custom player agent):

```csharp
public class ConvaiPlayer : MonoBehaviour, IConvaiPlayerAgent, IVisionConeProvider
{
    public float VisionConeAngle => 60f; // Narrow cone for focused interactions
}
```

`SingleCharacterFilter` checks for `IVisionConeProvider` on the player each `FixedUpdate` and uses the angle it returns. If the player does not implement `IVisionConeProvider`, the default `90°` is used.

***

### `ProximityCharacterFilter`

`ProximityCharacterFilter` tracks **all** characters within the collider radius that are also inside the player's vision cone. Unlike `SingleCharacterFilter`, multiple characters can be visible simultaneously.

**Best for:** Chat mode with multiple characters — all characters in front of the player contribute to the conversation transcript. Characters behind the player or outside the radius are filtered out.

**Vision cone and placement:** Same rules as `SingleCharacterFilter` — default `90°`, overridable via `IVisionConeProvider`, placed on the player.

***

### `IVisionConeProvider`

`IVisionConeProvider` is a single-member interface defined alongside `ProximityCharacterFilter`. Implement it on your player agent to provide a custom vision cone angle to both filter implementations.

```csharp
public interface IVisionConeProvider
{
    float VisionConeAngle { get; }
}
```

***

### Filter Comparison

| Filter                     | Characters shown    | Vision cone               | Best for                               |
| -------------------------- | ------------------- | ------------------------- | -------------------------------------- |
| `SingleCharacterFilter`    | Nearest one in cone | 90° default (overridable) | Subtitle mode — single-character focus |
| `ProximityCharacterFilter` | All in cone         | 90° default (overridable) | Chat mode — group conversation         |

***

### Scene Setup

{% stepper %}
{% step %}
**Add the Filter to the Player**

Add `SingleCharacterFilter` or `ProximityCharacterFilter` to your `ConvaiPlayer` `GameObject` (or a child).

If no `SphereCollider` is present, `TranscriptFilterBase` adds one automatically with radius `5f` on `OnEnable`. Adjust the radius by adding your own `SphereCollider` to the same `GameObject` before the component enables — the base class checks for an existing collider first.
{% endstep %}

{% step %}
**Ensure a Rigidbody Is Present**

Trigger callbacks (`OnTriggerEnter` / `OnTriggerExit`) require a `Rigidbody` on either the player or the character `GameObject`. The player's `ConvaiPlayer` component typically includes a `Rigidbody`. If characters do not enter/exit the filter, verify that one side of each interaction has a `Rigidbody`.
{% endstep %}

{% step %}
**Confirm the Filter Is Visible to ConvaiManager**

`TranscriptFilterBase` resolves `IVisibleCharacterService` automatically from `ConvaiManager.TryGetVisibleCharacterService()` on `OnEnable`. No Inspector wiring is required. Confirm `ConvaiManager` is initialized before the player `GameObject` enables.
{% endstep %}

{% step %}
**Test in Play Mode**

Walk toward a character. The character's transcript should appear. Turn away — after a moment (one `FixedUpdate`), the transcript should stop routing to the active UI. Walk toward a second character while in range of the first — for `SingleCharacterFilter`, only the nearer character's transcript shows; for `ProximityCharacterFilter`, both show.
{% endstep %}
{% endstepper %}

***

## Visual Customization

### Replacing Message Bubble Prefabs in Chat Mode

`ChatTranscriptUI` instantiates separate prefabs for character and player messages. Swap them in the Inspector:

1. Duplicate the default bubble prefab from `Packages/com.convai.convai-sdk-for-unity/Prefabs/TranscriptUI/`
2. Restyle the duplicate — change colors, fonts, layout, background sprites
3. Assign your duplicate to `characterMessagePrefab` or `playerMessagePrefab` on `ChatTranscriptUI`

The replacement prefab must contain a `ChatMessageBubble` component at its root. `ChatTranscriptUI` calls methods on `ChatMessageBubble` to populate text and sender info.

**`ChatMessageBubble` required references:**

| Field       | Description                                     |
| ----------- | ----------------------------------------------- |
| `senderUI`  | `TextMeshProUGUI` for the sender's display name |
| `messageUI` | `TextMeshProUGUI` for the transcript text       |

Additional styling methods available on `ChatMessageBubble`:

```csharp
bubble.SetSender("Dr. Chen");
bubble.SetSenderColor(Color.cyan);
bubble.SetMessage("The patient's vitals are stable.");
bubble.AppendMessage(" Blood pressure is normal.");
```

### Replacing the Notification Prefab

`UINotificationController` instantiates `UINotification` prefabs from its pool. To change the notification appearance:

1. Duplicate `Packages/com.convai.convai-sdk-for-unity/Prefabs/Notifications/Notification.prefab`
2. Restyle the duplicate
3. Assign your duplicate to the `uiNotificationPrefab` field on `UINotificationController`

Your replacement prefab must expose these references on its `UINotification` component:

| Field                       | Type              | Description                                        |
| --------------------------- | ----------------- | -------------------------------------------------- |
| `notificationRectTransform` | `RectTransform`   | Rect used by the controller for position animation |
| `notificationIcon`          | `Image`           | Icon sprite display                                |
| `notificationTitleText`     | `TextMeshProUGUI` | Title text                                         |
| `notificationMessageText`   | `TextMeshProUGUI` | Body text                                          |

### Replacing the Settings Panel View

If the `SettingsPanel_Landscape.prefab` layout does not fit your project, implement `ISettingsPanelView` and wire it to `SettingsPanelPresenter`. The presenter owns all business logic — your view only handles rendering and input events.

**`ISettingsPanelView` full contract:**

```csharp
public interface ISettingsPanelView
{
    // Input properties — your view reads from its controls
    string PlayerDisplayNameInput { get; }
    bool TranscriptEnabledInput { get; }
    bool NotificationsEnabledInput { get; }
    string SelectedMicrophoneDeviceId { get; }
    ConvaiTranscriptMode SelectedTranscriptModeInput { get; }
    ConversationInputMode SelectedConversationInputModeInput { get; }

    // Events — fire these from your Save and Close controls
    event Action SaveRequested;
    event Action CloseRequested;

    // Setter methods — called by the presenter to populate your controls
    void SetPlayerDisplayName(string value);
    void SetTranscriptEnabled(bool value);
    void SetNotificationsEnabled(bool value);
    void SetMicrophoneOptions(IReadOnlyList<ConvaiMicrophoneDevice> devices, string selectedDeviceId);
    void SetTranscriptModes(IReadOnlyList<ConvaiTranscriptMode> modes, ConvaiTranscriptMode selectedMode);
    void SetConversationInputMode(ConversationInputMode mode);
    void SetConversationInputModeVisible(bool visible);
}
```

The presenter calls all setter methods to initialize your controls on open. Your view fires `SaveRequested` or `CloseRequested` events; the presenter applies the patch and closes the panel controller.

***

## Usage Examples

### Medical Simulation — Clinical Notes Transcript

A surgical training simulation renders AI character transcripts as timestamped clinical notes instead of chat bubbles:

* Implement `ITranscriptUI` with `Identifier = "Chat"`
* On `DisplayMessage`, create a new note entry in a scroll panel with the speaker name, `viewModel.Timestamp`, and transcript text
* On `CompleteMessage`, add a lock indicator to finalize the note visually
* Remove the built-in `TranscriptUI_Chat.prefab` from the scene so only the clinical notes UI is active

### Multi-Character Environment — Single-Character Subtitle Focus

A museum kiosk has three exhibit guide characters in the same space. Players walk between exhibits and should only see the transcript of the guide they are currently facing:

* Add `SingleCharacterFilter` to the player `GameObject`
* Use `SubtitleTranscriptUI` as the active transcript mode
* No code changes required — `SingleCharacterFilter` automatically routes only the nearest forward-facing character's transcript to the subtitle display
* As the player turns to a different exhibit guide, the subtitle switches within one `FixedUpdate` frame

For a narrower focus on a single character at a time, implement `IVisionConeProvider` on `ConvaiPlayer` and return `60f` — the player must look more directly at the guide before their transcript appears.

### Custom Notification Skin — Themed Training Environment

A military readiness simulation replaces the default notification popup with an HUD-style alert:

1. Duplicate `Notification.prefab`
2. Replace the rounded card background with a sharp-edged HUD panel design
3. Change fonts and colors to match the simulation's visual language
4. Assign the duplicate to `UINotificationController.uiNotificationPrefab`

All animation timing, queuing, and dismissal behavior remain intact — only the visual appearance changes.

### Multi-User Fire Drill — Per-Player Attribution

A multi-user fire safety drill has up to four trainees in the same scene. The session log needs to attribute each transcript line to the specific trainee who spoke:

```csharp
using Convai.Runtime.Presentation.Services;
using UnityEngine;
using System.Collections.Generic;

public class DrillTranscriptLogger : MonoBehaviour, IMultiUserTranscriptListener
{
    private readonly List<string> _log = new();

    public string FilterCharacterId => null; // receive all characters

    public void OnCharacterTranscript(string characterId, string characterName, string text, bool isFinal)
    {
        if (isFinal) _log.Add($"[Instructor] {characterName}: {text}");
    }

    public void OnPlayerTranscript(string text, bool isFinal)
    {
        // Attribution handled in OnPlayerTranscriptWithSpeaker for multi-user rooms
    }

    public void OnPlayerTranscriptWithSpeaker(
        string speakerId, string speakerName, string participantId, string text, bool isFinal)
    {
        if (isFinal) _log.Add($"[Trainee/{speakerName}] {text}");
    }

    public IReadOnlyList<string> GetLog() => _log;
}
```

Place on any `GameObject` in the scene. `ConvaiManager` discovers and registers it automatically.

***

## Next Steps

{% content-ref url="/broken/pages/053a40b47d2606b92396e53d397d78c180dd4021" %}
[Broken link](/broken/pages/053a40b47d2606b92396e53d397d78c180dd4021)
{% endcontent-ref %}
