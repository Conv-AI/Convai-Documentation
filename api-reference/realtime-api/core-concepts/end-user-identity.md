---
title: End-user identity
description: "Understand end-user identity fields in the Realtime API: when they are required, how the server processes them, and what they enable."
last_reviewed: "2026-06-11"
---

End-user identity lets you associate a Realtime API session with a specific user in your product. Supplying an `end_user_id` enables per-user conversation history, Long Term Memory (LTM), and personalization. When `end_user_id` is absent, the session runs anonymously and no per-user state is created or retrieved.

## Identity fields

Both fields are supplied in the `POST /connect` request body and are echoed back in the `ConnectResponse`.

| Field | Type | Default | Description |
|---|---|---|---|
| `end_user_id` | `string` or `null` | `null` | Your application's identifier for the end user. The server strips leading and trailing whitespace before storing the value. Required when the character has LTM enabled. |
| `end_user_metadata` | `object` or `null` | `null` | Arbitrary JSON metadata for the end user. The key `name` must be a string or `null` if present. Silently ignored when `end_user_id` is absent. |

## Long Term Memory requirement

When a character has Long Term Memory enabled, `end_user_id` is mandatory. If the field is absent or empty, `POST /connect` returns HTTP `400` with the following detail:

```text
Missing end_user_id. end_user_id is required when the character has Long Term Memory enabled. Provide end_user_id or disable Long Term Memory.
```

The session is not created. Supply a non-empty `end_user_id` or disable LTM on the character in the Convai dashboard before retrying.

{% hint style="warning" %}
A `400` response at `/connect` with the message above means `end_user_id` is missing and the character requires it. The error comes from the server-side LTM check, not from request validation.
{% endhint %}

## Speaker resolution and personalization

When `end_user_id` is provided, Convai creates or retrieves an existing speaker record for that user under your account. This speaker record is what makes per-user features work.

- **Long Term Memory:** The character recalls facts from previous conversations with this user.
- **Personalization:** The character addresses the user by name when `end_user_metadata.name` is set.
- **Transcript attribution:** Transcriptions are labeled with the speaker's name and identifier.

The resolved speaker information is stored with the session and carried through the conversation. The `end_user_id` and `end_user_metadata` values are echoed back in the `ConnectResponse` so your application can confirm what the server recorded.

## Metadata rules

`end_user_metadata` follows two enforced rules.

**Silent ignore without end_user_id.** If `end_user_id` is absent, the server discards `end_user_metadata` without returning an error. The session proceeds anonymously. This means setting `end_user_metadata` alone has no effect.

**Name field type constraint.** If `end_user_metadata` contains the key `"name"`, its value must be a string or `null`. Any other type causes `POST /connect` to return HTTP `422`.

```json
{
  "end_user_id": "user-abc123",
  "end_user_metadata": {
    "name": "Alex",
    "department": "Engineering",
    "training_level": 2
  }
}
```

Keys other than `"name"` are stored with the speaker record and can be used to tag a session with any application-specific metadata you find useful. There is no enforced schema beyond the `"name"` type constraint.

## Related concepts

{% content-ref url="session-lifecycle.md" %}
[Session lifecycle](session-lifecycle.md)
{% endcontent-ref %}

{% content-ref url="rtvi-protocol.md" %}
[RTVI message protocol](rtvi-protocol.md)
{% endcontent-ref %}
