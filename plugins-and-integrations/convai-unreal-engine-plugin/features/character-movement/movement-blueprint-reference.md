---
title: Movement Blueprint reference
last_reviewed: "4.0.0-beta.27"
description: >-
  Reference for the Convai Move To and Convai Escort Blueprint nodes, their
  inputs, outputs, and every result code they can return.
---

`Convai Move To` and `Convai Escort` are the two Blueprint nodes for character movement, both in category `Convai|Movement`. Each is an async node backed by a Blueprint proxy object (`UConvaiMoveToProxy` and `UConvaiEscortProxy`) that exposes only `Succeeded` and `Failed` exec pins — the underlying native movement tasks have no Blueprint surface of their own.

## Convai Move To

Moves `Moving Actor` to `Destination`. Backed by the `ConvaiMoveTo` `UFUNCTION` on `UConvaiMoveToProxy`.

| Pin | Type | Direction | Description |
|---|---|---|---|
| `Moving Actor` | `Actor` | Input | The character to move. Must be a pawn controlled by an AI Controller with a movement component and a path-following component. |
| `Destination` | `FConvaiObjectEntry` | Input | What to move to — a whole actor, a specific component, or the entry's authored movement points. See [How character movement works](how-character-movement-works.md). |
| `Lock AI Logic` | `bool` | Input, advanced display | Default `false`. Reserved for compound behaviors that need to fully own the character's movement while this move runs. |
| `Succeeded` | exec, `Result Code` (`EConvaiMoveToResultCode`), `Additional Note` (`FString`) | Output | Fires when `Result Code` is `Reached` or `Already At Destination`. |
| `Failed` | exec, `Result Code` (`EConvaiMoveToResultCode`), `Additional Note` (`FString`) | Output | Fires for every other result code. |

`Additional Note` is safe to speak to a player or feed back into a character's context. It is populated on both `Succeeded` and `Failed`.

## Convai Escort

Sends `Escorting Actor` to `Destination`, leading `Escorted Character` there. Backed by the `ConvaiEscort` `UFUNCTION` on `UConvaiEscortProxy`.

| Pin | Type | Direction | Description |
|---|---|---|---|
| `Escorting Actor` | `Actor` | Input | The character doing the escorting. Owns the Convai chatbot used for the temporary follow prompt when `Escorted Character` falls behind. |
| `Escorted Character` | `FConvaiObjectEntry` | Input | The character being led to `Destination`. |
| `Destination` | `FConvaiObjectEntry` | Input | Where `Escorting Actor` leads `Escorted Character` — a whole actor, a specific component, or the entry's authored movement points. |
| `Succeeded` | exec, `Result Code` (`EConvaiEscortResultCode`), `Additional Note` (`FString`) | Output | Fires when `Result Code` is `Reached` or `Already At Destination`. |
| `Failed` | exec, `Result Code` (`EConvaiEscortResultCode`), `Additional Note` (`FString`) | Output | Fires for every other result code. |

`Escorting Actor` and `Escorted Character` are both `FConvaiObjectEntry` and retain their complete object-entry semantics — either can be scoped to a whole actor or a specific component.

## EConvaiMoveToResultCode

Reported on `Convai Move To`'s `Succeeded` and `Failed` pins as `Result Code`.

| Value | Display name | Meaning |
|---|---|---|
| `Reached` | `Reached` | The character reached the resolved destination. |
| `AlreadyAtDestination` | `Already At Destination` | No move was necessary because the character was already there. |
| `UnknownDestination` | `Unknown Destination` | The destination actor disappeared or could not be resolved. |
| `Unreachable` | `Unreachable` | The destination is known, but no usable route reaches it from here. |
| `InvalidCharacter` | `Invalid Character` | `Moving Actor` is not a usable pawn. |
| `MissingController` | `Missing AI Controller` | The pawn is not controlled by an AI Controller. |
| `MissingMovementComponent` | `Missing Movement Component` | The pawn has no movement component. |
| `MissingPathFollowingComponent` | `Missing Path Following Component` | The AI Controller has no path-following component. |
| `MissingNavigationData` | `Missing Navigation Data` | The world has no compatible navigation data for this pawn. |
| `MoveFailed` | `Move Failed` | Unreal stopped the move even though the destination still resolved as reachable. |
| `Cancelled` | Hidden — not selectable in Blueprint | Internal lifecycle marker. Reaches the `Failed` pin only when the request's owner is destroyed unexpectedly mid-move; an explicit `Cancel` call on the proxy detaches silently instead and fires neither pin. |

`Succeeded` fires for `Reached` and `Already At Destination`; every other value, including the hidden `Cancelled`, fires `Failed`.

## EConvaiEscortResultCode

Reported on `Convai Escort`'s `Succeeded` and `Failed` pins as `Result Code`.

| Value | Display name | Meaning |
|---|---|---|
| `Reached` | `Reached` | `Escorting Actor` and `Escorted Character` reached the destination. |
| `AlreadyAtDestination` | `Already At Destination` | The escort began with both actors already at the destination. |
| `EscorteeUnavailable` | `Character Unavailable` | `Escorted Character` disappeared or is not a valid escort target. |
| `DestinationUnavailable` | `Destination Unavailable` | `Destination` disappeared or could not be reached from here. |
| `InvalidGuideSetup` | `Invalid Escort Setup` | `Escorting Actor` is missing setup required by escort (for example, no AI Controller). |
| `MovementFailed` | `Movement Failed` | Unreal stopped the owned movement before escort reached its destination. |
| `Cancelled` | Hidden — not selectable in Blueprint | Internal lifecycle marker reported as a failed public request. |

`Succeeded` fires for `Reached` and `Already At Destination`; every other value, including the hidden `Cancelled`, fires `Failed`.

## Supporting types

### FConvaiObjectEntry

`Destination` on both nodes, and `Escorted Character` on `Convai Escort`, are `FConvaiObjectEntry`. The fields that drive movement:

| Field | Type | Description |
|---|---|---|
| `Ref` | `Actor` | The actor being referenced. |
| `ObjectReference` | `EConvaiObjectReference` | Shown as **Object Is**. What the entry represents — see the values table below. |
| `ComponentName` | `FString` | When `ObjectReference` is `Specific Component`, the component to target. |
| `SocketOrBoneName` | `FName` | Optional socket or bone on the matched component to target instead of its origin. |
| `AcceptanceRadius` | `float` | How close, in centimeters, counts as arrived. Default `150.0`. |
| `MovementPoints` | array of `FConvaiMovementPoint` | Authored access points that take over destination resolution when any are enabled. |
| `bFallbackToObjectWhenPointsUnreachable` | `bool` | Shown as **Use Object as Fallback**. Default `false`. When every movement point is unreachable, fall back to the object itself instead of reporting unreachable. |

For the full struct, including the non-movement fields, see [Convai Object Component](../../blueprint-reference/convai-object-component.md).

### FConvaiMovementPoint

An entry in `FConvaiObjectEntry.MovementPoints`, edited via the viewport visualizer on `Convai Object Component` or directly in the **Details** panel.

| Field | Type | Description |
|---|---|---|
| `Transform` | `Transform` | Where the character stands when this point is chosen. Only the location drives movement; rotation is stored for future facing control. |
| `Attachment` | `EConvaiMovementPointAttachment` | How the transform is interpreted — see the values table below. Default `Relative To Object`. |
| `bEnabled` | `bool` | Default `true`. Untick to take the point out of play without deleting it. If every point on an entry is disabled, the entry behaves as if it had none. |
| `bCreatesSeparateDestination` | `bool` | Shown as **Create Separate Destination**. Default `false`. When ticked, the point becomes its own named destination instead of one of several places to stand at the object. |
| `Name` | `FString` | Shown as **Destination Name**. Only used while `bCreatesSeparateDestination` is on. The character addresses it as "`<Object>` `<Destination Name>`". |

### EConvaiObjectReference

| Value | Display name | Meaning |
|---|---|---|
| `WholeActor` | `Whole Actor` | The whole actor is the object. Movement fallback: the character walks toward the actor and stops at its bounds. |
| `SpecificComponent` | `Specific Component` | A sub-component on the actor is the object. Movement fallback: the character walks to that component's location. |

### EConvaiMovementPointAttachment

| Value | Display name | Meaning |
|---|---|---|
| `RelativeToObject` | `Relative To Object` | Default. The point's transform is relative to the object — it moves with the goal actor, or with the specific component when `ObjectReference` is component-scoped. |
| `KeepWorldPosition` | `Keep World Position` | Advanced. The point's transform is absolute world space and stays put even if the object moves. |
