---
title: Response contract and parsing
description: >-
  How Convai separates a character's spoken response from its actions and other
  non-verbal output, exactly what the server removes from the spoken text, and
  which patterns are reserved.
---

# Response contract and parsing

A Convai character produces more than speech. It can also emit actions for your client to execute, emotional tone for an avatar, and — when narrative design or vision are active — internal control data. All of that originates from a single model output stream and is separated **server-side** before it reaches you.

This page documents that separation precisely: what reaches the spoken response, what is removed, and which patterns are reserved. If you author custom core descriptions, prompts, or output formats, read this page — a character can be broken by text that is silently removed, and knowing the rules is the difference between a working agent and an unexplainable one.

---

## The three kinds of output

| Output | Delivered as | Spoken? |
|---|---|---|
| **Spoken response** | `bot-llm-text` messages + the WebRTC audio track | Yes |
| **Actions** | [`action-response`](server-to-client-messages.md#action-response) messages | No |
| **Emotion** | [`bot-emotion`](server-to-client-messages.md#bot-emotion) messages | No |

{% hint style="info" %}
There is currently **no channel for non-spoken visual content** — tables, links, cards, or rich media. Any such content the model produces will appear in the spoken response and be read aloud. If your experience needs to display something without speaking it, encode it in an action and render it client-side.
{% endhint %}

---

## How actions are separated

Actions are **not** parsed out of the response text. They travel on a separate path from the beginning.

1. You declare the available affordances in `action_config` at [`/connect`](connect-api.md), or replace them mid-session with [`context-update`](client-to-server-messages.md#context-update).
2. Convai injects those affordances into the character's prompt, together with the action rules below.
3. When the character decides to act, the model invokes a dedicated action tool rather than writing the action into its reply.
4. The server validates the result against your declared affordances and emits [`action-response`](server-to-client-messages.md#action-response).

The spoken response and the action sequence therefore never contend for the same text. This is the mechanism that keeps `"Move To cube"` out of the audio.

### The action rules the character is given

Convai adds these constraints to the prompt whenever `action_config` declares at least one action. They are worth knowing because they explain behavior you will observe:

* A complete, ordered action sequence is returned **only** when the user asks for a physical task.
* Only exact action names from your `actions` list may be used. The model is instructed never to invent or rename actions.
* Only objects and characters from your `objects` and `characters` lists may be targeted. `scene_description` is descriptive context only — **it does not expand the affordance list**.
* `"me"`, `"my"`, and `"here"` resolve to the current speaker.
* `"this"`, `"that"`, `"it"`, and `"there"` resolve to `current_attention_object` when one is set.
* If the task is impossible, unsupported, non-physical, unsafe, or verbally refused, the action list is empty.
* If the character declines the task in its spoken reply, the action list is also empty.
* Action payloads must not be written into the spoken response.

{% hint style="warning" %}
If a character keeps attempting actions on objects that are not in your `objects` list, add them to `action_config` — describing them in `scene_description` is not sufficient.
{% endhint %}

---

## What the server removes from the spoken response

Before any `bot-llm-text` message is emitted or any text reaches speech synthesis, the server applies a fixed sequence of filters. **These apply to both the text you receive and the audio you hear** — they run once, upstream of both.

| # | Removed | Matched | Scope |
|---|---|---|---|
| 1 | Abstain control markers | `[ABSTAIN]`, `[ABSTAINED]` (case-insensitive) | Anywhere in the text |
| 2 | Internal tool-call syntax | See [reserved patterns](#reserved-patterns) below | **Leading only** |
| 3 | Markdown formatting | Standard markdown emphasis, headings, list markers, code fences | Anywhere |
| 4 | Visual modality labels | `[vision]`, `[camera]`, `camera:` and similar — see below | **Leading only**, when vision input is active |
| 5 | Narrative design index prefix | `<index>\|\|\|` at the very start of the response | Leading only, when narrative design is active |
| 6 | Emoji | Unicode emoji and shortcodes | Anywhere, at the speech synthesis stage |

{% hint style="info" %}
Filters 1–5 affect **both** the `bot-llm-text` you receive and the spoken audio. Filter 6 (emoji) is applied at the speech stage only — emoji may still appear in the text you receive, but are never spoken.
{% endhint %}

### Streaming behavior

Filters operate on a streaming token stream, not on a complete response. A pattern split across two chunks — `[ABS` followed by `TAIN]` — is still removed correctly: the server buffers any trailing fragment that could be the start of a reserved pattern and releases it once it is proven not to match. A consequence worth knowing: **the last few characters of a response may be held briefly** before being emitted.

---

## Reserved patterns

These patterns are removed when they appear at the **start** of the character's response. Do not instruct a character to begin a reply with any of them, and do not design a response format that uses them.

**Internal tool-call syntax.** A label followed by a call expression:

```
tool_code: <name>(...)
tool_call: <name>(...)
function_call: <name>(...)
```

where `<name>` is one of `look`, `get_image`, `abstain`, or `emit_actions`. Matching is case-insensitive. Bare call syntax — `get_image(...)`, `abstain(...)`, `emit_actions(...)` — is also removed. The parser matches balanced parentheses and respects quoting, so nested parentheses and quoted strings inside the call are handled correctly. Up to four consecutive such prefixes are stripped from one response.

**Visual modality labels.** Bracketed or colon-suffixed forms of `vision`, `visual`, `camera`, `webcam`, `canvas`, `screen`:

```
[vision] ...        [vision]: ...        vision: ...
[camera] ...        [camera]: ...        camera: ...
```

**Abstain markers.** `[ABSTAIN]` and `[ABSTAINED]`, anywhere in the text.

**Narrative design prefix.** A leading integer followed by three pipes — `1|||`, `-1|||` — when narrative design is active on the character.

{% hint style="success" %}
**Mid-sentence mentions are safe.** Tool-call syntax and vision labels are only removed at the start of a response. A character can say *"the camera: prefix is used for..."* mid-sentence without it being stripped. Only leading occurrences are treated as control syntax.
{% endhint %}

---

## Writing custom prompts and response formats

If you write your own core description, character prompt, or output format, these rules will keep you out of trouble:

* **Do not open a response with any reserved pattern.** A reply that begins `function_call: emit_actions(...)` will have that prefix silently removed and your client will never see it.
* **Do not rely on markdown surviving.** Emphasis, headings, and code fences are removed from the spoken response. If you need structured output for a client to parse, deliver it as an action, not as formatted text.
* **Do not put action payloads in the reply text.** Use `action_config` and let the action path deliver them. JSON written into the spoken response will be read aloud.
* **Expect the whole reply to be spoken.** Everything in `bot-llm-text` that survives filtering is sent to speech synthesis. There is no marker that makes part of a reply visible-but-silent.
* **Keep template and scene text free of reserved prefixes.** Values injected via `narrative_template_keys`, `update-scene-metadata`, or `context-update` become part of the prompt and can influence how a response begins.

---

## Troubleshooting

**The character reads scaffolding, JSON, or option lists aloud.**
Its output format is producing content that is not a reserved pattern, so it survives filtering and is treated as speech. Move that content into actions, or change the prompt so the character speaks a natural summary instead of its structure.

**An action never fires.**
Check in order: is the action name an exact match for an entry in `action_config.actions`? Is the target present in `objects` or `characters` — not merely in `scene_description`? Did the character verbally decline, which forces an empty action list?

**The character's reply is missing its first few words.**
Those words most likely matched a reserved leading pattern. Check the [reserved patterns](#reserved-patterns) list — particularly the vision labels, which are common English words followed by a colon.

**Actions and speech are out of sync.**
This is expected. Actions carry no positional relationship to the response text — see [Ordering guarantees](turn-lifecycle-and-message-ordering.md#ordering-guarantees).

**A leading `|||` sequence disappears from a response.**
Narrative design is active and the leading index prefix is being consumed. Avoid starting responses with an integer followed by three pipes.

---

## Related pages

* [Turn lifecycle and message ordering](turn-lifecycle-and-message-ordering.md) — how output is delivered and what ordering you can rely on
* [action-response](server-to-client-messages.md#action-response) — the action message format
* [Connect API](connect-api.md) — declaring `action_config`
* [context-update](client-to-server-messages.md#context-update) — replacing affordances mid-session
