# transcript ui

The transcript system routes every character and player speech segment from the Convai runtime to your UI layer. It handles partial text as speech is recognized, assembles final turns, and drives your UI through a well-defined pipeline — so your display code never touches network or audio state directly.

There are two integration paths. `ITranscriptListener` is a lightweight callback interface — right for scoring, analytics, or driving any custom component from transcript data. `ITranscriptUI` is the full display interface — right for building a replacement chat panel, world-space display, or any custom UI that needs complete control over message lifecycle. For querying the full turn history and timeline, see [Transcript History and Queries](/broken/pages/e35c99327d89a88db6262fb2f3709d28e036b516).

***

## How the Transcript System Works

The runtime delivers transcripts through a layered pipeline:

```mermaid
graph TD
    A[IRoomTranscriptEngine] -->|TranscriptUpdateBatch| B[TranscriptUIController]
    B -->|routes to active strategy| C[ITranscriptPresentationStrategy\nChat / Subtitle]
    C -->|OnMessageUpdated / OnMessageCompleted| D[ITranscriptUI\nChatTranscriptUI / SubtitleTranscriptUI]
    D --> E[Scene UI]
    B -->|simple callbacks| F[ITranscriptListener]
    F --> G[Your Script]
```

`IRoomTranscriptEngine` is the single source of truth for all transcript data. `TranscriptUIController` owns the active presentation strategy and dispatches to whichever `ITranscriptUI` implementation matches the current mode. `ITranscriptListener` is a parallel, simpler path that bypasses the strategy layer entirely.

`ConvaiManager` auto-discovers all `ITranscriptUI` and `ITranscriptListener` implementations present in your scene. You do not need to register them manually for the common case.

***

## Two Integration Paths

{% tabs %}
{% tab title="ITranscriptListener (Simple)" %}
Use `ITranscriptListener` when you need to react to transcript text without building a full custom UI. Examples: feeding transcripts into a scoring system, writing to a log, driving a custom text component, triggering scenario events based on what the player says.

**Interface contract:**

```csharp
public interface ITranscriptListener
{
    // Optional. Set to a character ID to receive only that character's transcripts.
    // Player transcripts are always received regardless of this value. Return null for no filtering.
    string FilterCharacterId { get; }

    void OnCharacterTranscript(string characterId, string characterName, string text, bool isFinal);
    void OnPlayerTranscript(string text, bool isFinal);
}
```

`isFinal` is `false` while speech is still being recognized (partial), and `true` when the turn is complete. Partial transcripts arrive frequently — only react to final ones unless you need real-time streaming feedback.

**Auto-discovery:** Add `ITranscriptListener` to any `MonoBehaviour` in the scene. `ConvaiManager` discovers and registers all implementations automatically during initialization.

**Multi-user attribution:** For multi-user rooms where you need to know which specific player spoke, implement `IMultiUserTranscriptListener` instead:

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
{% endtab %}

{% tab title="ITranscriptUI (Full Control)" %}
Use `ITranscriptUI` when you want to build a complete replacement for the built-in chat or subtitle UI — a custom scroll list, a 3D world-space panel, an HTML overlay in WebGL, or any layout the built-in prefabs cannot provide.

**Interface contract:**

```csharp
public interface ITranscriptUI
{
    // Must match a ConvaiTranscriptMode name: "Chat" or "Subtitle"
    string Identifier { get; }

    bool IsActive { get; }

    // Called for both partial and final transcripts
    void DisplayMessage(TranscriptViewModel viewModel);

    // Called when a specific message bubble should finalize
    void CompleteMessage(string messageId);

    // Called when all active player messages should finalize
    void CompletePlayerTurn();

    // Called to clear all displayed content
    void ClearAll();

    // Called by the controller to activate or deactivate this UI
    void SetActive(bool active);
}
```

`Identifier` determines which `ConvaiTranscriptMode` activates this UI. Use `"Chat"` to replace the chat UI, `"Subtitle"` to replace the subtitle UI.

`DisplayMessage` is called for both partial and final transcripts. Check `viewModel.IsFinal` to decide whether to keep updating a bubble or lock it in.

**Registration:** Add your implementation as a `MonoBehaviour` to the scene. `ConvaiManager` discovers it automatically. For manual control:

```csharp
ConvaiManager.ActiveManager.RegisterTranscriptUI(myUI);
ConvaiManager.ActiveManager.UnregisterTranscriptUI(myUI);
```
{% endtab %}
{% endtabs %}

***

## Adding the Built-In Chat UI

The SDK ships `TranscriptUI_Chat.prefab` — a ready-made scrollable chat panel with auto-scroll and sender-colored message bubbles.

{% stepper %}
{% step %}
**Add the Prefab to Your Scene**

Drag `Packages/com.convai.convai-sdk-for-unity/Prefabs/TranscriptUI/TranscriptUI_Chat.prefab` into your scene's Canvas hierarchy.

The prefab contains a `ChatTranscriptUI` component that registers itself with `ConvaiManager` on `Awake`.
{% endstep %}

{% step %}
**Ensure an EventSystem Exists**

The chat input field requires an `EventSystem` in the scene. If your scene does not have one, add it via **GameObject → UI → Event System**.
{% endstep %}

{% step %}
**Run Your Scene**

Connect to a character and speak. Character speech appears in one bubble column; your speech appears in the other. The panel auto-scrolls to the latest message as the conversation progresses.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
The chat UI activates automatically when `ConvaiTranscriptMode.Chat` is the current mode, which is the default. No additional configuration is required for basic setup.
{% endhint %}

***

## `ConvaiTranscriptDisplay` — Character-Local Display

`ConvaiTranscriptDisplay` is a lightweight component for displaying a single character's transcript directly on that character's `GameObject`. It does not participate in the room transcript pipeline and has no awareness of other characters or the player.

**Inspector fields:**

| Field                     | Default | Description                                                      |
| ------------------------- | ------- | ---------------------------------------------------------------- |
| `_transcriptText`         | —       | `TMP_Text` reference to render into                              |
| `_showPartialTranscripts` | `true`  | Update text during partial recognition                           |
| `_appendMode`             | `false` | Append new transcripts instead of replacing                      |
| `_clearOnNewFinal`        | `true`  | Clear the buffer before each final transcript (append mode only) |
| `_maxCharacters`          | `1000`  | Maximum characters kept in append mode. `0` = unlimited          |

**Requirement:** Must be on the same `GameObject` as `ConvaiCharacter`. Auto-subscribes to that character's transcript events.

{% hint style="info" %}
Use `ConvaiTranscriptDisplay` for per-character labels — a floating name tag above a training station, a panel display beside a character model. For full conversation history or player transcripts, use the chat prefab or `ITranscriptListener`.
{% endhint %}

***

## Switching the Active Transcript Mode

Switch transcript modes through the runtime settings service. The change applies immediately — the matching `ITranscriptUI` activates and any previous UI deactivates.

```csharp
using Convai.Runtime.Components;
using Convai.Shared.Types;

if (ConvaiManager.ActiveManager.TryGetRuntimeSettingsService(out var settings))
{
    var result = settings.Apply(new ConvaiRuntimeSettingsPatch
    {
        TranscriptMode = ConvaiTranscriptMode.Subtitle
    });

    if (!result.Success)
        Debug.LogWarning($"[Transcript] Mode switch failed: {result.ValidationMessage}");
}
```

Users can also switch modes through the built-in Settings Panel. See [Settings Panel](/broken/pages/5b9ad404d6290ca7355a75ec12b6e2f1a9ea1ceb) for details on what modes the panel exposes at runtime.

***

## Clearing the Transcript Display

Call `ClearAll()` on any `ITranscriptUI` component to destroy all displayed message bubbles and reset the panel. This clears the **visual display only** — the underlying room turn history in `ConvaiManager.Transcripts` is read-only and is not affected.

```csharp
using Convai.Runtime.Presentation.Views.Transcript;

// Via serialized field (recommended)
[SerializeField] private ChatTranscriptUI _chatUI;

public void ResetForNextScenario()
{
    _chatUI.ClearAll();
}
```

```csharp
// Or via scene lookup when you don't hold a reference
FindObjectOfType<ChatTranscriptUI>()?.ClearAll();
```

{% hint style="warning" %}
`ConvaiManager` does not expose a global `ClearAll()`. You must hold a direct component reference, use `FindObjectOfType`, or implement your own central reset controller that holds references to all registered UIs.
{% endhint %}

**Typical use cases:**

* New training scenario starts — clear the previous scenario's conversation history from the screen
* Post-debrief reset — trainee has reviewed the chat; wipe it before the next session begins
* Scene transition — clear before loading new content so stale messages do not flash in

***

## Usage Examples

### Compliance Scoring — `ITranscriptListener`

A safety training simulation scores a trainee's responses by reading final transcripts from the AI instructor interaction:

```csharp
using Convai.Runtime.Presentation.Services;
using UnityEngine;

public class ComplianceScorer : MonoBehaviour, ITranscriptListener
{
    [SerializeField] private string _instructorCharacterId;
    [SerializeField] private ScoreBoard _scoreBoard;

    public string FilterCharacterId => _instructorCharacterId;

    public void OnCharacterTranscript(string characterId, string characterName, string text, bool isFinal)
    {
        // Instructor prompt — not scored, but could be logged for reference
    }

    public void OnPlayerTranscript(string text, bool isFinal)
    {
        if (!isFinal) return;
        bool passed = text.Contains("hazard identified", System.StringComparison.OrdinalIgnoreCase);
        _scoreBoard.RecordResponse(text, passed);
    }
}
```

Place on any `GameObject` in the scene. `ConvaiManager` discovers and registers it automatically.

### Museum Kiosk — `ConvaiTranscriptDisplay`

A natural history museum kiosk shows each exhibit character's speech on the panel beside their display case:

* Add `ConvaiTranscriptDisplay` to the `ConvaiCharacter` `GameObject`
* Assign the panel's `TMP_Text` to `_transcriptText`
* Set `_appendMode` off and `_clearOnNewFinal` on — each new complete sentence replaces the previous one on the panel

### Multi-User Training Room — `IMultiUserTranscriptListener`

A multi-user fire safety drill tracks which specific trainee spoke and what they said for the post-session report:

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
        // Use OnPlayerTranscriptWithSpeaker for attribution in multi-user rooms
    }

    public void OnPlayerTranscriptWithSpeaker(
        string speakerId, string speakerName, string participantId, string text, bool isFinal)
    {
        if (isFinal) _log.Add($"[Trainee] {speakerName}: {text}");
    }

    public IReadOnlyList<string> GetLog() => _log;
}
```

***

## Next Steps

{% content-ref url="/broken/pages/e35c99327d89a88db6262fb2f3709d28e036b516" %}
[Broken link](/broken/pages/e35c99327d89a88db6262fb2f3709d28e036b516)
{% endcontent-ref %}

{% content-ref url="/broken/pages/7a60234ac501c2d7c4f7240396d285b464a3ae06" %}
[Broken link](/broken/pages/7a60234ac501c2d7c4f7240396d285b464a3ae06)
{% endcontent-ref %}

{% content-ref url="/broken/pages/e6b069465db52fd82502fece5f92ee2a696f9517" %}
[Broken link](/broken/pages/e6b069465db52fd82502fece5f92ee2a696f9517)
{% endcontent-ref %}
