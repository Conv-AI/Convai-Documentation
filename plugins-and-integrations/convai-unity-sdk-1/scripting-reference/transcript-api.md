---
title: Transcript API
description: Pull-based API reference for ConvaiTranscripts — query, filter, and subscribe to the live in-memory transcript timeline from C# scripts.
last_reviewed: "4.2.0"
---

`ConvaiTranscripts` gives you pull-based, snapshot access to the room's full transcript timeline. Unlike event relay components, which push individual updates as they arrive, the `ConvaiTranscripts` facade maintains a live in-memory timeline that you query on demand. This makes it the right tool for transcript history replay, custom chat UI construction, post-session export, and any feature that needs to read multiple turns at once. Access the facade via `ConvaiManager.ActiveManager.Transcripts`.

***

## Push vs. pull

|               | Event Relays / `ConvaiEvents`                    | `ConvaiTranscripts`                                      |
| ------------- | ------------------------------------------------ | -------------------------------------------------------- |
| **Delivery**  | Push — your callback is invoked per update       | Pull — you read the timeline whenever you need it        |
| **History**   | Only the most recent update per callback         | Full history: active turns + committed turns             |
| **Use cases** | Subtitle rendering, real-time animation triggers | Post-session export, custom chat logs, assessment review |
| **Access**    | `ConvaiSessionEventRelay`, `ConvaiEvents`        | `ConvaiManager.ActiveManager.Transcripts`                |

***

## `ConvaiTranscripts` facade

### Properties

| Member            | Type                         | Description                                                        |
| ----------------- | ---------------------------- | ------------------------------------------------------------------ |
| `CurrentTimeline` | `TranscriptTimelineSnapshot` | Snapshot of the entire transcript timeline at the moment of access |

### Methods

| Method                                    | Returns                                 | Description                                                                                                     |
| ----------------------------------------- | --------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `GetTurns(TranscriptQuery?)`              | `IReadOnlyList<TranscriptTurnSnapshot>` | Returns all turns matching the optional query. Pass `null` for all turns.                                       |
| `GetTurn(string turnId)`                  | `TranscriptTurnSnapshot`                | Retrieves a specific turn by its ID. Returns `null` if not found.                                               |
| `GetLatestTurn(TranscriptParticipantRef)` | `TranscriptTurnSnapshot`                | Returns the most recent turn for the given participant. Returns `null` if none.                                 |
| `Dispose()`                               | `void`                                  | Unsubscribes from internal change events. Call when your component is destroyed if you subscribed to `Changed`. |

### Events

| Event     | Argument                | Fires When                                                                          |
| --------- | ----------------------- | ----------------------------------------------------------------------------------- |
| `Changed` | `TranscriptUpdateBatch` | The timeline changes — a turn is added, updated, completed, interrupted, or removed |

```csharp
var transcripts = ConvaiManager.ActiveManager.Transcripts;
transcripts.Changed += OnTranscriptChanged;

private void OnTranscriptChanged(TranscriptUpdateBatch batch)
{
    foreach (var turnId in batch.CompletedTurnIds)
    {
        var turn = batch.Timeline.TurnsById[turnId];
        Debug.Log($"[{turn.Participant.DisplayName}] {turn.CommittedText}");
    }
}
```

***

## `TranscriptQuery` — filtering turns

| Field                   | Type                         | Default      | Description                                          |
| ----------------------- | ---------------------------- | ------------ | ---------------------------------------------------- |
| `ParticipantKind`       | `TranscriptParticipantKind?` | `null` (all) | Filter to `Player` or `Character` turns only         |
| `PlayerOrCharacterId`   | `string`                     | `null` (all) | Filter to a specific player or character ID          |
| `ParticipantId`         | `string`                     | `null` (all) | Filter to a specific room participant ID             |
| `IncludeActiveTurns`    | `bool`                       | `true`       | Include turns that are still streaming               |
| `IncludeCommittedTurns` | `bool`                       | `true`       | Include turns that have been finalized and committed |

```csharp
var query = new TranscriptQuery
{
    ParticipantKind       = TranscriptParticipantKind.Character,
    PlayerOrCharacterId   = "char_instructor_01",
    IncludeActiveTurns    = false,
    IncludeCommittedTurns = true
};

IReadOnlyList<TranscriptTurnSnapshot> turns =
    ConvaiManager.ActiveManager.Transcripts.GetTurns(query);
```

***

## `TranscriptTurnSnapshot`

| Property                        | Type                                       | Description                                               |
| ------------------------------- | ------------------------------------------ | --------------------------------------------------------- |
| `TurnId`                        | `string`                                   | Unique identifier for this turn (same as `MessageId`)     |
| `MessageId`                     | `string`                                   | Alias for `TurnId`                                        |
| `RoomSequence`                  | `long`                                     | Monotonically increasing sequence number within the room  |
| `Participant`                   | `TranscriptParticipantRef`                 | Who produced this turn                                    |
| `StartedAtUtc`                  | `DateTime`                                 | UTC time the turn began                                   |
| `LastUpdatedAtUtc`              | `DateTime`                                 | UTC time of the most recent update                        |
| `CompletedAtUtc`                | `DateTime?`                                | UTC time the turn was committed; `null` while active      |
| `Lifecycle`                     | `TranscriptLifecycle`                      | Current lifecycle stage of this turn                      |
| `CommittedText`                 | `string`                                   | Finalized text that will not change                       |
| `InterimText`                   | `string`                                   | In-progress text from the current streaming segment       |
| `DisplayText`                   | `string`                                   | `CommittedText + InterimText` — use this for live display |
| `WasInterrupted`                | `bool`                                     | True when the turn ended due to interruption              |
| `HasText`                       | `bool`                                     | True when `DisplayText` is non-empty                      |
| `Segments`                      | `IReadOnlyList<TranscriptSegmentSnapshot>` | Individual transcript segments within this turn           |
| `ConversationTargetCharacterId` | `string`                                   | Character this player turn was directed at, if known      |

{% hint style="info" %}
Use `DisplayText` for real-time subtitle or chat rendering. It combines `CommittedText` and `InterimText` so you always show the most complete text available, regardless of lifecycle stage.
{% endhint %}

***

## `TranscriptLifecycle` enum

| Value           | Description                                                                  |
| --------------- | ---------------------------------------------------------------------------- |
| `Streaming` (0) | Turn is actively receiving text; `InterimText` is updating                   |
| `Stable` (1)    | Streaming has paused; text is stable but turn is not yet committed           |
| `Completed` (2) | Turn is fully committed; `CommittedText` is final and `InterimText` is empty |

***

## `TranscriptTimelineSnapshot`

| Property                  | Type                                                  | Description                                                               |
| ------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------- |
| `Cursor`                  | `long`                                                | Monotonically increasing value; changes with every update to the timeline |
| `ActiveTurns`             | `IReadOnlyList<TranscriptTurnSnapshot>`               | Turns currently streaming or stable — not yet committed                   |
| `CommittedTurns`          | `IReadOnlyList<TranscriptTurnSnapshot>`               | Turns that are fully finalized                                            |
| `TurnsById`               | `IReadOnlyDictionary<string, TranscriptTurnSnapshot>` | All turns indexed by `TurnId` for O(1) lookup                             |
| `LatestTurnByParticipant` | `IReadOnlyDictionary<string, TranscriptTurnSnapshot>` | Most recent turn per participant, indexed by `ParticipantId`              |

`TranscriptTimelineSnapshot.Empty` is a safe default when no session is active.

***

## `TranscriptUpdateBatch`

| Property             | Type                                    | Description                                                 |
| -------------------- | --------------------------------------- | ----------------------------------------------------------- |
| `Timeline`           | `TranscriptTimelineSnapshot`            | Full snapshot of the timeline after this batch of changes   |
| `Cursor`             | `long`                                  | Convenience accessor for `Timeline.Cursor`                  |
| `ChangedTurns`       | `IReadOnlyList<TranscriptTurnSnapshot>` | All turns that changed in this batch                        |
| `AddedTurnIds`       | `IReadOnlyList<string>`                 | IDs of turns added for the first time in this batch         |
| `UpdatedTurnIds`     | `IReadOnlyList<string>`                 | IDs of turns that received new text or state                |
| `CompletedTurnIds`   | `IReadOnlyList<string>`                 | IDs of turns that transitioned to `Completed` in this batch |
| `InterruptedTurnIds` | `IReadOnlyList<string>`                 | IDs of turns that ended due to interruption                 |
| `RemovedTurnIds`     | `IReadOnlyList<string>`                 | IDs of turns removed from the timeline                      |

***

## `TranscriptParticipantRef` struct

| Property              | Type                        | Description                                                    |
| --------------------- | --------------------------- | -------------------------------------------------------------- |
| `Kind`                | `TranscriptParticipantKind` | Whether this participant is a `Player` or `Character`          |
| `PlayerOrCharacterId` | `string`                    | The character ID or player ID associated with this participant |
| `DisplayName`         | `string`                    | Human-readable name                                            |
| `ParticipantId`       | `string`                    | Room-level participant identifier                              |
| `IsEmpty`             | `bool`                      | True when `PlayerOrCharacterId` is null or whitespace          |

Equality comparison and `==`/`!=` operators are supported.

### `TranscriptParticipantKind` enum

| Value           | Description                 |
| --------------- | --------------------------- |
| `Player` (0)    | A human player participant  |
| `Character` (1) | An AI character participant |

***

## Usage examples

### Example 1 — Post-session transcript export

A medical training simulation exports the full session transcript to JSON after the session ends, for supervisor review.

{% code title="TranscriptExporter.cs" %}
```csharp
using Convai.Domain.Models;
using Convai.Runtime.Facades;
using Newtonsoft.Json;
using System.IO;
using System.Linq;
using UnityEngine;

public class TranscriptExporter : MonoBehaviour
{
    public void ExportToJson(string outputPath)
    {
        var transcripts = ConvaiManager.ActiveManager?.Transcripts;
        if (transcripts == null) return;

        var turns = transcripts.GetTurns()
            .Where(t => t.Lifecycle == TranscriptLifecycle.Completed)
            .OrderBy(t => t.RoomSequence)
            .Select(t => new
            {
                speaker   = t.Participant.DisplayName,
                role      = t.Participant.Kind.ToString(),
                text      = t.CommittedText,
                startedAt = t.StartedAtUtc.ToString("O"),
                completed = t.CompletedAtUtc?.ToString("O")
            })
            .ToArray();

        string json = JsonConvert.SerializeObject(turns, Formatting.Indented);
        File.WriteAllText(outputPath, json);
        Debug.Log($"Transcript saved to {outputPath}");
    }
}
```
{% endcode %}

### Example 2 — Reactive chat log that appends on completion

A corporate onboarding simulation builds a scrollable chat history that appends messages only when turns are committed — avoiding flicker from interim updates.

{% code title="CompletedTurnChatLog.cs" %}
```csharp
using Convai.Domain.Models;
using Convai.Runtime.Facades;
using TMPro;
using UnityEngine;

public class CompletedTurnChatLog : MonoBehaviour
{
    [SerializeField] private TMP_Text _log;

    private ConvaiTranscripts _transcripts;

    private void OnEnable()
    {
        _transcripts = ConvaiManager.ActiveManager?.Transcripts;
        if (_transcripts != null)
            _transcripts.Changed += OnTranscriptChanged;
    }

    private void OnDisable()
    {
        if (_transcripts != null)
            _transcripts.Changed -= OnTranscriptChanged;
    }

    private void OnTranscriptChanged(TranscriptUpdateBatch batch)
    {
        foreach (var turnId in batch.CompletedTurnIds)
        {
            if (!batch.Timeline.TurnsById.TryGetValue(turnId, out var turn)) continue;
            _log.text += $"\n<b>{turn.Participant.DisplayName}:</b> {turn.CommittedText}";
        }
    }
}
```
{% endcode %}

### Example 3 — Custom live chat UI with history replay

An industrial safety drill builds a full chat UI that replays all committed transcript history on enable — so late-joining viewers see the full conversation — then listens for live changes.

{% code title="LiveChatUI.cs" %}
```csharp
using Convai.Domain.Models;
using Convai.Runtime.Facades;
using System.Linq;
using TMPro;
using UnityEngine;

public class LiveChatUI : MonoBehaviour
{
    [SerializeField] private TMP_Text _chatContent;

    private ConvaiTranscripts _transcripts;

    private void OnEnable()
    {
        _transcripts = ConvaiManager.ActiveManager?.Transcripts;
        if (_transcripts == null) return;

        var history = _transcripts.GetTurns(new TranscriptQuery
        {
            IncludeActiveTurns    = false,
            IncludeCommittedTurns = true
        }).OrderBy(t => t.RoomSequence);

        _chatContent.text = string.Join("\n",
            history.Select(t => $"<b>{t.Participant.DisplayName}:</b> {t.CommittedText}"));

        _transcripts.Changed += OnChanged;
    }

    private void OnDisable()
    {
        if (_transcripts != null)
            _transcripts.Changed -= OnChanged;
    }

    private void OnChanged(TranscriptUpdateBatch batch)
    {
        foreach (var turn in batch.ChangedTurns)
        {
            if (turn.Lifecycle == TranscriptLifecycle.Streaming)
                UpdateLiveLine(turn.Participant.DisplayName, turn.DisplayText);
        }

        foreach (var turnId in batch.CompletedTurnIds)
        {
            if (batch.Timeline.TurnsById.TryGetValue(turnId, out var turn))
                CommitLine(turn.Participant.DisplayName, turn.CommittedText);
        }
    }

    private void UpdateLiveLine(string speaker, string text) =>
        Debug.Log($"[Live] {speaker}: {text}");

    private void CommitLine(string speaker, string text) =>
        _chatContent.text += $"\n<b>{speaker}:</b> {text}";
}
```
{% endcode %}

***

## Next steps

For event-driven transcript reactions without querying the timeline, use `ConvaiCharacterEventRelay` or `ConvaiTranscriptEventRelay` — see [Character Events](character-events.md). For full character scripting API, see [Character & Player API](character-and-player-api.md).
