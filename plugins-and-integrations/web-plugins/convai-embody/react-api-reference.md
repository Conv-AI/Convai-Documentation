---
title: React API reference
description: Reference for the Convai Embody React components and hooks, including every prop, its type and default, and what each hook returns.
last_reviewed: "0.4.2"
---

The React API is exported from `@convai/embody/react`. Every component and hook here also accepts the character options documented in the [createCharacter reference](createcharacter-reference.md), such as `characterId`, `token`, and `apiKey`.

## ConvaiCharacter

A self-contained character view: a `<Canvas>`, a camera, lights, orbit controls, and the character. It is both a named export and the default export of `@convai/embody/react`.

| Prop | Type | Default | Description |
|---|---|---|---|
| `style` | `React.CSSProperties` | `{ width: '100%', height: '100%', minHeight: '100vh' }`, merged with yours | Wrapper style. |
| `className` | `string` | none | Wrapper class name. |
| `background` | `string \| null` | `'#17181c'` | Scene background color. `null` renders transparent so the page shows through. |
| `camera` | `{ position?: [number, number, number]; fov?: number; target?: [number, number, number] }` | `position: [0, 1.45, 3.6]`, `fov: 35`, `target: [0, 0.92, 0]` | Camera framing in meters. |
| `orbit` | `boolean \| OrbitOptions` | `true` | Drag to turn around the character and scroll to move in and out. `false` fixes the camera. An object tunes the limits. |
| `fallback` | `React.ReactNode` | `null` | Rendered while the body loads. |
| `onReady` | `(character: CharacterHandle) => void` | none | Called once the body is loaded and the connection is live. |
| `onError` | `(error: Error) => void` | none | Called with the error that stopped loading. |
| `queue` | `BlendshapeQueue` | the character's own session | Overrides which turn this body lip-syncs to. Only needed when one client drives several characters. |

All [createCharacter options](createcharacter-reference.md#options) are accepted as props.

## CharacterModel

The character alone, for use inside a `<Canvas>` you create. It adds no camera, lights, or controls.

| Prop | Type | Default | Description |
|---|---|---|---|
| `onReady` | `(character: CharacterHandle) => void` | none | Called once the body is loaded and the connection is live. |
| `onError` | `(error: Error) => void` | none | Called with the error that stopped loading. |
| `queue` | `BlendshapeQueue` | the character's own session | Overrides which turn this body lip-syncs to. |

All [createCharacter options](createcharacter-reference.md#options) are accepted as props.

## OrbitOptions

Passed as the `orbit` prop of `ConvaiCharacter`, or as `options` to `OrbitRig`.

| Field | Type | Default | Description |
|---|---|---|---|
| `minDistance` | `number` | `0.6` | Closest the camera may come, in meters. |
| `maxDistance` | `number` | `8` | Furthest the camera may move away, in meters. |
| `minPolarAngle` | `number` | `Math.PI * 0.12` | Highest the camera may rise, in radians from straight up. |
| `maxPolarAngle` | `number` | `Math.PI * 0.52` | Lowest the camera may sink, in radians from straight up. Beyond `Math.PI / 2` it looks up from below. |
| `enablePan` | `boolean` | `false` | Drag the character around the frame. |
| `enableZoom` | `boolean` | `true` | Scroll to move in and out. |
| `autoRotate` | `boolean` | `false` | Turn slowly around the character on its own. |
| `autoRotateSpeed` | `number` | `1.2` | Speed while `autoRotate` is on. |

## OrbitRig

Orbit controls for a `<Canvas>` you create around `CharacterModel`, matching the behavior `ConvaiCharacter` provides.

| Prop | Type | Default | Description |
|---|---|---|---|
| `target` | `[number, number, number]` | required | The point the camera orbits, in meters. Use the character's head height rather than its feet. |
| `options` | `OrbitOptions` | the defaults above | Orbit limits. |

## useCharacter

```tsx
function useCharacter(options: UseCharacterOptions): UseCharacterResult
```

Loads a character and returns it. `UseCharacterOptions` is every [createCharacter option](createcharacter-reference.md#options) plus `queue`. Must be called inside a `<Canvas>`.

| Field | Type | Description |
|---|---|---|
| `character` | `CharacterHandle \| null` | The loaded character, or `null` until it is ready. |
| `client` | `ConvaiClient \| null` | The connected client once ready. The same object as `character.client`. |
| `error` | `Error \| null` | The error that stopped loading. |
| `status` | `'loading' \| 'ready' \| 'error'` | `'loading'` until the body and the connection are both up. |

## useWidgetClient

```tsx
function useWidgetClient(client: ConvaiClient | null): WidgetClient | null
```

Adapts a character's `ConvaiClient` to the `convaiClient` prop of `ConvaiWidget`, without opening a second connection. Returns `null` while `client` is `null`. `WidgetClient` is `ConvaiClient` plus `activity`, `isAudioMuted`, `isVideoEnabled`, and the other state fields the widget reads.

## Re-exported from the Convai Web SDK

These are the Convai Web SDK's own exports, re-exported unchanged so an app needs only `@convai/embody`.

| Export | Kind |
|---|---|
| `ConvaiWidget` | React component |
| `useConvaiClient` | React hook. Constructs a separate client and connection; do not use it for a character's widget. |
| `AudioRenderer` | React component |
| `AudioContext` | React context |
| `ConvaiClient` | Class |
| `ConvaiConfig` | Type |

## Related reference

{% content-ref url="createcharacter-reference.md" %}
[createCharacter reference](createcharacter-reference.md)
{% endcontent-ref %}
