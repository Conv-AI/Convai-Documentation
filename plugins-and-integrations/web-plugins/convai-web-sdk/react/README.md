---
title: Get started with React
description: Install the Convai Web SDK in a React app and add a ready-made chat and voice widget, with optional camera and screen sharing for your character.
last_reviewed: "1.9.4"
icon: react
---

Add a Convai character to a React app with the `useConvaiClient` hook and the `ConvaiWidget` component. Use this page when setting up the React bindings for the first time. At the end, the page shows a widget button that opens a voice and text conversation with your character.

## Prerequisites

- A React 18 or 19 app with a bundler. `react` and `react-dom` 18 or 19 are peer dependencies of the SDK.
- A Convai account and an API key from <code class="expression">space.vars.dashboard_url</code>.
- The ID of the character to connect to.

## Install the package

The React bindings ship in `@convai/web-sdk` and are imported from the `@convai/web-sdk/react` subpath. There is no separate React package.

{% tabs %}
{% tab title="npm" %}
```bash
npm install @convai/web-sdk
```
{% endtab %}

{% tab title="pnpm" %}
```bash
pnpm add @convai/web-sdk
```
{% endtab %}

{% tab title="yarn" %}
```bash
yarn add @convai/web-sdk
```
{% endtab %}
{% endtabs %}

## Add the widget

`useConvaiClient` creates one client for the component and stores the config. `ConvaiWidget` renders the conversation UI and connects with that stored config when someone first selects its button, so the browser asks for the microphone only after a user action.

{% code title="src/App.tsx" %}
```tsx
import { useConvaiClient, ConvaiWidget } from '@convai/web-sdk/react';

export default function App() {
  const convaiClient = useConvaiClient({
    apiKey: 'YOUR_API_KEY',
    characterId: 'YOUR_CHARACTER_ID',
    endUserId: 'user-123',
  });

  return <ConvaiWidget convaiClient={convaiClient} />;
}
```
{% endcode %}

The widget plays the character's voice, captures the microphone in voice mode, and shows the conversation as it streams.

`endUserId` is optional. Pass a stable, unique ID for each person, such as a UUID, to enable long-term memory and per-user analytics. Without it the session is anonymous. See [Use long-term memory](../long-term-memory.md).

{% hint style="danger" %}
An API key in client code is readable by anyone who opens the page. For a public page, create a short-lived auth token on your server and pass `authToken` instead of `apiKey`. See [Connect with an auth token](../auth-tokens.md).
{% endhint %}

## Enable camera and screen sharing

Set `enableVideo: true` to connect with the `"video"` connection type, which carries audio, camera video, and screen share. `startWithVideoOn` turns the camera on at connect; it defaults to `false`. The widget shows camera and screen share buttons in its settings tray when the connection type is `"video"`; hide either with `showVideo={false}` or `showScreenShare={false}`.

```tsx
const convaiClient = useConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  enableVideo: true,
  startWithVideoOn: false,
});

return <ConvaiWidget convaiClient={convaiClient} showVideo showScreenShare />;
```

## Verify the integration

Start your dev server and open the page. Select the widget button, allow microphone access, and say something to the character.

{% hint style="success" %}
The widget opens in voice mode, your speech appears as a message, and the character answers in text and speech.
{% endhint %}

## Next steps

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>useConvaiClient hook reference</strong><br>Everything the hook returns, including its React-only state.</td>
<td><a href="useconvaiclient-hook.md">useconvaiclient-hook.md</a></td>
</tr>
<tr>
<td><strong>ConvaiWidget component reference</strong><br>Props, defaults, and what the widget does on your behalf.</td>
<td><a href="convaiwidget.md">convaiwidget.md</a></td>
</tr>
<tr>
<td><strong>Add lip sync in React</strong><br>Drive a 3D face from the blendshape stream in a render loop.</td>
<td><a href="real-time-lipsync.md">real-time-lipsync.md</a></td>
</tr>
<tr>
<td><strong>Build a custom UI in React</strong><br>Replace the widget with your own messages and controls.</td>
<td><a href="custom-ui-and-advanced-usage.md">custom-ui-and-advanced-usage.md</a></td>
</tr>
<tr>
<td><strong>Add an audio visualizer in React</strong><br>Draw the character's voice level with the Web Audio API.</td>
<td><a href="audio-visualizer-optional.md">audio-visualizer-optional.md</a></td>
</tr>
</tbody>
</table>
