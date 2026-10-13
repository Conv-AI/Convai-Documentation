---
title: ConvaiWidget component reference
description: Reference for the prebuilt React chat and voice widget, including every prop, its default, and what the widget handles for you during a session.
last_reviewed: "1.9.1"
---

`ConvaiWidget` is the prebuilt React component exported from `@convai/web-sdk/react`. It renders a collapsible conversation panel for text, voice, camera, and screen share, driven by a client from `useConvaiClient`.

## Props

The props type is not exported from the package. Pass the props inline as JSX attributes.

| Prop | Type | Default | Description |
|---|---|---|---|
| `convaiClient` | Return value of `useConvaiClient` | required | The client the widget drives. It must provide `isAudioMuted`, `isVideoEnabled`, and `isScreenShareActive`, which the hook supplies. |
| `showVideo` | `boolean` | `true` | Shows the camera button in the settings tray. The button appears only when `connectionType` is `"video"`. |
| `showScreenShare` | `boolean` | `true` | Shows the screen share button in the settings tray. The button appears only when `connectionType` is `"video"`. |
| `defaultVoiceMode` | `boolean` | `true` | Opens the panel in voice mode and unmutes the microphone the first time it opens after each connection. Ignored for text-only sessions. |
| `requestPublicationGrant` | `() => Promise<string>` | none | Returns a fresh single-use launch token. When set, the widget connects with `connectWithPublicationGrant` and runs as a text-only chat. Required to reopen a published chat session. |
| `publishedChatConnectOptions` | `PublishedChatConnectOptions` | none | Options passed to `connectWithPublicationGrant`, such as `url` and `signal`. The widget drops `connectAttemptId` so each new grant gets a new attempt ID. |
| `publishedChatDescriptor` | `{ display_name; image_url }` | none | Name and image shown in the header of a published chat session. |

## Connection behavior

- The widget does not connect on mount. The first selection of its button calls `connect()` with the config stored in `useConvaiClient`, then opens the panel.
- After the client has been connected once, the button calls `reconnect()` instead.
- When `requestPublicationGrant` is set, or the client is a published chat session, the button calls `requestPublicationGrant()` and then `connectWithPublicationGrant()`.
- A connection error is logged to the console with `Failed to connect:` and the panel stays closed. Subscribe to the client's `error` event to show it in your UI.
- The panel closes when the client disconnects.

## Conversation behavior

- The widget plays the character's voice. With the LiveKit transport it creates its own `AudioRenderer`; with the WebSocket transport the voice is played by `useConvaiClient`.
- The message list shows `ChatMessage` entries whose type is `user-transcription`, `user-llm-text`, `bot-llm-text`, `bot-output`, or `bot-emotion`, and whose content is not empty.
- Text can be sent only while `state.isConnected` and `isBotReady` are both `true`.
- In text mode the widget mutes the microphone with `audioControls.muteAudio()`.
- The speaker button mutes the character's voice locally. It does not stop the response.
- The character name and image in the header come from Convai for the connected character, or from `publishedChatDescriptor` in a published chat session.

## Settings tray

The settings tray appears while the client is connected.

| Control | Action |
|---|---|
| Reset | Calls `disconnect()`, then `resetSession()`. It does not reconnect; the next selection of the widget button starts a new session. |
| Disconnect | Calls `disconnect()`. |
| Camera | Calls `videoControls.enableVideo()` or `videoControls.disableVideo()`. Shown when `showVideo` is `true` and `connectionType` is `"video"`. |
| Screen share | Calls `screenShareControls.toggleScreenShare()`. Shown when `showScreenShare` is `true` and `connectionType` is `"video"`. |

Reset and Disconnect are hidden in a published chat session that has no `requestPublicationGrant`, because the widget could not start a new session.

## Example

```tsx
import { useConvaiClient, ConvaiWidget } from '@convai/web-sdk/react';

export default function App() {
  const convaiClient = useConvaiClient({
    apiKey: 'YOUR_API_KEY',
    characterId: 'YOUR_CHARACTER_ID',
    enableVideo: true,
    startWithAudioOn: false,
  });

  return (
    <ConvaiWidget
      convaiClient={convaiClient}
      showVideo={true}
      showScreenShare={false}
      defaultVoiceMode={false}
    />
  );
}
```

## Related reference

{% content-ref url="useconvaiclient-hook.md" %}
[useConvaiClient hook reference](useconvaiclient-hook.md)
{% endcontent-ref %}

{% content-ref url="custom-ui-and-advanced-usage.md" %}
[Build a custom UI in React](custom-ui-and-advanced-usage.md)
{% endcontent-ref %}

{% content-ref url="../vanilla-typescript/README.md" %}
[Get started with vanilla TypeScript](../vanilla-typescript/README.md)
{% endcontent-ref %}
