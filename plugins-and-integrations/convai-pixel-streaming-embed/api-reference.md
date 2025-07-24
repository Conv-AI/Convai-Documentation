---
description: >-
  Explore the available props, options, and methods for using Convai's Pixel
  Streaming client across React, Vanilla JS, TypeScript, and CDN setups.
icon: webhook
---

# API Reference

## PixelStreamComponent Props (React)

| Prop                          | Type              | Required | Description                                                                  |
| ----------------------------- | ----------------- | -------- | ---------------------------------------------------------------------------- |
| `expId`                       | `string`          | ✅ Yes    | The unique experience ID for the experience you want to load.                |
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

***

## PixelStreamClient Options (Vanilla / TS / CDN)

| Option                        | Type          | Required | Description                                                                  |
| ----------------------------- | ------------- | -------- | ---------------------------------------------------------------------------- |
| `container`                   | `HTMLElement` | ✅ Yes    | DOM element where the pixel stream will be mounted.                          |
| `expId`                       | `string`      | ✅ Yes    | The experience ID to load the experience.                                    |
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
| `destroy()`               | Cleans up the stream and DOM elements.         |
