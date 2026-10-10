---
title: Configure an on-premise deployment
description: Point the Pixel Streaming Embed package at your own session service and stream servers instead of Convai's, for on-premise and self-hosted deployments.
last_reviewed: "0.7.1"
icon: building
---

Route the embed's session request and its stream to services you host, with the `serviceUrls` option. Use this page when an experience runs on your own Pixel Streaming servers. At the end, the embed requests its session from your service and loads the stream from your servers.

## Prerequisites

- An embed that already works against Convai. See [Embed an experience in a React TypeScript app](react-typescript.md) or [Embed an experience with a script tag](cdn-umd-script.md).
- A session service and a stream server that implement the requests described on this page.

## How the embed reaches its services

The embed makes two requests. `serviceUrls` replaces the base URL of each one:

| Key | Default | Request the embed makes |
|---|---|---|
| `sessionFetch` | `https://api.convai.com` | `POST <sessionFetch>/xp/streams/viewPublishedExperience` to create a session |
| `pixelStreamBase` | Convai's stream servers | Loads the stream page for the session in the iframe, by default from `https://x.convai.com/stream-v2/<sessionId>/` |

`sessionFetch` is a base URL: the embed appends `/xp/streams/viewPublishedExperience` to it.

## Set the service URLs

{% tabs %}
{% tab title="React" %}
```tsx
<PixelStreamComponent
  expId="YOUR_EXPERIENCE_ID"
  serviceUrls={{
    sessionFetch: 'https://sessions.example.com',
    pixelStreamBase: 'https://stream.example.com',
  }}
/>
```
{% endtab %}

{% tab title="JavaScript" %}
```js
const experience = new PixelStreamCore.PixelStreamClient({
  container: document.getElementById('experience'),
  expId: 'YOUR_EXPERIENCE_ID',
  serviceUrls: {
    sessionFetch: 'https://sessions.example.com',
    pixelStreamBase: 'https://stream.example.com/stream-v2/',
  },
});
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
The React component and the framework-free client build the stream URL differently. `PixelStreamComponent` loads `<pixelStreamBase>/stream-v2/<sessionId>/`. `PixelStreamClient` loads `<pixelStreamBase><sessionId>/`, with no separator, so end its `pixelStreamBase` with the path to the session, including the trailing `/`.
{% endhint %}

## Implement the session service

The embed sends a JSON body to the session service:

```json
{
  "experience_id": "YOUR_EXPERIENCE_ID",
  "allocate_server": false,
  "end_user_id": "user-123"
}
```

`end_user_id` is present only when the embed has an `endUserId`. When the embed has an `authToken`, the request carries it in the `API-AUTH-TOKEN` header.

The embed reads the response this way:

| Response | Result |
|---|---|
| Status `200` with `{ "session": { "session_id": "<id>" } }` | The embed loads the stream page for `<id>`. |
| Status `200` with `{ "status": "retry", "message": "<text>" }` | The embed shows its error screen. |
| Any other status, with `{ "ERROR": "<text>" }` | The embed shows its error screen. |

After the stream page loads, the embed posts it a JSON string, `{"type":"SESSION_ID","sessionId":"<id>"}`, and, when `endUserId` is set, an `END_USER_ID` message carrying `end_user_id` and `end_user_metadata`.

## Verify the deployment

Load the page and open the browser's network panel.

{% hint style="success" %}
The session request goes to your `sessionFetch` URL, and the iframe loads from your `pixelStreamBase` URL.
{% endhint %}

## Next steps

{% content-ref url="api-reference.md" %}
[Pixel Streaming Embed API reference](api-reference.md)
{% endcontent-ref %}
