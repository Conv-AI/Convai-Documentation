---
title: How character actions work
description: Understand the action affordance model, how the server resolves pronoun references, and why scene metadata does not grant new actions.
last_reviewed: "2026-06-11"
---

Character actions are structured instructions that Convai emits alongside spoken output when a user's request maps to a physical interaction in your scene. The affordance model governs which actions, objects, and characters the character is permitted to target, and why descriptive scene metadata cannot expand that set.

## The action affordance model

An affordance is the set of actions a character is allowed to perform, together with the objects and characters it can target. Affordances are declared once, at connect time, inside the `action_config` field of the `POST /connect` body.

The affordance set has three components:

- **Actions**: the verbs the character may use, such as `"Move To"` or `"Pick Up"`.
- **Objects**: the named objects in the scene that actions can be applied to, each with a short description.
- **Characters**: the named participants the character can target, each with a brief biography.

Convai treats `action_config` as the single authority for what the character is allowed to do. No subsequent message can expand the allowed action target set.

## Why update-scene-metadata does not grant affordances

The `update-scene-metadata` client message updates the server's descriptive understanding of the environment. It lets you describe objects that have entered or changed in the scene so the character can speak about them accurately.

`update-scene-metadata` is descriptive only. It does not add objects to `action_config.objects` and does not grant the character permission to act on those objects.

The reason for this separation is intentional: affordance state is kept authoritative and stable for the life of the session. Descriptive state is permitted to change freely as the user moves through the environment. Conflating the two would make it impossible to reason about which actions the character can take at any point in the session.

If you need the character to act on a new object that was not in the original `action_config`, you must disconnect and reconnect with an updated `action_config`.

## How Convai resolves pronoun references

When a user refers to something with a pronoun, Convai uses session state to resolve the referent.

| Pronoun class | Resolves to |
|---|---|
| `"this"`, `"that"`, `"it"`, `"there"` | The current `current_attention_object` when one is set |
| `"me"`, `"my"`, `"here"` | The current speaker or player |

For example, if `current_attention_object` is set to `"cube"` and the user says "pick that up", the server resolves `"that"` to `"cube"` and may emit a `Pick Up` action targeting `"cube"`.

If no `current_attention_object` is set, the pronouns in the first group cannot be resolved and the character is less likely to emit meaningful action output for requests that rely on implicit object reference.

## The action-response loop

Each conversation turn follows this sequence:

1. Convai receives user speech or text.
2. The language model produces spoken output and decides which actions, if any, are appropriate.
3. Convai emits an `action-response` server event containing an ordered array of `{ name, target }` objects.
4. If no action is appropriate — because the request is conversational, impossible, unsupported, non-physical, or the character verbally declines — the array is empty (`[]`).

The `action-response` event always arrives as an array. No-action turns emit `[]`, not `null` and not the legacy string `"None"`. Your client must treat an empty array as a valid no-op.

## Reconnecting when affordances change

If the set of objects or actions the character should be allowed to target changes during a session, you must reconnect. Sending a new `update-scene-metadata` payload does not update affordances. Only the `action_config` on `POST /connect` is authoritative.

{% content-ref url="configure-actions.md" %}
[Configure actions on connect](configure-actions.md)
{% endcontent-ref %}

{% content-ref url="update-scene-and-attention.md" %}
[Update scene context and attention](update-scene-and-attention.md)
{% endcontent-ref %}
