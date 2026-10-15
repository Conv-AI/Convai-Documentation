---
title: Handle errors and disconnects
description: Catch connection failures, react to dropped sessions with your own reconnect logic, and read the acknowledgments Convai returns for each message.
last_reviewed: "1.9.4"
icon: cloud-xmark
---

Handle the failures a Convai Web SDK session can hit: a connection that never opens, a session that drops, and a message that Convai rejects. Use this page when you move from a prototype to an application that has to recover on its own.

## Where failures surface

| Failure | Where it surfaces |
|---|---|
| `connect()` cannot open a session | The `connect()` promise rejects, and the `error` event fires with the same error. |
| The character never signals that it is ready | The `error` event fires (LiveKit transport only). |
| The session ends, intentionally or not | The `disconnect` event fires with a reason code. |
| Convai accepts or rejects a message you sent | The `serverResponse` event fires. |
| The character chose not to answer | The `llmNoResponse` event fires. |
| The session is about to time out for inactivity | The `idleWarning` event fires. |

## Catch connection failures

Wrap `connect()` in `try`/`catch`. The SDK emits `error` with the same value it rethrows, so handle it in one place to avoid reporting it twice.

```typescript
try {
  await client.connect();
} catch (err) {
  showError(err instanceof Error ? err.message : String(err));
}
```

`connect()` throws these errors before any request is sent:

| Message | Cause |
|---|---|
| `No configuration provided. Pass config to connect() or store it in the client` | No configuration was passed to the constructor or to `connect()`. |
| `Either apiKey or authToken is required, and characterId is required` | A credential or the character ID is missing. |

When Convai answers `/connect` with an error status, the error message is the `message`, `error`, or `detail` field of the response body. A validation error that lists several problems is joined into one message as `field: problem; field: problem`. A response without a readable body produces `HTTP <status>` followed by the body text.

The `error` event payload is typed `unknown`, because it carries whatever failed. Narrow it before reading properties:

```typescript
client.on('error', (err: unknown) => {
  console.error(err instanceof Error ? err.message : err);
});
```

On the LiveKit transport, the SDK waits for the character to signal readiness after connecting. If no signal arrives in 45 seconds, `error` fires with `bot-ready not received within 45000ms`. The session stays connected; disconnect and connect again to recover.

## React to disconnects

The `disconnect` event receives a `DisconnectReason` code. When the transport gives no reason, the SDK reports `0`. A `disconnect()` call on the WebSocket transport reports `1`. The last reason is also on `client.state.disconnectReason`, which is `null` while connected.

`getDisconnectReasonMessage()` turns a code into text. Both it and `DisconnectReasonEnum` are exported from `@convai/web-sdk/core`, `@convai/web-sdk/react`, and `@convai/web-sdk/vanilla`.

| Code | `DisconnectReasonEnum` key | `getDisconnectReasonMessage()` text |
|---|---|---|
| `0` | `UNKNOWN_REASON` | `Network unavailable or unknown cause` |
| `1` | `CLIENT_INITIATED` | `User disconnected` |
| `2` | `DUPLICATE_IDENTITY` | `Another client with same identity joined` |
| `3` | `SERVER_SHUTDOWN` | `Server is shutting down` |
| `4` | `PARTICIPANT_REMOVED` | `Removed by RemoveParticipant API` |
| `5` | `ROOM_DELETED` | `Room ended via DeleteRoom API` |
| `6` | `STATE_MISMATCH` | `State mismatch` |
| `7` | `JOIN_FAILURE` | `Failed to join` |
| `8` | `MIGRATION` | `Participant moved to different room` |
| `9` | `SIGNAL_CLOSE` | `Signal connection closed` |

Any other code returns `Disconnected`, and `null` returns `Connected`.

## Reconnect with backoff

The SDK never reconnects on its own: it configures its LiveKit room with a policy that refuses every retry. Reconnect from your `disconnect` handler when the reason is not intentional.

`reconnect()` connects again with the last configuration, including the character session ID Convai returned, so the conversation resumes. It throws `No stored config available for reconnection` if `connect()` never ran with a configuration.

```typescript
import { DisconnectReasonEnum, getDisconnectReasonMessage } from '@convai/web-sdk/core';

async function retryWithBackoff(fn: () => Promise<void>, attempts = 3, delayMs = 500) {
  for (let i = 1; i <= attempts; i++) {
    try {
      return await fn();
    } catch (err) {
      if (i === attempts) throw err;
      await new Promise((r) => setTimeout(r, delayMs * 2 ** (i - 1)));
    }
  }
}

const doNotRetry: number[] = [
  DisconnectReasonEnum.CLIENT_INITIATED,
  DisconnectReasonEnum.DUPLICATE_IDENTITY,
  DisconnectReasonEnum.JOIN_FAILURE,
];

client.on('disconnect', (reason: number) => {
  console.log(getDisconnectReasonMessage(reason));
  if (!doNotRetry.includes(reason)) {
    void retryWithBackoff(() => client.reconnect());
  }
});
```

{% hint style="warning" %}
`disconnect()` also fires `disconnect` with `CLIENT_INITIATED`. Exclude that code, or every intentional disconnect starts a reconnect.
{% endhint %}

## Check that messages were accepted

Most send methods return `void` and do nothing when the transport is not ready, without throwing. This covers `sendUserTextMessage()`, `sendTriggerMessage()`, `sendInterruptMessage()`, `updateContext()`, `updateDynamicInfo()`, `updateTemplateKeys()`, `updateSceneMetadata()`, `toggleTts()`, `toggleStt()`, and `resetIdleTimer()`. Send only after `botReady` has fired:

```typescript
function safeSend(text: string) {
  if (!client.state.isConnected || !client.isBotReady) return;
  client.sendUserTextMessage(text);
}
```

`sendActionResult()` is the exception: it throws when the session is not ready or the result is invalid. See [Handle character actions](actions.md).

Convai acknowledges messages with the `serverResponse` event. `event_type` is the message type you sent, `status` is `success`, `error`, `processing`, or `pending`, `message` is a description or `null`, and `extras` holds event-specific data or `null`.

```typescript
import type { ServerResponse } from '@convai/web-sdk/core';

client.on('serverResponse', (res: ServerResponse) => {
  if (res.status === 'error') {
    console.error(`${res.event_type} failed: ${res.message}`);
  }
  if (res.event_type === 'context-update' && res.extras) {
    const { token_count, max_tokens, remaining_tokens } = res.extras;
    console.log(`Context tokens: ${token_count}/${max_tokens}, ${remaining_tokens} left`);
  }
});
```

## Handle silent turns and idle sessions

`llmNoResponse` fires when the character deliberately does not answer a turn. Clear any thinking indicator when it fires.

`idleWarning` fires before Convai closes an inactive session. Its payload is `{ remainingSeconds }`, a number or `null`. Call `resetIdleTimer()` on end-user activity to keep the session open.

```typescript
client.on('llmNoResponse', () => hideThinkingIndicator());

client.on('idleWarning', ({ remainingSeconds }: { remainingSeconds: number | null }) => {
  if (remainingSeconds !== null) {
    showBanner(`Session closes in ${remainingSeconds} seconds`);
  }
});

document.addEventListener('pointerdown', () => client.resetIdleTimer());
```

## Guard media controls

Microphone, camera, and screen-share methods are asynchronous and reject when the browser denies a permission or a device is unavailable. Catch the rejection and show a message:

```typescript
try {
  await client.audioControls.toggleAudio();
} catch (err) {
  showError('Microphone unavailable. Check the browser permission.');
}
```

## Next steps

{% content-ref url="event-reference.md" %}
[Web SDK event reference](event-reference.md)
{% endcontent-ref %}

{% content-ref url="vanilla-typescript/convaiclient-core-api.md" %}
[ConvaiClient reference](vanilla-typescript/convaiclient-core-api.md)
{% endcontent-ref %}

{% content-ref url="auth-tokens.md" %}
[Connect with an auth token](auth-tokens.md)
{% endcontent-ref %}
