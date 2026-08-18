---
title: Convai Debug Overlay reference
description: Every panel, glyph, key, and setting the in-game Convai Debug Overlay exposes, with exact on-screen labels, colors, and keyboard shortcuts.
last_reviewed: "4.0.0-beta.27"
---

The Convai Debug Overlay is an in-game panel that displays a selected character's live context states, facts, surroundings text, events, and action queue. It has no Blueprint API and no console variables — the toggle key and the `Convai.DebugOverlay` console command are the entire surface. For a task-oriented walkthrough, see [Inspect a character with the Convai Debug Overlay](convai-debug-overlay.md).

## Toggle

| Method | Default | Notes |
|---|---|---|
| Key chord | `Ctrl+Alt+K` | Configurable. Ignored while a text field has keyboard focus. |
| Console command | `Convai.DebugOverlay` | Toggles the same overlay; works regardless of the configured key. |

## Settings

Configured on `UConvaiSettings`, category **Debug Overlay**, under **Project Settings > Plugins > Convai**.

| Setting | Type | Default | Description |
|---|---|---|---|
| `Toggle Key (with Ctrl+Alt)` | `FKey` | `K` | The key combined with `Ctrl+Alt` to open or close the overlay. |
| `Allow In Shipping Builds` | `bool` | `false` | When off, the overlay is a silent no-op in Shipping and Test builds: no widget appears, and both the toggle key and `Convai.DebugOverlay` do nothing. |

There is no separate enable switch. The overlay is always available in the Editor, in Play In Editor, and in Development builds.

## Build availability

| Build type | Behavior |
|---|---|
| Editor, Play In Editor, Development | Overlay always available. |
| Shipping, Test | Silent no-op unless `Allow In Shipping Builds` is on. No widget, no response to the key chord or console command. |

## Header

| Format | When shown |
|---|---|
| `Convai Debug — no character` | No character is selected. |
| `<CharacterName>  · TALKING  · looking at <Attention>` | A character is selected, currently talking, with an attention object set. |
| `<CharacterName>  · idle` | A character is selected, not talking, with no attention object set. |

## Panels

Panels apply to the currently selected character.

| Panel label | Contents |
|---|---|
| `CONTEXT STATES` | Key : value rows for every tracked context state. A row belonging to the currently selected object is tinted cyan. Each row carries a pulse dot colored by its response setting: red for `Always`, amber for `Auto`, grey for `Never`. |
| `FACTS` | Key : value rows for facts given to the character. Collapses when there are no facts. |
| `SURROUNDINGS` | One row per nearby object: the object name, `— reached` once the character's last move to it completed, `— no path` when navigation could not find a route, the verbatim sentence the character receives about the object, and `(pending flush)` when the entry is staged but not yet sent. |
| `EVENTS` | The last six committed events, in chronological order, followed by anything staged for the next flush (marked `(pending flush)`) and any one-shot events (marked `(one-shot)`). Collapses when there is nothing to show. |

## World-space markers

| Glyph | Meaning |
|---|---|
| `◆` | A registered character or `UConvaiObjectComponent` in the level. |
| `◇` | A named, enabled movement point on a registered object. |

Both marker types fade when occluded by level geometry.

## Action queue and results

Shown above the selected character.

| Glyph or format | Meaning |
|---|---|
| `▶ <action>` | The currently executing action. |
| `■ cancelling · <action>` | The current action, in the process of being cancelled. |
| `· <action>` | A queued action, not yet executing. |
| `<action> — done` | The action succeeded. Shown in the results ribbon for 2.5 seconds. |
| `<action> — failed (<note>)` | The action failed, with an optional note. Shown for 2.5 seconds. |
| `<action> — aborted (<note>)` | The action was aborted, with an optional note. Shown for 2.5 seconds. |

## Selection

| Input | Effect |
|---|---|
| `PgUp` | Cycle to the previous item in the current selection mode. |
| `PgDn` | Cycle to the next item in the current selection mode. |
| `Shift` + `PgUp` / `PgDn` | Switch selection mode between characters and objects, then cycle. |

Selection is keyboard-only; there is no mouse picking.

## Not a Blueprint surface

The debug overlay exposes no Blueprint nodes, no `UFUNCTION`s, and no console variables (CVars). The classes that implement it are internal: neither is `BlueprintType`, and the overlay widget lives in a private header. The toggle key and the `Convai.DebugOverlay` console command are the complete API — there is nothing further to call from Blueprint or C++.

## Related reference

{% content-ref url="convai-debug-overlay.md" %}
[Inspect a character with the Convai Debug Overlay](convai-debug-overlay.md)
{% endcontent-ref %}

{% content-ref url="README.md" %}
[Troubleshooting](README.md)
{% endcontent-ref %}
