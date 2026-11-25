---
title: What the SDK stores on the device
description: Inspect the local preference and session keys written by the default runtime, and distinguish clearing device data from deleting server records.
last_reviewed: "5.0.0-pre.1"
---

The runtime uses Unity `PlayerPrefs` for settings overrides, saved character session identifiers, and the device fallback identity.

## Keys written by the default runtime

| Key | Value |
| --- | --- |
| `convai.runtime.settings.v1.player_display_name` | Display-name override |
| `convai.runtime.settings.v1.transcript_enabled` | Transcript preference as `1` or `0` |
| `convai.runtime.settings.v1.notifications_enabled` | Notification preference as `1` or `0` |
| `convai.runtime.settings.v1.preferred_microphone_device_id` | Preferred microphone identifier |
| `convai.session.convai-session-v3:<hash>` | Scoped saved character session identifier |
| `convai.end_user_id` | Fallback ID when no usable device identifier is available and when running in the Editor |

A null settings override removes its key. `ConvaiRuntimeSettingsStore.ClearOverrides()` removes the four setting keys and saves the store.

## Session clearing and scope

The hash includes character and end-user identity, service origin, environment, application namespace, and room context, including a selected character version or roster where applicable. The active room passes this scoped ID to `KeyValueStoreSessionPersistence`. Its `ClearSession` method clears the cache and the matching local preference.

To start a fresh conversation, turn off **Resume Last Conversation** on the character or use `ResumePolicy.AlwaysFresh`. Local keys and Convai’s stored conversations and Long-Term Memory have separate lifecycles. See [Session lifecycle](../core-concepts/session-lifecycle.md).

## Credentials

The saved account key belongs to `ConvaiSettings`. Auth tokens are resolved in memory for connections. See [Authentication](../authentication/README.md) for how the build processor handles the saved key.

## Related pages

- [Runtime settings API](../ui-and-presentation/settings-panel/runtime-settings-api.md)
- [Migrate custom persistence integrations](custom-providers/custom-persistence-provider.md)
