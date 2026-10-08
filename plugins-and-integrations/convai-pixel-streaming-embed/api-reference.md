---
description: >-
  Explore the available props, options, and methods for using Convai's Pixel
  Streaming client across React, Vanilla JS, TypeScript, and CDN setups.
icon: webhook
---

# API Reference

Reference for the props, options, and methods of `@convai/experience-embed` in React, Vanilla JavaScript, TypeScript, and CDN setups.

## PixelStreamComponent Props (React)

| Prop                          | Type              | Required | Description                                                                  |
| ----------------------------- | ----------------- | -------- | ---------------------------------------------------------------------------- |
| `expId`                       | `string`          | ✅ Yes    | The unique experience ID for the experience you want to load.                |
| `authToken`                   | `string`          | ❌ No     | Convai auth token minted on your server. Without it, the page's domain must be whitelisted. See [Authorize embeds with an auth token](authorize-embeds-with-an-auth-token.md). |
| `chatStyle`                   | `{ backgroundOpacity?: number }` | ❌ No | Appearance of the built-in chat window. `backgroundOpacity` (0–1, default `0.7`) sets how transparent its backplate is. |
| `InitialScreen`               | `React.ReactNode` | ❌ No     | Optional custom loading screen component shown before the stream loads.      |
| `serviceUrls`                 | `object`          | ❌ No     | Override default service endpoints (useful for on-premise or custom setups). |
| `serviceUrls.sessionFetch`    | `string`          | ❌ No     | Custom URL for fetching session data.                                        |
| `serviceUrls.pixelStreamBase` | `string`          | ❌ No     | Custom base URL for connecting to the Pixel Streaming server.                |

***

## PixelStreamComponentHandles Methods (React)

These methods are exposed via the `ref` to the component:

| Method                    | Description                                |
| ------------------------- | ------------------------------------------ |
| `enableCamera()`          | Enables the user's webcam.                 |
| `disableCamera()`         | Disables the user's webcam.                |
| `enableCharacterAudio()`  | Unmutes audio coming from the character.   |
| `disableCharacterAudio()` | Mutes the character audio.                 |
| `initializeExperience()`  | Starts the experience if not auto-started. |
| `setChatStyle(style)`     | Changes the built-in chat window's appearance, such as `{ backgroundOpacity: 0.3 }`. |

***

## PixelStreamClient Options (Vanilla / TS / CDN)

| Option                        | Type          | Required | Description                                                                  |
| ----------------------------- | ------------- | -------- | ---------------------------------------------------------------------------- |
| `container`                   | `HTMLElement` | ✅ Yes    | DOM element where the pixel stream will be mounted.                          |
| `expId`                       | `string`      | ✅ Yes    | The experience ID to load the experience.                                    |
| `authToken`                   | `string`      | ❌ No     | Convai auth token minted on your server. Without it, the page's domain must be whitelisted. See [Authorize embeds with an auth token](authorize-embeds-with-an-auth-token.md). |
| `chatStyle`                   | `{ backgroundOpacity?: number }` | ❌ No | Appearance of the built-in chat window. `backgroundOpacity` (0–1, default `0.7`) sets how transparent its backplate is. |
| `InitialScreen`               | `HTMLElement` | ❌ No     | Optional loading screen shown while the experience initializes.              |
| `serviceUrls`                 | `object`      | ❌ No     | Object to override default endpoints (for on-premise or custom backend use). |
| `serviceUrls.sessionFetch`    | `string`      | ❌ No     | Custom endpoint for session fetch API.                                       |
| `serviceUrls.pixelStreamBase` | `string`      | ❌ No     | Base URL of the Pixel Streaming backend server.                              |

***

## PixelStreamClient Methods

These are available on the `pixelStream` instance in Vanilla/TS/CDN setups:

| Method                    | Description                                    |
| ------------------------- | ---------------------------------------------- |
| `enableCamera()`          | Enables the user’s webcam. Returns a Promise.  |
| `disableCamera()`         | Disables the user’s webcam. Returns a Promise. |
| `enableCharacterAudio()`  | Enables character audio output.                |
| `disableCharacterAudio()` | Disables character audio output.               |
| `initializeExperience()`  | Starts the experience manually.                |
| `setChatStyle(style)`     | Changes the built-in chat window's appearance, such as `{ backgroundOpacity: 0.3 }`. |
| `destroy()`               | Cleans up the stream and DOM elements.         |
