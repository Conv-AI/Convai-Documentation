---
title: Migrate transcript code to SDK 5.0
description: Migrate custom transcript views and Inspector listeners to history entries, batched updates, live captions, and explicit subscription cleanup.
last_reviewed: "5.0.0-preview"
---

Update custom transcript UI and Inspector listeners when moving to the current SDK. History now exposes immutable entries and change batches; captions remain a separate view of speech.

## Replace the old calls

| Previous surface | Current surface |
| --- | --- |
| `TranscriptTurn`, timeline turns | `TranscriptEntry`, `CurrentTimeline.Entries` |
| `GetTurns`, `GetTurn` | `GetEntries`, `TryGetEntry` |
| `SubscribeCommitted` | `SubscribeFinalized` |
| `Subscribe` with per-change callback | `Subscribe(Action<TranscriptChangeBatch>)` |
| `Clear` | `ClearHistory` |
| Export format argument | `Export(new TranscriptExportOptions { Format = ... })` |
| `ReplayExisting` / `ReplayLatest` | `Replay` |
| Active/terminal history filters | `IncludeOpen` and query `IncludeFinal` |
| Caption `Streaming` / `Stable` | `Active`; handle new `Cleared` |
| `ConvaiCharacter.OnTranscriptReceived` | `OnSpokenLine` for spoken sentences; facade for history |
| Facade raw transcript event properties | `Subscribe`, `SubscribeFinalized`, or `SubscribeCaptions` |

## Update row handling

Use `TranscriptEntry.Id` as the key. For Added, Updated, Finalized, and Corrected, replace the row with the complete `Entry.Text`. Remove `EntryId` for Removed and clear all rows for Reset. Do not append incoming text as a token delta or depend on object identity changing.

`Subscribe` replays history by default. `SubscribeFinalized` does not, and excludes later corrections. Choose based on whether the consumer renders current state or reacts once to new finalization.

## Rewire Inspector listeners

`ConvaiCharacterEventRelay.OnSpokenLine` uses `CharacterSpokenLineRelayData`. The old serialized field name can migrate, but listeners expecting the removed payload need rewiring.

`ConvaiTranscriptEventRelay` now emits entry updated/finalized/corrected/removed callbacks plus reset. Set Speaker Filter and Character Id Filter. Remove code that depends on FinalOnly, IgnoreInterimUpdates, or removed player/character transcript payloads.

## Apply lifecycle and presentation rules

Subscribe, dispose subscriptions, and clear history on Unity's main thread. The facade belongs to the manager; do not dispose it. Custom views must honor `IsPresentationEnabled` and `PresentationEnabledChanged`, because the relay and data subscriptions continue while presentation is off.

Handle caption Cleared immediately. For other final captions, choose a hold duration in the view. For paged history, use `NextBeforeOrder` and respect retention boundaries.

## Verify the migration

Test replay after enabling the view, a partial entry update, finalization, a correction, clearing, and removal due to retention. Confirm that rows update by ID, text is not duplicated, and disabling the view releases its subscriptions.

See [Transcript API](transcript-api.md) for current types and [Transcript history and queries](../ui-and-presentation/transcript-ui/transcript-history-and-queries.md) for paging.
