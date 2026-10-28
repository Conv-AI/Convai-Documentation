---
title: Transcript API
description: Reference transcript entries, paged history, change batches, live captions, presentation state, export formats, and retained-history limits.
last_reviewed: "5.0.0-preview"
---

`ConvaiTranscripts` in `Convai.Runtime.Facades` provides room history and live captions. Access it through `ConvaiManager.Transcripts` after initialization, or `TryGetTranscripts`. The manager owns the facade: dispose your subscriptions, not the facade.

## Read and subscribe

| Member | Contract |
| --- | --- |
| `CurrentTimeline` | Immutable history with `Version` and `Entries` in ascending `Order` |
| `CurrentCaptions` | Latest caption per speaker |
| `Health` | Retained entry/text counts, open/truncated entries, and eviction count |
| `IsPresentationEnabled`, `PresentationEnabledChanged` | Presentation state; data ingestion continues independently |
| `GetEntries(TranscriptQuery)` | Newest matching page, with entries returned in ascending order |
| `TryGetEntry(id, out entry)` | Look up a retained entry |
| `Subscribe(Action<TranscriptChangeBatch>, options)` | History changes; replay defaults on |
| `SubscribeFinalized(Action<TranscriptChange>, options)` | Once when each entry becomes final; replay defaults off |
| `SubscribeCaptions(Action<TranscriptCaption>, options)` | Live caption updates; replay defaults on |
| `ClearHistory()` | Clear retained history and publish a Reset |
| `Export(TranscriptExportOptions)` | Export matching entries in order; final entries only by default |

Subscribe, dispose subscriptions, and clear history on Unity's main thread. Reads work from any thread. Subscriber exceptions are isolated and logged so other subscribers still receive the update. Changes initiated inside a callback are queued after the current batch.

## Transcript entries

`TranscriptEntry` is in `Convai.Domain.Models`.

| Property | Meaning |
| --- | --- |
| `Id`, `Revision`, `Order` | Stable row key, change revision, and room-wide sort order |
| `Speaker`, `Source` | Speaker identity and text source |
| `Text` | Complete current text; assign it instead of appending it as a delta |
| `IsFinal`, `Outcome`, `Completion` | Whether assembly closed, how it ended, and what closed it |
| `AbortReason` | Supplied reason for an aborted entry |
| `SpokenText`, `SpokenExtent` | What the voice reported as spoken; distinct from full reply text |
| `Correlation`, `Segments`, `Flags` | Correlation IDs, assembly parts, and content qualifiers |
| `CreatedAtUtc`, `UpdatedAtUtc` | Observation timestamps |

Finality does not prove audio or the logical turn finished; a final entry can still be corrected. Unchanged entries may retain object identity across timeline versions. Use `Revision` or change kinds to detect an update.

`TranscriptSpeakerType` is `Unknown`, `Player`, `Character`, or `System`. Speaker filters can match player/character ID or server speaker ID; use `ParticipantId` to narrow a shared-room participant.

## Change batches

`TranscriptChangeBatch` contains `Timeline`, `Changes`, and `Version`. The timeline is the whole history, even for a filtered subscription. Each change has `Kind`, `Entry`, `EntryId`, `Version`, `Origin`, and optional reset/previous-entry data.

| Kind | Renderer action |
| --- | --- |
| `Added`, `Updated`, `Finalized`, `Corrected` | Upsert by `Entry.Id` and replace displayed text |
| `Removed` | Remove `EntryId`; `Entry` is null and `PreviousEntry` identifies the removed speaker |
| `Reset` | Clear every row; `Entry` and `EntryId` are null |

`Origin` is `Live` or `Replay`. `SubscribeFinalized` excludes later corrections and outcome updates; use `Subscribe` when those matter.

`TranscriptSubscriptionOptions` has nullable value options `Replay` and `SpeakerType`, optional string filters `SpeakerId` and `ParticipantId`, and a non-nullable `IncludeOpen` bool that defaults to true. A null `Replay` uses the method default. Reset reaches all subscribers regardless of filters.

## Paging

`TranscriptQuery` includes speaker filters, `IncludeOpen = true`, `IncludeFinal = true`, optional `BeforeOrder`, and `Limit = 50` (clamped to 1–200). A page contains `Entries`, `Version`, `HasMore`, `NextBeforeOrder`, and `ReachedRetentionStart`. Pass `NextBeforeOrder` to retrieve the next older page. `ReachedRetentionStart` means the oldest retained match, not the beginning of all past conversations.

## Captions

`SubscribeCaptions` delivers `TranscriptCaption` for player speech and character sentences as they are spoken. Caption states are `Active`, `Completed`, `Interrupted`, and `Cleared`. Remove a Cleared caption immediately. The view chooses how long to hold completed captions.

`TranscriptCaptionSubscriptionOptions` has `Replay`, `IncludeOpen`, and `IncludeFinal` defaulting to true, plus speaker and participant filters. Timing metadata distinguishes speech-activity timing from more precise voice timing when available. Captions are not an archive of the whole conversation.

## Retention and export

The engine bounds history to 500 final entries, 1,000,000 characters, 32,768 characters per entry, and at most 64 open entries. Eviction publishes Removed changes; inspect `Health` to see truncation and eviction. Export before data leaves retention if your application requires an archive.

`TranscriptExportOptions` supports `PlainText`, `Markdown`, or `Json`, speaker filters, and `IncludeOpen` (false by default). JSON includes `schemaVersion` and `entries`. Export only when your application needs the transcript, and store it according to your application's data policy.

## Related pages

- [Migrate transcript code to SDK 5.0](migrate-transcripts-to-5-0.md)
- [Transcript history and queries](../ui-and-presentation/transcript-ui/transcript-history-and-queries.md)
- [Customize UI components](../ui-and-presentation/customizing-ui-components.md)
