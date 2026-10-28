---
title: What the SDK stores on the device
description: Inspect the local preference and session keys written by the default runtime, and distinguish clearing device data from deleting server records.
last_reviewed: "5.0.0-preview"
---

The default runtime uses Unity `PlayerPrefs` for runtime setting overrides and saved session identifiers. Device fallback identity also uses `PlayerPrefs`. These values are local client data, separate from server-side conversations and long-term memory.

## Keys written by the default runtime

| Key | Value |
|---|---|
| `convai.runtime.settings.v1.player_display_name` | Runtime display-name override. |
| `convai.runtime.settings.v1.transcript_enabled` | Transcript preference, stored as `1` or `0`. |
| `convai.runtime.settings.v1.notifications_enabled` | Notification preference, stored as `1` or `0`. |
| `convai.runtime.settings.v1.preferred_microphone_device_id` | Preferred microphone identifier. |
| `convai.session.<scoped storage ID>` | Saved session identifier for a character. |
| `convai.session.__keys` | Index of known character session keys. |
| `convai.end_user_id` | Persisted fallback GUID: used in the Editor and when a player device identifier is unusable. |

A null setting override removes its key. `ConvaiRuntimeSettingsStore.ClearOverrides()` removes only the four runtime preference keys and saves the store. There is no `convai.prefs.*` key family in this implementation.

## Session clearing

`KeyValueStoreSessionPersistence.ClearSession(characterId)` removes that character's cached and stored session. `ClearAllSessions()` removes known indexed sessions and the index; it does not delete unrelated preferences or device identity. These operations affect local state, not Convai's server-side records.

The default runtime constructs its own `PlayerPrefsKeyValueStore`. Standalone store constructors accept `IKeyValueStore`, but constructing a replacement does not install it into the manager. See [Custom persistence provider](custom-providers/custom-persistence-provider.md) for migration guidance.

## Credentials are separate

The saved account key belongs to `ConvaiSettings`, not these runtime preference keys. Auth tokens are resolved for connections and are not written to this store. See [Authentication](../authentication/README.md) for build stripping and token handling.

## Resume-key scope

The active room uses a hashed storage ID scoped to character, end-user identity, room/join context, and version/roster where applicable. Service origin, environment, and developer namespace add a service scope. The prefix is `convai-session-v3:` with service scope and `convai-session-v2:` otherwise, beneath `convai.session.`. A raw Character ID is not sufficient to address these entries. `ClearCharacterSessionId()` only clears the character's current value; disable resume or choose `AlwaysFresh` when a new conversation is required.
