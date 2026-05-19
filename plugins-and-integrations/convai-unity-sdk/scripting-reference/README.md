# Scripting Reference

The Convai Unity SDK exposes its full functionality through two complementary wiring approaches. **Inspector relay components** (`ConvaiSessionEventRelay`, `ConvaiCharacterEventRelay`, `ConvaiTranscriptEventRelay`) let you wire events directly in the Unity Inspector without writing code. **C# subscriptions** via the `ConvaiEvents` typed event hub and component APIs give you full programmatic control from script.

Both approaches work simultaneously — use Inspector relays for quick prototype wiring and C# subscriptions for logic that needs branching, coroutines, or runtime dynamism.

The `ConvaiSDK` static class exposes one property that is useful regardless of which approach you use:

```csharp
// Runtime version check
Debug.Log($"Convai SDK version: {ConvaiSDK.Version}");
```

***

## Pages In This Section

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Session Events</strong><br>Connection state, errors, usage limits, and participant changes — Inspector relay and C# subscription.</td><td><a href="/broken/pages/1b01792b79aac77224746d4978c273cc313e4be6">Broken link</a></td></tr><tr><td><strong>Character Events</strong><br>Character speech, transcript, emotion, and player transcript events — both wiring approaches.</td><td><a href="/broken/pages/0885a87d4c65cd590cd00c0dc9b29e07caec08eb">Broken link</a></td></tr><tr><td><strong>Transcript API</strong><br>Pull-based transcript history and snapshot access via the <code>ConvaiTranscripts</code> facade.</td><td><a href="/broken/pages/54ac28f655897d0d4d976ece967d7de5bd22f354">Broken link</a></td></tr><tr><td><strong>Character &#x26; Player API</strong><br>Full scripting API for <code>ConvaiCharacter</code> and <code>ConvaiPlayer</code> — methods, events, and properties.</td><td><a href="/broken/pages/97d732f5b53a3459bf84007d80080e9fff1133eb">Broken link</a></td></tr><tr><td><strong>ConvaiManager API</strong><br>SDK entry point — connection, conversation control, ownership, and service accessors.</td><td><a href="/broken/pages/d082c97e6b4098eb0e296e4081e67a269a54e95f">Broken link</a></td></tr><tr><td><strong>Audio API</strong><br>Microphone control, per-character muting, and WebGL audio unlock via <code>ConvaiAudio</code>.</td><td><a href="/broken/pages/e9b5d9cc91874a287c298ab78a6e343eb8121b72">Broken link</a></td></tr><tr><td><strong>Operation &#x26; Stream Types</strong><br>Complete reference for <code>IConvaiOperation&#x3C;T></code>, <code>IConvaiStream&#x3C;T></code>, <code>ConvaiError</code>, and related types.</td><td><a href="/broken/pages/c85e4c39417c86d16620034c1e6853fa363955a3">Broken link</a></td></tr><tr><td><strong>Async Patterns</strong><br>How to consume SDK operations — async/await, coroutines, chaining, progress, cancellation, and streams.</td><td><a href="/broken/pages/c2a4043a68a4907f1f014dd56e2828505536b856">Broken link</a></td></tr></tbody></table>
