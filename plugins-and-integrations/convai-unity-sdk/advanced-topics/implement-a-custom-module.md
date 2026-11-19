---
title: Implement a custom module
description: Build a custom runtime module that starts with the SDK, accesses its services, and reacts to character and session events.
last_reviewed: "5.0.0-pre.1"
---

Implement `IConvaiModule` to give a Unity feature the same start, pause, resume, and stop lifecycle as the Convai runtime. This example counts character-readiness events while a module is active.

## Prerequisites

Set up an active `ConvaiManager` and at least one `ConvaiCharacter`. For setup, see [Build a custom scene](../getting-started/build-a-custom-scene.md).

## Implement and register the module

Save the script as `CharacterReadinessCounter.cs`. Add it to a GameObject and assign the scene manager. The script holds the manager reference from `Awake` through `OnDestroy`.

{% code title="Assets/Scripts/CharacterReadinessCounter.cs" %}
```csharp
using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Convai.Domain.DomainEvents.Runtime;
using Convai.Domain.EventSystem;
using Convai.Runtime.Components;
using Convai.Runtime.Core;
using Convai.Runtime.Core.Modules;
using UnityEngine;

public sealed class CharacterReadinessCounter : MonoBehaviour, IConvaiModule
{
    [SerializeField] private ConvaiManager manager;

    private IEventSubscriberHub events;
    private SubscriptionToken readySubscription;
    private bool paused;

    public string ModuleId => "example.character-readiness-counter";
    public string DisplayName => "Character readiness counter";
    public IReadOnlyList<string> RequiredModules => Array.Empty<string>();
    public bool IsActive => events != null;
    public int ReadyCount { get; private set; }

    private void Awake() => manager.RegisterModule(this);

    private void OnDestroy()
    {
        if (manager != null)
            manager.UnregisterModule(this);
    }

    public ValueTask RegisterAsync(IModuleContext context, CancellationToken ct) => default;

    public ValueTask StartAsync(IModuleContext context, CancellationToken ct)
    {
        events = context.Events;
        readySubscription = events.Subscribe<CharacterReady>(RecordReady);
        return default;
    }

    public ValueTask PauseAsync(RuntimePauseReason reason, CancellationToken ct)
    {
        paused = true;
        return default;
    }

    public ValueTask ResumeAsync(CancellationToken ct)
    {
        paused = false;
        return default;
    }

    public ValueTask StopAsync(CancellationToken ct)
    {
        if (events != null)
            events.Unsubscribe(readySubscription);
        events = null;
        paused = false;
        return default;
    }

    private void RecordReady(CharacterReady ready)
    {
        if (!paused)
            ReadyCount++;
    }
}
```
{% endcode %}

The runtime calls `RegisterAsync` before `StartAsync`. Register before the runtime starts when a feature must see startup events. A module added to a running manager starts after a frame deferral, and it receives future events from the time it subscribes. Use distinct module IDs. If your module needs another module to start first, declare that relationship in `RequiredModules` and register the dependency first.

## Verify and troubleshoot

Connect a character and check `ReadyCount` in a debugger or bind it to an application display. It increases when a character becomes ready while the module is active. Stop the runtime or destroy the script, then verify that it no longer counts events.

If `StartAsync` never runs, confirm the scene manager is active before the example registers. If the counter stays at zero, confirm the character reached readiness after module startup and that presentation is active.

## Related pages

- [Runtime module system](extending-the-sdk.md)
- [Character events](../scripting-reference/character-events.md)
- [Session lifecycle](../core-concepts/session-lifecycle.md)
