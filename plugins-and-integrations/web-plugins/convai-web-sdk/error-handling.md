---
description: >-
  The SDK surfaces errors through four channels. Each has a different scope and
  payload — knowing which one to use for a given scenario is the key to reliable
  apps.
icon: cloud-xmark
---

# Error Handling

<table><thead><tr><th>Channel</th><th>Event</th><th width="286.31640625">When it fires</th></tr></thead><tbody><tr><td>Transport errors</td><td><code>error</code></td><td>Low-level WebRTC / WebSocket exceptions</td></tr><tr><td>Session end</td><td><code>disconnect</code></td><td>Every session end, with a reason code</td></tr><tr><td>Server acknowledgments</td><td><code>serverResponse</code></td><td>After every message you send</td></tr><tr><td>Silent LLM</td><td><code>llmNoResponse</code></td><td>LLM deliberately chose not to respond</td></tr><tr><td>Idle timeout</td><td><code>idleWarning</code></td><td>Server about to disconnect an idle session</td></tr></tbody></table>

***

### `error` event

Fires for low-level transport exceptions. The payload is `unknown` because it wraps whatever the underlying transport threw.

```ts
client.on('error', (err) => {
  if (err instanceof Error) {
    console.error(err.name, err.message);
  } else {
    console.error(err);
  }
});
```

Common causes on the WebRTC transport:

| Code | Meaning                                                                 |
| ---- | ----------------------------------------------------------------------- |
| 1    | `ConnectionError` — permission denied, server unreachable, or cancelled |
| 13   | `NegotiationError` — WebRTC negotiation failed                          |
| 21   | `DeviceUnsupportedError` — microphone or camera not available           |

***

### `disconnect` event

Fires on every session end — intentional or not. The payload is a numeric `DisconnectReason` code.

#### React

```tsx
import { useConvaiClient, DisconnectReasonEnum, getDisconnectReasonMessage } from '@convai/web-sdk';
import { useEffect } from 'react';

function App() {
  const client = useConvaiClient({ apiKey: '...', characterId: '...' });

  useEffect(() => {
    return client.on('disconnect', (reason) => {
      console.log(getDisconnectReasonMessage(reason));

      switch (reason) {
        case DisconnectReasonEnum.CLIENT_INITIATED:
          // User pressed disconnect — nothing to do
          break;

        case DisconnectReasonEnum.SIGNAL_CLOSE:
        case DisconnectReasonEnum.UNKNOWN_REASON:
        case DisconnectReasonEnum.STATE_MISMATCH:
          // Network drop — retry
          retryWithBackoff(() => client.reconnect());
          break;

        case DisconnectReasonEnum.SERVER_SHUTDOWN:
          setTimeout(() => client.reconnect(), 5000);
          break;

        case DisconnectReasonEnum.DUPLICATE_IDENTITY:
          // Another tab / device took over — don't auto-retry
          alert('Session opened in another window.');
          break;

        case DisconnectReasonEnum.JOIN_FAILURE:
          // Config problem — surface to user, don't loop
          alert('Failed to join. Check your API key and character ID.');
          break;
      }
    });
  }, [client]);
}
```

#### Vanilla JS

```ts
import { ConvaiClient, DisconnectReasonEnum, getDisconnectReasonMessage } from '@convai/web-sdk/core';

const client = new ConvaiClient({ apiKey: '...', characterId: '...' });

client.on('disconnect', (reason) => {
  console.log(getDisconnectReasonMessage(reason));

  if (reason !== DisconnectReasonEnum.CLIENT_INITIATED) {
    retryWithBackoff(() => client.reconnect());
  }
});
```

#### Reason code reference

| Code | Enum key              | Meaning                                                                                             | Auto-retry?      |
| ---- | --------------------- | --------------------------------------------------------------------------------------------------- | ---------------- |
| 0    | `UNKNOWN_REASON`      | Network unavailable or browser went offline — this is the most common reason for an unexpected drop | Yes              |
| 1    | `CLIENT_INITIATED`    | User called `disconnect()`                                                                          | No — intentional |
| 2    | `DUPLICATE_IDENTITY`  | Another session with same identity joined                                                           | No — prompt user |
| 3    | `SERVER_SHUTDOWN`     | Server restarting                                                                                   | Yes — with delay |
| 4    | `PARTICIPANT_REMOVED` | Removed via server API                                                                              | No               |
| 5    | `ROOM_DELETED`        | Session closed server-side                                                                          | No               |
| 6    | `STATE_MISMATCH`      | Client/server state diverged                                                                        | Yes              |
| 7    | `JOIN_FAILURE`        | Failed to join — check config                                                                       | No — fix config  |
| 9    | `SIGNAL_CLOSE`        | WebSocket signal channel closed cleanly                                                             | Yes              |

**`UNKNOWN_REASON` vs `SIGNAL_CLOSE`:** Both indicate a network drop and both should trigger a retry. The difference is timing — when the browser goes fully offline (`n +avigator.onLine = false`), LiveKit fires `UNKNOWN_REASON (0)` immediately via its off +line detector before the WebSocket even closes. `SIGNAL_CLOSE (9)` fires when the sig +nal WebSocket itself closes, which requires the network to be partially reachable. In + practice, pulling WiFi or DevTools → Offline always produces `UNKNOWN_REASON`.

The last reason is also available synchronously on `client.state.disconnectReason` — `null` when connected.

***

### `serverResponse` event

The server sends an acknowledgment for **every message your client sends** — `sendUserTextMessage`, `updateContext`, `sendTriggerMessage`, `toggleTts`, etc. Check `status` to know if the server accepted the request.

#### React

```tsx
import type { ServerResponse } from '@convai/web-sdk';
import { useEffect } from 'react';

useEffect(() => {
  return client.on('serverResponse', (res: ServerResponse) => {
    if (res.status === 'error') {
      console.error(`[${res.event_type}] failed: ${res.message}`);
    }

    // context-update includes the current token budget
    if (res.event_type === 'context-update' && res.extras) {
      const { token_count, remaining_tokens, max_tokens } = res.extras;
      console.log(`Context: ${token_count}/${max_tokens} tokens used, ${remaining_tokens} remaining`);
      if (remaining_tokens < 5000) {
        console.warn('Context budget low — consider resetting ephemeral context');
      }
    }
  });
}, [client]);
```

#### Vanilla JS

```ts
import type { ServerResponse } from '@convai/web-sdk/core';

client.on('serverResponse', (res: ServerResponse) => {
  if (res.status === 'error') {
    console.error(`[${res.event_type}] failed: ${res.message}`);
  }

  if (res.event_type === 'context-update' && res.extras) {
    const { token_count, remaining_tokens, max_tokens } = res.extras;
    console.log(`Context: ${token_count}/${max_tokens} tokens used, ${remaining_tokens} remaining`);
  }
});

```

#### Payload shape

```ts
interface ServerResponse {
  event_type: string;                                        // message type you sent
  status: 'success' | 'error' | 'processing' | 'pending';
  message: string | null;                                    // non-null on error
  extras: ServerResponseExtras | null;                       // event-specific data
}
```

For `context-update`, `extras` contains token budget info:

```ts
{
  token_count: number;       // tokens currently used
  max_tokens: number;        // budget ceiling (50 000)
  remaining_tokens: number;  // tokens left before LRU trimming begins
}
```

***

### `llmNoResponse` event

Fires when the LLM deliberately chose not to respond — not an error, but your UI should stop showing a thinking indicator.

```ts
client.on('llmNoResponse', () => {
  hideThinkingIndicator();
});
```

***

### `idleWarning` event

Fires before the server disconnects an idle session. Call `resetIdleTimer()` on any user activity to keep the session alive.

```ts
client.on('idleWarning', ({ remainingSeconds }) => {
  if (remainingSeconds !== null) {
    showBanner(`Session closes in ${remainingSeconds}s due to inactivity`);
  }
  // Reset on any user interaction
  document.addEventListener('click', () => client.resetIdleTimer(), { once: true });
});
```

***

### Reliability patterns

#### Retry with exponential backoff

The SDK does not auto-reconnect. Implement your own backoff on non-intentional disconnects.

```ts
async function retryWithBackoff(
  fn: () => Promise<void>,
  attempts = 3,
  delayMs = 500,
): Promise<void> {
  for (let i = 1; i <= attempts; i++) {
    try {
      return await fn();
    } catch (err) {
      if (i === attempts) throw err;
      await new Promise((r) => setTimeout(r, delayMs * 2 ** (i - 1)));
    }
  }
}

client.on('disconnect', (reason) => {
  if (
    reason !== DisconnectReasonEnum.CLIENT_INITIATED &&
    reason !== DisconnectReasonEnum.DUPLICATE_IDENTITY &&
    reason !== DisconnectReasonEnum.JOIN_FAILURE
  ) {
    retryWithBackoff(() => client.reconnect());
  }
});
```

#### Safe send guard

Check connection state before sending to avoid silent drops.

```ts
function safeSend(client: IConvaiClient, text: string) {
  if (!client.state.isConnected || !client.isBotReady) return;
  client.sendUserTextMessage(text);
}
```

#### Protect media control calls

Audio and video control methods are async and can throw on permission denial.

```ts
async function safeToggleMic(client: IConvaiClient) {
  try {
    await client.audioControls.toggleAudio();
  } catch (err) {
    console.error('Microphone toggle failed:', err);
    // Show a permission prompt or device error message
  }
}
```

#### Always unsubscribe

Every `client.on(...)` call returns an unsubscribe function. Call it on unmount or session teardown.

```tsx
// React
useEffect(() => {
  const unsubs = [
    client.on('error', handleError),
    client.on('disconnect', handleDisconnect),
    client.on('serverResponse', handleServerResponse),
  ];
  return () => unsubs.forEach((u) => u());
}, [client]);
```

```ts
// Vanilla
const unsubError = client.on('error', handleError);
const unsubDisconnect = client.on('disconnect', handleDisconnect);

// On cleanup
unsubError();
unsubDisconnect();
```

***

### Quick reference — which channel to use

| Scenario                           | Channel                                      |
| ---------------------------------- | -------------------------------------------- |
| Network dropped mid-session        | `disconnect` → `SIGNAL_CLOSE` (9)            |
| User pressed disconnect            | `disconnect` → `CLIENT_INITIATED` (1)        |
| Same user opened another tab       | `disconnect` → `DUPLICATE_IDENTITY` (2)      |
| Server maintenance                 | `disconnect` → `SERVER_SHUTDOWN` (3)         |
| `updateContext` rejected by server | `serverResponse` → `status: 'error'`         |
| Dynamic context token budget low   | `serverResponse` → `extras.remaining_tokens` |
| WebRTC negotiation failed          | `error` — code 13                            |
| Microphone permission denied       | `error` — code 1 (sub-reason 0)              |
| LLM decided not to reply           | `llmNoResponse`                              |
| Session about to time out          | `idleWarning`                                |
