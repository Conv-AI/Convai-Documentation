---
title: Inspect a character with the Convai Debug Overlay
description: Turn on the in-game overlay to see the context, facts, surroundings text, and action queue a Convai character currently has.
last_reviewed: "4.0.0-beta.27"
---

When a character ignores an instruction, walks to the wrong object, or answers as if it never received a fact you sent it, the fastest way to find out why is to look at what the character actually knows, not at your own Blueprint graph. The Convai Debug Overlay is an in-game panel that shows, live, every context state, fact, and surroundings sentence a character has been given, along with its current action queue. This page shows you how to turn it on, select a character, and read the panels against a real question.

## Prerequisites

- The Convai Unreal Engine plugin is installed and at least one `UConvaiChatbotComponent` is placed in the level.
- You are running the Editor, Play In Editor (PIE), or a Development build. The overlay is a silent no-op in Shipping and Test builds unless you turn on **Allow In Shipping Builds** (see [Convai Debug Overlay reference](convai-debug-overlay-reference.md)).

## Turn on the overlay

Press **Ctrl+Alt+K** during Play In Editor or in a Development build. If a text field currently has keyboard focus, the chord is ignored — click into the viewport first.

You can also toggle the overlay from the console with:

```text
Convai.DebugOverlay
```

Both the chord and the console command open the same overlay, and either one toggles it off again.

{% hint style="info" %}
The default key is **K**. To use a different key, or to allow the overlay in Shipping builds, open **Project Settings > Plugins > Convai** and change **Toggle Key (with Ctrl+Alt)** or **Allow In Shipping Builds** under **Debug Overlay**. There is no separate on/off switch for the overlay itself — the toggle key and console command are the whole interface.
{% endhint %}

With no character selected, the header reads `Convai Debug — no character`. Once you select a character, the header shows its name, whether it is talking or idle, and what it is looking at, for example `Guard  · TALKING  · looking at Crate_03`.

## Select the character or object to inspect

The overlay tracks every registered character and every registered `UConvaiObjectComponent` in the level, marked in world space with a ◆ over each character or object and a ◇ over each named, enabled movement point.

Cycle the selection with the keyboard:

- **PgUp** / **PgDn** — cycle to the previous or next item.
- **Shift** + **PgUp** / **PgDn** — switch between cycling characters and cycling objects.

The selected character's panels populate on the left, and its action queue and results ribbon appear above it in world space.

## Read the panels against a question

Each panel answers a different question about what the character knows. For example, to find out why a character did not walk to a crate when asked:

1. Select the character and check **SURROUNDINGS** for the crate's entry. `— reached` means the character's last move to it completed; `— no path` means the navigation system could not find a route; `(pending flush)` means the update is still batched and has not been sent to Convai yet.
2. Check the crate's row for the exact sentence the character receives about it — this is the verbatim surroundings text, not a summary, so you can see precisely what the AI was told.
3. Check the action queue above the character. A `▶` marks the currently executing action, `·` marks queued actions behind it, and `■ cancelling ·` marks an action being cancelled. A results ribbon appears for 2.5 seconds after an action finishes, reading `<action> — done`, `<action> — failed (<note>)`, or `<action> — aborted (<note>)`.
4. Check **CONTEXT STATES** and **FACTS** for any state or fact that should have influenced the decision. Each context state row has a pulse dot: red means the state is set to respond **Always**, amber means **Auto**, and grey means **Never** — a state pulsing grey explains why the character never reacted to it.

**FACTS** and **EVENTS** each collapse when there is nothing to show, so their absence from the panel is itself informative. **EVENTS** lists the last six committed events plus anything staged for the next flush or sent as a one-shot.

For the full list of panels, labels, and glyphs, see [Convai Debug Overlay reference](convai-debug-overlay-reference.md).

## Verify the overlay is showing live data

Trigger the behavior you are debugging — send a context update, move the character, or wait for an action to complete — and confirm the relevant panel updates within a second or two.

{% hint style="success" %}
A panel that updates as you trigger events confirms the overlay is reading the selected character's live state, not a cached snapshot.
{% endhint %}

## Troubleshooting

### The overlay does not appear

**Symptom:** Pressing **Ctrl+Alt+K** or running `Convai.DebugOverlay` does nothing.

**Cause:** You are in a Shipping or Test build and **Allow In Shipping Builds** is off, or a text field has keyboard focus and is swallowing the key chord.

**Fix:** Click into the viewport to clear text field focus, then try the chord again. If you are testing a Shipping or Test build, enable **Allow In Shipping Builds** under **Project Settings > Plugins > Convai > Debug Overlay** and repackage.

**Verify:** The header line `Convai Debug — no character` (or a character name) appears on screen.

### A panel stays empty

**Symptom:** **FACTS** or **EVENTS** never appears for a selected character.

**Cause:** Both panels collapse when there is nothing to show — the character genuinely has no facts or committed events yet.

**Fix:** Send the character a fact or context event and confirm the panel appears once it has content.

**Verify:** The panel heading appears above its rows after the update lands.

## Next steps

{% content-ref url="convai-debug-overlay-reference.md" %}
[Convai Debug Overlay reference](convai-debug-overlay-reference.md)
{% endcontent-ref %}

{% content-ref url="README.md" %}
[Troubleshooting](README.md)
{% endcontent-ref %}
