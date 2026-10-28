---
title: Troubleshoot long-term memory
description: Diagnose identity, character settings, connection status, and memory requests while keeping backend behavior and deletion completion separate.
last_reviewed: "5.0.0-preview"
---

Start with the identity and status reported for the current connection, then inspect the character's settings and stored records. A connection, a memory request, and a recalled fact establish different things.

## Check the connected identity and status

In Play mode, inspect `ConvaiManager` **End User** and **Memory**. In code, read `CurrentEndUserId` and `CurrentLongTermMemoryStatus`. Do not instantiate a new default provider to diagnose a connection that may use a custom provider or explicit options.

| Status | Meaning and next check |
| --- | --- |
| `Active` | The connection reported active memory. Check the intended character/user records and account availability if recall is unexpected. |
| `SkippedNoEndUser` | The connection reported no end-user identity for memory. Supply a stable ID if persistence is needed. |
| `NotReported` | No status was reported. This includes disconnected states and responses from multi-character/group paths that omit it; it does not establish that memory is disabled. |

Use **See What They Remember** to inspect the reported user and addressed character. Keep identifiers, metadata, and memory text out of public logs and screenshots.

## Resolve connection errors

| Code | Action |
| --- | --- |
| `connection.connect_end_user_id_required` | Supply a valid stable ID or deliberately configure the character's requirement as Optional. |
| `connection.connect_ltm_end_user_limit_reached` | Check account memory end-user availability with the account/service owner. Client changes do not grant more capacity. |
| `connection.connect_ltm_not_configured` | Check character memory settings and service configuration with the owner. |

A blank identity is not a universal anonymous-memory mode. **Required** and **Optional** express different connection contracts; see [Configure the end-user ID requirement](configure-end-user-id-requirement.md).

## Diagnose missing or unexpected memories

| Symptom | Check |
| --- | --- |
| A returning user appears new | Compare the resolved identity privately; account changes, device IDs, or cleared preferences can produce another ID. |
| The display name differs | Typed `EndUserName` takes precedence, followed by metadata `name`, then the player's display-name fallback. Metadata `name` must be a string. |
| Connection fails before a request | IDs are limited to 512 UTF-16 code units and display names to 255; metadata must serialize to JSON and must not have duplicate keys after trimming. |
| Memory setting appears unchanged | Read it back; a pinned character version retains that version's enabled setting, while the ID requirement applies across versions. |
| A session ended but no new record appears | The client does not specify extraction timing or guarantee every utterance becomes a memory. Inspect service results and reproduce with the backend owner. |
| Stored facts exist but a response omits them | Record storage and conversational recall are separate checks. Reproduce in a fresh session with the same pair. |
| A bulk deletion returned but records remain | Check again; the API contract permits background deletion. Preserve failure details and remaining counts. |
| Memories disappeared after deactivation | Deactivation makes old memories unavailable through that user; it does not prove they were erased. |

## Handle REST errors

Memory management calls throw `ConvaiRestException`. Inspect `Category`, `StatusCode`, and `StatusCodeInt` for classification. `RequestTraceId` and `RetryAfter` may be absent; use available trace IDs when reporting a failed request.

| Error/category | Response |
| --- | --- |
| 400 or 422 / `BadRequest` | Correct the identifiers, request body, or configuration before retrying. |
| 401 / `Unauthorized` | Check credentials in the trusted tool. |
| 403 / `Forbidden` | Check character ownership and account permission. |
| 404 / `NotFound` | Check the user, character, and record scope. |
| 409 / `Conflict` | Read current state and resolve the reported conflict. |
| 429 / `RateLimited` | Honor `RetryAfter` when supplied and retry with a bounded backoff. |
| `Timeout` or `ServerError` | Retry reads with a bounded delay; inspect state before repeating a mutation whose result is unknown. |

Always support cancellation. Do not retry every error indefinitely, and do not turn a timeout into a claim that a mutation failed to reach the service.

## Report a reproducible issue

Include the SDK revision, platform, connection status, sanitized error category/code, available request trace ID, operation name, and whether the problem occurred on connect, record inspection, or recall. Share identity and memory content only through an appropriate private support channel when required.

## Next steps

{% content-ref url="end-user-identity.md" %}
[End-user identity](end-user-identity.md)
{% endcontent-ref %}
{% content-ref url="long-term-memory-window.md" %}
[Inspect and manage long-term memories](long-term-memory-window.md)
{% endcontent-ref %}
