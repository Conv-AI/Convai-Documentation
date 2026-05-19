# extending the sdk

The Convai Unity SDK is built around a module system that gives optional features — lip sync, emotion, vision, narrative design — a defined place in the runtime lifecycle. You can add your own modules using the same system: they receive the same startup sequence, access the same services, and can share interfaces with other modules.

This page covers what the module system provides, how to implement `IConvaiModule`, how to share services between modules, and what the SDK's dependency injection pattern looks like for character and player components.

***

## What a Module Is

A module is a class that implements `IConvaiModule`. It:

* Has a stable `ModuleId` string (unique, lowercase, hyphen-separated by convention — e.g., `"my-company.haptic-feedback"`).
* Declares dependencies on other modules via `RequiredModules` and on runtime services via `RequiredServices`.
* Participates in the runtime lifecycle: Register → Start → Pause ↔ Resume → Stop.
* Can expose typed services to other modules via `IModuleContext.ProvideModuleService<T>()`.

The module system handles startup ordering automatically — modules are started in dependency order, stopped in reverse.

***

## `IConvaiModule` — Full Contract

```csharp
public interface IConvaiModule
{
    string ModuleId { get; }
    string DisplayName { get; }
    IReadOnlyList<string> RequiredModules { get; }
    IReadOnlyList<Type> RequiredServices { get; }
    IReadOnlyList<Type> ProvidedServices { get; }
    bool IsActive { get; }

    ValueTask RegisterAsync(IModuleContext context, CancellationToken ct = default);
    ValueTask StartAsync(IModuleContext context, CancellationToken ct = default);
    ValueTask PauseAsync(RuntimePauseReason reason, CancellationToken ct = default);
    ValueTask ResumeAsync(CancellationToken ct = default);
    ValueTask StopAsync(CancellationToken ct = default);
}
```

### Lifecycle Methods

| Method          | When Called                                        | What To Do                                                                                           |
| --------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `RegisterAsync` | During runtime build — before any `StartAsync`     | Register services this module provides via `context.ProvideModuleService<T>()`. Subscribe to events. |
| `StartAsync`    | Runtime start — after all modules are registered   | Start active behaviors: begin subscriptions, start coroutines, initialize hardware.                  |
| `PauseAsync`    | Runtime paused (app loses focus, deliberate pause) | Stop processing. Receive `RuntimePauseReason` to distinguish why.                                    |
| `ResumeAsync`   | Runtime resumed                                    | Restart processing paused in `PauseAsync`.                                                           |
| `StopAsync`     | Runtime stopping or module removed                 | Clean up: unsubscribe, stop coroutines, release resources.                                           |

`RegisterAsync` runs before `StartAsync` for all modules. Use `RegisterAsync` for setup that other modules may depend on.

***

## `IModuleContext` — Available Services

The `IModuleContext` passed to each lifecycle method provides typed access to runtime services:

| Property      | Type                      | Availability | Description                                  |
| ------------- | ------------------------- | ------------ | -------------------------------------------- |
| `Runtime`     | `ConvaiRuntime`           | Always       | The runtime instance this module belongs to. |
| `Events`      | `IEventHub`               | Always       | Publish and subscribe to domain events.      |
| `Agents`      | `IAgentRegistry`          | Always       | Query registered characters and players.     |
| `Transport`   | `ITransportProvider`      | May be null  | Platform-specific communication layer.       |
| `Preferences` | `IRuntimePreferences`     | May be null  | Mutable runtime preferences.                 |
| `Logger`      | `ILogger`                 | May be null  | Logger for diagnostics.                      |
| `RoomAudio`   | `IConvaiRoomAudioService` | May be null  | Microphone and playback service.             |
| `Credentials` | `ICredentialProvider`     | May be null  | API key and server URL resolution.           |

Always null-check `Transport`, `Preferences`, `Logger`, `RoomAudio`, and `Credentials` before use. `Events` and `Agents` are always available.

***

## Implementing A Custom Module

### Minimal Module

{% code title="HapticFeedbackModule.cs" lineNumbers="true" %}
```csharp
using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Convai.Domain.DomainEvents.Runtime;
using Convai.Domain.EventSystem;
using Convai.Domain.Logging;
using Convai.Runtime.Core.Modules;

public class HapticFeedbackModule : IConvaiModule
{
    public string ModuleId    => "my-company.haptic-feedback";
    public string DisplayName => "Haptic Feedback";

    // No module dependencies
    public IReadOnlyList<string> RequiredModules  => Array.Empty<string>();
    public IReadOnlyList<Type>   RequiredServices => Array.Empty<Type>();
    public IReadOnlyList<Type>   ProvidedServices => Array.Empty<Type>();

    public bool IsActive { get; private set; }

    private ILogger _logger;
    private IDisposable _subscription;

    public ValueTask RegisterAsync(IModuleContext context, CancellationToken ct = default)
    {
        _logger = context.Logger;
        return ValueTask.CompletedTask;
    }

    public ValueTask StartAsync(IModuleContext context, CancellationToken ct = default)
    {
        _subscription = context.Events.Subscribe<CharacterSpeechStateChanged>(OnCharacterSpeechStateChanged);
        IsActive = true;

        _logger?.Debug("[HapticFeedbackModule] Started.", LogCategory.SDK);
        return ValueTask.CompletedTask;
    }

    public ValueTask PauseAsync(RuntimePauseReason reason, CancellationToken ct = default)
    {
        IsActive = false;
        return ValueTask.CompletedTask;
    }

    public ValueTask ResumeAsync(CancellationToken ct = default)
    {
        IsActive = true;
        return ValueTask.CompletedTask;
    }

    public ValueTask StopAsync(CancellationToken ct = default)
    {
        _subscription?.Dispose();
        IsActive = false;

        _logger?.Debug("[HapticFeedbackModule] Stopped.", LogCategory.SDK);
        return ValueTask.CompletedTask;
    }

    private void OnCharacterSpeechStateChanged(CharacterSpeechStateChanged e)
    {
        // Fire haptic only when character starts speaking, not when they stop
        if (!IsActive || !e.IsSpeaking) return;
        HapticService.Pulse(HapticPattern.Soft);
    }
}
```
{% endcode %}

***

### Module Sharing Services With Other Modules

A module can expose a typed service via `ProvideModuleService<T>()` in `RegisterAsync`, and other modules can retrieve it via `TryGetModuleService<T>()`:

{% code title="AudioAnalysisModule.cs" lineNumbers="true" %}
```csharp
public class AudioAnalysisModule : IConvaiModule
{
    public string ModuleId    => "my-company.audio-analysis";
    public string DisplayName => "Audio Analysis";
    public IReadOnlyList<string> RequiredModules  => Array.Empty<string>();
    public IReadOnlyList<Type>   RequiredServices => Array.Empty<Type>();

    // Declare what this module provides so dependent modules can declare RequiredServices
    public IReadOnlyList<Type>   ProvidedServices => new[] { typeof(IAudioAnalysisService) };

    public bool IsActive { get; private set; }

    private AudioAnalysisService _service;

    public ValueTask RegisterAsync(IModuleContext context, CancellationToken ct = default)
    {
        _service = new AudioAnalysisService(context.RoomAudio);
        context.ProvideModuleService<IAudioAnalysisService>(_service);
        return ValueTask.CompletedTask;
    }

    public ValueTask StartAsync(IModuleContext context, CancellationToken ct = default)
    { IsActive = true; _service.Start(); return ValueTask.CompletedTask; }

    public ValueTask PauseAsync(RuntimePauseReason reason, CancellationToken ct = default)
    { IsActive = false; return ValueTask.CompletedTask; }

    public ValueTask ResumeAsync(CancellationToken ct = default)
    { IsActive = true; return ValueTask.CompletedTask; }

    public ValueTask StopAsync(CancellationToken ct = default)
    { IsActive = false; _service.Stop(); return ValueTask.CompletedTask; }
}
```
{% endcode %}

A consuming module declares a dependency and retrieves the service in `StartAsync`:

```csharp
public class VisualizerModule : IConvaiModule
{
    public IReadOnlyList<Type> RequiredServices => new[] { typeof(IAudioAnalysisService) };
    // ... RequiredModules = new[] { "my-company.audio-analysis" } if you want order guarantee

    public ValueTask StartAsync(IModuleContext context, CancellationToken ct = default)
    {
        if (context.TryGetModuleService<IAudioAnalysisService>(out var analysis))
        {
            // Use the service
        }
        return ValueTask.CompletedTask;
    }
}
```

Use `TryGetModuleService` — never assume the service is present. Another module's `RegisterAsync` may have failed or the module may not be registered.

***

## Registering A Custom Module

Two registration paths exist depending on your needs.

{% tabs %}
{% tab title="MonoBehaviour Self-Registration (Recommended)" %}
This is how all shipped SDK modules (LipSync, Vision, Emotion, etc.) register themselves. The module component calls `ConvaiManager.RegisterModule(this)` in its own `Awake()`. `ConvaiManager` discovers all registered modules in `Start()` before the runtime activates.

```csharp
using Convai.Runtime.Components;
using Convai.Runtime.Core.Modules;
using UnityEngine;

public class HapticFeedbackBridge : MonoBehaviour, IConvaiModule
{
    // IConvaiModule implementation ...
    public string ModuleId    => "my-company.haptic-feedback";
    public string DisplayName => "Haptic Feedback";
    // ...

    private void Awake()
    {
        ConvaiManager.ActiveManager?.RegisterModule(this);
    }

    private void OnDestroy()
    {
        ConvaiManager.ActiveManager?.UnregisterModule(this);
    }
}
```

Add this component to any GameObject in the scene. `ConvaiManager.Awake()` runs at execution order −1100; your `Awake()` runs at default order 0, so the manager is always ready when you call `RegisterModule`.

{% hint style="success" %}
After `Start()` completes on `ConvaiManager`, check `ConvaiManager.ActiveManager.IsInitialized == true`. If so, all registered modules have been discovered and the runtime has started.
{% endhint %}
{% endtab %}

{% tab title="CreateRuntimeBuilder Override" %}
Use this when you want all runtime customization in one place, or when the module is a plain C# class (not a MonoBehaviour).

```csharp
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

Modules added this way are available before any MonoBehaviour `Awake()` runs and are always part of the runtime regardless of scene composition.
{% endtab %}
{% endtabs %}

***

## The Dependency Injection Pattern

Character and player components receive typed dependency bundles via `IInjectable<TDependencies>`. Understanding this pattern helps when writing components that integrate tightly with `ConvaiCharacter` or `ConvaiPlayer`.

### `IInjectable<TDependencies>`

```csharp
public interface IInjectable<TDependencies>
{
    int InjectionOrder { get; }           // Lower = injected first. Default 0.
    void InjectDependencies(TDependencies dependencies);
}
```

`InjectionOrder` controls sequencing. Infrastructure components (e.g., room managers that must configure themselves before character scripts) use negative values (e.g., `−100`). Application-level components use `0` or positive values.

### `IConvaiCharacterDependencies`

The bundle injected into components on a `ConvaiCharacter` GameObject:

| Property            | Type                           | Availability |
| ------------------- | ------------------------------ | ------------ |
| `EventHub`          | `IEventHub`                    | Required     |
| `ConnectionService` | `IConvaiRoomConnectionService` | Required     |
| `AudioService`      | `IConvaiRoomAudioService`      | Required     |
| `AgentRegistry`     | `IAgentRegistry`               | Optional     |
| `Logger`            | `ILogger`                      | Optional     |

### `IConvaiPlayerDependencies`

The bundle injected into components on a `ConvaiPlayer` GameObject:

| Property                 | Type                            | Availability |
| ------------------------ | ------------------------------- | ------------ |
| `PlayerInputService`     | `IPlayerInputService`           | Optional     |
| `RuntimeSettingsService` | `IConvaiRuntimeSettingsService` | Optional     |
| `Logger`                 | `ILogger`                       | Optional     |

### Writing An Injectable Component

Add `IInjectable<IConvaiCharacterDependencies>` to a component on a character's GameObject and the SDK will inject dependencies automatically at startup:

```csharp
using Convai.Domain.DomainEvents.Runtime;
using Convai.Domain.EventSystem;
using Convai.Domain.Logging;
using Convai.Runtime.Core.DependencyInjection;
using UnityEngine;

public class CharacterHealthIndicator : MonoBehaviour,
    IInjectable<IConvaiCharacterDependencies>
{
    public int InjectionOrder => 0;

    private IEventHub _events;
    private ILogger _logger;

    public void InjectDependencies(IConvaiCharacterDependencies dependencies)
    {
        _events = dependencies.EventHub;
        _logger = dependencies.Logger;

        // Safe to subscribe here — injection happens before Start()
        _events.Subscribe<CharacterTurnCompleted>(OnTurnCompleted);
    }

    private void OnTurnCompleted(CharacterTurnCompleted e)
    {
        _logger?.Debug("[CharacterHealthIndicator] Turn completed.", LogCategory.Character);
        // Update health UI based on turn outcome
    }

    private void OnDestroy()
    {
        _events?.Unsubscribe<CharacterTurnCompleted>(OnTurnCompleted);
    }
}
```

***

## What Is Safe To Extend vs. What Is Internal

### Safe Extension Points

| What                                  | How                                                                            |
| ------------------------------------- | ------------------------------------------------------------------------------ |
| Custom module behavior                | Implement `IConvaiModule` and register via `RegisterModule()` or `AddModule()` |
| Inter-module services                 | `ProvideModuleService<T>()` / `TryGetModuleService<T>()`                       |
| Custom credentials                    | Override `CreateRuntimeBuilder()` and call `builder.UseConfig()`               |
| Custom identity                       | `SetEndUserIdentityProvider()` / `SetEndUserMetadataProvider()`, or builder    |
| Custom persistence                    | Override `CreateRuntimeBuilder()` and call `builder.UsePersistence()`          |
| Character-level component integration | Implement `IInjectable<IConvaiCharacterDependencies>`                          |
| Event subscriptions                   | `IEventHub.Subscribe<T>()` / `Unsubscribe<T>()`                                |
| Log routing                           | `ConvaiLogger.RegisterSink(ILogSink)`                                          |

### Do Not Touch (Internal)

| Area                                                   | Why                                                                         |
| ------------------------------------------------------ | --------------------------------------------------------------------------- |
| `ConvaiRuntime` internals                              | Private by design; subject to change without notice                         |
| Transport layer (`ITransportProvider` implementations) | Platform-specific; changes break platform support                           |
| RTVI protocol handler (`RTVIHandler`)                  | Serialization format is tied to Convai's backend — any override will desync |
| `ConvaiRoomManager` internals                          | Room coordinator internals are not extension points                         |
| Module execution ordering beyond `RequiredModules`     | The topological sort is automatic; do not rely on registration order        |

{% hint style="danger" %}
Do not reflect into internal types or bypass the builder to inject dependencies. The SDK's internal composition changes between versions, and code that bypasses the public API will break on upgrade.
{% endhint %}

***

## Usage Examples

### Example 1: Biometric Feedback Module for Medical Simulation

A medical simulation records trainee physiological data (heart rate, galvanic skin response) during high-stress scenarios. A custom module subscribes to character emotion events and streams emotion data to the biometric logger:

```csharp
using Convai.Domain.DomainEvents.Runtime;

public class BiometricCorrelationModule : IConvaiModule
{
    public string ModuleId    => "medsim.biometric-correlation";
    public string DisplayName => "Biometric Correlation";
    public IReadOnlyList<string> RequiredModules  => Array.Empty<string>();
    public IReadOnlyList<Type>   RequiredServices => Array.Empty<Type>();
    public IReadOnlyList<Type>   ProvidedServices => Array.Empty<Type>();
    public bool IsActive { get; private set; }

    private IDisposable _emotionSubscription;
    private BiometricLogger _bioLogger;

    public ValueTask RegisterAsync(IModuleContext context, CancellationToken ct = default)
    {
        _bioLogger = BiometricLogger.Instance;
        return ValueTask.CompletedTask;
    }

    public ValueTask StartAsync(IModuleContext context, CancellationToken ct = default)
    {
        _emotionSubscription = context.Events.Subscribe<CharacterEmotionChanged>(OnEmotionChanged);
        IsActive = true;
        return ValueTask.CompletedTask;
    }

    public ValueTask PauseAsync(RuntimePauseReason reason, CancellationToken ct = default)
    { IsActive = false; return ValueTask.CompletedTask; }

    public ValueTask ResumeAsync(CancellationToken ct = default)
    { IsActive = true; return ValueTask.CompletedTask; }

    public ValueTask StopAsync(CancellationToken ct = default)
    {
        _emotionSubscription?.Dispose();
        IsActive = false;
        return ValueTask.CompletedTask;
    }

    private void OnEmotionChanged(CharacterEmotionChanged e)
    {
        if (!IsActive) return;
        _bioLogger.Record(timestamp: e.Timestamp,
                          emotionLabel: e.Emotion,
                          intensity: e.Intensity);
    }
}
```

Register in `Awake()` on a MonoBehaviour, or via `CreateRuntimeBuilder()` on a custom manager subclass.

***

### Example 2: Assessment Scoring Module for Industrial Training

A factory safety simulation tracks every in-scene action the AI character executes (e.g., "open valve," "don safety gear") and feeds them into a scoring engine. The module subscribes to action dispatch events:

```csharp
using Convai.Domain.DomainEvents.Runtime;

public class ScoringModule : IConvaiModule
{
    public string ModuleId    => "industrial.scoring";
    public string DisplayName => "Assessment Scoring";
    public IReadOnlyList<string> RequiredModules  => Array.Empty<string>();
    public IReadOnlyList<Type>   RequiredServices => Array.Empty<Type>();
    public IReadOnlyList<Type>   ProvidedServices => new[] { typeof(IAssessmentScoreService) };
    public bool IsActive { get; private set; }

    private AssessmentScoreService _scoreService;
    private IDisposable _actionSubscription;

    public ValueTask RegisterAsync(IModuleContext context, CancellationToken ct = default)
    {
        _scoreService = new AssessmentScoreService();
        context.ProvideModuleService<IAssessmentScoreService>(_scoreService);
        return ValueTask.CompletedTask;
    }

    public ValueTask StartAsync(IModuleContext context, CancellationToken ct = default)
    {
        _actionSubscription = context.Events.Subscribe<CharacterActionReceived>(OnActionReceived);
        IsActive = true;
        return ValueTask.CompletedTask;
    }

    // ... PauseAsync, ResumeAsync, StopAsync follow the same pattern

    private void OnActionReceived(CharacterActionReceived e)
    {
        if (!IsActive) return;
        foreach (var action in e.Actions)
            _scoreService.RecordAction(action.Name, action.Target, e.Timestamp);
    }
}
```

A HUD component retrieves `IAssessmentScoreService` via `TryGetModuleService` to display the live score without coupling to the module directly.

***

## Next Steps

{% content-ref url="/broken/pages/a58f1d98b0a82868bb728feac43c66a53a7ad23f" %}
[Broken link](/broken/pages/a58f1d98b0a82868bb728feac43c66a53a7ad23f)
{% endcontent-ref %}

{% content-ref url="/broken/pages/fe15ce405ecded16923b808753cce24f0bdf9c56" %}
[Broken link](/broken/pages/fe15ce405ecded16923b808753cce24f0bdf9c56)
{% endcontent-ref %}
