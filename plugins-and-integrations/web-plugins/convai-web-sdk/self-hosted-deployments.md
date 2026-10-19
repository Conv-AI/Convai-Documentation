---
title: Connect to a self-hosted deployment
description: Point the Web SDK at your own Convai deployment instead of Convai's hosted service, set every host it calls, and keep requests and API keys inside your network.
last_reviewed: "2.0.1"
icon: server
---

Point the Web SDK at a Convai deployment you run yourself, such as an on-premises or private-cloud install, instead of Convai's hosted service. Use this page when your character runs somewhere other than `api.convai.com`, or when the browser must not reach Convai's public hosts.

The SDK does not use one base URL. It talks to several services, and on Convai's hosted service each one has its own host. Set each one you use to the matching host in your deployment.

## Prerequisites

- The Convai Web SDK 2.0 or later. If you use the prebuilt chat widget, `@convai/web-widget` installed next to it.
- The public URL of each service in your deployment. Your deployment's administrator can provide them.

## Set the hosts

| Option | Service | Hosted default | What calls it |
|---|---|---|---|
| `url` | Core service (realtime) | `https://realtime-api.convai.com` | `connect()`, which posts to `{url}/connect` |
| `characterInfoUrl` | Character info | `https://api.convai.com` | The chat widget from `@convai/web-widget`, which looks up the character's name and avatar with `POST /character/get` |
| `characterApiUrl` | Character REST platform | `https://api2.convai.com` | `client.characterVersions` |
| `interactionApiUrl` | Interaction API | none | The SSE transport. See [Chat over the SSE transport](sse-transport.md). |

Pass them in the same configuration object as your credentials. It works the same with `new ConvaiClient(...)` from `@convai/web-sdk/core` and with `useConvaiClient(...)` in React.

```ts
import { ConvaiClient } from '@convai/web-sdk/core';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  url: 'https://realtime-api.example.com',
  characterInfoUrl: 'https://api.example.com',
  characterApiUrl: 'https://api2.example.com',
});

await client.connect();
```

Replace the `example.com` hosts with your deployment's hosts. Use an origin only, with no path and no trailing route such as `/connect`.

You do not configure LiveKit. The core service returns the LiveKit room URL in its `/connect` response, so setting `url` is enough for the WebRTC transport. On the WebSocket transport, the client uses `wss://` whenever your page or `url` is served over HTTPS.

## Set characterInfoUrl even if the chat looks right

The SDK makes no request to this host itself; it stores the value on the client as `client.characterInfoUrl`, and the chat widget from `@convai/web-widget` reads it from there. If you leave `characterInfoUrl` unset, the widget sends its character lookup to `https://api.convai.com`, and your API key goes with that request. On a restricted network, that is a failed request plus a credential sent to a host outside your network.

This failure is hard to spot. The widget still works without the lookup. It shows the fallback name `Convi` and no avatar, so a missing setting looks like a cosmetic glitch rather than an error. If your widget header shows `Convi` instead of your character's name, check this setting first.

The lookup authenticates with the `CONVAI-API-KEY` header when you pass `apiKey`, or `API-AUTH-TOKEN` when you pass `authToken`. Configure your deployment's `POST /character/get` to accept the same header. SDK versions up to 1.9.2 sent the API key as `X-API-Key`, which self-hosted deployments reject with `401`.

`characterInfoUrl` and `characterApiUrl` are separate options because they are separate services. The Character REST platform does not serve `/character/get`, so one value cannot be used for both.

## Set the hosts for the other APIs

Some parts of the SDK are created outside the client and take their own host:

- **Long-term memory.** Pass your deployment's API origin as the fourth argument: `new MemoryManager(apiKey, characterId, endUserId, 'https://api.example.com')`. It defaults to `https://api.convai.com`. See [Use long-term memory](long-term-memory.md).
- **Published text chat.** Pass both the publication API origin and the core origin, for example `loadPublishedChatSession(publicationId, 'https://api.example.com')` and `connectWithPublicationGrant(launchToken, { url: 'https://realtime-api.example.com' })`. See [Connect to a published text chat](published-text-chat.md).

## Connect to a LiveKit server without TURN

The client defaults to `iceTransportPolicy: 'relay'`, which sends media only through a TURN server. Convai's hosted LiveKit provides one. If your LiveKit deployment has no TURN server, set `iceTransportPolicy: 'all'` so the browser can also use direct connections:

```ts
const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  url: 'https://realtime-api.example.com',
  iceTransportPolicy: 'all',
});
```

The SSE and WebSocket transports do not use WebRTC, so they ignore this option.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| The widget header shows `Convi` and no avatar. | `characterInfoUrl` is unset or wrong, so the character lookup failed. | Set `characterInfoUrl` to your deployment's API origin. |
| `POST {characterInfoUrl}/character/get` returns `401`, on SDK 1.9.2 or earlier. | Those versions send the API key as `X-API-Key`, and your deployment expects `CONVAI-API-KEY`. | Upgrade the SDK. |
| A request to `api.convai.com` appears in the browser's network log. | One of the options on this page is unset. | Check the request's path against the table above and set the matching option. |
| The first connection fails with `v1 RTC path not found. Consider upgrading your LiveKit server version`. | Your LiveKit server is older than the `livekit-client` 2.x that the SDK uses. | Upgrade the LiveKit server. No SDK version changes this. |
| Connecting with a `characterVersion` fails with `503 Character version resolution is unavailable`. | Your deployment does not resolve character versions. | Omit `characterVersion`. See [Connect to a character version](character-versioning.md). |
| WebRTC connects but no audio flows, on a LiveKit server without TURN. | The default `relay` policy allows only TURN connections. | Set `iceTransportPolicy: 'all'`. |

## API reference

| Option | Type | Default | Description |
|---|---|---|---|
| `url` | `string` | `https://realtime-api.convai.com` | Origin of the core service. The client posts to `{url}/connect`. |
| `characterInfoUrl` | `string` | `https://api.convai.com` | Origin that serves `POST /character/get`, used by the `@convai/web-widget` chat widget for the character's name and avatar. Read it back as `client.characterInfoUrl`. |
| `characterApiUrl` | `string` | `https://api2.convai.com` | Origin of the Character REST platform, used by `client.characterVersions`. |
| `interactionApiUrl` | `string` | none | SSE endpoint. Setting it selects the SSE transport when `transport` is omitted. |
| `iceTransportPolicy` | `"relay" \| "all"` | `"relay"` | WebRTC ICE policy. Use `"all"` for a LiveKit server without TURN. |
