---
title: How character movement works
last_reviewed: "4.0.0-beta.27"
description: >-
  Explains how Convai resolves a movement destination, picks a movement
  point, falls back to an object's bounds, and defines arrival.
---

`Convai Move To` and `Convai Escort` both resolve their destination through the same `FConvaiObjectEntry` the rest of the plugin uses for objects and characters. Understanding that resolution — what counts as the destination, which movement point wins when several are available, and what happens when none are authored — explains why a character walks where it does and why some moves finish instantly.

## How a destination is resolved

Every `Destination` passed to `Convai Move To` or `Convai Escort` is an `FConvaiObjectEntry`. Its `Object Is` field (`ObjectReference`, of type `EConvaiObjectReference`) decides what the entry's `Ref` actor represents:

- `Whole Actor` — the entire actor is the destination. With no movement points authored, the character walks toward the actor and stops at its bounds.
- `Specific Component` — a named sub-component (optionally a socket or bone, via `ComponentName` and `SocketOrBoneName`) is the destination. With no movement points authored, the character walks to that component's location.

The entry's own `ResolveGoalLocation` function turns this into the goal location, acceptance radius, and — when a moving actor is supplied — whether that actor is already at the goal (`bOutAlreadyThere`) and whether a navmesh path can reach it (`bOutReachable`).

## Choosing a movement point

A `Convai Object Component` can carry a list of `FConvaiMovementPoint` entries — designer-authored access points that describe where a character should stand when it approaches the object, such as one point on each side of a door. When an entry has enabled movement points, they take over destination resolution entirely: the object reference above still defines what the object *is*, but the movement points define *where* a character walking to it stands.

Resolution picks the reachable point with the shortest walking path. Every enabled point is checked, and the point with the shortest navmesh path from the moving character wins; an exact tie keeps the point earlier in the list. A point can also be disabled (`bEnabled = false`) without removing it, which takes it out of consideration without deleting its placement.

If every movement point is unreachable, the destination normally reports unreachable rather than silently picking a blocked point — a door with both sides barricaded should read as unreachable, not walkable. Ticking `Use Object as Fallback` (`bFallbackToObjectWhenPointsUnreachable`) changes this: when every authored point is blocked, resolution falls back to the object itself instead of failing.

## Falling back to the object's bounds

When an entry has no movement points at all, resolution falls back to the object reference itself:

- `Whole Actor` — the character walks toward the actor and the move stops at the actor's bounds, rather than at the actor's exact origin. This matters for wide objects: a character does not need to reach the object's pivot to count as arrived.
- `Specific Component` with `ComponentName` set — the character walks to that component's (or named socket/bone's) location.
- `Specific Component` with `ComponentName` left empty — the character walks to the actor's own position, the same as `Whole Actor` without bounds-stepping.

This fallback is what a designer gets by leaving `Movement Points` empty on a `Convai Object Component` — no extra setup is required for a character to be able to walk up to an object.

## Arriving versus already being there

A finished `Convai Move To` or `Convai Escort` request reports one of two success outcomes, and they mean different things:

- **Already at destination** — the moving character was already at the resolved goal when the request was made, so no move ever ran. This is reported immediately, without creating a movement task: `Convai Move To` resolves the destination, finds the character already within range, and finishes on the spot.
- **Reached** — a move actually ran and the character arrived at the resolved goal, whether the destination was stationary the whole time or moved while the character was walking toward it (a moving-target case is re-resolved as the move progresses).

Being "already there" is checked against `max(Acceptance Radius, 150 cm)` of a movement point, or `max(Acceptance Radius × 2, 150 cm)` of the object's bounding-box footprint when no movement points are authored, plus a check on the moving character's own height. `Convai Escort` uses this same resolution and the same arrival test for both the escorting actor and the character being escorted — see [Escort a character](escort-a-character.md) for how it waits and resumes.

For the complete list of result codes each node can report, see [Movement Blueprint reference](movement-blueprint-reference.md).
