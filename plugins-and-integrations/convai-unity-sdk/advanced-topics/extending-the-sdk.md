---
title: Runtime module system
description: Understand the Convai runtime module system, including when to use custom modules, the module lifecycle states, and which SDK extension points are safe to use.
last_reviewed: "5.0.0-pre.1"
---

Use the manager's public facades for application scripts, and implement `IConvaiModule` when a feature must start, pause, resume, and stop with the Convai runtime.

## Choose an extension point

| Your feature needs to | Use |
| --- | --- |
| React to room state or character speech, actions, and emotion | `ConvaiManager.Events` |
| Display chat history or captions | `ConvaiManager.Transcripts` |
| Handle ordered action commands | An executor registered with the character’s action system |
| Fetch player-specific Convai credentials | `IConvaiAuthTokenProvider` or `RoomSessionConnectOptions.SetAuthToken` |
| Supply application identity | `SetEndUserIdentityProvider` and `SetEndUserMetadataProvider` on the manager |
| Participate in runtime startup and shutdown | `IConvaiModule` with `ConvaiManager.RegisterModule` |

## Module lifecycle

A module has its own activity state. Its runtime can start before a room connects, pause local presentation while the connection remains open, and stop when the manager is torn down. Code that needs a connected room can subscribe to session events or check the manager's state.

| Callback | What it does |
| --- | --- |
| `RegisterAsync` | Prepare the module using the context supplied by the runtime |
| `StartAsync` | Activate the module and subscribe to runtime events |
| `PauseAsync`, `ResumeAsync` | Suspend or restore the module's local activity |
| `StopAsync` | Release the module's subscriptions and resources |

`IModuleContext` exposes `Events`, `Agents`, `Transport`, and `Logger`. Keep responsibilities local to the module. Runtime room and audio operations go through `ConvaiManager` and `ConvaiManager.Audio`.

## Migrate builder-based integrations

The manager now composes its runtime internally. Replace a subclass override of `CreateRuntimeBuilder` with a component that registers its module with the scene manager. Register identities and metadata directly on the manager. Configure authentication with project settings or the supported token sources.

## Related pages

- [Implement a custom module](implement-a-custom-module.md)
- [Runtime architecture](../core-concepts/runtime-architecture.md)
- [Authentication](../authentication/README.md)
