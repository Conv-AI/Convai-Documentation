---
title: Host several characters in one room
description: Connect a roster of Convai characters to one realtime room, choose which one answers, change the roster live, and let a second person join.
last_reviewed: "1.9.0"
---

Host several characters in one realtime room and talk to any of them without reconnecting. Use this page for scenes with more than one speaker, such as a guide and an assessor, a panel interview or a group of NPCs.

{% hint style="warning" %}
Multi-character rooms are in beta. They require the `MULTI_CHARACTER_V0` entitlement on your account, which is off by default. Without it, connecting with a roster fails with `403 MULTI_CHARACTER_V0_DISABLED`.
{% endhint %}

## How a roster room works

Every character in the room is a separate participant with its own voice, conversation history and lifecycle. The room is shared; the character state is not.

You create the room by passing an ordered `characters` array instead of `characterId`. Each entry becomes one member of the roster:

* `characters[0]` is the initial active member, the one that answers first.
* The same `characterId` can appear more than once. Each entry is an independent copy with its own history and voice.
* Every member gets a `membershipId`. Address members by `membershipId`, never by `characterId`, because two copies of one character share a `characterId`.

Roster rooms need the realtime (WebRTC) transport and a nonblank `endUserId`.

## Connect with a roster

{% tabs %}
{% tab title="React" %}
{% code title="src/App.tsx" %}
```tsx
import { useConvaiClient, ConvaiWidget } from '@convai/web-sdk/react';

const GUIDE = 'YOUR_CHARACTER_ID';
const ASSESSOR = 'YOUR_SECOND_CHARACTER_ID';

export default function App() {
  const client = useConvaiClient({
    apiKey: 'YOUR_API_KEY',
    endUserId: 'player-42',
    characters: [
      { characterId: GUIDE },     // characters[0] answers first
      { characterId: ASSESSOR },
      { characterId: GUIDE },     // an independent second copy of the guide
    ],
    maxNumParticipants: 2,
  });

  const { characters, activeMembershipId } = client.state;

  return (
    <div>
      <ul>
        {characters.map((c) => (
          <li key={c.membershipId}>
            {c.displayName ?? c.membershipId.slice(0, 8)} · {c.provisioningStatus}
            {c.membershipId === activeMembershipId && ' · active'}
            {c.failureCode && ` · failed: ${c.failureCode}`}
          </li>
        ))}
      </ul>
      <ConvaiWidget convaiClient={client} />
    </div>
  );
}
```
{% endcode %}
{% endtab %}

{% tab title="TypeScript" %}
{% code title="src/main.ts" %}
```typescript
import { ConvaiClient, ConvaiRoomError } from '@convai/web-sdk/core';

const GUIDE = 'YOUR_CHARACTER_ID';
const ASSESSOR = 'YOUR_SECOND_CHARACTER_ID';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  endUserId: 'player-42',
  characters: [
    { characterId: GUIDE },
    { characterId: ASSESSOR, characterSessionId: 'resume-this-history' },
  ],
  sharedSessionKey: 'match-7-party-a',
  maxNumParticipants: 2,
});

try {
  await client.connect();
  console.log(client.roomSession?.roomSessionId);
  console.log(client.characters.map((c) => c.membershipId));
} catch (error) {
  if (error instanceof ConvaiRoomError) {
    // Log requestTraceId: support uses it to find the request.
    console.error(error.status, error.code, error.requestTraceId);
  }
}
```
{% endcode %}
{% endtab %}
{% endtabs %}

* `characters` and `characterId` are mutually exclusive. Passing both throws before any request is sent.
* Roster entries take a bare character UUID. The version selectors that `characterId` accepts, such as `<uuid>-draft` or `<uuid>-1.2`, are rejected inside a roster.
* `characterSessionId` on an entry resumes that member's earlier history. It must be unique within the roster.
* `client.characterId` and `client.characterSessionId` mirror `characters[0]`.
* `sharedSessionKey` groups requests into one room: a matching create request reuses the existing room.

## Tell members apart

`client.characters` (and `client.state.characters` in React) lists the roster in order. It is empty in a single-character session, so checking its length tells the two apart. Each entry is a `ConvaiCharacterInstance` carrying its `membershipId`, `characterId`, `displayName` when the runtime sends one, and its status.

Everything a member produces is attributed by `membershipId`, so two copies of one character never merge:

* Transcript messages carry `membershipId` and `characterId`.
* `characterAudioTrack` names the member that owns each audio track.
* `characterReady` passes the member that became ready.

### Readiness is not dispatch

`provisioningStatus` describes dispatch only: `dispatch_queued`, `dispatch_accepted` or `dispatch_failed`. `dispatch_accepted` does not mean ready. A member is usable once its own ready signal arrives, which sets `isReady` to `true` and fires `characterReady`.

```ts
client.on('characterReady', (member) => {
  console.log('ready', member?.membershipId);
});

client.on('characterStatus', ({ membershipId, status, failureCode }) => {
  if (status === 'failed') console.warn(membershipId, failureCode);
});
```

`characterStatus` reports members added at runtime and members whose dispatch failed in the background. Do not enable interaction from a `ready` status alone; wait for `characterReady`.

### Play each member's audio

The built-in widgets render one shared transcript, attributed per message, and play every member's audio. For a separate pane per character, bind the audio yourself from `characterAudioTrack`. The event always names the owning member in a roster room, and a track that cannot be attributed to a member is dropped.

```ts
client.on('characterAudioTrack', ({ membershipId, track }) => {
  const el = document.querySelector<HTMLAudioElement>(`audio[data-member="${membershipId}"]`);
  if (el) el.srcObject = new MediaStream([track]);
});
```

### Mute one member

Pass a `membershipId` to `setCharacterMuted` to silence one member and leave the rest audible. A call without it sets every character in the room. See [Mute the character's voice](mute-the-characters-voice.md).

```ts
const [, second] = client.characters;
client.setCharacterMuted(true, { membershipId: second.membershipId });
client.isCharacterMuted(second.membershipId);   // true
```

## Switch who answers

Only the active member consumes user turns. Call `setInteractionTarget` with a `membershipId` before directing the next message elsewhere.

```ts
const assessor = client.characters.find((c) => c.characterId === ASSESSOR)!;

await client.setInteractionTarget(assessor.membershipId);
client.sendUserTextMessage('Now grade my answer.');
```

Render the active member from `activeCharacterChange` rather than from your own call, because another participant in the room can switch the target too.

```ts
client.on('activeCharacterChange', ({ previous, active, routeEpoch }) => {
  console.log('now talking to', active, 'at epoch', routeEpoch);
});
```

* `setInteractionTarget(null)` closes every gate. No member hears the user until you set a target again.
* A target that is not ready yet is refused before the command is sent.
* If another participant switched first, the call retries once against the server's current state.

## Add and remove members live

`updateCharacterRoster` changes the roster of a connected room. `remove` takes membership ids, not character ids.

```ts
await client.updateCharacterRoster({
  add: [{ characterId: NARRATOR }],
  remove: [someMembershipId],
});
```

* Removing the active member needs a replacement that is ready and stays in the room. One is chosen automatically when you do not pass `replacementTarget`.
* New members cannot be addressed until each sends its own ready signal. Watch `characterReady`.
* The room cannot be emptied.
* If another participant changed the roster first, the call rejects with the conflict for you to reconcile. It does not retry.
* `rosterChange` fires with the added and removed members and the roster after the change.

{% hint style="info" %}
A lost acknowledgement is not a failure. When the server's acknowledgement goes missing, the promise rejects saying the outcome is unknown. Read `client.roomSession` to see what actually happened before sending a conflicting command.
{% endhint %}

## Let another person join

A second person joins the room the first one created, by `roomSessionId` or by `sharedSessionKey`. A join sends no roster: the roster belongs to the server, and a join never adds, removes or repairs a character.

```typescript
const second = new ConvaiClient({ apiKey: 'YOUR_API_KEY' });

await second.joinRoom({
  roomSessionId: 'the-room-session-id',   // or: sharedSessionKey: 'match-7-party-a'
  endUserId: 'player-99',
});

console.log(second.characters.length);   // the existing roster
```

* Pass exactly one locator. `roomSessionId` is preferred.
* `endUserId` is required.
* Capacity counts distinct people by `endUserId` and defaults to 1. Set `maxNumParticipants` when you create the room, or the join fails with `409 Human room capacity reached`. A reconnect by the same person does not use another slot.

## Limitations

* **Realtime transport only.** Roster rooms do not run on the WebSocket or SSE transports. See [Choose a transport](choose-a-transport.md).
* **No action protocol v2 or client tools.** `capabilities.actionProtocolVersion: 2` (or `modelOutputVersion: 2`) needs a single-character room, so `actionConfig.tools` is unavailable too. Version 1 works. The SDK rejects the combination before sending the request.
* **`resetSession()` throws** in a roster room, because the server owns each member's session.
* **Reusing a `sharedSessionKey`** with a different ordered roster, creator or capacity fails with `ROSTER_FINGERPRINT_MISMATCH`. Reordering the same characters counts as different, because it changes the initial member.
* **Provisioning retries.** When an identical request is still creating the room, the SDK retries with bounded backoff. Pass `rosterProvisioningRetry: false` to handle `ROSTER_PROVISIONING_IN_PROGRESS` yourself.

## Errors

A roster `connect()` and `joinRoom()` throw `ConvaiRoomError` when the room cannot be created or joined. It carries `status`, `code`, `requestTraceId`, `detail` and `isRetryable`. Include `requestTraceId` when you contact support.

| Code | Status | Meaning |
| --- | --- | --- |
| `MULTI_CHARACTER_V0_DISABLED` | 403 | Multi-character rooms are not enabled for your account. |
| `MULTI_CHARACTER_ROSTER_LIMIT_EXCEEDED` | 403 | The roster is larger than your account allows. |
| `CHARACTER_NOT_FOUND_OR_INACCESSIBLE` | 404 | A roster entry names a character you cannot use. |
| `ROSTER_FINGERPRINT_MISMATCH` | 409 | A `sharedSessionKey` was reused with a different roster, creator or capacity. |
| `ROSTER_PROVISIONING_IN_PROGRESS` | 409 | The room is still being created. Retried automatically. |
| `Human room capacity reached` | 409 | The room already holds `maxNumParticipants` people. |

## API reference

| Property / Method | Type | Description |
| --- | --- | --- |
| `characters` (config) | `ConvaiCharacterSpec[]` | Ordered roster, passed instead of `characterId`. Each entry is `{ characterId, characterSessionId? }`. |
| `sharedSessionKey` (config) | `string` | Groups create requests into one room; also a join locator. |
| `connectAttemptId` (config) | `string` | Idempotency key for one logical connect. Reuse it only when retrying an identical request. |
| `maxNumParticipants` (config) | `number` | Maximum distinct people in the room. Characters do not count. Default 1. |
| `rosterProvisioningRetry` (config) | `{ attempts?, initialDelayMs? } \| false` | Retry while the room is provisioning. Default four attempts from 500 ms. |
| `characters` | `ConvaiCharacterInstance[]` | The roster in order. Empty in a single-character session. Also on `state`. |
| `activeMembershipId` | `string \| null` | Member currently receiving user turns. Also on `state`. |
| `roomSession` | `ConvaiRoomSession \| null` | Server-owned room snapshot: `roomSessionId`, `activeMembershipId`, `routeEpoch`, `rosterEpoch`, `partialDispatch`, `characters`. Null in a single-character session. |
| `setInteractionTarget(membershipId)` | `(membershipId: string \| null) => Promise<ActiveCharacterChange>` | Route later user turns to another member. `null` closes every gate. |
| `updateCharacterRoster(options)` | `(options: UpdateCharacterRosterOptions) => Promise<CharacterRosterChange>` | Add members (`add`), remove them by membership id (`remove`), and optionally name a `replacementTarget`. |
| `joinRoom(options)` | `(options: JoinRoomOptions) => Promise<void>` | Join an existing room by `roomSessionId` or `sharedSessionKey`, with a required `endUserId`. |
| `appendMessage(message)` | `(message: AppendMessageOptions) => ChatMessage` | Insert a transcript line locally without sending it. Pass `membershipId` to attribute it to a member. |
| `setCharacterMuted(muted, options?)` | `(muted: boolean, options?: { membershipId?: string }) => void` | Silence every character, or one member. |
| `isCharacterMuted(membershipId?)` | `(membershipId?: string) => boolean` | The room-wide setting, or one member's effective setting. |
| `characterReady` (event) | `(instance: ConvaiCharacterInstance \| undefined) => void` | A member sent its ready signal. |
| `characterStatus` (event) | `(status: CharacterStatusEvent) => void` | A member is `starting`, `ready` or `failed`, with `failureCode` on failure. |
| `activeCharacterChange` (event) | `(change: ActiveCharacterChange) => void` | The active member changed: `previous`, `active`, `routeEpoch`. |
| `rosterChange` (event) | `(change: CharacterRosterChange) => void` | The roster changed: `added`, `removed`, `characters`, `activeMembershipId`. |
| `characterAudioTrack` (event) | `(event: CharacterAudioTrackEvent) => void` | An audio track with the `membershipId` and `characterId` that own it. |

For the full list of events, see [Event reference](event-reference.md).
