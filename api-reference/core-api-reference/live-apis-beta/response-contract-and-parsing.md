---
title: Response contract and parsing
description: >-
  Understand legacy and canonical model output, raw text projection, action
  parsing, client execution feedback, and reserved response patterns.
---

A Convai character can produce conversational text, semantic actions, client tool calls, and emotion. The contract your client receives depends on the capabilities selected at `/connect`.

{% hint style="warning" %}
Actions protocol v2, canonical model output v2, and raw `bot-llm-text` are opt-in candidate surfaces. This documentation does not confirm production availability or a published SDK release. Verify the `capabilities` returned by your target environment.
{% endhint %}

---

## Select an output contract

| Selection | Delivered behavior |
|---|---|
| Omit `capabilities` | Action protocol v1, model output v1, and legacy filtered `bot-llm-text`. The `/connect` response omits `capabilities`. |
| `action_protocol_version: 2` | Correlated client `tool_call` items and [`action-result`](client-to-server-messages.md#action-result) feedback. |
| `model_output_version: 2` | Typed [`model-output`](server-to-client-messages.md#model-output) envelopes become the canonical output authority. |
| `bot_llm_text_mode: "raw"` | The existing `bot-llm-text` event carries provider-visible text before structured-output parsing and conversational filtering. |

These selections are independent, but every non-legacy selection requires a singular created session. See [Agentic Actions v2 preview](connect-api.md#agentic-actions-v2-preview) for the topology and tool declaration constraints.

This candidate surface does not define built-in display, link, card, table, CSV, or quick-response schemas. Do not treat raw text as a display protocol. If your application uses an `extension` item, accept only schemas and versions that your client explicitly recognizes, and always provide a safe fallback.

---

## How actions are separated

Semantic actions and client tool calls use different paths:

1. You declare semantic action affordances and optional client tools in `action_config` at [`/connect`](connect-api.md).
2. When **Enable Agentic Actions** is on for the character, Convai adds the applicable contract to the prompt. When it is off, semantic action and client tool schemas are not exposed to the model. A missing persisted setting is treated as off with model output v2, while model output v1 keeps its legacy behavior.
3. Semantic actions can use provider-native calls or a supported structured response that Convai parses. Client tools require provider-native function calling.
4. Convai emits semantic actions or correlated client tool calls through canonical `model-output` when selected. It can also emit `action-response` as a compatibility projection.

The resolved model must support provider-native function calling for client tools. Capability negotiation alone does not authorize an operation or guarantee that a model can call a declared tool.

### The action rules the character is given

Convai adds these constraints when semantic action affordances are active:

* A complete, ordered action sequence is returned **only** when the user asks for a physical task.
* Only exact action names from your `actions` list may be used. The model is instructed never to invent or rename actions.
* Only objects and characters from your `objects` and `characters` lists may be targeted. `scene_description` is descriptive context only — **it does not expand the affordance list**.
* `"me"`, `"my"`, and `"here"` resolve to the current speaker.
* `"this"`, `"that"`, `"it"`, and `"there"` resolve to `current_attention_object` when one is set.
* If the task is impossible, unsupported, non-physical, unsafe, or verbally refused, the action list is empty.
* If the character declines the task in its spoken reply, the action list is also empty.
* Action payloads should not be written into conversational text.

{% hint style="warning" %}
Prompt instructions reduce invalid model output, but they are not client authorization. Convai validates semantic action names and targets before projection. For client tools, it validates the declared name and JSON Schema arguments, while your application remains responsible for permissions, confirmation, execution, and side-effect safety.
{% endhint %}

---

## Canonical model output

When `model_output_version` is `2`, each completed envelope includes a unique `output_id`, an optional `logical_turn_id`, the original `raw` string, and typed `items`. Use `items` as the only trusted renderable or executable projection. Never parse or execute `raw`.

A logical turn can produce multiple envelopes, such as one for text and another for a semantic action or client tool call. Deduplicate by `output_id`. Group related envelopes by `logical_turn_id` when it is present. `final: true` completes one envelope rather than the entire logical turn.

The supported item types are:

| Item | Purpose |
|---|---|
| `message` | Assistant `content` on the `"final"` or `"commentary"` channel. |
| `semantic_action` | Validated semantic action with `id`, `name`, and optional `target`. |
| `tool_call` | Correlated client tool request with `id`, `name`, optional `target`, and validated `arguments`. |
| `emotion` | Emotion `name` and intensity `scale`. |
| `extension` | Schema-versioned payload for a client-recognized extension. No display or quick-response schema is defined by this preview. |

Current producers emit final-channel messages, semantic actions, client tool calls, and emotions. Commentary-channel messages and `extension` items are valid typed projections that candidate clients can parse, but the current runtime does not produce them.

Convai continues to emit legacy projections for compatibility. If your client chooses model output v2, consume `model-output.items` and ignore duplicate `action-response` messages.

## Client tool execution feedback

A `tool_call` is a request for the client to consider. Convai does not execute it. The client validates the request against local policy, performs or rejects the operation, and sends one terminal [`action-result`](client-to-server-messages.md#action-result) with `"completed"`, `"error"`, or `"cancelled"`.

Convai acknowledges the result with `server-response`. Retrying the same terminal payload for an accepted call ID is idempotent. A conflicting retry is rejected. After an accepted result, Convai supplies it to the same model context so generation can continue. Do not use the acknowledgment as an ordering barrier; continuation output can arrive first.

Calls can be outstanding in parallel. The candidate implementation permits up to `8` outstanding calls and up to `8` continuation rounds per user turn. It waits `60` seconds by default before returning a timeout error to the model. These limits do not imply sequential execution or exactly-once side effects in your application.

## bot-llm-text modes

`bot-llm-text` remains a streaming text projection in both modes:

| Mode | Content | Safe use |
|---|---|---|
| `"legacy"` or omitted | Conversational text after the legacy parsing and filtering path. | Chat transcript and the established spoken-response path. |
| `"raw"` | Provider-visible text chunks before Convai's structured-output parsing and conversational filtering. | Diagnostics or an explicitly labeled developer view. |

Raw mode can include structured JSON, control syntax, refusal text, audio-transcript text, or other provider-visible text fields. It is not guaranteed to include non-text native tool-call deltas. It does not replace `model-output.items`, and it must not drive actions. The parsed conversational and speech path remains authoritative even when raw text is projected to the client.

If raw delivery fails, Convai continues the parsed output path and can emit a nonfatal `raw_bot_llm_text_delivery_failed` error. The failed raw chunk is not replayed.

---

## Legacy text filtering

In legacy mode, Convai applies a fixed filter sequence before conversational text is projected or reaches speech synthesis. Raw `bot-llm-text` bypasses this client projection filter, but it does not change the parsed speech path.

| # | Removed | Matched | Scope |
|---|---|---|---|
| 1 | Abstain control markers | `[ABSTAIN]`, `[ABSTAINED]` (case-insensitive) | Anywhere in the text |
| 2 | Internal tool-call syntax | See [reserved patterns](#reserved-patterns) below | **Leading only** |
| 3 | Markdown formatting | Standard markdown emphasis, headings, list markers, code fences | Anywhere |
| 4 | Visual modality labels | `[vision]`, `[camera]`, `camera:` and similar — see below | **Leading only**, when vision input is active |
| 5 | Narrative design index prefix | `<index>\|\|\|` at the very start of the response | Leading only, when narrative design is active |
| 6 | Emoji | Unicode emoji and shortcodes | Anywhere, at the speech synthesis stage |

Filters 1–5 affect legacy `bot-llm-text` and the spoken path. Filter 6 applies only at the speech stage, so emoji may remain in legacy text while being omitted from speech.

### Streaming behavior

Filters operate on a streaming token stream, not on a complete response. A pattern split across two chunks — `[ABS` followed by `TAIN]` — is still removed correctly: the server buffers any trailing fragment that could be the start of a reserved pattern and releases it once it is proven not to match. A consequence worth knowing: **the last few characters of a response may be held briefly** before being emitted.

---

## Reserved patterns

These patterns are removed when they appear at the **start** of the character's response. Do not instruct a character to begin a reply with any of them, and do not design a response format that uses them.

**Internal tool-call syntax.** A label followed by a call expression:

```text
tool_code: <name>(...)
tool_call: <name>(...)
function_call: <name>(...)
```

where `<name>` is one of `look`, `get_image`, `abstain`, or `emit_actions`. Matching is case-insensitive. Bare call syntax — `get_image(...)`, `abstain(...)`, `emit_actions(...)` — is also removed. The parser matches balanced parentheses and respects quoting, so nested parentheses and quoted strings inside the call are handled correctly. Up to four consecutive such prefixes are stripped from one response.

**Visual modality labels.** Bracketed or colon-suffixed forms of `vision`, `visual`, `camera`, `webcam`, `canvas`, `screen`:

```text
[vision] ...        [vision]: ...        vision: ...
[camera] ...        [camera]: ...        camera: ...
```

**Abstain markers.** `[ABSTAIN]` and `[ABSTAINED]`, anywhere in the text.

**Narrative design prefix.** A leading integer followed by three pipes — `1|||`, `-1|||` — when narrative design is active on the character.

Mid-sentence mentions are preserved by these leading-pattern filters. Only occurrences at the start of legacy conversational output are treated as tool-call or vision control syntax.

---

## Writing custom prompts and response formats

If you write your own core description, character prompt, or output format, these rules will keep you out of trouble:

* **Do not open a response with any reserved pattern.** A reply that begins `function_call: emit_actions(...)` will have that prefix silently removed and your client will never see it.
* **Do not rely on markdown surviving the legacy path.** Emphasis, headings, and code fences are removed from conversational output. Use canonical `model-output.items` or a declared client tool instead of parsing formatted text.
* **Do not put action payloads in conversational text.** Use `action_config` and process validated semantic items. JSON that survives the legacy path can be read aloud.
* **Keep raw text separate from speech.** Raw `bot-llm-text` is a developer projection and can differ from the parsed text sent through the spoken path.
* **Keep template and scene text free of reserved prefixes.** Values injected via `narrative_template_keys`, `update-scene-metadata`, or `context-update` become part of the prompt and can influence how a response begins.

---

## Troubleshooting

**The character reads scaffolding, JSON, or option lists aloud.**
The parsed conversational output contains structure that survives filtering. Move executable data into a declared tool or semantic action, and keep the conversational response natural.

**An action never fires.**
Confirm that **Enable Agentic Actions** is on for the character and that the target model supports the required output mode. For a semantic action, confirm that its name and target are declared. For a client tool, confirm that action protocol v2 was selected and the declaration passed schema validation.

**A tool call appears, but the model never continues.**
Return an `action-result` whose `id` matches the call. Check the `server-response` acknowledgment for `status: "success"`. Unknown, stale, cross-session, conflicting, or oversized results are rejected.

**The character's reply is missing its first few words.**
Those words most likely matched a reserved leading pattern. Check the [reserved patterns](#reserved-patterns) list — particularly the vision labels, which are common English words followed by a colon.

**Actions and speech are out of sync.**
Semantic items can share a `logical_turn_id`, but they do not carry word-level offsets. See [Ordering guarantees](turn-lifecycle-and-message-ordering.md#ordering-guarantees).

**A leading `|||` sequence disappears from a response.**
Narrative design is active and the leading index prefix is being consumed. Avoid starting responses with an integer followed by three pipes.

---

## Related pages

* [Turn lifecycle and message ordering](turn-lifecycle-and-message-ordering.md) — how output is delivered and what ordering you can rely on
* [model-output](server-to-client-messages.md#model-output) — canonical v2 envelope and item fields
* [action-response](server-to-client-messages.md#action-response) — legacy and compatibility projections
* [Connect API](connect-api.md#agentic-actions-v2-preview) — capabilities, tools, limits, and topology constraints
* [action-result](client-to-server-messages.md#action-result) — returning correlated client execution feedback
