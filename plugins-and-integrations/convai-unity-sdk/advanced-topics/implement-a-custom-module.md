---
title: Implement a custom module
description: Implement `IConvaiModule` to add custom runtime behavior that starts with the SDK, accesses runtime services, and reacts to domain events.
last_reviewed: "4.6.0"
---

Build a custom module that integrates with the Convai runtime lifecycle, accesses SDK services, and subscribes to domain events. Before starting, read [Runtime module system](extending-the-sdk.md) to understand when a module is the right tool and how the lifecycle states map to your implementation.

## Prerequisites

* A working Convai scene with a `ConvaiManager` component
* C# proficiency, including async/await and Unity's `MonoBehaviour` lifecycle
* Familiarity with the [Runtime module system](extending-the-sdk.md)

## Quickstart: minimal module

Before reading the full interface contract, here is the shortest path to a working module — a `MonoBehaviour` that registers itself and subscribes to one SDK event:

```csharp
// MinimalModule.cs
using System;
using System.Collections.Generic;
using System.Threading;
using Convai.Domain.DomainEvents.Runtime;
using Convai.Domain.EventSystem;
using Convai.Runtime.Components;
using Convai.Runtime.Core;
using Convai.Runtime.Core.Modules;
using UnityEngine;

public class MinimalModule : MonoBehaviour, IConvaiModule
{
    public string ModuleId    => "my-project.minimal";
    public string DisplayName => "Minimal Module";

    public IReadOnlyList<string> RequiredModules  => Array.Empty<string>();
    public IReadOnlyList<Type>   RequiredServices => Array.Empty<Type>();
    public IReadOnlyList<Type>   ProvidedServices => Array.Empty<Type>();
    public bool IsActive { get; private set; }

    private IEventHub _events;
    private SubscriptionToken _subscription;

    private void Awake() => ConvaiManager.ActiveManager?.RegisterModule(this);
    private void OnDestroy() => ConvaiManager.ActiveManager?.UnregisterModule(this);

    public System.Threading.Tasks.ValueTask RegisterAsync(IModuleContext ctx, CancellationToken ct = default)
        => default;

    public System.Threading.Tasks.ValueTask StartAsync(IModuleContext ctx, CancellationToken ct = default)
    {
        _events = ctx.Events;
        _subscription = _events.Subscribe<CharacterSpeechStateChanged>(e =>
        {
            if (e.IsSpeaking) Debug.Log($"[MinimalModule] Character {e.CharacterId} started speaking.");
        });
        IsActive = true;
        return default;
    }

    public System.Threading.Tasks.ValueTask PauseAsync(RuntimePauseReason r, CancellationToken ct = default)
    { IsActive = false; return default; }

    public System.Threading.Tasks.ValueTask ResumeAsync(CancellationToken ct = default)
    { IsActive = true; return default; }

    public System.Threading.Tasks.ValueTask StopAsync(CancellationToken ct = default)
    {
        _events?.Unsubscribe(_subscription);
        _events = null;
        IsActive = false;
        return default;
    }
}
```

Add this component to any GameObject in the scene. The full interface contract and advanced patterns follow below.

## IConvaiModule interface

```csharp
// API excerpt: imports and the surrounding namespace are omitted.
public interface IConvaiModule
{
    string ModuleId    { get; }
    string DisplayName { get; }
    IReadOnlyList<string> RequiredModules  { get; }
    IReadOnlyList<Type>   RequiredServices { get; }
    IReadOnlyList<Type>   ProvidedServices { get; }
    bool IsActive { get; }

    ValueTask RegisterAsync(IModuleContext context, CancellationToken ct = default);
    ValueTask StartAsync(IModuleContext context, CancellationToken ct = default);
    ValueTask PauseAsync(RuntimePauseReason reason, CancellationToken ct = default);
    ValueTask ResumeAsync(CancellationToken ct = default);
    ValueTask StopAsync(CancellationToken ct = default);
}
```

### Lifecycle method reference

| Method | When called | What to do |
| --------------- | -------------------------------------------------- | -------------------------------------------------------------------------------- |
| `RegisterAsync` | During runtime build — before any `StartAsync` | Register services via `context.ProvideModuleService<T>()`. Subscribe to events. |
| `StartAsync` | Runtime start — after all modules are registered | Start active behaviors: begin processing, initialize hardware, start coroutines. |
| `PauseAsync` | Runtime paused (app loses focus, deliberate pause) | Stop processing. Use `RuntimePauseReason` to distinguish why. |
| `ResumeAsync` | Runtime resumed | Restart processing paused in `PauseAsync`. |
| `StopAsync` | Runtime stopping or module removed | Clean up: unsubscribe, stop coroutines, release resources. |

## IModuleContext services

| Property | Type | Availability | Description |
| ------------- | ------------------------- | ------------ | -------------------------------------------- |
| `Runtime` | `ConvaiRuntime` | Always | The runtime instance this module belongs to. |
| `Events` | `IEventHub` | Always | Publish and subscribe to domain events. |
| `Agents` | `IAgentRegistry` | Always | Query registered characters and players. |
| `Transport` | `ITransportProvider` | May be null | Platform-specific communication layer. |
| `Preferences` | `IRuntimePreferences` | May be null | Mutable runtime preferences. |
| `Logger` | `ILogger` | May be null | Logger for diagnostics. |
| `RoomAudio` | `IConvaiRoomAudioService` | May be null | Shared microphone plus per-character and participant playback controls. |
| `Credentials` | `ICredentialProvider` | May be null | API key and project-level Core Server URL resolution. |

{% hint style="warning" %}
Always null-check `Transport`, `Preferences`, `Logger`, `RoomAudio`, and `Credentials` before use. `Events` and `Agents` are guaranteed to be non-null. Accessing a null service throws a `NullReferenceException` that halts the module's lifecycle.
{% endhint %}

For the full list of subscribable domain events, see [Event System](../core-concepts/event-system.md).

### Access the shared room service

**Unity SDK <code class="expression">space.vars.unity_sdk_preview_version</code> preview:** The multi-character session, target, and roster members below are staged ahead of the current <code class="expression">space.vars.unity_sdk_version</code> Asset Store release. Resolving optional module services remains supported in the current release.

`IConvaiRoomConnectionService` is pre-populated as an optional module service rather than exposed as a typed `IModuleContext` property. Resolve it with `TryGetModuleService` before reading the multi-character roster or issuing target and roster commands:

```csharp
using Convai.Runtime.Room;

if (context.TryGetModuleService(out IConvaiRoomConnectionService room))
{
    MultiCharacterRoomSession session = room.CurrentMultiCharacterSession;
    if (session != null)
        context.Logger?.Debug(
            $"Room {session.RoomSessionId} has {session.Characters.Count} character memberships.",
            LogCategory.SDK);
}
```

The connection service owns one room lifecycle. Its `SetInteractionTargetAsync`, `ClearInteractionTargetAsync`, `AddCharacterAsync`, and `RemoveCharacterAsync` operations complete after the server acknowledges the corresponding route or roster epoch. Do not model these as independent per-character connections. `IConvaiRoomAudioService` remains the appropriate surface for character mute, remote-audio subscription, participant output binding, and microphone control.

## Implement a module

### Event subscriber example

A module that subscribes to a domain event and triggers haptic feedback when a character speaks.

```csharp
// HapticFeedbackModule.cs
using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Convai.Domain.DomainEvents.Runtime;
using Convai.Domain.EventSystem;
using Convai.Domain.Logging;
using Convai.Runtime.Core;
using Convai.Runtime.Core.Modules;

// Application-owned output. Implement this with the haptics API for your target device.
public interface IHapticOutput
{
    void PulseSoft();
}

public class HapticFeedbackModule : IConvaiModule
{
    public string ModuleId    => "my-company.haptic-feedback";
    public string DisplayName => "Haptic Feedback";

    public IReadOnlyList<string> RequiredModules  => Array.Empty<string>();
    public IReadOnlyList<Type>   RequiredServices => Array.Empty<Type>();
    public IReadOnlyList<Type>   ProvidedServices => Array.Empty<Type>();

    public bool IsActive { get; private set; }

    private readonly IHapticOutput _hapticOutput;
    private ILogger _logger;
    private IEventHub _events;
    private SubscriptionToken _subscription;

    public HapticFeedbackModule(IHapticOutput hapticOutput = null)
    {
        _hapticOutput = hapticOutput;
    }

    public ValueTask RegisterAsync(IModuleContext context, CancellationToken ct = default)
    {
        _logger = context.Logger;
        return default;
    }

    public ValueTask StartAsync(IModuleContext context, CancellationToken ct = default)
    {
        _events = context.Events;
        _subscription = _events.Subscribe<CharacterSpeechStateChanged>(OnSpeechStateChanged);
        IsActive = true;
        _logger?.Debug("[HapticFeedbackModule] Started.", LogCategory.SDK);
        return default;
    }

    public ValueTask PauseAsync(RuntimePauseReason reason, CancellationToken ct = default)
    {
        IsActive = false;
        return default;
    }

    public ValueTask ResumeAsync(CancellationToken ct = default)
    {
        IsActive = true;
        return default;
    }

    public ValueTask StopAsync(CancellationToken ct = default)
    {
        _events?.Unsubscribe(_subscription);
        _events = null;
        IsActive = false;
        _logger?.Debug("[HapticFeedbackModule] Stopped.", LogCategory.SDK);
        return default;
    }

    private void OnSpeechStateChanged(CharacterSpeechStateChanged e)
    {
        if (!IsActive || !e.IsSpeaking) return;
        _hapticOutput?.PulseSoft();
    }
}
```

### Service provider and consumer example

A module declares its provided services in `ProvidedServices`, registers the instance in `RegisterAsync`, and consuming modules retrieve it via `TryGetModuleService<T>`.

```csharp
// AudioAnalysisModule.cs — provides IAudioAnalysisService
using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Convai.Runtime.Core;
using Convai.Runtime.Core.Modules;
using Convai.Runtime.Room;

// Application-owned service contract. Add the analysis data your visualizer needs.
public interface IAudioAnalysisService
{
    bool IsMicrophoneMuted { get; }
    void Start();
    void Stop();
}

// Minimal application-owned implementation. Replace Start and Stop with your analyzer lifecycle.
public sealed class AudioAnalysisService : IAudioAnalysisService
{
    private readonly IConvaiRoomAudioService _roomAudio;

    public AudioAnalysisService(IConvaiRoomAudioService roomAudio)
    {
        _roomAudio = roomAudio;
    }

    public bool IsMicrophoneMuted => _roomAudio == null || _roomAudio.IsMicMuted;
    public void Start() { }
    public void Stop() { }
}

public class AudioAnalysisModule : IConvaiModule
{
    public string ModuleId    => "my-company.audio-analysis";
    public string DisplayName => "Audio Analysis";

    public IReadOnlyList<string> RequiredModules  => Array.Empty<string>();
    public IReadOnlyList<Type>   RequiredServices => Array.Empty<Type>();
    public IReadOnlyList<Type>   ProvidedServices => new[] { typeof(IAudioAnalysisService) };

    public bool IsActive { get; private set; }
    private AudioAnalysisService _service;

    public ValueTask RegisterAsync(IModuleContext context, CancellationToken ct = default)
    {
        _service = new AudioAnalysisService(context.RoomAudio);
        context.ProvideModuleService<IAudioAnalysisService>(_service); // Must be in RegisterAsync, not StartAsync.
        return default;
    }

    public ValueTask StartAsync(IModuleContext context, CancellationToken ct = default)
    { IsActive = true; _service.Start(); return default; }

    public ValueTask PauseAsync(RuntimePauseReason reason, CancellationToken ct = default)
    { IsActive = false; return default; }

    public ValueTask ResumeAsync(CancellationToken ct = default)
    { IsActive = true; return default; }

    public ValueTask StopAsync(CancellationToken ct = default)
    { IsActive = false; _service.Stop(); return default; }
}
```

A consuming module would resolve that application-owned service as follows. This excerpt omits the other `IConvaiModule` members so the focus stays on service discovery:

```csharp
// VisualizerModule.cs — consumes IAudioAnalysisService
// pseudocode: the remaining IConvaiModule members are omitted.
public class VisualizerModule : IConvaiModule
{
    public IReadOnlyList<Type> RequiredServices => new[] { typeof(IAudioAnalysisService) };
    // ... other interface members ...

    public ValueTask StartAsync(IModuleContext context, CancellationToken ct = default)
    {
        if (context.TryGetModuleService<IAudioAnalysisService>(out var analysis))
        {
            // analysis is guaranteed non-null here.
        }
        return default;
    }
}
```

{% hint style="warning" %}
Always use `TryGetModuleService` — never assume the service is present. If `AudioAnalysisModule` is not registered, `TryGetModuleService` returns `false` without throwing, letting `VisualizerModule` degrade gracefully.
{% endhint %}

## Register a module

### MonoBehaviour self-registration (recommended)

Attach the module as a component to any GameObject. It self-registers with `ConvaiManager` on `Awake`.

```csharp
// HapticFeedbackBridge.cs
// pseudocode: implement the remaining IConvaiModule members from the interface above.
using Convai.Runtime.Components;
using Convai.Runtime.Core.Modules;
using UnityEngine;

public class HapticFeedbackBridge : MonoBehaviour, IConvaiModule
{
    public string ModuleId    => "my-company.haptic-feedback";
    public string DisplayName => "Haptic Feedback";
    // ... implement remaining IConvaiModule members ...

    private void Awake()
    {
        // ConvaiManager.Awake() runs at execution order -1100.
        // This Awake() runs at default order 0 — ConvaiManager.ActiveManager is already set.
        ConvaiManager.ActiveManager?.RegisterModule(this);
    }

    private void OnDestroy()
    {
        ConvaiManager.ActiveManager?.UnregisterModule(this);
    }
}
```

After `ConvaiManager.Start()` completes, `ConvaiManager.ActiveManager.IsInitialized` returns `true`, indicating all registered modules have been discovered and the runtime has started.

### CreateRuntimeBuilder override

Use this when you prefer all customization in one place, or when the module is not a `MonoBehaviour`.

```csharp
// CustomRuntimeManager.cs
using Convai.Runtime.Components;
using Convai.Runtime.Core;

public class CustomRuntimeManager : ConvaiManager
{
    protected override ConvaiRuntimeBuilder CreateRuntimeBuilder()
    {
        ConvaiRuntimeBuilder builder = base.CreateRuntimeBuilder();
        builder.AddModule(new HapticFeedbackModule());
        builder.AddModule(new AudioAnalysisModule());
        return builder;
    }
}
```

## Use the dependency injection pattern

Components on `ConvaiCharacter` or `ConvaiPlayer` GameObjects can receive SDK services automatically by implementing `IInjectable<TDependencies>`. The SDK injects dependencies after the character or player is registered with the runtime.

### IInjectable\<TDependencies\>

```csharp
public interface IInjectable<in TDependencies> where TDependencies : class
{
    int  InjectionOrder => 0;                        // Lower = injected first. Default 0.
    void InjectDependencies(TDependencies dependencies);
}
```

### IConvaiCharacterDependencies

| Property | Type | Availability |
| ------------------- | ------------------------------ | ------------ |
| `EventHub` | `IEventHub` | Required |
| `ConnectionService` | `IConvaiRoomConnectionService` | Required |
| `AudioService` | `IConvaiRoomAudioService` | Required |
| `AgentRegistry` | `IAgentRegistry` | Optional |
| `Logger` | `ILogger` | Optional |

### IConvaiPlayerDependencies

| Property | Type | Availability |
| ------------------------ | ------------------------------- | ------------ |
| `PlayerInputService` | `IPlayerInputService` | Optional |
| `RuntimeSettingsService` | `IConvaiRuntimeSettingsService` | Optional |
| `Logger` | `ILogger` | Optional |

### Write an injectable component

```csharp
// CharacterHealthIndicator.cs
using Convai.Domain.DomainEvents.Runtime;
using Convai.Domain.EventSystem;
using Convai.Domain.Logging;
using Convai.Runtime.Core.DependencyInjection;
using UnityEngine;
using ConvaiLogger = Convai.Domain.Logging.ILogger;

public class CharacterHealthIndicator : MonoBehaviour,
    IInjectable<IConvaiCharacterDependencies>
{
    public int InjectionOrder => 0;

    private IEventHub _events;
    private ConvaiLogger _logger;
    private SubscriptionToken _subscription;

    public void InjectDependencies(IConvaiCharacterDependencies dependencies)
    {
        _events = dependencies.EventHub;
        _logger = dependencies.Logger;
        _subscription = _events.Subscribe<CharacterTurnCompleted>(OnTurnCompleted);
    }

    private void OnTurnCompleted(CharacterTurnCompleted e)
    {
        _logger?.Debug("[CharacterHealthIndicator] Turn completed.", LogCategory.Character);
        // Update health indicator UI here.
    }

    private void OnDestroy()
    {
        _events?.Unsubscribe(_subscription);
    }
}
```

Add this component to the same GameObject as `ConvaiCharacter`. The SDK calls `InjectDependencies` automatically during character registration.

## Usage examples

### Example 1: Biometric correlation module for medical simulation

The following integration excerpt records character emotion data alongside biometric sensor readings for post-session analysis. `BiometricLogger` represents your application's sensor logger and is intentionally not defined by the SDK.

```csharp
// pseudocode: BiometricLogger is an application-owned sensor integration.
using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Convai.Domain.DomainEvents.Runtime;
using Convai.Domain.EventSystem;
using Convai.Runtime.Core;
using Convai.Runtime.Core.Modules;

public class BiometricCorrelationModule : IConvaiModule
{
    public string ModuleId    => "medsim.biometric-correlation";
    public string DisplayName => "Biometric Correlation";
    public IReadOnlyList<string> RequiredModules  => Array.Empty<string>();
    public IReadOnlyList<Type>   RequiredServices => Array.Empty<Type>();
    public IReadOnlyList<Type>   ProvidedServices => Array.Empty<Type>();
    public bool IsActive { get; private set; }

    private IEventHub _events;
    private SubscriptionToken _emotionSubscription;
    private BiometricLogger _bioLogger;

    public ValueTask RegisterAsync(IModuleContext context, CancellationToken ct = default)
    {
        _bioLogger = BiometricLogger.Instance;
        return default;
    }

    public ValueTask StartAsync(IModuleContext context, CancellationToken ct = default)
    {
        _events = context.Events;
        _emotionSubscription = _events.Subscribe<CharacterEmotionChanged>(OnEmotionChanged);
        IsActive = true;
        return default;
    }

    public ValueTask PauseAsync(RuntimePauseReason reason, CancellationToken ct = default)
    { IsActive = false; return default; }

    public ValueTask ResumeAsync(CancellationToken ct = default)
    { IsActive = true; return default; }

    public ValueTask StopAsync(CancellationToken ct = default)
    {
        _events?.Unsubscribe(_emotionSubscription);
        _events = null;
        IsActive = false;
        return default;
    }

    private void OnEmotionChanged(CharacterEmotionChanged e)
    {
        if (!IsActive) return;
        _bioLogger.Record(timestamp: e.Timestamp, emotionLabel: e.Emotion, intensity: e.Intensity);
    }
}
```

### Example 2: Assessment scoring module for industrial training

This excerpt tracks character-triggered actions against a scoring rubric and exposes an application-owned score service to other modules via `ProvideModuleService`.

```csharp
// pseudocode: IAssessmentScoreService and AssessmentScoreService are application-owned.
using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Convai.Domain.DomainEvents.Runtime;
using Convai.Domain.EventSystem;
using Convai.Runtime.Core;
using Convai.Runtime.Core.Modules;

public class ScoringModule : IConvaiModule
{
    public string ModuleId    => "industrial.scoring";
    public string DisplayName => "Assessment Scoring";
    public IReadOnlyList<string> RequiredModules  => Array.Empty<string>();
    public IReadOnlyList<Type>   RequiredServices => Array.Empty<Type>();
    public IReadOnlyList<Type>   ProvidedServices => new[] { typeof(IAssessmentScoreService) };
    public bool IsActive { get; private set; }

    private AssessmentScoreService _scoreService;
    private IEventHub _events;
    private SubscriptionToken _actionSubscription;

    public ValueTask RegisterAsync(IModuleContext context, CancellationToken ct = default)
    {
        _scoreService = new AssessmentScoreService();
        context.ProvideModuleService<IAssessmentScoreService>(_scoreService);
        return default;
    }

    public ValueTask StartAsync(IModuleContext context, CancellationToken ct = default)
    {
        _events = context.Events;
        _actionSubscription = _events.Subscribe<CharacterActionReceived>(OnActionReceived);
        IsActive = true;
        return default;
    }

    public ValueTask PauseAsync(RuntimePauseReason reason, CancellationToken ct = default)
    { IsActive = false; return default; }

    public ValueTask ResumeAsync(CancellationToken ct = default)
    { IsActive = true; return default; }

    public ValueTask StopAsync(CancellationToken ct = default)
    {
        _events?.Unsubscribe(_actionSubscription);
        _events = null;
        IsActive = false;
        return default;
    }

    private void OnActionReceived(CharacterActionReceived e)
    {
        if (!IsActive) return;
        foreach (var action in e.Actions)
            _scoreService.RecordAction(action.Name, action.Target, e.Timestamp);
    }
}
```

## Troubleshooting

| Symptom | Likely cause | Fix |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Module's `StartAsync` never called | `RegisterAsync` threw an unhandled exception; the runtime halts module startup silently | Wrap `RegisterAsync` body in a try-catch and log explicitly. |
| `TryGetModuleService<T>` returns `false` unexpectedly | `ProvideModuleService<T>` was called in `StartAsync` instead of `RegisterAsync` | Move `ProvideModuleService<T>` to `RegisterAsync` — services must be registered before any module's `StartAsync` runs. |
| Module starts but misses early events | Subscribed in `RegisterAsync` but event fires during startup before `StartAsync` | Move subscriptions to `StartAsync`, or guard with `IsActive` check in the handler. |
| `RequiredModules` entry causes startup error | Listed module ID not registered before runtime build | Verify the module ID string matches exactly — IDs are case-sensitive. |
| `InjectDependencies` never called on `IInjectable` component | Component is not on a GameObject in the `ConvaiCharacter` hierarchy | `IInjectable<IConvaiCharacterDependencies>` only works on GameObjects that are children of a character. |
| `ConvaiManager.ActiveManager` is null in `Awake` | Manager's `Awake` has not yet run at execution order −1100 | Register modules in `Start()` or use `ConvaiManager.ActiveManager?.RegisterModule(this)` with null-safety. |

## Next steps

{% content-ref url="performance-and-optimization.md" %}
[Logging, metrics, and retry policy](performance-and-optimization.md)
{% endcontent-ref %}

{% content-ref url="../core-concepts/event-system.md" %}
[Event System](../core-concepts/event-system.md)
{% endcontent-ref %}
