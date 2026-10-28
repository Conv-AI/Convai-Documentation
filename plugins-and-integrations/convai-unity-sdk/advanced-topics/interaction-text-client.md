---
title: Interaction text client
description: Reference the opt-in text interaction client, its explicit identity and session fields, response validation, streaming callbacks, and disposal behavior.
last_reviewed: "5.0.0-preview"
---

`Convai.CoreApi.ConvaiInteractionClient` is an opt-in text client for a specific JSON and server-sent event contract. It is separate from the room-based Unity conversation flow. You must obtain the intended endpoint and credential from your service configuration; the class does not discover them or establish account access.

## Construction and ownership

The constructor accepts `Uri endpoint`, `string credential`, optional `IConvaiApiTransport transport`, and optional `TimeSpan timeout`. It requires an absolute HTTP or HTTPS URI, a non-empty credential, and a positive timeout. The default timeout is `30` seconds. Requests use HTTP POST with `Authorization: Bearer`, a JSON body, and the appropriate Accept header.

Use an HTTPS endpoint for deployed traffic. Supplying an endpoint and bearer string satisfies local constructor validation only; it does not prove that the service accepts that credential.

The client creates and owns a transport when none is supplied. `Dispose()` cancels its active operations and disposes only a transport it created. Calls after disposal throw `ObjectDisposedException`.

## Request fields

`ConvaiInteractionTextRequest` requires non-empty `characterId` and `text` arguments:

| Argument | Wire field | Client behavior |
|---|---|---|
| `characterId` | `character_id` | Required; passed as supplied. |
| `text` | `text` | Required; passed as supplied. |
| `characterSessionId` | `character_session_id` | Blank becomes null. Supply the previous character session to request continuation. |
| `endUserId` | `end_user_id` | Blank becomes null. No device-identity fallback is added. |
| `endUserMetadata` | `end_user_metadata` | Copied only when a non-empty end-user ID and non-empty metadata are supplied. |

Identity and session are explicit on each call. The client rejects a response that changes a requested character session. These checks do not define server retention or memory policy.

## JSON response path

`SendTextAsync(request, cancellationToken)` returns `Task<ConvaiInteractionResult>`. It requires successful transport status, a JSON object, non-empty `character_session_id` and `session_id`, an event list with a terminal semantic event, and a text field. A terminal event is `bot-turn-completed` or `llm-no-response`. An error event or an event after completion fails the operation.

The result exposes the execution and character session identifiers, terminal event, text, optional request trace ID, and event data. Keep returned text and identity out of diagnostic logs unless your application explicitly permits that content.

## Streaming response path

`StreamTextAsync(request, Action<ConvaiApiSseEvent> onEvent, cancellationToken)` requires a non-null callback and a transport whose capabilities include incremental SSE, or server-sent events. It validates this sequence:

1. A `session` event establishes the character session.
2. Incremental events precede a terminal semantic event.
3. A final `done` event confirms the same character session and supplies the execution session ID.

An early end, repeated session event, error event, or event after completion fails the call. The method completes only after semantic completion and `done`. Consume text and actions incrementally in your callback; the result does not retain the whole stream for you.

Callbacks run on the transport callback context. Do not assume they can call Unity scene APIs directly; marshal application UI work to the Unity main thread. A callback exception cancels the request and is rethrown from the operation.

## Error handling

HTTP failures become `ConvaiApiException`. Invalid response shape or event order uses the Contract error category; a stream error event uses Server. Caller cancellation and client disposal cancel pending work. This reference describes the client validation contract, not endpoint availability, entitlement, or production service qualification.

{% content-ref url="../authentication/README.md" %}
[Authentication](../authentication/README.md)
{% endcontent-ref %}
