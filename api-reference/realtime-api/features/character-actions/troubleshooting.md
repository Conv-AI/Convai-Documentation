---
title: Troubleshoot character actions
description: Fix common character action failures in the Realtime API, including missing action responses, unrecognized objects, and attention name mismatches.
last_reviewed: "2026-06-11"
---

This page covers the most common failure modes for character actions in the Realtime API. Each entry describes the symptom, explains the cause, and provides a fix.

## No action-response event is received

**Symptom:** The character speaks normally but no `action-response` event arrives on any turn.

**Cause:** The session was established without `action_config`. When `action_config` is absent from the `POST /connect` body, the character operates in conversational-only mode and never emits `action-response` events.

**Fix:** Reconnect and include `action_config` in the `/connect` request body with at least one entry in `actions` and one entry in `objects`. See [Configure actions on connect](configure-actions.md).

**Verify:** After reconnecting, send a message that requests a physical action on one of the configured objects. An `action-response` event should arrive alongside the spoken response.

## action-response arrives but actions array is always empty

**Symptom:** `action-response` events arrive but `actions` is always `[]`, even for requests that should trigger an action.

**Cause:** The user's request does not map to any configured action or object. Other causes include: the user is using pronouns with no `current_attention_object` set, or the character determines the request is non-physical, unsafe, or declined.

**Fix:**
- Confirm that the action verbs in `action_config.actions` match the phrasing a user would naturally trigger.
- Confirm that the objects the user references by name or pronoun are listed in `action_config.objects`.
- If the user is using pronouns such as `"that"` or `"it"`, confirm that `current_attention_object` is set to a valid object name before the turn. See [Update scene context and attention](update-scene-and-attention.md).

**Verify:** After making the corrections, send a request that should trigger the configured action verb on the named object. An `action-response` event with a non-empty `actions` array should arrive alongside the spoken response.

## update-scene-metadata does not grant new action targets

**Symptom:** Objects listed in `update-scene-metadata` are not appearing as targets in `action-response` events.

**Cause:** `update-scene-metadata` is descriptive only. Objects in scene metadata are not added to the authoritative action target list. Only objects declared in `action_config.objects` at connect time can appear as `target` values in `action-response`.

**Fix:** Disconnect and reconnect with an updated `action_config` that includes the new object in `objects`.

{% hint style="warning" %}
This is the most frequent misconception when integrating character actions. The separation between `action_config` (authoritative affordances) and `update-scene-metadata` (descriptive context) is intentional. Sending `update-scene-metadata` cannot expand the allowed action target set.
{% endhint %}

**Verify:** After reconnecting with the updated `action_config`, confirm that the new object's `name` appears as a `target` in `action-response` events when the user requests an action on it.

## current_attention_object update is rejected

**Symptom:** Sending `context-update` with a `current_attention_object` value causes an error or the attention object does not change.

**Cause:** The value does not match any `name` in the `action_config.objects` list for this session. The server validates `current_attention_object` against that list on every update.

**Fix:** Ensure the string you pass as `current_attention_object` exactly matches the `name` field of an object declared in `action_config.objects` at connect time. Object names are case-sensitive.

**Verify:** Log the object names from your `action_config` and compare them character-by-character with the value you are sending in `context-update`.

## action-response targets do not resolve to scene entities

**Symptom:** `action-response` events arrive with valid-looking `name` and `target` values but your client cannot find the corresponding scene entity.

**Cause:** The `target` value in `action-response` is the `name` string from `action_config.objects` or `action_config.characters`. If your local object map uses different keys, the lookup fails.

**Fix:** Maintain a local map from each object's `name` (as declared in `action_config`) to your runtime entity or game object. Look up `action.target` in that map when dispatching each action.

**Verify:** Log the resolved `action.target` value and confirm it matches the `name` string in your local object map. A successful lookup confirms the mapping is correct.

{% content-ref url="how-character-actions-work.md" %}
[How character actions work](how-character-actions-work.md)
{% endcontent-ref %}

{% content-ref url="configure-actions.md" %}
[Configure actions on connect](configure-actions.md)
{% endcontent-ref %}
