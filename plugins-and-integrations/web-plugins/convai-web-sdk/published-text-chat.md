---
title: Connect to a published text chat
description: Start a credential-free, text-only chat with a published Convai character from a single-use launch grant, in React, plain TypeScript or a copy/paste embed.
last_reviewed: "2.0.0"
icon: comments
---

Let a visitor chat with a published character without putting an API key, a character ID or any reusable credential in the browser. Use this page when you embed a published chat in your own app, or when you are moving a page off the removed `<convai-chat>` element.

## How a published chat works

A published chat is identified by a publication ID. The browser never sees the character's configuration; it works from two public endpoints on the publication API and one exchange with Core:

1. Fetch the public descriptor: the display name, description, image and mode (always `"text"`).
2. Mint a short-lived, single-use launch grant.
3. Pass the grant to `connectWithPublicationGrant()`, which exchanges it with Core and joins the session.

The session is text-only. `client.connectionType` is `"text"` and `client.isPublishedChatSession` is `true`, and the room token Core issues does not allow publishing a microphone or camera track. A grant works once, so every new session needs a new grant.

The helpers for steps 1 and 2 live in `@convai/web-sdk/embed`. They have no transport dependencies and are safe to import on a server.

## Prerequisites

- `@convai/web-sdk` 1.9.0 or later installed.
- A publication ID (a UUID) for a published character.
- The publication API origin and the Core origin for your deployment. The defaults are `https://api.convai.com` and `https://realtime-api.convai.com`; pass both explicitly for staging or on-premises deployments.

## Connect and show the chat

`loadPublishedChatSession()` fetches the descriptor and one grant together. Connect with that grant, label the widget from the descriptor, and give the widget `requestPublicationGrant` so it can start later sessions on its own.

{% tabs %}
{% tab title="React" %}
{% code title="src/PublishedChat.tsx" %}
```tsx
import { useState } from 'react';
import { useConvaiClient } from '@convai/web-sdk/react';
import { ConvaiWidget } from '@convai/web-widget/react';
import {
  getPublishedChatEndpoints,
  loadPublishedChatSession,
  requestPublishedChatGrant,
} from '@convai/web-sdk/embed';

const publicationId = 'PUBLICATION_UUID';
const publicationApiUrl = 'https://api.convai.com';
const coreUrl = 'https://realtime-api.convai.com';

export default function PublishedChat() {
  const client = useConvaiClient();
  const [descriptor, setDescriptor] =
    useState<{ display_name: string; image_url: string | null }>();

  const connect = async () => {
    const session = await loadPublishedChatSession(publicationId, publicationApiUrl);
    setDescriptor(session.descriptor);
    await client.connectWithPublicationGrant(session.launchToken, { url: coreUrl });
  };

  const { launchGrantUrl } = getPublishedChatEndpoints(publicationId, publicationApiUrl);

  return (
    <>
      <button onClick={connect}>Start chat</button>
      <ConvaiWidget
        convaiClient={client}
        defaultVoiceMode={false}
        publishedChatDescriptor={descriptor}
        publishedChatConnectOptions={{ url: coreUrl }}
        requestPublicationGrant={() => requestPublishedChatGrant(launchGrantUrl.toString())}
      />
    </>
  );
}
```
{% endcode %}
{% endtab %}

{% tab title="TypeScript" %}
{% code title="src/main.ts" %}
```typescript
import { ConvaiClient } from '@convai/web-sdk/core';
import { createConvaiWidget } from '@convai/web-widget/vanilla';
import {
  getPublishedChatEndpoints,
  loadPublishedChatSession,
  requestPublishedChatGrant,
} from '@convai/web-sdk/embed';

const publicationId = 'PUBLICATION_UUID';
const publicationApiUrl = 'https://api.convai.com';
const coreUrl = 'https://realtime-api.convai.com';

const client = new ConvaiClient();

const { launchGrantUrl } = getPublishedChatEndpoints(publicationId, publicationApiUrl);
const session = await loadPublishedChatSession(publicationId, publicationApiUrl);
await client.connectWithPublicationGrant(session.launchToken, { url: coreUrl });

createConvaiWidget(document.body, {
  convaiClient: client,
  defaultVoiceMode: false,
  publishedChatDescriptor: session.descriptor,
  publishedChatConnectOptions: { url: coreUrl },
  requestPublicationGrant: () => requestPublishedChatGrant(launchGrantUrl.toString()),
});
```
{% endcode %}
{% endtab %}
{% endtabs %}

`useConvaiClient()` and `new ConvaiClient()` take no configuration here: the grant carries everything the session needs.

The descriptor is safe to display. Character configuration, API keys and other publisher-only data are never returned to the browser.

## Connect without the widget

Mint a grant with `requestPublishedChatGrant()` and connect. Wait for `botReady` before sending the first message.

{% code title="src/headless.ts" %}
```typescript
import { ConvaiClient } from '@convai/web-sdk/core';
import { getPublishedChatEndpoints, requestPublishedChatGrant } from '@convai/web-sdk/embed';

const { launchGrantUrl } = getPublishedChatEndpoints('PUBLICATION_UUID', 'https://api.convai.com');
const launchToken = await requestPublishedChatGrant(launchGrantUrl.toString());

const client = new ConvaiClient();
const unsubscribe = client.on('botReady', () => {
  unsubscribe();
  client.sendUserTextMessage('Hello!');
});

await client.connectWithPublicationGrant(launchToken, { url: 'https://realtime-api.convai.com' });
```
{% endcode %}

## Start a new session

The grant is consumed by the first connection and is not kept for reconnecting. Request a new one for every new session.

The widgets do this through `requestPublicationGrant`. Reset, Disconnect and reopening the panel call it for a fresh grant instead of reusing the spent one. Without it, starting a new session from the widget throws `Published chat widgets require requestPublicationGrant to start a new session`.

`requestPublicationGrant` can call your own backend instead of the publication API, as long as it resolves to the `launch_token` string:

{% code title="src/PublishedChat.tsx" %}
```tsx
<ConvaiWidget
  convaiClient={client}
  publishedChatDescriptor={descriptor}
  requestPublicationGrant={async () => {
    const response = await fetch(`/api/chat/${publicationId}/grant`, { method: 'POST' });
    if (!response.ok) throw new Error('Unable to relaunch published chat');
    return (await response.json()).launch_token;
  }}
/>
```
{% endcode %}

If you build your own interface and keep `PublishedChatConnectOptions` from one session to the next, pass them through `freshPublicationGrantOptions()` before each new session. It keeps `url`, `iceTransportPolicy` and `signal`, and drops `connectAttemptId`, which may be reused only while retrying the same grant.

```typescript
import { freshPublicationGrantOptions, requestPublishedChatGrant } from '@convai/web-sdk/embed';

const launchToken = await requestPublishedChatGrant(launchGrantUrl.toString());
await client.connectWithPublicationGrant(launchToken, freshPublicationGrantOptions(savedOptions));
```

## Retries, cancellation and errors

`connectWithPublicationGrant()` sends each exchange with an idempotency key, `connectAttemptId`. The SDK generates one when you omit it. If the exchange fails with a network error, a 5xx status or a malformed response, the SDK retries once with the same key, so Core replays the same logical connection instead of stranding the grant or creating a second session.

{% hint style="warning" %}
Do not cache a grant, put it in a URL, or retry with a newly minted grant. If you add your own retry on top of the SDK's, pass the same `connectAttemptId` with the same grant.
{% endhint %}

| Situation | What happens |
| --- | --- |
| The grant is not a string of 32 to 512 characters | Throws `A valid publication launch token is required` before any request. |
| The client is already connected or connecting | Throws `Disconnect the current session before connecting again`. Call `disconnect()` first. |
| `signal` aborts | The exchange or room connection is cancelled and torn down, and the promise rejects with an `AbortError`. |
| Core rejects the grant | The promise rejects with the server's message, the `error` event fires with the same error, and `client.requestTraceId` holds the trace ID when the server returned one. |
| The publication API rejects a descriptor or grant request | `loadPublishedChatSession()` or `requestPublishedChatGrant()` rejects with the server's message, or `Unable to load published chat (status)` / `Unable to start published chat (status)`. |

Quote `client.requestTraceId` when you report a failed connection.

## Network and deployment

Published chat connects over WebRTC with `iceTransportPolicy: 'relay'` by default, so traffic goes through a TURN server. Convai-hosted Core has one. For a deployment without TURN, pass `iceTransportPolicy: 'all'`.

```typescript
await client.connectWithPublicationGrant(launchToken, {
  url: 'https://realtime.example.com',
  iceTransportPolicy: 'all',
});
```

## Call the grant helpers from a server

In a browser, `requestPublishedChatGrant()` and `loadPublishedChatSession()` create a per-browser requester ID and send it with each grant request. On a server or during server-side rendering there is no browser to scope it to, so the call throws unless you pass a requester ID for the visitor you are serving: 16 to 128 characters of letters, digits, `_` or `-`.

```typescript
const launchToken = await requestPublishedChatGrant(
  launchGrantUrl.toString(),
  fetch,
  undefined,        // signal
  visitorScopedId,  // one ID per visitor
);
```

{% hint style="warning" %}
Do not reuse one process-wide requester ID for every visitor.
{% endhint %}

## Embed without a build step

For a page that only needs the chat dropped in, use the `<convai-widget>` element from [`@convai/web-widget`](https://www.npmjs.com/package/@convai/web-widget). It mints its own grant per session and labels its header from the public descriptor, so the host page never holds a character ID or a credential.

{% code title="index.html" %}
```html
<script src="https://cdn.jsdelivr.net/npm/@convai/web-widget/v1.js" async></script>

<convai-widget
  publication-id="PUBLICATION_UUID"
  publication-api-url="https://api.convai.com"
  core-url="https://realtime-api.convai.com"
  placement="inline"
  style="display:block;width:100%;height:640px">
</convai-widget>
```
{% endcode %}

Two details matter, and getting either wrong renders nothing:

- Do not add `type="module"` to the script tag. The loader reads `document.currentScript`, which is `null` in a module script.
- Set `placement="inline"` for a panel sized by `style`. Without it, the widget is a floating launcher in the bottom-right corner.

Theming, events and the element's other attributes are documented in the `@convai/web-widget` package.

## Migrate from `<convai-chat>`

Version 1.9.0 removed the `<convai-chat>` element and the `@convai/web-sdk/embed/browser` entry point (`dist/embed/chat-embed-v1.js`). Replace the script tag and the element; the publication attributes stay the same.

{% code title="index.html" %}
```html
<!-- before -->
<script
  type="module"
  src="https://cdn.jsdelivr.net/npm/@convai/web-sdk@X/dist/embed/chat-embed-v1.js"
></script>
<convai-chat
  publication-id="…"
  publication-api-url="…"
  core-url="…"
></convai-chat>

<!-- after -->
<script
  src="https://cdn.jsdelivr.net/npm/@convai/web-widget@X/v1.js"
  async
></script>
<convai-widget
  publication-id="…"
  publication-api-url="…"
  core-url="…"
  placement="inline"
></convai-widget>
```
{% endcode %}

Note that `type="module"` is removed and `placement="inline"` is added. The helpers in `@convai/web-sdk/embed` and `connectWithPublicationGrant()` are unchanged.

## API reference

| Property / Method | Type | Description |
| --- | --- | --- |
| `connectWithPublicationGrant` | `(launchToken: string, options?: PublishedChatConnectOptions) => Promise<void>` | Exchanges a single-use grant with Core and opens a text-only session. |
| `PublishedChatConnectOptions.url` | `string` | Core origin. Defaults to `https://realtime-api.convai.com`. |
| `PublishedChatConnectOptions.iceTransportPolicy` | `RTCIceTransportPolicy` | Defaults to `'relay'`. Use `'all'` only when the deployment has no TURN server. |
| `PublishedChatConnectOptions.signal` | `AbortSignal` | Cancels an in-flight grant exchange or room connection and tears it down. |
| `PublishedChatConnectOptions.connectAttemptId` | `string` | Idempotency key. Generated when omitted; reuse only while retrying the same grant. |
| `client.connectionType` | `'audio' \| 'video' \| 'text' \| null` | `'text'` for a published chat session. |
| `client.isPublishedChatSession` | `boolean` | Whether the client last connected through a publication grant. |
| `client.requestTraceId` | `string \| null` | Server trace ID for the most recent connection request, when provided. |
| `loadPublishedChatSession` | `(publicationId, publicationApiUrl?, fetch?, signal?, requesterId?) => Promise<PublishedChatSession>` | Fetches the public descriptor and one grant. Resolves to `{ descriptor, launchToken }`. |
| `requestPublishedChatGrant` | `(launchGrantUrl, fetch?, signal?, requesterId?) => Promise<string>` | Mints a grant for a new session. Server callers must pass `requesterId`. |
| `getPublishedChatEndpoints` | `(publicationId, publicationApiUrl?) => PublishedChatEndpoints` | Returns validated `descriptorUrl` and `launchGrantUrl`. Throws if the publication ID is not a UUID. |
| `fetchPublishedChatDescriptor` | `(descriptorUrl, fetch?, signal?) => Promise<PublishedChatDescriptor>` | Fetches only the public descriptor. |
| `freshPublicationGrantOptions` | `(options?: PublishedChatConnectOptions) => PublishedChatConnectOptions \| undefined` | Copies the options without `connectAttemptId`, for the start of a new session. |
| `PublishedChatDescriptor` | `{ publication_id, display_name, description, image_url, mode: 'text' }` | Public display data for a publication. |
| `requestPublicationGrant` (widget option) | `() => Promise<string>` | Mints a fresh grant when the widget starts a later session. Required for published chat. |
| `publishedChatConnectOptions` (widget option) | `PublishedChatConnectOptions` | Options the widget passes to `connectWithPublicationGrant()`. |
| `publishedChatDescriptor` (widget option) | `{ display_name, image_url }` | Labels the widget header without a character lookup. |
