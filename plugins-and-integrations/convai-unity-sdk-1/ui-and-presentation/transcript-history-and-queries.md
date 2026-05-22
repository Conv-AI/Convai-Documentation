---
title: Transcript history and queries
description: >-
  Query the conversation turn timeline from code — read committed turns, detect
  interruptions, and build post-session exports or live analytics.
last_reviewed: "4.2.0"
---

`ConvaiManager.Transcripts` gives your code structured access to every conversation turn in the current session. Subscribe to `Changed` to react as turns arrive, or poll `CurrentTimeline` for a consistent snapshot of the full state at any moment. This API reflects the state managed by the runtime's `IRoomTranscriptEngine` — it does not control UI display and does not modify the transcript history.

For driving visual display from this data, see [Transcript UI](transcript-ui.md).

## Access patterns

### Subscribe to `Changed`

`ConvaiManager.Transcripts.Changed` fires every time the timeline updates. The `TranscriptUpdateBatch` payload tells you exactly what changed — new turns added, existing turns updated, turns completed, and turns interrupted — so you can react efficiently without diffing the full timeline.

```csharp
using Convai.Domain.Models;
using Convai.Runtime.Components;
using UnityEngine;

public class TranscriptReactor : MonoBehaviour
{
    private void OnEnable()
    {
        ConvaiManager.ActiveManager.Transcripts.Changed += OnTranscriptChanged;
    }

    private void OnDisable()
    {
        ConvaiManager.ActiveManager.Transcripts.Changed -= OnTranscriptChanged;
    }

    private void OnTranscriptChanged(TranscriptUpdateBatch batch)
    {
        foreach (string turnId in batch.CompletedTurnIds)
        {
            TranscriptTurnSnapshot turn = batch.Timeline.TurnsById[turnId];
            Debug.Log($"[{turn.Participant.DisplayName}] {turn.DisplayText}");
        }
    }
}
```

### Poll `CurrentTimeline`

`ConvaiManager.Transcripts.CurrentTimeline` returns an immutable `TranscriptTimelineSnapshot` — a consistent view of the full turn state at the moment you call it. Use polling for post-session exports, debrief screens, or one-off reads triggered by game events.

```csharp
public string BuildSessionReport()
{
    var timeline = ConvaiManager.ActiveManager.Transcripts.CurrentTimeline;
    var sb = new System.Text.StringBuilder();

    foreach (TranscriptTurnSnapshot turn in timeline.CommittedTurns)
        sb.AppendLine($"[{turn.StartedAtUtc:HH:mm:ss}] {turn.Participant.DisplayName}: {turn.DisplayText}");

    return sb.ToString();
}
```

## Core data structures

### `ConvaiTranscripts` — the facade

Accessed via `ConvaiManager.Transcripts`. All members are available after `ConvaiManager` initializes.

| Member | Type | Description |
| --- | --- | --- |
| `CurrentTimeline` | `TranscriptTimelineSnapshot` | Immutable snapshot of the full turn timeline right now |
| `Changed` | `event Action<TranscriptUpdateBatch>` | Fired whenever the timeline changes |
| `GetTurns(TranscriptQuery)` | `IReadOnlyList<TranscriptTurnSnapshot>` | Query turns with optional filter |
| `GetTurn(string turnId)` | `TranscriptTurnSnapshot` | Fast lookup by turn ID |
| `GetLatestTurn(TranscriptParticipantRef)` | `TranscriptTurnSnapshot` | Most recent turn for a specific participant |

### `TranscriptTimelineSnapshot`

An immutable room-wide snapshot. Every field is a collection; all are safe to iterate without null checks.

| Property | Type | Description |
| --- | --- | --- |
| `ActiveTurns` | `IReadOnlyList<TranscriptTurnSnapshot>` | Turns currently in progress (Streaming or Stable) |
| `CommittedTurns` | `IReadOnlyList<TranscriptTurnSnapshot>` | Finalized turns in room sequence order |
| `TurnsById` | `IReadOnlyDictionary<string, TranscriptTurnSnapshot>` | Fast lookup by `TurnId` — covers active and committed |
| `LatestTurnByParticipant` | `IReadOnlyDictionary<string, TranscriptTurnSnapshot>` | Most recent turn keyed by `ParticipantId` |
| `Cursor` | `long` | Monotonically increasing counter. Use to detect whether the timeline changed since your last read |

### `TranscriptTurnSnapshot`

Represents one continuous speech segment from a single participant. Immutable — a new snapshot is produced for every update.

| Property | Type | Description |
| --- | --- | --- |
| `TurnId` | `string` | Stable identifier for this turn. Also accessible as `MessageId` |
| `RoomSequence` | `long` | Monotonic ordering position within the room session |
| `Participant` | `TranscriptParticipantRef` | Who produced this turn (see below) |
| `StartedAtUtc` | `DateTime` | UTC time the turn began |
| `LastUpdatedAtUtc` | `DateTime` | UTC time of the most recent update to this turn |
| `CompletedAtUtc` | `DateTime?` | UTC time the turn finalized. `null` while still active |
| `Lifecycle` | `TranscriptLifecycle` | Current stability state (Streaming / Stable / Completed) |
| `CommittedText` | `string` | Final, confirmed portion of the transcript |
| `InterimText` | `string` | Current partial (not yet confirmed) portion |
| `DisplayText` | `string` | Concatenation of `CommittedText` + `InterimText` — use this for display |
| `WasInterrupted` | `bool` | `true` if the turn was cut short by another speaker |
| `HasText` | `bool` | `true` if `DisplayText` contains non-whitespace content |
| `ConversationTargetCharacterId` | `string` | Character this player turn was directed at (player turns only) |
| `Segments` | `IReadOnlyList<TranscriptSegmentSnapshot>` | Ordered sub-segments within the turn (advanced use) |

### `TranscriptParticipantRef`

Stable participant identity attached to every `TranscriptTurnSnapshot`.

| Property | Type | Description |
| --- | --- | --- |
| `Kind` | `TranscriptParticipantKind` | `Player` or `Character` |
| `PlayerOrCharacterId` | `string` | The player or character's stable SDK identifier |
| `DisplayName` | `string` | Human-readable name as it would appear in transcript UI |
| `ParticipantId` | `string` | Room-scoped participant identifier (useful in multi-user rooms) |
| `IsEmpty` | `bool` | `true` if `PlayerOrCharacterId` is null or whitespace |

### `TranscriptLifecycle`

Describes how stable a turn's text is at a given point in time.

| Value | Description |
| --- | --- |
| `Streaming` | Text is actively changing — interim speech recognition results arriving |
| `Stable` | Text is locked for this point in the turn, but the turn is still open |
| `Completed` | Turn is fully finalized — no further updates will arrive |

### `TranscriptUpdateBatch`

The payload delivered to `Changed` subscribers. Describes what changed since the last batch.

| Property | Type | Description |
| --- | --- | --- |
| `Timeline` | `TranscriptTimelineSnapshot` | Full timeline state after this batch |
| `Cursor` | `long` | Timeline cursor after this batch |
| `ChangedTurns` | `IReadOnlyList<TranscriptTurnSnapshot>` | Full turn snapshots for all turns that changed |
| `AddedTurnIds` | `IReadOnlyList<string>` | Turn IDs that are new since the previous batch |
| `UpdatedTurnIds` | `IReadOnlyList<string>` | Turn IDs that were updated (text changed) |
| `CompletedTurnIds` | `IReadOnlyList<string>` | Turn IDs that transitioned to `Completed` |
| `InterruptedTurnIds` | `IReadOnlyList<string>` | Turn IDs where `WasInterrupted` became `true` |
| `RemovedTurnIds` | `IReadOnlyList<string>` | Turn IDs removed from the timeline |

## Filter turns with `TranscriptQuery`

Pass a `TranscriptQuery` to `GetTurns()` to retrieve a subset of the timeline. All fields are optional — omitting a field disables that filter.

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `ParticipantKind` | `TranscriptParticipantKind?` | `null` (any) | Restrict to `Player` or `Character` turns only |
| `PlayerOrCharacterId` | `string` | `null` (any) | Restrict to a specific player or character by ID |
| `ParticipantId` | `string` | `null` (any) | Restrict by room-scoped participant ID (multi-user) |
| `IncludeActiveTurns` | `bool` | `true` | Include in-progress turns in results |
| `IncludeCommittedTurns` | `bool` | `true` | Include finalized turns in results |

**Example — all committed character turns:**

```csharp
var query = new TranscriptQuery
{
    ParticipantKind = TranscriptParticipantKind.Character,
    IncludeActiveTurns = false,
    IncludeCommittedTurns = true
};

IReadOnlyList<TranscriptTurnSnapshot> characterTurns =
    ConvaiManager.ActiveManager.Transcripts.GetTurns(query);
```

## Usage examples

### Post-session report — export committed turns

A corporate onboarding simulation generates a session transcript when the trainee completes the onboarding conversation:

```csharp
using Convai.Domain.Models;
using Convai.Runtime.Components;
using System.Text;
using UnityEngine;

public class SessionReporter : MonoBehaviour
{
    public string GenerateReport()
    {
        var timeline = ConvaiManager.ActiveManager.Transcripts.CurrentTimeline;
        var sb = new StringBuilder();
        sb.AppendLine("=== Session Transcript ===");

        foreach (TranscriptTurnSnapshot turn in timeline.CommittedTurns)
        {
            string speaker = turn.Participant.Kind == TranscriptParticipantKind.Character
                ? $"[AI] {turn.Participant.DisplayName}"
                : $"[Trainee] {turn.Participant.DisplayName}";

            sb.AppendLine($"{turn.StartedAtUtc:HH:mm:ss}  {speaker}: {turn.DisplayText}");
        }

        return sb.ToString();
    }
}
```

At runtime, call `GenerateReport()` after the session ends to produce a timestamped, ordered transcript the trainee or supervisor can review.

### Live analytics — track player word count

A communication skills simulation tracks how many words the trainee speaks in real time, updating a live counter on the debrief HUD as the conversation progresses:

```csharp
using Convai.Domain.Models;
using Convai.Runtime.Components;
using UnityEngine;
using TMPro;

public class WordCountTracker : MonoBehaviour
{
    [SerializeField] private TMP_Text _wordCountLabel;

    private void OnEnable()
    {
        ConvaiManager.ActiveManager.Transcripts.Changed += OnTranscriptChanged;
    }

    private void OnDisable()
    {
        ConvaiManager.ActiveManager.Transcripts.Changed -= OnTranscriptChanged;
    }

    private void OnTranscriptChanged(TranscriptUpdateBatch batch)
    {
        bool playerTurnChanged = false;
        foreach (TranscriptTurnSnapshot turn in batch.ChangedTurns)
        {
            if (turn.Participant.Kind == TranscriptParticipantKind.Player)
            {
                playerTurnChanged = true;
                break;
            }
        }

        if (!playerTurnChanged) return;

        int wordCount = 0;
        var query = new TranscriptQuery { ParticipantKind = TranscriptParticipantKind.Player };

        foreach (TranscriptTurnSnapshot turn in ConvaiManager.ActiveManager.Transcripts.GetTurns(query))
            wordCount += turn.DisplayText.Split(' ', System.StringSplitOptions.RemoveEmptyEntries).Length;

        _wordCountLabel.text = $"Words spoken: {wordCount}";
    }
}
```

### Interruption detection — training scoring penalty

A customer service training simulation penalizes the trainee when the AI character's turn was interrupted — indicating the trainee spoke over the instructor:

```csharp
using Convai.Domain.Models;
using Convai.Runtime.Components;
using UnityEngine;

public class InterruptionDetector : MonoBehaviour
{
    [SerializeField] private string _instructorCharacterId;
    private int _interruptionCount;

    private void OnEnable()
    {
        ConvaiManager.ActiveManager.Transcripts.Changed += OnTranscriptChanged;
    }

    private void OnDisable()
    {
        ConvaiManager.ActiveManager.Transcripts.Changed -= OnTranscriptChanged;
    }

    private void OnTranscriptChanged(TranscriptUpdateBatch batch)
    {
        foreach (string turnId in batch.InterruptedTurnIds)
        {
            if (!batch.Timeline.TurnsById.TryGetValue(turnId, out var turn)) continue;
            if (turn.Participant.PlayerOrCharacterId != _instructorCharacterId) continue;

            _interruptionCount++;
            Debug.Log($"Interruption detected. Total: {_interruptionCount}");
        }
    }

    public int GetInterruptionCount() => _interruptionCount;
}
```

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `ConvaiManager.Transcripts` is `null` | `ConvaiManager` not yet initialized | Subscribe in `OnEnable` and check `ConvaiManager.IsBootstrapped` before accessing |
| `Changed` never fires | Not subscribed, or subscribed after session ended | Subscribe in `OnEnable` before the room connects; unsubscribe in `OnDisable` |
| `CommittedTurns` is empty during session | Session not yet started or all turns still active | Check `ActiveTurns` during an active conversation; `CommittedTurns` populates as turns complete |
| `GetTurns()` returns 0 results with a filter | `PlayerOrCharacterId` or `ParticipantId` does not match any participant | Log `turn.Participant.PlayerOrCharacterId` from a `Changed` handler to find the correct ID |
| `WasInterrupted` never `true` | Session does not use multi-speaker mode | `WasInterrupted` is set by the runtime when one speaker overlaps another — confirm multi-speaker is configured |

## Next steps

You now have full read access to the room transcript timeline. For displaying this data in your scene, see Transcript UI. For configuring which visual mode is active at runtime, see the Settings Panel.

{% content-ref url="transcript-ui.md" %}
[Transcript UI](transcript-ui.md)
{% endcontent-ref %}

{% content-ref url="settings-panel.md" %}
[Settings Panel](settings-panel.md)
{% endcontent-ref %}
