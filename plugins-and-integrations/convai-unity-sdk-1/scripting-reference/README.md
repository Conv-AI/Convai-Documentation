---
description: >-
  C# scripting reference for the Convai Unity SDK — session events, character
  events, transcripts, audio control, async operations, and supported
  consumption patterns.
---

# Scripting Reference

## Convai SDK Scripting Reference

The Convai Unity SDK exposes two complementary approaches for integrating functionality from C#. `ConvaiSessionEventRelay`, `ConvaiCharacterEventRelay`, and `ConvaiTranscriptEventRelay` are MonoBehaviours that wire events directly in the Inspector — no code required. For scripted reactions and programmatic control, the `ConvaiEvents` typed event hub and each component's C# API give you full access from any script.

Both approaches observe the same underlying SDK events and can be combined freely.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Session Events</strong><br>Connection state, errors, idle warnings, and participant changes via relay component or typed C# hub.</td><td><a href="/broken/pages/6693225e7706eebee9867d22a339a171cc2cb941">Broken link</a></td></tr><tr><td><strong>Character Events</strong><br>Speech, emotion, transcript, turn lifecycle, and action events via relay component or typed C# hub.</td><td><a href="/broken/pages/fc07c80b0235dd0fd0ac50cfcae4e2da2d0625e9">Broken link</a></td></tr><tr><td><strong>Transcript API</strong><br>Pull-based facade for querying and subscribing to the live in-memory transcript timeline.</td><td><a href="/broken/pages/45c153c71b4ebf451c79cd8df9097040c6b6c0ae">Broken link</a></td></tr><tr><td><strong>Character &#x26; Player API</strong><br>Full method, property, and event reference for <code>ConvaiCharacter</code> and <code>ConvaiPlayer</code>.</td><td><a href="/broken/pages/a8097439acc902b54dbd69e05d17f34ada7f5d47">Broken link</a></td></tr><tr><td><strong>ConvaiManager API</strong><br>SDK entry point — connection control, facade accessors, conversation ownership, and service discovery.</td><td><a href="/broken/pages/5c82d99b3d29c0ac22b83ce0d785795a51a65ce0">Broken link</a></td></tr><tr><td><strong>Audio API</strong><br>Microphone muting, per-character audio control, audio playback unlock, and listening state.</td><td><a href="/broken/pages/db6bacc342ed5a7c72ae5e5ebcfd966982bb0ceb">Broken link</a></td></tr><tr><td><strong>Operation &#x26; Stream Types</strong><br>Type reference for <code>IConvaiOperation&#x3C;T></code>, <code>IConvaiStream&#x3C;T></code>, <code>ConvaiError</code>, <code>Unit</code>, and status enums.</td><td><a href="/broken/pages/4d7cb1a3f9e7ebc60cb992eefa79319ca84c08f5">Broken link</a></td></tr><tr><td><strong>Async Patterns</strong><br>Six patterns for consuming SDK async types: async/await, coroutines, chaining, progress, cancellation, and streams.</td><td><a href="/broken/pages/6ebf9d21669c690909a7387265f77966e5398fa9">Broken link</a></td></tr></tbody></table>

## Next Steps

Start with [Session Events](/broken/pages/6693225e7706eebee9867d22a339a171cc2cb941) and [Character Events](/broken/pages/fc07c80b0235dd0fd0ac50cfcae4e2da2d0625e9) to wire SDK events to your scene logic, then explore the [ConvaiManager API](/broken/pages/5c82d99b3d29c0ac22b83ce0d785795a51a65ce0) for connection control and the [Async Patterns](/broken/pages/6ebf9d21669c690909a7387265f77966e5398fa9) page for consumption guidance.
