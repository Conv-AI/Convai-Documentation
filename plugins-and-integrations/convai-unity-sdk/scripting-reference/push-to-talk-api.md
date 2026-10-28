---
title: Push-to-talk scripting reference
description: Drive push-to-talk from custom Unity input, observe capture and commit state, interpret release results, and recover a failed connection.
last_reviewed: "5.0.0-preview"
---

Use `ConvaiPushToTalkController` in `Convai.Runtime.Components` for custom input. It keeps capture, target ownership, and response waiting together. `PttState`, `PttCommitResult`, and release policy types live in `Convai.Runtime.Room`.

## Controller methods and state

| Member | Contract |
| --- | --- |
| `Press()` | Returns true if the press was accepted; releases on focus loss |
| `Press(bool keepThroughFocusLoss)` | Keep this accepted press through focus loss only when the caller can observe release without focus |
| `Release()` | Request release of the held capture; does not await its result |
| `SetPressed(bool)` | Calls Press or Release |
| `IsPressed` | Whether a press is held |
| `IsAwaitingTurnCompletion` | Whether reply waiting gates input |
| `State`, `ReleaseId` | PTT lifecycle and correlated release identifier |
| `BlockedReason` | Why a press was refused |
| `CompatibilityReason` | Why the Legacy path is in use |
| `ActiveTargetCharacterId`, `ActiveTargetParticipantId` | Target captured for the active press |
| `StateChanged` | `Action<PttState>` |
| `CommitCompleted` | `Action<PttCommitResult>`; correlated release only |
| `RetryAsync(CancellationToken)` | Recovery connection operation returning `RoomSession` |

State values are `Idle`, `Preparing`, `Capturing`, `Draining`, `AwaitingCommit`, `AwaitingBotTurn`, and `Error`. A true return from `Release()` only accepts the release path. For correlated release, observe `CommitCompleted` separately. The Legacy compatibility path, including unsupported Auto capture such as WebGL, does not emit that event or a `PttCommitResult`. Use `StateChanged`, `IsAwaitingTurnCompletion`, and `CompatibilityReason` to follow local compatibility progress without treating it as a server commit receipt.

A press requires a connected, microphone-enabled room in push-to-talk mode, available targeting, and no conflicting capture/release. A held press ends on pause, disable, disconnect, target/mode changes, or input holds even if it was created with `Press(true)`.

## Input lease

`ConvaiManager.AcquirePushToTalkInput()` returns `IDisposable`. Hold the lease while your input source replaces the manager's polling and dispose it when disabled. Drive the controller with your UI, Input System action, or platform input source. See [Use your own push-to-talk input](../getting-started/use-your-own-push-to-talk-input.md) for setup.

## Commit result

`ReleaseId`, `CommitCompleted`, and `PttCommitResult` describe the correlated release protocol. Do not wait for them when the controller uses Legacy compatibility release.

| Property | Meaning |
| --- | --- |
| `ReleaseId` | Correlates a local release |
| `Status` | `Committed`, `Empty`, or `Failed` |
| `ResponseId` | Service response identifier when supplied |
| `Reason` | Supplied reason or local failure description |
| `ReconnectRequired` | Connection needs recovery, including some committed outcomes |

Committed means speech submission was accepted by this protocol; it does not mean a character finished answering. Local drain completion alone is also not server receipt.

## Room-level API

`ConvaiRoomManager` in `Convai.Runtime.Adapters.Networking` exposes `PttState`, `PttReleaseId`, `PttError`, `LastPttCommitResult`, `PttCompatibilityReason`, `PttStateChanged`, and `PttCommitCompleted`.

`ForceUserStoppedSpeakingAsync(string releaseId, CancellationToken)` returns `IConvaiOperation<PttCommitResult>` for correlated stop handling. `RetryPttAsync(CancellationToken)` returns a recovery connection operation. These are lower-level services; ordinary input should use the controller so capture and target cleanup remain coordinated.

## Related pages

- [Push-to-talk lifecycle](../core-concepts/push-to-talk-lifecycle.md)
- [Turn-taking modes](../core-concepts/turn-taking-modes.md)
