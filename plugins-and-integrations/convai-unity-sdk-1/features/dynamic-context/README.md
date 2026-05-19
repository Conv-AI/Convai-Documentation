---
description: >-
  Learn how to feed live in-scene state and events to Convai characters so their
  responses reflect current conditions in your training simulation or
  experience.
---

# Dynamic Context

## Feeding Live In-Scene State to Your Characters

Dynamic Context gives your Convai characters real-time awareness of what is happening in the scene. Rather than responding only from a static system prompt, characters can reference live conditions — a trainee's current location, equipment collected, hazards triggered, or checkpoint status — and incorporate that information naturally into dialogue.

The system is built on two primitive types: **states**, which are named key-value pairs that track current conditions, and **events**, which are chronological one-time occurrences that accumulate in order. When a conversation is active, state and event updates reach the character in the same turn they are sent.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Quick Start</strong><br>Add the command component to an NPC and verify context-aware dialogue in five steps.</td><td><a href="/broken/pages/eca1675c31e01d8ec3f0ab8e44b3606e34f0ba16">Broken link</a></td></tr><tr><td><strong>Command Component Reference</strong><br>Field-by-field reference for all six command types, reaction modes, and validation warnings.</td><td><a href="/broken/pages/23641f6cd1ed71a4253512d00b181ad823093beb">Broken link</a></td></tr><tr><td><strong>Static Context at Connection Time</strong><br>Configure initial dynamic info sent once at connection for facts that do not change during a session.</td><td><a href="/broken/pages/ab4e5ca9e5f073792816b3ee7460e9c313b7dd04">Broken link</a></td></tr><tr><td><strong>Usage Examples</strong><br>Four end-to-end scenarios covering safety drills, onboarding, guided tours, and emergency transitions.</td><td><a href="/broken/pages/3a063e80d55ef385d5c5660d77ed448c0849e797">Broken link</a></td></tr><tr><td><strong>Scripting API Reference</strong><br>Full API reference for <code>IConvaiDynamicContext</code> — all seven methods with signatures and queueing behavior.</td><td><a href="/broken/pages/a6c0e9bdb7266d4e4677d7e8e2bf710fc8a3cbfa">Broken link</a></td></tr><tr><td><strong>Sync Behavior and Timing</strong><br>How and when Replace, Append, and Reset messages are transmitted for each context operation.</td><td><a href="/broken/pages/0a43f55b4dceed83ec93a264b6df1af85ba7d4a9">Broken link</a></td></tr><tr><td><strong>Troubleshooting &#x26; Diagnostics</strong><br>Investigation checklist, symptom table, decision tree, and Console log reference for common issues.</td><td><a href="/broken/pages/bba88c3acced140fc919269b5eafa038292fb2c0">Broken link</a></td></tr></tbody></table>

## How It Works

Dynamic Context operates on two building blocks.

**States** are persistent, named key-value pairs. When you set a state, any previous value for that name is replaced. The character always references the current value. States appear in the canonical context in the order they were **first set** — updating a value does not change its position.

**Events** are chronological, one-time occurrences. Unlike states, events accumulate in sequence and are never replaced or deduplicated. Each event is appended after all states in the canonical context.

When the SDK sends an update to Convai, the character receives the assembled canonical context: states first (in insertion order, formatted as `{Name} is {Value}`), then events in call order. This structure is built and managed automatically — you supply only names, values, and event text.

## Two Entry Points

**Inspector (no code required):** Add `ConvaiDynamicContextCommand` to the NPC's GameObject, configure the command type and values in the Inspector, and wire `Execute()` to a UnityEvent, animation, or trigger collider. One component = one command. For multiple commands per NPC, place each on a child GameObject.

**Scripting:** Access `character.DynamicContext` to get an `IConvaiDynamicContext` interface with seven methods: `SetState`, `SetStates`, `AddEvent`, `RemoveState`, `Reset`, `TryGetStateValue`, and `Apply`. Both paths write to the same underlying tracker and produce identical network behavior.

## Pre-Conversation Queueing

Updates made before a conversation begins are automatically queued. When the session connects, the SDK delivers a single Replace message containing the full canonical context. You do not need to delay updates until the character is connected — set state freely from `Awake` or `Start` and the SDK handles delivery.

{% hint style="warning" %}
`Apply()` is the one exception: it does not queue. If called before a conversation starts, the update is discarded. Use `SetState`, `AddEvent`, or other tracked methods for pre-conversation context. See [Scripting API Reference](/broken/pages/a6c0e9bdb7266d4e4677d7e8e2bf710fc8a3cbfa) for details.
{% endhint %}

## Next Steps

Start with [Quick Start](/broken/pages/eca1675c31e01d8ec3f0ab8e44b3606e34f0ba16) to get context-aware dialogue running in five steps. Then read [Command Component Reference](/broken/pages/23641f6cd1ed71a4253512d00b181ad823093beb) for the full Inspector configuration options, or [Scripting API Reference](/broken/pages/a6c0e9bdb7266d4e4677d7e8e2bf710fc8a3cbfa) for direct C# control.
