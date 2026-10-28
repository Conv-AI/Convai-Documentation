---
title: Transcript history and queries
last_reviewed: "5.0.0-preview"
description: Read and page through retained conversation entries, handle live changes and finalization, and export or clear local transcript history.
---

`ConvaiManager.Transcripts` provides entry queries, change subscriptions, and export for retained local conversation history. The facade is `ConvaiTranscripts` in `Convai.Runtime.Facades`; its data models are in `Convai.Domain.Models`. For migration from turn-based APIs, see [Transcript migration](../../scripting-reference/migrate-transcripts-to-5-0.md).

## Read the current transcript state

`CurrentTimeline` returns an immutable snapshot with `Version` and `Entries`. Entries are ordered by ascending `Order`. Use `TryGetEntry(string entryId, out TranscriptEntry entry)` for ID lookup.

Resolve an initialized manager through `TryGetTranscripts` before using the facade. `ActiveManager` can be null, and the `Transcripts` property throws if services are not ready.

| Entry member | Meaning |
| --- | --- |
| `Id` | Stable opaque ID; use as your UI row key |
| `Revision` | Increases when the entry changes |
| `Order` | Stable room-wide sequence position |
| `Speaker` | Speaker type, IDs, display name, and participant attribution |
| `Text` | Complete current text; replace a row's text instead of appending it |
| `IsFinal` | Normal text assembly has closed; corrections can still arrive |
| `Outcome` | `Open`, `Completed`, `Interrupted`, `Aborted`, or `Incomplete` |
| `CreatedAtUtc` / `UpdatedAtUtc` | Observation and last-change timestamps |
| `Correlation` | Known turn, response, submission, and group-line IDs with attribution quality |
| `SpokenText` / `SpokenExtent` | Spoken portion of a character reply, distinct from generated text |
| `Flags` | Truncation, unknown typed-message delivery, or incomplete capture |

Snapshots may reuse unchanged entry instances. Use `Revision`, `Version`, and change kinds to detect updates, rather than relying on reference identity. `IsFinal` does not mean the character's audio has finished.

## Filter and page through entries

`GetEntries(query)` returns a `TranscriptPage`. Without `BeforeOrder`, it selects the newest matching page, but `page.Entries` is in ascending `Order`, not newest-first display order.

| Query field | Default | Purpose |
| --- | --- | --- |
| `SpeakerType` | `null` | Optional `TranscriptSpeakerType` filter |
| `SpeakerId` | `null` | Player/character ID, or a player's server speaker ID |
| `ParticipantId` | `null` | Room participant filter |
| `IncludeOpen` / `IncludeFinal` | `true` | Include unfinished/final entries |
| `BeforeOrder` | `null` | Read entries whose order is smaller than this value |
| `Limit` | `50` | Page size, clamped to `1..200` |

`TranscriptPage` also exposes `Version`, `HasMore`, `NextBeforeOrder`, and `ReachedRetentionStart`. Pass `NextBeforeOrder` into the next query only while `HasMore` is true. Reaching retention start means reaching the oldest retained match, not necessarily the beginning of the original conversation.

This component exports the latest page of final character entries as a report:

```csharp
using System.Text;
using Convai.Domain.Models;
using Convai.Runtime.Components;
using UnityEngine;

public class SessionReporter : MonoBehaviour
{
    public string BuildReport()
    {
        var manager = ConvaiManager.ActiveManager;
        if (manager == null || !manager.TryGetTranscripts(out var transcripts)) return string.Empty;
        var page = transcripts.GetEntries(new TranscriptQuery
        {
            SpeakerType = TranscriptSpeakerType.Character,
            IncludeOpen = false,
            Limit = 50
        });
        var report = new StringBuilder();
        foreach (var entry in page.Entries)
            report.AppendLine($"[{entry.CreatedAtUtc:HH:mm:ss}] {entry.Speaker.DisplayName}: {entry.Text}");
        return report.ToString();
    }
}
```

## React to live transcript changes

`Subscribe(Action<TranscriptChangeBatch>, options)` sends one batch per history change. Its default replay sends existing matches as `Added` changes with `Origin = Replay`. A batch's `Timeline` is the whole snapshot, even when its `Changes` are filtered.

| Change kind | UI behavior |
| --- | --- |
| `Added` / `Updated` | Insert or replace the row identified by `Entry.Id` |
| `Finalized` | Mark the row final; inspect `Outcome` separately |
| `Corrected` | Replace a final row's text |
| `Removed` | Remove the row using `EntryId` |
| `Reset` | Clear all rows; it reaches every subscriber regardless of filters |

`TranscriptSubscriptionOptions` has `SpeakerType`, `SpeakerId`, `ParticipantId`, `IncludeOpen` (default `true`), and nullable `Replay`. `SubscribeFinalized(Action<TranscriptChange>, options)` defaults replay to off and reports each entry once at finalization. It does not send subsequent corrections or outcome updates. Set `Replay = true` explicitly if finished history should run through that callback.

Call subscriptions, subscription disposal, and `ClearHistory()` on Unity's main thread. Calling them from a worker thread throws `InvalidOperationException` in the runtime facade. Read-only queries work from any thread. Subscriber exceptions are logged without preventing delivery to other subscribers.

A custom history label can subscribe with this component. It waits for initialization and displays the number of retained entries without logging transcript text:

```csharp
using System;
using Convai.Domain.Models;
using Convai.Runtime.Components;
using Convai.Runtime.Facades;
using TMPro;
using UnityEngine;

public class TranscriptCountLabel : MonoBehaviour
{
    [SerializeField] private TMP_Text label;
    private IDisposable subscription;

    private void Update()
    {
        if (subscription != null) return;
        var manager = ConvaiManager.ActiveManager;
        if (manager == null || !manager.TryGetTranscripts(out ConvaiTranscripts transcripts)) return;
        subscription = transcripts.Subscribe(OnChanged);
        ShowCount(transcripts.CurrentTimeline);
    }

    private void OnChanged(TranscriptChangeBatch batch) => ShowCount(batch.Timeline);

    private void ShowCount(TranscriptTimeline timeline)
    {
        if (label != null) label.text = $"Retained entries: {timeline.Entries.Count}";
    }

    private void OnDisable()
    {
        subscription?.Dispose();
        subscription = null;
    }
}
```

This example assumes one manager while the component is enabled. Rebind if your application replaces that manager. For a transcript-rendering component, also observe `IsPresentationEnabled` and `PresentationEnabledChanged`.

## Caption subscriptions

`SubscribeCaptions` takes `Action<TranscriptCaption>` and `TranscriptCaptionSubscriptionOptions`. Its `Replay`, `IncludeOpen`, and `IncludeFinal` defaults are all `true`. The same speaker and participant filters are available.

Caption states are `Active`, `Completed`, `Interrupted`, and `Cleared`. Remove a `Cleared` caption immediately; it is not a completed or interrupted line. Use [Chat and subtitle modes](chat-and-subtitle-modes.md) for the sample's cue expiry behavior.

## Export and clear transcript history

`Export(new TranscriptExportOptions { Format = TranscriptExportFormat.Json })` returns a string. `PlainText`, `Markdown`, and `Json` are supported. Export includes final entries by default; set `IncludeOpen = true` to include unfinished entries. `SpeakerType` and `SpeakerId` optionally filter the export.

JSON export is an object with `schemaVersion` and `entries`, not a bare array. Persist the returned string through your application's storage flow if it must outlive local history. Export only includes data still retained at the time of the call.

`ClearHistory()` removes local retained history and sends a `Reset` batch. It is different from `ChatTranscriptUI.ClearAll()`, which only clears rendered bubbles. Neither operation is a request to delete long-term memory in Convai.

## Retention and health

The engine defaults to 500 closed entries and 1,000,000 retained text units. Individual text is capped at 32,768 UTF-16 units. The 64-open-turn threshold triggers recovery of the oldest eligible unfinished turn; a character reply still in progress is excluded from that recovery selection, so this is not an unconditional hard cap on open entries.

`Health` contains `RetainedEntryCount`, `RetainedTextLength`, `OpenEntryCount`, `TruncatedEntryCount`, and `EvictedEntryCount`. These counts contain no transcript text. Monitor them if your UI needs to explain an incomplete scrollback or export.

## Troubleshooting

| Symptom | Cause | Fix and verification |
| --- | --- | --- |
| No facade at scene startup | Manager initialization has not completed | Retry `TryGetTranscripts`; verify it returns true |
| A filtered query is empty | IDs or inclusion flags exclude entries | Compare with an unfiltered query and inspect speaker IDs in your own UI |
| Earlier messages are absent | The page limit or retention boundary was reached | Follow `NextBeforeOrder` while `HasMore`; inspect `Health.EvictedEntryCount` |
| Text repeats in a custom bubble | The callback text was appended as a delta | Replace the text by entry ID and verify a streaming update |
| Export is empty during a reply | Default export includes only final entries | Wait for finalization or set `IncludeOpen = true` |
| Subscription throws off the main thread | Subscription delivery belongs to Unity's thread | Subscribe and dispose from a Unity lifecycle method |

## Next steps

{% content-ref url="../../scripting-reference/transcript-api.md" %}
[Transcript API](../../scripting-reference/transcript-api.md)
{% endcontent-ref %}
