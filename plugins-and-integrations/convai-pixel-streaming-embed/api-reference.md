---
title: Pixel Streaming Embed API reference
description: Reference for the React component, the framework-free client, their options and methods, the events they report, and the errors they show.
last_reviewed: "0.7.1"
icon: webhook
---

`@convai/experience-embed` exports a React component, `PixelStreamComponent`, and a framework-free class, `PixelStreamClient`. Both render a Convai Pixel Streaming experience in an iframe and take the same options, apart from the differences noted on this page.

## Entry points

| Import | Format | Exports |
|---|---|---|
| `@convai/experience-embed` | ES module | `PixelStreamComponent`, `getPixelStream`, and the types `PixelStreamComponentProps`, `PixelStreamComponentHandles`, `EndUserId`, and `ChatStyle` |
| `@convai/experience-embed/core` | UMD, `require` only | `PixelStreamClient`, and the types `PixelStreamOptions`, `EndUserId`, and `ChatStyle` |
| `dist/core/convai-embed.umd.js` loaded by a `<script>` tag | UMD | The global `PixelStreamCore`, whose `PixelStreamClient` property is the class |

The UMD file is self-contained. The ES module imports `react` from your app. The package declares `react` and `react-dom` `^18.3.1` as dependencies.

## PixelStreamComponent props

| Prop | Type | Default | Description |
|---|---|---|---|
| `expId` | `string` | required | The experience ID of a published experience. |
| `authToken` | `string` | none | A Convai auth token minted by your server. When set, it authorizes the session instead of the page's domain. Changing it starts a new session. |
| `endUserId` | `string` | none | Your identifier for the person using the experience. Sent when the session is created, and bound to that session. Changing it starts a new session. An empty or whitespace-only value is left out of the session request. |
| `endUserMetadata` | `Record<string, any>` | none | Extra details about the end user, sent to the stream page with `endUserId`. Allowed only when `endUserId` is set. |
| `InitialScreen` | `React.ReactNode` | a **Click to start your experience** screen | Shown before the experience starts. A custom screen does not start the experience on click; call `initializeExperience()`. |
| `LoadingScreenComponent` | `React.ReactNode` | none | Shown over the iframe until the stream page reports that it has finished loading. |
| `chatStyle` | `ChatStyle` | none | Appearance of the built-in chat window. Changes are applied while the experience runs. |
| `serviceUrls` | `{ sessionFetch?: string; pixelStreamBase?: string }` | Convai's services | Self-hosted service URLs. See [Configure an on-premise deployment](on-premise-deployment.md). |
| `avatarStudio` | `boolean` | none | When `true`, requests the `vhh_character_creator` session mode. |
| `ref` | `React.Ref<PixelStreamComponentHandles>` | none | Receives the methods listed in the next section. |

The component also takes every callback in [Callbacks](#callbacks) as a prop. It fills its parent element, so give the parent a width and a height.

## PixelStreamComponentHandles

The methods available on the component's `ref`. A method called before the stream page has loaded sends nothing:

| Method | Returns | Description |
|---|---|---|
| `initializeExperience()` | `void` | Replaces the initial screen with the experience. |
| `sendMessageToCharacter(message: string)` | `void` | Sends a text message to the character. |
| `beginVoiceInteraction()` | `void` | Sends the experience the signal to start voice input. |
| `endVoiceInteraction()` | `void` | Sends the experience the signal to stop voice input. In a hands-free experience the character keeps hearing the user; use `muteMicrophone()` instead. |
| `muteMicrophone()` | `void` | Mutes the user's microphone while the conversation continues. The mute is kept when the stream reconnects. `onMicStatus` reports when it is applied. |
| `unmuteMicrophone()` | `void` | Unmutes the user's microphone. |
| `enableCamera()` | `Promise<boolean>` | Turns on the user's webcam. Resolves when the stream page reports the camera state: `true` if the camera is on. |
| `disableCamera()` | `Promise<boolean>` | Turns off the user's webcam. Resolves `true` when the stream page reports that the camera is off. |
| `enableCharacterAudio()` | `void` | Unmutes the character's audio. |
| `disableCharacterAudio()` | `void` | Mutes the character's audio. |
| `setChatStyle(style: ChatStyle)` | `void` | Changes the chat appearance. Prefer the `chatStyle` prop. |

When the experience shows its built-in chat and you have not called `muteMicrophone()` or `unmuteMicrophone()`, the microphone starts muted.

## PixelStreamClient options

```ts
new PixelStreamClient(options: PixelStreamOptions)
```

The constructor requests a session and renders into `container` without further calls.

| Option | Type | Default | Description |
|---|---|---|---|
| `container` | `HTMLElement` | required | The element the experience renders into. Its contents are replaced. |
| `expId` | `string` | required | The experience ID of a published experience. |
| `authToken` | `string` | none | A Convai auth token minted by your server. When set, it authorizes the session instead of the page's domain. |
| `endUserId` | `string` | none | Your identifier for the person using the experience, bound to the session when it is created. |
| `endUserMetadata` | `Record<string, any>` | none | Extra details about the end user. Allowed only when `endUserId` is set. |
| `InitialScreen` | `HTMLElement` | a **Click to start your experience** screen | Shown before the experience starts. A custom screen does not start the experience on click; call `initializeExperience()`. |
| `LoadingScreenComponent` | `HTMLElement` | none | Shown over the iframe until the stream page reports that it has finished loading. |
| `chatStyle` | `ChatStyle` | none | Initial appearance of the built-in chat window. |
| `serviceUrls` | `{ sessionFetch?: string; pixelStreamBase?: string }` | Convai's services | Self-hosted service URLs. See [Configure an on-premise deployment](on-premise-deployment.md). |
| `avatarStudio` | `boolean` | none | When `true`, requests the `vhh_character_creator` session mode. |

`PixelStreamClient` also takes every callback in [Callbacks](#callbacks) as an option.

## PixelStreamClient methods

`PixelStreamClient` has the methods of `PixelStreamComponentHandles`, with these differences:

| Method | Difference |
|---|---|
| `enableCharacterAudio()`, `disableCharacterAudio()` | Return `Promise<boolean>`, which resolves `true` once the message is sent. |
| `setChatStyle(style: ChatStyle)` | Merges `style` into the current style, so fields you leave out keep their value. Can be called before the experience loads. |
| `destroy()` | Only on `PixelStreamClient`. Stops listening for messages from the stream page. It does not remove the iframe; clear `container` yourself. |

## Callbacks

Each callback fires when the stream page posts the matching message. An error thrown inside a callback is logged to the console and does not stop the embed:

| Callback | Fires when | Payload |
|---|---|---|
| `onIframeLoaded` | The stream page has loaded. Once per session. | `null` |
| `onCharacterMessage` | The user or the character says something. A character's reply arrives in parts. | The message object from the experience, including `message`, the text; `player`, `true` for the user's own lines; `endofmessage`, `true` on the last part of a reply; and `sentenceready` |
| `onAfk` | The stream disconnects. | `'Disconnected'` |
| `onCameraStatus` | The webcam turns on or off. | `boolean` |
| `onCameraStream` | The experience starts or stops the webcam stream. | `boolean` |
| `onUserUpdated` | The experience updates the user's details. | `null` |
| `onConfigChanged` | The experience changes its configuration. | `null` |
| `onMicStatus` | The stream page applies `muteMicrophone()` or `unmuteMicrophone()`, the user selects the built-in chat's microphone button, or the stream connects. | `{ muted: boolean }` |

## ChatStyle

| Field | Type | Default | Description |
|---|---|---|---|
| `backgroundOpacity` | `number` | `0.7` | Opacity of the backplate behind the chat text, from `0`, fully transparent, to `1`. The input field and microphone button scale by the same factor. |

Values outside `0` to `1` are clamped, and a value that is not a number is ignored.

## getPixelStream

```ts
getPixelStream(options: {
  exp_id: string
  exp_base?: string
  avatarStudio?: boolean
  end_user_id?: string
  auth_token?: string
}): Promise<{ loading: boolean; data: { session: { session_id: string } } | null; error: string | null }>
```

The session request that `PixelStreamComponent` makes before it renders the iframe. It sends `POST <exp_base>/xp/streams/viewPublishedExperience`, where `exp_base` defaults to `https://api.convai.com`, with `auth_token` in the `API-AUTH-TOKEN` header. It never throws: a failure is returned in `error`.

## Errors

When the session request fails, the embed shows an error screen instead of the experience:

| Condition | Message on the error screen |
|---|---|
| No `authToken`, and the request fails | `Please contact convai to get <origin> whitelisted!` |
| `authToken` set, and Convai's error mentions the auth token | `This experience couldn't start: the Convai auth token is invalid or has expired.` |
| `authToken` set, and the request fails for another reason | `This experience couldn't start. Please try again later.` |

## Related reference

{% content-ref url="whitelisting-and-publishing-an-experience.md" %}
[Publish and authorize an experience](whitelisting-and-publishing-an-experience.md)
{% endcontent-ref %}
