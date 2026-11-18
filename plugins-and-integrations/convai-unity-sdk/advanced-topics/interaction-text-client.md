---
title: Migrate from the standalone text client
description: Move typed Unity conversations from the retired standalone text client to a scene room with readiness checks, transcript updates, and captions.
last_reviewed: "5.0.0-pre.1"
---

Use the scene room to exchange typed messages with a Convai character. The room handles readiness, player identity, and transcript history.

{% hint style="warning" %}
SDK 5.0 removes the standalone `ConvaiInteractionClient` and its response stream. Migrate Unity chat integrations to `ConvaiPlayer` and `ConvaiManager.Transcripts`.
{% endhint %}

## Move the conversation into a scene room

Set up a `ConvaiManager`, a `ConvaiPlayer`, and at least one `ConvaiCharacter`. Connect with `ConvaiManager.ConnectAsync`. For typed input with the microphone kept closed, follow [Run a text-only session](../getting-started/run-a-text-only-session.md). Group voice rooms require voice input.

## Send text and render the answer

Read `manager.ConversationAvailability` and observe `manager.Events.OnConversationAvailabilityChanged` to update input state. Call `manager.Player.TrySendTextMessage(message, out reason)` and show `reason` when the room refuses the input.

Replace response stream parsing with `manager.Transcripts.Subscribe`. Check typed entries for `DeliveryUnknown` or a `send_failed` abort when the UI should report delivery. For each change, use `Entry.Id` as the row key and assign the complete `Entry.Text`. `SubscribeFinalized` lets gameplay react when the transcript finishes assembling. Use `SubscribeCaptions` for temporary captions timed to speech.

Dispose subscriptions when the view is disabled. For a custom UI and replay example, see [Transcript history and queries](../ui-and-presentation/transcript-ui/transcript-history-and-queries.md).

## Verify the migration

Send a message in a ready room. Confirm that the chat shows one player entry and updates a reply entry in place. Disconnect with `ConvaiManager.DisconnectAsync`, then check that further sends are refused.
