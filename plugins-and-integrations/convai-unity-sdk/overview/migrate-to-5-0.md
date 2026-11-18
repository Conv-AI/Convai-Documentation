---
title: Migrate to SDK 5.0
description: >-
  Update an existing Unity integration for the 5.0 transcript API, player
  identity, microphone policy, native audio libraries, and platform changes.
last_reviewed: "5.0.0-pre.1"
---

SDK 5.0 changes where Unity stores room settings, which APIs own a conversation, and how scenes receive replies. Open a copy of your project in source control so you can compare old prefab values and saved event bindings during the upgrade. This guide applies to the prerelease package <code class="expression">space.vars.unity_sdk_version</code>.

## Before installing the new package

In a copy of the project that still opens with the old SDK, record the values on each character and room profile and which scene or prefab uses it. Note existing local player IDs, custom chat prompts, and persistent UnityEvent listeners. For each Action Set, save its action names, parameter definitions, targets, and executor assignments. Keep that copy until you have verified a conversation and an action in the upgraded project.

If you already upgraded and an Inspector shows a missing script, open your pre-upgrade revision with its original package to recover those settings.

## Inspect saved scenes and prefabs

Copy the settings you need from old `ConvaiCharacterProfile` and `ConvaiRoomManagerProfile` assets onto the character and room components. Use prefabs for settings shared across scenes. Remove missing scripts left by `ConvaiSceneInstaller` or `ConvaiSceneMetadataCollector` after recovering their intended configuration. The manager discovers agents. For scenes with multiple players, assign the intended **Player** explicitly.

Recreate Action Set definitions in the character’s **Convai Actions** list and assign their executor references. Check existing UI and UnityEvent bindings. Older serialized field names and the old transcript relay binding do not migrate automatically. If an older project held only a plaintext API key, enter it again under **Convai > Settings > Credentials**. Follow [Scene components](../getting-started/scene-components.md) and [Validate your setup](../getting-started/validate-your-setup.md).

## Check automatic connection

Set **Connect On Start** on `ConvaiRoomManager`. It controls automatic connection for the room. The per-character **Auto Connect** switch is gone. For a user-initiated session, turn **Connect On Start** off and call `manager.ConnectAsync()` or `character.StartConversationAsync()`. Close the room with `manager.DisconnectAsync()`.

Re-enabling a character after a failed or manually closed connection leaves the room closed. Have your retry button start the connection explicitly. Use `manager.ReconnectAsync()` to reconnect with the scene settings and configured providers. If you need to supply a fresh token, a room to join, or per-connection input settings, wait for `manager.DisconnectAsync()` to finish, then call `manager.ConnectAsync(options)`. The options overload requires a room that is neither connected nor connecting. See [Session lifecycle](../core-concepts/session-lifecycle.md).

## Replace conversation and service calls

| Older integration | Migration |
| --- | --- |
| `ConnectWithAuthTokenAsync` | Put the token on `RoomSessionConnectOptions` with `SetAuthToken` and pass the options to `manager.ConnectAsync(options)`. [Connect with an auth token](../authentication/connect-with-auth-token.md) |
| Legacy or Upgraded **API Mode** and `ConvaiRestClient` | Select the client for the service you call. Review its credentials and host. [REST API clients](../scripting-reference/rest-api-client.md) |
| Standalone interaction text client | Open a room with **Allow Microphone** off and call `ConvaiPlayer.TrySendTextMessage` once the character is ready. A successful return and the player’s `OnTextMessageSent` event mean the SDK accepted the text locally. [Text-only sessions](../getting-started/run-a-text-only-session.md) |
| Character or player behavior hooks | Move project logic to a component and subscribe to the relevant events. [Extend character behavior](../advanced-topics/extend-character-behavior.md) |
| Awaiting a generic stream or chaining operations | Await the typed operation and inspect its result. [Asynchronous operations](../scripting-reference/operation-and-stream-types.md) |
| `ConvaiCharacter` narrative command shortcuts | Use the character's `NarrativeDesign` facade. [Narrative design](../features/narrative-design/README.md) |

`ConvaiPlayer.PlayerId` identifies the local player for ownership and attribution. Use an end-user identity for memory and read the identity confirmed by the service. See [Long-term memory](../features/long-term-memory/README.md).

If your 4.x code used `Characters.SetMemoryEnabledAsync`, check each character's end-user ID requirement before upgrading. That setter could reset **Optional** to **Required**. In 5.0, use the Platform client's memory settings methods and read back the saved values. [Configure memory for a character](../features/long-term-memory/configure-memory-for-a-character.md)

## Replace transcript integrations

Use `manager.Transcripts.GetEntries()` for history. Key each rendered row by entry ID and replace its text with the newest revision. A subscription can deliver several changes together. Use `SubscribeFinalized` for completed entries and `SubscribeCaptions` for live captions. A finalized entry can still be corrected. A final transcript is also distinct from the end of audio playback.

Rewire saved spoken-line listeners. Use `character.OnSpokenLine` for a character-local notification and `manager.Events` for room-wide emotion, speech, and turn events. [Migrate transcripts to 5.0](../scripting-reference/migrate-transcripts-to-5-0.md) covers the signatures and lifecycle.

## Review audio, vision, and actions

* Install the [native transport libraries](../platform-guides/native-transport-libraries.md) matching the package. The native FFI bridge is <code class="expression">space.vars.unity_native_ffi_version</code>. WebGL uses its browser transport.
* Keep the character's voice `AudioSource` separate from sound effects. Set volume per character. Choose **Allow Microphone** before connecting if the app must start without opening capture.
* Push-to-talk uses a correlated release. A source that reports audio drain can finish after sending its captured audio. On other sources, including WebGL, the SDK waits the release tail and mutes. Group conversation requires push-to-talk, a started group, and a selected member who owns the microphone route. See [Push-to-talk lifecycle](../core-concepts/push-to-talk-lifecycle.md).
* Remap lip sync to a built-in profile and the correct renderer. Replace custom profile registries with a character-specific map. See [Profiles and mappings](../getting-started/add-lip-sync/profiles-and-mappings.md).
* Recheck the [Vision frame source](../features/vision/frame-sources.md), especially which image WebGL publishes. Sending visual context and asking the character to reply are separate operations.
* Review [Actions](../features/character-actions/README.md) in the Actions Editor. Verify saved action definitions, targets, and how your behaviors handle a missing parameter or a JSON value.

## Verify the migrated project

Import the package and check that your scripts compile. Reopen saved scenes and prefabs, run **GameObject > Convai > Validate Scene Setup**, then complete a turn using each input your app offers. Test reconnect, mic denial, audio playback, transcript corrections, and any changes to the addressed character in a player build. For an IL2CPP player, use the [stripping and validation checks](../compatibility-and-requirements/platform-support-matrix.md#il2cpp-stripping-and-validation) with the stripping level you plan to ship. Test group conversation and memory against the account and service configuration you intend to deploy.

If you automate the Editor, [set up Unity CLI MCP](../ai-coding-assistant/quick-start.md) and refresh each assistant's project skill and managed instructions. Check tool names, inputs, and outputs against the [MCP tools reference](../ai-coding-assistant/mcp-tools-reference.md).
