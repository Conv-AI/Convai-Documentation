---
title: Connect to a character version
description: Connect to a character's draft, latest release or a tagged version, and list, compare, release, promote and discard versions from the client.
last_reviewed: "2.0.1"
icon: code-branch
---

Every character has an editable draft and, once released, a set of immutable tagged versions such as `1.0` and `1.1`. A movable `latest` pointer names the release the runtime uses when a client connects without a selector. Use this page to test changes in the draft, release a tag when it is ready, and roll back by pointing `latest` at an older tag.

{% hint style="warning" %}
Character versioning is in beta. Explicit selectors (`draft`, `latest` or a tag) work on production and staging. A deployment without character version resolution, such as a self-hosted runtime, answers them with `503 Character version resolution is unavailable`. Omitting `characterVersion` works as before.
{% endhint %}

## Prerequisites

- The Convai Web SDK installed, with a client that connects. See [Web SDK quickstart](quickstart.md).
- A Convai API key. `client.characterVersions` is `null` without one.

## Choose a version selector

Set `characterVersion` in the client configuration to pick the version that runs.

| `characterVersion` | Runs |
|---|---|
| *(omitted)* | The effective latest release. Characters that predate versioning behave as before. |
| `'draft'` | The editable draft, for testing unreleased changes. |
| `'latest'` | The promoted latest release, explicitly. |
| `'1.2'` / `'1.2.3'` | An immutable tagged version, in `major.minor` or `major.minor.patch` form. |

On the wire the selector is joined to the character ID as `<uuid>-draft`, `<uuid>-latest` or `<uuid>-1.2`. `characterId` may carry that suffix directly instead; setting both is allowed only when they agree. After you connect, `client.characterId` still returns the bare UUID, `client.characterVersion` returns the selector and `client.characterReference` returns the joined form.

## Connect to a version

`characterVersion` is part of `ConvaiConfig`, so you can pass it to `useConvaiClient`, `new ConvaiClient()` or `connect()`.

{% tabs %}
{% tab title="React" %}
{% code title="src/App.tsx" %}
```tsx
import { useConvaiClient } from '@convai/web-sdk/react';
import { ConvaiWidget } from '@convai/web-widget/react';

export default function App() {
  const client = useConvaiClient({
    apiKey: 'YOUR_API_KEY',
    characterId: 'YOUR_CHARACTER_ID',
    characterVersion: 'draft', // or 'latest', '1.2', or omit
  });

  return <ConvaiWidget convaiClient={client} />;
}
```
{% endcode %}

The hook returns `characterVersion`, `characterReference` and `characterVersions` alongside the other client members.
{% endtab %}

{% tab title="TypeScript" %}
{% code title="src/main.ts" %}
```typescript
import { ConvaiClient } from '@convai/web-sdk/core';
import { createConvaiWidget } from '@convai/web-widget/vanilla';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  characterVersion: 'latest',
});

await client.connect();

createConvaiWidget(document.body, { convaiClient: client });
```
{% endcode %}
{% endtab %}
{% endtabs %}

Changing the version means a new session. Call `disconnect()`, then `connect()` with the new configuration. `reconnect()` reuses the stored configuration, including its `characterVersion`.

An unknown tag fails with `404 Character version was not found`.

## Manage versions

`client.characterVersions` returns a `CharacterVersionManager` for the configured character. It is available as soon as the configuration has an `apiKey` and a `characterId`, before you connect, so you can list versions, pick one, and then connect to it.

By default the manager calls `https://api2.convai.com`. Set `characterApiUrl` to `https://api2-stg.convai.com` to work against staging.

{% tabs %}
{% tab title="React" %}
{% code title="src/App.tsx" %}
```tsx
import { useConvaiClient } from '@convai/web-sdk/react';
import { ConvaiWidget } from '@convai/web-widget/react';

export default function App() {
  const client = useConvaiClient({
    apiKey: 'YOUR_API_KEY',
    characterId: 'YOUR_CHARACTER_ID',
    characterVersion: 'draft',
    characterApiUrl: 'https://api2-stg.convai.com', // optional, defaults to production
  });

  const release = async () => {
    const versions = client.characterVersions;
    if (!versions) return; // no apiKey configured
    const { has_unpublished_changes, latest_version } = await versions.list();
    if (has_unpublished_changes) {
      await versions.create('1.1', { makeLatest: true });
    }
    console.log('latest was', latest_version);
  };

  return (
    <>
      <button onClick={release}>Release draft as 1.1</button>
      <ConvaiWidget convaiClient={client} />
    </>
  );
}
```
{% endcode %}
{% endtab %}

{% tab title="TypeScript" %}
{% code title="src/main.ts" %}
```typescript
import { ConvaiClient } from '@convai/web-sdk/core';
import { createConvaiWidget } from '@convai/web-widget/vanilla';

const config = {
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
};

const client = new ConvaiClient(config);
const versions = client.characterVersions;

if (versions) {
  // Review what the draft changes, then release it.
  const diff = await versions.diff('latest', 'draft', { view: 'semantic' });
  diff.changes.forEach((c) => console.log(`${c.change_type} ${c.label}`));
  const released = await versions.create('2.0', { makeLatest: true });

  // Connect to the tag that was just released.
  await client.connect({ ...config, characterVersion: released.version });
}

createConvaiWidget(document.body, { convaiClient: client });
```
{% endcode %}
{% endtab %}
{% endtabs %}

Every method returns the API's JSON as it arrives, with snake_case field names. The SDK checks the selector or tag locally first and throws before sending a request when it is malformed.

### List versions

`list()` returns the released tags in `items`, plus the state of `latest` and the draft.

```ts
const { items, latest_version, draft_revision_id, has_unpublished_changes } = await versions.list();
```

`has_unpublished_changes` is `true` when the draft differs from the release it was branched from. `draft_revision_id` is `null` for a character that predates versioning and has no draft yet.

### Compare versions

`diff(from, to)` compares two selectors. Each side is `'draft'`, `'latest'` or a tag.

```ts
const raw = await versions.diff('1.0', '1.1');                                 // JSON paths
const semantic = await versions.diff('latest', 'draft', { view: 'semantic' }); // labelled changes
```

The default raw view lists the JSON paths that changed. The semantic view groups them into labelled changes, each with a `change_id` you can pass to `revert()`.

### Release the draft

`create(version)` releases the current draft as an immutable tag. The tag must be `major.minor` or `major.minor.patch`. `latest` does not move unless you pass `makeLatest: true`.

```ts
await versions.create('1.1');                       // tag only, latest unchanged
await versions.create('1.2', { makeLatest: true }); // tag and point latest at it
```

### Promote or roll back

`promote(version)` points `latest` at a released tag. Promoting an older tag is how you roll back; the newer tag stays connectable by its tag.

```ts
await versions.promote('1.1'); // latest → 1.1
await versions.promote('1.0'); // roll back: latest → 1.0
```

### Discard or revert draft changes

`discardDraft()` resets the draft to its released parent. `revert()` undoes one change from a semantic diff. Both take the draft revision you last saw.

```ts
const { draft_revision_id } = await versions.list();
if (draft_revision_id) {
  await versions.discardDraft(draft_revision_id);
}
```

```ts
const diff = await versions.diff('latest', 'draft', { view: 'semantic' });
const change = diff.changes.find((c) => c.can_revert);
if (change && diff.draft_revision_id) {
  await versions.revert({
    from: 'latest',
    changeId: change.change_id,
    expectedDraftRevisionId: diff.draft_revision_id,
  });
}
```

{% hint style="info" %}
`discardDraft()` and `revert()` are refused if the draft moved since you read its revision, so a concurrent edit is not silently thrown away. After a failure, call `list()` again for the current `draft_revision_id`.
{% endhint %}

### Fork a released version

`fork(version)` replaces the draft with the contents of a released tag, so you can start new work from an older version. Pass the draft revision you last saw as the second argument to refuse the fork if someone else changed the draft in the meantime.

```ts
const { draft_revision_id } = await versions.list();
await versions.fork('1.0', draft_revision_id ?? undefined);
```

### Deprecate a tag

`deprecate(version)` flags a tag as deprecated, and `deprecate(version, false)` clears the flag. Deprecated tags remain connectable.

### Give a legacy character a draft

`bootstrap()` creates the draft for a character that predates versioning. It is idempotent: `created` is `false` when the character already had a draft.

```ts
await versions.bootstrap();
```

## Use the manager without a client

`CharacterVersionManager` can be constructed on its own, with either an API key or a Convai personal access token. Import it from `@convai/web-sdk/core` or `@convai/web-sdk/vanilla`.

{% code title="versions.ts" %}
```ts
import { CharacterVersionManager } from '@convai/web-sdk/core';

const versions = new CharacterVersionManager({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
});

const { has_unpublished_changes } = await versions.list();
```
{% endcode %}

## Handle errors

A non-2xx answer rejects with `CharacterApiError`. Its `status` is the HTTP code and `detail` is the parsed response body.

```ts
import { CharacterApiError } from '@convai/web-sdk/core';

try {
  await versions.promote('9.9');
} catch (err) {
  if (err instanceof CharacterApiError) {
    console.error(err.status, err.detail);
  }
}
```

| Error | Cause |
|---|---|
| `503 Character version resolution is unavailable` | The runtime does not resolve explicit selectors, for example a self-hosted deployment without character version resolution. Omit `characterVersion` there. |
| `404 Character version was not found` | The tag does not exist for this character. |
| `403` from `resolve()` | `includeRuntimeSettings` is reserved for trusted services. An API key cannot request it. |
| `Expected "draft", "latest", or a major.minor[.patch] tag` | A malformed selector, rejected locally before any request. |

## API reference

| Property / Method | Type | Description |
|---|---|---|
| `ConvaiConfig.characterVersion` | `'draft' \| 'latest' \| string \| null` | Version to connect to. A `major.minor[.patch]` string selects a tag. Omit for the effective latest. |
| `ConvaiConfig.characterId` | `string` | May carry the selector directly as `<uuid>-draft`. Setting both is allowed only when they agree. |
| `ConvaiConfig.characterApiUrl` | `string` | Base URL for `client.characterVersions`. Default `https://api2.convai.com`; staging is `https://api2-stg.convai.com`. |
| `client.characterId` | `string \| null` | Bare character UUID of the current connection. |
| `client.characterVersion` | `CharacterVersionSelector \| null` | Selector in effect, or `null` when unversioned. |
| `client.characterReference` | `string \| null` | The joined `<uuid>[-selector]` sent to the runtime. |
| `client.characterVersions` | `CharacterVersionManager \| null` | Version manager for the configured character; `null` without an `apiKey`. |
| `new CharacterVersionManager(options)` | `{ characterId, apiKey?, personalAccessToken?, baseUrl?, workspaceId? }` | Standalone construction. One credential is required. |
| `list()` | `Promise<CharacterVersionList>` | Released tags plus the `latest_*`, `draft_*` and `has_unpublished_changes` fields. |
| `resolve(version?, { includeRuntimeSettings? })` | `Promise<ResolvedCharacterVersion>` | The configuration snapshot the runtime would run for that reference. |
| `diff(from, to, { view? })` | `Promise<CharacterVersionRawDiff \| CharacterVersionSemanticDiff>` | Compare two selectors. `view: 'semantic'` returns labelled, revertable changes. |
| `create(version, { makeLatest? })` | `Promise<CharacterVersionInfo>` | Release the draft as an immutable tag. |
| `promote(version)` | `Promise<CharacterVersionInfo>` | Point `latest` at a released tag. |
| `discardDraft(expectedDraftRevisionId)` | `Promise<DiscardCharacterDraftResult>` | Reset the draft to its released parent. |
| `revert({ from, changeId, expectedDraftRevisionId })` | `Promise<RevertCharacterChangeResult>` | Undo one semantic change in the draft. |
| `fork(version, expectedDraftRevisionId?)` | `Promise<ForkCharacterVersionResult>` | Replace the draft with a released tag's contents. |
| `deprecate(version, deprecated = true)` | `Promise<CharacterVersionInfo>` | Flag or unflag a tag. Deprecated tags remain connectable. |
| `bootstrap()` | `Promise<CharacterDraftBootstrapResult>` | Create the draft for a character that predates versioning. |
| `CharacterApiError` | `Error` with `status: number`, `detail: unknown` | Rejection for any non-2xx answer from the Character API. |
