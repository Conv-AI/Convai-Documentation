---
title: Mute the character's voice
description: Silence what the character says without stopping the conversation, build your own mute button, and mute one character in a multi-character session.
last_reviewed: "1.9.2"
icon: volume-xmark
---

Silence the character's voice while the conversation continues. Use this page when you are building your own mute button, or when one character in a multi-character session should be heard and another should not.

This is the speaker, not the microphone. `setCharacterMuted` changes what the person hears; [`audioControls.muteAudio`](../convai-web-sdk/README.md) changes what their microphone sends. The two are independent.

## Prerequisites

- The Convai Web SDK installed, with a client that connects. See [Web SDK quickstart](quickstart.md).

## Mute and unmute

Call `setCharacterMuted` with `true` to silence the character and `false` to restore it. The method is on the client, so it works the same on `new ConvaiClient(...)` from `@convai/web-sdk/core` and on the object `useConvaiClient(...)` returns.

```ts
client.setCharacterMuted(true);   // the character is silent
client.setCharacterMuted(false);  // the character is audible again
```

The conversation is unaffected. The character goes on talking, the reply goes on streaming, and transcripts, emotions, and blendshapes go on arriving. Only the sound stops, which means a 3D character keeps lip-syncing while muted.

Nothing is renegotiated with the server, so muting in the middle of a sentence and unmuting a moment later resumes in place instead of restarting the reply.

## Mute on the WebSocket transport

`setCharacterMuted` works on the WebRTC and WebSocket transports. WebSocket support requires 1.9.2 or later; on earlier versions the client reports muted but the voice keeps playing. On the WebSocket transport, speech made while muted is dropped, not queued, so unmuting resumes from what the character is saying at that moment.

## Read the current state

`isCharacterMuted` returns whether the character is silenced.

```ts
client.setCharacterMuted(!client.isCharacterMuted());   // toggle
```

It is a method, not reactive state. In React, keep your own state beside it so the button re-renders:

```tsx
const [muted, setMuted] = useState(false);

const toggle = () => {
  const next = !muted;
  client.setCharacterMuted(next);
  setMuted(next);
};

return <button onClick={toggle}>{muted ? 'Unmute' : 'Mute'}</button>;
```

The bundled `ConvaiWidget` already shows a mute button, and it calls this same method. A button of your own and the widget's icon therefore describe one shared state rather than two.

## Mute before connecting

A call made before the client connects is remembered and applied to the first audio that arrives, so a session that should start silent does not begin with an audible moment.

```ts
client.setCharacterMuted(true);
await client.connect();   // the character is silent from the first word
```

The setting also survives a reconnect, and a character who joins a multi-character session later arrives muted rather than audible.

## Mute one character in a multi-character session

Pass the `membershipId` of a roster member to address that member alone. Omit it to set every character in the session.

```ts
const [first, second] = client.characters;

client.setCharacterMuted(true, { membershipId: second.membershipId });

client.isCharacterMuted();                      // false, the session is audible
client.isCharacterMuted(second.membershipId);   // true, this member is not
```

A call without `membershipId` sets the whole session and clears the settings made for individual members. This is why `setCharacterMuted(false)` always restores every voice: without it, a member muted on its own earlier would stay silent with nothing in your code to explain it.

`isCharacterMuted(membershipId)` reports what that member actually does: its own setting when one was made for it, and the session-wide setting otherwise.

See [Multi-character sessions](README.md) for where `membershipId` comes from.

## Reference

| Method | Signature | Description |
|---|---|---|
| `setCharacterMuted` | `(muted: boolean, options?: { membershipId?: string }) => void` | Silences the character's voice, or restores it. Remembered across reconnects and applied to audio that arrives later. |
| `isCharacterMuted` | `(membershipId?: string) => boolean` | The session-wide setting with no argument, or that member's effective setting with one. |
