---
title: Scripting reference
description: Find Unity SDK scripting references for scene managers, characters, audio, push-to-talk, transcript history, events, and REST clients.
last_reviewed: "5.0.0-preview"
---

Use these references when connecting scene scripts to the SDK. Public scene components live in `Convai.Runtime.Components`; the event, audio, and transcript facades live in `Convai.Runtime.Facades`.

<table data-view="cards"><thead><tr><th></th><th></th></tr></thead><tbody>
<tr><td><a href="convaimanager-api.md">ConvaiManager API</a></td><td>Connect, find services, select characters, and manage runtime ownership.</td></tr>
<tr><td><a href="convairoommanager-api.md">ConvaiRoomManager API</a></td><td>Room policies, microphone permissions, diagnostics, and commands.</td></tr>
<tr><td><a href="character-and-player-api.md">Character and player API</a></td><td>Readiness, identity, text input, and per-character behavior.</td></tr>
<tr><td><a href="audio-api.md">Audio API</a></td><td>Microphone capture, mute, remote tracks, and browser playback unlock.</td></tr>
<tr><td><a href="push-to-talk-api.md">Push-to-talk scripting reference</a></td><td>Press/release input, state changes, commit results, and recovery.</td></tr>
<tr><td><a href="transcript-api.md">Transcript API</a></td><td>History entries, live captions, subscriptions, and export.</td></tr>
<tr><td><a href="migrate-transcripts-to-5-0.md">Migrate transcript code to SDK 5.0</a></td><td>Replace removed turn APIs and relay payloads.</td></tr>
<tr><td><a href="character-events.md">Character events</a></td><td>Speech, emotion, tool calls, and playback completion.</td></tr>
<tr><td><a href="session-events.md">Session events</a></td><td>Connection state, errors, idle warnings, and session endings.</td></tr>
<tr><td><a href="server-command-results.md">Server command results</a></td><td>Distinguish a sent command from an accepted command.</td></tr>
<tr><td><a href="async-patterns.md">Async patterns</a></td><td>Await operations, use coroutines, and pass cancellation tokens.</td></tr>
<tr><td><a href="operation-and-stream-types.md">Operation and stream types</a></td><td>Shared result types and producer contracts.</td></tr>
<tr><td><a href="rest-api-client.md">REST API client reference</a></td><td>Client services, routing options, and transport ownership.</td></tr>
</tbody></table>

## Related pages

- [Event system](../core-concepts/event-system.md)
- [Runtime architecture](../core-concepts/runtime-architecture.md)
