---
title: Transcript history and queries
description: >-
  Read the current conversation turn timeline from code, react to live turn
  changes as they happen, and export session history as text, Markdown, or
  JSON.
last_reviewed: 4.4.0
---

`ConvaiManager.ActiveManager.Transcripts` gives your code structured access to every conversation turn in the current room session. Read the current state through `CurrentTimeline` and `GetTurns`, react to live changes through `Subscribe` and `SubscribeCommitted`, and export finished turns through `Export`. This facade does not control what appears on screen — see [Transcript UI](./) for that. For the full API reference, see [Transcript API](../../scripting-reference/transcript-api.md).

## Read the current transcript state

`ConvaiManager.ActiveManager.Transcripts.CurrentTimeline` returns an immutable `TranscriptTimeline` — a consistent view of every turn in the room at the moment you read it. Reading it repeatedly is cheap: it returns the same instance until the runtime publishes a change, and a new instance only when the timeline actually changes.

{% hint style="info" %}
`ConvaiManager.ActiveManager.Transcripts` throws `InvalidOperationException` if the SDK has not finished initializing. For code that runs early (`OnEnable`, `Awake`), use `ConvaiManager.ActiveManager.TryGetTranscripts(out ConvaiTranscripts transcripts)` instead, which returns `false` rather than throwing.
{% endhint %}

| Member | Type | Description |
| --- | --- | --- |
| `Cursor` | `long` | Monotonically increasing counter. Changes whenever the runtime publishes an update |
| `ActiveTurns` | `IReadOnlyList<TranscriptTurn>` | Turns still in progress — not yet committed or interrupted |
| `CommittedTurns` | `IReadOnlyList<TranscriptTurn>` | Finalized turns (`Committed` or `Interrupted` state) |
| `TurnsById` | `IReadOnlyDictionary<string, TranscriptTurn>` | Fast lookup by `TranscriptTurn.Id`, covering active and committed turns |
| `Turns` | `IReadOnlyList<TranscriptTurn>` | Every turn (active and committed), ordered by `RoomSequence` |

Each `TranscriptTurn` exposes `DisplayText` (committed text plus any in-progress interim text), `Speaker` (a `TranscriptSpeaker` with `Type`, `Id`, `DisplayName`, `ParticipantId`), `StartedAtUtc`, `WasInterrupted`, and `Revision` — an integer that increments every time the turn's stored data changes. Use `turn.IsCommitted` to check whether a turn is finished instead of comparing `State` directly.

```csharp
using Convai.Domain.Models;
using Convai.Runtime.Components;
using System.Text;
using UnityEngine;

public class SessionReporter : MonoBehaviour
{
    public string BuildSessionReport()
    {
        TranscriptTimeline timeline = ConvaiManager.ActiveManager.Transcripts.CurrentTimeline;
        var sb = new StringBuilder();

        foreach (TranscriptTurn turn in timeline.CommittedTurns)
            sb.AppendLine($"[{turn.StartedAtUtc:HH:mm:ss}] {turn.Speaker.DisplayName}: {turn.DisplayText}");

        return sb.ToString();
    }
}
```

### Look up a single turn

Use `GetTurn(string turnId)` for an O(1) lookup by ID, or `GetLatestTurn(TranscriptParticipantRef)` for the most recent turn from a specific player or character.

```csharp
using Convai.Domain.Models;
using Convai.Runtime.Components;

// Look up a turn by its stable ID
TranscriptTurn turn = ConvaiManager.ActiveManager.Transcripts.GetTurn(turnId);

// Look up the most recent turn from a specific character
var characterRef = new TranscriptParticipantRef(
    TranscriptParticipantKind.Character,
    playerOrCharacterId: characterId,
    displayName: characterName);

TranscriptTurn latest = ConvaiManager.ActiveManager.Transcripts.GetLatestTurn(characterRef);
```

Both methods return `null` when no matching turn exists.

## Filter turns with `TranscriptQuery`

Pass a `TranscriptQuery` to `GetTurns(query)` to retrieve a subset of the timeline. Omitting the query, or leaving a field unset, disables that filter. Results are ordered by `RoomSequence`.

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `ParticipantKind` | `TranscriptParticipantKind?` | `null` (any) | Restrict to `Player` or `Character` turns only |
| `PlayerOrCharacterId` | `string` | `null` (any) | Restrict to a specific player or character by ID |
| `ParticipantId` | `string` | `null` (any) | Restrict by room-scoped participant ID (multi-user rooms) |
| `IncludeActiveTurns` | `bool` | `true` | Include in-progress turns in the results |
| `IncludeCommittedTurns` | `bool` | `true` | Include finalized turns in the results |

`TranscriptQuery.ParticipantKind` uses `TranscriptParticipantKind` (`Player` or `Character`). This is a separate enum from `TranscriptSpeakerType` (`Player`, `Character`, or `System`), which appears on `TranscriptSpeaker` and `TranscriptSubscriptionOptions` further down this page.

```csharp
using Convai.Domain.Models;
using Convai.Runtime.Components;
using System.Collections.Generic;

var query = new TranscriptQuery
{
    ParticipantKind = TranscriptParticipantKind.Character,
    IncludeActiveTurns = false,
    IncludeCommittedTurns = true
};

IReadOnlyList<TranscriptTurn> characterTurns =
    ConvaiManager.ActiveManager.Transcripts.GetTurns(query);
```

## React to live transcript changes

Call `Subscribe(callback, options)` to receive a `TranscriptChange` every time a matching turn changes. `Subscribe` returns an `IDisposable` — dispose it to unsubscribe, typically in `OnDisable`.

`TranscriptChange.Kind` tells you what happened; `TranscriptChange.Turn` is the updated turn, or `null` when `Kind` is `Removed` (read `TurnId` in that case).

| `TranscriptChangeKind` | Meaning |
| --- | --- |
| `Added` | The turn appears in the timeline for the first time |
| `Updated` | The turn's text changed while still active (streaming or stable) |
| `Committed` | The turn finalized normally |
| `Interrupted` | The turn finalized because another speaker cut it off |
| `Corrected` | Previously delivered text for the turn was retroactively corrected |
| `Removed` | The turn was removed from the timeline; `Turn` is `null` |

`TranscriptSubscriptionOptions` controls which turns and change kinds reach your callback:

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `ReplayExisting` | `bool` | `false` | Immediately invoke the callback for every currently matching turn before live updates begin |
| `IncludeActive` | `bool` | `true` | Include changes to turns that are not yet finalized |
| `IncludeTerminal` | `bool` | `true` | Include changes to turns that are committed, interrupted, or corrected |
| `SpeakerType` | `TranscriptSpeakerType?` | `null` (any) | Restrict to `Player`, `Character`, or `System` turns only |
| `SpeakerId` | `string` | `null` (any) | Restrict to a specific player or character by ID |
| `ParticipantId` | `string` | `null` (any) | Restrict by room-scoped participant ID (multi-user rooms) |

`SubscribeCommitted(callback, options)` is a convenience wrapper around `Subscribe` that forces `IncludeActive = false` and `IncludeTerminal = true`, so the callback only fires once a turn is finished — use it when you only care about finalized history, such as a chat log or a scoring system.

```csharp
using Convai.Domain.Models;
using Convai.Runtime.Components;
using Convai.Runtime.Facades;
using System;
using TMPro;
using UnityEngine;

public class WordCountTracker : MonoBehaviour
{
    [SerializeField] private TMP_Text _wordCountLabel;

    private ConvaiTranscripts _transcripts;
    private IDisposable _subscription;
    private int _wordCount;

    private void OnEnable()
    {
        ConvaiManager manager = ConvaiManager.ActiveManager;
        if (manager == null || !manager.TryGetTranscripts(out _transcripts)) return;

        _subscription = _transcripts.SubscribeCommitted(
            OnPlayerTurnCommitted,
            new TranscriptSubscriptionOptions { SpeakerType = TranscriptSpeakerType.Player });
    }

    private void OnDisable()
    {
        _subscription?.Dispose();
        _subscription = null;
    }

    private void OnPlayerTurnCommitted(TranscriptChange change)
    {
        if (change.Turn == null) return;
        if (change.Kind != TranscriptChangeKind.Committed && change.Kind != TranscriptChangeKind.Interrupted) return;

        _wordCount += change.Turn.DisplayText.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length;
        _wordCountLabel.text = $"Words spoken: {_wordCount}";
    }
}
```

For a late-joining viewer that needs to see prior turns immediately, set `ReplayExisting = true` on the options passed to `Subscribe` — matching turns are delivered to your callback once before live updates start.

## Export and clear transcript history

`Export(TranscriptExportFormat format)` serializes every committed turn, ordered by `RoomSequence`, into a single string. It reads from `CurrentTimeline.CommittedTurns` — active turns are never included.

| `TranscriptExportFormat` | Output |
| --- | --- |
| `PlainText` | One line per turn: `"{speaker}: {turn.DisplayText}"` |
| `Markdown` | One line per turn: `"**{speaker}:** {turn.DisplayText}"`, with a blank line between turns |
| `Json` | An indented JSON array of `TranscriptTurn` objects |

The `{speaker}` value is `turn.Speaker.DisplayName`, or `turn.Speaker.Type` when `DisplayName` is empty.

```csharp
using Convai.Domain.Models;
using Convai.Runtime.Components;
using System.IO;
using UnityEngine;

public class SessionExporter : MonoBehaviour
{
    public void ExportSessionToDisk(string filePath)
    {
        string json = ConvaiManager.ActiveManager.Transcripts.Export(TranscriptExportFormat.Json);
        File.WriteAllText(filePath, json);
    }
}
```

Call `Clear()` to remove every turn from the canonical room history:

```csharp
ConvaiManager.ActiveManager.Transcripts.Clear();
```

{% hint style="warning" %}
`Clear()` purges the canonical room history that `CurrentTimeline`, `GetTurns`, and `Export` all read from — it is not the same as clearing a chat panel's visual display, and it cannot be undone.
{% endhint %}

## Troubleshooting

| Symptom | Likely cause | Fix | Verify |
| --- | --- | --- | --- |
| `ConvaiManager.ActiveManager.Transcripts` throws `InvalidOperationException` | Accessed before `ConvaiManager` finishes initializing | Use `ConvaiManager.ActiveManager.TryGetTranscripts(out var transcripts)`, or check `ConvaiManager.IsBootstrapped` first | `TryGetTranscripts` returns `true` and `transcripts` is non-null |
| `Subscribe` callback never fires | Subscribed after the room session already ended, or the `TranscriptSubscriptionOptions` filters exclude every turn | Subscribe before or immediately after the room connects; confirm `SpeakerType`, `SpeakerId`, and `ParticipantId` match an actual participant | The callback fires on the next turn change after subscribing |
| `GetTurns()` returns an empty list with a query set | `PlayerOrCharacterId` or `ParticipantId` does not match any participant, or both `IncludeActiveTurns` and `IncludeCommittedTurns` are `false` | Log `turn.Speaker.Id` and `turn.Speaker.ParticipantId` from an unfiltered `Subscribe` callback to find the correct value | `GetTurns()` with the corrected query returns a non-empty list |
| `change.Turn` is `null` inside a `Subscribe` callback | `change.Kind` is `TranscriptChangeKind.Removed` | Read `change.TurnId` instead of `change.Turn` when `Kind` is `Removed` | The callback no longer throws a null-reference exception on removal |
| `Export(TranscriptExportFormat.PlainText)` returns an empty string | No turns have committed yet | `Export` only reads `CurrentTimeline.CommittedTurns`; wait for turns to finalize, or check `CommittedTurns.Count` first | `CurrentTimeline.CommittedTurns.Count` is greater than zero before exporting |

## Next steps

You now have full read access to the room transcript timeline, live change notifications, and export support. For the complete API surface behind this page, see the Transcript API reference. For displaying this data in your scene, see Transcript UI. For configuring which visual mode is active at runtime, see the Settings Panel.

{% content-ref url="../../scripting-reference/transcript-api.md" %}
[transcript-api.md](../../scripting-reference/transcript-api.md)
{% endcontent-ref %}

{% content-ref url="./" %}
[.](./)
{% endcontent-ref %}

{% content-ref url="../settings-panel/" %}
[settings-panel](../settings-panel/)
{% endcontent-ref %}
