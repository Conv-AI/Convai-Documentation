---
title: Transcript API
description: Query transcript turns, subscribe to live changes, read captions, and export session history from Unity scripts using the transcript facade.
last_reviewed: "4.4.0"
---

`ConvaiTranscripts` is the Convai Unity SDK's canonical transcript facade: a live, in-memory timeline of every player and character turn in the room, with pull-based queries, push-based change events, live captions, and a session export helper. Use this page when scripting custom chat UI, transcript export, or turn-level conversation logic. Access the facade through `ConvaiManager.ActiveManager.Transcripts`.

{% hint style="warning" %}
**Breaking change in SDK 4.4.0.** The snapshot-based transcript model is replaced. `CurrentTimeline` now returns `TranscriptTimeline` instead of `TranscriptTimelineSnapshot`. The `Changed` event now carries `TranscriptChangeBatch` instead of `TranscriptUpdateBatch`, and turns are `TranscriptTurn` instead of `TranscriptTurnSnapshot`. The entire legacy presentation and history layer is removed: `ITranscriptUI`, `ITranscriptListener`, `TranscriptViewModel`, `TranscriptUIController`, `ChatPresentationStrategy`, `ITranscriptPresentationStrategy`, `ConversationHistoryService`, `TranscriptEntry`, and `ConversationExportFormat` no longer exist. Replace `ConversationHistoryService.Entries` with `CurrentTimeline.Turns` or `GetTurns(...)`, replace `EntryAdded` with `SubscribeCommitted(...)`, and replace `Export(ConversationExportFormat)` with `Export(TranscriptExportFormat)`. If you used the beta `TranscriptSubscriptionOptions.IncludeInterim`/`IncludeCommitted` fields, rename them to `IncludeActive` and `IncludeTerminal`.
{% endhint %}

***

## Push vs. pull

|               | Event relays (`ConvaiTranscriptEventRelay`, `ConvaiEvents`) | `ConvaiTranscripts`                                                   |
| ------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------- |
| **Delivery**  | Push — Inspector `UnityEvent`s or C# events fire per update  | Pull (`CurrentTimeline`, `GetTurns`) and push (`Changed`, `Subscribe`) |
| **History**   | Only the current update                                      | Full history: active turns, committed turns, and live captions        |
| **Use cases** | Subtitle rendering, per-character animation triggers         | Custom chat UI, post-session export, turn-level assessment logic       |
| **Access**    | `ConvaiTranscriptEventRelay`, `ConvaiManager.ActiveManager.Events` | `ConvaiManager.ActiveManager.Transcripts`                         |

***

## `ConvaiTranscripts` facade

```csharp
ConvaiManager manager = ConvaiManager.ActiveManager;
if (manager == null || !manager.TryGetTranscripts(out ConvaiTranscripts transcripts))
    return;
```

`ConvaiManager.ActiveManager.Transcripts` throws `InvalidOperationException` if the SDK has not finished bootstrapping. Use `manager.TryGetTranscripts(out ConvaiTranscripts transcripts)` when the caller might run before initialization completes, such as `OnEnable`.

### Properties

| Member                  | Type                        | Description                                                                                                                     |
| ------------------------ | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `CurrentTimeline`        | `TranscriptTimeline`         | Current transcript timeline. Returns the same instance until the underlying engine snapshot changes.                              |
| `CurrentCaptions`        | `TranscriptCaptionSnapshot`  | Current live caption snapshot for speech-aligned subtitles.                                                                        |
| `IsPresentationEnabled`  | `bool`                       | Whether shipped presentation components should render transcript updates. Read-only; canonical history keeps recording regardless. |

### Events

| Event                        | Argument                    | Fires when                                                                             |
| ----------------------------- | ----------------------------- | ----------------------------------------------------------------------------------------- |
| `Changed`                     | `TranscriptChangeBatch`      | One or more turns were added, updated, committed, interrupted, corrected, or removed     |
| `TurnUpdated`                 | `TranscriptTurn`             | A turn receives new text or a non-terminal state change                                  |
| `TurnCommitted`                | `TranscriptTurn`             | A turn transitions to `Committed` or `Interrupted`                                       |
| `TurnCorrected`                | `TranscriptTurn`             | A previously committed turn's text is corrected                                          |
| `TurnRemoved`                  | `string` (turn ID)           | A turn is removed from the timeline                                                      |
| `CaptionsChanged`              | `TranscriptCaptionSnapshot`  | The live caption snapshot changes                                                        |
| `PresentationEnabledChanged`   | `bool`                       | `IsPresentationEnabled` changes                                                          |

### Methods

| Method                                                                                          | Returns                          | Description                                                                                             |
| ------------------------------------------------------------------------------------------------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `GetTurns(TranscriptQuery query = null)`                                                        | `IReadOnlyList<TranscriptTurn>`  | Returns all turns matching the optional query. Pass `null` for every turn.                              |
| `GetTurn(string turnId)`                                                                         | `TranscriptTurn`                 | Retrieves a specific turn by ID. Returns `null` if not found.                                            |
| `GetLatestTurn(TranscriptParticipantRef participant)`                                            | `TranscriptTurn`                 | Returns the most recent turn for the given participant. Returns `null` if none.                          |
| `Subscribe(Action<TranscriptChange> callback, TranscriptSubscriptionOptions options = null)`     | `IDisposable`                    | Registers a callback for matching turn changes. Dispose the return value to unsubscribe.                |
| `SubscribeCommitted(Action<TranscriptChange> callback, TranscriptSubscriptionOptions options = null)` | `IDisposable`                | Shortcut for `Subscribe` with `IncludeActive = false` and `IncludeTerminal = true` — committed and interrupted turns only. |
| `SubscribeCaptions(Action<TranscriptCaption> callback, TranscriptCaptionSubscriptionOptions options = null)` | `IDisposable`             | Registers a callback for live caption updates.                                                           |
| `Clear()`                                                                                         | `void`                           | Clears the canonical transcript history.                                                                 |
| `Export(TranscriptExportFormat format)`                                                          | `string`                         | Serializes every committed turn to plain text, Markdown, or JSON.                                        |
| `Dispose()`                                                                                       | `void`                           | Unsubscribes from internal engine events. Call when the owning component is destroyed.                  |

```csharp
transcripts.Changed += OnTranscriptChanged;

private void OnTranscriptChanged(TranscriptChangeBatch batch)
{
    foreach (TranscriptChange change in batch.Changes)
    {
        if (change.Kind == TranscriptChangeKind.Removed || change.Turn == null) continue;
        Debug.Log($"[{change.Turn.Speaker.DisplayName}] {change.Turn.DisplayText}");
    }
}
```

***

## `TranscriptTimeline`

| Property         | Type                                          | Description                                                               |
| ------------------ | ------------------------------------------------ | ------------------------------------------------------------------------------ |
| `Cursor`          | `long`                                        | Monotonically increasing value that changes whenever the timeline updates |
| `ActiveTurns`     | `IReadOnlyList<TranscriptTurn>`               | Turns that are not yet committed (`Listening`, `Streaming`, or `Stable`)   |
| `CommittedTurns`  | `IReadOnlyList<TranscriptTurn>`               | Turns in a terminal state (`Committed` or `Interrupted`)                  |
| `TurnsById`       | `IReadOnlyDictionary<string, TranscriptTurn>` | All turns indexed by `TranscriptTurn.Id`                                  |
| `Turns`           | `IReadOnlyList<TranscriptTurn>`               | `ActiveTurns` and `CommittedTurns` combined and ordered by `RoomSequence`  |

`TranscriptTimeline.Empty` is a static, reusable empty instance — a safe default before a session connects.

***

## `TranscriptTurn`

| Property             | Type                             | Description                                                            |
| ---------------------- | ----------------------------------- | -------------------------------------------------------------------------- |
| `Id`                  | `string`                         | Unique identifier for this turn                                        |
| `MessageId`           | `string`                         | Message identifier associated with this turn                           |
| `ResponseId`          | `string`                         | Response identifier associated with this turn, when applicable         |
| `RoomSequence`        | `long`                           | Monotonically increasing sequence number within the room                |
| `Revision`            | `int`                            | Increments each time the turn's content or state changes               |
| `Speaker`             | `TranscriptSpeaker`              | Who produced this turn                                                 |
| `State`               | `TranscriptTurnState`            | Current lifecycle state of this turn                                   |
| `PrimaryTextSource`   | `TranscriptTextSource`           | Dominant text source backing this turn's display text                  |
| `StableText`          | `string`                         | Finalized text that will not change on further updates                 |
| `InterimText`         | `string`                         | In-progress text from the current streaming segment                    |
| `DisplayText`         | `string`                         | Text to render for this turn — combines `StableText` and `InterimText` |
| `StartedAtUtc`        | `DateTime`                       | UTC time the turn began                                                |
| `LastUpdatedAtUtc`    | `DateTime`                       | UTC time of the most recent update                                     |
| `CommittedAtUtc`      | `DateTime?`                      | UTC time the turn was committed; `null` while active                   |
| `WasInterrupted`      | `bool`                           | `true` when the turn ended due to interruption                         |
| `Segments`            | `IReadOnlyList<TranscriptSegment>` | Individual transcript segments that make up this turn                |
| `HasText`             | `bool`                           | `true` when `DisplayText` is non-empty                                 |
| `IsCommitted`         | `bool`                           | `true` when `State` is `Committed` or `Interrupted`                    |

{% hint style="info" %}
Use `DisplayText` for real-time rendering. It combines `StableText` and `InterimText`, so it always shows the most complete text available regardless of `State`.
{% endhint %}

### `TranscriptTurnState` enum

| Value             | Description                                                                          |
| ------------------- | --------------------------------------------------------------------------------------- |
| `Listening` (0)    | Turn is open and waiting for speech or text input; no text captured yet               |
| `Streaming` (1)    | Turn is actively receiving text; `InterimText` is updating                            |
| `Stable` (2)       | Streaming has paused; text is stable but the turn is not yet committed                |
| `Committed` (4)    | Turn is fully committed; `StableText` is final                                        |
| `Interrupted` (5)  | Turn ended because it was interrupted (`WasInterrupted` is `true`)                     |
| `Discarded` (6)    | Turn was closed with no text and excluded from both `ActiveTurns` and `CommittedTurns` |

***

## `TranscriptSegment`

| Property        | Type                    | Description                                  |
| ----------------- | ------------------------- | ----------------------------------------------- |
| `Id`             | `string`                | Unique identifier for this segment            |
| `TurnId`         | `string`                | ID of the parent `TranscriptTurn`             |
| `Speaker`        | `TranscriptSpeaker`     | Who produced this segment                     |
| `StableText`     | `string`                | Finalized text for this segment               |
| `InterimText`    | `string`                | In-progress text for this segment             |
| `DisplayText`    | `string`                | Text to render for this segment               |
| `State`          | `TranscriptTurnState`   | Lifecycle state of this segment               |
| `Source`         | `TranscriptTextSource`  | Origin of this segment's text                 |
| `StartedAtUtc`   | `DateTime`              | UTC time this segment began                   |
| `UpdatedAtUtc`   | `DateTime`              | UTC time of the most recent update            |
| `StoppedAtUtc`   | `DateTime?`             | UTC time this segment stopped; `null` while active |

### `TranscriptTextSource` enum

| Value                     | Description                                              |
| --------------------------- | ------------------------------------------------------------ |
| `Unknown` (0)              | Source could not be determined                            |
| `InterimAsr` (1)           | In-progress speech-to-text recognition                    |
| `AsrFinal` (2)             | Finalized speech-to-text recognition                       |
| `ProcessedFinal` (3)       | Finalized text after player-side processing                |
| `TypedText` (4)            | Text typed by the player rather than spoken                |
| `BotOutput` (5)            | Finalized character response text                          |
| `BotPreview` (6)           | In-progress character response preview (LLM streaming)     |
| `LegacyBotTranscript` (7)  | Character transcript text from the legacy pipeline          |

***

## `TranscriptSpeaker`

| Property         | Type                    | Description                                  |
| ------------------ | ------------------------- | ----------------------------------------------- |
| `Type`            | `TranscriptSpeakerType` | Whether this speaker is a `Player`, `Character`, or `System` |
| `Id`              | `string`                | Character ID or player ID for this speaker    |
| `DisplayName`     | `string`                | Human-readable name                            |
| `ParticipantId`   | `string`                | Room-level participant identifier              |

### `TranscriptSpeakerType` enum

| Value             | Description                                                    |
| ------------------- | ------------------------------------------------------------------ |
| `Player` (0)       | A human player participant                                       |
| `Character` (1)    | An AI character participant                                       |
| `System` (2)       | A system-originated speaker, not tied to a player or character   |

***

## `TranscriptChange` and `TranscriptChangeBatch`

`TranscriptChange`:

| Property   | Type                     | Description                                          |
| ------------ | -------------------------- | ------------------------------------------------------- |
| `Kind`      | `TranscriptChangeKind`    | The kind of change this instance represents          |
| `Turn`      | `TranscriptTurn`          | The affected turn; `null` when `Kind` is `Removed`    |
| `TurnId`    | `string`                  | ID of the affected turn                               |

`TranscriptChangeBatch`:

| Property       | Type                              | Description                                              |
| ---------------- | ------------------------------------ | ------------------------------------------------------------ |
| `Timeline`      | `TranscriptTimeline`               | Full timeline after this batch of changes                |
| `Changes`       | `IReadOnlyList<TranscriptChange>`  | Every change included in this batch                      |
| `ChangedTurns`  | `IReadOnlyList<TranscriptTurn>`    | Convenience accessor: every non-null `Turn` from `Changes` |

### `TranscriptChangeKind` enum

| Value              | Description                                                       |
| -------------------- | --------------------------------------------------------------------- |
| `Added` (0)         | A new turn was created                                            |
| `Updated` (1)       | An existing turn received new text or a non-terminal state change |
| `Committed` (2)     | A turn transitioned to `Committed`                                |
| `Interrupted` (3)   | A turn transitioned to `Interrupted`                              |
| `Corrected` (4)     | A previously committed turn's text was corrected                  |
| `Removed` (5)       | A turn was removed from the timeline                              |

***

## `TranscriptQuery` — filter `GetTurns` results

| Field                    | Type                          | Default      | Description                                            |
| -------------------------- | -------------------------------- | -------------- | ----------------------------------------------------------- |
| `ParticipantKind`         | `TranscriptParticipantKind?`   | `null` (all) | Filter to `Player` or `Character` turns only            |
| `PlayerOrCharacterId`     | `string`                       | `null` (all) | Filter to a specific player or character ID              |
| `ParticipantId`           | `string`                       | `null` (all) | Filter to a specific room participant ID                 |
| `IncludeActiveTurns`      | `bool`                         | `true`       | Include turns that are still active (not yet committed)  |
| `IncludeCommittedTurns`   | `bool`                         | `true`       | Include turns that have been committed or interrupted     |

```csharp
var query = new TranscriptQuery
{
    ParticipantKind      = TranscriptParticipantKind.Character,
    PlayerOrCharacterId  = "char_instructor_01",
    IncludeActiveTurns   = false,
    IncludeCommittedTurns = true
};

IReadOnlyList<TranscriptTurn> turns = transcripts.GetTurns(query);
```

`TranscriptQuery` is unchanged from earlier SDK versions — it keeps the `IncludeActiveTurns`/`IncludeCommittedTurns` field names. Only the newer `TranscriptSubscriptionOptions`, used by `Subscribe`, uses the renamed `IncludeActive`/`IncludeTerminal` fields.

### `TranscriptParticipantKind` enum

| Value             | Description                    |
| ------------------- | --------------------------------- |
| `Player` (0)       | A human player participant       |
| `Character` (1)    | An AI character participant      |

### `TranscriptParticipantRef` struct

Used as the `participant` argument to `GetLatestTurn`.

| Property               | Type                        | Description                                                    |
| ------------------------ | ----------------------------- | -------------------------------------------------------------------- |
| `Kind`                  | `TranscriptParticipantKind` | Whether this participant is a `Player` or `Character`                |
| `PlayerOrCharacterId`   | `string`                    | The character ID or player ID for this participant                   |
| `DisplayName`           | `string`                    | Human-readable name                                                   |
| `ParticipantId`         | `string`                    | Room-level participant identifier                                     |
| `IsEmpty`               | `bool`                      | `true` when `PlayerOrCharacterId` is null or whitespace                |

Constructed with `new TranscriptParticipantRef(TranscriptParticipantKind kind, string playerOrCharacterId, string displayName, string participantId = null)`. Implements `IEquatable<TranscriptParticipantRef>` and the `==`/`!=` operators.

***

## `TranscriptSubscriptionOptions` — filter `Subscribe` callbacks

| Field               | Type                       | Default      | Description                                                                          |
| --------------------- | ----------------------------- | -------------- | ----------------------------------------------------------------------------------------- |
| `ReplayExisting`     | `bool`                      | `false`      | When `true`, `Subscribe` immediately invokes the callback for every matching turn already in `CurrentTimeline` |
| `IncludeActive`      | `bool`                      | `true`       | Include turns that are not yet committed                                             |
| `IncludeTerminal`    | `bool`                      | `true`       | Include turns that are committed or interrupted                                       |
| `SpeakerType`        | `TranscriptSpeakerType?`    | `null` (all) | Filter to a specific speaker type                                                     |
| `SpeakerId`          | `string`                    | `null` (all) | Filter to a specific speaker ID                                                       |
| `ParticipantId`      | `string`                    | `null` (all) | Filter to a specific room participant ID                                              |

In SDK 4.4.0, these fields were renamed from `IncludeInterim` and `IncludeCommitted` to `IncludeActive` and `IncludeTerminal`.

***

## Live captions

Captions are a separate, ephemeral projection of speech-aligned text — kept apart from durable chat history so ephemeral TTS preview text is never treated as canonical conversation history.

### `TranscriptCaption`

| Property            | Type                      | Description                                          |
| --------------------- | --------------------------- | --------------------------------------------------------- |
| `TurnId`             | `string`                  | ID of the transcript turn this caption is aligned to |
| `Speaker`            | `TranscriptSpeaker`       | Who produced this caption                            |
| `Text`               | `string`                  | Caption text                                          |
| `State`              | `TranscriptCaptionState`  | Current caption state                                 |
| `UpdatedAtUtc`       | `DateTime`                | UTC time of the most recent update                    |
| `HasText`            | `bool`                    | `true` when `Text` is non-empty                       |
| `IsFinal`            | `bool`                    | `true` when `State` is `Completed` or `Interrupted`    |
| `WasInterrupted`     | `bool`                    | `true` when `State` is `Interrupted`                  |

### `TranscriptCaptionState` enum

| Value              | Description                                        |
| -------------------- | ------------------------------------------------------- |
| `Streaming` (0)     | Caption text is actively updating                  |
| `Stable` (1)        | Caption text has paused updating but is not yet final |
| `Completed` (2)     | Caption finished normally                           |
| `Interrupted` (3)   | Caption ended because the turn was interrupted      |

### `TranscriptCaptionSnapshot`

| Property     | Type                                 | Description                                                    |
| -------------- | --------------------------------------- | -------------------------------------------------------------------- |
| `Cursor`      | `long`                                | Monotonically increasing value that changes whenever captions update |
| `Captions`    | `IReadOnlyList<TranscriptCaption>`   | Current set of live captions                                        |

`TranscriptCaptionSnapshot.Empty` is a static, reusable empty instance.

### `TranscriptCaptionSubscriptionOptions`

| Field                | Type                       | Default      | Description                                                                          |
| ---------------------- | ----------------------------- | -------------- | ----------------------------------------------------------------------------------------- |
| `ReplayLatest`        | `bool`                      | `true`       | When `true`, `SubscribeCaptions` immediately invokes the callback for every current matching caption |
| `IncludeStreaming`    | `bool`                      | `true`       | Include captions that are still updating                                             |
| `IncludeFinal`        | `bool`                      | `true`       | Include captions that have completed or were interrupted                              |
| `SpeakerType`         | `TranscriptSpeakerType?`    | `null` (all) | Filter to a specific speaker type                                                     |
| `SpeakerId`           | `string`                    | `null` (all) | Filter to a specific speaker ID                                                       |
| `ParticipantId`       | `string`                    | `null` (all) | Filter to a specific room participant ID                                              |

***

## Export the transcript

`Export(TranscriptExportFormat format)` serializes every turn in `CurrentTimeline.CommittedTurns`, ordered by `RoomSequence`, to a single string. Speaker labels fall back to `Speaker.Type` when `Speaker.DisplayName` is empty.

### `TranscriptExportFormat` enum

| Value            | Description                                                 |
| ------------------ | ---------------------------------------------------------------- |
| `PlainText` (0)   | One line per turn: `speaker: text`                              |
| `Markdown` (1)    | One line per turn: `**speaker:** text`, with a blank line between turns |
| `Json` (2)        | Indented JSON array of the committed `TranscriptTurn` objects     |

***

## Usage examples

### Example 1 — Post-session transcript export

A medical training simulation exports the full session transcript to JSON after the session ends, for supervisor review.

{% code title="TranscriptExporter.cs" %}
```csharp
using Convai.Domain.Models;
using Convai.Runtime.Components;
using Convai.Runtime.Facades;
using System.IO;
using UnityEngine;

public class TranscriptExporter : MonoBehaviour
{
    public void ExportToJson(string outputPath)
    {
        ConvaiManager manager = ConvaiManager.ActiveManager;
        if (manager == null || !manager.TryGetTranscripts(out ConvaiTranscripts transcripts))
            return;

        string json = transcripts.Export(TranscriptExportFormat.Json);
        File.WriteAllText(outputPath, json);
        Debug.Log($"Transcript saved to {outputPath}");
    }
}
```
{% endcode %}

### Example 2 — Reactive chat log that appends on commit

A corporate onboarding simulation builds a scrollable chat history that appends messages only when turns are committed — avoiding flicker from interim updates.

{% code title="CompletedTurnChatLog.cs" %}
```csharp
using Convai.Domain.Models;
using Convai.Runtime.Components;
using Convai.Runtime.Facades;
using System;
using TMPro;
using UnityEngine;

public class CompletedTurnChatLog : MonoBehaviour
{
    [SerializeField] private TMP_Text _log;

    private IDisposable _subscription;

    private void OnEnable()
    {
        ConvaiManager manager = ConvaiManager.ActiveManager;
        if (manager == null || !manager.TryGetTranscripts(out ConvaiTranscripts transcripts))
            return;

        _subscription = transcripts.SubscribeCommitted(OnTurnCommitted, new TranscriptSubscriptionOptions
        {
            ReplayExisting = true
        });
    }

    private void OnDisable() => _subscription?.Dispose();

    private void OnTurnCommitted(TranscriptChange change)
    {
        if (change.Turn == null) return;
        _log.text += $"\n<b>{change.Turn.Speaker.DisplayName}:</b> {change.Turn.DisplayText}";
    }
}
```
{% endcode %}

### Example 3 — Chat history with live subtitles

An industrial safety drill replays committed chat history on enable, then keeps a subtitle line in sync with live captions — separately from the durable chat log.

{% code title="LiveChatAndSubtitleUI.cs" %}
```csharp
using Convai.Domain.Models;
using Convai.Runtime.Components;
using Convai.Runtime.Facades;
using System;
using System.Linq;
using TMPro;
using UnityEngine;

public class LiveChatAndSubtitleUI : MonoBehaviour
{
    [SerializeField] private TMP_Text _chatContent;
    [SerializeField] private TMP_Text _subtitleText;

    private IDisposable _chatSubscription;
    private IDisposable _captionSubscription;

    private void OnEnable()
    {
        ConvaiManager manager = ConvaiManager.ActiveManager;
        if (manager == null || !manager.TryGetTranscripts(out ConvaiTranscripts transcripts))
            return;

        _chatContent.text = string.Join("\n",
            transcripts.CurrentTimeline.CommittedTurns
                .OrderBy(turn => turn.RoomSequence)
                .Select(turn => $"<b>{turn.Speaker.DisplayName}:</b> {turn.DisplayText}"));

        _chatSubscription = transcripts.SubscribeCommitted(OnTurnCommitted);
        _captionSubscription = transcripts.SubscribeCaptions(OnCaption);
    }

    private void OnDisable()
    {
        _chatSubscription?.Dispose();
        _captionSubscription?.Dispose();
    }

    private void OnTurnCommitted(TranscriptChange change)
    {
        if (change.Turn == null) return;
        _chatContent.text += $"\n<b>{change.Turn.Speaker.DisplayName}:</b> {change.Turn.DisplayText}";
    }

    private void OnCaption(TranscriptCaption caption) => _subtitleText.text = caption.Text;
}
```
{% endcode %}

***

## Troubleshooting

| Symptom | Likely Cause | Fix |
| ------- | ------------ | --- |
| `ConvaiManager.ActiveManager.Transcripts` throws `InvalidOperationException` | Accessed before the SDK finished bootstrapping | Use `manager.TryGetTranscripts(out var transcripts)` instead of the `Transcripts` property during early `OnEnable` or `Awake` |
| `GetTurns()` returns an empty list | No turns exist yet, or the query's `IncludeActiveTurns` is `false` while every current turn is still active | Omit the `TranscriptQuery`, or set `IncludeActiveTurns = true` to include in-progress turns |
| `Subscribe` callback never fires | Subscribed too late, or `IncludeActive`/`IncludeTerminal` exclude every matching turn | Subscribe before or immediately after `ConnectAsync`; set `ReplayExisting = true` to receive existing turns immediately |
| `TranscriptTurn.StableText` is empty | Turn is still `Streaming` or `Stable` — text is not stable until the turn commits | Use `DisplayText` for in-progress rendering, or subscribe with `SubscribeCommitted` |
| `SubscribeCaptions` callback never fires | `IncludeStreaming`/`IncludeFinal` or the speaker filters exclude every matching caption, or `ReplayLatest` is `false` and no new caption has arrived yet | Check `IncludeStreaming`, `IncludeFinal`, `SpeakerType`, `SpeakerId`, and `ParticipantId` on `TranscriptCaptionSubscriptionOptions`; set `ReplayLatest = true` to receive the current caption immediately |

***

## Next steps

For event-driven transcript reactions without querying the timeline, use `ConvaiCharacterEventRelay` or `ConvaiTranscriptEventRelay` — see [Character Events](character-events.md). For the full character scripting API, see [Character & Player API](character-and-player-api.md). For the complete list of facade accessors on `ConvaiManager`, see [ConvaiManager API](convaimanager-api.md).
